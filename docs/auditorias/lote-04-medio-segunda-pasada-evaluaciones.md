# Segunda pasada — evaluaciones de 4.º medio (Forma B)

**Rama:** `qa/fase-2-matriz-trazabilidad`  
**Alcance:** revisión estructural de las seis evaluaciones Forma B disponibles en `contenido/04-medio/examenes/`. Se contrastaron metadatos, distribución declarada, puntajes y pautas visibles. No se modificaron exámenes ni se compararon exhaustivamente todos los enunciados con Forma A.

## Hallazgos

### LGS-4M-EVAL-001 — Puntajes de Ciencias para la Ciudadanía: suma declarada consistente
- **Estado:** verificado sin discrepancia en la suma.
- **Archivo:** `ciencias-para-la-ciudadania-examen-forma-b.md`.
- **Evidencia:** 7 preguntas de alternativas × 1 punto = 7; 4 de verdadero/falso × 1 = 4; 7 de desarrollo breve × 2 = 14; 7 de desarrollo extenso × 3 = 21.
- **Comprobación:** 7 + 4 + 14 + 21 = **46 puntos**, coincidente con el total declarado. La distribución suma 25 preguntas.
- **Acción:** conservar como control positivo; verificar igualmente la pauta completa al automatizar la auditoría.

### LGS-4M-EVAL-002 — Puntaje de Filosofía: suma declarada consistente
- **Estado:** verificado sin discrepancia en la suma.
- **Archivo:** `filosofia-examen-forma-b.md`.
- **Evidencia:** la tabla declara 16 puntos de selección múltiple, 15 puntos de desarrollo breve y 20 puntos de desarrollo extenso.
- **Comprobación:** 16 + 15 + 20 = **51 puntos**, coincidente con el total declarado. La distribución indicada corresponde a 25 preguntas.
- **Acción:** mantener la tabla de puntajes sincronizada con cada criterio de corrección si se edita el examen.

### LGS-4M-EVAL-003 — Inglés: aclarar el criterio de puntaje para formatos heterogéneos
- **Severidad provisional:** P2 (transparencia de evaluación).
- **Archivo:** `ingles-examen-forma-b.md`.
- **Evidencia:** las instrucciones dicen que todas las preguntas valen el mismo puntaje, mientras que el examen combina alternativas, completar, emparejar, verdadero/falso, producción breve y respuestas en inglés.
- **Evaluación:** no es necesariamente un error que todas las preguntas valgan lo mismo, pero la pauta debe dejar claro cómo se asigna el punto en respuestas abiertas y producciones, incluidos errores parciales de gramática, contenido y comprensión.
- **Recomendación:** agregar una rúbrica breve o una regla explícita de crédito parcial y aceptación de respuestas equivalentes; verificar que la suma de claves y puntos sea consistente con las instrucciones.

### LGS-4M-EVAL-004 — Matemática: comprobar la pauta de las preguntas de desarrollo
- **Severidad provisional:** P2 (verificación pendiente, no error confirmado).
- **Archivo:** `matematica-examen-forma-b.md`.
- **Evidencia:** declara 25 preguntas, con 12 de alternativas y 13 de desarrollo; la pregunta 21 pide calcular la probabilidad binomial de obtener exactamente 6 aciertos en 8 intentos con p = 0,5.
- **Evaluación:** el enunciado define los datos necesarios. Para certificar el examen falta comprobar, en toda la pauta, la corrección de cada resultado, el puntaje asignado a los pasos y la suma máxima de puntos.
- **Recomendación:** calcular de forma independiente cada respuesta numérica y contrastar la tabla OA/puntaje con el total del examen. No inferir errores por ausencia de un total en el extracto revisado.

### LGS-4M-EVAL-005 — Comparación de Forma A y Forma B: promesa pendiente de verificar
- **Severidad provisional:** P2 (validez y variedad de práctica).
- **Archivos:** los seis exámenes Forma B y sus referencias a Forma A.
- **Evidencia:** los encabezados de varias evaluaciones declaran que la Forma B usa preguntas distintas de la Forma A.
- **Evaluación:** esta pasada no establece por sí sola que la promesa se cumpla, porque no se realizó comparación completa pregunta por pregunta de las dos formas.
- **Recomendación:** comparar texto, cifras, estímulos, claves y estructura de cada ítem entre formas; distinguir repetición exacta de reutilización legítima de OA con escenarios distintos.

## Estado y próximos controles
**4.º medio — Forma B: segunda pasada estructural parcial documentada.** Se verificaron dos sumas de puntaje y se identificaron controles pendientes de rúbricas y validación cruzada. No se declara certificación total del examen ni de sus respuestas.
