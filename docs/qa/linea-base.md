# Línea Base Certificada de Pruebas Automatizadas
**Proyecto:** Logos School  
**Commit de Referencia:** `2265984` (sincronizado con `origin/main`)  
**Fecha de Verificación en Vivo:** 21 de octubre de 2026  
**Entorno de Ejecución:** macOS local, PostgreSQL `logos_qa` (puerto 5432), Python 3.14.5 (.venv), Node.js v25.1.0

> **Actualización 2026-10-28:** sobre `main`, el frontend unitario se verificó en vivo: **46/46 pruebas en verde (10 archivos)**. Backend y E2E no se pudieron ejecutar porque el daemon de Docker estaba detenido y PostgreSQL no escuchaba en 5432. Las cifras de 491 / 33 / 362 de este documento son la línea base histórica del 21-10-2026, no el estado actual. El estado vigente está en `docs/auditorias/00-CENTRO-DE-CONTROL-AUDITORIA.md` §15.

---

## 1. Resumen Ejecutivo de la Línea Base

La plataforma Logos School cuenta con una pirámide integral de pruebas automatizadas compuesta por **886 pruebas de software**. Para garantizar transparencia metodológica, se clasifica rigurosamente el estado de certificación de cada suite:

| Suite / Nivel | Comando de Reproducción | Resultados Verificados | Estado de Certificación | Tiempo de Ejecución |
|---|---|:---:|:---:|:---:|
| **Backend (Pytest)** | `cd backend && .venv/bin/pytest -q` | **491 aprobadas** (11 warnings, 0 fallos) | **Certificación Actual Verificada en Vivo** (21-oct-2026 14:40 -03:00) | 5 min 46 s |
| **Frontend Unitario (Vitest)** | `cd frontend && npm test -- --watch=false` | **33 aprobadas** (8 archivos spec, 0 fallos) | **Certificación Actual Verificada en Vivo** (21-oct-2026 14:39 -03:00) | 959 ms |
| **Frontend E2E (Playwright)** | `cd frontend && npx playwright test` | **362 aprobadas** (64 suites completas) | **Evidencia Histórica Reproducible** (Commit `86a4c93`, 20-oct-2026 19:00 -03:00) | ~18 min |
| **Total Pirámide de Software** | — | **886 pruebas (100% verde)** | **Línea Base Funcional Completa** | — |

---

## 2. Detalle y Evidencia de Ejecución en Vivo

### 2.1. Backend: Pytest (491 pruebas)
- **Comando:** `cd backend && .venv/bin/pytest -q`
- **Timestamp:** 21-oct-2026 14:40:24 -03:00
- **Log de Salida:**
```text
........................................................................ [ 14%]
........................................................................ [ 29%]
........................................................................ [ 43%]
........................................................................ [ 58%]
........................................................................ [ 73%]
........................................................................ [ 87%]
...........................................................              [100%]
491 passed, 11 warnings in 346.15s (0:05:46)
```
- **Cobertura validada:** Autenticación JWT, control de acceso basado en roles (RBAC apoderado, alumno, profesor, administrador), matriz automática de permisos en endpoints, motor de evaluación, generación de diagnósticos, cálculo de calificaciones y reportes.

### 2.2. Frontend: Vitest (33 pruebas unitarias)
- **Comando:** `cd frontend && npm test -- --watch=false`
- **Timestamp:** 21-oct-2026 14:39:57 -03:00
- **Log de Salida:**
```text
 ✓ |frontend| src/app/shared/emoji-pipe.spec.ts (4 tests) 3ms
 ✓ |frontend| src/app/shared/estilo-asignatura.spec.ts (9 tests) 3ms
 ✓ |frontend| src/app/core/rut.util.spec.ts (6 tests) 3ms
 ✓ |frontend| src/app/core/sesion-admin.service.spec.ts (4 tests) 3ms
 ✓ |frontend| src/app/core/sesion-profesor.service.spec.ts (4 tests) 3ms
 ✓ |frontend| src/app/core/auth.guard.spec.ts (2 tests) 9ms
 ✓ |frontend| src/app/core/admin.guard.spec.ts (2 tests) 9ms
 ✓ |frontend| src/app/core/profesor.guard.spec.ts (2 tests) 8ms

 Test Files  8 passed (8)
      Tests  33 passed (33)
   Duration  959ms
```
- **Cobertura validada:** Utilidades de validación de RUT chileno (Módulo 11), tuberías de emojis responsivos, estilos por asignatura y guardianes de ruta (`auth.guard`, `admin.guard`, `profesor.guard`).

### 2.3. Frontend: Playwright E2E (362 pruebas en 64 suites)
- **Estado:** Evidencia histórica reproducible certificada en el commit `86a4c935945d` (20 de octubre de 2026).
- **Cobertura validada:** 64 archivos spec que cubren los flujos de navegación completos de los 12 cursos escolares (1° básico a 4° medio), rendición de pruebas de unidad, autoevaluaciones, portal de apoderados, gestión de suscripciones, plan lector, útiles escolares y check-in emocional.
- **Protocolo de verificación:** Para reproducir la suite E2E completa de forma local:
  1. Levantar servicios: `./iniciar.sh`
  2. En otra terminal: `cd frontend && npx playwright test`

---

## 3. Delimitación Estricta: Software vs Contenido Pedagógico

> [!IMPORTANT]
> **Distinción entre Pruebas de Código y Validación Curricular:**  
> Las 886 pruebas automatizadas certifican exclusivamente el correcto funcionamiento del **código fuente de la aplicación** (FastAPI, PostgreSQL, Angular, lógica de negocio y seguridad).  
> **Ninguna de las 857 preguntas de Matemática se declara "certificada matemáticamente o pedagógicamente".**  
> Su estado actual es: **Inventariadas y Analizadas Sintácticamente**. La comprobación aritmética de cada cálculo, alternativa y retroalimentación didáctica corresponde a una etapa independiente de revisión pedagógica.
