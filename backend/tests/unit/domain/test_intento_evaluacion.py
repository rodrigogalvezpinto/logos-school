"""Tests del agregado IntentoEvaluacion en aislamiento total — sin FastAPI, sin Postgres.
Antes esta lógica (reanudación, invariante de no-responder-tras-entregar, idempotencia
de entregar, cálculo de nota) solo se podía probar a través del ciclo HTTP completo."""

from datetime import datetime, timedelta, timezone

import pytest

from app.domain.evaluaciones.entities import IntentoEvaluacion
from app.domain.evaluaciones.exceptions import IntentoYaEntregado
from app.domain.evaluaciones.value_objects import PreguntaParaCorreccion


class FakeReloj:
    def __init__(self, ahora: datetime | None = None):
        self._ahora = ahora or datetime(2026, 1, 1, tzinfo=timezone.utc)

    def ahora(self) -> datetime:
        return self._ahora

    def avanzar(self, segundos: int) -> None:
        self._ahora += timedelta(seconds=segundos)


PREGUNTAS = [
    PreguntaParaCorreccion(id=1, tipo="alternativas", respuesta_correcta="4"),
    PreguntaParaCorreccion(id=2, tipo="alternativas", respuesta_correcta="6"),
    PreguntaParaCorreccion(id=3, tipo="desarrollo_breve", respuesta_correcta="algo"),
]


def test_iniciar_crea_un_intento_sin_entregar():
    intento = IntentoEvaluacion.iniciar(perfil_alumno_id=1, conjunto_evaluacion_id=10, reloj=FakeReloj())
    assert intento.id is None
    assert not intento.esta_entregado
    assert intento.respuestas == {}


def test_responder_guarda_la_respuesta():
    intento = IntentoEvaluacion.iniciar(1, 10, FakeReloj())
    intento.responder(1, "4")
    assert intento.respuestas == {"1": "4"}


def test_responder_tras_entregar_lanza_intento_ya_entregado():
    reloj = FakeReloj()
    intento = IntentoEvaluacion.iniciar(1, 10, reloj)
    intento.entregar(PREGUNTAS, reloj)
    with pytest.raises(IntentoYaEntregado):
        intento.responder(1, "4")


def test_entregar_calcula_puntaje_y_nota_solo_con_autocorregibles():
    reloj = FakeReloj()
    intento = IntentoEvaluacion.iniciar(1, 10, reloj)
    intento.responder(1, "4")  # correcta
    intento.responder(2, "5")  # incorrecta
    intento.responder(3, "algo")  # desarrollo, no autocorregible — no cuenta

    intento.entregar(PREGUNTAS, reloj)

    assert intento.puntaje == 1.0
    assert intento.nota == 3.5  # calcular_nota(1, 2): aprobación=1.2, nota=1+3*(1/1.2)=3.5
    assert intento.esta_entregado


def test_entregar_es_idempotente_no_recalcula():
    reloj = FakeReloj()
    intento = IntentoEvaluacion.iniciar(1, 10, reloj)
    intento.responder(1, "4")
    intento.entregar(PREGUNTAS, reloj)
    primera_nota, primer_termino = intento.nota, intento.fecha_termino

    reloj.avanzar(9999)
    intento.entregar(PREGUNTAS, reloj)  # no debería cambiar nada

    assert intento.nota == primera_nota
    assert intento.fecha_termino == primer_termino


def test_entregar_sin_preguntas_autocorregibles_da_nota_none():
    reloj = FakeReloj()
    intento = IntentoEvaluacion.iniciar(1, 10, reloj)
    solo_desarrollo = [PreguntaParaCorreccion(id=3, tipo="desarrollo_breve", respuesta_correcta="algo")]
    intento.entregar(solo_desarrollo, reloj)
    assert intento.puntaje == 0.0
    assert intento.nota is None


def test_entregar_calcula_tiempo_usado_en_segundos():
    reloj = FakeReloj()
    intento = IntentoEvaluacion.iniciar(1, 10, reloj)
    reloj.avanzar(125)
    intento.entregar(PREGUNTAS, reloj)
    assert intento.tiempo_usado_seg == 125
