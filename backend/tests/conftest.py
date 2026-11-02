import os

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.engine import make_url
from sqlmodel import Session, SQLModel, create_engine

from app.core.config import settings
from app.infrastructure.persistence.db import get_session
from app.core.limiter import limiter
from app.main import app

TEST_DATABASE_URL = os.environ.get(
    "LOGOS_TEST_DATABASE_URL",
    "postgresql://logos_dev:logos_dev_local@localhost:5432/logos_test",
)
_test_url = make_url(TEST_DATABASE_URL)
if _test_url.host not in {"localhost", "127.0.0.1", "::1"} or _test_url.database not in {
    "logos_test", "logos_auditoria_test"
}:
    raise RuntimeError("Las fixtures destructivas requieren una base local de pruebas autorizada.")
engine_test = create_engine(TEST_DATABASE_URL)


@pytest.fixture(autouse=True)
def _tablas_limpias():
    SQLModel.metadata.drop_all(engine_test)
    SQLModel.metadata.create_all(engine_test)
    limiter.reset()  # el rate-limit (5/min en /auth/registro) no debe acumularse entre tests
    yield
    SQLModel.metadata.drop_all(engine_test)


@pytest.fixture(autouse=True)
def _sin_correo_real(monkeypatch):
    """El `.env` local de Desarrollo puede traer una RESEND_API_KEY real (para que la app
    mande correos de verdad al usarla a mano) — los tests no deben depender de la red ni
    golpear la API real de Resend en cada registro (son decenas por corrida). `_enviar()` ya
    trata la clave vacía como "no configurada" y solo registra el correo en el log."""
    monkeypatch.setattr(settings, "resend_api_key", "")


@pytest.fixture()
def session():
    with Session(engine_test) as s:
        yield s


@pytest.fixture()
def client(session):
    def _get_session_override():
        yield session

    app.dependency_overrides[get_session] = _get_session_override
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()
