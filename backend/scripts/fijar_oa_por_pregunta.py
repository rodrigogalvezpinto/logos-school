"""Fija en el frontmatter (`oa_por_pregunta`) el OA de cada pregunta de prueba de unidad.

En 1.º a 4.º básico, varias pruebas no declaraban el OA de cada pregunta: el importador lo
deducía buscando la MISMA pregunta (texto idéntico) en el banco de la guía. Al convertir las
preguntas abiertas a alternativas (decisión 2026-11-06) los textos de guía y prueba dejan de
ser idénticos, y esa deducción se pierde. Este script resuelve el OA con los textos de una
referencia git anterior (por defecto e6336af, antes de la conversión) y lo declara de forma
explícita cuando la resolución actual se perdió o cambió. Nunca inventa un OA: solo copia la
asociación que la versión anterior ya producía.

Uso: python backend/scripts/fijar_oa_por_pregunta.py <carpeta-curso> [ref_git]
"""

import json
import re
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from importar_contenido import (  # noqa: E402
    CONTENIDO_DIR,
    CURSOS,
    _asignatura_por_archivo,
    _indexar_banco,
    _resolver_oa_pregunta,
)
from parser_contenido import parsear_guia  # noqa: E402
from parser_prueba_examen import parsear_prueba_o_examen  # noqa: E402

RAIZ = CONTENIDO_DIR.parent


def _git_show(ref: str, ruta: Path) -> str | None:
    try:
        return subprocess.check_output(
            ["git", "show", f"{ref}:{ruta.relative_to(RAIZ)}"], cwd=RAIZ, text=True, stderr=subprocess.DEVNULL
        )
    except subprocess.CalledProcessError:
        return None


def _resolver(texto_prueba: str, texto_guia: str) -> dict[int, str | None]:
    objetivos = parsear_guia(texto_guia)
    ids = {(oa.modulo, oa.codigo_oficial): i for i, oa in enumerate(objetivos)}
    inverso = {i: (modulo, codigo) for (modulo, codigo), i in ids.items()}
    banco = _indexar_banco(objetivos)
    resultado = {}
    for pregunta, pauta in parsear_prueba_o_examen(texto_prueba):
        oa_id = _resolver_oa_pregunta(pregunta, pauta, ids, banco)
        if oa_id is None:
            resultado[pregunta.numero] = None
        else:
            modulo, codigo = inverso[oa_id]
            resultado[pregunta.numero] = f"{codigo} (Módulo {modulo})" if modulo else codigo
    return resultado


def _escribir_mapa(texto: str, nuevos: dict[int, str]) -> str:
    frontmatter = re.match(r"\s*---[ \t]*\n(.*?)\n---(?:\n|$)", texto, re.DOTALL)
    if not frontmatter:
        raise SystemExit("La prueba no tiene frontmatter: no se puede declarar oa_por_pregunta")
    cuerpo = frontmatter.group(1)
    linea = re.search(r"(?m)^oa_por_pregunta[ \t]*:[ \t]*(.*)$", cuerpo)
    mapa = dict(json.loads(linea.group(1))) if linea else {}
    for numero, codigo in nuevos.items():
        mapa[str(numero)] = codigo
    ordenado = {k: mapa[k] for k in sorted(mapa, key=int)}
    nueva_linea = "oa_por_pregunta: " + json.dumps(ordenado, ensure_ascii=False, separators=(",", ":"))
    if linea:
        cuerpo_nuevo = cuerpo[:linea.start()] + nueva_linea + cuerpo[linea.end():]
    else:
        cuerpo_nuevo = cuerpo + "\n" + nueva_linea
    inicio, fin = frontmatter.span(1)
    return texto[:inicio] + cuerpo_nuevo + texto[fin:]


def main() -> None:
    carpeta = sys.argv[1]
    ref = sys.argv[2] if len(sys.argv) > 2 else "e6336af"
    curso = next(c for c in CURSOS if c["carpeta"] == carpeta)
    slugs = [slug for slug, _ in curso["asignaturas"]]
    for ruta in sorted((CONTENIDO_DIR / carpeta / "pruebas").glob("*.md")):
        slug = _asignatura_por_archivo(ruta.stem, slugs)
        guia = CONTENIDO_DIR / carpeta / f"{slug}.md"
        texto_actual = ruta.read_text(encoding="utf-8")
        anterior_prueba, anterior_guia = _git_show(ref, ruta), _git_show(ref, guia)
        if anterior_prueba is None or anterior_guia is None:
            print(f"{ruta.name}: sin versión en {ref}, se omite")
            continue
        antes = _resolver(anterior_prueba, anterior_guia)
        ahora = _resolver(texto_actual, guia.read_text(encoding="utf-8"))
        nuevos = {n: c for n, c in antes.items() if c and ahora.get(n) != c}
        if nuevos:
            ruta.write_text(_escribir_mapa(texto_actual, nuevos), encoding="utf-8")
            ahora = _resolver(ruta.read_text(encoding="utf-8"), guia.read_text(encoding="utf-8"))
        perdidas = [n for n, c in antes.items() if c and ahora.get(n) != c]
        sin_oa = [n for n, c in ahora.items() if c is None]
        estado = "OK" if not perdidas else f"DIFERENCIAS {perdidas}"
        print(f"{estado} {ruta.relative_to(RAIZ)}: fijadas {sorted(nuevos)}; sin OA {sin_oa}")


if __name__ == "__main__":
    main()
