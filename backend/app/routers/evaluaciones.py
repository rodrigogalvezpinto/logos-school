"""Endpoints de evaluación: autoevaluación formativa (por OA) y el ciclo completo de
Pruebas de unidad / Exámenes simulacro (listar → iniciar intento → autoguardar
respuestas → entregar y calcular nota).

Ver planificacion/12-motor-de-evaluacion.md para la especificación completa del flujo,
y planificacion/20-seguridad-y-casos-borde.md para los casos borde que esto cubre
(autosave/reanudar, no perder progreso, cálculo de nota server-side).
"""

from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlmodel import Session, select

from app.core.db import get_session
from app.models import ConjuntoEvaluacion, IntentoEvaluacion, ObjetivoAprendizaje, PerfilAlumno, Pregunta
from app.services.calificacion import calcular_nota

router = APIRouter(prefix="/evaluaciones", tags=["evaluaciones"])

TIPOS_AUTOCORREGIBLES = {"alternativas", "verdadero_falso"}


class PreguntaAutoevaluacion(BaseModel):
    id: int
    tipo: str
    enunciado: str
    opciones: list[str] | None
    respuesta_correcta: str
    retroalimentacion: str


@router.get("/autoevaluacion/{oa_id}", response_model=list[PreguntaAutoevaluacion])
def obtener_autoevaluacion(oa_id: int, session: Session = Depends(get_session)):
    oa = session.get(ObjetivoAprendizaje, oa_id)
    if not oa:
        raise HTTPException(status_code=404, detail="Objetivo de Aprendizaje no encontrado")
    preguntas = session.exec(select(Pregunta).where(Pregunta.oa_id == oa_id)).all()
    return preguntas


class ConjuntoRespuesta(BaseModel):
    id: int
    tipo: str
    nombre: str
    forma: str | None
    tiempo_sugerido_min: int | None
    num_preguntas: int


@router.get("/conjuntos/asignatura/{asignatura_id}", response_model=list[ConjuntoRespuesta])
def listar_conjuntos_de_asignatura(asignatura_id: int, session: Session = Depends(get_session)):
    conjuntos = session.exec(
        select(ConjuntoEvaluacion).where(ConjuntoEvaluacion.asignatura_id == asignatura_id)
    ).all()
    return [
        ConjuntoRespuesta(
            id=c.id, tipo=c.tipo, nombre=c.nombre, forma=c.forma,
            tiempo_sugerido_min=c.tiempo_sugerido_min, num_preguntas=len(c.pregunta_ids),
        )
        for c in conjuntos
    ]


@router.get("/conjuntos/nivel/{nivel_id}", response_model=list[ConjuntoRespuesta])
def listar_conjuntos_integrados_de_nivel(nivel_id: int, session: Session = Depends(get_session)):
    """Exámenes integrados de Régimen A (1°-4° básico) — no pertenecen a una asignatura."""
    conjuntos = session.exec(
        select(ConjuntoEvaluacion).where(ConjuntoEvaluacion.nivel_id == nivel_id)
    ).all()
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
def obtener_conjunto(conjunto_id: int, session: Session = Depends(get_session)):
    conjunto = session.get(ConjuntoEvaluacion, conjunto_id)
    if not conjunto:
        raise HTTPException(status_code=404, detail="Prueba/examen no encontrado")
    preguntas = [session.get(Pregunta, pid) for pid in conjunto.pregunta_ids]
    return ConjuntoDetalle(
        id=conjunto.id,
        tipo=conjunto.tipo,
        nombre=conjunto.nombre,
        forma=conjunto.forma,
        tiempo_sugerido_min=conjunto.tiempo_sugerido_min,
        preguntas=[PreguntaSinRespuesta(id=p.id, tipo=p.tipo, enunciado=p.enunciado, opciones=p.opciones) for p in preguntas if p],
    )


class IniciarIntento(BaseModel):
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


@router.post("/intentos", response_model=IntentoRespuesta, status_code=201)
def iniciar_intento(datos: IniciarIntento, session: Session = Depends(get_session)):
    perfil = session.get(PerfilAlumno, datos.perfil_alumno_id)
    if not perfil:
        raise HTTPException(status_code=404, detail="Perfil de alumno no encontrado")
    conjunto = session.get(ConjuntoEvaluacion, datos.conjunto_evaluacion_id)
    if not conjunto:
        raise HTTPException(status_code=404, detail="Prueba/examen no encontrado")

    # Caso borde: si ya hay un intento sin terminar para este alumno+conjunto, se
    # reanuda en vez de crear uno nuevo (ver planificacion/20-seguridad-y-casos-borde.md,
    # "abandono y reingreso" y "misma evaluación en dos pestañas").
    existente = session.exec(
        select(IntentoEvaluacion).where(
            IntentoEvaluacion.perfil_alumno_id == datos.perfil_alumno_id,
            IntentoEvaluacion.conjunto_evaluacion_id == datos.conjunto_evaluacion_id,
            IntentoEvaluacion.fecha_termino.is_(None),
        )
    ).first()
    if existente:
        return existente

    intento = IntentoEvaluacion(
        perfil_alumno_id=datos.perfil_alumno_id,
        conjunto_evaluacion_id=datos.conjunto_evaluacion_id,
        respuestas={},
    )
    session.add(intento)
    session.commit()
    session.refresh(intento)
    return intento


@router.get("/intentos/{intento_id}", response_model=IntentoRespuesta)
def obtener_intento(intento_id: int, session: Session = Depends(get_session)):
    intento = session.get(IntentoEvaluacion, intento_id)
    if not intento:
        raise HTTPException(status_code=404, detail="Intento no encontrado")
    return intento


class ResponderPregunta(BaseModel):
    pregunta_id: int
    respuesta: str


@router.patch("/intentos/{intento_id}/responder", response_model=IntentoRespuesta)
def responder_pregunta(intento_id: int, datos: ResponderPregunta, session: Session = Depends(get_session)):
    intento = session.get(IntentoEvaluacion, intento_id)
    if not intento:
        raise HTTPException(status_code=404, detail="Intento no encontrado")
    if intento.fecha_termino is not None:
        raise HTTPException(status_code=400, detail="Este intento ya fue entregado")

    respuestas = dict(intento.respuestas)
    respuestas[str(datos.pregunta_id)] = datos.respuesta
    intento.respuestas = respuestas
    session.add(intento)
    session.commit()
    session.refresh(intento)
    return intento


@router.post("/intentos/{intento_id}/entregar", response_model=IntentoRespuesta)
def entregar_intento(intento_id: int, session: Session = Depends(get_session)):
    intento = session.get(IntentoEvaluacion, intento_id)
    if not intento:
        raise HTTPException(status_code=404, detail="Intento no encontrado")
    if intento.fecha_termino is not None:
        return intento  # ya entregado — idempotente, no recalcula ni sobreescribe

    conjunto = session.get(ConjuntoEvaluacion, intento.conjunto_evaluacion_id)
    preguntas = [session.get(Pregunta, pid) for pid in conjunto.pregunta_ids]
    preguntas_autocorregibles = [p for p in preguntas if p and p.tipo in TIPOS_AUTOCORREGIBLES]

    correctas = 0
    for p in preguntas_autocorregibles:
        respuesta_alumno = intento.respuestas.get(str(p.id), "").strip().lower()
        respuesta_correcta = p.respuesta_correcta.strip().lower()
        if respuesta_alumno and respuesta_alumno == respuesta_correcta:
            correctas += 1

    puntaje_total = len(preguntas_autocorregibles)
    nota = calcular_nota(correctas, puntaje_total) if puntaje_total > 0 else None

    intento.puntaje = correctas
    intento.nota = nota
    intento.fecha_termino = datetime.now(timezone.utc)
    # Postgres devuelve fecha_inicio sin tzinfo aunque se guardó en UTC (columna
    # TIMESTAMP sin zona) — se normalizan ambas fechas a "naive" antes de restar.
    inicio_naive = intento.fecha_inicio.replace(tzinfo=None)
    termino_naive = intento.fecha_termino.replace(tzinfo=None)
    intento.tiempo_usado_seg = int((termino_naive - inicio_naive).total_seconds())
    session.add(intento)
    session.commit()
    session.refresh(intento)
    return intento
