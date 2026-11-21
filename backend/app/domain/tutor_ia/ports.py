"""Profesor IA (Fase 2, tarea 14, 2026-11-18): contrato del tutor. El dominio no sabe qué proveedor responde."""
from dataclasses import dataclass
from typing import Literal, Protocol


@dataclass(frozen=True)
class MensajeTutor:
    rol: Literal["alumno", "tutor"]
    texto: str


@dataclass(frozen=True)
class RespuestaTutor:
    texto: str
    # True cuando el proveedor declinó responder (p. ej. por seguridad): el alumno ve un mensaje neutro.
    declinada: bool = False


class TutorIA(Protocol):
    def responder(self, *, nivel: str, objetivo: str, guia: str, mensajes: list[MensajeTutor]) -> RespuestaTutor: ...


class TutorNoDisponible(Exception):
    """El proveedor no respondió (sin clave, límite de uso del proveedor, caída de red)."""
