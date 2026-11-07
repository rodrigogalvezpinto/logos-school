"""Hallazgo de auditoría 2026-11-07: mezclar pregunta por pregunta separaba las preguntas de
una misma lectura y rompía referencias como «la pregunta anterior»."""
from app.domain.evaluaciones.value_objects import (
    bloques_de_lectura,
    mezclar_por_bloques,
    quitar_numeracion_de_rangos,
)

LECTURA = "Lee este cuento y responde las preguntas 1 a 3: > Valentina vivía en Caleta Tortel " + "x" * 120


def test_preguntas_con_el_mismo_estimulo_quedan_juntas_y_en_orden():
    enunciados = [LECTURA + " ¿Qué pidió la abuela?", LECTURA + " ¿Dónde vive?", LECTURA + " ¿Qué opinas?",
                  "Calcula 2 + 2", "Sobre el mismo párrafo de la pregunta anterior: ¿qué conector?", "¿Qué es un sustantivo?"]
    assert bloques_de_lectura(enunciados) == [[0, 1, 2], [3, 4], [5]]
    for semilla in range(30):
        orden = mezclar_por_bloques(list(range(6)), enunciados, semilla)
        assert sorted(orden) == list(range(6))
        i = orden.index(0)
        assert orden[i:i + 3] == [0, 1, 2]
        assert orden[orden.index(3) + 1] == 4


def test_mezcla_por_bloques_es_estable_por_semilla():
    enunciados = [f"Pregunta suelta {i}" for i in range(10)]
    assert mezclar_por_bloques(list(range(10)), enunciados, 7) == mezclar_por_bloques(list(range(10)), enunciados, 7)
    assert any(mezclar_por_bloques(list(range(10)), enunciados, s) != list(range(10)) for s in range(5))


def test_quita_la_numeracion_de_rangos_que_el_barajado_vuelve_falsa():
    assert quitar_numeracion_de_rangos("Lee este cuento y responde las preguntas 1 a 5: > ...") == \
        "Lee este cuento y responde las preguntas siguientes: > ..."
    assert quitar_numeracion_de_rangos("Calcula 3 a 5") == "Calcula 3 a 5"
    assert quitar_numeracion_de_rangos("Lee estas instrucciones y responde la pregunta 3: >") == \
        "Lee estas instrucciones y responde la pregunta siguiente: >"
    assert quitar_numeracion_de_rangos("Lee esta nota y responde las preguntas 1 y 2:") == \
        "Lee esta nota y responde las preguntas siguientes:"
