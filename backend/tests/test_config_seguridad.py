"""Auditoría de seguridad (2026-08-17): la app no debe poder arrancar en Producción con el
JWT_SECRET por defecto (público en el repo) — ver `app/core/config.py`."""

import pytest

from app.core.config import Settings


def test_produccion_sin_jwt_secret_propio_no_arranca():
    with pytest.raises(ValueError, match="JWT_SECRET"):
        Settings(_env_file=None, entorno="produccion")


def test_produccion_con_jwt_secret_propio_arranca_normal():
    settings = Settings(_env_file=None, entorno="produccion", jwt_secret="un-secreto-real-y-largo")
    assert settings.jwt_secret == "un-secreto-real-y-largo"


def test_desarrollo_sin_jwt_secret_propio_arranca_igual():
    """El valor por defecto es válido en Desarrollo — la protección es solo para
    Producción, donde el riesgo real (tokens forjables por cualquiera) existe."""
    settings = Settings(_env_file=None, entorno="desarrollo")
    assert settings.jwt_secret  # no vacío, aunque sea el valor por defecto
