"""Plan Lector por nivel — hallazgo comparando en vivo contra Brincus (ver
planificacion/25-analisis-competencia-brincus.md): lista curada de libros con
título/autor/editorial, contenido de valor percibido alto y costo de mantención bajo, que
Logos no tenía pese a tener Lenguaje como asignatura central. Solo lectura, sin datos
personales — mismo criterio de "público, sin sesión" que /contenido/niveles."""

from fastapi import APIRouter, Depends
from pydantic import BaseModel

from app.core.deps import get_repositorio_plan_lector
from app.infrastructure.persistence.repositorios.plan_lector import RepositorioPlanLectorSQLModel

router = APIRouter(prefix="/plan-lector", tags=["plan-lector"])


class LibroRespuesta(BaseModel):
    id: int
    titulo: str
    autor: str
    editorial: str


@router.get("/nivel/{nivel_id}", response_model=list[LibroRespuesta])
def listar_plan_lector(
    nivel_id: int, repositorio: RepositorioPlanLectorSQLModel = Depends(get_repositorio_plan_lector)
):
    return repositorio.listar_por_nivel(nivel_id)
