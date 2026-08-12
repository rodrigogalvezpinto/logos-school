---
título: Motor de evaluación — flujo de rendir guía/prueba/examen, cálculo de nota
estado: especificación lista para desarrollo (2026-08-12), parte de la Fase 1.1
última actualización: 2026-08-12
---

## Qué es esto

El "motor de evaluación" es el componente reutilizable que maneja **cualquier instancia en
que el alumno responde preguntas**: autoevaluación formativa por OA, prueba de unidad, o
examen simulacro. Los tres usan el mismo mecanismo de navegación y envío, pero con
parámetros distintos (cronometrado o no, con nota o no, feedback inmediato o al final).

| | Autoevaluación por OA | Prueba de unidad | Examen simulacro |
|---|---|---|---|
| Cronómetro | No | **No** (decisión 2026-08-12: sin presión de tiempo, el alumno responde a su ritmo) | Sí, estricto (90 min real, sin excepción) |
| Feedback | Inmediato, pregunta a pregunta | Solo al final | Solo al final |
| ¿Tiene nota? | No (es formativo, práctica libre) | Sí | Sí |
| Presión/tono en la UI | Relajado, "estás practicando" | Relajado, sin cronómetro, pero sí con nota al final | Serio, simula la condición real |

**Nota 2026-08-12:** se decidió explícitamente que las Pruebas de unidad NO tienen
cronómetro — solo el Examen simulacro lo mantiene, porque es el único que debe imitar la
condición real del examen Mineduc (90 minutos estrictos). Las pruebas de unidad son para
practicar sin presión de tiempo, aunque sí generan una nota al terminar.

## Flujo de "rendir" una evaluación (prueba de unidad / examen simulacro)

1. **Pantalla de inicio**: nombre de la evaluación, cantidad de preguntas, tiempo asignado
   (solo si aplica — examen simulacro), instrucciones breves, botón "Comenzar". Para el
   examen simulacro, remarcar que simula la condición real (sin pausas, sin ayuda, 90
   minutos estrictos) — coherente con lo investigado en `07-experto-examenes-libres.md`
   sobre el examen real. Las pruebas de unidad no muestran cronómetro.
2. **Arranca el cronómetro** (cuenta regresiva visible) al presionar Comenzar — solo en el
   examen simulacro.
3. **Navegación pregunta a pregunta**: se muestra una pregunta a la vez (no todas juntas),
   con:
   - El enunciado y, si aplica, las alternativas (checkbox/radio de selección única) o un
     campo de texto (preguntas de desarrollo/abiertas).
   - Botones "Anterior" / "Siguiente".
   - Indicador de progreso ("Pregunta 7 de 20") y un mapa de preguntas (miniatura numerada,
     clickeable) que muestra de un vistazo cuáles están respondidas, cuáles no, y cuáles
     marcadas para revisar — así el alumno nunca pierde noción de qué le falta.
   - Opción de "marcar para revisar" (para volver antes de enviar).
   - La respuesta se guarda automáticamente al cambiar de pregunta y también en segundo
     plano cada cierto tiempo (autosave) — si el alumno cierra la pestaña, pierde la
     conexión, o su dispositivo falla, **no pierde lo avanzado**: al volver a entrar a esa
     misma evaluación, continúa exactamente donde quedó, con todas sus respuestas
     anteriores intactas (ver `20-seguridad-y-casos-borde.md`, caso "abandono y
     reingreso").
4. **Validación antes de enviar (obligatoria, no opcional)**: al presionar "Entregar", el
   sistema revisa si quedan preguntas sin responder.
   - **Si falta algo**: aparece un aviso claro y difícil de ignorar (modal, no un texto
     chico) — *"Te falta responder la pregunta 8 (y 2 más). ¿Quieres revisarlas o enviar
     igual, dejándolas en blanco?"* — con dos botones igual de visibles: "Ir a revisar" y
     "Enviar de todas formas". El botón final de "Enviar evaluación" **no se habilita**
     hasta que el alumno pase por esta confirmación explícita — nunca se envía por
     accidente ni sin que el alumno sepa exactamente qué está dejando en blanco.
   - **Si todo está respondido**: confirmación simple ("¿Seguro que quieres entregar?") antes
     de enviar, para evitar un envío accidental por doble clic.
5. **Envío**: manual (tras la validación de arriba) o automático si se agota el tiempo en el
   examen simulacro — en ese caso se envía lo que esté respondido hasta ese momento, sin
   excepción (así se comporta el examen real; no aplica a pruebas de unidad, que no tienen
   límite de tiempo).
6. **Corrección automática** de preguntas objetivas (alternativas, verdadero/falso) al
   instante. Para preguntas de desarrollo/abiertas (frecuentes en Lenguaje, Historia,
   Filosofía): como no hay Profesor activo en el MVP, el alumno se autoevalúa comparando su
   respuesta contra la pauta de corrección ya escrita en el contenido (`contenido/{curso}/
   pruebas/` y `contenido/{curso}/examenes/` ya incluyen pauta completa) — se le muestra su
   respuesta junto a la pauta esperada y confirma si la considera correcta, parcial o
   incorrecta. Es una limitación conocida del modo autoestudio, coherente con no tener
   Profesor en el MVP; no se intenta corrección automática de texto libre por IA en esta
   etapa (evita falsos positivos/negativos en algo que afecta la nota).
7. **Pantalla de resultado final**:
   - Puntaje (preguntas correctas / total) y **nota** calculada (ver fórmula abajo).
   - Desglose "lo bueno y lo malo": qué OA dominó (todas o casi todas correctas) y cuáles
     debe reforzar (con link directo a la guía de ese OA).
   - Para examen simulacro Régimen A (integrado): desglose adicional por asignatura, ya que
     mezcla las 4 en una sola prueba.
   - Tiempo usado vs. tiempo disponible.
   - Se guarda como `IntentoEvaluacion` (ver `11-especificacion-mvp-para-desarrollo.md`).

## Autoevaluación por OA (sin nota, distinta de lo anterior)

Mismo mecanismo de navegación pregunta a pregunta, pero:
- Sin cronómetro bloqueante.
- Feedback inmediato después de cada respuesta (correcto/incorrecto + explicación), no al
  final — es para aprender mientras se practica, no para medir.
- No genera una "nota" formal, aunque sí queda registrado como actividad (Fase 1.2, para el
  historial).

## Cálculo de la nota (escala chilena 1.0–7.0, exigencia 60%)

Se usa la fórmula estándar del sistema escolar chileno (la misma lógica que ya se usó en
algunas pautas de corrección del contenido ya escrito, ej. Régimen C con "exigencia de
referencia 60%"), para que la nota se sienta familiar y comparable a lo que un apoderado
chileno ya conoce:

```
puntaje_total       = suma de puntos posibles de la evaluación (o N° de preguntas, si cada
                       una vale 1 punto)
puntaje_aprobacion  = puntaje_total × 0.60   (el 60% de exigencia estándar)

si puntaje_obtenido <= puntaje_aprobacion:
    nota = 1.0 + 3.0 × (puntaje_obtenido / puntaje_aprobacion)
si puntaje_obtenido > puntaje_aprobacion:
    nota = 4.0 + 3.0 × ((puntaje_obtenido - puntaje_aprobacion) / (puntaje_total - puntaje_aprobacion))

nota final = redondeada a 1 decimal, rango [1.0, 7.0], aprueba con nota >= 4.0
```

## Notas por materia y señal real de preparación (Fase 1.2)

- La **nota de una asignatura** se calcula agregando las notas de las pruebas de unidad
  rendidas en esa asignatura (ej. promedio, o la más reciente por eje — a definir en diseño
  de detalle, no bloquea el modelo de datos).
- Esta nota es **una señal de práctica**, útil para que el alumno y el apoderado vean avance,
  pero se le debe dejar explícito en la UI que **no es garantía de aprobar el examen real**.
- El **examen simulacro** es la señal fuerte: como imita exactamente el formato/duración/
  cantidad de preguntas del examen real de Mineduc (ver `08-diseno-pruebas-vs-examenes.md`),
  su resultado es la mejor estimación disponible de si el alumno realmente está preparado.
  La UI debe distinguir visualmente "notas de práctica" (pruebas de unidad) de "resultado de
  simulacro" — por ejemplo, con una etiqueta o color distinto, y un mensaje del tipo "esta es
  tu mejor referencia de cómo te iría en el examen real".

## Fuera de alcance de esta especificación (no bloquea la Fase 1.1)

- Corrección automática por IA de respuestas de desarrollo — se usa autocorrección guiada
  con pauta (ver arriba).
- Ponderación distinta entre preguntas fáciles/difíciles en el cálculo de nota — en el MVP
  todas las preguntas valen igual (1 punto), simple y transparente.
