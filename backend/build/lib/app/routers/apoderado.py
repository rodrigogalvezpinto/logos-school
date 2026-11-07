"""Vistas agregadas para el Apoderado sobre todos sus alumnos — idea propia, no un hallazgo
de la competencia (ver `app/application/apoderado/consultas.py`)."""

from fastapi import APIRouter, Depends
from pydantic import BaseModel

from app.application.apoderado.casos_de_uso import MarcarAgendaFamiliarConversada
from app.application.apoderado.consultas import ObtenerAgendaFamiliar, ObtenerEstadisticasFamiliares, ObtenerMetaFamiliar
from app.core.deps import (
    get_cuenta_actual,
    get_marcar_agenda_familiar_conversada_uc,
    get_obtener_agenda_familiar_uc,
    get_obtener_estadisticas_familiares_uc,
    get_obtener_meta_familiar_uc,
    get_reloj,
    verificar_perfil_propio,
)
from app.domain.auth.entities import Cuenta
from app.domain.shared.reloj import Reloj

router = APIRouter(prefix="/apoderado", tags=["apoderado"])


class EstadisticaAlumnoRespuesta(BaseModel):
    perfil_alumno_id: int
    nombre: str
    cobertura_pct: float
    racha_dias_actual: int
    tiene_alerta_de_ritmo: bool


@router.get("/estadisticas", response_model=list[EstadisticaAlumnoRespuesta])
def obtener_estadisticas(
    cuenta: Cuenta = Depends(get_cuenta_actual),
    uc: ObtenerEstadisticasFamiliares = Depends(get_obtener_estadisticas_familiares_uc),
    reloj: Reloj = Depends(get_reloj),
):
    return [
        EstadisticaAlumnoRespuesta(
            perfil_alumno_id=e.perfil_alumno_id, nombre=e.nombre, cobertura_pct=e.cobertura_pct,
            racha_dias_actual=e.racha_dias_actual, tiene_alerta_de_ritmo=e.tiene_alerta_de_ritmo,
        )
        for e in uc.ejecutar(cuenta.id, reloj.ahora().date())
    ]


class MetaFamiliarRespuesta(BaseModel):
    dias_esta_semana: int
    dias_semana_anterior: int
    es_nueva_marca: bool


@router.get("/meta-familiar", response_model=MetaFamiliarRespuesta | None)
def obtener_meta_familiar(
    cuenta: Cuenta = Depends(get_cuenta_actual),
    uc: ObtenerMetaFamiliar = Depends(get_obtener_meta_familiar_uc),
    reloj: Reloj = Depends(get_reloj),
):
    resultado = uc.ejecutar(cuenta.id, reloj.ahora().date())
    if not resultado:
        return None
    return MetaFamiliarRespuesta(
        dias_esta_semana=resultado.dias_esta_semana, dias_semana_anterior=resultado.dias_semana_anterior,
        es_nueva_marca=resultado.es_nueva_marca,
    )


class AgendaFamiliarRespuesta(BaseModel):
    preguntas: list[str]
    ya_conversada: bool


@router.get("/agenda-familiar/{perfil_alumno_id}", response_model=AgendaFamiliarRespuesta)
def obtener_agenda_familiar(
    perfil_alumno_id: int = Depends(verificar_perfil_propio),
    uc: ObtenerAgendaFamiliar = Depends(get_obtener_agenda_familiar_uc),
    reloj: Reloj = Depends(get_reloj),
):
    resultado = uc.ejecutar(perfil_alumno_id, reloj.ahora().date())
    return AgendaFamiliarRespuesta(preguntas=resultado.preguntas, ya_conversada=resultado.ya_conversada)


@router.post("/agenda-familiar/{perfil_alumno_id}/conversada", status_code=204)
def marcar_agenda_familiar_conversada(
    perfil_alumno_id: int = Depends(verificar_perfil_propio),
    uc: MarcarAgendaFamiliarConversada = Depends(get_marcar_agenda_familiar_conversada_uc),
    reloj: Reloj = Depends(get_reloj),
):
    uc.ejecutar(perfil_alumno_id, reloj.ahora().date())
