"""Adaptador del Profesor IA con la API de Claude (SDK oficial `anthropic`), 2026-11-18.

- Modelo configurable (`LOGOS_IA_MODELO`, por defecto Claude Opus 5.5) con esfuerzo bajo: es una conversación breve.
- El pensamiento adaptativo está siempre activo en Opus 5.5; no se envía `thinking`.
- Prefijo estable (instrucciones + guía del OA) con caché automática: cada pregunta del mismo OA reutiliza el prefijo.
- Respaldo del servidor ante rechazos (`fallbacks: "default"`), como recomienda la documentación para Opus 5.5.
- Solo se envía texto de la guía y lo que escribió el alumno, ya anonimizado (ver `salvaguardas`).
"""
import logging

import anthropic

from app.domain.tutor_ia.instrucciones import instrucciones_para
from app.domain.tutor_ia.ports import MensajeTutor, RespuestaTutor, TutorNoDisponible

log = logging.getLogger(__name__)

RESPUESTA_DECLINADA = "No puedo ayudarte con eso. Si quieres, sigamos con el tema de la guía: ¿qué parte te cuesta más?"


class TutorIAClaude:
    def __init__(self, api_key: str, modelo: str):
        self._cliente = anthropic.Anthropic(api_key=api_key, max_retries=2, timeout=60.0)
        self._modelo = modelo

    def responder(self, *, nivel: str, objetivo: str, guia: str, mensajes: list[MensajeTutor]) -> RespuestaTutor:
        try:
            respuesta = self._cliente.beta.messages.create(
                model=self._modelo,
                max_tokens=8000,
                betas=["server-side-fallback-2026-07-01"],
                fallbacks="default",
                output_config={"effort": "low"},
                cache_control={"type": "ephemeral"},
                system=instrucciones_para(nivel, objetivo, guia),
                messages=[
                    {"role": "user" if m.rol == "alumno" else "assistant", "content": m.texto} for m in mensajes
                ],
            )
        except anthropic.AuthenticationError as e:
            log.error("Profesor IA: clave inválida (request_id=%s)", getattr(e, "request_id", None))
            raise TutorNoDisponible from e
        except anthropic.RateLimitError as e:
            log.warning("Profesor IA: límite de uso del proveedor")
            raise TutorNoDisponible from e
        except anthropic.APIStatusError as e:
            log.error("Profesor IA: error %s del proveedor", e.status_code)
            raise TutorNoDisponible from e
        except anthropic.APIConnectionError as e:
            log.error("Profesor IA: sin conexión con el proveedor")
            raise TutorNoDisponible from e

        if respuesta.stop_reason == "refusal":
            return RespuestaTutor(texto=RESPUESTA_DECLINADA, declinada=True)
        texto = "".join(b.text for b in respuesta.content if b.type == "text").strip()
        if not texto:
            raise TutorNoDisponible("respuesta vacía")
        return RespuestaTutor(texto=texto)


class TutorIADesactivado:
    """Sin clave o sin `LOGOS_IA_HABILITADA`: el tutor no existe para la app."""

    def responder(self, *, nivel: str, objetivo: str, guia: str, mensajes: list[MensajeTutor]) -> RespuestaTutor:
        raise TutorNoDisponible("Profesor IA desactivado")
