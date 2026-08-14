import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))

from parser_prueba_examen import parsear_prueba_o_examen

TEXTO_CON_INSTRUCCIONES = """
## Instrucciones para el estudiante

1. Este examen contiene **2 preguntas** y tiene una duración de 90 minutos.
2. Se permite el uso de calculadora.

## PREGUNTAS

**1. (Matemática)** ¿Cuánto es 2 + 2?

a) 3
b) 4
c) 5
d) 6

**2. (Historia)** ¿Verdadero o falso: Chile está en Sudamérica?

## Pauta de respuestas

**1.** b) 4 — Suma básica.
**2.** Verdadero — Chile está en el continente sudamericano.
"""


def test_las_instrucciones_numeradas_no_se_cuelan_como_preguntas():
    """Bug real encontrado simulando un examen completo (2026-08-13): las instrucciones
    numeradas al inicio del examen ("1. Este examen contiene...", "2. Se permite...") se
    parseaban como preguntas falsas, desalineando toda la pauta de respuestas con las
    preguntas reales. Las preguntas reales siempre empiezan la línea con "**" (negrita);
    las instrucciones no."""
    resultado = parsear_prueba_o_examen(TEXTO_CON_INSTRUCCIONES)

    assert len(resultado) == 2
    enunciados = [p.enunciado for p, _ in resultado]
    assert not any("contiene" in e.lower() or "duración" in e.lower() for e in enunciados)
    assert "2 + 2" in enunciados[0]

    pregunta_1, pauta_1 = resultado[0]
    assert pauta_1 is not None
    # La pauta trae la letra ("b") pero IntentoEvaluacion.entregar() compara contra el
    # TEXTO de la opción que el alumno clickeó — la letra sola nunca podría calzar
    # (bug real encontrado simulando un examen con las respuestas correctas reales:
    # 0/12 correctas pese a responder exactamente lo que decía la pauta).
    assert pauta_1.respuesta_correcta == "4"

    pregunta_2, pauta_2 = resultado[1]
    assert pauta_2 is not None
    assert pauta_2.respuesta_correcta.lower().startswith("verdadero")
