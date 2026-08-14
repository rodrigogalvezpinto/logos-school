"""Cierra el vacío de test que tenía el flujo de account-linking de login-google: antes
vivía inline en el router sin ningún test. Usa fakes en memoria para los tres puertos —
cero base de datos, cero red."""

from app.application.auth.casos_de_uso import IniciarSesionConGoogle
from app.domain.auth.entities import Cuenta
from app.domain.auth.exceptions import GoogleLoginNoConfigurado, TokenGoogleInvalido
from app.domain.auth.ports import InfoGoogle
import pytest


class FakeRepositorioCuentas:
    def __init__(self, cuentas: list[Cuenta] | None = None):
        self._cuentas = cuentas or []
        self._siguiente_id = max([c.id for c in self._cuentas if c.id], default=0) + 1

    def buscar_por_email(self, email):
        return next((c for c in self._cuentas if c.email == email), None)

    def buscar_por_google_id(self, google_id):
        return next((c for c in self._cuentas if c.google_id == google_id), None)

    def buscar_por_id(self, cuenta_id):
        return next((c for c in self._cuentas if c.id == cuenta_id), None)

    def guardar(self, cuenta):
        if cuenta.id is None:
            cuenta.id = self._siguiente_id
            self._siguiente_id += 1
            self._cuentas.append(cuenta)
        return cuenta


class FakeVerificadorGoogle:
    def __init__(self, info: InfoGoogle | None = None, error: Exception | None = None):
        self._info = info
        self._error = error

    def verificar(self, id_token):
        if self._error:
            raise self._error
        return self._info


class FakeServicioToken:
    def generar(self, cuenta_id, sesion_version=0):
        return f"token-de-{cuenta_id}"

    def decodificar(self, token):
        raise NotImplementedError

    def decodificar_con_version(self, token):
        raise NotImplementedError


def test_google_no_configurado_propaga_la_excepcion_de_dominio():
    uc = IniciarSesionConGoogle(
        FakeRepositorioCuentas(), FakeVerificadorGoogle(error=GoogleLoginNoConfigurado()), FakeServicioToken()
    )
    with pytest.raises(GoogleLoginNoConfigurado):
        uc.ejecutar("cualquier-token")


def test_token_invalido_propaga_la_excepcion_de_dominio():
    uc = IniciarSesionConGoogle(
        FakeRepositorioCuentas(), FakeVerificadorGoogle(error=TokenGoogleInvalido()), FakeServicioToken()
    )
    with pytest.raises(TokenGoogleInvalido):
        uc.ejecutar("token-malo")


def test_google_id_ya_registrado_no_crea_cuenta_nueva():
    existente = Cuenta.crear_con_google(email="a@test.cl", nombre="A", google_id="g-1")
    existente.id = 1
    repo = FakeRepositorioCuentas([existente])
    verificador = FakeVerificadorGoogle(info=InfoGoogle(google_id="g-1", email="a@test.cl", nombre="A"))

    uc = IniciarSesionConGoogle(repo, verificador, FakeServicioToken())
    token = uc.ejecutar("token-valido")

    assert token == "token-de-1"
    assert len(repo._cuentas) == 1


def test_correo_existente_sin_google_se_vincula_en_vez_de_duplicar():
    existente = Cuenta.crear_con_password(email="a@test.cl", nombre="A", password_hash="hash")
    existente.id = 1
    repo = FakeRepositorioCuentas([existente])
    verificador = FakeVerificadorGoogle(info=InfoGoogle(google_id="g-nuevo", email="a@test.cl", nombre="A"))

    uc = IniciarSesionConGoogle(repo, verificador, FakeServicioToken())
    token = uc.ejecutar("token-valido")

    assert token == "token-de-1"
    assert len(repo._cuentas) == 1
    assert repo.buscar_por_id(1).google_id == "g-nuevo"


def test_correo_y_google_id_desconocidos_crea_cuenta_nueva():
    repo = FakeRepositorioCuentas()
    verificador = FakeVerificadorGoogle(info=InfoGoogle(google_id="g-2", email="nueva@test.cl", nombre="Nueva"))

    uc = IniciarSesionConGoogle(repo, verificador, FakeServicioToken())
    uc.ejecutar("token-valido")

    assert len(repo._cuentas) == 1
    assert repo._cuentas[0].email == "nueva@test.cl"
    assert repo._cuentas[0].google_id == "g-2"
