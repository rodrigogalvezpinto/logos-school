# 02 — Hallazgos Consolidados de Auditoría
**Fecha:** 21 de octubre de 2026  
**Alcance:** Evaluación técnica, pedagógica y de interfaz de usuario en Logos School.

---

## 1. Clasificación de Severidad

Los hallazgos se clasifican en cuatro niveles de impacto:
- 🔴 **Crítica (P0):** Bloquea la experiencia del alumno, falsea calificaciones o rompe la lógica de evaluación.
- 🟠 **Alta (P1):** Afecta la comprensión pedagógica, confunde severamente al estudiante o presenta contenido desordenado/ilegible.
- 🟡 **Media (P2):** Deficiencias funcionales de UX que omiten advertencias relevantes o información contextual clave.
- 🟢 **Baja / Editorial (P3):** Ajustes de redacción, notas internas filtradas o mejoras estéticas no bloqueantes.

---

## 2. Matriz de Hallazgos Consolidados

| ID | Área | Tipo | Severidad | Ubicación | Estado |
|---|---|---|---|---|---|
| **MAT-UI-001** | Software / Runner | Falso negativo en evaluación | 🔴 **Crítica** | `frontend/src/app/shared/evaluacion-runner/evaluacion-runner.ts` (l. 355) | Confirmado |
| **UX-001** | UI / Runner | Feedback automático (auto-spoil) | 🔴 **Crítica** | `frontend/src/app/shared/evaluacion-runner/evaluacion-runner.ts` (l. 120) | Confirmado |
| **CONT-001** | Contenido / Parser | Contaminación de pregunta con poema | 🟠 **Alta** | `contenido/06-basico/examenes/lenguaje-y-comunicacion-examen-forma-b.md` (l. 56) y DB `pregunta` id=2394 | Confirmado |
| **PARSER-001** | Parser / Ingesta | Pregunta clasificada como alternativa sin opciones | 🟠 **Alta** | `backend/scripts/parser_contenido.py` (l. 91) y `contenido/04-medio/matematica.md` (l. 134) | Confirmado |
| **UX-002** | UI / Runner | Omisión de aviso de preguntas marcadas al entregar | 🟡 **Media** | `frontend/src/app/shared/evaluacion-runner/evaluacion-runner.ts` (l. 413) | Confirmado |
| **UX-003** | UI / Renderizado | Enunciados extensos sin formato Markdown | 🟡 **Media** | `frontend/src/app/shared/evaluacion-runner/evaluacion-runner.ts` (l. 80) | Confirmado |
| **UX-004** | UI / Identidad | Ausencia del curso junto al nombre del alumno | 🟡 **Media** | `frontend/src/app/layout/shell/shell.ts` y `topbar.ts` | Confirmado |
| **MAT-CONT-003** | Contenido Matemática | Convención de varianza no explicitada | 🟡 **Media** | `contenido/03-medio/matematica.md` (l. 412, 436) | Confirmado |
| **MAT-CONT-001** | Contenido Matemática | División con reparto discreto sin explicitar resto | 🟢 **Baja** | `contenido/06-basico/matematica.md` (l. 77) | Confirmado |
| **MAT-CONT-002** | Contenido Matemática | Nota de borrador interno en respuesta esperada | 🟢 **Baja** | `contenido/06-basico/matematica.md` (l. 152) | Confirmado |
| **BRAND-001** | UI / Branding | Logo genérico en SVG sin asset corporativo | 🟢 **Baja** | `frontend/src/app/shared/logo/logo.ts` | Confirmado |

---

## 3. Fichas de Detalle por Hallazgo

### MAT-UI-001 — Evaluación literal de respuestas abiertas
- **Ubicación:** `frontend/src/app/shared/evaluacion-runner/evaluacion-runner.ts`, función `esCorrectaEnAutoevaluacion()`:
  ```typescript
  esCorrectaEnAutoevaluacion(p: PreguntaRunner): boolean {
    const dada = (this.respuestas()[p.id] || '').trim().toLowerCase();
    return dada === (p.respuesta_correcta || '').trim().toLowerCase();
  }
  ```
- **Evidencia empírica:** En Matemática existen **509 preguntas de desarrollo (59.4% del total)**. Cuando el alumno escribe su respuesta en el `<textarea>`, el sistema compara su texto contra párrafos extensos de la clave. Salvo que el alumno adivine el texto del redactor con exactitud milimétrica de caracteres, el método evalúa a `false` y rotula en rojo: *"Respuesta esperada: ..."*.
- **Impacto:** Genera frustración masiva, califica erróneamente respuestas matemáticamente válidas y rompe la autoevaluación.
- **Acción requerida:** Desacoplar las preguntas de desarrollo de la validación booleana de acierto. En preguntas abiertas, presentar una **solución orientativa / rúbrica formativa** para que el estudiante contraste su propio razonamiento.

---

### UX-001 — Revelación prematura de respuestas en práctica (Auto-spoil)
- **Ubicación:** `frontend/src/app/shared/evaluacion-runner/evaluacion-runner.ts`, línea 120:
  ```html
  @if (modo === 'autoevaluacion' && respuestas()[preguntaActual.id]) {
    <div class="feedback">...</div>
  }
  ```
- **Evidencia empírica:** Captura de pantalla 1 aportada por el usuario en `/alumno/autoevaluacion/165`. Tan pronto como se selecciona un radio button, el bloque verde de retroalimentación se despliega de inmediato debajo de la opción, delatando si era o no la alternativa correcta.
- **Impacto:** Invalida el valor formativo de la práctica. El estudiante no tiene oportunidad de repensar, dudar ni ensayar otras respuestas.
- **Acción requerida:** El feedback debe mostrarse **únicamente bajo demanda** mediante un botón interactivo: `💡 Comprobar respuesta / Ver ayuda`.

---

### CONT-001 — Contaminación del enunciado en OA 165 con poema Texto 3
- **Ubicación:**
  - Archivo fuente: `contenido/06-basico/examenes/lenguaje-y-comunicacion-examen-forma-b.md`, líneas 56 a 75.
  - Base de datos `logos_qa`: Tabla `pregunta`, registro `id = 2394`, vinculado a `oa_id = 165`.
- **Evidencia empírica:** Captura de pantalla 2 del usuario. El enunciado de la pregunta 4 muestra:
  `Da tu opinión fundamentada... --- ## Texto 3 (para las preguntas 5 a 8) ### Poema: "Tren nocturno hacia el sur" > Estrofa 1...`
- **Mecanismo del defecto:** En `parser_prueba_examen.py`, el extractor divide el archivo buscando el patrón `**N. (Tipo)**`. Entre la pregunta 4 y la pregunta 5 existía un bloque de lectura intercalado (`## Texto 3...`). El parser absorbió todo ese texto dentro del cuerpo de la pregunta 4.
- **Impacto:** Enorme bloque de texto desordenado e ilegible en la pregunta 4, y pérdida del poema en las preguntas 5 a 8 que dependían de él.
- **Acción requerida:** Limpiar el campo `enunciado` del registro 2394 en la base de datos para contener únicamente la instrucción de la pregunta 4, y ajustar el parser para que los textos de lectura contextuales no contaminen preguntas adyacentes.

---

### PARSER-001 — Pregunta clasificada como alternativa con 0 opciones
- **Ubicación:** `backend/scripts/parser_contenido.py`, función `_clasificar_tipo()`:
  ```python
  def _clasificar_tipo(etiqueta: str) -> str:
      et = etiqueta.lower()
      if "verdadero" in et: return "verdadero_falso"
      if "alternativas" in et: return "alternativas"
      return "desarrollo_breve"
  ```
  En `contenido/04-medio/matematica.md`, línea 134:
  `**Pregunta 10 (desarrollo — evaluar alternativas de ahorro).**`
- **Evidencia empírica:** El script `inventario_matematica.py` detectó `[4° medio - OA 1 # 10] Pregunta de alternativas con 0 opciones`. Como el autor escribió la frase *"alternativas de ahorro"* en la descripción del ejercicio, el parser la rotuló como `alternativas`, pero al no tener opciones `a), b), c)`, quedó con `opciones = null`.
- **Impacto:** En el frontend, el runner intenta renderizar alternativas que no existen o cae a un textarea inconsistente con el tipo de pregunta en backend.
- **Acción requerida:** En `parser_contenido.py`, una pregunta solo puede tener `tipo = "alternativas"` si efectivamente se parseó una lista de opciones (`opciones is not None and len(opciones) >= 2`). Si no hay opciones, debe asignarse a `desarrollo_breve`.

---

### UX-002 — Modal de entrega no advierte de preguntas marcadas para revisar
- **Ubicación:** `frontend/src/app/shared/evaluacion-runner/evaluacion-runner.ts`, línea 413 (`intentarEnviar()`):
  ```typescript
  intentarEnviar() {
    if (this.faltantes().length > 0) {
      this.mostrarAvisoIncompleto.set(true);
    } else {
      this.confirmarEnvio();
    }
  }
  ```
- **Evidencia empírica:** Captura 3 del usuario. El modal alerta: *"Te falta responder 3 preguntas. Preguntas 6, 7, 9 — si envías ahora, quedarán en blanco"*. Sin embargo, el set `marcadas()` (`[x] Marcar para revisar después`) es completamente ignorado. Si un alumno contestó todo pero dejó 4 preguntas marcadas con bandera para revisar con calma, el examen se entrega directamente sin alertar.
- **Acción requerida:** Evaluar `marcadas().size`. Si existen preguntas marcadas, alertar en el modal: *"Tienes X preguntas marcadas para revisar (Preguntas: ...) y Y sin responder"*, permitiendo navegar directamente a ellas con un clic.

---

### UX-003 — Enunciados extensos sin formateo de párrafos (Markdown)
- **Ubicación:** `frontend/src/app/shared/evaluacion-runner/evaluacion-runner.ts`, línea 80:
  `<p class="pregunta__enunciado">{{ preguntaActual.enunciado }}</p>`
- **Evidencia empírica:** El enunciado se inyecta por interpolación directa de texto (`{{ ... }}`). Los saltos de línea se ignoran o se aplanan en una sola línea continua, los poemas pierden sus versos y estrofas, y las listas pierden sus viñetas.
- **Acción requerida:** Aplicar `MarkdownPipe` existente (`[innerHTML]="preguntaActual.enunciado | markdown"`) con sanitización de Angular para preservar párrafos, versos, estrofas y negritas.

---

### UX-004 — Ausencia del curso junto al nombre del estudiante
- **Ubicación:** `frontend/src/app/layout/shell/shell.ts` (l. 80), `topbar.ts`, `alumno-inicio.ts`.
- **Evidencia empírica:** El modelo `PerfilAlumnoActivo` en frontend contiene `{ id, nombre, apellidos, nivel_id }`. No contiene `nombre_nivel`. En la barra superior solo aparece `"Sofía"`, y en la pantalla de bienvenida `"¡Hola de nuevo, Sofía! 👋"`, sin indicar si está cursando 4° básico o 6° básico.
- **Acción requerida:** Incorporar `nombre_nivel` en el contrato de API `PerfilAlumnoRespuesta` y renderizar `Sofía · 4° Básico` en Topbar, Inicio, Selector de Perfiles y Panel Parental.

---

### MAT-CONT-003 — Convención de varianza poblacional vs muestral en 3° Medio
- **Ubicación:** `contenido/03-medio/matematica.md`, líneas 412 y 436 (OA 2).
- **Evidencia:** Ejercicio `{2, 4, 6}` con solución $\text{Var} = \frac{8}{3} \approx 2,67$, y ejercicio `{10, 12, 14, 16}` con $\text{Var} = \frac{20}{4} = 5$. Ambas dividen por $N$ (varianza poblacional).
- **Evaluación curricular:** El currículum oficial de Educación Media del MINEDUC define varianza dividiendo por $N$. Sin embargo, en estadística universitaria o pruebas electivas se utiliza $N-1$ (muestral).
- **Acción requerida:** Agregar una nota explícita en la síntesis conceptual de la guía: *"En este nivel utilizamos la varianza poblacional, promediando las desviaciones cuadráticas entre el total de datos $N$"*.

---

### MAT-CONT-001 — Reparto de 24.600 botellas en 6° Básico (Resto de 1 caja)
- **Ubicación:** `contenido/06-basico/matematica.md`, línea 77 (OA 2).
- **Evidencia:** Problema de 24.600 botellas en cajas de 12 para 3 distribuidores. La alternativa correcta (`b: División, luego división`) es 100% correcta. En la retroalimentación se indica `2.050 ÷ 3 ≈ 683 cajas cada uno`.
- **Evaluación:** Como $2.050 = 3 \times 683 + 1$, queda 1 caja sin repartir.
- **Acción requerida:** Precisar en la retroalimentación: `(2.050 ÷ 3 = 683 cajas para cada distribuidor y sobra 1 caja)`.

---

### MAT-CONT-002 — Nota interna editorial en respuesta de razón 5:3 en 6° Básico
- **Ubicación:** `contenido/06-basico/matematica.md`, línea 152 (OA 3).
- **Evidencia:** `Respuesta esperada: 15 ÷ 5 = 3, por lo tanto 3×3 : 5×3... cuidado con el orden: 5:3 amplificado por 3 es 15:9. Hay 9 libros de ciencia.`
- **Evaluación:** El cálculo final (9 libros) es matemáticamente exacto. La frase `... cuidado con el orden:` es una nota de borrador de autoría que quedó incrustada en la clave.
- **Acción requerida:** Limpiar la respuesta esperada: `15 ÷ 5 = 3 (factor de escala); la razón 5:3 amplificada por 3 es 15:9. Hay 9 libros de ciencia.`

---

### BRAND-001 — Logo corporativo genérico en código
- **Ubicación:** `frontend/src/app/shared/logo/logo.ts`.
- **Evidencia:** SVG codificado manualmente en el template. No existe carpeta `assets/` ni archivo de imagen oficial de Logos School.
- **Acción requerida:** Proveer un slot de carga para `assets/branding/logo.svg` (o PNG) con fallback visual automático si el recurso no está presente.
