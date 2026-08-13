"""Login del panel de administración comercial — cuenta separada de Apoderado, sin
endpoint de auto-registro (planificacion/18-panel-administrador.md: "solo para el usuario
dueño del proyecto y quien él autorice"). Las cuentas se crean con scripts/crear_admin.py."""

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, EmailStr

from app.application.admin.casos_de_uso import IniciarSesionAdmin
from app.core.deps import get_cuenta_admin_actual, get_iniciar_sesion_admin_uc
from app.domain.admin.entities import CuentaAdmin
from app.domain.admin.exceptions import CredencialesAdminInvalidas

router = APIRouter(prefix="/admin/auth", tags=["admin-auth"])


class LoginAdmin(BaseModel):
    email: EmailStr
    password: str


class TokenAdminRespuesta(BaseModel):
    access_token: str
    token_type: str = "bearer"


class CuentaAdminRespuesta(BaseModel):
    id: int
    email: str
    nombre: str


@router.post("/login", response_model=TokenAdminRespuesta)
def login(datos: LoginAdmin, uc: IniciarSesionAdmin = Depends(get_iniciar_sesion_admin_uc)):
    try:
        token = uc.ejecutar(datos.email, datos.password)
    except CredencialesAdminInvalidas:
        raise HTTPException(status_code=401, detail="Correo o contraseña incorrectos")
    return TokenAdminRespuesta(access_token=token)


@router.get("/yo", response_model=CuentaAdminRespuesta)
def yo(cuenta: CuentaAdmin = Depends(get_cuenta_admin_actual)):
    return CuentaAdminRespuesta(id=cuenta.id, email=cuenta.email, nombre=cuenta.nombre)
