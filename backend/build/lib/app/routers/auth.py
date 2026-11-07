from datetime import date, datetime, timezone

from fastapi import APIRouter, Depends, HTTPException, Request, Response, status
from pydantic import BaseModel, EmailStr, Field, field_validator

from app.application.auth.casos_de_uso import (
    AgregarPerfilAlumno,
    CerrarSesion,
    EliminarAlumno,
    IniciarSesion,
    IniciarSesionConGoogle,
    ListarPerfilesAlumno,
    RegistrarApoderado,
)
from app.application.comercial.casos_de_uso import IniciarPruebaGratis
from app.application.comercial.consultas import ObtenerSuscripcionDeAlumno
from app.application.gamificacion.casos_de_uso import ObtenerPerfilGamificacion
from app.application.progreso.consultas import ObtenerHistorialYNotas
from app.core.deps import (
    get_agregar_perfil_alumno_uc,
    get_cerrar_sesion_uc,
    get_cuenta_actual,
    get_eliminar_alumno_uc,
    get_iniciar_prueba_gratis_uc,
    get_iniciar_sesion_google_uc,
    get_iniciar_sesion_uc,
    get_listar_perfiles_alumno_uc,
    get_obtener_historial_y_notas_uc,
    get_obtener_perfil_gamificacion_uc,
    get_obtener_suscripcion_de_alumno_uc,
    get_registrar_apoderado_uc,
    get_repositorio_contenido,
    get_repositorio_perfiles_alumno,
    get_repositorio_planes,
    verificar_perfil_propio,
)
from app.domain.contenido.ports import RepositorioContenido
from app.domain.auth.ports import RepositorioPerfilesAlumno
from app.domain.gamificacion.entities import CATALOGO_LOGROS
from app.infrastructure.pdf.generador_certificado import generar_pdf_certificado
from app.services.correo import enviar_bienvenida, enviar_confirmacion_plan
from app.infrastructure.pdf.generador_informe_avance import generar_pdf_informe_avance
from app.core.config import settings
from app.core.limiter import limiter
from app.domain.auth.entities import Cuenta
from app.domain.auth.exceptions import (
    CorreoYaRegistrado,
    CredencialesInvalidas,
    GoogleLoginNoConfigurado,
    NivelNoEncontrado,
    RutYaRegistrado,
    TokenGoogleInvalido,
)
from app.domain.auth.value_objects import Rut
from app.domain.comercial.exceptions import AlumnoNoEncontrado, PlanNoEncontrado
from app.domain.comercial.ports import RepositorioPlanes

router = APIRouter(prefix="/auth", tags=["auth"])


class RegistroApoderado(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)
    nombre: str = Field(min_length=1, max_length=120)
    comuna_o_region: str | None = Field(default=None, max_length=120)
    pais: str | None = Field(default=None, max_length=120)


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
    nombre: str = Field(min_length=1, max_length=120)
    apellidos: str = Field(min_length=1, max_length=120)
    fecha_nacimiento: date
    rut: str = Field(max_length=20)
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
    nombre_nivel: str | None = None


@router.post("/registro", response_model=TokenRespuesta, status_code=status.HTTP_201_CREATED)
@limiter.limit(f"{settings.limite_registro_por_minuto}/minute")
def registrar(
    request: Request,
    datos: RegistroApoderado,
    uc: RegistrarApoderado = Depends(get_registrar_apoderado_uc),
):
    try:
        token = uc.ejecutar(datos.email, datos.password, datos.nombre, datos.comuna_o_region, datos.pais)
    except CorreoYaRegistrado:
        raise HTTPException(status_code=400, detail="Ya existe una cuenta con ese correo")
    enviar_bienvenida(datos.email.strip().lower(), datos.nombre)
    return TokenRespuesta(access_token=token)


@router.post("/login", response_model=TokenRespuesta)
@limiter.limit(f"{settings.limite_login_por_minuto}/minute")
def login(request: Request, datos: LoginApoderado, uc: IniciarSesion = Depends(get_iniciar_sesion_uc)):
    try:
        token = uc.ejecutar(datos.email, datos.password)
    except CredencialesInvalidas:
        raise HTTPException(status_code=401, detail="Correo o contraseña incorrectos")
    return TokenRespuesta(access_token=token)


@router.post("/login-google", response_model=TokenRespuesta)
@limiter.limit(f"{settings.limite_login_por_minuto}/minute")
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


@router.post("/logout", status_code=status.HTTP_204_NO_CONTENT)
def logout(cuenta: Cuenta = Depends(get_cuenta_actual), uc: CerrarSesion = Depends(get_cerrar_sesion_uc)):
    """Invalida de inmediato el token actual (y cualquier otro ya emitido para esta
    cuenta) — sin esto, cerrar sesión en el frontend solo borraba el token localmente,
    pero seguía siendo una credencial válida en el servidor hasta expirar."""
    uc.ejecutar(cuenta.id)


@router.post("/alumnos", response_model=PerfilAlumnoRespuesta, status_code=status.HTTP_201_CREATED)
@limiter.limit(f"{settings.limite_agregar_alumno_por_minuto}/minute")
def agregar_alumno(
    request: Request,
    datos: CrearPerfilAlumno,
    cuenta: Cuenta = Depends(get_cuenta_actual),
    uc: AgregarPerfilAlumno = Depends(get_agregar_perfil_alumno_uc),
    repositorio_contenido: RepositorioContenido = Depends(get_repositorio_contenido),
):
    try:
        perfil = uc.ejecutar(
            cuenta_apoderado_id=cuenta.id,
            nombre=datos.nombre,
            apellidos=datos.apellidos,
            fecha_nacimiento=datos.fecha_nacimiento,
            rut=Rut(datos.rut),
            nivel_id=datos.nivel_id,
        )
    except NivelNoEncontrado:
        raise HTTPException(status_code=404, detail="Nivel no encontrado")
    except RutYaRegistrado:
        raise HTTPException(status_code=400, detail="Ya existe un alumno registrado con ese RUT")
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))
    nivel = repositorio_contenido.obtener_nivel(perfil.nivel_id)
    return PerfilAlumnoRespuesta(
        id=perfil.id,
        nombre=perfil.nombre,
        apellidos=perfil.apellidos,
        nivel_id=perfil.nivel_id,
        nombre_nivel=nivel.nombre if nivel else None,
    )


@router.get("/alumnos", response_model=list[PerfilAlumnoRespuesta])
def listar_mis_alumnos(
    cuenta: Cuenta = Depends(get_cuenta_actual),
    uc: ListarPerfilesAlumno = Depends(get_listar_perfiles_alumno_uc),
    repositorio_contenido: RepositorioContenido = Depends(get_repositorio_contenido),
):
    perfiles = uc.ejecutar(cuenta.id)
    niveles = {n.id: n.nombre for n in repositorio_contenido.listar_niveles()}
    return [
        PerfilAlumnoRespuesta(
            id=p.id,
            nombre=p.nombre,
            apellidos=p.apellidos,
            nivel_id=p.nivel_id,
            nombre_nivel=niveles.get(p.nivel_id),
        )
        for p in perfiles
    ]


@router.delete("/alumnos/{perfil_alumno_id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_alumno(
    perfil_alumno_id: int = Depends(verificar_perfil_propio),
    uc: EliminarAlumno = Depends(get_eliminar_alumno_uc),
):
    """Auditoría de seguridad (2026-08-17): borrado en cascada de TODO lo asociado al
    alumno (evaluaciones, progreso, plan de estudio, gamificación, ánimo, sugerencias,
    calificaciones, reportes) — irreversible. `verificar_perfil_propio` ya garantiza que
    el perfil pertenece a la cuenta que pide el borrado."""
    uc.ejecutar(perfil_alumno_id)


class PlanRespuesta(BaseModel):
    id: int
    nombre: str
    precio_clp: int


@router.get("/planes", response_model=list[PlanRespuesta])
def listar_planes(
    cuenta: Cuenta = Depends(get_cuenta_actual),
    repositorio: RepositorioPlanes = Depends(get_repositorio_planes),
):
    return [
        PlanRespuesta(id=p.id, nombre=p.nombre, precio_clp=p.precio_clp)
        for p in repositorio.listar()
        if p.activo
    ]


class PruebaGratisRequest(BaseModel):
    plan_id: int


class PruebaGratisRespuesta(BaseModel):
    fecha_termino: str


@router.post("/alumnos/{perfil_alumno_id}/prueba-gratis", response_model=PruebaGratisRespuesta)
def iniciar_prueba_gratis(
    datos: PruebaGratisRequest,
    perfil_alumno_id: int = Depends(verificar_perfil_propio),
    cuenta: Cuenta = Depends(get_cuenta_actual),
    uc: IniciarPruebaGratis = Depends(get_iniciar_prueba_gratis_uc),
    repositorio_perfiles: RepositorioPerfilesAlumno = Depends(get_repositorio_perfiles_alumno),
    repositorio_planes: RepositorioPlanes = Depends(get_repositorio_planes),
):
    try:
        fecha_termino = uc.ejecutar(perfil_alumno_id, datos.plan_id)
    except AlumnoNoEncontrado:
        raise HTTPException(status_code=404, detail="Alumno no encontrado")
    except PlanNoEncontrado:
        raise HTTPException(status_code=404, detail="Plan no encontrado")

    perfil = repositorio_perfiles.buscar_por_id(perfil_alumno_id)
    plan = repositorio_planes.buscar_por_id(datos.plan_id)
    if perfil and plan:
        enviar_confirmacion_plan(cuenta.email, perfil.nombre, plan.nombre)

    return PruebaGratisRespuesta(fecha_termino=fecha_termino.isoformat())


@router.get("/alumnos/{perfil_alumno_id}/certificado.pdf")
def descargar_certificado_alumno_regular(
    perfil_alumno_id: int = Depends(verificar_perfil_propio),
    repositorio_perfiles: RepositorioPerfilesAlumno = Depends(get_repositorio_perfiles_alumno),
    repositorio_contenido: RepositorioContenido = Depends(get_repositorio_contenido),
):
    """Fase 1, ítem 2.7 (ver planificacion/27-plan-incorporacion-hallazgos-brincus.md) —
    constancia de inscripción en PDF, no un certificado oficial de aprobación del Examen
    Libre (ver el disclaimer dentro del propio PDF)."""
    perfil = repositorio_perfiles.buscar_por_id(perfil_alumno_id)
    if not perfil:
        raise HTTPException(status_code=404, detail="Perfil de alumno no encontrado")
    nivel = next((n for n in repositorio_contenido.listar_niveles() if n.id == perfil.nivel_id), None)
    nivel_nombre = nivel.nombre if nivel else "su nivel actual"

    pdf_bytes = generar_pdf_certificado(
        nombre_completo=f"{perfil.nombre} {perfil.apellidos}",
        nivel_nombre=nivel_nombre,
        fecha=datetime.now(timezone.utc).date(),
    )
    # Los headers HTTP deben ser ASCII — un nombre con tilde (ej. "María") rompía la
    # respuesta completa (UnicodeDecodeError en el cliente). El PDF en sí sí soporta
    # tildes (ver sanitizar_para_pdf, que trabaja en latin-1, no ASCII puro).
    nombre_archivo_ascii = perfil.nombre.encode("ascii", errors="ignore").decode("ascii").strip() or "alumno"
    return Response(
        content=pdf_bytes,
        media_type="application/pdf",
        headers={"Content-Disposition": f'inline; filename="certificado-{nombre_archivo_ascii}.pdf"'},
    )


@router.get("/alumnos/{perfil_alumno_id}/informe-avance.pdf")
def descargar_informe_avance(
    perfil_alumno_id: int = Depends(verificar_perfil_propio),
    repositorio_perfiles: RepositorioPerfilesAlumno = Depends(get_repositorio_perfiles_alumno),
    repositorio_contenido: RepositorioContenido = Depends(get_repositorio_contenido),
    historial_uc: ObtenerHistorialYNotas = Depends(get_obtener_historial_y_notas_uc),
    gamificacion_uc: ObtenerPerfilGamificacion = Depends(get_obtener_perfil_gamificacion_uc),
):
    """Informe de avance descargable para el Apoderado (Fase 1, ver
    planificacion/27-plan-incorporacion-hallazgos-brincus.md) — reutiliza los mismos datos
    que ya muestran /alumno/notas y /alumno/logros, solo los empaqueta en PDF."""
    perfil = repositorio_perfiles.buscar_por_id(perfil_alumno_id)
    if not perfil:
        raise HTTPException(status_code=404, detail="Perfil de alumno no encontrado")
    nivel = next((n for n in repositorio_contenido.listar_niveles() if n.id == perfil.nivel_id), None)
    nivel_nombre = nivel.nombre if nivel else "su nivel actual"

    resultado = historial_uc.ejecutar(perfil_alumno_id)
    perfil_gamificacion = gamificacion_uc.ejecutar(perfil_alumno_id)

    pdf_bytes = generar_pdf_informe_avance(
        nombre_completo=f"{perfil.nombre} {perfil.apellidos}",
        nivel_nombre=nivel_nombre,
        resultado=resultado,
        racha_dias_actual=perfil_gamificacion.racha_dias_actual,
        logros_desbloqueados=len(perfil_gamificacion.logros_desbloqueados()),
        logros_totales=len(CATALOGO_LOGROS),
        fecha=datetime.now(timezone.utc).date(),
    )
    nombre_archivo_ascii = perfil.nombre.encode("ascii", errors="ignore").decode("ascii").strip() or "alumno"
    return Response(
        content=pdf_bytes,
        media_type="application/pdf",
        headers={"Content-Disposition": f'inline; filename="informe-avance-{nombre_archivo_ascii}.pdf"'},
    )


class SuscripcionRespuesta(BaseModel):
    plan_id: int
    plan_nombre: str
    fecha_inicio: datetime
    fecha_termino: datetime | None
    estado: str
    origen: str


@router.get("/alumnos/{perfil_alumno_id}/suscripcion", response_model=SuscripcionRespuesta | None)
def obtener_suscripcion(
    perfil_alumno_id: int = Depends(verificar_perfil_propio),
    uc: ObtenerSuscripcionDeAlumno = Depends(get_obtener_suscripcion_de_alumno_uc),
):
    """Fase 1, ítem 2.8 (ver planificacion/27-plan-incorporacion-hallazgos-brincus.md) —
    historial de pagos para el Apoderado, con los datos que ya existen hoy (plan activo,
    fechas, origen). `Suscripcion` no acumula historial de transacciones todavía (una
    fila vigente por alumno) — el comprobante de pago con monto real queda pendiente de
    la pasarela de pago real, no se promete acá."""
    suscripcion = uc.ejecutar(perfil_alumno_id)
    if not suscripcion:
        return None
    return SuscripcionRespuesta(
        plan_id=suscripcion.plan_id,
        plan_nombre=suscripcion.plan_nombre,
        fecha_inicio=suscripcion.fecha_inicio,
        fecha_termino=suscripcion.fecha_termino,
        estado=suscripcion.estado,
        origen=suscripcion.origen,
    )
