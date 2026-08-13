from app.infrastructure.persistence.orm_models import CuentaAdmin, Nivel
from app.infrastructure.seguridad.bcrypt_hasheador import HasheadorPasswordBcrypt


def _headers_admin(client, session, email="admin@logos.cl"):
    cuenta = CuentaAdmin(email=email, nombre="Admin Test", password_hash=HasheadorPasswordBcrypt().hashear("ClaveAdmin123"))
    session.add(cuenta)
    session.commit()
    token = client.post("/admin/auth/login", json={"email": email, "password": "ClaveAdmin123"}).json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


def _registrar_profesor(client, email="prof@test.cl"):
    r = client.post("/profesor/auth/registro", json={"email": email, "password": "ClaveProfe123", "nombre": "Profe Test"})
    return r.json()["access_token"]


def test_listar_pendientes_requiere_sesion_admin(client):
    r = client.get("/admin/profesores/pendientes")
    assert r.status_code in (401, 403)


def test_listar_pendientes_incluye_profesor_recien_registrado(client, session):
    headers = _headers_admin(client, session)
    _registrar_profesor(client, "prof2@test.cl")

    r = client.get("/admin/profesores/pendientes", headers=headers)
    assert r.status_code == 200
    correos = {p["email"] for p in r.json()}
    assert "prof2@test.cl" in correos


def test_aprobar_profesor_le_permite_crear_curso(client, session):
    session.add(Nivel(
        nombre="4° básico", regimen="A", decreto="439/2012", formato_examen="integrado",
        num_preguntas_examen=20, duracion_examen_min=90,
    ))
    session.commit()

    headers_admin = _headers_admin(client, session)
    token_profesor = _registrar_profesor(client, "prof3@test.cl")
    headers_profesor = {"Authorization": f"Bearer {token_profesor}"}

    pendientes = client.get("/admin/profesores/pendientes", headers=headers_admin).json()
    profesor_id = next(p["id"] for p in pendientes if p["email"] == "prof3@test.cl")

    r = client.post(f"/admin/profesores/{profesor_id}/aprobar", headers=headers_admin)
    assert r.status_code == 200
    assert r.json()["estado"] == "aprobado"

    r = client.post("/profesor/cursos", headers=headers_profesor, json={"nivel_id": 1, "nombre": "6° básico A"})
    assert r.status_code == 201


def test_rechazar_profesor(client, session):
    headers_admin = _headers_admin(client, session)
    _registrar_profesor(client, "prof4@test.cl")

    pendientes = client.get("/admin/profesores/pendientes", headers=headers_admin).json()
    profesor_id = next(p["id"] for p in pendientes if p["email"] == "prof4@test.cl")

    r = client.post(f"/admin/profesores/{profesor_id}/rechazar", headers=headers_admin)
    assert r.status_code == 200
    assert r.json()["estado"] == "rechazado"

    pendientes_despues = client.get("/admin/profesores/pendientes", headers=headers_admin).json()
    assert profesor_id not in {p["id"] for p in pendientes_despues}


def test_aprobar_profesor_inexistente_da_404(client, session):
    headers_admin = _headers_admin(client, session)
    r = client.post("/admin/profesores/9999/aprobar", headers=headers_admin)
    assert r.status_code == 404
