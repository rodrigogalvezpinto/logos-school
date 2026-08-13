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
    GenerarSimulacroParcial,
    IniciarIntento,
    ObtenerIntento,
    ResponderPregunta,
)
from app.application.plan_estudio.casos_de_uso import CrearPlanDeEstudio, ObtenerPlanActivo
from app.application.admin.casos_de_uso import IniciarSesionAdmin
from app.application.admin.casos_de_uso_profesores import AprobarProfesor, ListarProfesoresPendientes, RechazarProfesor
from app.application.comercial.casos_de_uso import (
    AsignarSuscripcionCortesia,
    CambiarEstadoPlan,
    CrearCodigoDescuento,
    CrearPlan,
    DesactivarCodigoDescuento,
    EditarPlan,
    IniciarPruebaGratis,
)
from app.application.comercial.consultas import BuscarAlumnos, ObtenerMetricas
from app.application.curso_seccion.casos_de_uso import (
    AgregarAlumnoACurso,
    CrearCursoSeccion,
    PublicarComunicado,
    QuitarAlumnoDeCurso,
)
from app.application.curso_seccion.consultas import ObtenerMiCurso, ObtenerProgresoDeCurso
from app.application.profesor.casos_de_uso import IniciarSesionProfesor, RegistrarProfesor
from app.application.progreso.consultas import ObtenerFaltantes, ObtenerHistorialYNotas
from app.application.progreso.marcar_guia_revisada import MarcarGuiaRevisada
from app.infrastructure.persistence.db import get_session
from app.domain.admin.entities import CuentaAdmin
from app.domain.auth.entities import Cuenta
from app.domain.profesor.entities import CuentaProfesor
from app.infrastructure.auth_externa.google_oauth import VerificadorTokenGoogleAdapter
from app.infrastructure.persistence.repositorios.comunicados import RepositorioComunicadosSQLModel
from app.infrastructure.persistence.repositorios.conjuntos import RepositorioConjuntosSQLModel
from app.infrastructure.persistence.repositorios.contenido import RepositorioContenidoSQLModel
from app.infrastructure.persistence.repositorios.cuentas import RepositorioCuentasSQLModel
from app.infrastructure.persistence.repositorios.cuentas_admin import RepositorioCuentasAdminSQLModel
from app.infrastructure.persistence.repositorios.cuentas_profesor import RepositorioCuentasProfesorSQLModel
from app.infrastructure.persistence.repositorios.curso_seccion import RepositorioCursosSeccionSQLModel
from app.infrastructure.persistence.repositorios.descuentos import RepositorioDescuentosSQLModel
from app.infrastructure.persistence.repositorios.intentos import RepositorioIntentosSQLModel
from app.infrastructure.persistence.repositorios.perfiles_alumno import RepositorioPerfilesAlumnoSQLModel
from app.infrastructure.persistence.repositorios.plan_estudio import RepositorioPlanEstudioSQLModel
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


def get_iniciar_prueba_gratis_uc(
    repositorio_suscripciones: RepositorioSuscripcionesSQLModel = Depends(get_repositorio_suscripciones),
    repositorio_perfiles: RepositorioPerfilesAlumnoSQLModel = Depends(get_repositorio_perfiles_alumno),
    repositorio_planes: RepositorioPlanesSQLModel = Depends(get_repositorio_planes),
    reloj: RelojSistema = Depends(get_reloj),
) -> IniciarPruebaGratis:
    return IniciarPruebaGratis(repositorio_suscripciones, repositorio_perfiles, repositorio_planes, reloj)


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


def get_generar_simulacro_parcial_uc(
    repositorio_conjuntos: RepositorioConjuntosSQLModel = Depends(get_repositorio_conjuntos),
    repositorio_preguntas: RepositorioPreguntasSQLModel = Depends(get_repositorio_preguntas),
    repositorio_contenido: RepositorioContenidoSQLModel = Depends(get_repositorio_contenido),
    repositorio_progreso: RepositorioProgresoSQLModel = Depends(get_repositorio_progreso),
) -> GenerarSimulacroParcial:
    return GenerarSimulacroParcial(repositorio_conjuntos, repositorio_preguntas, repositorio_contenido, repositorio_progreso)


def get_obtener_faltantes_uc(
    repositorio_conjuntos: RepositorioConjuntosSQLModel = Depends(get_repositorio_conjuntos),
    repositorio_intentos: RepositorioIntentosSQLModel = Depends(get_repositorio_intentos),
    repositorio_preguntas: RepositorioPreguntasSQLModel = Depends(get_repositorio_preguntas),
    repositorio_contenido: RepositorioContenidoSQLModel = Depends(get_repositorio_contenido),
    repositorio_progreso: RepositorioProgresoSQLModel = Depends(get_repositorio_progreso),
) -> ObtenerFaltantes:
    return ObtenerFaltantes(
        repositorio_conjuntos, repositorio_intentos, repositorio_preguntas, repositorio_contenido, repositorio_progreso
    )


def get_repositorio_plan_estudio(session: Session = Depends(get_session)) -> RepositorioPlanEstudioSQLModel:
    return RepositorioPlanEstudioSQLModel(session)


def get_crear_plan_de_estudio_uc(
    repositorio_plan_estudio: RepositorioPlanEstudioSQLModel = Depends(get_repositorio_plan_estudio),
    repositorio_perfiles: RepositorioPerfilesAlumnoSQLModel = Depends(get_repositorio_perfiles_alumno),
    repositorio_contenido: RepositorioContenidoSQLModel = Depends(get_repositorio_contenido),
    repositorio_progreso: RepositorioProgresoSQLModel = Depends(get_repositorio_progreso),
    reloj: RelojSistema = Depends(get_reloj),
) -> CrearPlanDeEstudio:
    return CrearPlanDeEstudio(
        repositorio_plan_estudio, repositorio_perfiles, repositorio_contenido, repositorio_progreso, reloj
    )


def get_obtener_plan_activo_uc(
    repositorio_plan_estudio: RepositorioPlanEstudioSQLModel = Depends(get_repositorio_plan_estudio),
    repositorio_progreso: RepositorioProgresoSQLModel = Depends(get_repositorio_progreso),
) -> ObtenerPlanActivo:
    return ObtenerPlanActivo(repositorio_plan_estudio, repositorio_progreso)


def get_repositorio_cuentas_profesor(session: Session = Depends(get_session)) -> RepositorioCuentasProfesorSQLModel:
    return RepositorioCuentasProfesorSQLModel(session)


def get_repositorio_cursos_seccion(session: Session = Depends(get_session)) -> RepositorioCursosSeccionSQLModel:
    return RepositorioCursosSeccionSQLModel(session)


def get_repositorio_comunicados(session: Session = Depends(get_session)) -> RepositorioComunicadosSQLModel:
    return RepositorioComunicadosSQLModel(session)


def get_registrar_profesor_uc(
    repositorio: RepositorioCuentasProfesorSQLModel = Depends(get_repositorio_cuentas_profesor),
    hasheador: HasheadorPasswordBcrypt = Depends(get_hasheador_password),
    servicio_token: ServicioTokenJWT = Depends(get_servicio_token),
) -> RegistrarProfesor:
    return RegistrarProfesor(repositorio, hasheador, servicio_token)


def get_iniciar_sesion_profesor_uc(
    repositorio: RepositorioCuentasProfesorSQLModel = Depends(get_repositorio_cuentas_profesor),
    hasheador: HasheadorPasswordBcrypt = Depends(get_hasheador_password),
    servicio_token: ServicioTokenJWT = Depends(get_servicio_token),
) -> IniciarSesionProfesor:
    return IniciarSesionProfesor(repositorio, hasheador, servicio_token)


def get_cuenta_profesor_actual(
    credenciales: HTTPAuthorizationCredentials = Depends(security),
    servicio_token: ServicioTokenJWT = Depends(get_servicio_token),
    repositorio: RepositorioCuentasProfesorSQLModel = Depends(get_repositorio_cuentas_profesor),
) -> CuentaProfesor:
    cuenta_profesor_id = servicio_token.decodificar_profesor(credenciales.credentials)
    if cuenta_profesor_id is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Sesión de profesor inválida o expirada")
    cuenta = repositorio.buscar_por_id(cuenta_profesor_id)
    if cuenta is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Cuenta de profesor no encontrada")
    return cuenta


def get_profesor_aprobado_actual(cuenta: CuentaProfesor = Depends(get_cuenta_profesor_actual)) -> CuentaProfesor:
    """Igual que `get_cuenta_profesor_actual`, pero además exige que la cuenta ya haya
    sido aprobada por un Administrador — usarla en los endpoints que crean/modifican
    Cursos/Secciones, no en el login/estado de la cuenta."""
    if not cuenta.esta_aprobado:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Tu cuenta de profesor todavía está en revisión")
    return cuenta


def get_listar_profesores_pendientes_uc(
    repositorio: RepositorioCuentasProfesorSQLModel = Depends(get_repositorio_cuentas_profesor),
) -> ListarProfesoresPendientes:
    return ListarProfesoresPendientes(repositorio)


def get_aprobar_profesor_uc(
    repositorio: RepositorioCuentasProfesorSQLModel = Depends(get_repositorio_cuentas_profesor),
) -> AprobarProfesor:
    return AprobarProfesor(repositorio)


def get_rechazar_profesor_uc(
    repositorio: RepositorioCuentasProfesorSQLModel = Depends(get_repositorio_cuentas_profesor),
) -> RechazarProfesor:
    return RechazarProfesor(repositorio)


def get_crear_curso_seccion_uc(
    repositorio: RepositorioCursosSeccionSQLModel = Depends(get_repositorio_cursos_seccion),
) -> CrearCursoSeccion:
    return CrearCursoSeccion(repositorio)


def get_agregar_alumno_a_curso_uc(
    repositorio_cursos: RepositorioCursosSeccionSQLModel = Depends(get_repositorio_cursos_seccion),
    repositorio_perfiles: RepositorioPerfilesAlumnoSQLModel = Depends(get_repositorio_perfiles_alumno),
) -> AgregarAlumnoACurso:
    return AgregarAlumnoACurso(repositorio_cursos, repositorio_perfiles)


def get_quitar_alumno_de_curso_uc(
    repositorio_cursos: RepositorioCursosSeccionSQLModel = Depends(get_repositorio_cursos_seccion),
) -> QuitarAlumnoDeCurso:
    return QuitarAlumnoDeCurso(repositorio_cursos)


def get_publicar_comunicado_uc(
    repositorio_cursos: RepositorioCursosSeccionSQLModel = Depends(get_repositorio_cursos_seccion),
    repositorio_comunicados: RepositorioComunicadosSQLModel = Depends(get_repositorio_comunicados),
    reloj: RelojSistema = Depends(get_reloj),
) -> PublicarComunicado:
    return PublicarComunicado(repositorio_cursos, repositorio_comunicados, reloj)


def get_obtener_progreso_de_curso_uc(
    repositorio_cursos: RepositorioCursosSeccionSQLModel = Depends(get_repositorio_cursos_seccion),
    obtener_historial_y_notas: ObtenerHistorialYNotas = Depends(get_obtener_historial_y_notas_uc),
) -> ObtenerProgresoDeCurso:
    return ObtenerProgresoDeCurso(repositorio_cursos, obtener_historial_y_notas)


def get_buscar_alumnos_para_profesor_uc(
    repositorio_perfiles: RepositorioPerfilesAlumnoSQLModel = Depends(get_repositorio_perfiles_alumno),
    repositorio_cuentas: RepositorioCuentasSQLModel = Depends(get_repositorio_cuentas),
) -> BuscarAlumnos:
    # Mismo caso de uso que usa el panel Admin para Cortesías — genérico, sin ninguna
    # dependencia de CuentaAdmin, así que reutilizarlo acá no acopla nada nuevo.
    return BuscarAlumnos(repositorio_perfiles, repositorio_cuentas)


def get_obtener_mi_curso_uc(
    repositorio_cursos: RepositorioCursosSeccionSQLModel = Depends(get_repositorio_cursos_seccion),
    repositorio_comunicados: RepositorioComunicadosSQLModel = Depends(get_repositorio_comunicados),
    repositorio_cuentas_profesor: RepositorioCuentasProfesorSQLModel = Depends(get_repositorio_cuentas_profesor),
) -> ObtenerMiCurso:
    return ObtenerMiCurso(repositorio_cursos, repositorio_comunicados, repositorio_cuentas_profesor)


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
