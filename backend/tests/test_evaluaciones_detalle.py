"""Fase 1, ítem 2.1 del plan de incorporación de hallazgos de Brincus — resumen final con
detalle por pregunta. Ver planificacion/27-plan-incorporacion-hallazgos-brincus.md."""

from app.infrastructure.persistence.orm_models import Asignatura, ConjuntoEvaluacion, Nivel, Pregunta

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

    p1 = Pregunta(
        asignatura_id=asignatura.id, tipo="alternativas", enunciado="2+2?",
        opciones=["3", "4"], respuesta_correcta="4", retroalimentacion="Suma directa.",
    )
    p2 = Pregunta(
        asignatura_id=asignatura.id, tipo="alternativas", enunciado="3+3?",
        opciones=["5", "6"], respuesta_correcta="6", retroalimentacion="Suma directa.",
    )
    p3 = Pregunta(
        asignatura_id=asignatura.id, tipo="desarrollo_breve", enunciado="Explica el 10.",
        respuesta_correcta="algo", retroalimentacion="",
    )
    session.add(p1); session.add(p2); session.add(p3)
    session.commit()
    session.refresh(p1); session.refresh(p2); session.refresh(p3)

    conjunto = ConjuntoEvaluacion(
        tipo="prueba_unidad", asignatura_id=asignatura.id, nombre="Prueba de prueba",
        pregunta_ids=[p1.id, p2.id, p3.id],
    )
    session.add(conjunto)
    session.commit()
    session.refresh(conjunto)

    email = f"apoderado.detalle.{next(_CONTADOR_EMAILS)}@test.cl"
    token = client.post(
        "/auth/registro", json={"email": email, "password": "ClaveSegura123", "nombre": "Apoderado Test"}
    ).json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    perfil_id = client.post(
        "/auth/alumnos", headers=headers,
        json={"nombre": "Test", "apellidos": "Test", "fecha_nacimiento": "2016-01-01", "rut": "1-9", "nivel_id": nivel.id},
    ).json()["id"]

    return conjunto, perfil_id, (p1, p2, p3), headers


def test_detalle_antes_de_entregar_da_400(client, session):
    conjunto, perfil_id, _, headers = _preparar(client, session)
    intento_id = client.post(
        "/evaluaciones/intentos", headers=headers,
        json={"perfil_alumno_id": perfil_id, "conjunto_evaluacion_id": conjunto.id},
    ).json()["id"]

    r = client.get(f"/evaluaciones/intentos/{intento_id}/detalle", headers=headers)
    assert r.status_code == 400


def test_detalle_de_intento_inexistente_da_404(client, session):
    _, _, _, headers = _preparar(client, session)
    r = client.get("/evaluaciones/intentos/999999/detalle", headers=headers)
    assert r.status_code == 404


def test_detalle_tras_entregar_desglosa_pregunta_por_pregunta(client, session):
    conjunto, perfil_id, (p1, p2, p3), headers = _preparar(client, session)
    intento_id = client.post(
        "/evaluaciones/intentos", headers=headers,
        json={"perfil_alumno_id": perfil_id, "conjunto_evaluacion_id": conjunto.id},
    ).json()["id"]

    client.patch(
        f"/evaluaciones/intentos/{intento_id}/responder", headers=headers,
        json={"pregunta_id": p1.id, "respuesta": "4"},  # correcta
    )
    client.patch(
        f"/evaluaciones/intentos/{intento_id}/responder", headers=headers,
        json={"pregunta_id": p2.id, "respuesta": "5"},  # incorrecta
    )
    # p3 (desarrollo_breve) queda sin responder.

    client.post(f"/evaluaciones/intentos/{intento_id}/entregar", headers=headers)

    r = client.get(f"/evaluaciones/intentos/{intento_id}/detalle", headers=headers)
    assert r.status_code == 200
    detalle = {d["pregunta_id"]: d for d in r.json()}

    assert detalle[p1.id]["es_correcta"] is True
    assert detalle[p1.id]["respuesta_alumno"] == "4"
    assert detalle[p1.id]["respuesta_correcta"] == "4"

    assert detalle[p2.id]["es_correcta"] is False
    assert detalle[p2.id]["respuesta_alumno"] == "5"
    assert detalle[p2.id]["respuesta_correcta"] == "6"

    # No autocorregible: no hay veredicto ni "la" respuesta correcta.
    assert detalle[p3.id]["es_correcta"] is None
    assert detalle[p3.id]["respuesta_correcta"] is None
    assert detalle[p3.id]["respuesta_alumno"] is None  # nunca se respondió


def test_detalle_de_intento_ajeno_da_403(client, session):
    conjunto, perfil_id, _, headers = _preparar(client, session)
    intento_id = client.post(
        "/evaluaciones/intentos", headers=headers,
        json={"perfil_alumno_id": perfil_id, "conjunto_evaluacion_id": conjunto.id},
    ).json()["id"]
    client.post(f"/evaluaciones/intentos/{intento_id}/entregar", headers=headers)

    email_b = f"apoderado.detalle.ajeno.{next(_CONTADOR_EMAILS)}@test.cl"
    token_b = client.post(
        "/auth/registro", json={"email": email_b, "password": "ClaveSegura123", "nombre": "Otro Apoderado"}
    ).json()["access_token"]
    headers_b = {"Authorization": f"Bearer {token_b}"}

    r = client.get(f"/evaluaciones/intentos/{intento_id}/detalle", headers=headers_b)
    assert r.status_code == 403
