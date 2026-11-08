"""Reemplaza preguntas completas de un simulacro (bloque «**N.** … ---» y su fila «| N | … |» de la
pauta) a partir de un archivo JSON. Corrección C.1 de la Fase 1: simulacros independientes de la guía.

JSON: {"archivo": "contenido/…/examen-….md",
       "preguntas": {"4": {"bloque": "**4.** …\\n\\na) …\\n", "pauta": "| 4 | Ciencias Naturales | **a) …** … | OA 1 — … |"}}}
Uso: python scripts/reemplazar_pregunta_simulacro.py cambios.json
Verifica que cada bloque y cada fila existan una sola vez; si algo no cuadra, no escribe.
"""
import json
import re
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[2]


def main() -> None:
    cambios = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
    ruta = RAIZ / cambios["archivo"]
    texto = ruta.read_text(encoding="utf-8")
    for n, c in cambios["preguntas"].items():
        # El bloque termina en la pregunta siguiente, en un separador «---» o en un encabezado.
        bloque = re.compile(rf"^\*\*(?:Pregunta )?{n}[.* ].*?(?=^\*\*(?:Pregunta )?\d+[.* ]|^---$|^#)", re.S | re.M)
        hallados = bloque.findall(texto)
        if len(hallados) != 1:
            sys.exit(f"pregunta {n}: se esperaba 1 bloque y hay {len(hallados)}")
        texto = bloque.sub(lambda _m: c["bloque"].rstrip("\n") + "\n\n", texto, count=1)
        fila = re.compile(rf"^\| {n} \|.*$", re.M)
        if len(fila.findall(texto)) != 1:
            sys.exit(f"pauta {n}: se esperaba 1 fila")
        texto = fila.sub(lambda _m: c["pauta"], texto, count=1)
    ruta.write_text(texto, encoding="utf-8")
    print(f"{len(cambios['preguntas'])} preguntas reemplazadas en {ruta.relative_to(RAIZ)}")


if __name__ == "__main__":
    main()
