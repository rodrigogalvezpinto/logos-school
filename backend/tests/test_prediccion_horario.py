"""Cruce sueño / horario de estudio — idea propia (no un hallazgo de Brincus, ver
`app/application/prediccion/consultas.py`). Marca la fecha directo en el ORM (mismo patrón
que `test_plan_estudio.py` para "sesión atrasada") porque no hay forma de forzar la hora de
un intento a través de la API — siempre usa `reloj.ahora()`."""

from datetime import datetime, timezone

from app.infrastructure.persistence.orm_models import (
    Asignatura,
    ConjuntoEvaluacion,
    IntentoEvaluacion,
    Nivel,
    Pregunta,
)

_CONTADOR_EMAILS = iter(range(1, 100_000))


def _preparar(client, session):
    nivel = Nivel(
        nombre="4° básico", regimen="A", decreto="439/2012", formato_examen="integrado",
        num_preguntas_examen=20, duracion_examen_min=90,
    )
    session.add(nivel)
    session.commit()
    session.refresh(nivel)

    asignatura = Asignatura(nivel_id=nivel.id, nombre="Matemática")
    session.add(asignatura)
    session.commit()
    session.refresh(asignatura)

    pregunta = Pregunta(asignatura_id=asignatura.id, tipo="alternativas", enunciado="2+2?", opciones=["3", "4"], respuesta_correcta="4")
    session.add(pregunta)
    session.commit()
    session.refresh(pregunta)

    prueba = ConjuntoEvaluacion(tipo="prueba_unidad", asignatura_id=asignatura.id, nombre="Prueba 1", pregunta_ids=[pregunta.id])
    session.add(prueba)
    session.commit()
    session.refresh(prueba)

    email = f"apoderado.horario.{next(_CONTADOR_EMAILS)}@test.cl"
    token = client.post(
        "/auth/registro", json={"email": email, "password": "ClaveSegura123", "nombre": "Apoderado Test"}
    ).json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    perfil_id = client.post(
        "/auth/alumnos", headers=headers,
        json={"nombre": "Test", "apellidos": "Test", "fecha_nacimiento": "2016-01-01", "rut": "1-9", "nivel_id": nivel.id},
    ).json()["id"]

    return perfil_id, headers, prueba.id, pregunta.id


def _rendir_a_las(client, headers, perfil_id, conjunto_id, pregunta_id, session, hora_utc: int):
    r = client.post(
        "/evaluaciones/intentos", headers=headers,
        json={"perfil_alumno_id": perfil_id, "conjunto_evaluacion_id": conjunto_id},
    )
    intento_id = r.json()["id"]
    client.patch(
        f"/evaluaciones/intentos/{intento_id}/responder", headers=headers,
        json={"pregunta_id": pregunta_id, "respuesta": "4"},
    )
    client.post(f"/evaluaciones/intentos/{intento_id}/entregar", headers=headers)

    intento_orm = session.get(IntentoEvaluacion, intento_id)
    intento_orm.fecha_termino = datetime(2026, 8, 10, hora_utc, 0, 0)
    session.add(intento_orm)
    session.commit()


def test_sin_evaluaciones_entregadas_da_null(client, session):
    perfil_id, headers, _, _ = _preparar(client, session)
    r = client.get(f"/prediccion/{perfil_id}/horario-de-estudio", headers=headers)
    assert r.status_code == 200
    assert r.json() is None


def test_pocas_sesiones_tarde_no_da_observacion(client, session):
    """2 de 7 después de las 21:00 Chile — bajo el umbral de 3."""
    perfil_id, headers, conjunto_id, pregunta_id = _preparar(client, session)
    # 21:00 Chile = 00:00 UTC (offset fijo -3 usado por el proyecto).
    _rendir_a_las(client, headers, perfil_id, conjunto_id, pregunta_id, session, hora_utc=0)

    r = client.get(f"/prediccion/{perfil_id}/horario-de-estudio", headers=headers)
    datos = r.json()
    assert datos["tiene_observacion"] is False
    assert datos["sesiones_tarde"] == 1


def test_varias_sesiones_tarde_da_observacion(client, session):
    """Requiere >=3 conjuntos distintos porque un intento por (perfil, conjunto) ya
    entregado no permite un segundo — cada llamada usa su propio conjunto."""
    nivel = Nivel(
        nombre="5° básico", regimen="A", decreto="439/2012", formato_examen="separado_por_asignatura",
        num_preguntas_examen=25, duracion_examen_min=90,
    )
    session.add(nivel)
    session.commit()
    session.refresh(nivel)

    asignatura = Asignatura(nivel_id=nivel.id, nombre="Matemática")
    session.add(asignatura)
    session.commit()
    session.refresh(asignatura)

    email = f"apoderado.horario.tarde.{next(_CONTADOR_EMAILS)}@test.cl"
    token = client.post(
        "/auth/registro", json={"email": email, "password": "ClaveSegura123", "nombre": "Apoderado Test"}
    ).json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    perfil_id = client.post(
        "/auth/alumnos", headers=headers,
        json={"nombre": "Test", "apellidos": "Test", "fecha_nacimiento": "2016-01-01", "rut": "2-7", "nivel_id": nivel.id},
    ).json()["id"]

    for i in range(3):
        pregunta = Pregunta(asignatura_id=asignatura.id, tipo="alternativas", enunciado=f"{i}?", opciones=["3", "4"], respuesta_correcta="4")
        session.add(pregunta)
        session.commit()
        session.refresh(pregunta)
        prueba = ConjuntoEvaluacion(tipo="prueba_unidad", asignatura_id=asignatura.id, nombre=f"Prueba {i}", pregunta_ids=[pregunta.id])
        session.add(prueba)
        session.commit()
        session.refresh(prueba)
        # 23:00 Chile = 02:00 UTC del día siguiente.
        _rendir_a_las(client, headers, perfil_id, prueba.id, pregunta.id, session, hora_utc=2)

    r = client.get(f"/prediccion/{perfil_id}/horario-de-estudio", headers=headers)
    datos = r.json()
    assert datos["tiene_observacion"] is True
    assert datos["sesiones_tarde"] == 3
    assert "21:00" in datos["mensaje"]


def test_horario_de_alumno_ajeno_da_403(client, session):
    perfil_id, _, _, _ = _preparar(client, session)
    token_b = client.post(
        "/auth/registro", json={"email": f"ajeno.horario.{next(_CONTADOR_EMAILS)}@test.cl", "password": "ClaveSegura123", "nombre": "Otro"}
    ).json()["access_token"]
    r = client.get(f"/prediccion/{perfil_id}/horario-de-estudio", headers={"Authorization": f"Bearer {token_b}"})
    assert r.status_code == 403


def test_horario_sin_sesion_da_401(client, session):
    perfil_id, _, _, _ = _preparar(client, session)
    r = client.get(f"/prediccion/{perfil_id}/horario-de-estudio")
    assert r.status_code == 401
