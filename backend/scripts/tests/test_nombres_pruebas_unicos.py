"""Cada prueba de unidad debe tener un nombre distinto dentro de su curso y asignatura:
el alumno elige la prueba por su nombre (hallazgo E2E 2026-11-06: 22 pruebas compartían
«Prueba de Unidad — <ramo> <curso>»)."""
import collections
from pathlib import Path

from importar_contenido import _titulo_desde_encabezado

CONTENIDO = Path(__file__).resolve().parents[3] / "contenido"


def test_nombres_de_pruebas_unicos_por_curso_y_asignatura():
    vistos = collections.defaultdict(list)
    for ruta in sorted(CONTENIDO.glob("*/pruebas/*.md")):
        asignatura = ruta.name.split("-unidad")[0]
        vistos[(ruta.parts[-3], asignatura, _titulo_desde_encabezado(ruta))].append(ruta.name)
    repetidos = {k: v for k, v in vistos.items() if len(v) > 1}
    assert not repetidos, repetidos
