"""Idea 7 del boceto de innovación (2026-08-17): agenda familiar del domingo — 3 preguntas
armadas con datos reales, "ya conversamos" no vuelve a insistir esa semana. Ver
`app/application/apoderado/consultas.py` y `casos_de_uso.py`."""

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

    oa = ObjetivoAprendizaje(asignatura_id=asignatura.id, codigo_oficial="OA 1", descripcion="Sumar")
    session.add(oa)
    session.commit()
    session.refresh(oa)

    email = f"apoderado.agenda.{next(_CONTADOR_EMAILS)}@test.cl"
    token = client.post(
        "/auth/registro", json={"email": email, "password": "ClaveSegura123", "nombre": "Apoderado Test"}
    ).json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    perfil_id = client.post(
        "/auth/alumnos", headers=headers,
        json={"nombre": "Test", "apellidos": "Test", "fecha_nacimiento": "2016-01-01", "rut": "1-9", "nivel_id": nivel.id},
    ).json()["id"]

    return perfil_id, headers


def test_sin_ningun_dato_da_pregunta_generica(client, session):
    perfil_id, headers = _preparar(client, session)
    r = client.get(f"/apoderado/agenda-familiar/{perfil_id}", headers=headers)
    assert r.status_code == 200
    datos = r.json()
    assert len(datos["preguntas"]) == 1
    assert datos["ya_conversada"] is False


def test_marcar_conversada_persiste_para_esa_semana(client, session):
    perfil_id, headers = _preparar(client, session)
    r = client.get(f"/apoderado/agenda-familiar/{perfil_id}", headers=headers)
    assert r.json()["ya_conversada"] is False

    r = client.post(f"/apoderado/agenda-familiar/{perfil_id}/conversada", headers=headers)
    assert r.status_code == 204

    r = client.get(f"/apoderado/agenda-familiar/{perfil_id}", headers=headers)
    assert r.json()["ya_conversada"] is True


def test_marcar_conversada_es_idempotente(client, session):
    perfil_id, headers = _preparar(client, session)
    client.post(f"/apoderado/agenda-familiar/{perfil_id}/conversada", headers=headers)
    r = client.post(f"/apoderado/agenda-familiar/{perfil_id}/conversada", headers=headers)
    assert r.status_code == 204


def test_agenda_familiar_de_alumno_ajeno_da_403(client, session):
    perfil_id, _ = _preparar(client, session)
    token_b = client.post(
        "/auth/registro", json={"email": f"ajeno.agenda.{next(_CONTADOR_EMAILS)}@test.cl", "password": "ClaveSegura123", "nombre": "Otro"}
    ).json()["access_token"]
    r = client.get(f"/apoderado/agenda-familiar/{perfil_id}", headers={"Authorization": f"Bearer {token_b}"})
    assert r.status_code == 403


def test_agenda_familiar_sin_sesion_da_401(client, session):
    perfil_id, _ = _preparar(client, session)
    r = client.get(f"/apoderado/agenda-familiar/{perfil_id}")
    assert r.status_code == 401
