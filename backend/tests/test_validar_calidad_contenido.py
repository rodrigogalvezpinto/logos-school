"""Fase 1, ítem 2.5.1 del plan de incorporación de hallazgos de Brincus — control de
calidad de contenido. Ver planificacion/27-plan-incorporacion-hallazgos-brincus.md.

Prueba la LÓGICA del validador contra datos sintéticos, no contra el contenido real de
`contenido/` — correrlo contra el banco real es una tarea aparte
(`scripts/validar_calidad_contenido.py`, que sí encontró 153 hallazgos reales el
2026-08-14: preguntas de emparejamiento mal etiquetadas como "alternativas", ver el
propio script para el detalle)."""

from app.application.contenido.validar_calidad import validar
from app.infrastructure.persistence.orm_models import Asignatura, ConjuntoEvaluacion, Nivel, ObjetivoAprendizaje, Pregunta


def _nivel_y_asignaturas(session):
    nivel = Nivel(
        nombre="4° básico", regimen="A", decreto="439/2012", formato_examen="integrado",
        num_preguntas_examen=20, duracion_examen_min=90,
    )
    session.add(nivel)
    session.commit()
    session.refresh(nivel)

    matematica = Asignatura(nivel_id=nivel.id, nombre="Matemática")
    lenguaje = Asignatura(nivel_id=nivel.id, nombre="Lenguaje")
    session.add(matematica); session.add(lenguaje)
    session.commit()
    session.refresh(matematica); session.refresh(lenguaje)
    return matematica, lenguaje


def test_sin_contenido_no_hay_hallazgos(client, session):
    resultado = validar(session)
    assert resultado == []


def test_alternativas_bien_calibrada_no_es_hallazgo(client, session):
    matematica, _ = _nivel_y_asignaturas(session)
    p = Pregunta(asignatura_id=matematica.id, tipo="alternativas", enunciado="2+2?", opciones=["3", "4"], respuesta_correcta="4")
    session.add(p)
    session.commit()

    assert validar(session) == []


def test_alternativas_con_respuesta_fuera_de_opciones_es_hallazgo(client, session):
    """El bug real encontrado: preguntas de emparejamiento ("1-b, 2-c, 3-a") etiquetadas
    como tipo="alternativas" — imposibles de responder bien en la app hoy."""
    matematica, _ = _nivel_y_asignaturas(session)
    p = Pregunta(
        asignatura_id=matematica.id, tipo="alternativas", enunciado="Relaciona",
        opciones=["a) Uno", "b) Dos"], respuesta_correcta="1-b, 2-a",
    )
    session.add(p)
    session.commit()

    hallazgos = validar(session)
    assert len(hallazgos) == 1
    assert "no está entre las opciones" in hallazgos[0]


def test_verdadero_falso_con_respuesta_invalida_es_hallazgo(client, session):
    matematica, _ = _nivel_y_asignaturas(session)
    p = Pregunta(asignatura_id=matematica.id, tipo="verdadero_falso", enunciado="El sol es una estrella.", respuesta_correcta="Obvio")
    session.add(p)
    session.commit()

    hallazgos = validar(session)
    assert len(hallazgos) == 1
    assert 'no es "Verdadero" ni "Falso"' in hallazgos[0]


def test_guia_vacia_es_hallazgo(client, session):
    matematica, _ = _nivel_y_asignaturas(session)
    oa = ObjetivoAprendizaje(asignatura_id=matematica.id, codigo_oficial="MA04OA01", descripcion="Contar", contenido_guia="   ")
    session.add(oa)
    session.commit()

    hallazgos = validar(session)
    assert len(hallazgos) == 1
    assert "contenido_guia vacío" in hallazgos[0]


def test_pregunta_de_otra_asignatura_en_un_conjunto_es_hallazgo(client, session):
    """El análogo directo al bug de Brincus: contenido filed bajo la asignatura/unidad
    equivocada — una guía de "Números hasta 10.000" con ejercicios de otro nivel."""
    matematica, lenguaje = _nivel_y_asignaturas(session)
    p_lenguaje = Pregunta(asignatura_id=lenguaje.id, tipo="alternativas", enunciado="¿Sujeto?", opciones=["a", "b"], respuesta_correcta="a")
    session.add(p_lenguaje)
    session.commit()
    session.refresh(p_lenguaje)

    conjunto = ConjuntoEvaluacion(
        tipo="prueba_unidad", asignatura_id=matematica.id, nombre="Prueba de Matemática",
        pregunta_ids=[p_lenguaje.id],
    )
    session.add(conjunto)
    session.commit()

    hallazgos = validar(session)
    assert len(hallazgos) == 1
    assert "asignatura equivocada" in hallazgos[0]


def test_pregunta_id_inexistente_en_conjunto_es_hallazgo(client, session):
    matematica, _ = _nivel_y_asignaturas(session)
    conjunto = ConjuntoEvaluacion(
        tipo="prueba_unidad", asignatura_id=matematica.id, nombre="Prueba", pregunta_ids=[999999],
    )
    session.add(conjunto)
    session.commit()

    hallazgos = validar(session)
    assert len(hallazgos) == 1
    assert "que no existe" in hallazgos[0]
