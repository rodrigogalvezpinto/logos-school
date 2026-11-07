"""Calificación con estrellas por guía (Fase 1 del plan de incorporación de hallazgos de
Brincus — ver planificacion/27-plan-incorporacion-hallazgos-brincus.md, cuarta pasada:
Brincus tiene un tab "Evaluar Sección" con "¿Cuántas estrellas le darías a este video?",
separado de "Reportar error" — una señal de calidad de contenido más liviana y positiva,
no solo de bugs. Un alumno puede recalificar la misma guía (la última calificación reemplaza
a la anterior, no se acumulan filas por alumno+guía)."""

from dataclasses import dataclass
from datetime import datetime

from app.domain.calificaciones.exceptions import EstrellasInvalidas

ESTRELLAS_MIN = 1
ESTRELLAS_MAX = 5


@dataclass
class CalificacionGuia:
    id: int | None
    oa_id: int
    perfil_alumno_id: int
    estrellas: int
    fecha: datetime

    @classmethod
    def crear(cls, oa_id: int, perfil_alumno_id: int, estrellas: int, fecha: datetime) -> "CalificacionGuia":
        if not (ESTRELLAS_MIN <= estrellas <= ESTRELLAS_MAX):
            raise EstrellasInvalidas()
        return cls(id=None, oa_id=oa_id, perfil_alumno_id=perfil_alumno_id, estrellas=estrellas, fecha=fecha)
