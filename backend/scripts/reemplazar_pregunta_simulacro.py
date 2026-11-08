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
        # También termina en un estímulo compartido («*(Lee el cuento… preguntas 5 a 8)*», «**Texto A**»):
        # sin este corte, el estímulo de las preguntas siguientes se borraba junto con la pregunta (2026-11-08).
        bloque = re.compile(
            rf"^\*\*(?:Pregunta )?{n}[.* ].*?(?=^\*\*(?:Pregunta )?\d+[.* ]|^---$|^#"
            rf"|^\*{{0,2}}\(?[ \t]*(?:Lee|Lea|Observa|Utiliza|Usa|Vuelve a leer)\b|^\*\*Texto\b)", re.S | re.M)
        # Las preguntas se buscan solo antes de la pauta: «**1.** b) …» de la pauta parece una pregunta.
        m_pauta = re.search(r"(?m)^#{1,6}\s*Pauta|^\*\*Pauta", texto)
        corte = m_pauta.start() if m_pauta else len(texto)
        hallados = bloque.findall(texto[:corte])
        if len(hallados) != 1:
            sys.exit(f"pregunta {n}: se esperaba 1 bloque y hay {len(hallados)}")
        # Seguro: no perder texto citado, imágenes ni marcadores que el bloque nuevo no traiga.
        perdidas = [l for l in hallados[0].splitlines() if re.match(r"\s*(>|\[Imagen|::)", l) and l.strip() not in c["bloque"]]
        if perdidas and not cambios.get("forzar"):
            sys.exit(f"pregunta {n}: el bloque reemplazado contiene estímulo que se perdería: {perdidas[0][:80]!r}")
        texto = bloque.sub(lambda _m: c["bloque"].rstrip("\n") + "\n\n", texto[:corte], count=1) + texto[corte:]
        fila = re.compile(rf"^\| {n} +\|.*$", re.M)  # algunas pautas alinean con «| 6  |»
        if len(fila.findall(texto)) == 1:
            texto = fila.sub(lambda _m: c["pauta"], texto, count=1)
            continue
        # Pruebas de unidad: pauta en lista («1. **d) …**», «**4.** a) …») después del título «Pauta».
        inicio = texto.find("Pauta")
        if inicio < 0:
            sys.exit(f"pauta {n}: no hay fila de tabla ni sección «Pauta»")
        # La línea de pauta puede seguir en líneas sangradas: se reemplazan también (2026-11-08).
        item = re.compile(rf"^(?:\*\*{n}\.\*\*|{n}\.) .*$(?:\n {{2,}}\S.*$)*", re.M)
        cola = texto[inicio:]
        if len(item.findall(cola)) != 1:
            sys.exit(f"pauta {n}: se esperaba 1 línea en la pauta")
        texto = texto[:inicio] + item.sub(lambda _m: c["pauta"], cola, count=1)
    ruta.write_text(texto, encoding="utf-8")
    print(f"{len(cambios['preguntas'])} preguntas reemplazadas en {ruta.relative_to(RAIZ)}")


if __name__ == "__main__":
    main()
