"""Check-in emocional diario (Fase 1, ítem 2.4 del plan de incorporación de hallazgos de
Brincus — ver planificacion/27-plan-incorporacion-hallazgos-brincus.md). Dato simple, un
registro por alumno por día; sin visibilidad para el Apoderado todavía (pregunta abierta
#2 del plan, se dejó para más adelante — hoy es solo para acompañar al alumno)."""

from dataclasses import dataclass
from datetime import date

from app.domain.bienestar.exceptions import EstadoAnimoInvalido

ESTADOS_ANIMO = [
    "feliz",
    "tranquilo",
    "normal",
    "cansado",
    "preocupado",
    "triste",
    "frustrado",
]


@dataclass
class RegistroAnimo:
    id: int | None
    perfil_alumno_id: int
    estado: str
    fecha: date

    @classmethod
    def crear(cls, perfil_alumno_id: int, estado: str, fecha: date) -> "RegistroAnimo":
        if estado not in ESTADOS_ANIMO:
            raise EstadoAnimoInvalido()
        return cls(id=None, perfil_alumno_id=perfil_alumno_id, estado=estado, fecha=fecha)
