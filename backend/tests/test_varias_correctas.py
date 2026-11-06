"""Tipo `varias_correctas` (decisión 2026-11-06: todo el material es de alternativas).

Cubre la regla única de corrección del dominio y la lectura del formato Markdown en guías
(«Respuesta correcta: a, c y d») y en pruebas/simulacros (pauta en lista o tabla)."""

import json
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))

from parser_contenido import parsear_guia, resolver_letras_varias  # noqa: E402
from parser_prueba_examen import parsear_prueba_o_examen  # noqa: E402

from app.domain.evaluaciones.value_objects import TIPOS_AUTOCORREGIBLES, es_respuesta_correcta  # noqa: E402

CLAVE = json.dumps(["Agua", "Luz"])


@pytest.mark.parametrize(
    ("respuesta", "esperado"),
    [
        (json.dumps(["Agua", "Luz"]), True),
        (json.dumps(["Luz", "Agua"]), True),  # el orden no importa
        (json.dumps([" luz ", "AGUA"]), True),  # espacios y mayúsculas no importan
        (json.dumps(["Agua"]), False),  # incompleta: todo o nada
        (json.dumps(["Agua", "Luz", "Sal"]), False),  # sobra una incorrecta
        (json.dumps([]), False),
        ("", False),
        (None, False),
        ("Agua", False),  # no es lista JSON
        ("{no json", False),
    ],
)
def test_varias_correctas_todo_o_nada(respuesta, esperado):
    assert es_respuesta_correcta("varias_correctas", respuesta, CLAVE) is esperado


def test_alternativas_conserva_comparacion_por_texto():
    assert es_respuesta_correcta("alternativas", " unidad de MIL ", "Unidad de mil")
    assert not es_respuesta_correcta("alternativas", "", "Unidad de mil")
    assert not es_respuesta_correcta("alternativas", None, "Unidad de mil")
    assert "varias_correctas" in TIPOS_AUTOCORREGIBLES


@pytest.mark.parametrize(
    ("texto", "esperado"),
    [
        ("a, c y d", ["A", "C", "D"]),
        ("c) y a)", ["A", "C"]),
        ("b, e. Explicación", ["B", "E"]),
        ("a y b — porque", ["A", "B"]),
        ("a", None),  # una sola letra no es varias
        ("a, a", None),  # repetida
        ("a y z", None),
        ("Las alternativas a y c", None),  # debe empezar por la clave
    ],
)
def test_resolver_letras_varias(texto, esperado):
    resultado = resolver_letras_varias(texto, ["A", "B", "C", "D", "E"])
    assert (json.loads(resultado) if resultado else None) == esperado


GUIA = """
## OA 1: Seres vivos

Texto de la guía.

#### Preguntas de autoevaluación

**Pregunta 1 (Varias correctas).** ¿Qué necesita una planta para fotosintetizar? Marca todas las correctas.
a) Luz
b) Sal
c) Agua
d) Dióxido de carbono
e) Arena

**Respuesta correcta: a, c y d.**
*Retroalimentación:* la planta usa luz, agua y CO2.

**Pregunta 2 (Alternativas).** ¿Cuánto es 6 × 2?
a) 8
b) 12
c) 14
d) 62

**Respuesta correcta: b) 12.**
*Retroalimentación:* 6 grupos de 2.
"""


def test_guia_lee_varias_correctas_y_quinta_opcion():
    [oa] = parsear_guia(GUIA)
    varias, simple = oa.preguntas
    assert varias.tipo == "varias_correctas"
    assert varias.opciones == ["Luz", "Sal", "Agua", "Dióxido de carbono", "Arena"]
    assert json.loads(varias.respuesta_correcta) == ["Luz", "Agua", "Dióxido de carbono"]
    assert simple.tipo == "alternativas" and simple.respuesta_correcta == "12"


PRUEBA = """---
oa_evaluados: OA 1
---
# Prueba

**1.** *(Varias correctas)* ¿Cuáles son mamíferos? Marca todas las correctas.
a) Ballena
b) Tiburón
c) Murciélago
d) Pingüino

**2.** *(Alternativas)* ¿Cuál vuela?
a) Perro
b) Gato
c) Murciélago
d) Pez

## Pauta de respuestas

1. **a, c.** La ballena y el murciélago son mamíferos.
2. **c.** El murciélago vuela.
"""

PRUEBA_TABLA = PRUEBA.split("## Pauta")[0] + """# PAUTA DE CORRECCIÓN

| N° | Clave / criterio |
|---|---|
| 1 | a y c — ballena y murciélago son mamíferos |
| 2 | c — vuela |
"""


@pytest.mark.parametrize("texto", [PRUEBA, PRUEBA_TABLA])
def test_prueba_lee_varias_correctas_en_lista_y_tabla(texto):
    (p1, pauta1), (p2, pauta2) = parsear_prueba_o_examen(texto)
    assert p1.tipo == "varias_correctas"
    assert json.loads(pauta1.respuesta_correcta) == ["Ballena", "Murciélago"]
    assert p2.tipo == "alternativas" and pauta2.respuesta_correcta == "Murciélago"
