"""Centro de notificaciones (Fase 1 del plan de incorporación de hallazgos de Brincus —
ver planificacion/27-plan-incorporacion-hallazgos-brincus.md, Paso 12: campana con
Notificaciones / Preguntas y Respuestas / Errores reportados). "Preguntas y Respuestas" no
aplica (Logos no tiene chat/profesor IA todavía — Fase 2).

Deliberadamente NO es un agregado nuevo con estado leído/no-leído persistido: eso sería
infraestructura de notificaciones (con sus propias reglas de expiración, marcado masivo,
etc.) sin un caso de uso real que la justifique todavía. En cambio, esto es una vista
compuesta calculada al vuelo sobre datos que ya existen — comunicados del curso, sesiones de
Plan de Estudio atrasadas, reportes de error propios ya resueltos — mismo criterio de "cruce
legítimo entre contextos" que ya usa `AgregarSesionDeRepaso` o `ObtenerProgresoDeCurso`."""

from dataclasses import dataclass
from datetime import date, datetime, timezone

from app.application.curso_seccion.consultas import ObtenerMiCurso
from app.application.plan_estudio.casos_de_uso import ObtenerPlanActivo
from app.domain.plan_estudio.exceptions import PlanDeEstudioNoEncontrado
from app.domain.reportes.ports import RepositorioReportesError


@dataclass(frozen=True)
class Notificacion:
    tipo: str  # "comunicado" | "sesion_atrasada" | "reporte_resuelto"
    titulo: str
    detalle: str
    fecha: datetime


class ObtenerNotificaciones:
    def __init__(
        self,
        obtener_mi_curso: ObtenerMiCurso,
        obtener_plan_activo: ObtenerPlanActivo,
        repositorio_reportes: RepositorioReportesError,
    ):
        self._obtener_mi_curso = obtener_mi_curso
        self._obtener_plan_activo = obtener_plan_activo
        self._repositorio_reportes = repositorio_reportes

    def ejecutar(self, perfil_alumno_id: int, hoy: date) -> list[Notificacion]:
        notificaciones: list[Notificacion] = []

        mi_curso = self._obtener_mi_curso.ejecutar(perfil_alumno_id)
        if mi_curso:
            for c in mi_curso.comunicados:
                notificaciones.append(
                    Notificacion(tipo="comunicado", titulo=c.titulo, detalle=c.cuerpo, fecha=c.fecha)
                )

        try:
            plan, cumplidas = self._obtener_plan_activo.ejecutar(perfil_alumno_id)
            for sesion in plan.sesiones:
                if not cumplidas.get(sesion.id, False) and sesion.fecha_programada < hoy:
                    notificaciones.append(
                        Notificacion(
                            tipo="sesion_atrasada",
                            titulo="Sesión de estudio atrasada",
                            detalle=f"Tenías una sesión programada el {sesion.fecha_programada.isoformat()} que todavía no cumples.",
                            fecha=datetime.combine(sesion.fecha_programada, datetime.min.time(), tzinfo=timezone.utc),
                        )
                    )
        except PlanDeEstudioNoEncontrado:
            pass

        for r in self._repositorio_reportes.listar_por_perfil(perfil_alumno_id):
            if r.resuelto:
                notificaciones.append(
                    Notificacion(
                        tipo="reporte_resuelto",
                        titulo="Tu reporte de error fue revisado",
                        detalle=r.comentario or "Gracias por avisarnos — ya lo revisamos.",
                        fecha=r.fecha,
                    )
                )

        notificaciones.sort(key=lambda n: n.fecha, reverse=True)
        return notificaciones
