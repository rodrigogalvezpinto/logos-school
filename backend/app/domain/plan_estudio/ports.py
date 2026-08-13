from typing import Protocol

from app.domain.plan_estudio.entities import PlanDeEstudio


class RepositorioPlanEstudio(Protocol):
    def buscar_activo_por_perfil(self, perfil_alumno_id: int) -> PlanDeEstudio | None: ...

    def reemplazar_plan(self, plan: PlanDeEstudio) -> PlanDeEstudio:
        """Borra el plan (y sus sesiones) previo del perfil si existe, y guarda el nuevo —
        atómico, siempre hay a lo más un plan activo por alumno."""
        ...
