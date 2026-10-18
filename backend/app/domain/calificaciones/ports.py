from typing import Protocol

from app.domain.calificaciones.entities import CalificacionGuia


class RepositorioCalificaciones(Protocol):
    def guardar_o_actualizar(self, calificacion: CalificacionGuia) -> CalificacionGuia: ...
    def buscar_mia(self, oa_id: int, perfil_alumno_id: int) -> CalificacionGuia | None: ...
