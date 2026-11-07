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


@dataclass(frozen=True)
class SuscripcionLectura:
    """Fase 1, ítem 2.8 del plan de incorporación de hallazgos de Brincus — historial de
    pagos para el Apoderado con los datos que YA existen hoy. `Suscripcion` hoy es una
    única fila vigente por alumno (se reemplaza en cada `asignar_*`, no se acumula
    historial de transacciones) — por eso esto expone la suscripción actual, no una
    lista de pagos pasados; el comprobante con monto real queda pendiente de la pasarela
    de pago (ver planificacion/22-analisis-de-brechas.md)."""

    plan_id: int
    plan_nombre: str
    fecha_inicio: datetime
    fecha_termino: datetime | None
    estado: str
    origen: str


class RepositorioSuscripciones(Protocol):
    def asignar_cortesia(self, perfil_alumno_id: int, plan_id: int, ahora: datetime) -> None: ...
    def asignar_prueba_gratis(
        self, perfil_alumno_id: int, plan_id: int, ahora: datetime, fecha_termino: datetime
    ) -> None: ...
    def contar_activas_por_plan(self) -> list[ActivasPorPlan]: ...
    def sumar_ingresos_mes_pago(self, anio: int, mes: int) -> int: ...
    def buscar_por_perfil(self, perfil_alumno_id: int) -> SuscripcionLectura | None: ...


@dataclass(frozen=True)
class AlumnoEncontrado:
    perfil_alumno_id: int
    nombre: str
    apellidos: str
    rut: str
    cuenta_apoderado_id: int
    email_apoderado: str
