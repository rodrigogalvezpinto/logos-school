"""Encabezados de seguridad del navegador — auditoría de seguridad (2026-08-17): la API no
enviaba ninguno. Sin `X-Frame-Options`, la app podía cargarse dentro de un `<iframe>` en un
sitio ajeno (clickjacking — el usuario cree que hace clic en la página real, pero hace clic
en algo invisible superpuesto). Sin `X-Content-Type-Options`, el navegador puede "adivinar"
el tipo de un archivo servido y ejecutarlo de forma distinta a la esperada (MIME-sniffing).
Esto es una API JSON pura (el frontend Angular es un proyecto aparte), así que el CSP
relevante para contenido/scripts vive en el `_headers` del frontend, no acá."""

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request


class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        respuesta = await call_next(request)
        respuesta.headers["X-Content-Type-Options"] = "nosniff"
        respuesta.headers["X-Frame-Options"] = "DENY"
        respuesta.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
        # Ninguna función de navegador que esta API necesite — se desactivan todas.
        respuesta.headers["Permissions-Policy"] = "geolocation=(), camera=(), microphone=()"
        return respuesta
