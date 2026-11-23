"""Aviso de errores con Sentry (2026-11-22). Apagado mientras SENTRY_DSN esté vacío.

La app maneja datos de menores, así que a Sentry solo viaja el error técnico (tipo, mensaje, traza y la ruta),
nunca datos personales: sin cuerpos de petición, sin variables locales (pueden tener nombres o RUT), sin
encabezados de sesión, sin parámetros de la URL (el enlace de recuperación lleva un token) y sin usuario.
"""

import sentry_sdk

from app.core.config import settings

_ENCABEZADOS_PERMITIDOS = {"user-agent", "content-type", "accept"}


def limpiar_evento(evento: dict, _hint: dict | None = None) -> dict:
    peticion = evento.get("request")
    if isinstance(peticion, dict):
        peticion.pop("data", None)
        peticion.pop("cookies", None)
        peticion["query_string"] = ""
        encabezados = peticion.get("headers")
        if isinstance(encabezados, dict):
            peticion["headers"] = {k: v for k, v in encabezados.items() if k.lower() in _ENCABEZADOS_PERMITIDOS}
    evento.pop("user", None)
    return evento


def iniciar_monitoreo() -> bool:
    if not settings.sentry_dsn.strip():
        return False
    sentry_sdk.init(
        dsn=settings.sentry_dsn.strip(),
        environment=settings.entorno,
        send_default_pii=False,
        include_local_variables=False,
        max_request_body_size="never",
        traces_sample_rate=0.0,
        before_send=limpiar_evento,
    )
    return True
