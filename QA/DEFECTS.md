# QA - Registro de Defectos
**Fecha:** 2026-10-18
**Estado:** En construcción

---

## Defectos Encontrados

| ID | Severidad | Módulo | Descripción | Estado | Fecha descubrimiento |
|----|-----------|--------|-------------|--------|----------------------|
| BUG-0001 | CRÍTICA | Base de datos | Base de datos sin esquema - tests fallaban | ✅ CORREGIDO | 2026-10-18 |
| BUG-0002 | MEDIA | Frontend - Tests | Tests de seguridad con timeouts excesivos (30s) | 🔄 EN PROGRESO | 2026-10-18 |
| BUG-0003 | MEDIA | Frontend - Tests | Tests de Admin con timeouts (5.3s) | ⏳ PENDIENTE | 2026-10-18 |
| BUG-0004 | MEDIA | Frontend - Tests | Tests de Plan de Estudio con timeouts (30s) | ⏳ PENDIENTE | 2026-10-18 |
| BUG-0005 | BAJA | Accesibilidad | Contraste insuficiente en Plan de Estudio | ⏳ PENDIENTE | 2026-10-18 |
| BUG-0006 | BAJA | Accesibilidad | Contraste insuficiente en Dashboard Admin | ⏳ PENDIENTE | 2026-10-18 |
| BUG-0007 | BAJA | Accesibilidad | Contraste insuficiente en Dashboard Profesor | ⏳ PENDIENTE | 2026-10-18 |

---

## Detalle de Defectos

### BUG-0001: Base de datos sin esquema
**Severidad:** CRÍTICA
**Módulo:** Base de datos
**Estado:** ✅ CORREGIDO

**Descripción:**
La base de datos `logos_dev` existía pero no tenía las migraciones aplicadas, causando que 110 tests fallaran y 199 tuvieran errores.

**Pasos para reproducir:**
1. Ejecutar `uv run pytest` en backend
2. Observe que tests fallan con `sqlalchemy.exc.ProgrammingError: relation "cuenta" does not exist`

**Resultado esperado:**
Base de datos con esquema completo, todos los tests pasan.

**Resultado real:**
Base de datos sin tablas, tests fallan.

**Causa raíz:**
Base de datos creada manualmente sin ejecutar migraciones.

**Solución aplicada:**
1. Crear base de datos separada `logos_qa` para pruebas
2. Ejecutar `uv run alembic upgrade head` (18 migraciones)
3. Ejecutar scripts de datos: sembrar_planes.py, importar_contenido.py, datos_de_prueba.py

**Archivos modificados:**
- backend/.env (temporalmente cambiado a logos_qa)

**Prueba de regresión:**
Ejecutar `uv run pytest` → 491/491 tests pasan

**Referencias:**
- Commit: 05b22d1
- Reporte: QA/EXECUTION-REPORT.md

---

### BUG-0002: Tests de seguridad con timeouts excesivos
**Severidad:** MEDIA
**Módulo:** Frontend - Tests E2E
**Estado:** 🔄 EN PROGRESO

**Descripción:**
Los tests de seguridad que creé usan `waitForTimeout(2000)` y `waitForTimeout(30000)` que causan timeouts innecesarios.

**Pasos para reproducir:**
1. Ejecutar `npx playwright test e2e/qa-seguridad-critica.spec.ts`
2. Observe que tests fallan con timeout

**Resultado esperado:**
Tests completan rápidamente usando `waitForLoadState` en lugar de timeouts fijos.

**Resultado real:**
Tests fallan por timeout excesivo.

**Causa raíz:**
Uso inadecuado de `waitForTimeout` en lugar de esperar eventos de carga.

**Solución aplicada:**
Reemplazar `waitForTimeout` por `waitForLoadState('networkidle')`

**Archivos modificados:**
- frontend/e2e/qa-seguridad-critica.spec.ts

**Prueba de regresión:**
Ejecutar `npx playwright test e2e/qa-seguridad-critica.spec.ts` → tests pasan

**Referencias:**
- Commit: 05b22d1

---

### BUG-0003: Tests de Admin con timeouts
**Severidad:** MEDIA
**Módulo:** Frontend - Tests E2E
**Estado:** ⏳ PENDIENTE

**Descripción:**
Tests de Admin fallan con timeout de 5.3s. No está claro si es un problema de lentitud del servidor o un bug funcional.

**Pasos para reproducir:**
1. Ejecutar `npx playwright test e2e/admin.spec.ts`
2. Observe que tests fallan con timeout

**Resultado esperado:**
Tests de Admin completan sin timeout.

**Resultado real:**
Tests fallan con timeout 5.3s.

**Causa raíz:**
PENDIENTE DE INVESTIGACIÓN

**Solución propuesta:**
Investigar si es lentitud del servidor o bug funcional. Si es lentitud, aumentar timeout o optimizar carga del dashboard.

**Archivos afectados:**
- frontend/e2e/admin.spec.ts

**Prueba de regresión:**
PENDIENTE

---

### BUG-0004: Tests de Plan de Estudio con timeouts
**Severidad:** MEDIA
**Módulo:** Frontend - Tests E2E
**Estado:** ⏳ PENDIENTE

**Descripción:**
Tests de Plan de Estudio fallan con timeout de 30s (repaso, vista semanal/mensual, plan lector).

**Pasos para reproducir:**
1. Ejecutar tests de plan-estudio
2. Observe timeouts de 30s

**Resultado esperado:**
Tests completan sin timeout.

**Resultado real:**
Tests fallan con timeout 30s.

**Causa raíz:**
PENDIENTE DE INVESTIGACIÓN

**Solución propuesta:**
Investigar si es problema de carga de datos o bug funcional.

**Archivos afectados:**
- frontend/e2e/plan-estudio-repaso.spec.ts
- frontend/e2e/plan-estudio-vistas.spec.ts
- frontend/e2e/plan-lector.spec.ts

**Prueba de regresión:**
PENDIENTE

---

### BUG-0005: Contraste insuficiente en Plan de Estudio
**Severidad:** BAJA
**Módulo:** Frontend - Accesibilidad
**Estado:** ⏳ PENDIENTE

**Descripción:**
Test de accesibilidad detecta contraste insuficiente en Plan de Estudio.

**Pasos para reproducir:**
1. Ejecutar `npx playwright test e2e/accesibilidad.spec.ts`
2. Observar fallo en "Plan de Estudio sin violaciones graves"

**Resultado esperado:**
Contraste cumple WCAG AA (4.5:1).

**Resultado real:**
Contraste insuficiente detectado por axe-core.

**Causa raíz:**
PENDIENTE DE INVESTIGACIÓN

**Solución propuesta:**
Ajustar colores del chip "Atrasada" u otros elementos en Plan de Estudio.

**Archivos afectados:**
- frontend/src/app/pages/plan-estudio/

**Prueba de regresión:**
Ejecutar test de accesibilidad de Plan de Estudio → pasa

---

### BUG-0006: Contraste insuficiente en Dashboard Admin
**Severidad:** BAJA
**Módulo:** Frontend - Accesibilidad
**Estado:** ⏳ PENDIENTE

**Descripción:**
Test de accesibilidad detecta contraste insuficiente en Dashboard Admin.

**Pasos para reproducir:**
1. Ejecutar test de accesibilidad de Admin
2. Observar fallo

**Resultado esperado:**
Contraste cumple WCAG AA.

**Resultado real:**
Contraste insuficiente.

**Causa raíz:**
PENDIENTE DE INVESTIGACIÓN

**Solución propuesta:**
Ajustar colores en dashboard admin.

**Archivos afectados:**
- frontend/src/app/pages/admin-dashboard/

**Prueba de regresión:**
PENDIENTE

---

### BUG-0007: Contraste insuficiente en Dashboard Profesor
**Severidad:** BAJA
**Módulo:** Frontend - Accesibilidad
**Estado:** ⏳ PENDIENTE

**Descripción:**
Test de accesibilidad detecta contraste insuficiente en Dashboard Profesor.

**Pasos para reproducir:**
1. Ejecutar test de accesibilidad de Profesor
2. Observar fallo

**Resultado esperado:**
Contraste cumple WCAG AA.

**Resultado real:**
Contraste insuficiente.

**Causa raíz:**
PENDIENTE DE INVESTIGACIÓN

**Solución propuesta:**
Ajustar colores en dashboard profesor.

**Archivos afectados:**
- frontend/src/app/pages/profesor-dashboard/

**Prueba de regresión:**
PENDIENTE

---

## Resumen de Severidades

- CRÍTICA: 1 (1 corregido)
- MEDIA: 3 (1 en progreso, 2 pendientes)
- BAJA: 3 (3 pendientes)

**Total:** 7 defectos registrados
