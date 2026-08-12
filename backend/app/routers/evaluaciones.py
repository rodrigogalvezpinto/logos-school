"""Endpoints de evaluación.

Estado actual: solo autoevaluación por OA (la única fuente de contenido ya importada
a la base — ver scripts/importar_contenido.py). Las Pruebas de unidad y Exámenes
simulacro (contenido/{curso}/pruebas/ y /examenes/) todavía no se han importado como
`ConjuntoEvaluacion` — es el siguiente incremento de contenido, no de lógica: el motor
de `IntentoEvaluacion` y el cálculo de nota (app/services/calificacion.py, ya con
tests) están listos para conectarse en cuanto ese import exista.
"""

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlmodel import Session, select

from app.core.db import get_session
from app.models import ObjetivoAprendizaje, Pregunta

router = APIRouter(prefix="/evaluaciones", tags=["evaluaciones"])


class PreguntaAutoevaluacion(BaseModel):
    id: int
    tipo: str
    enunciado: str
    opciones: list[str] | None
    respuesta_correcta: str
    retroalimentacion: str


@router.get("/autoevaluacion/{oa_id}", response_model=list[PreguntaAutoevaluacion])
def obtener_autoevaluacion(oa_id: int, session: Session = Depends(get_session)):
    """Devuelve el banco de preguntas de un OA CON la respuesta y retroalimentación
    incluidas — correcto solo para autoevaluación formativa (feedback inmediato, sin
    nota), nunca para pruebas/exámenes (ver planificacion/12-motor-de-evaluacion.md).
    """
    oa = session.get(ObjetivoAprendizaje, oa_id)
    if not oa:
        raise HTTPException(status_code=404, detail="Objetivo de Aprendizaje no encontrado")
    preguntas = session.exec(select(Pregunta).where(Pregunta.oa_id == oa_id)).all()
    return preguntas
