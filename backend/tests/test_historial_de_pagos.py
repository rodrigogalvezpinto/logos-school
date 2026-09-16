"""Fase 1, ítem 2.8 del plan de incorporación de hallazgos de Brincus — historial de
pagos para el Apoderado, con los datos que ya existen hoy. Ver
planificacion/27-plan-incorporacion-hallazgos-brincus.md."""

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

    email = f"apoderado.pagos.{next(_CONTADOR_EMAILS)}@test.cl"
    token = client.post(
        "/auth/registro", json={"email": email, "password": "ClaveSegura123", "nombre": "Apoderado Test"}
    ).json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    perfil_id = client.post(
        "/auth/alumnos", headers=headers,
        json={"nombre": "Test", "apellidos": "Test", "fecha_nacimiento": "2016-01-01", "rut": "1-9", "nivel_id": nivel.id},
    ).json()["id"]

    return nivel, perfil_id, headers


def test_sin_suscripcion_devuelve_null(client, session):
    _, perfil_id, headers = _preparar(client, session)
    r = client.get(f"/auth/alumnos/{perfil_id}/suscripcion", headers=headers)
    assert r.status_code == 200
    assert r.json() is None


def test_con_prueba_gratis_activa_muestra_la_suscripcion(client, session):
    from app.infrastructure.persistence.orm_models import Plan

    nivel, perfil_id, headers = _preparar(client, session)
    plan = Plan(nombre="Mensual", nivel_de_acceso="completo", precio_clp=19990)
    session.add(plan)
    session.commit()
    session.refresh(plan)

    client.post(
        f"/auth/alumnos/{perfil_id}/prueba-gratis", headers=headers, json={"plan_id": plan.id},
    )

    r = client.get(f"/auth/alumnos/{perfil_id}/suscripcion", headers=headers)
    assert r.status_code == 200
    body = r.json()
    assert body["plan_nombre"] == "Mensual"
    assert body["origen"] == "prueba_gratis"
    assert body["estado"] == "activa"
    assert body["fecha_termino"] is not None


def test_suscripcion_de_alumno_ajeno_da_403(client, session):
    _, perfil_id, _ = _preparar(client, session)
    email_b = f"apoderado.pagos.ajeno.{next(_CONTADOR_EMAILS)}@test.cl"
    token_b = client.post(
        "/auth/registro", json={"email": email_b, "password": "ClaveSegura123", "nombre": "Otro"}
    ).json()["access_token"]
    headers_b = {"Authorization": f"Bearer {token_b}"}
    r = client.get(f"/auth/alumnos/{perfil_id}/suscripcion", headers=headers_b)
    assert r.status_code == 403


def test_suscripcion_sin_sesion_da_401(client, session):
    _, perfil_id, _ = _preparar(client, session)
    r = client.get(f"/auth/alumnos/{perfil_id}/suscripcion")
    assert r.status_code == 401
