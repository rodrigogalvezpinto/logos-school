from datetime import date
from typing import Protocol

from app.domain.bienestar.entities import RegistroAnimo


class RepositorioBienestar(Protocol):
    def buscar_de_fecha(self, perfil_alumno_id: int, fecha: date) -> RegistroAnimo | None: ...
    def guardar(self, registro: RegistroAnimo) -> RegistroAnimo: ...
