"""Nota estimada del Examen Libre y alerta temprana de ritmo de estudio — ideas propias, no
hallazgos de la competencia (ver `app/application/prediccion/consultas.py` para el detalle
de cada fórmula). Protegido con `verificar_perfil_propio`, mismo patrón que el resto de
rutas por perfil de alumno."""

from datetime import date

from fastapi import APIRouter, Depends
from pydantic import BaseModel

from app.application.prediccion.consultas import (
    EstimarNotaExamen,
    EvaluarRitmoDeEstudio,
    ObservarHorarioDeEstudio,
    ObtenerJardinSemanal,
    ObtenerMapaDeCalorPorEje,
)
from app.core.deps import (
    get_estimar_nota_examen_uc,
    get_evaluar_ritmo_de_estudio_uc,
    get_observar_horario_de_estudio_uc,
    get_obtener_jardin_semanal_uc,
    get_obtener_mapa_de_calor_uc,
    get_reloj,
    verificar_perfil_propio,
)
from app.domain.shared.reloj import Reloj

router = APIRouter(prefix="/prediccion", tags=["prediccion"])


class EstimacionAsignaturaRespuesta(BaseModel):
    asignatura_id: int
    asignatura_nombre: str
    nota_estimada: float | None
    confianza: str
    cobertura_pct: float


class EstimacionExamenRespuesta(BaseModel):
    nota_general_estimada: float | None
    confianza_general: str
    por_asignatura: list[EstimacionAsignaturaRespuesta]


@router.get("/{perfil_alumno_id}/nota-estimada", response_model=EstimacionExamenRespuesta)
def obtener_nota_estimada(
    nivel_id: int,
    perfil_alumno_id: int = Depends(verificar_perfil_propio),
    uc: EstimarNotaExamen = Depends(get_estimar_nota_examen_uc),
):
    resultado = uc.ejecutar(perfil_alumno_id, nivel_id)
    return EstimacionExamenRespuesta(
        nota_general_estimada=resultado.nota_general_estimada,
        confianza_general=resultado.confianza_general,
        por_asignatura=[
            EstimacionAsignaturaRespuesta(
                asignatura_id=a.asignatura_id, asignatura_nombre=a.asignatura_nombre,
                nota_estimada=a.nota_estimada, confianza=a.confianza, cobertura_pct=a.cobertura_pct,
            )
            for a in resultado.por_asignatura
        ],
    )


class AlertaRitmoRespuesta(BaseModel):
    tiene_alerta: bool
    mensaje: str
    dias_restantes: int
    oa_pendientes: int
    ritmo_actual_oa_por_dia: float
    ritmo_necesario_oa_por_dia: float


@router.get("/{perfil_alumno_id}/ritmo-de-estudio", response_model=AlertaRitmoRespuesta | None)
def obtener_alerta_de_ritmo(
    perfil_alumno_id: int = Depends(verificar_perfil_propio),
    uc: EvaluarRitmoDeEstudio = Depends(get_evaluar_ritmo_de_estudio_uc),
    reloj: Reloj = Depends(get_reloj),
):
    resultado = uc.ejecutar(perfil_alumno_id, reloj.ahora().date())
    if not resultado:
        return None
    return AlertaRitmoRespuesta(
        tiene_alerta=resultado.tiene_alerta, mensaje=resultado.mensaje, dias_restantes=resultado.dias_restantes,
        oa_pendientes=resultado.oa_pendientes, ritmo_actual_oa_por_dia=resultado.ritmo_actual_oa_por_dia,
        ritmo_necesario_oa_por_dia=resultado.ritmo_necesario_oa_por_dia,
    )


class CeldaMapaCalorRespuesta(BaseModel):
    asignatura_id: int
    asignatura_nombre: str
    eje_tematico: str
    pct_correctas: float
    total_preguntas: int


@router.get("/{perfil_alumno_id}/mapa-calor", response_model=list[CeldaMapaCalorRespuesta])
def obtener_mapa_de_calor(
    perfil_alumno_id: int = Depends(verificar_perfil_propio),
    uc: ObtenerMapaDeCalorPorEje = Depends(get_obtener_mapa_de_calor_uc),
):
    return [
        CeldaMapaCalorRespuesta(
            asignatura_id=c.asignatura_id, asignatura_nombre=c.asignatura_nombre, eje_tematico=c.eje_tematico,
            pct_correctas=c.pct_correctas, total_preguntas=c.total_preguntas,
        )
        for c in uc.ejecutar(perfil_alumno_id)
    ]


class ObservacionHorarioRespuesta(BaseModel):
    tiene_observacion: bool
    mensaje: str
    sesiones_tarde: int
    sesiones_analizadas: int


@router.get("/{perfil_alumno_id}/horario-de-estudio", response_model=ObservacionHorarioRespuesta | None)
def obtener_observacion_de_horario(
    perfil_alumno_id: int = Depends(verificar_perfil_propio),
    uc: ObservarHorarioDeEstudio = Depends(get_observar_horario_de_estudio_uc),
):
    resultado = uc.ejecutar(perfil_alumno_id)
    if not resultado:
        return None
    return ObservacionHorarioRespuesta(
        tiene_observacion=resultado.tiene_observacion, mensaje=resultado.mensaje,
        sesiones_tarde=resultado.sesiones_tarde, sesiones_analizadas=resultado.sesiones_analizadas,
    )


class SemanaJardinRespuesta(BaseModel):
    semana_inicio: str
    dias_activos: int
    etapa: str


@router.get("/{perfil_alumno_id}/jardin-semanal", response_model=list[SemanaJardinRespuesta])
def obtener_jardin_semanal(
    perfil_alumno_id: int = Depends(verificar_perfil_propio),
    uc: ObtenerJardinSemanal = Depends(get_obtener_jardin_semanal_uc),
    reloj: Reloj = Depends(get_reloj),
):
    return [
        SemanaJardinRespuesta(semana_inicio=s.semana_inicio.isoformat(), dias_activos=s.dias_activos, etapa=s.etapa)
        for s in uc.ejecutar(perfil_alumno_id, reloj.ahora().date())
    ]
