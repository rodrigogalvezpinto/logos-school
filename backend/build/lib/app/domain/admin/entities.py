from dataclasses import dataclass


@dataclass
class CuentaAdmin:
    id: int | None
    email: str
    nombre: str
    password_hash: str
