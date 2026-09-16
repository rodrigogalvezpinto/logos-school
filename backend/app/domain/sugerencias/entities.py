"""Buzón de sugerencias (Fase 1 del plan de incorporación de hallazgos de Brincus — ver
planificacion/27-plan-incorporacion-hallazgos-brincus.md, Paso 13: "¿Cómo doy ideas para
mejorar la plataforma?" es un tutorial propio en Brincus, canal explícito y visible, no
escondido en un correo de soporte). Mismo patrón que `ReporteError` — captura el dato, sin
panel de revisión de Admin todavía (ese mismo criterio ya se aplicó a los reportes de error:
existen y se guardan, sin bandeja de Admin construida)."""

from dataclasses import dataclass
from datetime import datetime


@dataclass
class Sugerencia:
    id: int | None
    perfil_alumno_id: int
    texto: str
    fecha: datetime

    @classmethod
    def crear(cls, perfil_alumno_id: int, texto: str, fecha: datetime) -> "Sugerencia":
        return cls(id=None, perfil_alumno_id=perfil_alumno_id, texto=texto.strip(), fecha=fecha)
