"""Historial y notas por materia (Fase 1.2) — ver planificacion/03-roadmap-etapas.md y
planificacion/12-motor-de-evaluacion.md, sección "Notas por materia y señal real de
preparación". Ambos endpoints exigen que el `perfil_alumno_id` de la ruta pertenezca a la
Cuenta autenticada (`verificar_perfil_propio`) — es la primera vista que expone datos
personales agregados de un menor."""

from datetime import datetime

from fastapi import APIRouter, Depends, status
from pydantic import BaseModel

from app.application.progreso.consultas import ObtenerFaltantes, ObtenerHistorialYNotas
from app.application.progreso.marcar_guia_revisada import MarcarGuiaRevisada
from app.core.deps import (
    get_marcar_guia_revisada_uc,
    get_obtener_faltantes_uc,
    get_obtener_historial_y_notas_uc,
    verificar_perfil_propio,
)

router = APIRouter(prefix="/progreso", tags=["progreso"])


class ItemHistorialRespuesta(BaseModel):
    intento_id: int
    conjunto_id: int
    tipo: str
    asignatura_id: int | None
    asignatura_nombre: str | None
    nombre: str
    nota: float | None
    fecha: datetime


class GuiaRevisadaRespuesta(BaseModel):
    oa_id: int
    fecha: datetime
    codigo_oficial: str
    asignatura_nombre: str


class NotaPorAsignaturaRespuesta(BaseModel):
    asignatura_id: int
    asignatura_nombre: str
    nota_practica: float | None
    nota_simulacro: float | None


class HistorialRespuesta(BaseModel):
    historial: list[ItemHistorialRespuesta]
    guias_revisadas: list[GuiaRevisadaRespuesta]
    notas_por_asignatura: list[NotaPorAsignaturaRespuesta]


@router.get("/{perfil_alumno_id}", response_model=HistorialRespuesta)
def obtener_historial(
    perfil_alumno_id: int = Depends(verificar_perfil_propio),
    uc: ObtenerHistorialYNotas = Depends(get_obtener_historial_y_notas_uc),
):
    resultado = uc.ejecutar(perfil_alumno_id)
    return HistorialRespuesta(
        historial=[
            ItemHistorialRespuesta(
                intento_id=i.intento_id, conjunto_id=i.conjunto_id, tipo=i.tipo,
                asignatura_id=i.asignatura_id, asignatura_nombre=i.asignatura_nombre,
                nombre=i.nombre, nota=i.nota, fecha=i.fecha,
            )
            for i in resultado.historial
        ],
        guias_revisadas=[
            GuiaRevisadaRespuesta(
                oa_id=g.oa_id, fecha=g.fecha,
                codigo_oficial=g.codigo_oficial, asignatura_nombre=g.asignatura_nombre,
            )
            for g in resultado.guias_revisadas
        ],
        notas_por_asignatura=[
            NotaPorAsignaturaRespuesta(
                asignatura_id=n.asignatura_id, asignatura_nombre=n.asignatura_nombre,
                nota_practica=n.nota_practica, nota_simulacro=n.nota_simulacro,
            )
            for n in resultado.notas_por_asignatura
        ],
    )


@router.post("/{perfil_alumno_id}/guias/{oa_id}/revisada", status_code=status.HTTP_204_NO_CONTENT)
def marcar_guia_revisada(
    oa_id: int,
    perfil_alumno_id: int = Depends(verificar_perfil_propio),
    uc: MarcarGuiaRevisada = Depends(get_marcar_guia_revisada_uc),
):
    uc.ejecutar(perfil_alumno_id, oa_id)


class ItemFaltanteRespuesta(BaseModel):
    conjunto_id: int
    tipo: str
    nombre: str
    asignatura_id: int | None
    habilitado: bool


class CoberturaAsignaturaRespuesta(BaseModel):
    asignatura_id: int
    asignatura_nombre: str
    cobertura_pct: float
    simulacro_parcial_disponible: bool


class FaltantesRespuesta(BaseModel):
    faltantes: list[ItemFaltanteRespuesta]
    coberturas: list[CoberturaAsignaturaRespuesta]


@router.get("/{perfil_alumno_id}/faltantes", response_model=FaltantesRespuesta)
def obtener_faltantes(
    nivel_id: int,
    perfil_alumno_id: int = Depends(verificar_perfil_propio),
    uc: ObtenerFaltantes = Depends(get_obtener_faltantes_uc),
):
    resultado = uc.ejecutar(perfil_alumno_id, nivel_id)
    return FaltantesRespuesta(
        faltantes=[
            ItemFaltanteRespuesta(
                conjunto_id=f.conjunto_id, tipo=f.tipo, nombre=f.nombre,
                asignatura_id=f.asignatura_id, habilitado=f.habilitado,
            )
            for f in resultado.faltantes
        ],
        coberturas=[
            CoberturaAsignaturaRespuesta(
                asignatura_id=c.asignatura_id, asignatura_nombre=c.asignatura_nombre,
                cobertura_pct=c.cobertura_pct, simulacro_parcial_disponible=c.simulacro_parcial_disponible,
            )
            for c in resultado.coberturas
        ],
    )
