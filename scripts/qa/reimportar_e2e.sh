#!/bin/zsh
# Recrea logos_e2e_alternativas desde contenido/, siembra datos, exporta el fixture E2E y reinicia la API en 8001.
set -e
source ${0:A:h}/entorno.sh
cd $RAIZ_QA/backend
pkill -f "uvicorn app.main:app --port 8001" 2>/dev/null || true
ADMIN=${E2E_DATABASE_URL%/*}/postgres
psql "$ADMIN" -q -c "DROP DATABASE IF EXISTS logos_e2e_alternativas WITH (FORCE);" -c "CREATE DATABASE logos_e2e_alternativas;"
export DATABASE_URL=$E2E_DATABASE_URL
.venv/bin/alembic upgrade head >/dev/null 2>&1 || true
.venv/bin/python scripts/importar_contenido.py > /tmp/logos-import.log 2>&1 || { echo "falló importar (ver /tmp/logos-import.log)"; exit 1; }
for s in sembrar_planes datos_de_prueba seed_plan_lector seed_utiles_escolares; do .venv/bin/python scripts/$s.py >/dev/null 2>&1 || echo "falló $s"; done
.venv/bin/python scripts/exportar_fixture_validacion_e2e.py ../frontend/e2e/fixtures/material-validacion.json
RESEND_API_KEY= nohup .venv/bin/uvicorn app.main:app --port 8001 > /tmp/logos-api8001.log 2>&1 &
for i in {1..30}; do curl -s -o /dev/null localhost:8001/docs && break; sleep 1; done
curl -s -o /dev/null -w "api %{http_code}\n" localhost:8001/docs
psql "$E2E_DATABASE_URL" -Atc "select 'preguntas sin OA: ' || count(*) filter (where oa_id is null) || ' de ' || count(*) from pregunta"
