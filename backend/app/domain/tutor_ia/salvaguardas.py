"""Salvaguardas del Profesor IA para menores de edad (2026-11-18).

1. Privacidad: solo se envía al proveedor el texto de la guía y lo que el alumno escribe, y antes se borran datos
   personales evidentes (RUT, correos, teléfonos). Nunca se envían nombre, curso real ni datos de la cuenta.
2. Señales de crisis: si el mensaje sugiere autolesión o riesgo, no se llama al proveedor; se responde con un mensaje
   fijo, cálido, que deriva a un adulto de confianza y a líneas de ayuda chilenas. Es una red de seguridad simple
   (por palabras), complementaria a las instrucciones del modelo, no un sistema de detección clínica.
3. Límites: largo máximo por mensaje y cantidad de mensajes de historial que se envían.
"""
import re

LARGO_MAXIMO_MENSAJE = 800
MENSAJES_DE_HISTORIAL = 10

_RUT = re.compile(r"\b\d{1,2}\.?\d{3}\.?\d{3}-?[\dkK]\b")
_CORREO = re.compile(r"\b[\w.+-]+@[\w-]+\.[\w.-]+\b")
_TELEFONO = re.compile(r"(?:\+?56\s?)?(?:\b9\s?\d{4}\s?\d{4}\b|\b\d{2}\s?\d{3}\s?\d{4}\b)")

_CRISIS = re.compile(
    r"\b(suicid\w*|matarme|quitarme la vida|me quiero morir|quiero morir(me)?|no quiero vivir|"
    r"hacerme daño|cortarme|autolesi\w*|me pegan|me golpean|abus\w+ de m[ií]|me tocan)\b",
    re.IGNORECASE,
)

RESPUESTA_CRISIS = (
    "Gracias por contármelo. Lo que sientes es importante y no tienes que enfrentarlo solo o sola. "
    "Por favor, habla ahora con un adulto de confianza: tu mamá, papá, apoderado, un profesor o alguien de tu familia. "
    "Si necesitas ayuda inmediata, puedes llamar gratis a la línea de prevención del suicidio *4141 (desde celulares) "
    "o a Salud Responde, 600 360 7777, las 24 horas. Si estás en peligro ahora, llama al 131 (SAMU) o al 133 (Carabineros). "
    "Yo soy un tutor de estudio y no puedo ayudarte con esto como lo haría una persona, pero hay personas listas para escucharte."
)


def anonimizar(texto: str) -> str:
    texto = _RUT.sub("[dato borrado]", texto)
    texto = _CORREO.sub("[dato borrado]", texto)
    return _TELEFONO.sub("[dato borrado]", texto)


def senal_de_crisis(texto: str) -> bool:
    return bool(_CRISIS.search(texto))
