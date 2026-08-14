"""Entidades de dominio del contexto Auth — objetos Python planos, sin ningún import de
SQLModel/FastAPI. Los factory methods son el único punto de construcción "válida"."""

from dataclasses import dataclass
from datetime import date, datetime

from app.domain.auth.value_objects import Rut


@dataclass
class Cuenta:
    id: int | None
    email: str
    nombre: str
    password_hash: str | None = None
    google_id: str | None = None
    comuna_o_region: str | None = None
    pais: str | None = None
    fecha_creacion: datetime | None = None
    # Se incrementa al cerrar sesión — un JWT emitido antes queda inválido de inmediato
    # aunque no haya expirado (ver ServicioTokenJWT y get_cuenta_actual). Sin esto, "cerrar
    # sesión" solo borraba el token del navegador pero el token seguía siendo válido en el
    # servidor hasta su expiración natural (bug real encontrado en esta app, con menores de
    # edad de por medio).
    sesion_version: int = 0

    def cerrar_todas_las_sesiones(self) -> None:
        self.sesion_version += 1

    @classmethod
    def crear_con_password(
        cls,
        email: str,
        nombre: str,
        password_hash: str,
        comuna_o_region: str | None = None,
        pais: str | None = None,
    ) -> "Cuenta":
        return cls(
            id=None,
            email=email,
            nombre=nombre,
            password_hash=password_hash,
            comuna_o_region=comuna_o_region,
            pais=pais,
        )

    @classmethod
    def crear_con_google(cls, email: str, nombre: str, google_id: str) -> "Cuenta":
        return cls(id=None, email=email, nombre=nombre, google_id=google_id)

    def vincular_google(self, google_id: str) -> None:
        self.google_id = google_id


@dataclass
class PerfilAlumno:
    id: int | None
    cuenta_apoderado_id: int
    nombre: str
    apellidos: str
    fecha_nacimiento: date
    rut: str
    nivel_id: int
    fecha_creacion: datetime | None = None

    @classmethod
    def crear(
        cls,
        cuenta_apoderado_id: int,
        nombre: str,
        apellidos: str,
        fecha_nacimiento: date,
        rut: Rut,
        nivel_id: int,
        hoy: date,
    ) -> "PerfilAlumno":
        if fecha_nacimiento >= hoy:
            raise ValueError("La fecha de nacimiento no puede ser hoy ni una fecha futura")
        return cls(
            id=None,
            cuenta_apoderado_id=cuenta_apoderado_id,
            nombre=nombre,
            apellidos=apellidos,
            fecha_nacimiento=fecha_nacimiento,
            rut=str(rut),
            nivel_id=nivel_id,
        )
