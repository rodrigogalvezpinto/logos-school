# Plan Maestro y Registro de Avance: Auditoría y Pruebas Reales de los 12 Cursos

**Última actualización:** 2026-10-19  
**Objetivo:** Probar el 100% de los 12 cursos de Logos School mediante pruebas automatizadas End-to-End con Playwright, validando cada sección de la aplicación con alumnos y apoderados reales, completando estudios y rindiendo evaluaciones en vivo.

---

## 📋 Protocolo de Prueba por Curso (100% de Cobertura Funcional)

Cada curso es sometido a una suite Playwright serial que ejecuta los siguientes 7 pasos:

1. **Registro y Onboarding de la Familia:**
   - Creación de cuenta de Apoderado con email único.
   - Enrolamiento del Alumno con su fecha de nacimiento y **RUT chileno válido** (Módulo 11).
   - Asignación del **Nivel oficial** en el desplegable (`1° básico` hasta `4° medio`).
   - Activación de prueba gratuita de 5 días en `/seleccion-plan`.
2. **Supervisión del Apoderado:**
   - Verificación de tarjeta del alumno en `/apoderado/inicio` con estado *Plan activo*.
   - Verificación de navegación a `/apoderado/plan`, `/apoderado/estadisticas` y `/apoderado/configuracion`.
3. **Inicio del Alumno y Asignaturas Oficiales:**
   - Saludo personalizado en `/alumno/inicio`.
   - Resolución del modal de **check-in emocional diario**.
   - Verificación de las **asignaturas oficiales** correspondientes al decreto del nivel en `/alumno/asignaturas`.
4. **Estudio Pedagógico y Autoevaluación:**
   - Ingreso a asignaturas clave y revisión de Objetivos de Aprendizaje (OA).
   - Lectura de guía de estudio en `/alumno/estudiar/:oaId` (HTML estructurado, sin markdown crudo, botón `🔊 Escuchar`, enlace `⬇ Descargar guía en PDF`).
   - Calificación interactiva de la guía (1 a 5 estrellas).
   - Autoevaluación en `/alumno/autoevaluacion/:oaId` soportando preguntas de alternativas y de desarrollo.
5. **Rendición de Prueba de Unidad:**
   - Navegación a `/alumno/evaluaciones`.
   - Rendición de intento, guardado de respuestas y entrega.
   - Validación de la **nota calculada en escala 1.0 - 7.0** por el backend y tabla de resultados.
6. **Rendición de Examen Simulacro:**
   - Inicio en `/examen/:id` con cronómetro activo.
   - Verificación del formato oficial de preguntas (Régimen A: 20 preguntas / Régimen B y C: 25 preguntas).
   - Entrega del examen y cálculo de nota oficial.
7. **Plan de Estudio, Historial de Notas y Gamificación:**
   - Consulta de horario semanal en `/alumno/plan-estudio`.
   - Verificación de notas y proyección en `/alumno/notas`.
   - Verificación de acumulación de XP y cambio de avatar en `/alumno/logros`.
   - Carga de Plan Lector (`/alumno/plan-lector`) y Útiles Escolares (`/alumno/utiles-escolares`).

---

## 📊 Matriz de Avance de los 12 Cursos

| # | Curso | Régimen | Decreto | Asignaturas | Formato Examen | Archivo de Prueba Playwright | Tests | Estado |
|---|---|---|---|---|---|---|---|---|
| 1 | **1° Básico** | A | 439/2012 | 4 | Integrado (20 preg.) | `e2e/flujo-completo-1-basico.spec.ts` | 7/7 | ✅ **COMPLETO** |
| 2 | **2° Básico** | A | 439/2012 | 4 | Integrado (20 preg.) | `e2e/flujo-completo-2-basico.spec.ts` | 7/7 | ✅ **COMPLETO** |
| 3 | **3° Básico** | A | 439/2012 | 4 | Integrado (20 preg.) | `e2e/flujo-completo-3-basico.spec.ts` | 7/7 | ✅ **COMPLETO** |
| 4 | **4° Básico** | A | 439/2012 | 4 | Integrado (20 preg.) | `e2e/flujo-completo-4-basico.spec.ts` | 7/7 | ✅ **COMPLETO** |
| 5 | **5° Básico** | B | 439/2012 | 5 (+Inglés) | Separado (25 preg.) | `e2e/flujo-completo-5-basico.spec.ts` | 7/7 | ✅ **COMPLETO** |
| 6 | **6° Básico** | B | 439/2012 | 5 (+Inglés) | Separado (25 preg.) | `e2e/flujo-completo-6-basico.spec.ts` | 7/7 | ✅ **COMPLETO** |
| 7 | **7° Básico** | B | 614/2013 | 5 (Lengua y Lit.) | Separado (25 preg.) | `e2e/flujo-completo-7-basico.spec.ts` | - | ⏳ **EN CURSO** |
| 8 | **8° Básico** | B | 614/2013 | 5 (Lengua y Lit.) | Separado (25 preg.) | `e2e/flujo-completo-8-basico.spec.ts` | - | ⏳ PENDIENTE |
| 9 | **1° Medio** | B | 614/2013 | 5 (Lengua y Lit.) | Separado (25 preg.) | `e2e/flujo-real-primero-medio.spec.ts` | 5/5 | ✅ **COMPLETO** |
| 10 | **2° Medio** | B | 614/2013 | 5 (Lengua y Lit.) | Separado (25 preg.) | `e2e/flujo-completo-2-medio.spec.ts` | - | ⏳ PENDIENTE |
| 11 | **3° Medio** | C | 193/2019 | 6 (Ciencias Ciudad.) | Separado (25 preg.) | `e2e/flujo-completo-3-medio.spec.ts` | - | ⏳ PENDIENTE |
| 12 | **4° Medio** | C | 193/2019 | 6 (Ciencias Ciudad.) | Separado (25 preg.) | `e2e/flujo-completo-4-medio.spec.ts` | - | ⏳ PENDIENTE |

---

## 📌 Progreso Global
- **Régimen A (1° a 4° Básico):** 4 / 4 Cursos ✅ **100% COMPLETADO**
- **Régimen B Básica (5° y 6° Básico):** 2 / 2 Cursos ✅ **100% COMPLETADO**
- **Cursos Completados en Total:** 7 / 12 (1° Básico, 2° Básico, 3° Básico, 4° Básico, 5° Básico, 6° Básico, 1° Medio)
- **Tests Playwright Ejecutados y Pasados:** 47 / 47 tests (100% pasando)
- **Tiempo de ejecución global acumulado:** ~1m 23s

---

## 🔄 Instrucciones de Reanudación (Si se agota el contexto o tokens)

1. Verificar el último commit en git: `git log -n 5 --oneline`.
2. Consultar la tabla de arriba en este archivo (`QA/PLAN-Y-AVANCE-12-CURSOS.md`) para ver cuál es el curso que está marcado como **EN CURSO** o siguiente **PENDIENTE**.
3. Tomar como plantilla `frontend/e2e/flujo-completo-1-basico.spec.ts` o `flujo-completo-2-basico.spec.ts` adaptando:
   - Nombre de nivel en `select[name=nivelId]` (ej. `3° básico`, `4° básico`, etc.).
   - Asignaturas oficiales según el Régimen (A: 4 asignaturas; B: 5 asignaturas; C: 6 asignaturas).
   - Tipo de examen (Integrado 20 preguntas o Separado 25 preguntas).
4. Ejecutar la prueba con:
   `npx playwright test e2e/<nombre-del-archivo>.spec.ts --project=chromium`
5. Actualizar la tabla en este archivo marcando el curso como ✅ **COMPLETO**.
6. Hacer commit y push a GitHub.
