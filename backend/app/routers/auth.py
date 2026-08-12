from datetime import date

from fastapi import APIRouter, Depends, HTTPException, Request, status
from google.auth.transport import requests as google_requests
from google.oauth2 import id_token
from pydantic import BaseModel, EmailStr
from sqlmodel import Session, select

from app.core.config import settings
from app.core.db import get_session
from app.core.deps import get_cuenta_actual
from app.core.limiter import limiter
from app.core.seguridad import crear_token, hashear_password, verificar_password
from app.models import Cuenta, PerfilAlumno

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


class PerfilAlumnoRespuesta(BaseModel):
    id: int
    nombre: str
    apellidos: str
    nivel_id: int


@router.post("/registro", response_model=TokenRespuesta, status_code=status.HTTP_201_CREATED)
@limiter.limit("5/minute")
def registrar(request: Request, datos: RegistroApoderado, session: Session = Depends(get_session)):
    existente = session.exec(select(Cuenta).where(Cuenta.email == datos.email)).first()
    if existente:
        raise HTTPException(status_code=400, detail="Ya existe una cuenta con ese correo")

    cuenta = Cuenta(
        email=datos.email,
        password_hash=hashear_password(datos.password),
        nombre=datos.nombre,
        comuna_o_region=datos.comuna_o_region,
        pais=datos.pais,
    )
    session.add(cuenta)
    session.commit()
    session.refresh(cuenta)
    return TokenRespuesta(access_token=crear_token(cuenta.id))


@router.post("/login", response_model=TokenRespuesta)
@limiter.limit("10/minute")
def login(request: Request, datos: LoginApoderado, session: Session = Depends(get_session)):
    cuenta = session.exec(select(Cuenta).where(Cuenta.email == datos.email)).first()
    if not cuenta or not cuenta.password_hash or not verificar_password(datos.password, cuenta.password_hash):
        # Mensaje genérico a propósito: no revelar si el correo existe o no (evita
        # que un atacante use el login para enumerar cuentas registradas).
        raise HTTPException(status_code=401, detail="Correo o contraseña incorrectos")
    return TokenRespuesta(access_token=crear_token(cuenta.id))


@router.post("/login-google", response_model=TokenRespuesta)
@limiter.limit("10/minute")
def login_google(request: Request, datos: LoginGoogle, session: Session = Depends(get_session)):
    if not settings.google_client_id:
        raise HTTPException(
            status_code=503,
            detail="Login con Google no está configurado todavía (falta GOOGLE_CLIENT_ID)",
        )
    try:
        info = id_token.verify_oauth2_token(
            datos.id_token, google_requests.Request(), settings.google_client_id
        )
    except ValueError:
        raise HTTPException(status_code=401, detail="Token de Google inválido")

    google_id = info["sub"]
    email = info["email"]
    nombre = info.get("name", email)

    cuenta = session.exec(select(Cuenta).where(Cuenta.google_id == google_id)).first()
    if not cuenta:
        cuenta = session.exec(select(Cuenta).where(Cuenta.email == email)).first()
        if cuenta:
            cuenta.google_id = google_id  # vincula Google a una cuenta ya existente con ese correo
        else:
            cuenta = Cuenta(email=email, nombre=nombre, google_id=google_id)
        session.add(cuenta)
        session.commit()
        session.refresh(cuenta)

    return TokenRespuesta(access_token=crear_token(cuenta.id))


@router.get("/yo", response_model=CuentaRespuesta)
def yo(cuenta: Cuenta = Depends(get_cuenta_actual)):
    return CuentaRespuesta(id=cuenta.id, email=cuenta.email, nombre=cuenta.nombre)


@router.post("/alumnos", response_model=PerfilAlumnoRespuesta, status_code=status.HTTP_201_CREATED)
def agregar_alumno(
    datos: CrearPerfilAlumno,
    cuenta: Cuenta = Depends(get_cuenta_actual),
    session: Session = Depends(get_session),
):
    perfil = PerfilAlumno(
        cuenta_apoderado_id=cuenta.id,
        nombre=datos.nombre,
        apellidos=datos.apellidos,
        fecha_nacimiento=datos.fecha_nacimiento,
        rut=datos.rut,
        nivel_id=datos.nivel_id,
    )
    session.add(perfil)
    session.commit()
    session.refresh(perfil)
    return PerfilAlumnoRespuesta(
        id=perfil.id, nombre=perfil.nombre, apellidos=perfil.apellidos, nivel_id=perfil.nivel_id
    )


@router.get("/alumnos", response_model=list[PerfilAlumnoRespuesta])
def listar_mis_alumnos(cuenta: Cuenta = Depends(get_cuenta_actual), session: Session = Depends(get_session)):
    perfiles = session.exec(
        select(PerfilAlumno).where(PerfilAlumno.cuenta_apoderado_id == cuenta.id)
    ).all()
    return [
        PerfilAlumnoRespuesta(id=p.id, nombre=p.nombre, apellidos=p.apellidos, nivel_id=p.nivel_id)
        for p in perfiles
    ]
