from typing import Protocol

from app.domain.sugerencias.entities import Sugerencia


class RepositorioSugerencias(Protocol):
    def guardar(self, sugerencia: Sugerencia) -> Sugerencia: ...
    def listar_por_perfil(self, perfil_alumno_id: int) -> list[Sugerencia]: ...
