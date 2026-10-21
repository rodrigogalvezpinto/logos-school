# QA - Logos School

## Instrucciones para ejecutar la auditoría

Esta carpeta contiene la documentación y resultados de la auditoría QA exhaustiva de Logos School.

## Estado de la Auditoría

**Fecha de inicio:** 2026-10-18
**Fase actual:** Fase Cero - Inspección y protección del entorno
**Responsable:** Equipo QA multidisciplinario (Devin AI)

## Estructura de Documentación

- `README.md` - Este archivo (instrucciones)
- `INVENTORY.md` - Inventario de módulos y funcionalidades
- `TEST-MATRIX.md` - Matriz de requisitos y casos de prueba
- `DEFECTS.md` - Registro histórico de defectos
- `COVERAGE.md` - Métricas de cobertura
- `EXECUTION-REPORT.md` - Informe de la última ejecución
- `REGRESSION.md` - Pruebas de regresión incorporadas

## Comandos de Ejecución

### Backend (Python/FastAPI)
```bash
cd backend
uv run pytest                    # Ejecutar todos los tests
uv run pytest -v                 # Verbose
uv run pytest --cov             # Con cobertura
uv run pytest tests/test_auth.py # Tests específicos
```

### Frontend (Angular/Playwright)
```bash
cd frontend
npx playwright test              # Ejecutar todos los tests E2E
npx playwright test e2e/*.spec.ts # Tests específicos
npx playwright test --ui         # UI interactiva
```

### Servicios
```bash
# Backend
cd backend
uv run uvicorn app.main:app --reload --port 8000

# Frontend
cd frontend
npm start  # puerto 4200
```

## Entorno de Pruebas

**Base de datos:** PostgreSQL local (no usar producción)
**Datos de prueba:** Cuentas creadas específicamente para QA
**Secretos:** No usar credenciales reales en pruebas

## Política de Seguridad

- No usar datos personales reales
- No ejecutar pruebas destructivas en producción
- Aislar datos de prueba (usar prefijos "qa-" en emails)
- Verificar aislamiento entre usuarios

## Protocolo de Corrección de Defectos

Cada defecto sigue este ciclo:
1. Crear ID único (BUG-0001)
2. Documentar pasos para reproducir
3. Identificar causa raíz
4. Corregir en rama de trabajo
5. Crear prueba de regresión
6. Validar corrección
7. Documentar estado final

## Criterios de Aceptación

La auditoría solo se considera cerrada cuando:
- El inventario está completo
- Todos los casos ejecutables han sido probados
- Defectos críticos y altos están corregidos
- Pruebas de regresión están implementadas
- Informe final con evidencias está disponible
