"""Inserta un bloque de texto antes de «#### Preguntas de autoevaluación» (o del marcador dado) del OA indicado.
Uso: insertar.py <archivo> "<encabezado OA exacto o prefijo>" <archivo_bloque> [marcador]"""
import sys
arch, oa, bloque = sys.argv[1:4]
marca = sys.argv[4] if len(sys.argv) > 4 else "#### Preguntas de autoevaluación"
s = open(arch, encoding="utf-8").read()
i = s.index(oa)
j = s.index(marca, i)
nuevo = open(bloque, encoding="utf-8").read().strip("\n") + "\n\n"
if nuevo.strip()[:60] in s:
    sys.exit("ya insertado")
open(arch, "w", encoding="utf-8").write(s[:j] + nuevo + s[j:])
print("ok", arch, oa)
