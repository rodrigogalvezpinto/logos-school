from datetime import datetime, timedelta, timezone

from jose import JWTError, jwt

from app.core.config import settings


class ServicioTokenJWT:
    """Implementa a la vez `ServicioToken` (Apoderado), `ServicioTokenAdmin` (panel de
    administración) y `ServicioTokenProfesor` — son tipos de token distintos por el claim
    `tipo`, para que un token de uno nunca sirva de credencial de otro aunque compartan
    secreto/algoritmo."""

    def generar(self, cuenta_id: int, sesion_version: int = 0) -> str:
        return self._generar(cuenta_id, sesion_version=sesion_version)

    def decodificar(self, token: str) -> int | None:
        resultado = self._decodificar(token, tipo_esperado=None)
        return resultado[0] if resultado else None

    def decodificar_con_version(self, token: str) -> tuple[int, int] | None:
        """Como `decodificar`, pero además devuelve la versión de sesión embebida en el
        token — se usa para revocar tokens al cerrar sesión sin mantener una blocklist:
        si no calza con `Cuenta.sesion_version` actual, el token es tratado como inválido
        aunque no haya expirado (ver `Cuenta.cerrar_todas_las_sesiones`)."""
        return self._decodificar(token, tipo_esperado=None)

    def generar_admin(self, cuenta_admin_id: int) -> str:
        return self._generar(cuenta_admin_id, tipo="admin")

    def decodificar_admin(self, token: str) -> int | None:
        resultado = self._decodificar(token, tipo_esperado="admin")
        return resultado[0] if resultado else None

    def generar_profesor(self, cuenta_profesor_id: int) -> str:
        return self._generar(cuenta_profesor_id, tipo="profesor")

    def decodificar_profesor(self, token: str) -> int | None:
        resultado = self._decodificar(token, tipo_esperado="profesor")
        return resultado[0] if resultado else None

    def _generar(self, cuenta_id: int, tipo: str | None = None, sesion_version: int = 0) -> str:
        expira = datetime.now(timezone.utc) + timedelta(minutes=settings.jwt_expiracion_minutos)
        payload = {"sub": str(cuenta_id), "exp": expira, "ver": sesion_version}
        if tipo is not None:
            payload["tipo"] = tipo
        return jwt.encode(payload, settings.jwt_secret, algorithm=settings.jwt_algoritmo)

    def _decodificar(self, token: str, tipo_esperado: str | None) -> tuple[int, int] | None:
        try:
            payload = jwt.decode(token, settings.jwt_secret, algorithms=[settings.jwt_algoritmo])
            if payload.get("tipo") != tipo_esperado:
                return None
            return int(payload["sub"]), int(payload.get("ver", 0))
        except (JWTError, KeyError, ValueError):
            return None
