# Skill: Logos School — Contexto del Proyecto y Trabajo en Español

## Descripción
Este skill define el contexto completo del proyecto **Logos School**, una plataforma web educativa para apoyar la preparación de **Exámenes Libres de Validación de Estudios** (Chile, 1° básico a 4° medio). Establece cómo trabajar juntos de forma fluida, en español, sin pisarnos ni entorpecer conversaciones.

---

## Contexto del Proyecto (Memoria Persistente)

### Qué es Logos School
- **Producto**: Aplicación web para estudio y preparación de Exámenes Libres Mineduc (Chile)
- **Cobertura**: 1° básico a 4° medio (12 cursos completos)
- **Objetivo**: Accesible, gratuita o muy bajo costo
- **Estado actual**: 🚧 Etapa 1 (MVP 4° básico) + Etapa 2 (Rol Profesor) + Fase 1 Brincus — **construidas y verificadas localmente (2026-08-14), sin desplegar**

### Contenido ya completo (no tocar salvo que el usuario pida)
- 12 temarios oficiales UCE/Mineduc en PDF (`Temarios/`)
- Extracción estructurada de 408 Objetivos de Aprendizaje (`Temarios/analisis/`)
- **2.917 preguntas** de autoevaluación (408/408 OA cubiertos)
- 156 pruebas de unidad calibradas por edad
- Exámenes tipo simulacro (Forma A/B por curso/asignatura, formato exacto Mineduc)
- Contenido de estudio: guía (explicación + ejemplos) por OA para los 12 cursos

### Hallazgo curricular clave
**No son 2 regímenes, son 3** (el corte no coincide con básica/media):
- **Régimen A** (1°-4° básico): prueba integrada 20 preguntas, 4 asignaturas (Dec. 439/2012)
- **Régimen B** (5° básico-2° medio): prueba por asignatura 25 preguntas, + Inglés (Dec. 439/2012 / 614/2013)
- **Régimen C** (3°-4° medio): currículo Dec. 193/2019 con asignaturas únicas (Ciencias para la Ciudadanía, Filosofía, Educación Ciudadana) — **contenido no reutilizable**

### Stack técnico decidido
- **Backend**: Python FastAPI (arquitectura hexagonal)
- **Frontend**: Angular
- **BD**: PostgreSQL (Neon con branches para dev/prod separados)
- **Deploy**: Backend → Render, Frontend → Cloudflare Pages
- **Auth**: Email/contraseña + Google OAuth
- **Correo**: Resend
- **Monitoreo**: Sentry + UptimeRobot
- **Pagos**: Pendiente (tope $19.990 CLP/mes, modelo empresa, no fundación)

### Tests verificados (2026-08-14)
- Backend: **326/326 tests** en verde
- Frontend: **69/69 Playwright** en verde
- QA automatizado: `scripts/qa_completo.sh` + `scripts/validar_calidad_contenido.py`

---

## Reglas de Colaboración (No Negociables)

### 1. Idioma: **Siempre español**
- Todas las respuestas, código, comentarios, documentación, commits: **en español**
- Nombrar variables, funciones, clases en español cuando sea natural del dominio (ej. `ObjetivoAprendizaje`, `calcularNota`, `alumno`)
- Excepciones: términos técnicos universales (API, JWT, SQL, HTTP, CSS, TypeScript)

### 2. Modo de operación (ver `planificacion/04-modo-de-operacion.md`)
- Opero como **profesor/educador experto** autónomo
- Produzco contenido pedagógico con criterio propio
- Pregunto al usuario **solo lo mínimo indispensable**
- **No pido confirmaciones sí/no** (feedback 2026-08-10): actúo con criterio e informo después
- Decido solo: redacción pedagógica, ejemplos, estructura de contenido, naming interno, refactors técnicos
- Pregunto al usuario: cambios de alcance, decisiones de producto/negocio, stack, deployment, UX mayor, privacidad/datos menores

### 3. Fases de trabajo (Etapa 1 = MVP 4° básico)
| Fase | Qué incluye | Estado |
|------|-------------|--------|
| 1.1 | Estudiar + rendir evaluaciones | ✅ Construida |
| 1.2 | Historial y notas por materia | ✅ Construida |
| 1.3 | Plan de estudio con horario + habilitación progresiva | ✅ Construida |
| Etapa 2 | Rol Profesor (Curso/Sección) | ✅ Construida |
| Fase 1 Brincus | 10 ítems sin deps externas | ✅ Construida (2026-08-14) |
| Fase 2 Brincus | IA, Juegos, Biblioteca, Plan Lector | ⏳ Pendiente |

### 4. Documentos fuente de verdad (leer antes de asumir)
- `CLAUDE.md` — Contexto general y memoria del proyecto
- `planificacion/00-vision-alcance.md` — Visión, decisiones, estado
- `planificacion/22-analisis-de-brechas.md` — **Auditoría real contra código** (qué falta realmente)
- `planificacion/27-plan-incorporacion-hallazgos-brincus.md` — Qué se construyó en Fase 1 Brincus
- `contenido/00-estado-contenido.md` — Detalle curso por curso, asignatura por asignatura

### 5. Git y GitHub
- **Repo local únicamente** (sin remote configurado aún)
- Rama actual: `main`
- Commits recientes describen trabajo completado (ver `git log --oneline`)
- **No asumir que está en GitHub** — el usuario decidirá cuándo y cómo subirlo

### 6. No tocar sin preguntar (salvo refactors técnicos menores)
- Contenido pedagógico ya validado (2.917 preguntas, 408 OA)
- Tests que pasan (326 backend, 69 frontend)
- Estructura de BD decidida (`planificacion/02-modelo-de-datos-conceptual.md`)
- Decisiones de producto registradas en `planificacion/00-vision-alcance.md`

---

## Patrones de Trabajo para Fluidez

### Inicio de conversación
1. **Leer `CLAUDE.md`** (se carga automáticamente en Claude Code, aquí leerlo explícitamente)
2. **Revisar `planificacion/22-analisis-de-brechas.md`** si se habla de "qué falta" o "estado real"
3. **No asumir que algo "ya funciona"** — verificar contra la auditoría de brechas

### Cuando el usuario pida algo nuevo
- Si es **contenido pedagógico**: producir directamente (modo experto)
- Si es **código/refactor**: implementar con criterio técnico, informar después
- Si es **decisión de producto/alcance**: proponer opciones, preguntar lo mínimo
- Si es **deployment/infra/credenciales**: son bloqueadores conocidos, no inventar soluciones

### Commits y cambios
- Commits atómicos, mensajes en español descriptivos
- No hacer push automático (no hay remote)
- El usuario decide cuándo commitear/pushear

### Estructura de carpetas clave
```
Temarios/                 # PDFs oficiales + análisis estructurado (408 OA)
contenido/                # Contenido de estudio real (guías, preguntas) — 12 cursos completos
backend/                  # FastAPI hexagonal + 326 tests
frontend/                 # Angular + 69 Playwright tests
planificacion/            # 28 docs de especificación, roadmap, auditorías
scripts/                  # QA automatizado, validación calidad
.claude/agents/           # Agente experto exámenes libres (prototipo chatbot)
```

---

## Qué NO hacer (para no entorpecer)

| ❌ No hacer | ✅ En su lugar |
|-------------|----------------|
| Preguntar "¿quieres que haga X?" por cada paso | Hacer X con criterio, informar "He hecho X porque Y" |
| Asumir que el frontend está conectado al backend | Leer `22-analisis-de-brechas.md`: **no está conectado** |
| Asumir que hay deployment/credenciales reales | Son bloqueadores conocidos (ver `17-infraestructura-y-entornos.md`) |
| Proponer cambiar stack (ya decidido) | Trabajar dentro de FastAPI + Angular + PostgreSQL |
| Tocar contenido validado sin pedido explícito | Respetar las 2.917 preguntas y 408 OA como fuente de verdad |
| Usar inglés en código/comentarios/respuestas | **Todo en español** |
| Crear skills duplicados o genéricos | Usar/extender este skill como base |

---

## Skills Complementarios Sugeridos (para crear después)

Cuando el proyecto lo requiera, crear skills específicos bajo `.opencode/skill/`:

1. **`backend-fastapi-hexagonal.md`** — Patrones, testing, migraciones, auth, endpoints del proyecto
2. **`frontend-angular-logos.md`** — Componentes, servicios, estado, Playwright, diseño visual (índigo/coral, Poppins/Inter)
3. **`contenido-pedagogico.md`** — Cómo producir/validar guías, preguntas, simulacros (408 OA, 3 regímenes)
4. **`auditoria-calidad.md`** — Scripts QA, validación contenido, análisis de brechas, checklist de releases
5. **`examenes-libres-chile.md`** — Trámite administrativo real (inscripción, 3 periodos, entidad examinadora, recorrección)
6. **`deployment-infra.md`** — Neon branches, Render, Cloudflare Pages, Resend, Sentry, variables de entorno dev/prod

---

## Cómo invocar este skill
- Se carga automáticamente al estar en `.opencode/skill/logos-school.md`
- Para referenciarlo explícitamente: "usa el skill logos-school"
- Sirve como **contexto compartido persistente** entre conversaciones

---

## Actualización
- Este skill es **vivo**: actualízalo cuando cambien decisiones centrales, se complete una fase, o cambie el estado del proyecto
- Última actualización: 2026-08-17 (post Fase 1 Brincus completa + QA exhaustivo)
- Próxima revisión sugerida: antes de iniciar Fase 2 Brincus o deployment