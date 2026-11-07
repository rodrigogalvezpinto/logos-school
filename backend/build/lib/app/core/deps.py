"""Composition root: aquí se cablean los adaptadores concretos de `infrastructure/` a
los puertos que consumen los casos de uso de `application/`, vía `Depends` de FastAPI.
Los routers nunca instancian un adaptador directo — siempre a través de estas factories."""

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlmodel import Session

from app.application.auth.casos_de_uso import (
    AgregarPerfilAlumno,
    CerrarSesion,
    EliminarAlumno,
    IniciarSesion,
    IniciarSesionConGoogle,
    ListarPerfilesAlumno,
    RegistrarApoderado,
)
from app.application.evaluaciones.casos_de_uso import (
    EntregarIntento,
    GenerarSimulacroParcial,
    IniciarIntento,
    ObtenerDetalleIntento,
    ObtenerIntento,
    ProgramarFechaSimulacro,
    ResponderPregunta,
)
from app.application.bienestar.casos_de_uso import ObtenerAnimoDeHoy, RegistrarAnimoDeHoy
from app.application.gamificacion.casos_de_uso import CambiarAvatar, ObtenerPerfilGamificacion, SumarXp
from app.application.onboarding.casos_de_uso import CompletarPasoOnboarding, ObtenerProgresoOnboarding
from app.application.plan_estudio.casos_de_uso import AgregarSesionDeRepaso, CrearPlanDeEstudio, ObtenerPlanActivo
from app.application.reportes.casos_de_uso import ListarReportesNoResueltos, ReportarErrorPregunta
from app.application.sugerencias.casos_de_uso import EnviarSugerencia, ListarMisSugerencias
from app.infrastructure.persistence.repositorios.sugerencias import RepositorioSugerenciasSQLModel
from app.application.calificaciones.casos_de_uso import CalificarGuia, ObtenerMiCalificacion
from app.infrastructure.persistence.repositorios.calificaciones import RepositorioCalificacionesSQLModel
from app.application.apoderado.casos_de_uso import MarcarAgendaFamiliarConversada
from app.application.apoderado.consultas import (
    ObtenerAgendaFamiliar,
    ObtenerEstadisticasFamiliares,
    ObtenerMetaFamiliar,
)
from app.infrastructure.persistence.repositorios.agenda_familiar import RepositorioAgendaFamiliarSQLModel
from app.application.prediccion.consultas import (
    EstimarNotaExamen,
    EvaluarRitmoDeEstudio,
    ObservarHorarioDeEstudio,
    ObtenerJardinSemanal,
    ObtenerMapaDeCalorPorEje,
)
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
from app.application.comercial.consultas import BuscarAlumnos, ObtenerMetricas, ObtenerSuscripcionDeAlumno
from app.application.curso_seccion.casos_de_uso import (
    AgregarAlumnoACurso,
    CrearCursoSeccion,
    PublicarComunicado,
    QuitarAlumnoDeCurso,
)
from app.application.curso_seccion.consultas import ObtenerMiCurso, ObtenerProgresoDeCurso
from app.application.notificaciones.consultas import ObtenerNotificaciones
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
from app.infrastructure.persistence.repositorios.plan_lector import RepositorioPlanLectorSQLModel
from app.infrastructure.persistence.repositorios.utiles_escolares import RepositorioUtilesEscolaresSQLModel
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
from app.infrastructure.persistence.repositorios.bienestar import RepositorioBienestarSQLModel
from app.infrastructure.persistence.repositorios.gamificacion import RepositorioGamificacionSQLModel
from app.infrastructure.persistence.repositorios.onboarding import RepositorioOnboardingSQLModel
from app.infrastructure.persistence.repositorios.progreso import RepositorioProgresoSQLModel
from app.infrastructure.persistence.repositorios.reportes import RepositorioReportesErrorSQLModel
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


def get_cerrar_sesion_uc(
    repositorio: RepositorioCuentasSQLModel = Depends(get_repositorio_cuentas),
) -> CerrarSesion:
    return CerrarSesion(repositorio)


def get_iniciar_sesion_google_uc(
    repositorio: RepositorioCuentasSQLModel = Depends(get_repositorio_cuentas),
    verificador_google: VerificadorTokenGoogleAdapter = Depends(get_verificador_google),
    servicio_token: ServicioTokenJWT = Depends(get_servicio_token),
) -> IniciarSesionConGoogle:
    return IniciarSesionConGoogle(repositorio, verificador_google, servicio_token)


def get_repositorio_contenido(session: Session = Depends(get_session)) -> RepositorioContenidoSQLModel:
    return RepositorioContenidoSQLModel(session)


def get_repositorio_plan_lector(session: Session = Depends(get_session)) -> RepositorioPlanLectorSQLModel:
    return RepositorioPlanLectorSQLModel(session)


def get_repositorio_utiles_escolares(session: Session = Depends(get_session)) -> RepositorioUtilesEscolaresSQLModel:
    return RepositorioUtilesEscolaresSQLModel(session)


def get_reloj() -> RelojSistema:
    return RelojSistema()


def get_agregar_perfil_alumno_uc(
    repositorio: RepositorioPerfilesAlumnoSQLModel = Depends(get_repositorio_perfiles_alumno),
    repositorio_contenido: RepositorioContenidoSQLModel = Depends(get_repositorio_contenido),
    reloj: RelojSistema = Depends(get_reloj),
) -> AgregarPerfilAlumno:
    return AgregarPerfilAlumno(repositorio, repositorio_contenido, reloj)


def get_listar_perfiles_alumno_uc(
    repositorio: RepositorioPerfilesAlumnoSQLModel = Depends(get_repositorio_perfiles_alumno),
) -> ListarPerfilesAlumno:
    return ListarPerfilesAlumno(repositorio)


def get_eliminar_alumno_uc(
    repositorio: RepositorioPerfilesAlumnoSQLModel = Depends(get_repositorio_perfiles_alumno),
) -> EliminarAlumno:
    return EliminarAlumno(repositorio)


def get_repositorio_intentos(session: Session = Depends(get_session)) -> RepositorioIntentosSQLModel:
    return RepositorioIntentosSQLModel(session)


def get_repositorio_conjuntos(session: Session = Depends(get_session)) -> RepositorioConjuntosSQLModel:
    return RepositorioConjuntosSQLModel(session)


def get_repositorio_preguntas(session: Session = Depends(get_session)) -> RepositorioPreguntasSQLModel:
    return RepositorioPreguntasSQLModel(session)


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


def get_obtener_detalle_intento_uc(
    repositorio_intentos: RepositorioIntentosSQLModel = Depends(get_repositorio_intentos),
    repositorio_conjuntos: RepositorioConjuntosSQLModel = Depends(get_repositorio_conjuntos),
    repositorio_preguntas: RepositorioPreguntasSQLModel = Depends(get_repositorio_preguntas),
) -> ObtenerDetalleIntento:
    return ObtenerDetalleIntento(repositorio_intentos, repositorio_conjuntos, repositorio_preguntas)


def get_repositorio_reportes_error(session: Session = Depends(get_session)) -> RepositorioReportesErrorSQLModel:
    return RepositorioReportesErrorSQLModel(session)


def get_reportar_error_pregunta_uc(
    repositorio_reportes: RepositorioReportesErrorSQLModel = Depends(get_repositorio_reportes_error),
    repositorio_preguntas: RepositorioPreguntasSQLModel = Depends(get_repositorio_preguntas),
    repositorio_perfiles: RepositorioPerfilesAlumnoSQLModel = Depends(get_repositorio_perfiles_alumno),
    reloj: RelojSistema = Depends(get_reloj),
) -> ReportarErrorPregunta:
    return ReportarErrorPregunta(repositorio_reportes, repositorio_preguntas, repositorio_perfiles, reloj)


def get_listar_reportes_no_resueltos_uc(
    repositorio_reportes: RepositorioReportesErrorSQLModel = Depends(get_repositorio_reportes_error),
) -> ListarReportesNoResueltos:
    return ListarReportesNoResueltos(repositorio_reportes)


def get_repositorio_sugerencias(session: Session = Depends(get_session)) -> RepositorioSugerenciasSQLModel:
    return RepositorioSugerenciasSQLModel(session)


def get_enviar_sugerencia_uc(
    repositorio_sugerencias: RepositorioSugerenciasSQLModel = Depends(get_repositorio_sugerencias),
    repositorio_perfiles: RepositorioPerfilesAlumnoSQLModel = Depends(get_repositorio_perfiles_alumno),
    reloj: RelojSistema = Depends(get_reloj),
) -> EnviarSugerencia:
    return EnviarSugerencia(repositorio_sugerencias, repositorio_perfiles, reloj)


def get_listar_mis_sugerencias_uc(
    repositorio_sugerencias: RepositorioSugerenciasSQLModel = Depends(get_repositorio_sugerencias),
) -> ListarMisSugerencias:
    return ListarMisSugerencias(repositorio_sugerencias)


def get_repositorio_calificaciones(session: Session = Depends(get_session)) -> RepositorioCalificacionesSQLModel:
    return RepositorioCalificacionesSQLModel(session)


def get_calificar_guia_uc(
    repositorio_calificaciones: RepositorioCalificacionesSQLModel = Depends(get_repositorio_calificaciones),
    repositorio_perfiles: RepositorioPerfilesAlumnoSQLModel = Depends(get_repositorio_perfiles_alumno),
    reloj: RelojSistema = Depends(get_reloj),
) -> CalificarGuia:
    return CalificarGuia(repositorio_calificaciones, repositorio_perfiles, reloj)


def get_obtener_mi_calificacion_uc(
    repositorio_calificaciones: RepositorioCalificacionesSQLModel = Depends(get_repositorio_calificaciones),
) -> ObtenerMiCalificacion:
    return ObtenerMiCalificacion(repositorio_calificaciones)


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
    resultado = servicio_token.decodificar_con_version(credenciales.credentials)
    if resultado is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Sesión inválida o expirada")
    cuenta_id, version_token = resultado
    cuenta = repositorio.buscar_por_id(cuenta_id)
    if cuenta is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Cuenta no encontrada")
    if version_token != cuenta.sesion_version:
        # El token es de una sesión ya cerrada (ver CerrarSesion) — aunque no haya
        # expirado, no sirve más como credencial.
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Sesión inválida o expirada")
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


def get_obtener_suscripcion_de_alumno_uc(
    repositorio_suscripciones: RepositorioSuscripcionesSQLModel = Depends(get_repositorio_suscripciones),
) -> ObtenerSuscripcionDeAlumno:
    return ObtenerSuscripcionDeAlumno(repositorio_suscripciones)


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
    reloj: RelojSistema = Depends(get_reloj),
) -> ObtenerFaltantes:
    return ObtenerFaltantes(
        repositorio_conjuntos, repositorio_intentos, repositorio_preguntas, repositorio_contenido,
        repositorio_progreso, reloj,
    )


def get_estimar_nota_examen_uc(
    obtener_historial_y_notas: ObtenerHistorialYNotas = Depends(get_obtener_historial_y_notas_uc),
    obtener_faltantes: ObtenerFaltantes = Depends(get_obtener_faltantes_uc),
) -> EstimarNotaExamen:
    return EstimarNotaExamen(obtener_historial_y_notas, obtener_faltantes)


def get_programar_fecha_simulacro_uc(
    repositorio_conjuntos: RepositorioConjuntosSQLModel = Depends(get_repositorio_conjuntos),
) -> ProgramarFechaSimulacro:
    return ProgramarFechaSimulacro(repositorio_conjuntos)


def get_repositorio_plan_estudio(session: Session = Depends(get_session)) -> RepositorioPlanEstudioSQLModel:
    return RepositorioPlanEstudioSQLModel(session)


def get_evaluar_ritmo_de_estudio_uc(
    repositorio_plan_estudio: RepositorioPlanEstudioSQLModel = Depends(get_repositorio_plan_estudio),
    repositorio_progreso: RepositorioProgresoSQLModel = Depends(get_repositorio_progreso),
) -> EvaluarRitmoDeEstudio:
    return EvaluarRitmoDeEstudio(repositorio_plan_estudio, repositorio_progreso)


def get_obtener_mapa_de_calor_uc(
    repositorio_intentos: RepositorioIntentosSQLModel = Depends(get_repositorio_intentos),
    repositorio_preguntas: RepositorioPreguntasSQLModel = Depends(get_repositorio_preguntas),
    repositorio_contenido: RepositorioContenidoSQLModel = Depends(get_repositorio_contenido),
) -> ObtenerMapaDeCalorPorEje:
    return ObtenerMapaDeCalorPorEje(repositorio_intentos, repositorio_preguntas, repositorio_contenido)


def get_observar_horario_de_estudio_uc(
    repositorio_intentos: RepositorioIntentosSQLModel = Depends(get_repositorio_intentos),
    repositorio_progreso: RepositorioProgresoSQLModel = Depends(get_repositorio_progreso),
) -> ObservarHorarioDeEstudio:
    return ObservarHorarioDeEstudio(repositorio_intentos, repositorio_progreso)


def get_obtener_jardin_semanal_uc(
    repositorio_intentos: RepositorioIntentosSQLModel = Depends(get_repositorio_intentos),
    repositorio_progreso: RepositorioProgresoSQLModel = Depends(get_repositorio_progreso),
) -> ObtenerJardinSemanal:
    return ObtenerJardinSemanal(repositorio_intentos, repositorio_progreso)


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


def get_agregar_sesion_de_repaso_uc(
    repositorio_plan_estudio: RepositorioPlanEstudioSQLModel = Depends(get_repositorio_plan_estudio),
    repositorio_perfiles: RepositorioPerfilesAlumnoSQLModel = Depends(get_repositorio_perfiles_alumno),
    repositorio_contenido: RepositorioContenidoSQLModel = Depends(get_repositorio_contenido),
) -> AgregarSesionDeRepaso:
    return AgregarSesionDeRepaso(repositorio_plan_estudio, repositorio_perfiles, repositorio_contenido)


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


def get_obtener_notificaciones_uc(
    obtener_mi_curso: ObtenerMiCurso = Depends(get_obtener_mi_curso_uc),
    obtener_plan_activo: ObtenerPlanActivo = Depends(get_obtener_plan_activo_uc),
    repositorio_reportes: RepositorioReportesErrorSQLModel = Depends(get_repositorio_reportes_error),
) -> ObtenerNotificaciones:
    return ObtenerNotificaciones(obtener_mi_curso, obtener_plan_activo, repositorio_reportes)


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


def get_repositorio_gamificacion(session: Session = Depends(get_session)) -> RepositorioGamificacionSQLModel:
    return RepositorioGamificacionSQLModel(session)


def get_obtener_perfil_gamificacion_uc(
    repositorio: RepositorioGamificacionSQLModel = Depends(get_repositorio_gamificacion),
) -> ObtenerPerfilGamificacion:
    return ObtenerPerfilGamificacion(repositorio)


def get_obtener_estadisticas_familiares_uc(
    repositorio_perfiles: RepositorioPerfilesAlumnoSQLModel = Depends(get_repositorio_perfiles_alumno),
    repositorio_gamificacion: RepositorioGamificacionSQLModel = Depends(get_repositorio_gamificacion),
    obtener_faltantes: ObtenerFaltantes = Depends(get_obtener_faltantes_uc),
    evaluar_ritmo: EvaluarRitmoDeEstudio = Depends(get_evaluar_ritmo_de_estudio_uc),
) -> ObtenerEstadisticasFamiliares:
    return ObtenerEstadisticasFamiliares(repositorio_perfiles, repositorio_gamificacion, obtener_faltantes, evaluar_ritmo)


def get_obtener_meta_familiar_uc(
    repositorio_perfiles: RepositorioPerfilesAlumnoSQLModel = Depends(get_repositorio_perfiles_alumno),
    repositorio_intentos: RepositorioIntentosSQLModel = Depends(get_repositorio_intentos),
    repositorio_progreso: RepositorioProgresoSQLModel = Depends(get_repositorio_progreso),
) -> ObtenerMetaFamiliar:
    return ObtenerMetaFamiliar(repositorio_perfiles, repositorio_intentos, repositorio_progreso)


def get_repositorio_agenda_familiar(session: Session = Depends(get_session)) -> RepositorioAgendaFamiliarSQLModel:
    return RepositorioAgendaFamiliarSQLModel(session)


def get_obtener_agenda_familiar_uc(
    obtener_mapa_calor: ObtenerMapaDeCalorPorEje = Depends(get_obtener_mapa_de_calor_uc),
    repositorio_gamificacion: RepositorioGamificacionSQLModel = Depends(get_repositorio_gamificacion),
    evaluar_ritmo: EvaluarRitmoDeEstudio = Depends(get_evaluar_ritmo_de_estudio_uc),
    repositorio_agenda: RepositorioAgendaFamiliarSQLModel = Depends(get_repositorio_agenda_familiar),
) -> ObtenerAgendaFamiliar:
    return ObtenerAgendaFamiliar(obtener_mapa_calor, repositorio_gamificacion, evaluar_ritmo, repositorio_agenda)


def get_marcar_agenda_familiar_conversada_uc(
    repositorio_agenda: RepositorioAgendaFamiliarSQLModel = Depends(get_repositorio_agenda_familiar),
) -> MarcarAgendaFamiliarConversada:
    return MarcarAgendaFamiliarConversada(repositorio_agenda)


def get_sumar_xp_uc(
    repositorio: RepositorioGamificacionSQLModel = Depends(get_repositorio_gamificacion),
    reloj: RelojSistema = Depends(get_reloj),
) -> SumarXp:
    return SumarXp(repositorio, reloj)


def get_cambiar_avatar_uc(
    repositorio: RepositorioGamificacionSQLModel = Depends(get_repositorio_gamificacion),
) -> CambiarAvatar:
    return CambiarAvatar(repositorio)


def get_repositorio_onboarding(session: Session = Depends(get_session)) -> RepositorioOnboardingSQLModel:
    return RepositorioOnboardingSQLModel(session)


def get_obtener_progreso_onboarding_uc(
    repositorio: RepositorioOnboardingSQLModel = Depends(get_repositorio_onboarding),
) -> ObtenerProgresoOnboarding:
    return ObtenerProgresoOnboarding(repositorio)


def get_completar_paso_onboarding_uc(
    repositorio: RepositorioOnboardingSQLModel = Depends(get_repositorio_onboarding),
) -> CompletarPasoOnboarding:
    return CompletarPasoOnboarding(repositorio)


def get_repositorio_bienestar(session: Session = Depends(get_session)) -> RepositorioBienestarSQLModel:
    return RepositorioBienestarSQLModel(session)


def get_obtener_animo_de_hoy_uc(
    repositorio: RepositorioBienestarSQLModel = Depends(get_repositorio_bienestar),
    reloj: RelojSistema = Depends(get_reloj),
) -> ObtenerAnimoDeHoy:
    return ObtenerAnimoDeHoy(repositorio, reloj)


def get_registrar_animo_de_hoy_uc(
    repositorio: RepositorioBienestarSQLModel = Depends(get_repositorio_bienestar),
    reloj: RelojSistema = Depends(get_reloj),
) -> RegistrarAnimoDeHoy:
    return RegistrarAnimoDeHoy(repositorio, reloj)
