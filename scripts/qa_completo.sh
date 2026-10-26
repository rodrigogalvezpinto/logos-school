#!/usr/bin/env bash
# QA completo de Logos School — un solo comando, un solo reporte.
#
# Corre, en orden, todo lo que hoy hay que acordarse de correr a mano:
#   1. Backend: pytest completo (incluye la matriz de permisos automática,
#      test_matriz_permisos.py, que detecta endpoints sin autenticación sin que
#      nadie tenga que acordarse de agregar un caso a mano).
#   2. Frontend: build de producción (atrapa errores de compilación/tipos).
#   3. Frontend: suite completa de Playwright E2E (flujos reales de Alumno,
#      Apoderado, Admin y Profesor, con el backend real).
#
# Requiere: backend (uvicorn) y frontend (ng serve) corriendo en las URLs de
# desarrollo de siempre (localhost:8000 y localhost:4300) — este script NO los
# levanta, porque en desarrollo normalmente ya están corriendo con --reload y
# reiniciarlos cortaría ese flujo. Ver planificacion/26-qa-sistema-automatizado.md.
#
# Uso: ./scripts/qa_completo.sh
# Código de salida: 0 si todo pasó, 1 si algo falló (para usar en CI más adelante).

set -uo pipefail
cd "$(dirname "${BASH_SOURCE[0]}")/.."

ROJO='\033[0;31m'
VERDE='\033[0;32m'
AMARILLO='\033[1;33m'
SIN_COLOR='\033[0m'

HAY_FALLOS=0
RESUMEN=()

paso() {
  echo ""
  echo -e "${AMARILLO}▶ $1${SIN_COLOR}"
}

ok() {
  RESUMEN+=("${VERDE}✔${SIN_COLOR} $1")
}

falla() {
  RESUMEN+=("${ROJO}✘${SIN_COLOR} $1")
  HAY_FALLOS=1
}

# --- 1. Backend: pytest completo ---
paso "Backend: pytest completo (incluye matriz de permisos automática)"
if (cd backend && uv run pytest -q); then
  ok "Backend: pytest completo"
else
  falla "Backend: pytest completo — revisa el detalle arriba"
fi

# --- 2. Frontend: build ---
paso "Frontend: build de producción"
if (cd frontend && npx ng build --configuration development > /tmp/logos_qa_build.log 2>&1); then
  ok "Frontend: build"
else
  falla "Frontend: build — ver /tmp/logos_qa_build.log"
fi

# --- 3. Frontend: E2E ---
paso "Frontend: suite Playwright E2E completa (backend real, --workers=1)"
if (cd frontend && npx playwright test --workers=1); then
  ok "Frontend: Playwright E2E"
else
  falla "Frontend: Playwright E2E — revisa el detalle arriba o 'npx playwright show-report'"
fi

# --- 4. Control de calidad de contenido (Fase 1, ítem 2.5.1) ---
paso "Contenido: control de calidad estructural (rango/dificultad/asignatura)"
if (cd backend && uv run python scripts/validar_calidad_contenido.py); then
  ok "Contenido: control de calidad"
else
  falla "Contenido: control de calidad — hallazgos reales en el banco de preguntas, no bloquean el resto del QA (ver planificacion/27-plan-incorporacion-hallazgos-brincus.md, ítem 2.5.1)"
fi

# --- Resumen ---
echo ""
echo "═══════════════════════════════════════════"
echo "  RESUMEN — QA completo de Logos School"
echo "═══════════════════════════════════════════"
for linea in "${RESUMEN[@]}"; do
  echo -e "  $linea"
done
echo ""

if [ "$HAY_FALLOS" -eq 0 ]; then
  echo -e "${VERDE}Todo verde. No se detectaron regresiones.${SIN_COLOR}"
else
  echo -e "${ROJO}Hay al menos un fallo — revisa el detalle arriba antes de dar por buena la sesión.${SIN_COLOR}"
fi

exit "$HAY_FALLOS"
