#!/bin/zsh
# Validación del material en la app (Playwright). Por defecto solo Chromium: para cambios de contenido
# basta un navegador; usar NAVEGADORES=todos ante cambios de código de la interfaz o al cerrar una etapa.
# Uso: scripts/qa/validar_material.sh ["1° básico" ...]   (sin argumentos: los 12 cursos)
source ${0:A:h}/entorno.sh
cd $RAIZ_QA/frontend
PROY=(--project=chromium); [[ $NAVEGADORES == todos ]] && PROY=()
if [[ $# -eq 0 ]]; then
  npx playwright test validacion-integral-material $PROY --reporter=line --output=/tmp/logos-pw 2>&1 | grep -E "passed|failed|flaky|Error:" | head -40
else
  for N in "$@"; do echo "$N: $(LOGOS_VALIDAR_NIVEL="$N" npx playwright test validacion-integral-material $PROY --reporter=line --output=/tmp/logos-pw 2>&1 | grep -E "passed|failed" | tr '\n' ' ')"; done
fi
