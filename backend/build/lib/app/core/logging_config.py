"""Logging estructurado — para monitoreo local (ver planificacion/17-infraestructura-
y-entornos.md, donde Sentry es el plan de monitoreo real de producción; esto cubre
mientras tanto el registro local de Desarrollo).

Todo request y toda excepción no controlada quedan en backend/logs/app.log, además de
la consola — así se puede hacer `tail -f logs/app.log` para ver errores en vivo.
"""

import logging
import time
from pathlib import Path

from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware

LOGS_DIR = Path(__file__).parent.parent.parent / "logs"
LOGS_DIR.mkdir(exist_ok=True)


def configurar_logging() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
        handlers=[
            logging.FileHandler(LOGS_DIR / "app.log", encoding="utf-8"),
            logging.StreamHandler(),
        ],
    )


logger_requests = logging.getLogger("logos.requests")


class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        inicio = time.monotonic()
        try:
            respuesta = await call_next(request)
        except Exception:
            logger_requests.exception(
                "Error no controlado en %s %s", request.method, request.url.path
            )
            raise
        duracion_ms = (time.monotonic() - inicio) * 1000
        nivel = logging.WARNING if respuesta.status_code >= 400 else logging.INFO
        logger_requests.log(
            nivel,
            "%s %s -> %d (%.1f ms)",
            request.method,
            request.url.path,
            respuesta.status_code,
            duracion_ms,
        )
        return respuesta
