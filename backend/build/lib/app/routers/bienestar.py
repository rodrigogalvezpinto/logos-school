"""Check-in emocional diario (Fase 1, ítem 2.4 — ver
planificacion/27-plan-incorporacion-hallazgos-brincus.md). Sin visibilidad para el
Apoderado todavía — es un dato solo para el propio alumno por ahora."""

from datetime import date

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

from app.application.bienestar.casos_de_uso import ObtenerAnimoDeHoy, RegistrarAnimoDeHoy
from app.core.deps import get_obtener_animo_de_hoy_uc, get_registrar_animo_de_hoy_uc, verificar_perfil_propio
from app.domain.bienestar.entities import ESTADOS_ANIMO
from app.domain.bienestar.exceptions import EstadoAnimoInvalido

router = APIRouter(prefix="/bienestar", tags=["bienestar"])


class AnimoDeHoyRespuesta(BaseModel):
    registrado: bool
    estado: str | None
    fecha: date | None
    estados_disponibles: list[str]


def _a_respuesta(registro) -> AnimoDeHoyRespuesta:
    return AnimoDeHoyRespuesta(
        registrado=registro is not None,
        estado=registro.estado if registro else None,
        fecha=registro.fecha if registro else None,
        estados_disponibles=ESTADOS_ANIMO,
    )


@router.get("/{perfil_alumno_id}/hoy", response_model=AnimoDeHoyRespuesta)
def obtener_animo_de_hoy(
    perfil_alumno_id: int = Depends(verificar_perfil_propio),
    uc: ObtenerAnimoDeHoy = Depends(get_obtener_animo_de_hoy_uc),
):
    return _a_respuesta(uc.ejecutar(perfil_alumno_id))


class RegistrarAnimoRequest(BaseModel):
    estado: str


@router.post("/{perfil_alumno_id}/hoy", response_model=AnimoDeHoyRespuesta)
def registrar_animo_de_hoy(
    datos: RegistrarAnimoRequest,
    perfil_alumno_id: int = Depends(verificar_perfil_propio),
    uc: RegistrarAnimoDeHoy = Depends(get_registrar_animo_de_hoy_uc),
):
    try:
        registro = uc.ejecutar(perfil_alumno_id, datos.estado)
    except EstadoAnimoInvalido:
        raise HTTPException(status_code=400, detail="Estado de ánimo no reconocido")
    return _a_respuesta(registro)
