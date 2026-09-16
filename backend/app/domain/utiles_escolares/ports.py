"""Puerto liviano de solo lectura — mismo criterio que app/domain/plan_lector/ports.py: la
lista de Útiles Escolares no tiene invariantes que proteger, solo una lista curada por nivel."""

from dataclasses import dataclass
from typing import Protocol


@dataclass(frozen=True)
class UtilEscolarLectura:
    id: int
    nombre: str
    cantidad: str | None
    asignatura: str | None


class RepositorioUtilesEscolares(Protocol):
    def listar_por_nivel(self, nivel_id: int) -> list[UtilEscolarLectura]: ...
