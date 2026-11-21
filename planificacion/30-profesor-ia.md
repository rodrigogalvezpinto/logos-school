# Profesor IA (Fase 2, tarea 14) — 2026-11-18

Rama `feature/profesor-ia` (sin unir a `main` hasta que el dueño lo apruebe). **Desactivado** mientras no exista clave.

## Qué es

Un panel «Pregúntale al Profesor IA» bajo la guía de cada OA. El alumno escribe una duda y un tutor con IA le
responde con pistas, apoyado en la guía de ese OA. No aparece si el backend no está activado.

## Cómo se activa (lo hace el dueño)

En `backend/.env` (nunca en el chat ni en git):

```
LOGOS_IA_HABILITADA=true
ANTHROPIC_API_KEY=<clave de la consola de Anthropic>
# Opcionales:
LOGOS_IA_MODELO=claude-opus-5-5   # modelo; para bajar costo se puede usar claude-haiku-5-5
LOGOS_IA_LIMITE_DIARIO=30         # preguntas por alumno y por día
```

Sin las dos primeras, `/tutor-ia/estado` responde `{"habilitado": false}` y el panel no se muestra.

## Salvaguardas para menores

| Riesgo | Medida |
|---|---|
| Datos personales al proveedor | Solo se envían la guía del OA, el nombre del curso («4° básico») y los mensajes del alumno. Antes se borran RUT, correos y teléfonos (`anonimizar`). Nunca nombre, cuenta ni perfil. El panel pide no escribir datos personales. |
| Señales de crisis | Si el mensaje sugiere autolesión, abuso o peligro, **no se llama al proveedor**: se responde un mensaje fijo que deriva a un adulto de confianza y a *4141, Salud Responde 600 360 7777, 131 y 133. Es una red por palabras, complementaria a las instrucciones del modelo. |
| Temas fuera del estudio | Las instrucciones limitan al tutor a temas escolares, sin pedir datos y presentándose como IA. Si el proveedor declina (`stop_reason: refusal`), se muestra un mensaje neutro. |
| Uso excesivo o costo | Tope diario por alumno (30 por defecto), largo máximo por mensaje (800) y solo los últimos 10 mensajes como contexto. El tope es en memoria: con varias instancias del backend hay que pasarlo a la base. |
| Dependencia del perfil | El endpoint exige que el perfil pertenezca a la cuenta autenticada (`verificar_perfil_propio`). |

## Decisiones técnicas

- SDK oficial `anthropic` (2.x), modelo por defecto Claude Opus 5.5 con esfuerzo `low` (conversación breve), pensamiento
  adaptativo siempre activo en ese modelo, respaldo del servidor ante rechazos (`fallbacks: "default"`) y caché del
  prefijo (instrucciones + guía), que es igual para todas las preguntas del mismo OA.
- Hexagonal: contrato `TutorIA` en el dominio; adaptadores `TutorIAClaude` y `TutorIADesactivado`; en los tests, un
  tutor falso. Ningún test llama a la API real.
- Costo de referencia: Opus 5.5 cuesta USD 4 por millón de tokens de entrada y 20 de salida, con lecturas de caché a
  0,20. Haiku 5.5 cuesta 0,10 y 0,50. Conviene medir con uso real antes de elegir.

## Pendiente

- Que el dueño cree la clave (ver `docs/PENDIENTES-USUARIO.md`) y pruebe con conversaciones reales antes de abrirlo a
  alumnos. Revisar con un profesor el tono y las respuestas.
- Registro de conversaciones para revisión docente: no se guarda nada hoy, por privacidad. Si se quiere, definir antes
  retención y consentimiento del apoderado.
