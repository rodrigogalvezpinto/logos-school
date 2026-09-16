"""Buzón de sugerencias (Fase 1 — ver planificacion/27-plan-incorporacion-hallazgos-brincus.md,
Paso 13). Protegido con `verificar_perfil_propio`, mismo patrón que el resto de rutas por
perfil de alumno."""

from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, Request
from pydantic import BaseModel, Field

from app.application.sugerencias.casos_de_uso import EnviarSugerencia, ListarMisSugerencias
from app.core.config import settings
from app.core.deps import get_enviar_sugerencia_uc, get_listar_mis_sugerencias_uc, verificar_perfil_propio
from app.core.limiter import limiter
from app.domain.evaluaciones.exceptions import PerfilAlumnoNoEncontrado
from app.domain.sugerencias.exceptions import SugerenciaVacia

router = APIRouter(prefix="/sugerencias", tags=["sugerencias"])


class EnviarSugerenciaRequest(BaseModel):
    texto: str = Field(min_length=1, max_length=2000)


class SugerenciaRespuesta(BaseModel):
    id: int
    texto: str
    fecha: datetime


@router.post("/{perfil_alumno_id}", response_model=SugerenciaRespuesta, status_code=201)
@limiter.limit(f"{settings.limite_sugerencia_por_minuto}/minute")
def enviar_sugerencia(
    request: Request,
    datos: EnviarSugerenciaRequest,
    perfil_alumno_id: int = Depends(verificar_perfil_propio),
    uc: EnviarSugerencia = Depends(get_enviar_sugerencia_uc),
):
    try:
        sugerencia = uc.ejecutar(perfil_alumno_id, datos.texto)
    except PerfilAlumnoNoEncontrado:
        raise HTTPException(status_code=404, detail="Perfil de alumno no encontrado")
    except SugerenciaVacia:
        raise HTTPException(status_code=422, detail="La sugerencia no puede estar vacía")
    return sugerencia


@router.get("/{perfil_alumno_id}", response_model=list[SugerenciaRespuesta])
def listar_mis_sugerencias(
    perfil_alumno_id: int = Depends(verificar_perfil_propio),
    uc: ListarMisSugerencias = Depends(get_listar_mis_sugerencias_uc),
):
    return uc.ejecutar(perfil_alumno_id)
