"""Puerto de solo lectura/escritura de hechos — sin agregado ni invariantes que proteger
(igual que `contenido`): marcar una guía como revisada es un registro de hecho, no una
operación de negocio que pueda fallar por una regla."""

from dataclasses import dataclass
from datetime import datetime
from typing import Protocol


@dataclass(frozen=True)
class GuiaRevisada:
    oa_id: int
    fecha: datetime


class RepositorioProgreso(Protocol):
    def marcar_guia_revisada(self, perfil_alumno_id: int, oa_id: int, fecha: datetime) -> None: ...
    def listar_guias_revisadas(self, perfil_alumno_id: int) -> list[GuiaRevisada]: ...


@dataclass(frozen=True)
class ItemHistorial:
    intento_id: int
    conjunto_id: int
    tipo: str  # "prueba_unidad" | "examen_simulacro"
    asignatura_id: int | None
    asignatura_nombre: str | None
    nombre: str
    nota: float | None
    fecha: datetime


@dataclass(frozen=True)
class NotaPorAsignatura:
    asignatura_id: int
    asignatura_nombre: str
    nota_practica: float | None
    nota_simulacro: float | None


@dataclass(frozen=True)
class ItemFaltante:
    conjunto_id: int
    tipo: str
    nombre: str
    asignatura_id: int | None
    habilitado: bool


@dataclass(frozen=True)
class CoberturaAsignatura:
    asignatura_id: int
    asignatura_nombre: str
    cobertura_pct: float
    simulacro_parcial_disponible: bool
