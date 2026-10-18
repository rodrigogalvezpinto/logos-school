"""Fase 1, ítem 2.4 del plan de incorporación de hallazgos de Brincus — check-in
emocional diario. Ver planificacion/27-plan-incorporacion-hallazgos-brincus.md."""

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

    email = f"apoderado.bienestar.{next(_CONTADOR_EMAILS)}@test.cl"
    token = client.post(
        "/auth/registro", json={"email": email, "password": "ClaveSegura123", "nombre": "Apoderado Test"}
    ).json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    perfil_id = client.post(
        "/auth/alumnos", headers=headers,
        json={"nombre": "Test", "apellidos": "Test", "fecha_nacimiento": "2016-01-01", "rut": "1-9", "nivel_id": nivel.id},
    ).json()["id"]

    return perfil_id, headers


def test_sin_registro_hoy_da_registrado_false(client, session):
    perfil_id, headers = _preparar(client, session)
    r = client.get(f"/bienestar/{perfil_id}/hoy", headers=headers)
    assert r.status_code == 200
    body = r.json()
    assert body["registrado"] is False
    assert body["estado"] is None
    assert "feliz" in body["estados_disponibles"]


def test_registrar_animo_de_hoy(client, session):
    perfil_id, headers = _preparar(client, session)
    r = client.post(f"/bienestar/{perfil_id}/hoy", headers=headers, json={"estado": "feliz"})
    assert r.status_code == 200
    body = r.json()
    assert body["registrado"] is True
    assert body["estado"] == "feliz"

    r = client.get(f"/bienestar/{perfil_id}/hoy", headers=headers)
    assert r.json()["estado"] == "feliz"


def test_registrar_dos_veces_el_mismo_dia_no_sobreescribe(client, session):
    perfil_id, headers = _preparar(client, session)
    client.post(f"/bienestar/{perfil_id}/hoy", headers=headers, json={"estado": "feliz"})
    r = client.post(f"/bienestar/{perfil_id}/hoy", headers=headers, json={"estado": "triste"})
    assert r.json()["estado"] == "feliz"  # el primero del día manda


def test_estado_invalido_da_400(client, session):
    perfil_id, headers = _preparar(client, session)
    r = client.post(f"/bienestar/{perfil_id}/hoy", headers=headers, json={"estado": "furioso"})
    assert r.status_code == 400


def test_bienestar_de_alumno_ajeno_da_403(client, session):
    perfil_id, _ = _preparar(client, session)
    email_b = f"apoderado.bienestar.ajeno.{next(_CONTADOR_EMAILS)}@test.cl"
    token_b = client.post(
        "/auth/registro", json={"email": email_b, "password": "ClaveSegura123", "nombre": "Otro"}
    ).json()["access_token"]
    headers_b = {"Authorization": f"Bearer {token_b}"}
    r = client.get(f"/bienestar/{perfil_id}/hoy", headers=headers_b)
    assert r.status_code == 403


def test_bienestar_sin_sesion_da_401(client, session):
    perfil_id, _ = _preparar(client, session)
    r = client.get(f"/bienestar/{perfil_id}/hoy")
    assert r.status_code == 401
