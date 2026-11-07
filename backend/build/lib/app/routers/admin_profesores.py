"""Aprobación de cuentas de Profesor desde el panel Admin — ver
planificacion/01-roles-y-permisos.md. Protegido por `get_cuenta_admin_actual` ya existente,
igual que Planes/Descuentos/Cortesías/Métricas de comercial.py."""

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

from app.application.admin.casos_de_uso_profesores import AprobarProfesor, ListarProfesoresPendientes, RechazarProfesor
from app.core.deps import (
    get_aprobar_profesor_uc,
    get_cuenta_admin_actual,
    get_listar_profesores_pendientes_uc,
    get_rechazar_profesor_uc,
)
from app.domain.profesor.exceptions import CuentaProfesorNoEncontrada

router = APIRouter(prefix="/admin/profesores", tags=["admin-profesores"], dependencies=[Depends(get_cuenta_admin_actual)])


class CuentaProfesorRespuesta(BaseModel):
    id: int
    email: str
    nombre: str
    estado: str


def _a_respuesta(cuenta) -> CuentaProfesorRespuesta:
    return CuentaProfesorRespuesta(id=cuenta.id, email=cuenta.email, nombre=cuenta.nombre, estado=cuenta.estado)


@router.get("/pendientes", response_model=list[CuentaProfesorRespuesta])
def listar_pendientes(uc: ListarProfesoresPendientes = Depends(get_listar_profesores_pendientes_uc)):
    return [_a_respuesta(c) for c in uc.ejecutar()]


@router.post("/{cuenta_profesor_id}/aprobar", response_model=CuentaProfesorRespuesta)
def aprobar(cuenta_profesor_id: int, uc: AprobarProfesor = Depends(get_aprobar_profesor_uc)):
    try:
        cuenta = uc.ejecutar(cuenta_profesor_id)
    except CuentaProfesorNoEncontrada:
        raise HTTPException(status_code=404, detail="Cuenta de profesor no encontrada")
    return _a_respuesta(cuenta)


@router.post("/{cuenta_profesor_id}/rechazar", response_model=CuentaProfesorRespuesta)
def rechazar(cuenta_profesor_id: int, uc: RechazarProfesor = Depends(get_rechazar_profesor_uc)):
    try:
        cuenta = uc.ejecutar(cuenta_profesor_id)
    except CuentaProfesorNoEncontrada:
        raise HTTPException(status_code=404, detail="Cuenta de profesor no encontrada")
    return _a_respuesta(cuenta)
