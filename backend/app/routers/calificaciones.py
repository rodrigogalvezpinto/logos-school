"""Calificación con estrellas por guía (Fase 1 — ver
planificacion/27-plan-incorporacion-hallazgos-brincus.md, cuarta pasada). Protegido con
`verificar_perfil_propio`, mismo patrón que el resto de rutas por perfil de alumno."""

from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field

from app.application.calificaciones.casos_de_uso import CalificarGuia, ObtenerMiCalificacion
from app.core.deps import get_calificar_guia_uc, get_obtener_mi_calificacion_uc, verificar_perfil_propio
from app.domain.calificaciones.exceptions import EstrellasInvalidas
from app.domain.evaluaciones.exceptions import PerfilAlumnoNoEncontrado

router = APIRouter(prefix="/calificaciones", tags=["calificaciones"])


class CalificarGuiaRequest(BaseModel):
    estrellas: int = Field(ge=1, le=5)


class CalificacionRespuesta(BaseModel):
    oa_id: int
    estrellas: int
    fecha: datetime


@router.put("/{perfil_alumno_id}/guias/{oa_id}", response_model=CalificacionRespuesta)
def calificar_guia(
    oa_id: int,
    datos: CalificarGuiaRequest,
    perfil_alumno_id: int = Depends(verificar_perfil_propio),
    uc: CalificarGuia = Depends(get_calificar_guia_uc),
):
    try:
        calificacion = uc.ejecutar(oa_id, perfil_alumno_id, datos.estrellas)
    except PerfilAlumnoNoEncontrado:
        raise HTTPException(status_code=404, detail="Perfil de alumno no encontrado")
    except EstrellasInvalidas:
        raise HTTPException(status_code=422, detail="Las estrellas deben estar entre 1 y 5")
    return calificacion


@router.get("/{perfil_alumno_id}/guias/{oa_id}", response_model=CalificacionRespuesta | None)
def obtener_mi_calificacion(
    oa_id: int,
    perfil_alumno_id: int = Depends(verificar_perfil_propio),
    uc: ObtenerMiCalificacion = Depends(get_obtener_mi_calificacion_uc),
):
    return uc.ejecutar(oa_id, perfil_alumno_id)
