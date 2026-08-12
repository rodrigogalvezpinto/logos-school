from datetime import datetime, timedelta, timezone

import bcrypt
from jose import JWTError, jwt

from app.core.config import settings

# Se usa el paquete `bcrypt` directo (no passlib, que está sin mantenimiento y tiene
# problemas de compatibilidad con versiones recientes de bcrypt).


def hashear_password(password: str) -> str:
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")


def verificar_password(password: str, password_hash: str) -> bool:
    return bcrypt.checkpw(password.encode("utf-8"), password_hash.encode("utf-8"))


def crear_token(cuenta_id: int) -> str:
    expira = datetime.now(timezone.utc) + timedelta(minutes=settings.jwt_expiracion_minutos)
    payload = {"sub": str(cuenta_id), "exp": expira}
    return jwt.encode(payload, settings.jwt_secret, algorithm=settings.jwt_algoritmo)


def decodificar_token(token: str) -> int | None:
    try:
        payload = jwt.decode(token, settings.jwt_secret, algorithms=[settings.jwt_algoritmo])
        return int(payload["sub"])
    except (JWTError, KeyError, ValueError):
        return None
