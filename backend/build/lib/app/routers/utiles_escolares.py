"""Útiles Escolares por nivel — hallazgo comparando en vivo contra Brincus (ver
planificacion/25-analisis-competencia-brincus.md): lista simple de materiales a comprar por
curso, contenido estático de bajo costo de mantención. Solo lectura, sin datos personales —
mismo criterio de "público, sin sesión" que /plan-lector y /contenido/niveles."""

from fastapi import APIRouter, Depends
from pydantic import BaseModel

from app.core.deps import get_repositorio_utiles_escolares
from app.infrastructure.persistence.repositorios.utiles_escolares import RepositorioUtilesEscolaresSQLModel

router = APIRouter(prefix="/utiles-escolares", tags=["utiles-escolares"])


class UtilEscolarRespuesta(BaseModel):
    id: int
    nombre: str
    cantidad: str | None
    asignatura: str | None


@router.get("/nivel/{nivel_id}", response_model=list[UtilEscolarRespuesta])
def listar_utiles_escolares(
    nivel_id: int, repositorio: RepositorioUtilesEscolaresSQLModel = Depends(get_repositorio_utiles_escolares)
):
    return repositorio.listar_por_nivel(nivel_id)
