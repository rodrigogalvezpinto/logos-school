"""Puerto liviano de solo lectura — sin entidades ni casos de uso: el contenido
(niveles/asignaturas/objetivos) no tiene invariantes que proteger, solo consultas."""

from dataclasses import dataclass
from typing import Protocol


@dataclass(frozen=True)
class NivelLectura:
    id: int
    nombre: str
    regimen: str
    num_preguntas_examen: int
    duracion_examen_min: int


@dataclass(frozen=True)
class AsignaturaLectura:
    id: int
    nombre: str


@dataclass(frozen=True)
class ObjetivoLectura:
    id: int
    codigo_oficial: str
    descripcion: str
    eje_tematico: str | None
    contenido_guia: str


class RepositorioContenido(Protocol):
    def listar_niveles(self) -> list[NivelLectura]: ...
    def listar_asignaturas(self, nivel_id: int) -> list[AsignaturaLectura]: ...
    def listar_objetivos(self, asignatura_id: int) -> list[ObjetivoLectura]: ...
    def obtener_objetivo(self, oa_id: int) -> ObjetivoLectura | None: ...
