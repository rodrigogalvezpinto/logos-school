"""Calificación con estrellas por guía (Fase 1 — ver
planificacion/27-plan-incorporacion-hallazgos-brincus.md, cuarta pasada, hallazgo comparando
en vivo contra Brincus: tab "Evaluar Sección" con estrellas, distinto de "Reportar error")."""

from app.infrastructure.persistence.orm_models import Asignatura, Nivel, ObjetivoAprendizaje

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

    oa = ObjetivoAprendizaje(asignatura_id=asignatura.id, codigo_oficial="OA 1", descripcion="Objetivo 1")
    session.add(oa)
    session.commit()
    session.refresh(oa)

    email = f"apoderado.calif.{next(_CONTADOR_EMAILS)}@test.cl"
    token = client.post(
        "/auth/registro", json={"email": email, "password": "ClaveSegura123", "nombre": "Apoderado Test"}
    ).json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    perfil_id = client.post(
        "/auth/alumnos", headers=headers,
        json={"nombre": "Test", "apellidos": "Test", "fecha_nacimiento": "2016-01-01", "rut": "1-9", "nivel_id": nivel.id},
    ).json()["id"]

    return oa, perfil_id, headers


def test_calificar_guia(client, session):
    oa, perfil_id, headers = _preparar(client, session)
    r = client.put(f"/calificaciones/{perfil_id}/guias/{oa.id}", headers=headers, json={"estrellas": 4})
    assert r.status_code == 200
    assert r.json()["estrellas"] == 4
    assert r.json()["oa_id"] == oa.id


def test_recalificar_la_misma_guia_actualiza_en_vez_de_duplicar(client, session):
    oa, perfil_id, headers = _preparar(client, session)
    client.put(f"/calificaciones/{perfil_id}/guias/{oa.id}", headers=headers, json={"estrellas": 2})
    r = client.put(f"/calificaciones/{perfil_id}/guias/{oa.id}", headers=headers, json={"estrellas": 5})
    assert r.status_code == 200
    assert r.json()["estrellas"] == 5

    consulta = client.get(f"/calificaciones/{perfil_id}/guias/{oa.id}", headers=headers)
    assert consulta.json()["estrellas"] == 5


def test_obtener_mi_calificacion_sin_calificar_devuelve_null(client, session):
    oa, perfil_id, headers = _preparar(client, session)
    r = client.get(f"/calificaciones/{perfil_id}/guias/{oa.id}", headers=headers)
    assert r.status_code == 200
    assert r.json() is None


def test_calificar_con_estrellas_fuera_de_rango_da_422(client, session):
    oa, perfil_id, headers = _preparar(client, session)
    r = client.put(f"/calificaciones/{perfil_id}/guias/{oa.id}", headers=headers, json={"estrellas": 6})
    assert r.status_code == 422
    r2 = client.put(f"/calificaciones/{perfil_id}/guias/{oa.id}", headers=headers, json={"estrellas": 0})
    assert r2.status_code == 422


def test_calificar_de_alumno_ajeno_da_403(client, session):
    oa, perfil_id, _ = _preparar(client, session)
    email_b = f"apoderado.calif.ajeno.{next(_CONTADOR_EMAILS)}@test.cl"
    token_b = client.post(
        "/auth/registro", json={"email": email_b, "password": "ClaveSegura123", "nombre": "Otro"}
    ).json()["access_token"]
    headers_b = {"Authorization": f"Bearer {token_b}"}
    r = client.put(f"/calificaciones/{perfil_id}/guias/{oa.id}", headers=headers_b, json={"estrellas": 3})
    assert r.status_code == 403


def test_calificar_sin_sesion_da_401(client, session):
    oa, perfil_id, _ = _preparar(client, session)
    r = client.put(f"/calificaciones/{perfil_id}/guias/{oa.id}", json={"estrellas": 3})
    assert r.status_code == 401
