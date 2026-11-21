"""«¿Olvidaste tu contraseña?» (2026-11-21): enlace por correo, de un solo uso y que vence en 1 hora."""

from datetime import datetime, timedelta, timezone

from jose import jwt

from app.core.config import settings
from app.routers import auth as router_auth

EMAIL = "mama.recupera@ejemplo.cl"


def _registrar(client):
    r = client.post("/auth/registro", json={"email": EMAIL, "password": "ClaveVieja123", "nombre": "Mamá"})
    assert r.status_code == 201
    return r.json()["access_token"]


def _pedir_enlace(client, monkeypatch, email=EMAIL):
    enviados = []
    monkeypatch.setattr(router_auth, "enviar_recuperacion_password", lambda d, n, e: enviados.append((d, n, e)))
    r = client.post("/auth/recuperar-password", json={"email": email})
    assert r.status_code == 202
    return r, enviados


def test_flujo_completo_cambia_la_clave_y_cierra_sesiones(client, monkeypatch):
    token_sesion = _registrar(client)
    _, enviados = _pedir_enlace(client, monkeypatch)
    assert len(enviados) == 1 and enviados[0][0] == EMAIL
    enlace = enviados[0][2]
    assert "/restablecer?token=" in enlace
    token = enlace.split("token=")[1]

    assert client.post("/auth/restablecer-password", json={"token": token, "password": "ClaveNueva456"}).status_code == 204
    assert client.post("/auth/login", json={"email": EMAIL, "password": "ClaveVieja123"}).status_code == 401
    assert client.post("/auth/login", json={"email": EMAIL, "password": "ClaveNueva456"}).status_code == 200
    # La sesión abierta antes del cambio queda cerrada.
    assert client.get("/auth/yo", headers={"Authorization": f"Bearer {token_sesion}"}).status_code == 401
    # El enlace es de un solo uso.
    r = client.post("/auth/restablecer-password", json={"token": token, "password": "OtraClave789"})
    assert r.status_code == 400


def test_correo_inexistente_responde_igual_y_no_envia_nada(client, monkeypatch):
    _registrar(client)
    r_existe, _ = _pedir_enlace(client, monkeypatch)
    r_no, enviados = _pedir_enlace(client, monkeypatch, "nadie@ejemplo.cl")
    assert enviados == []
    assert r_no.json() == r_existe.json()


def test_enlace_vencido_alterado_o_de_sesion_no_sirve(client, monkeypatch):
    token_sesion = _registrar(client)
    vencido = jwt.encode(
        {"sub": "1", "ver": 0, "tipo": "recuperar", "exp": datetime.now(timezone.utc) - timedelta(minutes=1)},
        settings.jwt_secret, algorithm=settings.jwt_algoritmo,
    )
    for token in (vencido, "x" * 40, token_sesion):
        r = client.post("/auth/restablecer-password", json={"token": token, "password": "ClaveNueva456"})
        assert r.status_code == 400, token


def test_el_enlace_no_sirve_como_sesion(client, monkeypatch):
    _registrar(client)
    _, enviados = _pedir_enlace(client, monkeypatch)
    token = enviados[0][2].split("token=")[1]
    assert client.get("/auth/yo", headers={"Authorization": f"Bearer {token}"}).status_code == 401


def test_clave_nueva_corta_se_rechaza(client, monkeypatch):
    _registrar(client)
    _, enviados = _pedir_enlace(client, monkeypatch)
    token = enviados[0][2].split("token=")[1]
    assert client.post("/auth/restablecer-password", json={"token": token, "password": "corta"}).status_code == 422


def test_url_publica_usa_url_frontend_o_el_primer_origen(monkeypatch):
    monkeypatch.setattr(settings, "url_frontend", "")
    monkeypatch.setattr(settings, "cors_origenes", "https://logosschool.cl/, https://www.logosschool.cl")
    assert settings.url_publica_frontend == "https://logosschool.cl"
    monkeypatch.setattr(settings, "url_frontend", "https://app.logosschool.cl/")
    assert settings.url_publica_frontend == "https://app.logosschool.cl"
