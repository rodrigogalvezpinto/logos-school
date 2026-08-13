from datetime import datetime, timedelta, timezone

from jose import JWTError, jwt

from app.core.config import settings


class ServicioTokenJWT:
    """Implementa a la vez el puerto `ServicioToken` (Apoderado) y `ServicioTokenAdmin`
    (panel de administración) — son tipos de token distintos por el claim `tipo`, para que
    un token de uno nunca sirva de credencial del otro aunque compartan secreto/algoritmo."""

    def generar(self, cuenta_id: int) -> str:
        return self._generar(cuenta_id)

    def decodificar(self, token: str) -> int | None:
        return self._decodificar(token, tipo_esperado=None)

    def generar_admin(self, cuenta_admin_id: int) -> str:
        return self._generar(cuenta_admin_id, tipo="admin")

    def decodificar_admin(self, token: str) -> int | None:
        return self._decodificar(token, tipo_esperado="admin")

    def _generar(self, cuenta_id: int, tipo: str | None = None) -> str:
        expira = datetime.now(timezone.utc) + timedelta(minutes=settings.jwt_expiracion_minutos)
        payload = {"sub": str(cuenta_id), "exp": expira}
        if tipo is not None:
            payload["tipo"] = tipo
        return jwt.encode(payload, settings.jwt_secret, algorithm=settings.jwt_algoritmo)

    def _decodificar(self, token: str, tipo_esperado: str | None) -> int | None:
        try:
            payload = jwt.decode(token, settings.jwt_secret, algorithms=[settings.jwt_algoritmo])
            if payload.get("tipo") != tipo_esperado:
                return None
            return int(payload["sub"])
        except (JWTError, KeyError, ValueError):
            return None
