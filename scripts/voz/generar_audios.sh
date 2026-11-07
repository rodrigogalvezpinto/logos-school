#!/bin/zsh
# Pregraba la lectura en voz alta (guías y preguntas) con Kokoro (voz em_alex), sin costo y sin servicios externos.
# Uso: DATABASE_URL=... scripts/voz/generar_audios.sh ["1° básico" … ] (por defecto, 1° a 4° básico: régimen A)
# Salida: frontend/public/audio/es/<clave>.m4a + manifest.json (no versionados: ver .gitignore).
# Primera vez: crea un entorno en ~/.cache/logos-voz y descarga el modelo (≈350 MB).
set -e
RAIZ=${0:A:h:h:h}
CACHE=$HOME/.cache/logos-voz
NIVELES=("$@")
[[ $# -eq 0 ]] && NIVELES=("1° básico" "2° básico" "3° básico" "4° básico")
MODELO=$CACHE/kokoro-v1.0.onnx
VOCES=$CACHE/voices-v1.0.bin
if [[ ! -x $CACHE/venv/bin/python ]] || ! $CACHE/venv/bin/python -c "import kokoro_onnx" 2>/dev/null; then
  mkdir -p $CACHE && uv venv -q -p 3.11 --allow-existing $CACHE/venv && uv pip install -q -p $CACHE/venv "kokoro-onnx==0.6.1" numpy
fi
B=https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0
[[ -f $MODELO ]] || curl -sfL -o $MODELO $B/kokoro-v1.0.onnx
[[ -f $VOCES ]] || curl -sfL -o $VOCES $B/voices-v1.0.bin
TMP=$(mktemp -d)
(cd $RAIZ/backend && .venv/bin/python scripts/exportar_textos_voz.py $TMP/fuente.json "${NIVELES[@]}")
(cd $RAIZ/frontend && npx esbuild tools/textos-voz.ts --bundle --platform=node --format=esm --outfile=$TMP/textos-voz.mjs --log-level=error \
  && node $TMP/textos-voz.mjs $TMP/fuente.json $TMP/textos.json)
# Kokoro (onnxruntime) usa todos los núcleos y satura el Mac: se limita a la mitad.
HILOS=$(( $(sysctl -n hw.ncpu 2>/dev/null || nproc) / 2 ))
OMP_NUM_THREADS=$HILOS ORT_NUM_THREADS=$HILOS $CACHE/venv/bin/python -I $RAIZ/scripts/voz/generar_audios.py $TMP/textos.json $MODELO $VOCES $RAIZ/frontend/public/audio/es
rm -rf $TMP
