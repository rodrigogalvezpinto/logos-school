"""Caso de uso de escritura para la agenda familiar del domingo (idea 7 del boceto de
innovación, 2026-08-17) — separado de `consultas.py` (solo lectura), mismo criterio que el
resto del proyecto."""

from datetime import date

from app.application.apoderado.consultas import _inicio_de_semana
from app.domain.agenda_familiar.ports import RepositorioAgendaFamiliar


class MarcarAgendaFamiliarConversada:
    def __init__(self, repositorio_agenda: RepositorioAgendaFamiliar):
        self._repositorio_agenda = repositorio_agenda

    def ejecutar(self, perfil_alumno_id: int, hoy: date) -> None:
        self._repositorio_agenda.marcar_conversada(perfil_alumno_id, _inicio_de_semana(hoy))
