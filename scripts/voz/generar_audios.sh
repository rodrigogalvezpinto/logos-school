#!/bin/zsh
# Pregraba la lectura en voz alta (guías y preguntas) con Piper, sin costo y sin servicios externos.
# Uso: DATABASE_URL=... scripts/voz/generar_audios.sh ["1° básico" "2° básico" ...]
# Salida: frontend/public/audio/es/<clave>.m4a + manifest.json (no versionados: ver .gitignore).
# Primera vez: crea un entorno en ~/.cache/logos-voz y descarga el modelo (≈63 MB).
set -e
RAIZ=${0:A:h:h:h}
CACHE=$HOME/.cache/logos-voz
NIVELES=("$@")
[[ $# -eq 0 ]] && NIVELES=("1° básico" "2° básico")
MODELO=$CACHE/es_MX-claude-high.onnx
if [[ ! -x $CACHE/venv/bin/python ]]; then
  mkdir -p $CACHE && uv venv -q -p 3.11 $CACHE/venv && uv pip install -q -p $CACHE/venv "piper-tts==1.8.0" numpy
fi
if [[ ! -f $MODELO ]]; then
  B=https://huggingface.co/rhasspy/piper-voices/resolve/main/es/es_MX/claude/high/es_MX-claude-high
  curl -sfL -o $MODELO $B.onnx && curl -sfL -o $MODELO.json $B.onnx.json
fi
# espeak-ng no acepta rutas largas: se usa un enlace corto al directorio de datos de Piper.
ESPEAK=$(print -r -- $CACHE/venv/lib/python3.11/site-packages/piper/espeak-ng-data)
ln -sfn $ESPEAK /tmp/logos-espeak
TMP=$(mktemp -d)
(cd $RAIZ/backend && .venv/bin/python scripts/exportar_textos_voz.py $TMP/fuente.json "${NIVELES[@]}")
(cd $RAIZ/frontend && npx esbuild tools/textos-voz.ts --bundle --platform=node --format=esm --outfile=$TMP/textos-voz.mjs --log-level=error \
  && node $TMP/textos-voz.mjs $TMP/fuente.json $TMP/textos.json)
$CACHE/venv/bin/python -I $RAIZ/scripts/voz/generar_audios.py $TMP/textos.json $MODELO /tmp/logos-espeak $RAIZ/frontend/public/audio/es
rm -rf $TMP
