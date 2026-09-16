"""Puertos del contexto Evaluaciones. Los read-models (ConjuntoLectura, PreguntaLectura)
son DTOs de lectura simples, no agregados — no protegen invariantes, solo desacoplan a
los routers de la fila SQLModel para las consultas de solo lectura (ver plan: `contenido`
y los endpoints de solo lectura de este contexto no necesitan ceremonia de caso de uso)."""

from dataclasses import dataclass
from datetime import datetime
from typing import Protocol

from app.domain.evaluaciones.entities import IntentoEvaluacion
from app.domain.evaluaciones.value_objects import PreguntaParaCorreccion


class RepositorioIntentos(Protocol):
    def buscar_por_id(self, intento_id: int) -> IntentoEvaluacion | None: ...
    def buscar_activo(self, perfil_alumno_id: int, conjunto_evaluacion_id: int) -> IntentoEvaluacion | None: ...
    def guardar(self, intento: IntentoEvaluacion) -> IntentoEvaluacion: ...
    def listar_entregados_por_perfil(self, perfil_alumno_id: int) -> list[IntentoEvaluacion]: ...


@dataclass(frozen=True)
class ConjuntoLectura:
    id: int
    tipo: str
    nombre: str
    forma: str | None
    tiempo_sugerido_min: int | None
    pregunta_ids: list[int]
    asignatura_id: int | None = None
    nivel_id: int | None = None
    fecha_programada: datetime | None = None
    """Simulacro con fecha programada por el Admin (Fase 1, ítem 2.1 del plan de
    incorporación de hallazgos de Brincus) — `None` = disponibilidad normal por cobertura,
    igual que siempre. Con valor, queda "próximamente" hasta esa fecha/hora."""


class RepositorioConjuntos(Protocol):
    def buscar_por_id(self, conjunto_id: int) -> ConjuntoLectura | None: ...
    def listar_por_asignatura(self, asignatura_id: int) -> list[ConjuntoLectura]: ...
    def listar_por_nivel(self, nivel_id: int) -> list[ConjuntoLectura]: ...
    def listar_por_ids(self, ids: list[int]) -> list[ConjuntoLectura]: ...

    def crear(
        self,
        tipo: str,
        nombre: str,
        forma: str | None,
        asignatura_id: int | None,
        nivel_id: int | None,
        pregunta_ids: list[int],
        tiempo_sugerido_min: int | None,
    ) -> ConjuntoLectura:
        """Único método de escritura del puerto — hoy `ConjuntoEvaluacion` es 100%
        estático (importado desde contenido), salvo el simulacro parcial generado on
        demand por `GenerarSimulacroParcial`."""
        ...

    def programar_fecha(self, conjunto_id: int, fecha_programada: datetime | None) -> ConjuntoLectura:
        """`None` quita la fecha programada (vuelve a disponibilidad normal por cobertura)."""
        ...


@dataclass(frozen=True)
class PreguntaLectura:
    id: int
    tipo: str
    enunciado: str
    opciones: list[str] | None
    respuesta_correcta: str
    retroalimentacion: str
    oa_id: int | None = None


class RepositorioPreguntas(Protocol):
    def existe_objetivo(self, oa_id: int) -> bool: ...
    def buscar_por_oa(self, oa_id: int) -> list[PreguntaLectura]: ...
    def listar_por_ids(self, ids: list[int]) -> list[PreguntaLectura]: ...
    def listar_para_correccion(self, ids: list[int]) -> list[PreguntaParaCorreccion]: ...


@dataclass(frozen=True)
class DetallePregunta:
    """Read-model de una pregunta ya corregida dentro de un intento entregado — solo se
    arma después de la entrega (`IntentoNoEntregado` antes de eso), para no filtrar la
    respuesta correcta de un intento todavía en curso."""

    pregunta_id: int
    enunciado: str
    tipo: str
    opciones: list[str] | None
    respuesta_alumno: str | None
    respuesta_correcta: str | None
    es_correcta: bool | None
    """`None` en los tres campos de corrección cuando la pregunta no es autocorregible
    (ej. desarrollo_breve) — no hay una "respuesta correcta" única que mostrar."""
