from app.infrastructure.persistence.orm_models import Asignatura, Nivel, ObjetivoAprendizaje, Pregunta


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
