"""Límite de intentos para endpoints sensibles (fuerza bruta) — ver
planificacion/20-seguridad-y-casos-borde.md.
"""

from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)
