import pytest
from sqlmodel import Session, SQLModel, create_engine

from app.infrastructure.persistence.orm_models import Asignatura, ConjuntoEvaluacion, Nivel, ObjetivoAprendizaje, Pregunta
from app.infrastructure.persistence.repositorios.preguntas import RepositorioPreguntasSQLModel


def _crear_nivel_con_pregunta(session):
    nivel = Nivel(
        nombre="4° básico",
        regimen="A",
        decreto="439/2012",
        formato_examen="integrado",
        num_preguntas_examen=20,
        duracion_examen_min=90,
    )
    session.add(nivel)
    session.commit()
    session.refresh(nivel)

    asignatura = Asignatura(nivel_id=nivel.id, nombre="Matemática")
    session.add(asignatura)
    session.commit()
    session.refresh(asignatura)

    oa = ObjetivoAprendizaje(
        asignatura_id=asignatura.id,
        codigo_oficial="OA 1",
        descripcion="Números hasta el 10.000",
        contenido_guia="Contenido de prueba.",
    )
    session.add(oa)
    session.commit()
    session.refresh(oa)

    session.add(
        Pregunta(
            oa_id=oa.id,
            tipo="alternativas",
            enunciado="¿Cuánto es 2+2?",
            opciones=["3", "4", "5", "6"],
            respuesta_correcta="4",
            retroalimentacion="2+2=4",
        )
    )
    session.commit()
    return nivel, asignatura, oa


def test_listar_niveles(client, session):
    _crear_nivel_con_pregunta(session)
    r = client.get("/contenido/niveles")
    assert r.status_code == 200
    assert len(r.json()) == 1
    assert r.json()[0]["nombre"] == "4° básico"


def test_listar_asignaturas_de_un_nivel(client, session):
    nivel, _, _ = _crear_nivel_con_pregunta(session)
    r = client.get(f"/contenido/niveles/{nivel.id}/asignaturas")
    assert r.status_code == 200
    assert r.json()[0]["nombre"] == "Matemática"


def test_listar_objetivos_de_una_asignatura(client, session):
    _, asignatura, _ = _crear_nivel_con_pregunta(session)
    r = client.get(f"/contenido/asignaturas/{asignatura.id}/objetivos")
    assert r.status_code == 200
    assert r.json()[0]["codigo_oficial"] == "OA 1"


def test_obtener_objetivo_inexistente_da_404(client, session):
    _crear_nivel_con_pregunta(session)
    r = client.get("/contenido/objetivos/999")
    assert r.status_code == 404


def test_autoevaluacion_devuelve_preguntas_con_respuesta(client, session):
    _, _, oa = _crear_nivel_con_pregunta(session)
    r = client.get(f"/evaluaciones/autoevaluacion/{oa.id}")
    assert r.status_code == 200
    preguntas = r.json()
    assert len(preguntas) == 1
    # A propósito SÍ incluye la respuesta — es autoevaluación formativa, no examen
    # (ver planificacion/12-motor-de-evaluacion.md)
    assert preguntas[0]["respuesta_correcta"] == "4"
    assert preguntas[0]["retroalimentacion"] == "2+2=4"


def test_autoevaluacion_de_oa_inexistente_da_404(client, session):
    _crear_nivel_con_pregunta(session)
    r = client.get("/evaluaciones/autoevaluacion/999")
    assert r.status_code == 404


@pytest.fixture
def banco_y_conjuntos_en_memoria():
    engine = create_engine("sqlite://")
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        session.add(Nivel(id=1, nombre="Nivel de prueba", regimen="A", decreto="439/2012",
                          formato_examen="integrado", num_preguntas_examen=20, duracion_examen_min=60))
        session.add(Asignatura(id=1, nivel_id=1, nombre="Matemática"))
        session.add_all([
            ObjetivoAprendizaje(id=i, asignatura_id=1, codigo_oficial=f"OA {i}", descripcion="Objetivo de prueba")
            for i in (1, 2)
        ])
        session.add_all([
            Pregunta(id=i, oa_id=2 if i == 5 else 1, asignatura_id=1,
                     tipo="desarrollo_breve" if i in (3, 4) else "alternativas",
                     enunciado=f"Pregunta {i}", opciones=None if i in (3, 4) else ["1", "2"],
                     respuesta_correcta="Justificación" if i in (3, 4) else "2")
            for i in range(1, 6)
        ])
        session.add_all([
            ConjuntoEvaluacion(tipo="prueba_unidad", asignatura_id=1, nombre="Unidad", pregunta_ids=[2]),
            ConjuntoEvaluacion(tipo="examen_simulacro", nivel_id=1, nombre="Examen", pregunta_ids=[2, 3]),
            ConjuntoEvaluacion(tipo="prueba_unidad", asignatura_id=1, nombre="Vacío", pregunta_ids=[]),
        ])
        session.commit()
        yield session
    engine.dispose()


def test_autoevaluacion_excluye_conjuntos_sin_perder_banco_abierto(banco_y_conjuntos_en_memoria):
    repositorio = RepositorioPreguntasSQLModel(banco_y_conjuntos_en_memoria)
    assert {p.id for p in repositorio.buscar_por_oa(1)} == {1, 4}
    assert {p.id for p in repositorio.buscar_por_oa(2)} == {5}
    assert repositorio.buscar_por_oa(999) == []


def test_simulacro_parcial_no_consume_el_banco_de_autoevaluacion(banco_y_conjuntos_en_memoria):
    session = banco_y_conjuntos_en_memoria
    session.add(ConjuntoEvaluacion(tipo="examen_simulacro_parcial", asignatura_id=1,
                                  nombre="Parcial", pregunta_ids=[1]))
    session.commit()
    repositorio = RepositorioPreguntasSQLModel(session)
    assert {p.id for p in repositorio.buscar_por_oa(1)} == {1, 4}


def test_busqueda_por_ids_conserva_preguntas_de_evaluaciones(banco_y_conjuntos_en_memoria):
    repositorio = RepositorioPreguntasSQLModel(banco_y_conjuntos_en_memoria)
    assert [p.id for p in repositorio.listar_por_ids([2, 3, 999])] == [2, 3]
    assert [p.id for p in repositorio.listar_para_correccion([2, 3, 999])] == [2, 3]
