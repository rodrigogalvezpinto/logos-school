"""Fase 1, ítem 2.3 del plan de incorporación de hallazgos de Brincus — onboarding con
checklist de primera sesión. Ver planificacion/27-plan-incorporacion-hallazgos-brincus.md."""

from app.infrastructure.persistence.orm_models import Nivel

_CONTADOR_EMAILS = iter(range(1, 100_000))


def _preparar(client, session):
    nivel = Nivel(
        nombre="4° básico", regimen="A", decreto="439/2012", formato_examen="integrado",
        num_preguntas_examen=20, duracion_examen_min=90,
    )
    session.add(nivel)
    session.commit()
    session.refresh(nivel)

    email = f"apoderado.onboarding.{next(_CONTADOR_EMAILS)}@test.cl"
    token = client.post(
        "/auth/registro", json={"email": email, "password": "ClaveSegura123", "nombre": "Apoderado Test"}
    ).json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    perfil_id = client.post(
        "/auth/alumnos", headers=headers,
        json={"nombre": "Test", "apellidos": "Test", "fecha_nacimiento": "2016-01-01", "rut": "1-9", "nivel_id": nivel.id},
    ).json()["id"]

    return perfil_id, headers


def test_progreso_nace_vacio(client, session):
    perfil_id, headers = _preparar(client, session)
    r = client.get(f"/onboarding/{perfil_id}", headers=headers)
    assert r.status_code == 200
    body = r.json()
    assert body["pasos_completados"] == []
    assert body["completo"] is False
    assert set(body["pasos"]) == {"ver_guia", "autoevaluacion", "plan_estudio", "elegir_avatar"}


def test_completar_un_paso(client, session):
    perfil_id, headers = _preparar(client, session)
    r = client.post(f"/onboarding/{perfil_id}/pasos/ver_guia/completar", headers=headers)
    assert r.status_code == 200
    assert r.json()["pasos_completados"] == ["ver_guia"]
    assert r.json()["completo"] is False


def test_completar_un_paso_dos_veces_no_lo_duplica(client, session):
    perfil_id, headers = _preparar(client, session)
    client.post(f"/onboarding/{perfil_id}/pasos/ver_guia/completar", headers=headers)
    r = client.post(f"/onboarding/{perfil_id}/pasos/ver_guia/completar", headers=headers)
    assert r.json()["pasos_completados"] == ["ver_guia"]


def test_completar_los_4_pasos_marca_completo(client, session):
    perfil_id, headers = _preparar(client, session)
    for paso in ["ver_guia", "autoevaluacion", "plan_estudio", "elegir_avatar"]:
        client.post(f"/onboarding/{perfil_id}/pasos/{paso}/completar", headers=headers)

    r = client.get(f"/onboarding/{perfil_id}", headers=headers)
    assert r.json()["completo"] is True
    assert sorted(r.json()["pasos_completados"]) == ["autoevaluacion", "elegir_avatar", "plan_estudio", "ver_guia"]


def test_completar_paso_invalido_da_400(client, session):
    perfil_id, headers = _preparar(client, session)
    r = client.post(f"/onboarding/{perfil_id}/pasos/no-existe/completar", headers=headers)
    assert r.status_code == 400


def test_onboarding_de_alumno_ajeno_da_403(client, session):
    perfil_id, _ = _preparar(client, session)
    email_b = f"apoderado.onboarding.ajeno.{next(_CONTADOR_EMAILS)}@test.cl"
    token_b = client.post(
        "/auth/registro", json={"email": email_b, "password": "ClaveSegura123", "nombre": "Otro"}
    ).json()["access_token"]
    headers_b = {"Authorization": f"Bearer {token_b}"}
    r = client.get(f"/onboarding/{perfil_id}", headers=headers_b)
    assert r.status_code == 403


def test_onboarding_sin_sesion_da_401(client, session):
    perfil_id, _ = _preparar(client, session)
    r = client.get(f"/onboarding/{perfil_id}")
    assert r.status_code == 401
