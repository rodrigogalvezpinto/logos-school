"""Consultas de aplicación del panel comercial — mismo criterio que
`application/progreso/consultas.py`: combinan datos de más de un repositorio con lógica de
agregación real, así que ameritan una clase en vez de un pass-through router→repositorio."""

from dataclasses import dataclass
from datetime import datetime

from app.domain.auth.ports import RepositorioCuentas, RepositorioPerfilesAlumno
from app.domain.comercial.ports import AlumnoEncontrado, RepositorioPlanes, RepositorioSuscripciones


class BuscarAlumnos:
    def __init__(self, repositorio_perfiles: RepositorioPerfilesAlumno, repositorio_cuentas: RepositorioCuentas):
        self._repositorio_perfiles = repositorio_perfiles
        self._repositorio_cuentas = repositorio_cuentas

    def ejecutar(self, consulta: str) -> list[AlumnoEncontrado]:
        perfiles = self._repositorio_perfiles.buscar_por_texto(consulta)
        resultado = []
        for perfil in perfiles:
            cuenta = self._repositorio_cuentas.buscar_por_id(perfil.cuenta_apoderado_id)
            resultado.append(
                AlumnoEncontrado(
                    perfil_alumno_id=perfil.id,
                    nombre=perfil.nombre,
                    apellidos=perfil.apellidos,
                    rut=perfil.rut,
                    cuenta_apoderado_id=perfil.cuenta_apoderado_id,
                    email_apoderado=cuenta.email if cuenta else "—",
                )
            )
        return resultado


@dataclass(frozen=True)
class SuscripcionesPorPlan:
    plan_id: int
    plan_nombre: str
    activas: int


@dataclass(frozen=True)
class Metricas:
    apoderados_registrados: int
    alumnos_registrados: int
    suscripciones_por_plan: list[SuscripcionesPorPlan]
    ingresos_mes_aprox_clp: int


class ObtenerMetricas:
    def __init__(
        self,
        repositorio_cuentas: RepositorioCuentas,
        repositorio_perfiles: RepositorioPerfilesAlumno,
        repositorio_planes: RepositorioPlanes,
        repositorio_suscripciones: RepositorioSuscripciones,
    ):
        self._repositorio_cuentas = repositorio_cuentas
        self._repositorio_perfiles = repositorio_perfiles
        self._repositorio_planes = repositorio_planes
        self._repositorio_suscripciones = repositorio_suscripciones

    def ejecutar(self, ahora: datetime) -> Metricas:
        planes = {p.id: p.nombre for p in self._repositorio_planes.listar()}
        activas_por_plan = self._repositorio_suscripciones.contar_activas_por_plan()

        # "Aprox": suma el precio_clp vigente del plan al momento de la consulta, no el
        # monto realmente cobrado en el momento del pago (no existe ese campo todavía —
        # llega con la pasarela de pago real, ver planificacion/22-analisis-de-brechas.md).
        ingresos_mes_aprox = self._repositorio_suscripciones.sumar_ingresos_mes_pago(ahora.year, ahora.month)

        return Metricas(
            apoderados_registrados=self._repositorio_cuentas.contar(),
            alumnos_registrados=self._repositorio_perfiles.contar(),
            suscripciones_por_plan=[
                SuscripcionesPorPlan(
                    plan_id=a.plan_id, plan_nombre=planes.get(a.plan_id, "—"), activas=a.cantidad
                )
                for a in activas_por_plan
            ],
            ingresos_mes_aprox_clp=ingresos_mes_aprox,
        )
