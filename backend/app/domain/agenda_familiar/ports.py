"""Puerto para la agenda familiar del domingo (idea 7 del boceto de innovación,
2026-08-17) — "ya conversamos" por (alumno, semana), sin más invariante que esa."""

from datetime import date
from typing import Protocol


class RepositorioAgendaFamiliar(Protocol):
    def ya_conversada(self, perfil_alumno_id: int, semana_inicio: date) -> bool: ...
    def marcar_conversada(self, perfil_alumno_id: int, semana_inicio: date) -> None: ...
