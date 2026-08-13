"""Value Objects del contexto Evaluaciones."""

from dataclasses import dataclass


def calcular_nota(puntaje_obtenido: float, puntaje_total: float, exigencia: float = 0.6) -> float:
    """Fórmula chilena estándar, exigencia 60% — ver planificacion/12-motor-de-evaluacion.md.

    - 0% de logro → nota 1.0
    - `exigencia` de logro (60% por defecto) → nota 4.0 (aprobación)
    - 100% de logro → nota 7.0
    """
    if puntaje_total <= 0:
        raise ValueError("puntaje_total debe ser mayor que 0")
    if not (0 < exigencia < 1):
        raise ValueError("exigencia debe estar entre 0 y 1 (excluyentes)")

    puntaje_aprobacion = puntaje_total * exigencia

    if puntaje_obtenido <= puntaje_aprobacion:
        nota = 1.0 + 3.0 * (puntaje_obtenido / puntaje_aprobacion)
    else:
        nota = 4.0 + 3.0 * (
            (puntaje_obtenido - puntaje_aprobacion) / (puntaje_total - puntaje_aprobacion)
        )

    nota = max(1.0, min(7.0, nota))
    return round(nota, 1)


@dataclass(frozen=True)
class Nota:
    """Envuelve una nota ya calculada — se valida a sí misma en el rango chileno 1.0-7.0,
    así ningún caller puede construir/propagar una nota fuera de escala por error."""

    valor: float

    def __post_init__(self) -> None:
        if not (1.0 <= self.valor <= 7.0):
            raise ValueError("La nota debe estar entre 1.0 y 7.0")

    @classmethod
    def desde_puntaje(cls, puntaje_obtenido: float, puntaje_total: float, exigencia: float = 0.6) -> "Nota":
        return cls(calcular_nota(puntaje_obtenido, puntaje_total, exigencia))

    def __float__(self) -> float:
        return self.valor


@dataclass(frozen=True)
class PreguntaParaCorreccion:
    """VO de lectura angosto — solo lo que el motor de autocorrección necesita de una
    pregunta, desacoplado de la fila ORM y de la vista completa de lectura (enunciado,
    opciones, etc. viven en el read-model de `RepositorioPreguntas`)."""

    id: int
    tipo: str
    respuesta_correcta: str


TIPOS_AUTOCORREGIBLES = {"alternativas", "verdadero_falso"}

# Simulacro parcial (Fase 1.3) — se habilita al cubrir la mitad del temario de la
# asignatura, con hasta 20 preguntas autocorregibles de las OA ya cubiertas.
UMBRAL_SIMULACRO_PARCIAL = 0.5
MAX_PREGUNTAS_SIMULACRO_PARCIAL = 20
