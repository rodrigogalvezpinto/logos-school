from datetime import date

from fastapi import APIRouter, Depends, HTTPException, Request, status
from pydantic import BaseModel, EmailStr, field_validator

from app.application.auth.casos_de_uso import (
    AgregarPerfilAlumno,
    IniciarSesion,
    IniciarSesionConGoogle,
    ListarPerfilesAlumno,
    RegistrarApoderado,
)
from app.core.deps import (
    get_agregar_perfil_alumno_uc,
    get_cuenta_actual,
    get_iniciar_sesion_google_uc,
    get_iniciar_sesion_uc,
    get_listar_perfiles_alumno_uc,
    get_registrar_apoderado_uc,
)
from app.core.limiter import limiter
from app.domain.auth.entities import Cuenta
from app.domain.auth.exceptions import CorreoYaRegistrado, CredencialesInvalidas, GoogleLoginNoConfigurado, TokenGoogleInvalido
from app.domain.auth.value_objects import Rut

router = APIRouter(prefix="/auth", tags=["auth"])


class RegistroApoderado(BaseModel):
    email: EmailStr
    password: str
    nombre: str
    comuna_o_region: str | None = None
    pais: str | None = None


class LoginApoderado(BaseModel):
    email: EmailStr
    password: str


class LoginGoogle(BaseModel):
    id_token: str


class TokenRespuesta(BaseModel):
    access_token: str
    token_type: str = "bearer"


class CuentaRespuesta(BaseModel):
    id: int
    email: str
    nombre: str


class CrearPerfilAlumno(BaseModel):
    nombre: str
    apellidos: str
    fecha_nacimiento: date
    rut: str
    nivel_id: int

    @field_validator("rut")
    @classmethod
    def _validar_rut(cls, v: str) -> str:
        Rut(v)  # lanza ValueError si es inválido — FastAPI lo traduce automáticamente a 422
        return v


class PerfilAlumnoRespuesta(BaseModel):
    id: int
    nombre: str
    apellidos: str
    nivel_id: int


@router.post("/registro", response_model=TokenRespuesta, status_code=status.HTTP_201_CREATED)
@limiter.limit("5/minute")
def registrar(
    request: Request,
    datos: RegistroApoderado,
    uc: RegistrarApoderado = Depends(get_registrar_apoderado_uc),
):
    try:
        token = uc.ejecutar(datos.email, datos.password, datos.nombre, datos.comuna_o_region, datos.pais)
    except CorreoYaRegistrado:
        raise HTTPException(status_code=400, detail="Ya existe una cuenta con ese correo")
    return TokenRespuesta(access_token=token)


@router.post("/login", response_model=TokenRespuesta)
@limiter.limit("10/minute")
def login(request: Request, datos: LoginApoderado, uc: IniciarSesion = Depends(get_iniciar_sesion_uc)):
    try:
        token = uc.ejecutar(datos.email, datos.password)
    except CredencialesInvalidas:
        raise HTTPException(status_code=401, detail="Correo o contraseña incorrectos")
    return TokenRespuesta(access_token=token)


@router.post("/login-google", response_model=TokenRespuesta)
@limiter.limit("10/minute")
def login_google(
    request: Request,
    datos: LoginGoogle,
    uc: IniciarSesionConGoogle = Depends(get_iniciar_sesion_google_uc),
):
    try:
        token = uc.ejecutar(datos.id_token)
    except GoogleLoginNoConfigurado:
        raise HTTPException(
            status_code=503,
            detail="Login con Google no está configurado todavía (falta GOOGLE_CLIENT_ID)",
        )
    except TokenGoogleInvalido:
        raise HTTPException(status_code=401, detail="Token de Google inválido")
    return TokenRespuesta(access_token=token)


@router.get("/yo", response_model=CuentaRespuesta)
def yo(cuenta: Cuenta = Depends(get_cuenta_actual)):
    return CuentaRespuesta(id=cuenta.id, email=cuenta.email, nombre=cuenta.nombre)


@router.post("/alumnos", response_model=PerfilAlumnoRespuesta, status_code=status.HTTP_201_CREATED)
def agregar_alumno(
    datos: CrearPerfilAlumno,
    cuenta: Cuenta = Depends(get_cuenta_actual),
    uc: AgregarPerfilAlumno = Depends(get_agregar_perfil_alumno_uc),
):
    perfil = uc.ejecutar(
        cuenta_apoderado_id=cuenta.id,
        nombre=datos.nombre,
        apellidos=datos.apellidos,
        fecha_nacimiento=datos.fecha_nacimiento,
        rut=Rut(datos.rut),
        nivel_id=datos.nivel_id,
    )
    return PerfilAlumnoRespuesta(id=perfil.id, nombre=perfil.nombre, apellidos=perfil.apellidos, nivel_id=perfil.nivel_id)


@router.get("/alumnos", response_model=list[PerfilAlumnoRespuesta])
def listar_mis_alumnos(
    cuenta: Cuenta = Depends(get_cuenta_actual),
    uc: ListarPerfilesAlumno = Depends(get_listar_perfiles_alumno_uc),
):
    perfiles = uc.ejecutar(cuenta.id)
    return [
        PerfilAlumnoRespuesta(id=p.id, nombre=p.nombre, apellidos=p.apellidos, nivel_id=p.nivel_id)
        for p in perfiles
    ]
