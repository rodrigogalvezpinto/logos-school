from google.auth.transport import requests as google_requests
from google.oauth2 import id_token as google_id_token

from app.core.config import settings
from app.domain.auth.exceptions import GoogleLoginNoConfigurado, TokenGoogleInvalido
from app.domain.auth.ports import InfoGoogle


class VerificadorTokenGoogleAdapter:
    """Adaptador del puerto VerificadorTokenGoogle — traduce los errores específicos de
    la librería google-auth y la configuración faltante a excepciones de dominio."""

    def verificar(self, id_token: str) -> InfoGoogle:
        if not settings.google_client_id:
            raise GoogleLoginNoConfigurado()
        try:
            info = google_id_token.verify_oauth2_token(
                id_token, google_requests.Request(), settings.google_client_id
            )
        except ValueError:
            raise TokenGoogleInvalido()
        return InfoGoogle(
            google_id=info["sub"],
            email=info["email"],
            nombre=info.get("name", info["email"]),
        )
