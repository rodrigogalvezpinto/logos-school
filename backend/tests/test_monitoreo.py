"""Sentry no recibe datos personales (2026-11-22)."""

from app.core import monitoreo
from app.core.config import settings


def test_sin_dsn_no_se_activa(monkeypatch):
    monkeypatch.setattr(settings, "sentry_dsn", "")
    assert monitoreo.iniciar_monitoreo() is False


def test_el_evento_pierde_datos_personales():
    evento = {
        "request": {
            "url": "https://api.x.cl/auth/restablecer-password",
            "query_string": "token=secreto",
            "data": {"password": "x", "rut": "1-9"},
            "cookies": {"a": "b"},
            "headers": {"Authorization": "Bearer abc", "User-Agent": "Mozilla", "Cookie": "c"},
        },
        "user": {"email": "mama@x.cl"},
        "exception": {"values": [{"type": "ValueError"}]},
    }
    limpio = monitoreo.limpiar_evento(evento)
    r = limpio["request"]
    assert "data" not in r and "cookies" not in r and r["query_string"] == ""
    assert r["headers"] == {"User-Agent": "Mozilla"}
    assert "user" not in limpio
    assert limpio["exception"]["values"][0]["type"] == "ValueError"
