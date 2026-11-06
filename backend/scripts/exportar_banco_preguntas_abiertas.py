"""Exporta todas las preguntas abiertas (desarrollo_breve) del corpus a un banco JSON
versionado, antes de convertirlas a alternativas (decisión de producto 2026-11-06).

El banco conserva enunciado, pauta, retroalimentación y OA de cada pregunta abierta para
reactivarlas cuando exista un corrector confiable (profesor o IA validada). No lo lee el
importador: es un archivo de respaldo pedagógico, no contenido activo.

Uso: python backend/scripts/exportar_banco_preguntas_abiertas.py [ref_git]
"""

import json
import pathlib
import subprocess
import sys

sys.path.insert(0, str(pathlib.Path(__file__).parent))
from parser_contenido import parsear_guia  # noqa: E402
from parser_prueba_examen import parsear_prueba_o_examen  # noqa: E402

RAIZ = pathlib.Path(__file__).resolve().parents[2]
DESTINO = RAIZ / "docs" / "banco-preguntas-abiertas" / "preguntas-abiertas.json"


def main() -> None:
    ref = sys.argv[1] if len(sys.argv) > 1 else "HEAD"
    sha = subprocess.check_output(["git", "rev-parse", ref], cwd=RAIZ, text=True).strip()
    rutas = subprocess.check_output(
        ["git", "ls-tree", "-r", "--name-only", ref, "contenido"], cwd=RAIZ, text=True
    ).split()
    preguntas = []
    for ruta in sorted(rutas):
        if not ruta.endswith(".md") or pathlib.Path(ruta).name.startswith("00-"):
            continue
        texto = subprocess.check_output(["git", "show", f"{ref}:{ruta}"], cwd=RAIZ, text=True)
        partes = pathlib.Path(ruta).parts
        base = {"archivo": ruta, "curso": partes[1]}
        if partes[2] in ("pruebas", "examenes"):
            for p, pauta in parsear_prueba_o_examen(texto):
                if p.tipo != "desarrollo_breve":
                    continue
                preguntas.append({
                    **base, "recurso": "simulacro" if partes[2] == "examenes" else "prueba_unidad",
                    "numero": p.numero, "oa": list(pauta.codigos_oa) if pauta else [],
                    "enunciado": p.enunciado,
                    "pauta": pauta.respuesta_correcta if pauta else None,
                    "retroalimentacion": pauta.retroalimentacion if pauta else None,
                })
        else:
            for oa in parsear_guia(texto):
                for indice, q in enumerate(oa.preguntas, start=1):
                    if q.tipo != "desarrollo_breve":
                        continue
                    preguntas.append({
                        **base, "recurso": "guia_autoevaluacion", "oa": [oa.codigo_oficial],
                        "modulo": oa.modulo, "posicion_en_oa": indice, "enunciado": q.enunciado,
                        "pauta": q.respuesta_correcta, "retroalimentacion": q.retroalimentacion,
                    })
    DESTINO.parent.mkdir(parents=True, exist_ok=True)
    DESTINO.write_text(json.dumps(
        {"origen_git": sha, "total": len(preguntas), "preguntas": preguntas},
        ensure_ascii=False, indent=1,
    ) + "\n")
    print(f"{len(preguntas)} preguntas abiertas exportadas desde {sha[:7]} a {DESTINO.relative_to(RAIZ)}")


if __name__ == "__main__":
    main()
