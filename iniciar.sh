#!/usr/bin/env bash
set -e

# ==============================================================================
# Logos School - Script de Inicio Rápido y Guía de Acceso
# ==============================================================================

DIR_RAIZ="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$DIR_RAIZ"

VERDE="\033[1;32m"
AZUL="\033[1;34m"
AMARILLO="\033[1;33m"
CYAN="\033[1;36m"
ROJO="\033[1;31m"
BOLD="\033[1m"
RESET="\033[0m"

echo -e "${AZUL}${BOLD}======================================================================${RESET}"
echo -e "${AZUL}${BOLD}               🚀 INICIANDO LOGOS SCHOOL                              ${RESET}"
echo -e "${AZUL}${BOLD}======================================================================${RESET}"

# Verificar si PostgreSQL está respondiendo
if ! pg_isready -h localhost -p 5432 >/dev/null 2>&1; then
  echo -e "${ROJO}⚠️  PostgreSQL no responde en localhost:5432.${RESET}"
  echo -e "   Por favor asegúrate de iniciar el servicio de PostgreSQL antes de continuar."
  exit 1
fi

PID_BACKEND=""
PID_FRONTEND=""

cleanup() {
  echo -e "\n${AMARILLO}🛑 Deteniendo servicios de Logos School...${RESET}"
  if [ -n "$PID_BACKEND" ]; then
    kill "$PID_BACKEND" 2>/dev/null || true
  fi
  if [ -n "$PID_FRONTEND" ]; then
    kill "$PID_FRONTEND" 2>/dev/null || true
  fi
  echo -e "${VERDE}✅ Servicios detenidos correctamente.${RESET}"
  exit 0
}

trap cleanup SIGINT SIGTERM

# 1. Iniciar Backend (FastAPI en puerto 8000)
if lsof -ti:8000 >/dev/null 2>&1; then
  echo -e "${VERDE}✔ Backend ya está corriendo en http://localhost:8000${RESET}"
else
  echo -e "${CYAN}▶ Iniciando Backend FastAPI (puerto 8000)...${RESET}"
  cd "$DIR_RAIZ/backend"
  .venv/bin/uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload >/dev/null 2>&1 &
  PID_BACKEND=$!
  cd "$DIR_RAIZ"

  echo -n "   Esperando que el backend responda..."
  until curl -s http://localhost:8000/docs >/dev/null 2>&1; do
    echo -n "."
    sleep 1
  done
  echo -e " ${VERDE}¡Listo!${RESET}"
fi

# 2. Iniciar Frontend (Angular en puerto 4200)
if lsof -ti:4200 >/dev/null 2>&1; then
  echo -e "${VERDE}✔ Frontend ya está corriendo en http://localhost:4200${RESET}"
else
  echo -e "${CYAN}▶ Iniciando Frontend Angular (puerto 4200)...${RESET}"
  cd "$DIR_RAIZ/frontend"
  npm start >/dev/null 2>&1 &
  PID_FRONTEND=$!
  cd "$DIR_RAIZ"

  echo -n "   Esperando que el frontend compile y responda..."
  until curl -s http://localhost:4200/ >/dev/null 2>&1; do
    echo -n "."
    sleep 2
  done
  echo -e " ${VERDE}¡Listo!${RESET}"
fi

# Banner con credenciales y accesos
echo ""
echo -e "${VERDE}${BOLD}======================================================================${RESET}"
echo -e "${VERDE}${BOLD}       ✨ PLATAFORMA LISTA PARA PROBAR - ACCESOS Y CREDENCIALES       ${RESET}"
echo -e "${VERDE}${BOLD}======================================================================${RESET}"
echo ""
echo -e "  🌐 ${BOLD}Aplicación Web:${RESET}       ${CYAN}http://localhost:4200${RESET}"
echo -e "  📚 ${BOLD}Documentación API:${RESET}    ${CYAN}http://localhost:8000/docs${RESET}"
echo ""
echo -e "${AZUL}${BOLD}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${RESET}"
echo -e "${AZUL}${BOLD} 1. CUENTA FAMILIAR (ALUMNO Y APODERADO - RECOMENDADA)                 ${RESET}"
echo -e "${AZUL}${BOLD}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${RESET}"
echo -e "  🔗 ${BOLD}URL de Login:${RESET}   http://localhost:4200/login"
echo -e "  📧 ${BOLD}Email:${RESET}          ${VERDE}apoderado.prueba@logos.cl${RESET}"
echo -e "  🔑 ${BOLD}Contraseña:${RESET}     ${VERDE}Logos2026!${RESET}"
echo ""
echo -e "  ${BOLD}Al ingresar tendrás acceso inmediato a:${RESET}"
echo -e "   • ${CYAN}Sofía (4° Básico):${RESET} Alumna con historial de notas, insignias, XP ganado,"
echo -e "     guías completadas, plan lector, útiles escolares y evaluaciones sumativas."
echo -e "   • ${CYAN}Mateo (6° Básico):${RESET} Alumno con asignatura de Inglés y formato de 25 preguntas."
echo -e "   • ${CYAN}Panel Apoderado:${RESET} Coaching para padres, descarga de Informe de Avance PDF,"
echo -e "     Certificado de Alumno Regular oficial en PDF y gestión familiar."
echo ""
echo -e "${AZUL}${BOLD}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${RESET}"
echo -e "${AZUL}${BOLD} 2. CUENTA PROFESOR                                                    ${RESET}"
echo -e "${AZUL}${BOLD}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${RESET}"
echo -e "  🔗 ${BOLD}URL de Login:${RESET}   http://localhost:4200/profesor/login"
echo -e "  📧 ${BOLD}Email:${RESET}          ${VERDE}profesor.prueba@logos.cl${RESET}"
echo -e "  🔑 ${BOLD}Contraseña:${RESET}     ${VERDE}ProfesorLogos2026!${RESET}"
echo -e "  📋 ${BOLD}Funciones:${RESET}      Creación y gestión de cursos, notas y comunicados."
echo ""
echo -e "${AZUL}${BOLD}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${RESET}"
echo -e "${AZUL}${BOLD} 3. CUENTA ADMINISTRADOR                                               ${RESET}"
echo -e "${AZUL}${BOLD}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${RESET}"
echo -e "  🔗 ${BOLD}URL de Login:${RESET}   http://localhost:4200/admin/login"
echo -e "  📧 ${BOLD}Email:${RESET}          ${VERDE}admin.prueba@logos.cl${RESET}"
echo -e "  🔑 ${BOLD}Contraseña:${RESET}     ${VERDE}AdminLogos2026!${RESET}"
echo -e "  📊 ${BOLD}Funciones:${RESET}      Métricas globales, planes, aprobación de profesores."
echo ""
echo -e "${AZUL}${BOLD}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${RESET}"
echo -e "${AZUL}${BOLD} 4. REGISTRO DESDE CERO (NUEVA FAMILIA)                               ${RESET}"
echo -e "${AZUL}${BOLD}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${RESET}"
echo -e "  🔗 ${BOLD}URL:${RESET}            http://localhost:4200/registro"
echo -e "  💡 ${BOLD}RUTs de prueba:${RESET} 21.345.678-4  |  19.876.543-2  |  20.987.654-K"
echo ""
echo -e "${AMARILLO}💡 Para detener los servicios presiona Ctrl+C en esta terminal.${RESET}"
echo -e "${VERDE}${BOLD}======================================================================${RESET}"

# Si lanzamos procesos en segundo plano, esperamos que terminen con el trap
if [ -n "$PID_BACKEND" ] || [ -n "$PID_FRONTEND" ]; then
  wait
else
  # Si ya estaban corriendo externamente, dejamos un bucle esperando Ctrl+C
  while true; do
    sleep 2
  done
fi
