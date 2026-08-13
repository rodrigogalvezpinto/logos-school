"""Entidades del contexto Comercial (Plan, Código de descuento) — ver
planificacion/18-panel-administrador.md."""

from dataclasses import dataclass
from datetime import date


@dataclass
class Plan:
    id: int | None
    nombre: str
    nivel_de_acceso: str
    precio_clp: int
    activo: bool = True

    @classmethod
    def crear(cls, nombre: str, nivel_de_acceso: str, precio_clp: int) -> "Plan":
        if precio_clp < 0:
            raise ValueError("precio_clp no puede ser negativo")
        return cls(id=None, nombre=nombre, nivel_de_acceso=nivel_de_acceso, precio_clp=precio_clp, activo=True)

    def editar(self, nombre: str, nivel_de_acceso: str, precio_clp: int) -> None:
        if precio_clp < 0:
            raise ValueError("precio_clp no puede ser negativo")
        self.nombre = nombre
        self.nivel_de_acceso = nivel_de_acceso
        self.precio_clp = precio_clp

    def activar(self) -> None:
        self.activo = True

    def desactivar(self) -> None:
        self.activo = False


@dataclass
class CodigoDescuento:
    id: int | None
    codigo: str
    tipo: str  # "porcentaje" | "monto_fijo"
    valor: int
    fecha_vencimiento: date | None  # primer día en que YA NO es válido (límite exclusivo)
    usos_maximos: int | None
    usos_actuales: int

    @classmethod
    def crear(
        cls, codigo: str, tipo: str, valor: int,
        fecha_vencimiento: date | None = None, usos_maximos: int | None = None,
    ) -> "CodigoDescuento":
        return cls(
            id=None, codigo=codigo, tipo=tipo, valor=valor,
            fecha_vencimiento=fecha_vencimiento, usos_maximos=usos_maximos, usos_actuales=0,
        )

    def vigente(self, hoy: date) -> bool:
        if self.fecha_vencimiento is not None and hoy >= self.fecha_vencimiento:
            return False
        if self.usos_maximos is not None and self.usos_actuales >= self.usos_maximos:
            return False
        return True

    def desactivar(self, hoy: date) -> None:
        """Fija `fecha_vencimiento` a hoy — el código deja de ser vigente de inmediato
        (ver `vigente()`), sin necesitar una columna `activo` separada."""
        self.fecha_vencimiento = hoy
