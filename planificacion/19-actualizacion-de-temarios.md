---
título: Qué pasa cuando Mineduc cambie los temarios (proceso de actualización de materia)
estado: decisión de proceso (2026-08-12) — no es una función dentro de la app
última actualización: 2026-08-12
---

## El problema

Los temarios oficiales de Mineduc pueden cambiar con los años (nuevos decretos, ajuste de
Objetivos de Aprendizaje, cambio de asignaturas). El usuario preguntó cómo se va a mantener
Logos al día con eso — y planteó dos caminos: construir una función dentro de la app para
cargar temarios nuevos, o simplemente hacerlo "por fuera", conversando con Claude Code como
se hizo para construir el contenido original.

## Decisión: el proceso se hace por fuera de la app, vía Claude Code — no se construye una función de "cargar temario" dentro del producto

El usuario mismo concluyó que es más simple y directo: cuando cambie un temario, se abre una
conversación de Claude Code en este mismo proyecto, se le pasa el PDF/documento del temario
nuevo, y se repite el mismo proceso ya usado para construir todo el contenido actual
(extracción estructurada → comparación contra el contenido existente → actualización de
guías/bancos de preguntas/pruebas/exámenes afectados → reimportación a la base de datos con
el mismo script de `scripts/importar_contenido.py`). No hay beneficio real en construir una
interfaz web de "subir temario" para algo que ocurre, en el mejor de los casos, una vez
cada varios años y que de todas formas requiere criterio pedagógico experto para decidir qué
cambia — exactamente lo que ya se hace en estas conversaciones.

**Esto significa que NO es una función del producto** — no hay pantalla de "actualizar
temario" en el panel de Administrador. Es un proceso operativo documentado aquí para que
quede claro cómo proceder cuando llegue el momento, y no se pierda ni se re-litigue esta
decisión.

## Cómo se hace, paso a paso, cuando corresponda

1. El usuario consigue el temario oficial actualizado (PDF de Mineduc/UCE) y lo coloca en
   `Temarios/` (reemplazando o versionando el anterior).
2. Se abre una conversación de Claude Code en este proyecto y se le pide comparar el
   temario nuevo contra `Temarios/analisis/{curso}.md` existente, para identificar
   exactamente qué OA cambiaron, se agregaron o se eliminaron.
3. Se actualiza `Temarios/analisis/{curso}.md` con el detalle nuevo.
4. Se actualiza el contenido afectado en `contenido/{curso}/` (guía, banco de preguntas,
   pruebas de unidad, exámenes simulacro) — solo lo que cambió, no se rehace todo desde
   cero si el cambio es parcial.
5. Se corre `scripts/importar_contenido.py` de nuevo para ese curso, para que la base de
   datos (ambiente Desarrollo primero, luego Producción) refleje el contenido actualizado.
6. Se documenta el cambio en `contenido/00-estado-contenido.md` con la fecha y qué cambió.

## Qué sí podría automatizarse más adelante (no ahora)

Si en el futuro esto se vuelve muy frecuente o son muchos cursos a la vez, se podría
evaluar automatizar parte del paso 2 (comparación) con un agente dedicado — pero no hay
necesidad de diseñarlo ahora, dado que los temarios de Mineduc no cambian con frecuencia y
el usuario ya prefiere el control directo vía conversación con Claude Code.
