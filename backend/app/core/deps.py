from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlmodel import Session

from app.core.db import get_session
from app.core.seguridad import decodificar_token
from app.models import Cuenta

security = HTTPBearer()


def get_cuenta_actual(
    credenciales: HTTPAuthorizationCredentials = Depends(security),
    session: Session = Depends(get_session),
) -> Cuenta:
    cuenta_id = decodificar_token(credenciales.credentials)
    if cuenta_id is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Sesión inválida o expirada")
    cuenta = session.get(Cuenta, cuenta_id)
    if cuenta is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Cuenta no encontrada")
    return cuenta
