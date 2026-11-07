#!/bin/zsh
# Compila el frontend apuntando a la API E2E (8001) y lo sirve en 4300.
set -e
RAIZ=${0:A:h:h:h}
cd $RAIZ/frontend
npx ng build --configuration development --define "LOGOS_API_URL='http://localhost:8001'" 2>&1 | grep -iE "error|Output" || true
pkill -f "servir_spa.mjs" 2>/dev/null || true
nohup node $RAIZ/scripts/qa/servir_spa.mjs dist/frontend/browser 4300 > /tmp/logos-spa4300.log 2>&1 &
sleep 1; curl -s -o /dev/null -w "spa %{http_code}\n" localhost:4300/
