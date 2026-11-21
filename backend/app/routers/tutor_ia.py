"""Profesor IA (Fase 2, tarea 14, 2026-11-18; diseño en planificacion/30-profesor-ia.md).

Detrás de configuración: solo responde si `LOGOS_IA_HABILITADA=true` y hay `ANTHROPIC_API_KEY` en el `.env`.
El alumno conversa sobre el OA que está estudiando. Al proveedor se envía solo la guía del OA, el nombre del curso
(«4° básico») y los mensajes del alumno, anonimizados. Nada de la cuenta ni del perfil.
"""
from collections import defaultdict
from datetime import date
from threading import Lock
from typing import Literal

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field

from app.core.config import settings
from app.core.deps import get_repositorio_contenido, verificar_perfil_propio
from app.domain.contenido.ports import RepositorioContenido
from app.domain.tutor_ia.ports import MensajeTutor, TutorIA, TutorNoDisponible
from app.domain.tutor_ia.salvaguardas import (
    LARGO_MAXIMO_MENSAJE,
    MENSAJES_DE_HISTORIAL,
    RESPUESTA_CRISIS,
    anonimizar,
    senal_de_crisis,
)

router = APIRouter(prefix="/tutor-ia", tags=["tutor-ia"])


def tutor_habilitado() -> bool:
    return settings.logos_ia_habilitada and bool(settings.anthropic_api_key)


def get_tutor_ia() -> TutorIA:
    from app.infrastructure.ia.tutor_claude import TutorIAClaude, TutorIADesactivado

    if not tutor_habilitado():
        return TutorIADesactivado()
    return TutorIAClaude(api_key=settings.anthropic_api_key, modelo=settings.logos_ia_modelo)


class _UsoDiario:
    """Tope de mensajes por alumno y día. En memoria del proceso: suficiente con una sola instancia del backend;
    con varias, pasarlo a la base de datos."""

    def __init__(self):
        self._conteo: dict[tuple[int, date], int] = defaultdict(int)
        self._lock = Lock()

    def registrar(self, perfil_alumno_id: int, limite: int) -> bool:
        clave = (perfil_alumno_id, date.today())
        with self._lock:
            if self._conteo[clave] >= limite:
                return False
            self._conteo[clave] += 1
            return True


uso_diario = _UsoDiario()


class EstadoTutor(BaseModel):
    habilitado: bool


class MensajeEntrada(BaseModel):
    rol: Literal["alumno", "tutor"]
    texto: str = Field(min_length=1, max_length=4000)


class Conversacion(BaseModel):
    mensajes: list[MensajeEntrada] = Field(min_length=1, max_length=40)


class RespuestaSalida(BaseModel):
    texto: str
    derivacion: bool = False  # True cuando se respondió con el mensaje fijo de ayuda (señal de crisis)


@router.get("/estado", response_model=EstadoTutor)
def estado():
    return EstadoTutor(habilitado=tutor_habilitado())


@router.post("/{perfil_alumno_id}/oa/{oa_id}", response_model=RespuestaSalida)
def preguntar(
    oa_id: int,
    conversacion: Conversacion,
    perfil_alumno_id: int = Depends(verificar_perfil_propio),
    contenido: RepositorioContenido = Depends(get_repositorio_contenido),
    tutor: TutorIA = Depends(get_tutor_ia),
):
    if conversacion.mensajes[-1].rol != "alumno":
        raise HTTPException(status_code=422, detail="El último mensaje debe ser del alumno")
    ultimo = conversacion.mensajes[-1].texto
    # Red de seguridad: ante una señal de crisis no se llama al proveedor y se deriva a personas.
    if senal_de_crisis(ultimo):
        return RespuestaSalida(texto=RESPUESTA_CRISIS, derivacion=True)
    if not tutor_habilitado():
        raise HTTPException(status_code=503, detail="El Profesor IA no está disponible")

    oa = contenido.obtener_objetivo(oa_id)
    if not oa:
        raise HTTPException(status_code=404, detail="Objetivo de Aprendizaje no encontrado")
    asignatura = contenido.obtener_asignatura(oa.asignatura_id)
    nivel = contenido.obtener_nivel(asignatura.nivel_id) if asignatura else None

    if not uso_diario.registrar(perfil_alumno_id, settings.logos_ia_limite_diario):
        raise HTTPException(status_code=429, detail="Llegaste al máximo de preguntas de hoy. ¡Mañana puedes seguir!")

    mensajes = [
        MensajeTutor(rol=m.rol, texto=anonimizar(m.texto[:LARGO_MAXIMO_MENSAJE]))
        for m in conversacion.mensajes[-MENSAJES_DE_HISTORIAL:]
    ]
    while mensajes and mensajes[0].rol != "alumno":  # la conversación enviada debe empezar por el alumno
        mensajes.pop(0)
    try:
        r = tutor.responder(
            nivel=nivel.nombre if nivel else "enseñanza escolar",
            objetivo=f"{oa.codigo_oficial}: {oa.descripcion}",
            guia=oa.contenido_guia,
            mensajes=mensajes,
        )
    except TutorNoDisponible:
        raise HTTPException(status_code=503, detail="El Profesor IA no pudo responder ahora. Intenta en unos minutos.")
    return RespuestaSalida(texto=r.texto)
