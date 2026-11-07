# Entorno de verificación aislado (no toca logos_qa): base logos_e2e_alternativas, API 8001, SPA 4300.
# Se carga con `source scripts/qa/entorno.sh`. Toma usuario y clave del backend/.env local.
RAIZ_QA=${${(%):-%x}:A:h:h:h}
BASE_DEV=$(grep '^DATABASE_URL=' $RAIZ_QA/backend/.env | cut -d= -f2-)
export E2E_DATABASE_URL=${BASE_DEV%/*}/logos_e2e_alternativas
export LOGOS_E2E_WEB_URL=http://localhost:4300
export LOGOS_E2E_API_URL=http://localhost:8001
