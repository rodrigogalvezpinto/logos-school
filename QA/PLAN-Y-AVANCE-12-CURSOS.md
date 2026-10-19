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

## 📊 Matriz de Avance de los 12 Cursos (100% COMPLETADA)

| # | Curso | Régimen | Decreto | Asignaturas | Formato Examen | Archivo de Prueba Playwright | Tests | Estado |
|---|---|---|---|---|---|---|---|---|
| 1 | **1° Básico** | A | 439/2012 | 4 | Integrado (20 preg.) | `e2e/flujo-completo-1-basico.spec.ts` | 7/7 | ✅ **COMPLETO** |
| 2 | **2° Básico** | A | 439/2012 | 4 | Integrado (20 preg.) | `e2e/flujo-completo-2-basico.spec.ts` | 7/7 | ✅ **COMPLETO** |
| 3 | **3° Básico** | A | 439/2012 | 4 | Integrado (20 preg.) | `e2e/flujo-completo-3-basico.spec.ts` | 7/7 | ✅ **COMPLETO** |
| 4 | **4° Básico** | A | 439/2012 | 4 | Integrado (20 preg.) | `e2e/flujo-completo-4-basico.spec.ts` | 7/7 | ✅ **COMPLETO** |
| 5 | **5° Básico** | B | 439/2012 | 5 (+Inglés) | Separado (25 preg.) | `e2e/flujo-completo-5-basico.spec.ts` | 7/7 | ✅ **COMPLETO** |
| 6 | **6° Básico** | B | 439/2012 | 5 (+Inglés) | Separado (25 preg.) | `e2e/flujo-completo-6-basico.spec.ts` | 7/7 | ✅ **COMPLETO** |
| 7 | **7° Básico** | B | 614/2013 | 5 (Lengua y Lit.) | Separado (25 preg.) | `e2e/flujo-completo-7-basico.spec.ts` | 7/7 | ✅ **COMPLETO** |
| 8 | **8° Básico** | B | 614/2013 | 5 (Lengua y Lit.) | Separado (25 preg.) | `e2e/flujo-completo-8-basico.spec.ts` | 7/7 | ✅ **COMPLETO** |
| 9 | **1° Medio** | B | 614/2013 | 5 (Lengua y Lit.) | Separado (25 preg.) | `e2e/flujo-real-primero-medio.spec.ts` | 5/5 | ✅ **COMPLETO** |
| 10 | **2° Medio** | B | 614/2013 | 5 (Lengua y Lit.) | Separado (25 preg.) | `e2e/flujo-completo-2-medio.spec.ts` | 7/7 | ✅ **COMPLETO** |
| 11 | **3° Medio** | C | 193/2019 | 6 (Ciencias Ciudad.) | Separado (25 preg.) | `e2e/flujo-completo-3-medio.spec.ts` | 7/7 | ✅ **COMPLETO** |
| 12 | **4° Medio** | C | 193/2019 | 6 (Ciencias Ciudad.) | Separado (25 preg.) | `e2e/flujo-completo-4-medio.spec.ts` | 7/7 | ✅ **COMPLETO** |

---

## 📌 Progreso Global Final
- **Enseñanza Básica (1° a 8° Básico):** 8 / 8 Cursos (56/56 tests) ✅ **100% COMPLETADO**
- **Enseñanza Media (1° a 4° Medio):** 4 / 4 Cursos (26/26 tests) ✅ **100% COMPLETADO**
- **Total Cursos del Sistema Escolar Chileno:** 12 / 12 Cursos ✅ **100% COBERTURA TOTAL**
- **Total de Tests Playwright Pasando:** 82 / 82 tests (100% éxito)
- **Todas las Secciones Probadas:**
  - Onboarding familiar y RUT chileno con Módulo 11
  - Panel y supervisión de apoderados (métricas, plan, pagos)
  - Dashboard del alumno con check-in socioemocional
  - Catálogo de asignaturas oficiales por decreto ministerial (439/2012, 614/2013, 193/2019)
  - Estudio pedagógico con síntesis curricular, lectura por voz sintetizada, descarga PDF y rating de comprensión
  - Autoevaluaciones formativas con preguntas de selección múltiple y de desarrollo
  - Pruebas de unidad evaluadas y calificadas en vivo por el backend en escala chilena 1.0 a 7.0
  - Exámenes simulacros oficiales con cronómetro activo y formato de 20 o 25 preguntas según régimen
  - Plan de estudio personalizado y horario semanal
  - Proyección académica y registro histórico de notas
  - Gamificación: acumulación de XP y personalización de avatar
  - Plan lector y lista de útiles escolares
