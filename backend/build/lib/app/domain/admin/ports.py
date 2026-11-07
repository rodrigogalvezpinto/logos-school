from typing import Protocol

from app.domain.admin.entities import CuentaAdmin


class RepositorioCuentasAdmin(Protocol):
    def buscar_por_email(self, email: str) -> CuentaAdmin | None: ...
    def buscar_por_id(self, cuenta_admin_id: int) -> CuentaAdmin | None: ...


class ServicioTokenAdmin(Protocol):
    """Puerto angosto y deliberadamente distinto de `ServicioToken` (Apoderado, en
    domain/auth/ports.py) — mismos nombres de método no, para que quede explícito en la
    firma de cada caso de uso qué tipo de token está generando/leyendo."""

    def generar_admin(self, cuenta_admin_id: int) -> str: ...
    def decodificar_admin(self, token: str) -> int | None: ...
