"""Agregado IntentoEvaluacion — protege sus propios invariantes (no responder tras
entregar, entrega idempotente) en vez de dejarlos dispersos en routers/casos de uso."""

from dataclasses import dataclass, field
from datetime import datetime

from app.domain.evaluaciones.exceptions import IntentoYaEntregado
from app.domain.evaluaciones.value_objects import TIPOS_AUTOCORREGIBLES, Nota, PreguntaParaCorreccion
from app.domain.shared.reloj import Reloj


@dataclass
class IntentoEvaluacion:
    id: int | None
    perfil_alumno_id: int
    conjunto_evaluacion_id: int
    fecha_inicio: datetime
    fecha_termino: datetime | None = None
    respuestas: dict[str, str] = field(default_factory=dict)
    puntaje: float | None = None
    nota: float | None = None
    tiempo_usado_seg: int | None = None

    @classmethod
    def iniciar(cls, perfil_alumno_id: int, conjunto_evaluacion_id: int, reloj: Reloj) -> "IntentoEvaluacion":
        return cls(
            id=None,
            perfil_alumno_id=perfil_alumno_id,
            conjunto_evaluacion_id=conjunto_evaluacion_id,
            fecha_inicio=reloj.ahora(),
            respuestas={},
        )

    @property
    def esta_entregado(self) -> bool:
        return self.fecha_termino is not None

    def responder(self, pregunta_id: int, respuesta: str) -> None:
        if self.esta_entregado:
            raise IntentoYaEntregado()
        self.respuestas = {**self.respuestas, str(pregunta_id): respuesta}

    def entregar(self, preguntas: list[PreguntaParaCorreccion], reloj: Reloj) -> None:
        """Idempotente: un intento ya entregado es inmutable — no recalcula ni
        sobreescribe. La invariante vive acá para proteger a cualquier caller, no solo
        al caso de uso EntregarIntento."""
        if self.esta_entregado:
            return

        autocorregibles = [p for p in preguntas if p.tipo in TIPOS_AUTOCORREGIBLES]
        correctas = 0
        for p in autocorregibles:
            respuesta_alumno = self.respuestas.get(str(p.id), "").strip().lower()
            respuesta_correcta = p.respuesta_correcta.strip().lower()
            if respuesta_alumno and respuesta_alumno == respuesta_correcta:
                correctas += 1

        puntaje_total = len(autocorregibles)
        self.puntaje = float(correctas)
        self.nota = Nota.desde_puntaje(correctas, puntaje_total).valor if puntaje_total > 0 else None
        self.fecha_termino = reloj.ahora()
        # Resta aware-aware pura. El workaround de timezone de Postgres (columna
        # TIMESTAMP sin zona que devuelve datetimes naive al leer) vive únicamente en
        # el mapper de infraestructura (RepositorioIntentosSQLModel), no acá.
        self.tiempo_usado_seg = int((self.fecha_termino - self.fecha_inicio).total_seconds())
