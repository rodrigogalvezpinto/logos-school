from typing import Protocol

from app.domain.gamificacion.entities import PerfilGamificacion


class RepositorioGamificacion(Protocol):
    def obtener_o_crear(self, perfil_alumno_id: int) -> PerfilGamificacion: ...
    def guardar(self, perfil: PerfilGamificacion) -> PerfilGamificacion: ...
