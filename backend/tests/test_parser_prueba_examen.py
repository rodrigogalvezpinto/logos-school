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


TEXTO_OPCION_CON_WORD_WRAP = """
**Pregunta 1 (alternativas).** ¿Cuál de las siguientes NO corresponde?

a) Superar la ignorancia.
b) Predecir con exactitud eventos futuros mediante experimentos
   controlados.
c) Enfrentar problemas complejos.
d) Liberarnos de prejuicios y costumbres.

## Pauta de respuestas

**1.** b) Predecir con exactitud eventos futuros mediante experimentos controlados.
"""


def test_opcion_con_word_wrap_no_contamina_el_enunciado():
    """Mismo bug que en parser_contenido.py, encontrado en pruebas/exámenes también."""
    resultado = parsear_prueba_o_examen(TEXTO_OPCION_CON_WORD_WRAP)
    pregunta, pauta = resultado[0]
    assert pregunta.enunciado == "¿Cuál de las siguientes NO corresponde?"
    assert pregunta.opciones[1] == "Predecir con exactitud eventos futuros mediante experimentos controlados."


TEXTO_PREGUNTA_DE_EMPAREJAMIENTO = """
**3. (Relacionar / emparejar)** Une cada situación con la norma que corresponde:

1) Cruzar una calle con autos — 2) Hablar en clases mientras el profesor explica — 3) Visitar
un monumento histórico

a) No rayarlo ni dañarlo — b) Levantar la mano y esperar mi turno — c) Mirar hacia ambos lados

## Pauta de respuestas

**3.** 1-c, 2-b, 3-a. Cada situación tiene una norma distinta según el contexto.
"""


def test_pregunta_de_emparejamiento_no_se_reclasifica_como_alternativas_rota():
    """Bug real de contenido (73 preguntas en pruebas/exámenes, mismo bug que en
    parser_contenido.py): RE_OPCION confunde la línea en línea de definiciones
    ("a) A — b) B — c) C") con una alternativa real, dejando una sola opción ilegible y
    una pauta ("1-c, 2-b, 3-a") que nunca calza con ninguna opción clickeable — deben
    quedar como desarrollo_breve con el enunciado completo."""
    resultado = parsear_prueba_o_examen(TEXTO_PREGUNTA_DE_EMPAREJAMIENTO)
    pregunta, pauta = resultado[0]
    assert pregunta.tipo == "desarrollo_breve"
    assert pregunta.opciones is None
    assert "No rayarlo ni dañarlo" in pregunta.enunciado
    assert pauta is not None
    assert pauta.respuesta_correcta.startswith("1-c, 2-b, 3-a")


TEXTO_PAUTA_LETRA_CON_EM_DASH = """
**1. (Alternativas)** ¿Qué figura literaria usa "las manos del reloj corrían"?

a) Personificación
b) Metáfora
c) Hipérbole
d) Pregunta retórica

## Pauta de respuestas

**1.** b — se identifican directamente dos términos (las manos = manecillas), sin usar
"como" ni verbos de acción atribuidos a un objeto inanimado.
"""


def test_pauta_con_letra_y_em_dash_se_resuelve_al_texto_de_la_opcion():
    """Bug real (7 preguntas de 3°-4° medio): la pauta a veces escribe la letra seguida de
    un em-dash y la explicación ("b — se identifican...") en vez de "b." o "b)" — sin
    tolerar esa forma, RE_LETRA_INICIAL no reconocía la letra y el texto completo
    (truncado a 60 caracteres) quedaba como respuesta_correcta, sin calzar nunca con
    ninguna opción real."""
    resultado = parsear_prueba_o_examen(TEXTO_PAUTA_LETRA_CON_EM_DASH)
    pregunta, pauta = resultado[0]
    assert pauta is not None
    assert pauta.respuesta_correcta == "Metáfora"


TEXTO_EMPAREJAMIENTO_SIN_ETIQUETA = """
**4.** Une cada derecho del niño con un ejemplo de cómo se garantiza en Chile:

1) Derecho a la educación — 2) Derecho a la alimentación — 3) Derecho a la protección frente al trabajo infantil

a) Prohibición legal de que los niños trabajen antes de cierta edad — b) Educación gratuita y obligatoria — c) Programas de alimentación escolar, como los de JUNAEB

1) ___  2) ___  3) ___

## Pauta de respuestas

| N° | Respuesta correcta |
|----|---------------------|
| 4  | 1-b (educación — educación gratuita y obligatoria), 2-c (alimentación — programas como JUNAEB), 3-a (protección frente al trabajo infantil — prohibición legal) |
"""


def test_pregunta_de_emparejamiento_sin_etiqueta_se_detecta_por_estructura():
    """Bug real (30 preguntas restantes tras el fix por etiqueta): las pruebas de unidad a
    veces no traen ninguna etiqueta entre paréntesis (solo "**4.**"), así que detectar por
    la palabra "relacionar/emparejar" en la etiqueta no basta — hay que reconocer también
    la forma "a) ... — b) ..." (una línea con más de un marcador de letra pegado), que
    estructuralmente nunca ocurre en una alternativa real."""
    resultado = parsear_prueba_o_examen(TEXTO_EMPAREJAMIENTO_SIN_ETIQUETA)
    pregunta, pauta = resultado[0]
    assert pregunta.tipo == "desarrollo_breve"
    assert pregunta.opciones is None
    assert "Prohibición legal" in pregunta.enunciado
