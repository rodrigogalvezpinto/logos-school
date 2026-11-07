#!/bin/zsh
# Compila y publica el frontend en Cloudflare Pages por «carga directa» desde este Mac, incluyendo los
# audios pregrabados (no versionados). No se ejecuta solo: requiere `npx wrangler login` una vez.
# Uso: LOGOS_API_URL=https://api.tu-dominio.cl [LOGOS_GOOGLE_CLIENT_ID=…] scripts/desplegar/frontend.sh [proyecto-pages]
set -e
RAIZ=${0:A:h:h:h}
PROYECTO=${1:-logos-school}
: ${LOGOS_API_URL:?Falta LOGOS_API_URL (URL pública del backend en Render)}
ORIGEN_API=$(print -r -- $LOGOS_API_URL | sed -E 's#^(https?://[^/]+).*#\1#')
cd $RAIZ/frontend
[[ -f public/audio/es/manifest.json ]] || echo "⚠️  Sin audios pregrabados: se usará la voz del dispositivo (ver scripts/voz/generar_audios.sh)."
npx ng build --configuration production \
  --define "LOGOS_API_URL='$LOGOS_API_URL'" \
  --define "LOGOS_GOOGLE_CLIENT_ID='${LOGOS_GOOGLE_CLIENT_ID:-}'"
SALIDA=dist/frontend/browser
# El CSP de _headers trae el dominio de ejemplo: se reemplaza por el real del backend.
sed -i '' "s#https://api.logos.cl#$ORIGEN_API#g" $SALIDA/_headers
grep -q "$ORIGEN_API" $SALIDA/_headers && echo "CSP connect-src → $ORIGEN_API"
npx wrangler pages deploy $SALIDA --project-name "$PROYECTO" --branch main
