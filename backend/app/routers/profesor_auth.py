"""Login y registro del rol Profesor (Etapa 2) — a diferencia del panel Admin, sí tiene
auto-registro, pero la cuenta nace `estado="pendiente"` y no puede crear/gestionar cursos
hasta que un Administrador la aprueba desde /admin/profesores."""

from fastapi import APIRouter, Depends, HTTPException, Request
from pydantic import BaseModel, EmailStr

from app.application.profesor.casos_de_uso import IniciarSesionProfesor, RegistrarProfesor
from app.core.config import settings
from app.core.deps import get_cuenta_profesor_actual, get_iniciar_sesion_profesor_uc, get_registrar_profesor_uc
from app.core.limiter import limiter
from app.domain.profesor.entities import CuentaProfesor
from app.domain.profesor.exceptions import CorreoYaRegistrado, CredencialesProfesorInvalidas

router = APIRouter(prefix="/profesor/auth", tags=["profesor-auth"])


class RegistroProfesor(BaseModel):
    email: EmailStr
    password: str
    nombre: str


class LoginProfesor(BaseModel):
    email: EmailStr
    password: str


class TokenProfesorRespuesta(BaseModel):
    access_token: str
    token_type: str = "bearer"


class CuentaProfesorRespuesta(BaseModel):
    id: int
    email: str
    nombre: str
    estado: str


@router.post("/registro", response_model=TokenProfesorRespuesta, status_code=201)
@limiter.limit(f"{settings.limite_registro_profesor_por_minuto}/minute")
def registrar(request: Request, datos: RegistroProfesor, uc: RegistrarProfesor = Depends(get_registrar_profesor_uc)):
    try:
        token = uc.ejecutar(datos.email, datos.password, datos.nombre)
    except CorreoYaRegistrado:
        raise HTTPException(status_code=400, detail="Ya existe una cuenta de profesor con ese correo")
    return TokenProfesorRespuesta(access_token=token)


@router.post("/login", response_model=TokenProfesorRespuesta)
@limiter.limit(f"{settings.limite_login_profesor_por_minuto}/minute")
def login(request: Request, datos: LoginProfesor, uc: IniciarSesionProfesor = Depends(get_iniciar_sesion_profesor_uc)):
    try:
        token = uc.ejecutar(datos.email, datos.password)
    except CredencialesProfesorInvalidas:
        raise HTTPException(status_code=401, detail="Correo o contraseña incorrectos")
    return TokenProfesorRespuesta(access_token=token)


@router.get("/yo", response_model=CuentaProfesorRespuesta)
def yo(cuenta: CuentaProfesor = Depends(get_cuenta_profesor_actual)):
    return CuentaProfesorRespuesta(id=cuenta.id, email=cuenta.email, nombre=cuenta.nombre, estado=cuenta.estado)
