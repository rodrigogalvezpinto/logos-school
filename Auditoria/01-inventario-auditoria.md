# 01 — Inventario y Diagnóstico Inicial de Auditoría
**Fecha de corte:** 21 de octubre de 2026  
**Repositorio:** `rodrigogalvezpinto/logos-school`  
**Rama inspeccionada:** `main`  
**Commit de referencia:** `5ec3303e7d32158176b551bd379bb9238c89de5c`  
**Equipo auditor:** Arquitecto de Software, QA Engineer Senior, Especialista UX/UI, Profesor de Matemática Curricular, Especialista en Parsing de Contenido.

---

## 1. Arquitectura y Tecnologías del Repositorio

El sistema Logos School está constituido por una arquitectura desacoplada frontend/backend con persistencia relacional:

- **Frontend:**
  - Framework: Angular 22.1.0 (`frontend/package.json`).
  - Lenguaje y compilador: TypeScript 6.0.2 con arquitectura Standalone Components y Signals (`@angular/core`).
  - Estilos y UI: CSS nativo con variables CSS (`--color-primario`, etc.) sin dependencias pesadas de UI.
  - Parser Markdown: `marked` 18.0.9 integrado a través de `MarkdownPipe` (`frontend/src/app/shared/markdown.pipe.ts`).
  - Pruebas unitarias: Vitest 4.0.8 y `@angular/build` (33 pruebas unitarias).
  - Pruebas End-to-End: Playwright 1.62.1 y `@axe-core/playwright` 4.13.0 (64 suites spec, 362 tests ejecutados).

- **Backend:**
  - Framework: FastAPI 0.115+ (Python 3.14).
  - ORM y Modelado: SQLModel 0.0.22 / SQLAlchemy 2.0.
  - Migraciones: Alembic.
  - Rate Limiting: SlowAPI 0.1.9.
  - Generación documental: WeasyPrint (PDF de certificados, guías e informes de avance).
  - Pruebas backend: Pytest 9.1.1 (491 tests pasando).

- **Base de Datos:**
  - Motor: PostgreSQL 14+ en `localhost:5432`.
  - Base de producción local / QA: `logos_qa` (configurada en `backend/.env`).

- **Repositorio de Contenido Curricular:**
  - 12 carpetas curriculares en `contenido/` (`01-basico/` a `12-cuarto-medio/`).
  - Documentos Markdown con guías y bancos de autoevaluación: 52 archivos de asignaturas.
  - Pruebas de unidad y exámenes simulacros oficiales: 156 pruebas y 92 exámenes.
  - Temarios oficiales UCE MINEDUC: 12 documentos PDF oficiales en `Temarios/` y 12 análisis en `Temarios/analisis/`.

---

## 2. Inventario Comprobado de Matemática (12 Cursos)

El recuento se realizó combinando inspección estática del texto Markdown y la ejecución del parser oficial (`backend/scripts/parser_contenido.py`) sobre los 12 archivos `contenido/*/matematica.md`:

| Curso | Archivo | Líneas | Palabras | OA en Temario | OA en Guía | Preguntas Totales | Alternativas | Desarrollo | V/F |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| **1.º básico** | `contenido/01-basico/matematica.md` | 840 | 6.029 | 10 | 10 | **59** | 10 | 44 | 5 |
| **2.º básico** | `contenido/02-basico/matematica.md` | 997 | 8.368 | 13 | 13 | **84** | 20 | 50 | 14 |
| **3.º básico** | `contenido/03-basico/matematica.md` | 1.012 | 8.520 | 13 | 13 | **87** | 24 | 50 | 13 |
| **4.º básico** | `contenido/04-basico/matematica.md` | 1.084 | 9.100 | 14 | 14 | **84** | 24 | 48 | 12 |
| **5.º básico** | `contenido/05-basico/matematica.md` | 1.236 | 12.158 | 17 | 17 | **102** | 27 | 61 | 14 |
| **6.º básico** | `contenido/06-basico/matematica.md` | 774 | 8.556 | 11 | 11 | **66** | 18 | 40 | 8 |
| **7.º básico** | `contenido/07-basico/matematica.md` | 778 | 8.636 | 9 | 9 | **72** | 20 | 44 | 8 |
| **8.º básico** | `contenido/08-basico/matematica.md` | 849 | 10.457 | 10 | 10 | **80** | 20 | 50 | 10 |
| **1.º medio** | `contenido/01-medio/matematica.md` | 670 | 7.900 | 7 | 7 | **56** | 16 | 32 | 8 |
| **2.º medio** | `contenido/02-medio/matematica.md` | 620 | 7.272 | 6 | 6 | **57** | 16 | 33 | 8 |
| **3.º medio** | `contenido/03-medio/matematica.md` | 528 | 7.324 | 3 | 3 | **56** | 16 | 32 | 8 |
| **4.º medio** | `contenido/04-medio/matematica.md` | 522 | 8.962 | 3 | 3 | **54** | 16 | 25 | 13 |
| **TOTAL** | **12 guías curriculares** | **9.910** | **103.282** | **116** | **116** | **857** | **227 (26.5%)** | **509 (59.4%)** | **121 (14.1%)** |

### Observaciones del Inventario:
1. **Predominio de Preguntas Abiertas (59.4%):** Más de la mitad de las preguntas (509 de 857) corresponden a desarrollo formativo. Esto acentúa la criticidad del defecto `MAT-UI-001`.
2. **Coincidencia Exacta de OA (100%):** Los 116 identificadores OA presentes en los temarios oficiales de la UCE coinciden de manera unívoca con los encabezados de las guías.
3. **Discrepancia Regex vs Parser en 5° Básico:** Una búsqueda por expresiones regulares cruda detecta 104 líneas que inician con números de pregunta, mientras que el parser estructurado procesa exactamente 102 preguntas reales (las otras 2 líneas corresponden a numeración interna dentro de un ejemplo resuelto de la guía).

---

## 3. Componentes y Módulos de Código Inspeccionados

- **Evaluaciones y Runner:**
  - `frontend/src/app/shared/evaluacion-runner/evaluacion-runner.ts` (449 líneas): Controla el ciclo de vida del intento, cronómetro, respuestas y feedback.
  - `frontend/src/app/pages/autoevaluacion/autoevaluacion.ts`: Contenedor del modo práctica libre.
  - `frontend/src/app/pages/prueba-unidad/prueba-unidad.ts`: Contenedor de pruebas sumativas.
  - `frontend/src/app/pages/examen-simulacro/examen-simulacro.ts`: Contenedor de exámenes simulacros.
  - `backend/app/routers/evaluaciones.py`: Endpoints de autoevaluación, intentos, respuestas y calificación.
  - `backend/app/domain/evaluaciones/`: Entidades de dominio, cálculo de notas (escala 1.0-7.0 al 60%).

- **Sesión, Perfiles y Shell de Interfaz:**
  - `frontend/src/app/core/sesion.service.ts`: Manejo de tokens y `perfilActivo` (signals y `localStorage`).
  - `frontend/src/app/core/auth.service.ts`: Tipos `PerfilAlumnoRespuesta` y llamadas API.
  - `frontend/src/app/layout/shell/shell.ts`: Disposición de topbar y navegación.
  - `frontend/src/app/shared/topbar/topbar.ts`: Barra superior con nombre de usuario y buscador.
  - `frontend/src/app/pages/alumno-inicio/alumno-inicio.ts`: Pantalla principal del alumno.
  - `frontend/src/app/pages/selector-perfil/selector-perfil.ts`: Selector familiar de estudiante.
  - `frontend/src/app/shared/logo/logo.ts`: Componente visual del logo.

- **Importación y Modelos de Datos:**
  - `backend/scripts/importar_contenido.py`: Script maestro de ingesta.
  - `backend/scripts/parser_contenido.py`: Parser de guías y preguntas de autoevaluación.
  - `backend/scripts/parser_prueba_examen.py`: Parser de pruebas y exámenes con pauta.
  - `backend/app/infrastructure/persistence/orm_models.py`: Definición de tablas `pregunta`, `objetivo_aprendizaje`, `perfilalumno`, etc.

---

## 4. Limitaciones del Alcance de la Auditoría

1. **Sin Modificaciones Activas:** Conforme a la regla fundamental, no se alteró ningún archivo del código ni se hicieron commits en el repositorio.
2. **Entorno de Datos:** Las inspecciones se realizaron sobre la base PostgreSQL real `logos_qa` y los archivos fuente Markdown versionados en `git`.
3. **Cálculos Matemáticos:** Se auditaron computacionalmente las 857 preguntas a nivel sintáctico y se aislaron los casos sospechosos; la certificación de cálculo paso a paso requiere contrastación contra el solucionario curricular en la fase de ejecución.
