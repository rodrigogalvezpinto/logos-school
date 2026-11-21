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
# Con login de Google, el CSP debe permitir su script, su botón (iframe) y su hoja de estilos
# (lista oficial de Google Identity Services). Sin Client ID el CSP queda cerrado a 'self'.
if [[ -n ${LOGOS_GOOGLE_CLIENT_ID:-} ]]; then
  GSI=https://accounts.google.com/gsi/
  sed -i '' -E "s#script-src 'self'#script-src 'self' ${GSI}client#; s#style-src 'self'#style-src 'self' ${GSI}style#; s#(connect-src [^;]*)#\1 $GSI#; s#frame-ancestors#frame-src $GSI; frame-ancestors#" $SALIDA/_headers
  echo "CSP: se agregó Google Identity Services"
fi
grep "Content-Security-Policy" $SALIDA/_headers
npx wrangler pages deploy $SALIDA --project-name "$PROYECTO" --branch main
