"""Plan de estudio con horario (Fase 1.3) — ver planificacion/13-plan-de-estudio.md.
Protegido con `verificar_perfil_propio`, mismo patrón que progreso.py."""

from datetime import date

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel

from app.application.plan_estudio.casos_de_uso import AgregarSesionDeRepaso, CrearPlanDeEstudio, ObtenerPlanActivo
from app.core.deps import (
    get_agregar_sesion_de_repaso_uc,
    get_crear_plan_de_estudio_uc,
    get_obtener_plan_activo_uc,
    get_reloj,
    verificar_perfil_propio,
)
from app.domain.plan_estudio.entities import PlanDeEstudio
from app.domain.plan_estudio.exceptions import (
    AsignaturaNoEncontrada,
    DiasInvalidos,
    NivelNoEsAnterior,
    PerfilAlumnoNoEncontrado,
    PlanDeEstudioNoEncontrado,
)
from app.domain.shared.reloj import Reloj

router = APIRouter(prefix="/plan-estudio", tags=["plan-estudio"])


class CrearPlanRequest(BaseModel):
    dias_por_semana: int
    dias_elegidos: list[str]
    fecha_objetivo: date | None = None


class SesionRespuesta(BaseModel):
    id: int
    fecha_programada: date
    asignatura_id: int
    oa_ids: list[int]
    incluye_prueba_unidad: bool
    minutos_estimados: int
    cumplida: bool
    es_repaso: bool
    atrasada: bool
    """Fecha programada ya pasó y no se cumplió — hallazgo comparando en vivo contra
    Brincus (ver planificacion/25-analisis-competencia-brincus.md, Paso 12: "Finalizadas /
    Pendientes / No finalizadas"). Se calcula al vuelo (`fecha_programada < hoy`), no se
    persiste — mismo criterio que `cumplida`, que tampoco se guarda en la sesión."""


class PlanRespuesta(BaseModel):
    id: int
    dias_por_semana: int
    dias_elegidos: list[str]
    fecha_inicio: date
    fecha_objetivo: date | None
    sesiones: list[SesionRespuesta]


def _a_respuesta(plan: PlanDeEstudio, cumplidas: dict[int, bool], hoy: date) -> PlanRespuesta:
    return PlanRespuesta(
        id=plan.id,
        dias_por_semana=plan.dias_por_semana,
        dias_elegidos=plan.dias_elegidos,
        fecha_inicio=plan.fecha_inicio,
        fecha_objetivo=plan.fecha_objetivo,
        sesiones=[
            SesionRespuesta(
                id=s.id,
                fecha_programada=s.fecha_programada,
                asignatura_id=s.asignatura_id,
                oa_ids=s.oa_ids,
                incluye_prueba_unidad=s.incluye_prueba_unidad,
                minutos_estimados=s.minutos_estimados(),
                cumplida=cumplidas.get(s.id, False),
                es_repaso=s.es_repaso,
                atrasada=(not cumplidas.get(s.id, False)) and s.fecha_programada < hoy,
            )
            for s in plan.sesiones
        ],
    )


@router.post("/{perfil_alumno_id}", response_model=PlanRespuesta, status_code=status.HTTP_201_CREATED)
def crear_plan(
    datos: CrearPlanRequest,
    perfil_alumno_id: int = Depends(verificar_perfil_propio),
    uc: CrearPlanDeEstudio = Depends(get_crear_plan_de_estudio_uc),
    reloj: Reloj = Depends(get_reloj),
):
    try:
        plan = uc.ejecutar(perfil_alumno_id, datos.dias_por_semana, datos.dias_elegidos, datos.fecha_objetivo)
    except DiasInvalidos as e:
        raise HTTPException(status_code=422, detail=str(e))
    except PerfilAlumnoNoEncontrado:
        raise HTTPException(status_code=404, detail="Perfil de alumno no encontrado")
    # Recién generado: por construcción ninguna sesión cubre OA ya revisadas, así que
    # todas parten como no cumplidas.
    return _a_respuesta(plan, {s.id: False for s in plan.sesiones}, reloj.ahora().date())


@router.get("/{perfil_alumno_id}", response_model=PlanRespuesta)
def obtener_plan(
    perfil_alumno_id: int = Depends(verificar_perfil_propio),
    uc: ObtenerPlanActivo = Depends(get_obtener_plan_activo_uc),
    reloj: Reloj = Depends(get_reloj),
):
    try:
        plan, cumplidas = uc.ejecutar(perfil_alumno_id)
    except PlanDeEstudioNoEncontrado:
        raise HTTPException(status_code=404, detail="Este alumno todavía no tiene un plan de estudio")
    return _a_respuesta(plan, cumplidas, reloj.ahora().date())


class AgregarRepasoRequest(BaseModel):
    asignatura_id: int
    oa_ids: list[int]


@router.post("/{perfil_alumno_id}/repaso", response_model=SesionRespuesta, status_code=status.HTTP_201_CREATED)
def agregar_repaso(
    datos: AgregarRepasoRequest,
    perfil_alumno_id: int = Depends(verificar_perfil_propio),
    uc: AgregarSesionDeRepaso = Depends(get_agregar_sesion_de_repaso_uc),
):
    try:
        sesion = uc.ejecutar(perfil_alumno_id, datos.asignatura_id, datos.oa_ids)
    except PerfilAlumnoNoEncontrado:
        raise HTTPException(status_code=404, detail="Perfil de alumno no encontrado")
    except PlanDeEstudioNoEncontrado:
        raise HTTPException(status_code=404, detail="Este alumno todavía no tiene un plan de estudio")
    except AsignaturaNoEncontrada:
        raise HTTPException(status_code=404, detail="Asignatura no encontrada")
    except NivelNoEsAnterior:
        raise HTTPException(status_code=422, detail="Solo puedes repasar contenido de un nivel ya cursado")
    # Recién agregada, siempre a futuro (ver AgregarSesionDeRepaso: se agenda al final del
    # plan) — nunca puede nacer "atrasada".
    return SesionRespuesta(
        id=sesion.id, fecha_programada=sesion.fecha_programada, asignatura_id=sesion.asignatura_id,
        oa_ids=sesion.oa_ids, incluye_prueba_unidad=sesion.incluye_prueba_unidad,
        minutos_estimados=sesion.minutos_estimados(), cumplida=False, es_repaso=sesion.es_repaso,
        atrasada=False,
    )
