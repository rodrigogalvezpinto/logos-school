"""Casos de uso del contexto Auth — orquestan entidades + puertos. Cada uno depende
solo de los puertos que necesita (ISP), nunca de un adaptador concreto (DIP)."""

from datetime import date

from app.domain.auth.entities import Cuenta, PerfilAlumno
from app.domain.auth.exceptions import CorreoYaRegistrado, CredencialesInvalidas, NivelNoEncontrado, RutYaRegistrado
from app.domain.auth.ports import (
    HasheadorPassword,
    RepositorioCuentas,
    RepositorioPerfilesAlumno,
    ServicioToken,
    VerificadorTokenGoogle,
)
from app.domain.auth.value_objects import Rut
from app.domain.contenido.ports import RepositorioContenido
from app.domain.shared.reloj import Reloj


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
        # Normalizado a minúsculas — sin esto, "a@x.cl" y "A@X.CL" pasaban como cuentas
        # distintas (bug real encontrado probando la app).
        email = email.strip().lower()
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
        return self._servicio_token.generar(cuenta.id, cuenta.sesion_version)


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
        cuenta = self._repositorio_cuentas.buscar_por_email(email.strip().lower())
        credenciales_validas = (
            cuenta is not None
            and cuenta.password_hash is not None
            and self._hasheador.verificar(password, cuenta.password_hash)
        )
        if not credenciales_validas:
            # Mensaje genérico a propósito: no revelar si el correo existe o no (evita
            # que un atacante use el login para enumerar cuentas registradas).
            raise CredencialesInvalidas()
        return self._servicio_token.generar(cuenta.id, cuenta.sesion_version)


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
        email = info.email.strip().lower()

        cuenta = self._repositorio_cuentas.buscar_por_google_id(info.google_id)
        if not cuenta:
            cuenta = self._repositorio_cuentas.buscar_por_email(email)
            if cuenta:
                cuenta.vincular_google(info.google_id)  # vincula Google a una cuenta ya existente con ese correo
            else:
                cuenta = Cuenta.crear_con_google(email=email, nombre=info.nombre, google_id=info.google_id)
            cuenta = self._repositorio_cuentas.guardar(cuenta)

        return self._servicio_token.generar(cuenta.id, cuenta.sesion_version)


class AgregarPerfilAlumno:
    def __init__(
        self,
        repositorio_perfiles: RepositorioPerfilesAlumno,
        repositorio_contenido: RepositorioContenido,
        reloj: Reloj,
    ):
        self._repositorio_perfiles = repositorio_perfiles
        self._repositorio_contenido = repositorio_contenido
        self._reloj = reloj

    def ejecutar(
        self,
        cuenta_apoderado_id: int,
        nombre: str,
        apellidos: str,
        fecha_nacimiento: date,
        rut: Rut,
        nivel_id: int,
    ) -> PerfilAlumno:
        if not self._repositorio_contenido.existe_nivel(nivel_id):
            raise NivelNoEncontrado()
        if self._repositorio_perfiles.buscar_por_rut(str(rut)):
            raise RutYaRegistrado()
        perfil = PerfilAlumno.crear(
            cuenta_apoderado_id=cuenta_apoderado_id,
            nombre=nombre,
            apellidos=apellidos,
            fecha_nacimiento=fecha_nacimiento,
            rut=rut,
            nivel_id=nivel_id,
            hoy=self._reloj.ahora().date(),
        )
        return self._repositorio_perfiles.guardar(perfil)


class CerrarSesion:
    """Invalida de inmediato todos los JWT ya emitidos para esta cuenta, incrementando
    `sesion_version` — sin esto, "cerrar sesión" solo borraba el token del lado del
    navegador, pero el mismo token seguía siendo una credencial válida en el servidor
    hasta su expiración natural (12 horas)."""

    def __init__(self, repositorio_cuentas: RepositorioCuentas):
        self._repositorio_cuentas = repositorio_cuentas

    def ejecutar(self, cuenta_id: int) -> None:
        cuenta = self._repositorio_cuentas.buscar_por_id(cuenta_id)
        if not cuenta:
            return
        cuenta.cerrar_todas_las_sesiones()
        self._repositorio_cuentas.guardar(cuenta)


class ListarPerfilesAlumno:
    def __init__(self, repositorio_perfiles: RepositorioPerfilesAlumno):
        self._repositorio_perfiles = repositorio_perfiles

    def ejecutar(self, cuenta_apoderado_id: int) -> list[PerfilAlumno]:
        return self._repositorio_perfiles.listar_por_cuenta(cuenta_apoderado_id)


class EliminarAlumno:
    """Auditoría de seguridad (2026-08-17): no existía forma de que un apoderado pidiera
    borrar los datos de un hijo — brecha real de privacidad para una app que maneja datos
    de menores (RUT, fecha de nacimiento, historial completo de evaluaciones). La
    verificación de que el perfil pertenece a la cuenta que pide el borrado ya la hace
    `verificar_perfil_propio` en el router, antes de llegar acá — este caso de uso solo
    ejecuta el borrado en cascada."""

    def __init__(self, repositorio_perfiles: RepositorioPerfilesAlumno):
        self._repositorio_perfiles = repositorio_perfiles

    def ejecutar(self, perfil_alumno_id: int) -> None:
        self._repositorio_perfiles.eliminar_en_cascada(perfil_alumno_id)
