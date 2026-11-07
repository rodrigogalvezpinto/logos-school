"""CORS configurable por ambiente: sin esto la app desplegada no podía llamar a la API (2026-11-07)."""
from app.core.config import Settings


def test_desarrollo_acepta_localhost_y_los_extra():
    s = Settings(entorno="desarrollo", cors_origenes="https://logosschool.cl/")
    assert "http://localhost:4300" in s.origenes_permitidos
    assert "https://logosschool.cl" in s.origenes_permitidos


def test_produccion_solo_acepta_el_dominio_real():
    s = Settings(entorno="produccion", jwt_secret="x" * 40,
                 cors_origenes="https://logosschool.cl, https://www.logosschool.cl")
    assert s.origenes_permitidos == ["https://logosschool.cl", "https://www.logosschool.cl"]


def test_sin_variable_quedan_los_locales():
    assert Settings(entorno="desarrollo").origenes_permitidos[0] == "http://localhost:4300"
