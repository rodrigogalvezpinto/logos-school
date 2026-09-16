"""Endpoints de evaluación: autoevaluación formativa (por OA) y el ciclo completo de
Pruebas de unidad / Exámenes simulacro (listar → iniciar intento → autoguardar
respuestas → entregar y calcular nota).

Ver planificacion/12-motor-de-evaluacion.md para la especificación completa del flujo,
y planificacion/20-seguridad-y-casos-borde.md para los casos borde que esto cubre
(autosave/reanudar, no perder progreso, cálculo de nota server-side).

Los endpoints de solo lectura (autoevaluación, listar/obtener conjuntos) llaman al
repositorio directo — no hay invariantes que proteger, así que no se fuerza la ceremonia
de un caso de uso completo. Los que sí mutan el ciclo de un IntentoEvaluacion (iniciar,
responder, entregar) pasan por casos de uso que orquestan el agregado de dominio.
"""

from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, Request
from pydantic import BaseModel, Field

from app.application.evaluaciones.casos_de_uso import (
    EntregarIntento,
    GenerarSimulacroParcial,
    IniciarIntento,
    ObtenerDetalleIntento,
    ObtenerIntento,
    ResponderPregunta,
)
from app.application.gamificacion.casos_de_uso import SumarXp
from app.application.reportes.casos_de_uso import ReportarErrorPregunta
from app.core.config import settings
from app.core.limiter import limiter
from app.core.deps import (
    get_cuenta_actual,
    get_entregar_intento_uc,
    get_generar_simulacro_parcial_uc,
    get_iniciar_intento_uc,
    get_obtener_detalle_intento_uc,
    get_obtener_intento_uc,
    get_reportar_error_pregunta_uc,
    get_repositorio_conjuntos,
    get_repositorio_intentos,
    get_repositorio_perfiles_alumno,
    get_repositorio_preguntas,
    get_responder_pregunta_uc,
    get_sumar_xp_uc,
)
from app.domain.auth.entities import Cuenta
from app.domain.auth.ports import RepositorioPerfilesAlumno
from app.domain.evaluaciones.exceptions import (
    AsignaturaNoEncontrada,
    ConjuntoNoEncontrado,
    CoberturaInsuficiente,
    IntentoNoEncontrado,
    IntentoNoEntregado,
    IntentoYaEntregado,
    PerfilAlumnoNoEncontrado,
    PreguntaNoEncontrada,
    SinPreguntasDisponibles,
)
from app.domain.evaluaciones.ports import RepositorioConjuntos, RepositorioIntentos, RepositorioPreguntas
from app.domain.evaluaciones.value_objects import mezclar_orden_al_azar, mezclar_orden_estable

router = APIRouter(prefix="/evaluaciones", tags=["evaluaciones"])


def _verificar_perfil_propio(perfil_alumno_id: int, cuenta: Cuenta, repositorio: RepositorioPerfilesAlumno) -> None:
    """Bug de seguridad real encontrado con una matriz de permisos automática: todo este
    router no exigía sesión — cualquiera, sin login, podía iniciar/responder/entregar la
    evaluación de cualquier alumno con solo adivinar su id. Se exige sesión de Apoderado
    y que el perfil pertenezca a esa cuenta, igual que ya hace `verificar_perfil_propio`
    en progreso.py/plan_estudio.py (acá no se puede reusar tal cual porque el id viene del
    body, no de la ruta)."""
    perfil = repositorio.buscar_por_id(perfil_alumno_id)
    if perfil is None:
        raise HTTPException(status_code=404, detail="Perfil de alumno no encontrado")
    if perfil.cuenta_apoderado_id != cuenta.id:
        raise HTTPException(status_code=403, detail="Ese perfil no pertenece a tu cuenta")


def _verificar_intento_propio(
    intento_id: int, cuenta: Cuenta, repo_intentos: RepositorioIntentos, repo_perfiles: RepositorioPerfilesAlumno
) -> None:
    intento = repo_intentos.buscar_por_id(intento_id)
    if intento is None:
        raise HTTPException(status_code=404, detail="Intento no encontrado")
    _verificar_perfil_propio(intento.perfil_alumno_id, cuenta, repo_perfiles)


class PreguntaAutoevaluacion(BaseModel):
    id: int
    tipo: str
    enunciado: str
    opciones: list[str] | None
    respuesta_correcta: str
    retroalimentacion: str


@router.get("/autoevaluacion/{oa_id}", response_model=list[PreguntaAutoevaluacion])
def obtener_autoevaluacion(oa_id: int, repositorio: RepositorioPreguntas = Depends(get_repositorio_preguntas)):
    if not repositorio.existe_objetivo(oa_id):
        raise HTTPException(status_code=404, detail="Objetivo de Aprendizaje no encontrado")
    # Al azar en cada llamada: no hay un intento que retomar que proteger, y que la
    # práctica se sienta distinta cada vez es justamente el objetivo.
    return mezclar_orden_al_azar(repositorio.buscar_por_oa(oa_id))


class ConjuntoRespuesta(BaseModel):
    id: int
    tipo: str
    nombre: str
    forma: str | None
    tiempo_sugerido_min: int | None
    num_preguntas: int
    # Historial de intentos del alumno para este conjunto, visible directamente junto a
    # la prueba/examen en vez de obligarlo a ir a "Mis Notas" aparte (hallazgo comparando
    # en vivo contra Brincus, que muestra "Ver intentos" junto a cada cuestionario en el
    # propio temario) — solo se completa si se pasa `perfil_alumno_id`.
    intentos_entregados: int = 0
    ultima_nota: float | None = None


def _enriquecer_con_historial(
    conjuntos: list, perfil_alumno_id: int | None, repo_intentos: RepositorioIntentos
) -> list[ConjuntoRespuesta]:
    entregados_por_conjunto: dict[int, list] = {}
    if perfil_alumno_id is not None:
        for intento in repo_intentos.listar_entregados_por_perfil(perfil_alumno_id):
            entregados_por_conjunto.setdefault(intento.conjunto_evaluacion_id, []).append(intento)

    resultado = []
    for c in conjuntos:
        intentos = entregados_por_conjunto.get(c.id, [])
        ultimo = max(intentos, key=lambda i: i.fecha_termino) if intentos else None
        resultado.append(
            ConjuntoRespuesta(
                id=c.id, tipo=c.tipo, nombre=c.nombre, forma=c.forma,
                tiempo_sugerido_min=c.tiempo_sugerido_min, num_preguntas=len(c.pregunta_ids),
                intentos_entregados=len(intentos), ultima_nota=ultimo.nota if ultimo else None,
            )
        )
    return resultado


@router.get("/conjuntos/asignatura/{asignatura_id}", response_model=list[ConjuntoRespuesta])
def listar_conjuntos_de_asignatura(
    asignatura_id: int,
    perfil_alumno_id: int | None = None,
    cuenta: Cuenta = Depends(get_cuenta_actual),
    repositorio: RepositorioConjuntos = Depends(get_repositorio_conjuntos),
    repo_intentos: RepositorioIntentos = Depends(get_repositorio_intentos),
    repo_perfiles: RepositorioPerfilesAlumno = Depends(get_repositorio_perfiles_alumno),
):
    # `perfil_alumno_id` solo enriquece la respuesta con la nota/intentos del alumno — sin
    # verificar que sea suyo, cualquiera con sesión podría leer la nota de un perfil ajeno
    # con solo adivinar su id (mismo patrón de bug ya corregido en _verificar_perfil_propio).
    if perfil_alumno_id is not None:
        _verificar_perfil_propio(perfil_alumno_id, cuenta, repo_perfiles)
    conjuntos = repositorio.listar_por_asignatura(asignatura_id)
    return _enriquecer_con_historial(conjuntos, perfil_alumno_id, repo_intentos)


@router.get("/conjuntos/nivel/{nivel_id}", response_model=list[ConjuntoRespuesta])
def listar_conjuntos_integrados_de_nivel(
    nivel_id: int,
    perfil_alumno_id: int | None = None,
    cuenta: Cuenta = Depends(get_cuenta_actual),
    repositorio: RepositorioConjuntos = Depends(get_repositorio_conjuntos),
    repo_intentos: RepositorioIntentos = Depends(get_repositorio_intentos),
    repo_perfiles: RepositorioPerfilesAlumno = Depends(get_repositorio_perfiles_alumno),
):
    """Exámenes integrados de Régimen A (1°-4° básico) — no pertenecen a una asignatura."""
    if perfil_alumno_id is not None:
        _verificar_perfil_propio(perfil_alumno_id, cuenta, repo_perfiles)
    conjuntos = repositorio.listar_por_nivel(nivel_id)
    return _enriquecer_con_historial(conjuntos, perfil_alumno_id, repo_intentos)


class PreguntaSinRespuesta(BaseModel):
    id: int
    tipo: str
    enunciado: str
    opciones: list[str] | None


class ConjuntoDetalle(BaseModel):
    id: int
    tipo: str
    nombre: str
    forma: str | None
    tiempo_sugerido_min: int | None
    preguntas: list[PreguntaSinRespuesta]


@router.get("/conjuntos/{conjunto_id}", response_model=ConjuntoDetalle)
def obtener_conjunto(
    conjunto_id: int,
    perfil_alumno_id: int | None = None,
    repositorio_conjuntos: RepositorioConjuntos = Depends(get_repositorio_conjuntos),
    repositorio_preguntas: RepositorioPreguntas = Depends(get_repositorio_preguntas),
):
    conjunto = repositorio_conjuntos.buscar_por_id(conjunto_id)
    if not conjunto:
        raise HTTPException(status_code=404, detail="Prueba/examen no encontrado")
    preguntas = repositorio_preguntas.listar_por_ids(conjunto.pregunta_ids)
    if perfil_alumno_id is not None:
        # Semilla estable por (alumno, conjunto): el orden varía entre alumnos y entre
        # pruebas/exámenes distintos, pero no cambia si el mismo alumno recarga o retoma
        # el mismo intento — evita que "la pregunta 5" cambie de contenido a mitad de camino.
        preguntas = mezclar_orden_estable(preguntas, semilla=perfil_alumno_id * 1_000_003 + conjunto_id)
    return ConjuntoDetalle(
        id=conjunto.id,
        tipo=conjunto.tipo,
        nombre=conjunto.nombre,
        forma=conjunto.forma,
        tiempo_sugerido_min=conjunto.tiempo_sugerido_min,
        preguntas=[
            PreguntaSinRespuesta(id=p.id, tipo=p.tipo, enunciado=p.enunciado, opciones=p.opciones)
            for p in preguntas
        ],
    )


class IniciarIntentoRequest(BaseModel):
    perfil_alumno_id: int
    conjunto_evaluacion_id: int


class IntentoRespuesta(BaseModel):
    id: int
    conjunto_evaluacion_id: int
    fecha_inicio: datetime
    fecha_termino: datetime | None
    respuestas: dict[str, str]
    puntaje: float | None
    nota: float | None


def _a_respuesta(intento) -> IntentoRespuesta:
    return IntentoRespuesta(
        id=intento.id,
        conjunto_evaluacion_id=intento.conjunto_evaluacion_id,
        fecha_inicio=intento.fecha_inicio,
        fecha_termino=intento.fecha_termino,
        respuestas=intento.respuestas,
        puntaje=intento.puntaje,
        nota=intento.nota,
    )


@router.post("/intentos", response_model=IntentoRespuesta, status_code=201)
def iniciar_intento(
    datos: IniciarIntentoRequest,
    cuenta: Cuenta = Depends(get_cuenta_actual),
    uc: IniciarIntento = Depends(get_iniciar_intento_uc),
    repo_perfiles: RepositorioPerfilesAlumno = Depends(get_repositorio_perfiles_alumno),
):
    _verificar_perfil_propio(datos.perfil_alumno_id, cuenta, repo_perfiles)
    try:
        intento = uc.ejecutar(datos.perfil_alumno_id, datos.conjunto_evaluacion_id)
    except PerfilAlumnoNoEncontrado:
        raise HTTPException(status_code=404, detail="Perfil de alumno no encontrado")
    except ConjuntoNoEncontrado:
        raise HTTPException(status_code=404, detail="Prueba/examen no encontrado")
    return _a_respuesta(intento)


class SimulacroParcialRequest(BaseModel):
    perfil_alumno_id: int


@router.post("/simulacro-parcial/{asignatura_id}", response_model=IntentoRespuesta, status_code=201)
def generar_simulacro_parcial(
    asignatura_id: int,
    datos: SimulacroParcialRequest,
    cuenta: Cuenta = Depends(get_cuenta_actual),
    generar_uc: GenerarSimulacroParcial = Depends(get_generar_simulacro_parcial_uc),
    iniciar_uc: IniciarIntento = Depends(get_iniciar_intento_uc),
    repo_perfiles: RepositorioPerfilesAlumno = Depends(get_repositorio_perfiles_alumno),
):
    """Genera el conjunto dinámico y de inmediato inicia el intento — el frontend solo ve
    un IntentoRespuesta, igual que POST /evaluaciones/intentos, sin ninguna rama nueva."""
    _verificar_perfil_propio(datos.perfil_alumno_id, cuenta, repo_perfiles)
    try:
        conjunto = generar_uc.ejecutar(asignatura_id, datos.perfil_alumno_id)
    except AsignaturaNoEncontrada:
        raise HTTPException(status_code=404, detail="Asignatura no encontrada")
    except CoberturaInsuficiente:
        raise HTTPException(status_code=400, detail="Todavía no cubres suficiente temario para el simulacro parcial")
    except SinPreguntasDisponibles:
        raise HTTPException(status_code=400, detail="No hay preguntas disponibles para generar el simulacro parcial")

    intento = iniciar_uc.ejecutar(datos.perfil_alumno_id, conjunto.id)
    return _a_respuesta(intento)


@router.get("/intentos/{intento_id}", response_model=IntentoRespuesta)
def obtener_intento(
    intento_id: int,
    cuenta: Cuenta = Depends(get_cuenta_actual),
    uc: ObtenerIntento = Depends(get_obtener_intento_uc),
    repo_intentos: RepositorioIntentos = Depends(get_repositorio_intentos),
    repo_perfiles: RepositorioPerfilesAlumno = Depends(get_repositorio_perfiles_alumno),
):
    _verificar_intento_propio(intento_id, cuenta, repo_intentos, repo_perfiles)
    try:
        intento = uc.ejecutar(intento_id)
    except IntentoNoEncontrado:
        raise HTTPException(status_code=404, detail="Intento no encontrado")
    return _a_respuesta(intento)


class ResponderPreguntaRequest(BaseModel):
    pregunta_id: int
    # Sin límite hasta ahora — encontrado al auditar seguridad de los endpoints nuevos de
    # Fase 1 (ver planificacion/27-plan-incorporacion-hallazgos-brincus.md): un límite
    # generoso (una respuesta de desarrollo real nunca se acerca a esto) evita que un
    # request directo a la API (sin pasar por el frontend) guarde un blob de texto enorme.
    respuesta: str = Field(max_length=4000)


@router.patch("/intentos/{intento_id}/responder", response_model=IntentoRespuesta)
def responder_pregunta(
    intento_id: int,
    datos: ResponderPreguntaRequest,
    cuenta: Cuenta = Depends(get_cuenta_actual),
    uc: ResponderPregunta = Depends(get_responder_pregunta_uc),
    repo_intentos: RepositorioIntentos = Depends(get_repositorio_intentos),
    repo_perfiles: RepositorioPerfilesAlumno = Depends(get_repositorio_perfiles_alumno),
):
    _verificar_intento_propio(intento_id, cuenta, repo_intentos, repo_perfiles)
    try:
        intento = uc.ejecutar(intento_id, datos.pregunta_id, datos.respuesta)
    except IntentoNoEncontrado:
        raise HTTPException(status_code=404, detail="Intento no encontrado")
    except IntentoYaEntregado:
        raise HTTPException(status_code=400, detail="Este intento ya fue entregado")
    return _a_respuesta(intento)


XP_POR_ENTREGAR_INTENTO = 5


@router.post("/intentos/{intento_id}/entregar", response_model=IntentoRespuesta)
def entregar_intento(
    intento_id: int,
    cuenta: Cuenta = Depends(get_cuenta_actual),
    uc: EntregarIntento = Depends(get_entregar_intento_uc),
    repo_intentos: RepositorioIntentos = Depends(get_repositorio_intentos),
    repo_perfiles: RepositorioPerfilesAlumno = Depends(get_repositorio_perfiles_alumno),
    sumar_xp_uc: SumarXp = Depends(get_sumar_xp_uc),
):
    _verificar_intento_propio(intento_id, cuenta, repo_intentos, repo_perfiles)
    ya_estaba_entregado = repo_intentos.buscar_por_id(intento_id).esta_entregado
    try:
        intento = uc.ejecutar(intento_id)
    except IntentoNoEncontrado:
        raise HTTPException(status_code=404, detail="Intento no encontrado")
    # Gamificación (Fase 1, ítem 2.2): solo la primera entrega da XP — `EntregarIntento`
    # ya es idempotente, esto evita premiar XP de nuevo si se reintenta la llamada.
    if not ya_estaba_entregado and intento.esta_entregado:
        sumar_xp_uc.ejecutar(
            intento.perfil_alumno_id, XP_POR_ENTREGAR_INTENTO,
            tipo_actividad="evaluacion", tiempo_usado_seg=intento.tiempo_usado_seg,
        )
    return _a_respuesta(intento)


class DetallePreguntaRespuesta(BaseModel):
    pregunta_id: int
    enunciado: str
    tipo: str
    opciones: list[str] | None
    respuesta_alumno: str | None
    respuesta_correcta: str | None
    es_correcta: bool | None


@router.get("/intentos/{intento_id}/detalle", response_model=list[DetallePreguntaRespuesta])
def obtener_detalle_intento(
    intento_id: int,
    cuenta: Cuenta = Depends(get_cuenta_actual),
    uc: ObtenerDetalleIntento = Depends(get_obtener_detalle_intento_uc),
    repo_intentos: RepositorioIntentos = Depends(get_repositorio_intentos),
    repo_perfiles: RepositorioPerfilesAlumno = Depends(get_repositorio_perfiles_alumno),
):
    """Resumen final pregunta-por-pregunta (Fase 1, ítem 2.1 — ver
    planificacion/27-plan-incorporacion-hallazgos-brincus.md). Solo disponible tras
    entregar, para no filtrar la respuesta correcta de un intento en curso."""
    _verificar_intento_propio(intento_id, cuenta, repo_intentos, repo_perfiles)
    try:
        detalle = uc.ejecutar(intento_id)
    except IntentoNoEncontrado:
        raise HTTPException(status_code=404, detail="Intento no encontrado")
    except IntentoNoEntregado:
        raise HTTPException(status_code=400, detail="Este intento todavía no se ha entregado")
    return [
        DetallePreguntaRespuesta(
            pregunta_id=d.pregunta_id,
            enunciado=d.enunciado,
            tipo=d.tipo,
            opciones=d.opciones,
            respuesta_alumno=d.respuesta_alumno,
            respuesta_correcta=d.respuesta_correcta,
            es_correcta=d.es_correcta,
        )
        for d in detalle
    ]


class ReportarErrorRequest(BaseModel):
    perfil_alumno_id: int
    # Sin límite antes de esta auditoría — un reporte de error de verdad es una o dos
    # frases; 1000 caracteres deja margen de sobra sin permitir un blob de texto enorme
    # guardado sin ningún control por request.
    comentario: str = Field(default="", max_length=1000)


class ReporteErrorRespuesta(BaseModel):
    id: int
    tipo_contenido: str
    contenido_id: int
    fecha: datetime


@router.post("/preguntas/{pregunta_id}/reportar-error", response_model=ReporteErrorRespuesta, status_code=201)
@limiter.limit(f"{settings.limite_reportar_error_por_minuto}/minute")
def reportar_error_pregunta(
    request: Request,
    pregunta_id: int,
    datos: ReportarErrorRequest,
    cuenta: Cuenta = Depends(get_cuenta_actual),
    uc: ReportarErrorPregunta = Depends(get_reportar_error_pregunta_uc),
    repo_perfiles: RepositorioPerfilesAlumno = Depends(get_repositorio_perfiles_alumno),
):
    """Fase 1, ítems 2.1 y 2.6 (ver planificacion/27-plan-incorporacion-hallazgos-brincus.md)
    — reportar una pregunta con contenido incorrecto, disponible desde cualquier momento
    de un intento (no solo al terminarlo), inspirado en el "Notificar error" verificado en
    Brincus por pregunta individual."""
    _verificar_perfil_propio(datos.perfil_alumno_id, cuenta, repo_perfiles)
    try:
        reporte = uc.ejecutar(pregunta_id, datos.perfil_alumno_id, datos.comentario)
    except PerfilAlumnoNoEncontrado:
        raise HTTPException(status_code=404, detail="Perfil de alumno no encontrado")
    except PreguntaNoEncontrada:
        raise HTTPException(status_code=404, detail="Pregunta no encontrada")
    return ReporteErrorRespuesta(
        id=reporte.id, tipo_contenido=reporte.tipo_contenido, contenido_id=reporte.contenido_id, fecha=reporte.fecha
    )
