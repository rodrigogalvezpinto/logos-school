from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

from app.core.deps import get_repositorio_contenido
from app.domain.contenido.ports import RepositorioContenido

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
def listar_niveles(repositorio: RepositorioContenido = Depends(get_repositorio_contenido)):
    return repositorio.listar_niveles()


@router.get("/niveles/{nivel_id}/asignaturas", response_model=list[AsignaturaRespuesta])
def listar_asignaturas(nivel_id: int, repositorio: RepositorioContenido = Depends(get_repositorio_contenido)):
    return repositorio.listar_asignaturas(nivel_id)


@router.get("/asignaturas/{asignatura_id}/objetivos", response_model=list[ObjetivoRespuesta])
def listar_objetivos(asignatura_id: int, repositorio: RepositorioContenido = Depends(get_repositorio_contenido)):
    return repositorio.listar_objetivos(asignatura_id)


@router.get("/objetivos/{oa_id}", response_model=ObjetivoRespuesta)
def obtener_objetivo(oa_id: int, repositorio: RepositorioContenido = Depends(get_repositorio_contenido)):
    oa = repositorio.obtener_objetivo(oa_id)
    if not oa:
        raise HTTPException(status_code=404, detail="Objetivo de Aprendizaje no encontrado")
    return oa
