import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))

from parser_contenido import parsear_guia

TEXTO_BASE = """
# Asignatura de prueba

## OA N°1: Objetivo de ejemplo

Contenido de la guía.

### Banco de preguntas de autoevaluación — OA N°1

**1. (Alternativas)** ¿Cuánto es 2 + 2?

a) 3
b) 4
c) 5
d) 6

*Respuesta correcta: b.* Retroalimentación: suma básica.

**2. (Alternativas)** ¿Cuál es la capital de Francia?

a) Madrid
b) Roma
c) París
d) Berlín

**Respuesta correcta: c) París.**
**Retroalimentación:** es la capital de Francia.

**3. (Verdadero o Falso)** El cielo es azul.

✅ Respuesta correcta: **Verdadero**
💬 *Retroalimentación:* en un día despejado, el cielo se ve azul.
"""


def test_respuesta_solo_letra_se_resuelve_al_texto_de_la_opcion():
    """Bug real (2026-08-13): la pauta a veces solo trae la letra ("b."), sin repetir el
    texto de la opción — pero el alumno siempre responde con el texto completo, nunca
    con la letra. Sin resolver la letra acá, ninguna alternativa se podría corregir bien."""
    objetivos = parsear_guia(TEXTO_BASE)
    preguntas = objetivos[0].preguntas
    assert preguntas[0].respuesta_correcta == "4"
    assert preguntas[0].respuesta_correcta in preguntas[0].opciones


def test_respuesta_letra_mas_texto_repetido_tambien_se_resuelve():
    """Otras preguntas repiten el texto tras la letra ("c) París") — también hay que
    resolver por la letra, no confiar en el texto repetido (puede traer el prefijo
    "c) " que no calza exactamente con la opción tal como está en `opciones`)."""
    objetivos = parsear_guia(TEXTO_BASE)
    preguntas = objetivos[0].preguntas
    assert preguntas[1].respuesta_correcta == "París"


def test_emoji_de_vineta_no_contamina_la_respuesta():
    """Bug real: "💬 Retroalimentación:" en su propia línea dejaba el emoji pegado al
    final de respuesta_correcta ("Verdadero 💬"), rompiendo la comparación exacta."""
    objetivos = parsear_guia(TEXTO_BASE)
    preguntas = objetivos[0].preguntas
    assert preguntas[2].respuesta_correcta == "Verdadero"


TEXTO_INGLES = """
# Inglés de prueba

## OA N°1: Objetivo de ejemplo

Contenido.

### Banco de preguntas de autoevaluación — OA N°1

**1. (Verdadero o Falso)** Chile is in South America.

**Respuesta correcta:** True (Verdadero).
**Retroalimentación:** correcto.

**2. (Verdadero o Falso)** The sky is green.

**Respuesta correcta:** False (Falso).
**Retroalimentación:** el cielo es azul, no verde.
"""


def test_verdadero_falso_bilingue_se_normaliza_al_espanol():
    """El contenido de Inglés a veces escribe la respuesta en inglés/bilingüe
    ("True (Verdadero)") — las opciones reales que el alumno clickea son siempre
    "Verdadero"/"Falso" en español, hay que normalizar."""
    objetivos = parsear_guia(TEXTO_INGLES)
    preguntas = objetivos[0].preguntas
    assert preguntas[0].respuesta_correcta == "Verdadero"
    assert preguntas[1].respuesta_correcta == "Falso"
