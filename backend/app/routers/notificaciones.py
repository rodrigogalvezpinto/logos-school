"""Centro de notificaciones (Fase 1, ver planificacion/27-plan-incorporacion-hallazgos-brincus.md
— hallazgo comparando en vivo contra Brincus, Paso 12: campana con Notificaciones /
Preguntas y Respuestas / Errores reportados). Solo la parte de "Notificaciones" y "Errores
reportados" — "Preguntas y Respuestas" requiere chat/IA, fuera de alcance por ahora."""

from datetime import datetime

from fastapi import APIRouter, Depends
from pydantic import BaseModel

from app.application.notificaciones.consultas import ObtenerNotificaciones
from app.core.deps import get_obtener_notificaciones_uc, get_reloj, verificar_perfil_propio
from app.domain.shared.reloj import Reloj

router = APIRouter(prefix="/notificaciones", tags=["notificaciones"])


class NotificacionRespuesta(BaseModel):
    tipo: str
    titulo: str
    detalle: str
    fecha: datetime


@router.get("/{perfil_alumno_id}", response_model=list[NotificacionRespuesta])
def listar_notificaciones(
    perfil_alumno_id: int = Depends(verificar_perfil_propio),
    uc: ObtenerNotificaciones = Depends(get_obtener_notificaciones_uc),
    reloj: Reloj = Depends(get_reloj),
):
    return uc.ejecutar(perfil_alumno_id, reloj.ahora().date())
