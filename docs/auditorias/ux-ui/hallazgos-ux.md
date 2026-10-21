# Diagnóstico y Especificación de Hallazgos UX/UI
**Proyecto:** Logos School  
**Fecha:** 21 de octubre de 2026  
**Área:** Experiencia de Usuario, Accesibilidad e Interacción en Evaluaciones

---

## 1. Resumen de Hallazgos UX/UI Identificados

| Identificador | Severidad | Módulo / Componente | Descripción Resumida |
|---|:---:|---|---|
| **UX-001** / `MAT-UI-001` | **P0** | `frontend/src/app/shared/evaluacion-runner/` | Feedback instantáneo en autoevaluación (auto-spoiler) y calificación literal errónea en preguntas de desarrollo. |
| **UX-002** | **P1** | `frontend/src/app/shared/evaluacion-runner/` | Modal de entrega no advierte sobre preguntas marcadas para revisión (`marcadas()`). |
| **UX-003** | **P2** | `frontend/src/app/shared/evaluacion-runner/` | Enunciados extensos sin renderizado Markdown, fórmulas ni jerarquía visual legible. |
| **UX-004** | **P2** | `frontend/src/app/core/` / `topbar` / `inicio` | Nombre del estudiante no incluye su curso escolar asociado en la cabecera ni en el saludo. |
| **UX-005** | **P3** | `frontend/src/assets/` | Icono institucional pendiente de sustitución por el isotipo oficial de Logos. |

---

## 2. Fichas Técnicas Detalladas

### UX-001 / MAT-UI-001 — Feedback Inmediato y Autoevaluación en Preguntas de Desarrollo
- **Ubicación:** `frontend/src/app/shared/evaluacion-runner/evaluacion-runner.ts` y `.html`
- **Comportamiento Actual:**
  1. Al seleccionar una alternativa en modo práctica/autoevaluación, la interfaz revela de inmediato el veredicto (correcto/incorrecto) y la retroalimentación, impidiendo la reflexión del alumno.
  2. En preguntas de desarrollo (`p.tipo === 'desarrollo'`), el método `esCorrectaEnAutoevaluacion()` evalúa la respuesta ingresada mediante comparación de cadenas idénticas (`trim().toLowerCase()`). Esto marca como erróneas respuestas conceptualmente válidas que difieran en puntuación, sinónimos o redacción.
- **Impacto Pedagógico:** Frustración del estudiante y distorsión de la experiencia de práctica formativa.
- **Comportamiento Requerido:**
  1. La selección de una alternativa debe guardarse como estado sin revelar el resultado automáticamente.
  2. Incorporar un botón explícito de ayuda: `💡 Comprobar respuesta / Ver ayuda`. Solo al presionarlo se despliega la retroalimentación.
  3. En preguntas de desarrollo, no autocalificar con veredicto booleano de igualdad estricta; permitir al alumno escribir su desarrollo y mostrar la solución o criterios guía para que el estudiante compare su razonamiento.

---

### UX-002 — Alerta de Preguntas Marcadas para Revisión en Modal de Entrega
- **Ubicación:** `frontend/src/app/shared/evaluacion-runner/evaluacion-runner.html` y `.ts`
- **Comportamiento Actual:** El modal de confirmación antes de entregar solo comprueba `sinResponder().length`. Si el estudiante utilizó la herramienta de "Marcar para revisar" en preguntas que sí respondió o dejó pendientes, el sistema no le alerta de esta condición al hacer clic en "Entregar evaluación".
- **Impacto:** Pérdida de la utilidad de la función de marcado; el estudiante puede entregar por error sin volver a las preguntas que dejó en duda.
- **Comportamiento Requerido:** El modal debe inspeccionar la señal `marcadas()`. Si existen preguntas marcadas, debe incluir una advertencia explícita:  
  *⚠️ Tienes [X] preguntas marcadas para revisar. ¿Deseas revisarlas antes de enviar o entregar de todas formas?*

---

### UX-003 — Renderizado de Markdown y Legibilidad en Enunciados Complejos
- **Ubicación:** `frontend/src/app/shared/evaluacion-runner/evaluacion-runner.html`
- **Comportamiento Actual:** Los enunciados largos se muestran en texto crudo dentro de un bloque plano sin sangrías, viñetas, tablas ni separación visual de párrafos, generando sobrecarga cognitiva y rechazo lector.
- **Impacto:** Dificultad para comprender problemas extensos en cursos superiores (3° y 4° Medio) y problemas aritméticos con tablas o listas.
- **Comportamiento Requerido:** Implementar renderizado de Markdown (o pipe de texto estructurado) en el runner para soportar negritas, listas ordenadas, saltos de párrafo, tablas y renderizado tipográfico matemático.

---

### UX-004 — Despliegue del Curso Escolar junto al Nombre del Estudiante
- **Ubicación:**
  - `frontend/src/app/layout/topbar/topbar.component.html`
  - `frontend/src/app/features/alumno/inicio/inicio.component.html`
  - `frontend/src/app/shared/perfil-selector/perfil-selector.component.html`
- **Comportamiento Actual:** La interfaz solo muestra el primer nombre del alumno (ej. "Sofía").
- **Impacto:** En familias con múltiples hijos inscritos en diferentes niveles escolares o en sesiones compartidas, el apoderado o alumno no tiene confirmación visual inmediata del curso activo en el que se encuentra navegando.
- **Comportamiento Requerido:** Mostrar el formato compuesto: **`[Nombre] ([Curso])`** (ejemplo: `Sofía (4° Básico)`).

---

## 3. Evidencias y Recursos Visuales
- Las capturas base de los flujos de la aplicación se encuentran versionadas en `frontend/screenshots/` (ver `frontend/screenshots/05-panel-alumno.png` y `frontend/screenshots/flujo/`).
- En la Fase 2, una vez implementadas las correcciones en el runner y el layout, se generarán capturas comparativas "Antes / Después" para su archivo en `docs/auditorias/ux-ui/evidencias/`.
