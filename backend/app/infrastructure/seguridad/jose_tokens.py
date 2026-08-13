from datetime import datetime, timedelta, timezone

from jose import JWTError, jwt

from app.core.config import settings


class ServicioTokenJWT:
    def generar(self, cuenta_id: int) -> str:
        expira = datetime.now(timezone.utc) + timedelta(minutes=settings.jwt_expiracion_minutos)
        payload = {"sub": str(cuenta_id), "exp": expira}
        return jwt.encode(payload, settings.jwt_secret, algorithm=settings.jwt_algoritmo)

    def decodificar(self, token: str) -> int | None:
        try:
            payload = jwt.decode(token, settings.jwt_secret, algorithms=[settings.jwt_algoritmo])
            return int(payload["sub"])
        except (JWTError, KeyError, ValueError):
            return None
