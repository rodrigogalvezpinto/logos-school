"""Límite de intentos para endpoints sensibles (fuerza bruta) — ver
planificacion/20-seguridad-y-casos-borde.md.

`default_limits` es una red de seguridad por defecto (auditoría de seguridad, 2026-08-17):
sin esto, un endpoint nuevo que alguien agregue mañana queda sin ninguna protección salvo
que alguien se acuerde de decorarlo a mano con `@limiter.limit(...)`. Con `default_limits` +
`SlowAPIMiddleware` (ver `main.py`), TODO endpoint tiene un límite base por IP aunque nadie
lo decore explícitamente — los endpoints decorados (login, registro, etc.) usan su propio
límite más estricto, que reemplaza al default solo en esa ruta."""

from slowapi import Limiter
from slowapi.util import get_remote_address

from app.core.config import settings

limiter = Limiter(key_func=get_remote_address, default_limits=[f"{settings.limite_global_por_minuto}/minute"])
