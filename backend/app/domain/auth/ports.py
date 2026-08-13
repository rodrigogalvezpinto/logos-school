"""Puertos del contexto Auth — Protocols que la capa de aplicación consume y que
`infrastructure/` implementa. Ningún import de sqlmodel/bcrypt/jose/google acá: eso
es justamente lo que DIP prohíbe en esta capa."""

from dataclasses import dataclass
from typing import Protocol

from app.domain.auth.entities import Cuenta, PerfilAlumno


class RepositorioCuentas(Protocol):
    def buscar_por_email(self, email: str) -> Cuenta | None: ...
    def buscar_por_google_id(self, google_id: str) -> Cuenta | None: ...
    def buscar_por_id(self, cuenta_id: int) -> Cuenta | None: ...
    def guardar(self, cuenta: Cuenta) -> Cuenta: ...


class RepositorioPerfilesAlumno(Protocol):
    def guardar(self, perfil: PerfilAlumno) -> PerfilAlumno: ...
    def listar_por_cuenta(self, cuenta_apoderado_id: int) -> list[PerfilAlumno]: ...
    def buscar_por_id(self, perfil_id: int) -> PerfilAlumno | None: ...


class HasheadorPassword(Protocol):
    def hashear(self, password: str) -> str: ...
    def verificar(self, password: str, password_hash: str) -> bool: ...


class ServicioToken(Protocol):
    def generar(self, cuenta_id: int) -> str: ...
    def decodificar(self, token: str) -> int | None: ...


@dataclass(frozen=True)
class InfoGoogle:
    google_id: str
    email: str
    nombre: str


class VerificadorTokenGoogle(Protocol):
    def verificar(self, id_token: str) -> InfoGoogle: ...
