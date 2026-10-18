"""Puerto liviano de solo lectura — igual criterio que app/domain/contenido/ports.py: el
Plan Lector no tiene invariantes que proteger, solo una lista curada por nivel."""

from dataclasses import dataclass
from typing import Protocol


@dataclass(frozen=True)
class LibroLectura:
    id: int
    titulo: str
    autor: str
    editorial: str


class RepositorioPlanLector(Protocol):
    def listar_por_nivel(self, nivel_id: int) -> list[LibroLectura]: ...
