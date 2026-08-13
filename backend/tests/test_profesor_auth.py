from app.infrastructure.persistence.orm_models import CuentaAdmin
from app.infrastructure.seguridad.bcrypt_hasheador import HasheadorPasswordBcrypt


def _token_admin(client, session, email="admin@logos.cl"):
    cuenta = CuentaAdmin(email=email, nombre="Admin Test", password_hash=HasheadorPasswordBcrypt().hashear("ClaveAdmin123"))
    session.add(cuenta)
    session.commit()
    r = client.post("/admin/auth/login", json={"email": email, "password": "ClaveAdmin123"})
    return r.json()["access_token"]


def test_registro_profesor_nace_pendiente(client):
    r = client.post("/profesor/auth/registro", json={"email": "prof@test.cl", "password": "ClaveProfe123", "nombre": "Profe Test"})
    assert r.status_code == 201
    token = r.json()["access_token"]

    r = client.get("/profesor/auth/yo", headers={"Authorization": f"Bearer {token}"})
    assert r.status_code == 200
    assert r.json()["estado"] == "pendiente"


def test_registro_duplicado_falla(client):
    datos = {"email": "prof2@test.cl", "password": "ClaveProfe123", "nombre": "Profe Test"}
    client.post("/profesor/auth/registro", json=datos)
    r = client.post("/profesor/auth/registro", json=datos)
    assert r.status_code == 400


def test_login_profesor_correcto(client):
    client.post("/profesor/auth/registro", json={"email": "prof3@test.cl", "password": "ClaveProfe123", "nombre": "Profe Test"})
    r = client.post("/profesor/auth/login", json={"email": "prof3@test.cl", "password": "ClaveProfe123"})
    assert r.status_code == 200
    assert "access_token" in r.json()


def test_login_profesor_password_incorrecta(client):
    client.post("/profesor/auth/registro", json={"email": "prof4@test.cl", "password": "ClaveProfe123", "nombre": "Profe Test"})
    r = client.post("/profesor/auth/login", json={"email": "prof4@test.cl", "password": "otraClave"})
    assert r.status_code == 401


def test_crear_curso_con_cuenta_pendiente_da_403(client):
    r = client.post("/profesor/auth/registro", json={"email": "prof5@test.cl", "password": "ClaveProfe123", "nombre": "Profe Test"})
    token = r.json()["access_token"]
    r = client.post(
        "/profesor/cursos", headers={"Authorization": f"Bearer {token}"},
        json={"nivel_id": 1, "nombre": "6° básico A"},
    )
    assert r.status_code == 403


def test_token_de_profesor_no_sirve_en_endpoints_de_apoderado_ni_admin(client, session):
    r = client.post("/profesor/auth/registro", json={"email": "prof6@test.cl", "password": "ClaveProfe123", "nombre": "Profe Test"})
    token_profesor = r.json()["access_token"]

    r = client.get("/auth/yo", headers={"Authorization": f"Bearer {token_profesor}"})
    assert r.status_code == 401

    r = client.get("/admin/planes", headers={"Authorization": f"Bearer {token_profesor}"})
    assert r.status_code in (401, 403)


def test_token_de_apoderado_no_sirve_en_endpoints_de_profesor(client):
    token_apoderado = client.post(
        "/auth/registro", json={"email": "familia.profesor@test.cl", "password": "ClaveSegura123", "nombre": "Apoderado"}
    ).json()["access_token"]

    r = client.get("/profesor/auth/yo", headers={"Authorization": f"Bearer {token_apoderado}"})
    assert r.status_code == 401


def test_token_admin_no_sirve_en_endpoints_de_profesor(client, session):
    token_admin = _token_admin(client, session)
    r = client.get("/profesor/auth/yo", headers={"Authorization": f"Bearer {token_admin}"})
    assert r.status_code == 401
