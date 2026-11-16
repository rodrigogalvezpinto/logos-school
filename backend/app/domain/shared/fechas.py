"""Fechas de calendario en la hora de Chile (defecto corregido el 2026-11-15).

Las marcas de tiempo se guardan en UTC, pero «hoy», «esta semana» o «sesión atrasada» son conceptos del
calendario del alumno. Antes se calculaban en UTC: entre las 21:00 y las 24:00 de Chile ya era el día
siguiente, y la actividad del domingo en la noche contaba en la semana siguiente.
"""
from datetime import date, datetime, timezone
from zoneinfo import ZoneInfo

ZONA_CHILE = ZoneInfo("America/Santiago")


def fecha_local(momento: datetime) -> date:
    """Fecha de calendario en Chile de un instante. Un datetime sin zona se interpreta como UTC (así se guardan)."""
    if momento.tzinfo is None:
        momento = momento.replace(tzinfo=timezone.utc)
    return momento.astimezone(ZONA_CHILE).date()
