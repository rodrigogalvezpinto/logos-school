"""Servicio de envío de correo — usa Resend (ver planificacion/17-infraestructura-y-entornos.md).

Requiere la variable de entorno RESEND_API_KEY, que debe generarse en una cuenta de
Resend NUEVA y propia de este proyecto (no reutilizar la de otros proyectos, tal como
pidió el usuario). Mientras no esté configurada, las funciones no fallan: registran el
correo que habrían enviado en la consola, para no bloquear el resto del desarrollo.
"""

import logging
from html import escape

import resend

from app.core.config import settings

logger = logging.getLogger("logos.correo")


def _enviar(destinatario: str, asunto: str, html: str) -> None:
    if not settings.resend_api_key:
        logger.warning(
            "RESEND_API_KEY no configurada — correo NO enviado (solo registrado). "
            "Para: %s | Asunto: %s",
            destinatario,
            asunto,
        )
        return

    resend.api_key = settings.resend_api_key
    try:
        resend.Emails.send(
            {
                "from": settings.resend_remitente,
                "to": [destinatario],
                "subject": asunto,
                "html": html,
            }
        )
    except Exception:
        # Nunca debe romper el flujo real (registro, activar plan) por un problema de
        # correo (dominio sin verificar en Resend, corte de red, etc.) — el correo es una
        # notificación secundaria, no una condición para que la acción principal funcione.
        logger.exception("Falló el envío de correo — no se interrumpe el flujo. Para: %s | Asunto: %s", destinatario, asunto)


def enviar_bienvenida(destinatario: str, nombre_apoderado: str) -> None:
    html = f"""
    <h2>¡Bienvenido/a a Logos School, {escape(nombre_apoderado)}!</h2>
    <p>Tu cuenta ya está lista. Puedes agregar a tus alumnos y elegir un plan para
    empezar a estudiar el temario oficial del Examen Libre.</p>
    """
    _enviar(destinatario, "Bienvenido/a a Logos School", html)


def enviar_confirmacion_plan(destinatario: str, nombre_alumno: str, nombre_plan: str) -> None:
    html = f"""
    <h2>Plan activado</h2>
    <p>El plan <strong>{escape(nombre_plan)}</strong> ya está activo para {escape(nombre_alumno)}.
    ¡A estudiar!</p>
    """
    _enviar(destinatario, f"Plan activado para {nombre_alumno}", html)


def enviar_recuperacion_password(destinatario: str, nombre: str, enlace: str) -> None:
    html = f"""
    <h2>Crear una contraseña nueva</h2>
    <p>Hola {escape(nombre)}: recibimos una solicitud para cambiar la contraseña de tu cuenta de Logos School.</p>
    <p><a href="{escape(enlace)}">Crear mi contraseña nueva</a></p>
    <p>El enlace vence en 1 hora y sirve una sola vez. Si no lo pediste, ignora este correo: tu contraseña
    sigue igual.</p>
    """
    _enviar(destinatario, "Logos School: crear una contraseña nueva", html)
