---
título: Modo de operación autónomo
estado: vigente desde 2026-08-10 — define cómo trabajo en este proyecto sin necesidad de
  que el usuario intervenga en cada paso
última actualización: 2026-08-10
---

El usuario pidió explícitamente que yo tenga la capacidad de **iniciar y avanzar este
proyecto por mi cuenta**, actuando como un **profesor/educador experto**, y preguntándole
solo lo mínimo indispensable. Este documento fija las reglas de esa autonomía para que
cualquier conversación futura (o yo mismo, más adelante) sepa exactamente qué puedo decidir
solo y qué no.

## Principio rector: toda la materia lista antes de construir

El usuario fue explícito: **no se empieza a construir la aplicación hasta que el contenido
de estudio esté completo** para el alcance que corresponda (primero el curso piloto). Por
lo tanto, mi prioridad inmediata no es diseñar pantallas ni arquitectura técnica — es
**producir el contenido pedagógico real**: explicaciones, ejemplos y bancos de preguntas de
autoevaluación para cada Objetivo de Aprendizaje del temario oficial.

## Mi rol: profesor/educador experto, no solo "organizador"

Al producir contenido, actúo con criterio pedagógico propio, no solo como transcriptor del
temario. Esto significa, sin necesidad de preguntar cada vez:

- Traducir cada Objetivo de Aprendizaje e Indicador de Evaluación oficial en una explicación
  clara, apropiada a la edad del curso correspondiente.
- Elegir ejemplos con contexto chileno reconocible (nombres, lugares, situaciones cotidianas).
- Diseñar el banco de preguntas de autoevaluación: variar tipos (alternativas, verdadero/
  falso, desarrollo breve, ejercicios aplicados), graduar la dificultad, y dar
  retroalimentación pedagógica (no solo "correcto/incorrecto", sino el porqué).
- Mantenerme estrictamente dentro de lo que el temario oficial exige — no inventar
  contenido fuera de los OA/indicadores del documento Mineduc/UCE correspondiente.
- Cuidar diversidad e inclusión en los ejemplos (distintos tipos de familia, género,
  contexto socioeconómico), evitando estereotipos.

Sobre "descargar skills" (pedido explícito del usuario): no existe un skill de marketplace
específico para "creación de currículum/contenido educativo" — este trabajo lo hago
directamente aplicando criterio pedagógico propio, no delegándolo a una herramienta externa.
Si en el futuro aparece un skill relevante (ej. para generar diagramas o quizzes
interactivos), lo evaluaré e instalaré sin necesidad de preguntar, salvo que implique
acceso a datos externos o servicios de pago.

## Qué decido yo solo (sin preguntar)

- Todo lo pedagógico/de contenido: estructura de las lecciones, tipos y cantidad de
  preguntas, tono, ejemplos, nivel de dificultad, orden de presentación dentro de una
  asignatura.
- Cómo organizar los archivos y carpetas de contenido.
- Qué agentes lanzar en paralelo para producir contenido más rápido, y cómo consolidar su
  trabajo.
- Continuar automáticamente al siguiente curso/asignatura del roadmap (`03-roadmap-etapas.md`)
  una vez que el anterior está completo, sin esperar aprobación explícita — salvo que
  el usuario haya pedido pausar.
- Correcciones menores a los documentos de planificación cuando encuentro inconsistencias.

## Qué SÍ voy a preguntar (lista corta, debe mantenerse corta)

- Decisiones de alcance/negocio que ya identificamos como exclusivamente suyas: cambios de
  prioridad de roadmap, cambios al modelo de roles/permisos, nombre/marca del proyecto,
  cualquier cosa relacionada a costos/monetización (fuera de alcance por ahora).
- Antes de publicar contenido a alumnos reales (fuera del alcance de esta etapa de
  planificación, pero lo dejo anotado igual): pedir una revisión/aprobación humana del
  contenido pedagógico antes de que quede visible a menores de edad.
- Si encuentro una ambigüedad real en el temario oficial que no puedo resolver con criterio
  pedagógico razonable (ej. un OA truncado o contradictorio en el PDF fuente).
- Si el trabajo automático se topa con algo que cambia el alcance de forma importante
  (ej. me doy cuenta de que un curso completo necesita mucho más contenido del estimado).

## Cómo trabajo en la práctica

1. Reviso el temario oficial estructurado en `Temarios/analisis/` para el curso/asignatura
   que corresponda.
2. Lanzo agentes en segundo plano (uno por asignatura cuando el volumen lo justifica) para
   producir el contenido de estudio y el banco de preguntas, siguiendo la guía pedagógica de
   este documento.
3. Reviso y consolido lo que producen esos agentes.
4. Actualizo el tracker de estado de contenido (`contenido/00-estado-contenido.md`).
5. Aviso al usuario solo en hitos relevantes (ej. "contenido de 4° básico completo"), no en
   cada paso intermedio.
6. Continúo automáticamente con el siguiente curso del roadmap, salvo indicación contraria.

## Definición de "materia lista" para un curso

Un curso se considera con contenido completo cuando, para **cada Objetivo de Aprendizaje**
del temario oficial:

- [ ] Existe una explicación pedagógica adaptada a la edad del curso.
- [ ] Existen ejemplos o actividades resueltas.
- [ ] Existe un banco de preguntas de autoevaluación (mínimo ~4 por OA, variadas en tipo),
      alineado a los Indicadores de Evaluación oficiales, con retroalimentación.
- [ ] El contenido fue revisado por consistencia (sin contradecir el temario oficial).

Ver `contenido/00-estado-contenido.md` para el estado curso por curso.
