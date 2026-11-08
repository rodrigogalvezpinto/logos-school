"""Escribe en el frontmatter de cada prueba de unidad un `oa_por_pregunta` completo (C.2, Fase 1).

Por qué: varias pruebas no declaraban el OA de cada pregunta; el importador lo deducía buscando la
misma pregunta en la guía. Al reescribir una pregunta copiada (C.2), esa deducción falla y la pregunta
quedaría sin OA. Este script resuelve el OA exactamente como el importador (mismo parser, mismo banco de
la guía) y lo deja explícito, para que la reescritura no cambie el OA.

Uso: python scripts/fijar_oa_pruebas.py [carpeta-curso ...] [--escribir]   (por defecto, los 12; sin
--escribir solo informa). No toca preguntas ni pautas: solo la línea `oa_por_pregunta`.
"""
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from importar_contenido import _asignatura_por_archivo, _indexar_banco, _resolver_oa_pregunta  # noqa: E402
from parser_contenido import parsear_guia  # noqa: E402
from parser_prueba_examen import parsear_prueba_o_examen  # noqa: E402

CONTENIDO = Path(__file__).resolve().parents[2] / "contenido"


def valor(identidad: tuple[str | None, str]) -> str:
    modulo, codigo = identidad
    return f"{codigo} (Mód. {modulo})" if modulo else codigo


def procesar_curso(curso: Path, escribir: bool) -> list[str]:
    guias = {g.stem: parsear_guia(g.read_text(encoding="utf-8")) for g in curso.glob("*.md")
             if not g.name.startswith("00")}
    avisos = []
    for ruta in sorted((curso / "pruebas").glob("*.md")):
        slug = _asignatura_por_archivo(ruta.stem, list(guias))
        if not slug:
            avisos.append(f"{ruta.name}: sin guía asociada")
            continue
        objetivos = guias[slug]
        mapa = {(o.modulo, o.codigo_oficial): (o.modulo, o.codigo_oficial) for o in objetivos}
        banco = _indexar_banco(objetivos)
        texto = ruta.read_text(encoding="utf-8")
        oa = {}
        for pregunta, pauta in parsear_prueba_o_examen(texto):
            identidad = _resolver_oa_pregunta(pregunta, pauta, mapa, banco)
            if identidad is None:
                avisos.append(f"{ruta.name}: pregunta {pregunta.numero} sin OA resoluble")
                continue
            oa[str(pregunta.numero)] = valor(identidad)
        linea = "oa_por_pregunta: " + json.dumps(oa, ensure_ascii=False, separators=(",", ":"))
        fm = re.match(r"---[ \t]*\n(.*?)\n---[ \t]*\n", texto, re.S)
        if not fm:
            nuevo = f"---\n{linea}\n---\n\n" + texto
        elif re.search(r"(?m)^oa_por_pregunta[ \t]*:.*$", fm.group(1)):
            nuevo = texto[:fm.start(1)] + re.sub(r"(?m)^oa_por_pregunta[ \t]*:.*$", lambda _m: linea, fm.group(1)) + texto[fm.end(1):]
        else:
            nuevo = texto[:fm.end(1)] + "\n" + linea + texto[fm.end(1):]
        if nuevo != texto and escribir:
            ruta.write_text(nuevo, encoding="utf-8")
    return avisos


def main() -> None:
    escribir = "--escribir" in sys.argv
    cursos = [CONTENIDO / c for c in sys.argv[1:] if not c.startswith("--")] or sorted(
        p for p in CONTENIDO.iterdir() if p.is_dir() and (p / "pruebas").exists())
    for curso in cursos:
        for aviso in procesar_curso(curso, escribir):
            print(f"{curso.name}: {aviso}")
    print("escrito" if escribir else "solo lectura (usar --escribir)")


if __name__ == "__main__":
    main()
