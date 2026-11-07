from dataclasses import dataclass


@dataclass
class CuentaProfesor:
    id: int | None
    email: str
    nombre: str
    password_hash: str
    estado: str = "pendiente"  # "pendiente" | "aprobado" | "rechazado"

    @classmethod
    def crear(cls, email: str, nombre: str, password_hash: str) -> "CuentaProfesor":
        return cls(id=None, email=email, nombre=nombre, password_hash=password_hash, estado="pendiente")

    @property
    def esta_aprobado(self) -> bool:
        return self.estado == "aprobado"

    def aprobar(self) -> None:
        self.estado = "aprobado"

    def rechazar(self) -> None:
        self.estado = "rechazado"
