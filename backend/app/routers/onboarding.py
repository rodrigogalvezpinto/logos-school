"""Onboarding con checklist de primera sesión (Fase 1, ítem 2.3 — ver
planificacion/27-plan-incorporacion-hallazgos-brincus.md)."""

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

from app.application.onboarding.casos_de_uso import CompletarPasoOnboarding, ObtenerProgresoOnboarding
from app.core.deps import get_completar_paso_onboarding_uc, get_obtener_progreso_onboarding_uc, verificar_perfil_propio
from app.domain.onboarding.entities import PASOS_ONBOARDING
from app.domain.onboarding.exceptions import PasoInvalido

router = APIRouter(prefix="/onboarding", tags=["onboarding"])


class ProgresoOnboardingRespuesta(BaseModel):
    perfil_alumno_id: int
    pasos: list[str]
    pasos_completados: list[str]
    completo: bool


def _a_respuesta(progreso) -> ProgresoOnboardingRespuesta:
    return ProgresoOnboardingRespuesta(
        perfil_alumno_id=progreso.perfil_alumno_id,
        pasos=PASOS_ONBOARDING,
        pasos_completados=sorted(progreso.pasos_completados),
        completo=progreso.completo,
    )


@router.get("/{perfil_alumno_id}", response_model=ProgresoOnboardingRespuesta)
def obtener_progreso(
    perfil_alumno_id: int = Depends(verificar_perfil_propio),
    uc: ObtenerProgresoOnboarding = Depends(get_obtener_progreso_onboarding_uc),
):
    return _a_respuesta(uc.ejecutar(perfil_alumno_id))


@router.post("/{perfil_alumno_id}/pasos/{paso_id}/completar", response_model=ProgresoOnboardingRespuesta)
def completar_paso(
    paso_id: str,
    perfil_alumno_id: int = Depends(verificar_perfil_propio),
    uc: CompletarPasoOnboarding = Depends(get_completar_paso_onboarding_uc),
):
    try:
        progreso = uc.ejecutar(perfil_alumno_id, paso_id)
    except PasoInvalido:
        raise HTTPException(status_code=400, detail="Paso de onboarding no reconocido")
    return _a_respuesta(progreso)
