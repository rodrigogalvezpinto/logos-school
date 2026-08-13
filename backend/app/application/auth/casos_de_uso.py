"""Casos de uso del contexto Auth — orquestan entidades + puertos. Cada uno depende
solo de los puertos que necesita (ISP), nunca de un adaptador concreto (DIP)."""

from datetime import date

from app.domain.auth.entities import Cuenta, PerfilAlumno
from app.domain.auth.exceptions import CorreoYaRegistrado, CredencialesInvalidas
from app.domain.auth.ports import (
    HasheadorPassword,
    RepositorioCuentas,
    RepositorioPerfilesAlumno,
    ServicioToken,
    VerificadorTokenGoogle,
)
from app.domain.auth.value_objects import Rut


class RegistrarApoderado:
    def __init__(
        self,
        repositorio_cuentas: RepositorioCuentas,
        hasheador: HasheadorPassword,
        servicio_token: ServicioToken,
    ):
        self._repositorio_cuentas = repositorio_cuentas
        self._hasheador = hasheador
        self._servicio_token = servicio_token

    def ejecutar(
        self,
        email: str,
        password: str,
        nombre: str,
        comuna_o_region: str | None,
        pais: str | None,
    ) -> str:
        if self._repositorio_cuentas.buscar_por_email(email):
            raise CorreoYaRegistrado()
        cuenta = Cuenta.crear_con_password(
            email=email,
            nombre=nombre,
            password_hash=self._hasheador.hashear(password),
            comuna_o_region=comuna_o_region,
            pais=pais,
        )
        cuenta = self._repositorio_cuentas.guardar(cuenta)
        return self._servicio_token.generar(cuenta.id)


class IniciarSesion:
    def __init__(
        self,
        repositorio_cuentas: RepositorioCuentas,
        hasheador: HasheadorPassword,
        servicio_token: ServicioToken,
    ):
        self._repositorio_cuentas = repositorio_cuentas
        self._hasheador = hasheador
        self._servicio_token = servicio_token

    def ejecutar(self, email: str, password: str) -> str:
        cuenta = self._repositorio_cuentas.buscar_por_email(email)
        credenciales_validas = (
            cuenta is not None
            and cuenta.password_hash is not None
            and self._hasheador.verificar(password, cuenta.password_hash)
        )
        if not credenciales_validas:
            # Mensaje genérico a propósito: no revelar si el correo existe o no (evita
            # que un atacante use el login para enumerar cuentas registradas).
            raise CredencialesInvalidas()
        return self._servicio_token.generar(cuenta.id)


class IniciarSesionConGoogle:
    def __init__(
        self,
        repositorio_cuentas: RepositorioCuentas,
        verificador_google: VerificadorTokenGoogle,
        servicio_token: ServicioToken,
    ):
        self._repositorio_cuentas = repositorio_cuentas
        self._verificador_google = verificador_google
        self._servicio_token = servicio_token

    def ejecutar(self, id_token: str) -> str:
        # GoogleLoginNoConfigurado/TokenGoogleInvalido se propagan tal cual desde el
        # adaptador — son excepciones de dominio, el puerto solo delega su origen.
        info = self._verificador_google.verificar(id_token)

        cuenta = self._repositorio_cuentas.buscar_por_google_id(info.google_id)
        if not cuenta:
            cuenta = self._repositorio_cuentas.buscar_por_email(info.email)
            if cuenta:
                cuenta.vincular_google(info.google_id)  # vincula Google a una cuenta ya existente con ese correo
            else:
                cuenta = Cuenta.crear_con_google(email=info.email, nombre=info.nombre, google_id=info.google_id)
            cuenta = self._repositorio_cuentas.guardar(cuenta)

        return self._servicio_token.generar(cuenta.id)


class AgregarPerfilAlumno:
    def __init__(self, repositorio_perfiles: RepositorioPerfilesAlumno):
        self._repositorio_perfiles = repositorio_perfiles

    def ejecutar(
        self,
        cuenta_apoderado_id: int,
        nombre: str,
        apellidos: str,
        fecha_nacimiento: date,
        rut: Rut,
        nivel_id: int,
    ) -> PerfilAlumno:
        perfil = PerfilAlumno.crear(
            cuenta_apoderado_id=cuenta_apoderado_id,
            nombre=nombre,
            apellidos=apellidos,
            fecha_nacimiento=fecha_nacimiento,
            rut=rut,
            nivel_id=nivel_id,
        )
        return self._repositorio_perfiles.guardar(perfil)


class ListarPerfilesAlumno:
    def __init__(self, repositorio_perfiles: RepositorioPerfilesAlumno):
        self._repositorio_perfiles = repositorio_perfiles

    def ejecutar(self, cuenta_apoderado_id: int) -> list[PerfilAlumno]:
        return self._repositorio_perfiles.listar_por_cuenta(cuenta_apoderado_id)
