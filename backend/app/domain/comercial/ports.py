from dataclasses import dataclass
from datetime import datetime
from typing import Protocol

from app.domain.comercial.entities import CodigoDescuento, Plan


class RepositorioPlanes(Protocol):
    def buscar_por_id(self, plan_id: int) -> Plan | None: ...
    def listar(self) -> list[Plan]: ...
    def guardar(self, plan: Plan) -> Plan: ...


class RepositorioDescuentos(Protocol):
    def buscar_por_id(self, descuento_id: int) -> CodigoDescuento | None: ...
    def buscar_por_codigo(self, codigo: str) -> CodigoDescuento | None: ...
    def listar(self) -> list[CodigoDescuento]: ...
    def guardar(self, descuento: CodigoDescuento) -> CodigoDescuento: ...


@dataclass(frozen=True)
class ActivasPorPlan:
    plan_id: int
    cantidad: int


class RepositorioSuscripciones(Protocol):
    def asignar_cortesia(self, perfil_alumno_id: int, plan_id: int, ahora: datetime) -> None: ...
    def contar_activas_por_plan(self) -> list[ActivasPorPlan]: ...
    def sumar_ingresos_mes_pago(self, anio: int, mes: int) -> int: ...


@dataclass(frozen=True)
class AlumnoEncontrado:
    perfil_alumno_id: int
    nombre: str
    apellidos: str
    rut: str
    cuenta_apoderado_id: int
    email_apoderado: str
