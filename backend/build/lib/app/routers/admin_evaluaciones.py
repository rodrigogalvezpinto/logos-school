"""Simulacro con fecha programada por el Admin — Fase 1, ítem 2.1 del plan de
incorporación de hallazgos de Brincus (ver
planificacion/27-plan-incorporacion-hallazgos-brincus.md). Protegido por
`get_cuenta_admin_actual` ya existente, igual que Planes/Descuentos/Profesores."""

from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

from app.application.evaluaciones.casos_de_uso import ProgramarFechaSimulacro
from app.core.deps import get_cuenta_admin_actual, get_programar_fecha_simulacro_uc
from app.domain.evaluaciones.exceptions import ConjuntoNoEncontrado

router = APIRouter(prefix="/admin/evaluaciones", tags=["admin-evaluaciones"], dependencies=[Depends(get_cuenta_admin_actual)])


class ProgramarFechaRequest(BaseModel):
    fecha_programada: datetime | None
    """`null` quita la fecha programada (vuelve a disponibilidad normal por cobertura)."""


class ConjuntoProgramadoRespuesta(BaseModel):
    id: int
    nombre: str
    tipo: str
    fecha_programada: datetime | None


@router.patch("/conjuntos/{conjunto_id}/programar-fecha", response_model=ConjuntoProgramadoRespuesta)
def programar_fecha(
    conjunto_id: int,
    datos: ProgramarFechaRequest,
    uc: ProgramarFechaSimulacro = Depends(get_programar_fecha_simulacro_uc),
):
    try:
        conjunto = uc.ejecutar(conjunto_id, datos.fecha_programada)
    except ConjuntoNoEncontrado:
        raise HTTPException(status_code=404, detail="Prueba/examen no encontrado")
    return ConjuntoProgramadoRespuesta(
        id=conjunto.id, nombre=conjunto.nombre, tipo=conjunto.tipo, fecha_programada=conjunto.fecha_programada
    )
