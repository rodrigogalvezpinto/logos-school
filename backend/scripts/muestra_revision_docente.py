"""Genera la muestra de preguntas para la revisión docente (auditoría Fase 1, 2026-11-15).

Por qué: los validadores automáticos comprueban formato, claves y que la prueba no copie la guía, pero no
pueden juzgar si una pregunta es pedagógicamente buena. Un profesor revisa una muestra por curso; si la
muestra sale bien, aumenta la confianza en el resto; si sale mal, indica dónde mirar.

La muestra es estratificada (se reparte entre asignaturas y entre guía, prueba de unidad y simulacro) y
reproducible (semilla fija por curso): volver a generarla da las mismas preguntas mientras el material no
cambie.

Uso: python scripts/muestra_revision_docente.py [--por-curso 25]
Escribe docs/auditorias/fase1/muestra-docente/NN-curso.md (uno por curso).
"""
import json
import random
import re
import sys
import unicodedata
from collections import defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from importar_contenido import _asignatura_por_archivo  # noqa: E402
from parser_contenido import parsear_guia  # noqa: E402
from parser_prueba_examen import parsear_prueba_o_examen  # noqa: E402

RAIZ = Path(__file__).resolve().parents[2]
CONTENIDO = RAIZ / "contenido"
SALIDA = RAIZ / "docs/auditorias/fase1/muestra-docente"
FUENTES = ("guía", "prueba de unidad", "simulacro")


def nombre_curso(carpeta: str) -> str:
    n, ciclo = carpeta.split("-")
    return f"{int(n)}.° {'básico' if ciclo == 'basico' else 'medio'}"


NOMBRES: dict[str, str] = {}  # slug de la guía → «asignatura:» de su frontmatter


def titulo_asignatura(slug: str) -> str:
    return NOMBRES.get(slug) or slug.replace("-", " ").capitalize()


def slug_guia(nombre: str | None, guias: list[str]) -> str | None:
    """«Ciencias Naturales» o «Historia» (pauta de un examen integrado) → slug de la guía del curso."""
    if not nombre:
        return None
    s = unicodedata.normalize("NFKD", nombre.lower()).encode("ascii", "ignore").decode()
    s = re.sub(r"[^a-z0-9]+", "-", s).strip("-")
    return next((g for g in guias if g == s or g.startswith(s)), None)


def recolectar(curso: Path) -> list[dict]:
    items = []
    guias = {g.stem: g for g in curso.glob("*.md") if not g.name.startswith("00")}
    for slug, ruta in guias.items():
        m = re.search(r"(?m)^asignatura:\s*(.+)$", ruta.read_text(encoding="utf-8")[:600])
        if m:
            NOMBRES[slug] = m.group(1).strip()
    for slug, ruta in sorted(guias.items()):
        for oa in parsear_guia(ruta.read_text(encoding="utf-8")):
            for i, p in enumerate(oa.preguntas, 1):
                items.append({"fuente": "guía", "archivo": ruta, "asignatura": slug, "oa": oa.codigo_oficial,
                              "ref": f"{oa.codigo_oficial}, pregunta {i} de la autoevaluación", "tipo": p.tipo,
                              "enunciado": p.enunciado, "opciones": p.opciones, "clave": p.respuesta_correcta,
                              "retro": p.retroalimentacion})
    for carpeta, fuente in (("pruebas", "prueba de unidad"), ("examenes", "simulacro")):
        for ruta in sorted((curso / carpeta).glob("*.md")):
            asignatura_archivo = _asignatura_por_archivo(ruta.stem, list(guias)) or "examen integrado"
            for p, r in parsear_prueba_o_examen(ruta.read_text(encoding="utf-8")):
                # Fuera de contexto no se entiende una pregunta que remite a la anterior.
                if re.search(r"pregunta anterior|mismo (texto|párrafo|gráfico) de la", p.enunciado, re.I):
                    continue
                asignatura = slug_guia(r.asignatura, list(guias)) or asignatura_archivo
                items.append({"fuente": fuente, "archivo": ruta, "asignatura": asignatura,
                              "oa": r.codigo_oa, "ref": f"pregunta {p.numero}", "tipo": p.tipo,
                              "enunciado": p.enunciado, "opciones": p.opciones, "clave": r.respuesta_correcta,
                              "retro": r.retroalimentacion})
    return items


def elegir(items: list[dict], cantidad: int, semilla: str) -> list[dict]:
    """Reparte la cuota entre asignaturas y, dentro de cada una, entre las tres fuentes (por turnos)."""
    azar = random.Random(semilla)
    grupos: dict[str, dict[str, list[dict]]] = defaultdict(lambda: defaultdict(list))
    for it in items:
        grupos[it["asignatura"]][it["fuente"]].append(it)
    for por_fuente in grupos.values():
        for lista in por_fuente.values():
            azar.shuffle(lista)
    elegidos: list[dict] = []
    asignaturas = sorted(grupos)
    turno = 0
    while len(elegidos) < cantidad and any(any(v) for g in grupos.values() for v in g.values()):
        for asig in asignaturas:
            fuente = FUENTES[turno % len(FUENTES)]
            orden = [fuente] + [f for f in FUENTES if f != fuente]
            for f in orden:
                if grupos[asig][f]:
                    elegidos.append(grupos[asig][f].pop())
                    break
            if len(elegidos) >= cantidad:
                break
        turno += 1
    return elegidos


def bloque(n: int, it: dict) -> str:
    enunciado = it["enunciado"].strip()
    # Los estímulos largos (lecturas) se muestran citados para separarlos de la pregunta.
    if "\n" in enunciado:
        enunciado = "\n".join("> " + linea if linea.strip() else ">" for linea in enunciado.splitlines())
    clave = it["clave"]
    # En «varias correctas» la clave es una lista JSON de opciones (formato del importador).
    if isinstance(clave, str) and clave.startswith("["):
        clave = json.loads(clave)
    claves = set(clave) if isinstance(clave, (list, tuple)) else {clave}
    opciones = "\n".join(
        f"{'abcdefgh'[i]}) {o}{'  ✅' if o in claves else ''}" for i, o in enumerate(it["opciones"] or []))
    ruta = it["archivo"].relative_to(RAIZ)
    return (f"### {n}. {titulo_asignatura(it['asignatura'])} — {it['fuente']} — {it['oa'] or 'sin OA'}\n\n"
            f"*Fuente:* `{ruta}` ({it['ref']}) · *Tipo:* {it['tipo'].replace('_', ' ')}\n\n"
            f"{enunciado}\n\n{opciones}\n\n"
            f"**Explicación que verá el alumno:** {(it['retro'] or '—').strip()}\n\n"
            "| Criterio | Sí | No | Comentario |\n|---|:-:|:-:|---|\n"
            "| Evalúa el OA indicado | | | |\n| La clave es correcta y única | | | |\n"
            "| Los distractores son plausibles | | | |\n| Lenguaje adecuado a la edad | | | |\n"
            "| La explicación es correcta y útil | | | |\n\n---\n")


def main() -> None:
    cantidad = int(sys.argv[sys.argv.index("--por-curso") + 1]) if "--por-curso" in sys.argv else 25
    SALIDA.mkdir(parents=True, exist_ok=True)
    for curso in sorted(p for p in CONTENIDO.iterdir() if p.is_dir() and (p / "pruebas").exists()):
        items = recolectar(curso)
        muestra = elegir(items, cantidad, semilla=curso.name)
        por_fuente = {f: sum(1 for m in muestra if m["fuente"] == f) for f in FUENTES}
        cab = (f"# Muestra para revisión docente — {nombre_curso(curso.name)}\n\n"
               f"{len(muestra)} preguntas elegidas al azar (semilla fija) de un total de {len(items)}: "
               + ", ".join(f"{v} de {k}" for k, v in por_fuente.items())
               + ". La alternativa marcada con ✅ es la clave.\n\n"
               "Instrucciones en [`00-INSTRUCCIONES.md`](00-INSTRUCCIONES.md).\n\n---\n\n")
        texto = cab + "\n".join(bloque(i, it) for i, it in enumerate(muestra, 1))
        destino = SALIDA / f"{curso.name}.md"
        destino.write_text(re.sub(r"\n{3,}", "\n\n", texto), encoding="utf-8")
        print(f"{curso.name}: {len(muestra)} de {len(items)} → {destino.relative_to(RAIZ)}")


if __name__ == "__main__":
    main()
