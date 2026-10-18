from app.core.config import settings
from app.infrastructure.persistence.orm_models import CuentaAdmin
from app.infrastructure.seguridad.bcrypt_hasheador import HasheadorPasswordBcrypt


def _crear_cuenta_admin(session, email="admin@logos.cl", password="ClaveAdmin123"):
    cuenta = CuentaAdmin(email=email, nombre="Admin Test", password_hash=HasheadorPasswordBcrypt().hashear(password))
    session.add(cuenta)
    session.commit()
    session.refresh(cuenta)
    return cuenta


def test_login_admin_correcto_devuelve_token(client, session):
    _crear_cuenta_admin(session)
    r = client.post("/admin/auth/login", json={"email": "admin@logos.cl", "password": "ClaveAdmin123"})
    assert r.status_code == 200
    assert "access_token" in r.json()


def test_login_admin_password_incorrecta(client, session):
    _crear_cuenta_admin(session)
    r = client.post("/admin/auth/login", json={"email": "admin@logos.cl", "password": "otraClave"})
    assert r.status_code == 401


def test_login_admin_correo_inexistente(client, session):
    r = client.post("/admin/auth/login", json={"email": "nadie@logos.cl", "password": "loquesea"})
    assert r.status_code == 401


def test_no_existe_endpoint_de_auto_registro_admin(client):
    r = client.post("/admin/auth/registro", json={})
    assert r.status_code == 404


def test_yo_admin_con_token_devuelve_cuenta(client, session):
    _crear_cuenta_admin(session)
    token = client.post("/admin/auth/login", json={"email": "admin@logos.cl", "password": "ClaveAdmin123"}).json()["access_token"]
    r = client.get("/admin/auth/yo", headers={"Authorization": f"Bearer {token}"})
    assert r.status_code == 200
    assert r.json()["email"] == "admin@logos.cl"


def test_token_de_apoderado_no_sirve_para_endpoints_admin(client, session):
    _crear_cuenta_admin(session)
    token_apoderado = client.post(
        "/auth/registro", json={"email": "familia@test.cl", "password": "ClaveSegura123", "nombre": "Apoderado"}
    ).json()["access_token"]

    r = client.get("/admin/auth/yo", headers={"Authorization": f"Bearer {token_apoderado}"})
    assert r.status_code == 401

    r = client.get("/admin/planes", headers={"Authorization": f"Bearer {token_apoderado}"})
    assert r.status_code == 401


def test_token_admin_no_sirve_para_endpoints_de_apoderado(client, session):
    _crear_cuenta_admin(session)
    token_admin = client.post(
        "/admin/auth/login", json={"email": "admin@logos.cl", "password": "ClaveAdmin123"}
    ).json()["access_token"]

    r = client.get("/auth/yo", headers={"Authorization": f"Bearer {token_admin}"})
    assert r.status_code == 401

    r = client.get("/auth/alumnos", headers={"Authorization": f"Bearer {token_admin}"})
    assert r.status_code == 401


def test_login_admin_da_429_al_pasar_el_limite_configurado(client, session):
    """Auditoría de seguridad (2026-08-17): el login de Admin —la cuenta de mayor
    privilegio de todo el sistema— no tenía NINGUNA protección contra fuerza bruta antes de
    esto. El límite se lee de `settings.limite_admin_login_por_minuto`, mismo criterio que
    el resto de endpoints de auth (ver `test_auth.py`)."""
    _crear_cuenta_admin(session)

    limite = settings.limite_admin_login_por_minuto
    for _ in range(limite):
        r = client.post("/admin/auth/login", json={"email": "admin@logos.cl", "password": "clave-mala"})
        assert r.status_code == 401

    r = client.post("/admin/auth/login", json={"email": "admin@logos.cl", "password": "clave-mala"})
    assert r.status_code == 429
