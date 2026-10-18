"""Fase 1, ítem 2.1 del plan de incorporación de hallazgos de Brincus — simulacro con
fecha programada por el Admin. Ver planificacion/27-plan-incorporacion-hallazgos-brincus.md."""

from datetime import datetime, timedelta, timezone

from app.infrastructure.persistence.orm_models import Asignatura, ConjuntoEvaluacion, CuentaAdmin, Nivel, Pregunta
from app.infrastructure.seguridad.bcrypt_hasheador import HasheadorPasswordBcrypt

_CONTADOR_EMAILS = iter(range(1, 100_000))


def _headers_admin(client, session, email="admin.simulacro@logos.cl"):
    cuenta = CuentaAdmin(email=email, nombre="Admin Test", password_hash=HasheadorPasswordBcrypt().hashear("ClaveAdmin123"))
    session.add(cuenta)
    session.commit()
    token = client.post("/admin/auth/login", json={"email": email, "password": "ClaveAdmin123"}).json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


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

    conjunto = ConjuntoEvaluacion(
        tipo="examen_simulacro", asignatura_id=asignatura.id, nombre="Simulacro programado",
        pregunta_ids=[pregunta.id],
    )
    session.add(conjunto)
    session.commit()
    session.refresh(conjunto)

    email = f"apoderado.simulacro.{next(_CONTADOR_EMAILS)}@test.cl"
    token = client.post(
        "/auth/registro", json={"email": email, "password": "ClaveSegura123", "nombre": "Apoderado Test"}
    ).json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    perfil_id = client.post(
        "/auth/alumnos", headers=headers,
        json={"nombre": "Test", "apellidos": "Test", "fecha_nacimiento": "2016-01-01", "rut": "1-9", "nivel_id": nivel.id},
    ).json()["id"]

    return nivel, asignatura, conjunto, perfil_id, headers


def test_programar_fecha_requiere_sesion_admin(client, session):
    _, _, conjunto, _, _ = _preparar(client, session)
    r = client.patch(
        f"/admin/evaluaciones/conjuntos/{conjunto.id}/programar-fecha",
        json={"fecha_programada": None},
    )
    assert r.status_code in (401, 403)


def test_programar_fecha_de_conjunto_inexistente_da_404(client, session):
    headers_admin = _headers_admin(client, session)
    r = client.patch(
        "/admin/evaluaciones/conjuntos/999999/programar-fecha",
        headers=headers_admin,
        json={"fecha_programada": None},
    )
    assert r.status_code == 404


def test_programar_fecha_futura_y_consultarla(client, session):
    _, _, conjunto, _, _ = _preparar(client, session)
    headers_admin = _headers_admin(client, session)
    futuro = (datetime.now(timezone.utc) + timedelta(days=10)).isoformat()

    r = client.patch(
        f"/admin/evaluaciones/conjuntos/{conjunto.id}/programar-fecha",
        headers=headers_admin,
        json={"fecha_programada": futuro},
    )
    assert r.status_code == 200
    assert r.json()["fecha_programada"] is not None


def test_simulacro_con_fecha_futura_aparece_no_habilitado_en_faltantes(client, session):
    nivel, asignatura, conjunto, perfil_id, headers = _preparar(client, session)
    headers_admin = _headers_admin(client, session)
    futuro = (datetime.now(timezone.utc) + timedelta(days=10)).isoformat()
    client.patch(
        f"/admin/evaluaciones/conjuntos/{conjunto.id}/programar-fecha",
        headers=headers_admin,
        json={"fecha_programada": futuro},
    )

    r = client.get(f"/progreso/{perfil_id}/faltantes", params={"nivel_id": nivel.id}, headers=headers)
    assert r.status_code == 200
    faltante = next(f for f in r.json()["faltantes"] if f["conjunto_id"] == conjunto.id)
    assert faltante["habilitado"] is False
    assert faltante["fecha_programada"] is not None


def test_quitar_fecha_programada_con_null_vuelve_a_disponibilidad_normal(client, session):
    nivel, asignatura, conjunto, perfil_id, headers = _preparar(client, session)
    headers_admin = _headers_admin(client, session)
    futuro = (datetime.now(timezone.utc) + timedelta(days=10)).isoformat()
    client.patch(
        f"/admin/evaluaciones/conjuntos/{conjunto.id}/programar-fecha",
        headers=headers_admin, json={"fecha_programada": futuro},
    )

    r = client.patch(
        f"/admin/evaluaciones/conjuntos/{conjunto.id}/programar-fecha",
        headers=headers_admin, json={"fecha_programada": None},
    )
    assert r.status_code == 200
    assert r.json()["fecha_programada"] is None
