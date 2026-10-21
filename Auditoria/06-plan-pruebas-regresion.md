# 06 — Plan de Pruebas y Matriz de Regresión
**Fecha:** 21 de octubre de 2026  
**Objetivo:** Garantizar que las correcciones de UX/UI, evaluaciones y contenido se verifiquen con criterios de aceptación objetivos y que ninguna funcionalidad existente sufra regresión.

---

## 1. Inventario de Pruebas Existentes (Línea Base: 886 / 886 en Verde)

Antes de cualquier intervención, la plataforma cuenta con una base sólida de pruebas automatizadas:
- **Backend Pytest:** 491 tests (100% pasando).
- **Frontend Unit Tests (Vitest):** 33 tests en 8 suites (100% pasando).
- **Frontend E2E (Playwright):** 362 tests en 64 archivos spec (100% pasando).

---

## 2. Nuevos Casos de Prueba Requeridos

### Suite 1: Ayuda Bajo Demanda en Autoevaluación (`evaluacion-runner.spec.ts`)
- **Caso 1.1 (Sin revelación prematura):**
  - *Acción:* El alumno selecciona una alternativa en autoevaluación.
  - *Criterio de Aceptación:* El bloque `.feedback` NO debe estar visible en el DOM. Debe mostrarse el botón `btn-ayuda-practica`.
- **Caso 1.2 (Revelación bajo demanda):**
  - *Acción:* El alumno hace clic en `btn-ayuda-practica`.
  - *Criterio de Aceptación:* El bloque `.feedback` se hace visible, indicando si la opción es correcta y mostrando la retroalimentación.
- **Caso 1.3 (Desarrollo formativo sin falso negativo):**
  - *Acción:* El alumno escribe una respuesta abierta con sus propias palabras y hace clic en `btn-ayuda-practica`.
  - *Criterio de Aceptación:* NO debe aparecer el texto de error "Incorrecto", sino la pauta orientativa de autoevaluación.
- **Caso 1.4 (Blindaje de pruebas formales):**
  - *Acción:* En `modo === 'prueba'` o `modo === 'examen'`, el alumno responde preguntas.
  - *Criterio de Aceptación:* El botón de ayuda NO existe en la pantalla. Las respuestas jamás se revelan antes de entregar.

### Suite 2: Advertencia de Preguntas Marcadas al Entregar
- **Caso 2.1 (Todas respondidas, pero 2 marcadas):**
  - *Acción:* El alumno responde el 100% de las preguntas, marca las preguntas 2 y 4 con `[x] Marcar para revisar después` y hace clic en `Finalizar intento`.
  - *Criterio de Aceptación:* Se abre el modal de advertencia indicando: *"Dejaste 2 preguntas marcadas para revisar (Preguntas 2, 4)"*. El examen NO se envía automáticamente.
- **Caso 2.2 (Navegación desde el modal a preguntas pendientes):**
  - *Acción:* En el modal, el alumno hace clic en *"Ir a revisar"*.
  - *Criterio de Aceptación:* El modal se cierra y el runner navega directamente a la pregunta 2.
- **Caso 2.3 (Combinación de preguntas en blanco y marcadas):**
  - *Acción:* El alumno deja la pregunta 6 en blanco y marca la 3 para revisar.
  - *Criterio de Aceptación:* El modal detalla ambos casos de forma clara y diferenciada.

### Suite 3: Visualización de Nombre y Curso del Estudiante
- **Caso 3.1 (Topbar del alumno):**
  - *Criterio de Aceptación:* El enlace de perfil en la barra superior muestra `Sofía` acompañado de `4° básico`.
- **Caso 3.2 (Inicio del alumno):**
  - *Criterio de Aceptación:* El saludo principal contiene el badge o texto del curso (`¡Hola de nuevo, Sofía! 👋 · 4° Básico`).
- **Caso 3.3 (Cambio de perfil):**
  - *Criterio de Aceptación:* Al cambiar al perfil de `Mateo`, la interfaz se actualiza a `6° básico`.

### Suite 4: Renderizado Markdown de Preguntas y Poemas
- **Caso 4.1 (Saltos de línea y párrafos):**
  - *Criterio de Aceptación:* Enunciados con múltiples párrafos se renderizan en etiquetas `<p>` separadas, no como una sola línea continua.
- **Caso 4.2 (Citas y versos):**
  - *Criterio de Aceptación:* Bloques que inician con `>` se renderizan con estilo de `<blockquote>` o versos indentados.
- **Caso 4.3 (Seguridad contra inyección XSS):**
  - *Criterio de Aceptación:* Etiquetas scripts o payloads HTML maliciosos son sanitizados por Angular DOMPurify/Sanitizer.

### Suite 5: Fallback y Carga del Logo
- **Caso 5.1 (Fallback automático):**
  - *Criterio de Aceptación:* Si no existe el archivo físico `assets/branding/logo.svg`, el componente renderiza el SVG vectorial por defecto sin errores en la consola.
- **Caso 5.2 (Asset presente):**
  - *Criterio de Aceptación:* Al existir el archivo de imagen oficial, se renderiza la imagen sin alterar el layout del sidebar ni del selector de perfiles.

---

## 3. Matriz de No-Regresión

Toda modificación debe revalidar las siguientes suites críticas existentes:

| Suite E2E a Revalidar | Archivo | Comprobación Clave |
|---|---|---|
| **12 Cursos Completos** | `frontend/e2e/flujo-completo-*.spec.ts` | Onboarding, estudio, prueba de unidad y examen en los 12 niveles |
| **Casos Borde** | `frontend/e2e/casos-borde.spec.ts` | Modal de confirmación y recarga de página |
| **Simulacro Parcial** | `frontend/e2e/faltantes-simulacro-parcial.spec.ts` | Desbloqueo de examen al 50% del temario |
| **Auto-envío por Tiempo** | `frontend/e2e/examen-auto-envio.spec.ts` | Entrega automática al llegar el reloj a 00:00 |
| **Accesibilidad WCAG AA** | `frontend/e2e/accesibilidad.spec.ts` | Cero violaciones de accesibilidad en axe-core |
| **Responsive Móvil** | `frontend/e2e/responsive.spec.ts` | Visualización en pantallas móviles (375x667) |
| **Pytest Backend** | `backend/tests/` | 491 tests de backend sin fallos |
| **Vitest Frontend** | `frontend/src/app/**/*.spec.ts` | 33 tests unitarios en verde |
