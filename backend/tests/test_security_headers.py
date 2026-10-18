"""Auditoría de seguridad (2026-08-17): la API no enviaba ningún encabezado de seguridad
del navegador. Ver `app/core/security_headers.py`."""


def test_respuesta_incluye_encabezados_de_seguridad(client):
    r = client.get("/contenido/niveles")
    assert r.status_code == 200
    assert r.headers["X-Content-Type-Options"] == "nosniff"
    assert r.headers["X-Frame-Options"] == "DENY"
    assert r.headers["Referrer-Policy"] == "strict-origin-when-cross-origin"
    assert "geolocation=()" in r.headers["Permissions-Policy"]


def test_encabezados_de_seguridad_tambien_en_respuestas_de_error(client):
    """No deben depender de que el request haya sido exitoso — un 401/404 también debe
    llevarlos, ya que un atacante puede aprender de las respuestas de error igual."""
    r = client.get("/auth/yo")
    assert r.status_code == 401
    assert r.headers["X-Frame-Options"] == "DENY"
