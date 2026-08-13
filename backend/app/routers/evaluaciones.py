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
    get_entregar_intento_uc,
    get_generar_simulacro_parcial_uc,
    get_iniciar_intento_uc,
    get_obtener_intento_uc,
    get_repositorio_conjuntos,
    get_repositorio_preguntas,
    get_responder_pregunta_uc,
)
from app.domain.evaluaciones.exceptions import (
    AsignaturaNoEncontrada,
    ConjuntoNoEncontrado,
    CoberturaInsuficiente,
    IntentoNoEncontrado,
    IntentoYaEntregado,
    PerfilAlumnoNoEncontrado,
    SinPreguntasDisponibles,
)
from app.domain.evaluaciones.ports import RepositorioConjuntos, RepositorioPreguntas

router = APIRouter(prefix="/evaluaciones", tags=["evaluaciones"])


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
    return repositorio.buscar_por_oa(oa_id)


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
    repositorio_conjuntos: RepositorioConjuntos = Depends(get_repositorio_conjuntos),
    repositorio_preguntas: RepositorioPreguntas = Depends(get_repositorio_preguntas),
):
    conjunto = repositorio_conjuntos.buscar_por_id(conjunto_id)
    if not conjunto:
        raise HTTPException(status_code=404, detail="Prueba/examen no encontrado")
    preguntas = repositorio_preguntas.listar_por_ids(conjunto.pregunta_ids)
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
def iniciar_intento(datos: IniciarIntentoRequest, uc: IniciarIntento = Depends(get_iniciar_intento_uc)):
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
    generar_uc: GenerarSimulacroParcial = Depends(get_generar_simulacro_parcial_uc),
    iniciar_uc: IniciarIntento = Depends(get_iniciar_intento_uc),
):
    """Genera el conjunto dinámico y de inmediato inicia el intento — el frontend solo ve
    un IntentoRespuesta, igual que POST /evaluaciones/intentos, sin ninguna rama nueva."""
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
def obtener_intento(intento_id: int, uc: ObtenerIntento = Depends(get_obtener_intento_uc)):
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
    intento_id: int, datos: ResponderPreguntaRequest, uc: ResponderPregunta = Depends(get_responder_pregunta_uc)
):
    try:
        intento = uc.ejecutar(intento_id, datos.pregunta_id, datos.respuesta)
    except IntentoNoEncontrado:
        raise HTTPException(status_code=404, detail="Intento no encontrado")
    except IntentoYaEntregado:
        raise HTTPException(status_code=400, detail="Este intento ya fue entregado")
    return _a_respuesta(intento)


@router.post("/intentos/{intento_id}/entregar", response_model=IntentoRespuesta)
def entregar_intento(intento_id: int, uc: EntregarIntento = Depends(get_entregar_intento_uc)):
    try:
        intento = uc.ejecutar(intento_id)
    except IntentoNoEncontrado:
        raise HTTPException(status_code=404, detail="Intento no encontrado")
    return _a_respuesta(intento)
