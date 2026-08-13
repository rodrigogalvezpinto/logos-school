"""Composition root: aquí se cablean los adaptadores concretos de `infrastructure/` a
los puertos que consumen los casos de uso de `application/`, vía `Depends` de FastAPI.
Los routers nunca instancian un adaptador directo — siempre a través de estas factories."""

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlmodel import Session

from app.application.auth.casos_de_uso import (
    AgregarPerfilAlumno,
    IniciarSesion,
    IniciarSesionConGoogle,
    ListarPerfilesAlumno,
    RegistrarApoderado,
)
from app.application.evaluaciones.casos_de_uso import (
    EntregarIntento,
    IniciarIntento,
    ObtenerIntento,
    ResponderPregunta,
)
from app.application.admin.casos_de_uso import IniciarSesionAdmin
from app.application.comercial.casos_de_uso import (
    AsignarSuscripcionCortesia,
    CambiarEstadoPlan,
    CrearCodigoDescuento,
    CrearPlan,
    DesactivarCodigoDescuento,
    EditarPlan,
)
from app.application.comercial.consultas import BuscarAlumnos, ObtenerMetricas
from app.application.progreso.consultas import ObtenerHistorialYNotas
from app.application.progreso.marcar_guia_revisada import MarcarGuiaRevisada
from app.infrastructure.persistence.db import get_session
from app.domain.admin.entities import CuentaAdmin
from app.domain.auth.entities import Cuenta
from app.infrastructure.auth_externa.google_oauth import VerificadorTokenGoogleAdapter
from app.infrastructure.persistence.repositorios.conjuntos import RepositorioConjuntosSQLModel
from app.infrastructure.persistence.repositorios.contenido import RepositorioContenidoSQLModel
from app.infrastructure.persistence.repositorios.cuentas import RepositorioCuentasSQLModel
from app.infrastructure.persistence.repositorios.cuentas_admin import RepositorioCuentasAdminSQLModel
from app.infrastructure.persistence.repositorios.descuentos import RepositorioDescuentosSQLModel
from app.infrastructure.persistence.repositorios.intentos import RepositorioIntentosSQLModel
from app.infrastructure.persistence.repositorios.perfiles_alumno import RepositorioPerfilesAlumnoSQLModel
from app.infrastructure.persistence.repositorios.planes import RepositorioPlanesSQLModel
from app.infrastructure.persistence.repositorios.preguntas import RepositorioPreguntasSQLModel
from app.infrastructure.persistence.repositorios.progreso import RepositorioProgresoSQLModel
from app.infrastructure.persistence.repositorios.suscripciones import RepositorioSuscripcionesSQLModel
from app.infrastructure.reloj_sistema import RelojSistema
from app.infrastructure.seguridad.bcrypt_hasheador import HasheadorPasswordBcrypt
from app.infrastructure.seguridad.jose_tokens import ServicioTokenJWT

security = HTTPBearer()


def get_repositorio_cuentas(session: Session = Depends(get_session)) -> RepositorioCuentasSQLModel:
    return RepositorioCuentasSQLModel(session)


def get_repositorio_perfiles_alumno(session: Session = Depends(get_session)) -> RepositorioPerfilesAlumnoSQLModel:
    return RepositorioPerfilesAlumnoSQLModel(session)


def get_hasheador_password() -> HasheadorPasswordBcrypt:
    return HasheadorPasswordBcrypt()


def get_servicio_token() -> ServicioTokenJWT:
    return ServicioTokenJWT()


def get_verificador_google() -> VerificadorTokenGoogleAdapter:
    return VerificadorTokenGoogleAdapter()


def get_registrar_apoderado_uc(
    repositorio: RepositorioCuentasSQLModel = Depends(get_repositorio_cuentas),
    hasheador: HasheadorPasswordBcrypt = Depends(get_hasheador_password),
    servicio_token: ServicioTokenJWT = Depends(get_servicio_token),
) -> RegistrarApoderado:
    return RegistrarApoderado(repositorio, hasheador, servicio_token)


def get_iniciar_sesion_uc(
    repositorio: RepositorioCuentasSQLModel = Depends(get_repositorio_cuentas),
    hasheador: HasheadorPasswordBcrypt = Depends(get_hasheador_password),
    servicio_token: ServicioTokenJWT = Depends(get_servicio_token),
) -> IniciarSesion:
    return IniciarSesion(repositorio, hasheador, servicio_token)


def get_iniciar_sesion_google_uc(
    repositorio: RepositorioCuentasSQLModel = Depends(get_repositorio_cuentas),
    verificador_google: VerificadorTokenGoogleAdapter = Depends(get_verificador_google),
    servicio_token: ServicioTokenJWT = Depends(get_servicio_token),
) -> IniciarSesionConGoogle:
    return IniciarSesionConGoogle(repositorio, verificador_google, servicio_token)


def get_agregar_perfil_alumno_uc(
    repositorio: RepositorioPerfilesAlumnoSQLModel = Depends(get_repositorio_perfiles_alumno),
) -> AgregarPerfilAlumno:
    return AgregarPerfilAlumno(repositorio)


def get_listar_perfiles_alumno_uc(
    repositorio: RepositorioPerfilesAlumnoSQLModel = Depends(get_repositorio_perfiles_alumno),
) -> ListarPerfilesAlumno:
    return ListarPerfilesAlumno(repositorio)


def get_repositorio_contenido(session: Session = Depends(get_session)) -> RepositorioContenidoSQLModel:
    return RepositorioContenidoSQLModel(session)


def get_repositorio_intentos(session: Session = Depends(get_session)) -> RepositorioIntentosSQLModel:
    return RepositorioIntentosSQLModel(session)


def get_repositorio_conjuntos(session: Session = Depends(get_session)) -> RepositorioConjuntosSQLModel:
    return RepositorioConjuntosSQLModel(session)


def get_repositorio_preguntas(session: Session = Depends(get_session)) -> RepositorioPreguntasSQLModel:
    return RepositorioPreguntasSQLModel(session)


def get_reloj() -> RelojSistema:
    return RelojSistema()


def get_iniciar_intento_uc(
    repositorio_intentos: RepositorioIntentosSQLModel = Depends(get_repositorio_intentos),
    repositorio_conjuntos: RepositorioConjuntosSQLModel = Depends(get_repositorio_conjuntos),
    repositorio_perfiles: RepositorioPerfilesAlumnoSQLModel = Depends(get_repositorio_perfiles_alumno),
    reloj: RelojSistema = Depends(get_reloj),
) -> IniciarIntento:
    return IniciarIntento(repositorio_intentos, repositorio_conjuntos, repositorio_perfiles, reloj)


def get_obtener_intento_uc(
    repositorio_intentos: RepositorioIntentosSQLModel = Depends(get_repositorio_intentos),
) -> ObtenerIntento:
    return ObtenerIntento(repositorio_intentos)


def get_responder_pregunta_uc(
    repositorio_intentos: RepositorioIntentosSQLModel = Depends(get_repositorio_intentos),
) -> ResponderPregunta:
    return ResponderPregunta(repositorio_intentos)


def get_entregar_intento_uc(
    repositorio_intentos: RepositorioIntentosSQLModel = Depends(get_repositorio_intentos),
    repositorio_conjuntos: RepositorioConjuntosSQLModel = Depends(get_repositorio_conjuntos),
    repositorio_preguntas: RepositorioPreguntasSQLModel = Depends(get_repositorio_preguntas),
    reloj: RelojSistema = Depends(get_reloj),
) -> EntregarIntento:
    return EntregarIntento(repositorio_intentos, repositorio_conjuntos, repositorio_preguntas, reloj)


def get_repositorio_progreso(session: Session = Depends(get_session)) -> RepositorioProgresoSQLModel:
    return RepositorioProgresoSQLModel(session)


def get_obtener_historial_y_notas_uc(
    repositorio_intentos: RepositorioIntentosSQLModel = Depends(get_repositorio_intentos),
    repositorio_conjuntos: RepositorioConjuntosSQLModel = Depends(get_repositorio_conjuntos),
    repositorio_contenido: RepositorioContenidoSQLModel = Depends(get_repositorio_contenido),
    repositorio_progreso: RepositorioProgresoSQLModel = Depends(get_repositorio_progreso),
) -> ObtenerHistorialYNotas:
    return ObtenerHistorialYNotas(repositorio_intentos, repositorio_conjuntos, repositorio_contenido, repositorio_progreso)


def get_marcar_guia_revisada_uc(
    repositorio_progreso: RepositorioProgresoSQLModel = Depends(get_repositorio_progreso),
    reloj: RelojSistema = Depends(get_reloj),
) -> MarcarGuiaRevisada:
    return MarcarGuiaRevisada(repositorio_progreso, reloj)


def get_cuenta_actual(
    credenciales: HTTPAuthorizationCredentials = Depends(security),
    servicio_token: ServicioTokenJWT = Depends(get_servicio_token),
    repositorio: RepositorioCuentasSQLModel = Depends(get_repositorio_cuentas),
) -> Cuenta:
    cuenta_id = servicio_token.decodificar(credenciales.credentials)
    if cuenta_id is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Sesión inválida o expirada")
    cuenta = repositorio.buscar_por_id(cuenta_id)
    if cuenta is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Cuenta no encontrada")
    return cuenta


def get_repositorio_cuentas_admin(session: Session = Depends(get_session)) -> RepositorioCuentasAdminSQLModel:
    return RepositorioCuentasAdminSQLModel(session)


def get_repositorio_planes(session: Session = Depends(get_session)) -> RepositorioPlanesSQLModel:
    return RepositorioPlanesSQLModel(session)


def get_repositorio_descuentos(session: Session = Depends(get_session)) -> RepositorioDescuentosSQLModel:
    return RepositorioDescuentosSQLModel(session)


def get_repositorio_suscripciones(session: Session = Depends(get_session)) -> RepositorioSuscripcionesSQLModel:
    return RepositorioSuscripcionesSQLModel(session)


def get_iniciar_sesion_admin_uc(
    repositorio: RepositorioCuentasAdminSQLModel = Depends(get_repositorio_cuentas_admin),
    hasheador: HasheadorPasswordBcrypt = Depends(get_hasheador_password),
    servicio_token: ServicioTokenJWT = Depends(get_servicio_token),
) -> IniciarSesionAdmin:
    return IniciarSesionAdmin(repositorio, hasheador, servicio_token)


def get_cuenta_admin_actual(
    credenciales: HTTPAuthorizationCredentials = Depends(security),
    servicio_token: ServicioTokenJWT = Depends(get_servicio_token),
    repositorio: RepositorioCuentasAdminSQLModel = Depends(get_repositorio_cuentas_admin),
) -> CuentaAdmin:
    cuenta_admin_id = servicio_token.decodificar_admin(credenciales.credentials)
    if cuenta_admin_id is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Sesión de administrador inválida o expirada")
    cuenta = repositorio.buscar_por_id(cuenta_admin_id)
    if cuenta is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Cuenta de administrador no encontrada")
    return cuenta


def get_crear_plan_uc(repositorio: RepositorioPlanesSQLModel = Depends(get_repositorio_planes)) -> CrearPlan:
    return CrearPlan(repositorio)


def get_editar_plan_uc(repositorio: RepositorioPlanesSQLModel = Depends(get_repositorio_planes)) -> EditarPlan:
    return EditarPlan(repositorio)


def get_cambiar_estado_plan_uc(
    repositorio: RepositorioPlanesSQLModel = Depends(get_repositorio_planes),
) -> CambiarEstadoPlan:
    return CambiarEstadoPlan(repositorio)


def get_crear_codigo_descuento_uc(
    repositorio: RepositorioDescuentosSQLModel = Depends(get_repositorio_descuentos),
) -> CrearCodigoDescuento:
    return CrearCodigoDescuento(repositorio)


def get_desactivar_codigo_descuento_uc(
    repositorio: RepositorioDescuentosSQLModel = Depends(get_repositorio_descuentos),
    reloj: RelojSistema = Depends(get_reloj),
) -> DesactivarCodigoDescuento:
    return DesactivarCodigoDescuento(repositorio, reloj)


def get_asignar_suscripcion_cortesia_uc(
    repositorio_suscripciones: RepositorioSuscripcionesSQLModel = Depends(get_repositorio_suscripciones),
    repositorio_perfiles: RepositorioPerfilesAlumnoSQLModel = Depends(get_repositorio_perfiles_alumno),
    repositorio_planes: RepositorioPlanesSQLModel = Depends(get_repositorio_planes),
    reloj: RelojSistema = Depends(get_reloj),
) -> AsignarSuscripcionCortesia:
    return AsignarSuscripcionCortesia(repositorio_suscripciones, repositorio_perfiles, repositorio_planes, reloj)


def get_buscar_alumnos_uc(
    repositorio_perfiles: RepositorioPerfilesAlumnoSQLModel = Depends(get_repositorio_perfiles_alumno),
    repositorio_cuentas: RepositorioCuentasSQLModel = Depends(get_repositorio_cuentas),
) -> BuscarAlumnos:
    return BuscarAlumnos(repositorio_perfiles, repositorio_cuentas)


def get_obtener_metricas_uc(
    repositorio_cuentas: RepositorioCuentasSQLModel = Depends(get_repositorio_cuentas),
    repositorio_perfiles: RepositorioPerfilesAlumnoSQLModel = Depends(get_repositorio_perfiles_alumno),
    repositorio_planes: RepositorioPlanesSQLModel = Depends(get_repositorio_planes),
    repositorio_suscripciones: RepositorioSuscripcionesSQLModel = Depends(get_repositorio_suscripciones),
) -> ObtenerMetricas:
    return ObtenerMetricas(repositorio_cuentas, repositorio_perfiles, repositorio_planes, repositorio_suscripciones)


def verificar_perfil_propio(
    perfil_alumno_id: int,
    cuenta: Cuenta = Depends(get_cuenta_actual),
    repositorio: RepositorioPerfilesAlumnoSQLModel = Depends(get_repositorio_perfiles_alumno),
) -> int:
    """Dependencia reutilizable para endpoints con datos personales de un Alumno: exige
    que el `perfil_alumno_id` de la ruta pertenezca a la Cuenta autenticada."""
    perfil = repositorio.buscar_por_id(perfil_alumno_id)
    if perfil is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Perfil de alumno no encontrado")
    if perfil.cuenta_apoderado_id != cuenta.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Ese perfil no pertenece a tu cuenta")
    return perfil_alumno_id
