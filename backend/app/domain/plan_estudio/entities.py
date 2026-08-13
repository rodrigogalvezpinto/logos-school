"""Contexto Plan de Estudio — ver planificacion/13-plan-de-estudio.md.

`generar_sesiones` es una función pura (sin I/O): reparte las OA pendientes por asignatura
en sesiones round-robin entre las fechas disponibles, alternando asignaturas para no
concentrar todo el estudio de una sola materia seguida. Testeable sin base de datos, mismo
criterio que `calcular_nota`/`IntentoEvaluacion.entregar`."""

import math
from dataclasses import dataclass, field
from datetime import date, timedelta

from app.domain.plan_estudio.exceptions import DiasInvalidos

MINUTOS_POR_OA = 25
SEMANAS_PLAZO_DEFECTO = 8
DIAS_VALIDOS = {"lunes", "martes", "miercoles", "jueves", "viernes", "sabado", "domingo"}
_NOMBRE_POR_INDICE = ["lunes", "martes", "miercoles", "jueves", "viernes", "sabado", "domingo"]


@dataclass
class SesionEstudio:
    id: int | None
    plan_estudio_id: int | None
    fecha_programada: date
    asignatura_id: int
    oa_ids: list[int]
    incluye_prueba_unidad: bool

    def esta_cumplida(self, oa_revisados: set[int]) -> bool:
        return bool(self.oa_ids) and set(self.oa_ids).issubset(oa_revisados)

    def minutos_estimados(self) -> int:
        return len(self.oa_ids) * MINUTOS_POR_OA


@dataclass
class PlanDeEstudio:
    id: int | None
    perfil_alumno_id: int
    dias_por_semana: int
    dias_elegidos: list[str]
    fecha_inicio: date
    fecha_objetivo: date | None
    sesiones: list[SesionEstudio] = field(default_factory=list)

    @classmethod
    def crear(
        cls,
        perfil_alumno_id: int,
        dias_por_semana: int,
        dias_elegidos: list[str],
        fecha_inicio: date,
        fecha_objetivo: date | None,
        pendientes_por_asignatura: dict[int, list[int]],
    ) -> "PlanDeEstudio":
        if dias_por_semana not in (3, 4, 5):
            raise DiasInvalidos("Los días de estudio deben ser 3, 4 o 5 por semana")
        if len(dias_elegidos) != dias_por_semana:
            raise DiasInvalidos("La cantidad de días elegidos debe calzar con dias_por_semana")
        if not set(dias_elegidos).issubset(DIAS_VALIDOS):
            raise DiasInvalidos(f"Día de la semana inválido — usa: {', '.join(sorted(DIAS_VALIDOS))}")

        sesiones = generar_sesiones(pendientes_por_asignatura, dias_elegidos, fecha_inicio, fecha_objetivo)
        return cls(
            id=None, perfil_alumno_id=perfil_alumno_id, dias_por_semana=dias_por_semana,
            dias_elegidos=dias_elegidos, fecha_inicio=fecha_inicio, fecha_objetivo=fecha_objetivo,
            sesiones=sesiones,
        )


def _fechas_disponibles(dias_elegidos: list[str], fecha_inicio: date, fecha_objetivo: date | None) -> list[date]:
    fecha_fin = fecha_objetivo or (fecha_inicio + timedelta(weeks=SEMANAS_PLAZO_DEFECTO))
    if fecha_fin <= fecha_inicio:
        return []
    fechas = []
    cursor = fecha_inicio
    while cursor < fecha_fin:
        if _NOMBRE_POR_INDICE[cursor.weekday()] in dias_elegidos:
            fechas.append(cursor)
        cursor += timedelta(days=1)
    return fechas


def generar_sesiones(
    pendientes_por_asignatura: dict[int, list[int]],
    dias_elegidos: list[str],
    fecha_inicio: date,
    fecha_objetivo: date | None,
) -> list[SesionEstudio]:
    fechas = _fechas_disponibles(dias_elegidos, fecha_inicio, fecha_objetivo)
    colas = {a: list(oas) for a, oas in pendientes_por_asignatura.items() if oas}
    asignaturas = list(colas.keys())
    if not fechas or not asignaturas:
        return []

    sesiones: list[SesionEstudio] = []
    i = 0
    idx_asignatura = 0
    # Cota de seguridad: nunca más vueltas que asignaturas * fechas restantes.
    intentos_maximos = len(asignaturas) * (len(fechas) + 1)
    intentos = 0

    while any(colas.values()) and i < len(fechas) and intentos < intentos_maximos:
        intentos += 1
        asignatura_id = asignaturas[idx_asignatura % len(asignaturas)]
        idx_asignatura += 1
        cola = colas[asignatura_id]
        if not cola:
            continue

        # Cupos de sesión que le quedan a esta asignatura entre las fechas restantes,
        # repartidos parejo con el resto de asignaturas (con ceil, no floor+1, para no
        # sobreestimar cuántas rondas más le tocan y dejar OA sin asignar al final).
        sesiones_restantes = max(1, math.ceil((len(fechas) - i) / len(asignaturas)))
        tomar = max(1, math.ceil(len(cola) / sesiones_restantes))
        oa_tomadas, colas[asignatura_id] = cola[:tomar], cola[tomar:]

        sesiones.append(
            SesionEstudio(
                id=None, plan_estudio_id=None, fecha_programada=fechas[i],
                asignatura_id=asignatura_id, oa_ids=oa_tomadas,
                incluye_prueba_unidad=(len(colas[asignatura_id]) == 0),
            )
        )
        i += 1

    return sesiones
