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

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

from app.application.evaluaciones.casos_de_uso import (
    EntregarIntento,
    GenerarSimulacroParcial,
    IniciarIntento,
    ObtenerIntento,
    ResponderPregunta,
)
from app.core.deps import (
    get_cuenta_actual,
    get_entregar_intento_uc,
    get_generar_simulacro_parcial_uc,
    get_iniciar_intento_uc,
    get_obtener_intento_uc,
    get_repositorio_conjuntos,
    get_repositorio_intentos,
    get_repositorio_perfiles_alumno,
    get_repositorio_preguntas,
    get_responder_pregunta_uc,
)
from app.domain.auth.entities import Cuenta
from app.domain.auth.ports import RepositorioPerfilesAlumno
from app.domain.evaluaciones.exceptions import (
    AsignaturaNoEncontrada,
    ConjuntoNoEncontrado,
    CoberturaInsuficiente,
    IntentoNoEncontrado,
    IntentoYaEntregado,
    PerfilAlumnoNoEncontrado,
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


@router.get("/conjuntos/asignatura/{asignatura_id}", response_model=list[ConjuntoRespuesta])
def listar_conjuntos_de_asignatura(
    asignatura_id: int, repositorio: RepositorioConjuntos = Depends(get_repositorio_conjuntos)
):
    conjuntos = repositorio.listar_por_asignatura(asignatura_id)
    return [
        ConjuntoRespuesta(
            id=c.id, tipo=c.tipo, nombre=c.nombre, forma=c.forma,
            tiempo_sugerido_min=c.tiempo_sugerido_min, num_preguntas=len(c.pregunta_ids),
        )
        for c in conjuntos
    ]


@router.get("/conjuntos/nivel/{nivel_id}", response_model=list[ConjuntoRespuesta])
def listar_conjuntos_integrados_de_nivel(
    nivel_id: int, repositorio: RepositorioConjuntos = Depends(get_repositorio_conjuntos)
):
    """Exámenes integrados de Régimen A (1°-4° básico) — no pertenecen a una asignatura."""
    conjuntos = repositorio.listar_por_nivel(nivel_id)
    return [
        ConjuntoRespuesta(
            id=c.id, tipo=c.tipo, nombre=c.nombre, forma=c.forma,
            tiempo_sugerido_min=c.tiempo_sugerido_min, num_preguntas=len(c.pregunta_ids),
        )
        for c in conjuntos
    ]


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
    respuesta: str


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


@router.post("/intentos/{intento_id}/entregar", response_model=IntentoRespuesta)
def entregar_intento(
    intento_id: int,
    cuenta: Cuenta = Depends(get_cuenta_actual),
    uc: EntregarIntento = Depends(get_entregar_intento_uc),
    repo_intentos: RepositorioIntentos = Depends(get_repositorio_intentos),
    repo_perfiles: RepositorioPerfilesAlumno = Depends(get_repositorio_perfiles_alumno),
):
    _verificar_intento_propio(intento_id, cuenta, repo_intentos, repo_perfiles)
    try:
        intento = uc.ejecutar(intento_id)
    except IntentoNoEncontrado:
        raise HTTPException(status_code=404, detail="Intento no encontrado")
    return _a_respuesta(intento)
