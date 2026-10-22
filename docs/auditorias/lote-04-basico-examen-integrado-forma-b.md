# Lote de auditoría — 4.º básico, examen integrado Forma B

**Fecha:** 21 de octubre de 2026  
**Archivo revisado:** `contenido/04-basico/examenes/examen-integrado-forma-b.md`  
**Rama:** `qa/fase-2-matriz-trazabilidad`  
**Tipo de revisión de este lote:** coherencia documental de la clave de corrección frente a las alternativas, con lectura de las 20 entradas de la pauta.  
**Estado:** revisión parcial; no equivale a aprobación pedagógica ni curricular.

## Alcance y criterio

Se contrastó la tabla «Pauta de corrección — Forma B» (20 preguntas) con el enunciado y las alternativas disponibles en el mismo archivo. Se comprobó si la letra y el valor/contenido que indica la clave coinciden con la alternativa señalada. La revisión de esta tabla no certifica por sí sola la validez disciplinar de cada pregunta, la alineación curricular, el nivel de dificultad, ni la experiencia de render/importación de la app.

## Resultado

| Control | Resultado |
|---|---|
| Preguntas listadas en la pauta | 20 |
| Discrepancia letra-respuesta reproducida | 1 |
| Otras entradas de la pauta | Pendientes de revisión disciplinar independiente; no declaradas aprobadas por ausencia de discrepancia automática |
| Render e importación en app | No verificados en este lote |

## Hallazgo confirmado

### LGS-4B-EVAL-001 — Pregunta 16: letra de clave incompatible con la alternativa

- **Enunciado:** «Si x + 9 = 23, ¿cuál es el valor de x?»
- **Alternativas del archivo:** a) 32; b) 14; c) 13; d) 15.
- **Pauta de corrección, fila 16:** `c) 14`.
- **Comprobación:** (23 - 9 = 14). El valor correcto es 14 y está en la alternativa **b)**; la alternativa **c)** contiene 13.
- **Impacto:** una corrección automática basada en la letra podría marcar como incorrecta una respuesta correcta o validar una incorrecta. Clasificación provisional P1.
- **Estado:** confirmado documentalmente y detectado por el validador automático. No corregido en este lote.
- **Corrección propuesta para aprobación:** cambiar únicamente la letra de la pauta de `c) 14` a `b) 14`. Antes de editar el material, confirmar aprobación del responsable y añadir/verificar regresión.

## Matriz de cobertura del lote

| Preguntas | Revisión en este lote | Estado |
|---|---|---|
| 1–15 | Contrastadas como parte de la lectura de la pauta; no se ha completado una validación independiente de contenido y currículo para cada una | Revisión disciplinar pendiente |
| 16 | Letra de clave no coincide con la alternativa que contiene el resultado correcto | Hallazgo confirmado P1 |
| 17–20 | Contrastadas como parte de la lectura de la pauta; no se ha completado una validación independiente de contenido y currículo para cada una | Revisión disciplinar pendiente |

## Próximas comprobaciones necesarias

1. Aprobar y aplicar la corrección de la letra de la clave, sin alterar el enunciado ni las alternativas.
2. Añadir una prueba de regresión que compruebe que la pregunta 16 tiene como clave la alternativa b) y que su valor es 14.
3. Ejecutar el validador y la suite del workflow.
4. Revisar de manera independiente el contenido disciplinar de las 20 preguntas, sus OA declarados, ambigüedades, distractores y nivel de 4.º básico.
5. Inspeccionar el render e importación del examen en el entorno QA.

**Conclusión del lote:** se ha reproducido una discrepancia concreta de clave-respuesta. El examen no debe marcarse como auditado integralmente ni como aprobado hasta completar los pasos anteriores y las revisiones pendientes.
