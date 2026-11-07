from typing import Protocol

from app.domain.plan_estudio.entities import PlanDeEstudio, SesionEstudio


class RepositorioPlanEstudio(Protocol):
    def buscar_activo_por_perfil(self, perfil_alumno_id: int) -> PlanDeEstudio | None: ...

    def reemplazar_plan(self, plan: PlanDeEstudio) -> PlanDeEstudio:
        """Borra el plan (y sus sesiones) previo del perfil si existe, y guarda el nuevo —
        atómico, siempre hay a lo más un plan activo por alumno."""
        ...

    def agregar_sesion(self, plan_estudio_id: int, sesion: SesionEstudio) -> SesionEstudio:
        """Agrega una sesión suelta a un plan ya existente, sin tocar el resto — usada
        para "repasar contenido de un nivel anterior" (no reemplaza el plan completo)."""
        ...
