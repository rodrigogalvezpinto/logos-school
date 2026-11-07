"""Reporte de error de contenido — Fase 1, ítems 2.1 y 2.6 del plan de incorporación de
hallazgos de Brincus (ver planificacion/27-plan-incorporacion-hallazgos-brincus.md).
Genérico por `tipo_contenido` para no atarlo solo a preguntas: hoy solo se expone el
endpoint de preguntas, pero el mismo mecanismo sirve para guía/video más adelante sin
cambiar el dominio."""

from dataclasses import dataclass
from datetime import datetime

TIPOS_CONTENIDO_REPORTABLE = {"pregunta", "guia", "video"}


@dataclass
class ReporteError:
    id: int | None
    tipo_contenido: str
    contenido_id: int
    perfil_alumno_id: int
    comentario: str
    fecha: datetime
    resuelto: bool = False

    @classmethod
    def crear(
        cls, tipo_contenido: str, contenido_id: int, perfil_alumno_id: int, comentario: str, fecha: datetime
    ) -> "ReporteError":
        return cls(
            id=None,
            tipo_contenido=tipo_contenido,
            contenido_id=contenido_id,
            perfil_alumno_id=perfil_alumno_id,
            comentario=comentario.strip(),
            fecha=fecha,
            resuelto=False,
        )
