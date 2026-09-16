"""Gamificación (Fase 1, ítem 2.2 — ver
planificacion/27-plan-incorporacion-hallazgos-brincus.md): XP, nivel derivado y selección
de avatar. El XP en sí se otorga desde otros routers (evaluaciones.py al entregar un
intento, progreso.py al revisar una guía por primera vez) — este router solo expone
consultar el perfil y cambiar de avatar."""

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

from app.application.gamificacion.casos_de_uso import CambiarAvatar, ObtenerPerfilGamificacion
from app.core.deps import get_cambiar_avatar_uc, get_obtener_perfil_gamificacion_uc, verificar_perfil_propio
from app.domain.gamificacion.entities import AVATARES_DISPONIBLES, CATALOGO_LOGROS, xp_acumulado_para_nivel
from app.domain.gamificacion.exceptions import AvatarInvalido

router = APIRouter(prefix="/gamificacion", tags=["gamificacion"])


class LogroRespuesta(BaseModel):
    id: str
    nombre: str
    descripcion: str
    icono: str
    categoria: str
    desbloqueado: bool


class PerfilGamificacionRespuesta(BaseModel):
    perfil_alumno_id: int
    xp: int
    nivel: int
    avatar_id: str
    xp_para_siguiente_nivel: int
    avatares_disponibles: list[str]
    racha_dias_actual: int
    racha_dias_maxima: int
    guias_revisadas_total: int
    evaluaciones_entregadas_total: int
    tiempo_evaluando_total_seg: int
    logros: list[LogroRespuesta]


def _a_respuesta(perfil) -> PerfilGamificacionRespuesta:
    desbloqueados = perfil.logros_desbloqueados()
    return PerfilGamificacionRespuesta(
        perfil_alumno_id=perfil.perfil_alumno_id,
        xp=perfil.xp,
        nivel=perfil.nivel,
        avatar_id=perfil.avatar_id,
        xp_para_siguiente_nivel=xp_acumulado_para_nivel(perfil.nivel + 1) - perfil.xp,
        avatares_disponibles=AVATARES_DISPONIBLES,
        racha_dias_actual=perfil.racha_dias_actual,
        racha_dias_maxima=perfil.racha_dias_maxima,
        guias_revisadas_total=perfil.guias_revisadas_total,
        evaluaciones_entregadas_total=perfil.evaluaciones_entregadas_total,
        tiempo_evaluando_total_seg=perfil.tiempo_evaluando_total_seg,
        logros=[
            LogroRespuesta(
                id=logro.id, nombre=logro.nombre, descripcion=logro.descripcion,
                icono=logro.icono, categoria=logro.categoria, desbloqueado=logro.id in desbloqueados,
            )
            for logro in CATALOGO_LOGROS
        ],
    )


@router.get("/{perfil_alumno_id}", response_model=PerfilGamificacionRespuesta)
def obtener_perfil(
    perfil_alumno_id: int = Depends(verificar_perfil_propio),
    uc: ObtenerPerfilGamificacion = Depends(get_obtener_perfil_gamificacion_uc),
):
    return _a_respuesta(uc.ejecutar(perfil_alumno_id))


class CambiarAvatarRequest(BaseModel):
    avatar_id: str


@router.patch("/{perfil_alumno_id}/avatar", response_model=PerfilGamificacionRespuesta)
def cambiar_avatar(
    datos: CambiarAvatarRequest,
    perfil_alumno_id: int = Depends(verificar_perfil_propio),
    uc: CambiarAvatar = Depends(get_cambiar_avatar_uc),
):
    try:
        perfil = uc.ejecutar(perfil_alumno_id, datos.avatar_id)
    except AvatarInvalido:
        raise HTTPException(status_code=400, detail="Avatar no disponible")
    return _a_respuesta(perfil)
