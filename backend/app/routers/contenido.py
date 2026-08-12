from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlmodel import Session, select

from app.core.db import get_session
from app.models import Asignatura, Nivel, ObjetivoAprendizaje

router = APIRouter(prefix="/contenido", tags=["contenido"])


class NivelRespuesta(BaseModel):
    id: int
    nombre: str
    regimen: str
    num_preguntas_examen: int
    duracion_examen_min: int


class AsignaturaRespuesta(BaseModel):
    id: int
    nombre: str


class ObjetivoRespuesta(BaseModel):
    id: int
    codigo_oficial: str
    descripcion: str
    eje_tematico: str | None
    contenido_guia: str


@router.get("/niveles", response_model=list[NivelRespuesta])
def listar_niveles(session: Session = Depends(get_session)):
    niveles = session.exec(select(Nivel)).all()
    return niveles


@router.get("/niveles/{nivel_id}/asignaturas", response_model=list[AsignaturaRespuesta])
def listar_asignaturas(nivel_id: int, session: Session = Depends(get_session)):
    return session.exec(select(Asignatura).where(Asignatura.nivel_id == nivel_id)).all()


@router.get("/asignaturas/{asignatura_id}/objetivos", response_model=list[ObjetivoRespuesta])
def listar_objetivos(asignatura_id: int, session: Session = Depends(get_session)):
    return session.exec(
        select(ObjetivoAprendizaje).where(ObjetivoAprendizaje.asignatura_id == asignatura_id)
    ).all()


@router.get("/objetivos/{oa_id}", response_model=ObjetivoRespuesta)
def obtener_objetivo(oa_id: int, session: Session = Depends(get_session)):
    oa = session.get(ObjetivoAprendizaje, oa_id)
    if not oa:
        raise HTTPException(status_code=404, detail="Objetivo de Aprendizaje no encontrado")
    return oa
