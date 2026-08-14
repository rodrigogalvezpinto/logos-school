---
título: Roadmap por etapas
estado: borrador — etapas 0 y 1 razonablemente claras; etapas 2+ son dirección tentativa
última actualización: 2026-08-10
---

Se eligió partir con **un curso piloto único** (no todos los niveles a la vez) y con
**autoestudio primero** (el rol Profesor se activa después). Este roadmap refleja esa
decisión.

## Etapa 0 — Cimientos (donde estamos ahora)

- [x] Reunir los 12 temarios oficiales UCE (`Temarios/`).
- [x] Extraer los 12 temarios a formato estructurado (`Temarios/analisis/`) — 408 OA
      extraídos, confirmados 3 regímenes de examen distintos (ver `00-resumen-general.md`).
- [x] Definir roles preliminares (Alumno, Apoderado, Profesor, Administrador propuesto).
- [x] Definir modelo conceptual de Nivel / Curso-Sección / Asignatura / OA.
- [x] **Elegir el curso piloto específico**: **4° básico**.
- [ ] Confirmar permisos detallados de Apoderado y necesidad del rol Administrador.
- [ ] Definir mecanismo de verificación de vínculos (apoderado-alumno, identidad de
      profesor) — importante por tratarse de menores de edad.
- [ ] Decidir si el "banco de preguntas" de autoevaluación se crea a mano, con ayuda de IA
      revisada por humanos, o se contrata/curatea de terceros (no se ha conversado aún).

## Etapa 1 — MVP: piloto de un curso, modo autoestudio

Alcance mínimo para validar el modelo completo end-to-end en un solo nivel antes de
escalar: **4° básico**, formato de prueba integrada (4 asignaturas), Régimen A. Roles
Alumno y Apoderado únicamente (sin Profesor/Curso-Sección — Etapa 2).

**Estado: ✅ contenido de 4° básico completo (2026-08-10).** Los 32 OA oficiales de las 4
asignaturas están cubiertos en `contenido/04-basico/`, con 195 preguntas de autoevaluación,
más pruebas de unidad y exámenes simulacro (ver `contenido/00-estado-contenido.md`).

**Decisión 2026-08-12:** la Etapa 1 se construye en **3 fases incrementales**, cada una
entregable y usable por sí sola antes de pasar a la siguiente — no se espera a tener las 3
listas para lanzar la primera:

### Fase 1.1 — Estudiar y evaluarse (el núcleo mínimo lanzable)

Un alumno puede entrar, revisar las unidades de estudio (guía por OA), rendir
autoevaluaciones formativas, pruebas de unidad y exámenes simulacro, y ver el resultado
(nota y desglose) al terminar cada uno. **No incluye todavía** historial acumulado ni plan
de estudio con calendario — cada evaluación se toma y se resuelve en el momento. Ver
`12-motor-de-evaluacion.md` para el detalle completo del flujo de "rendir" una evaluación
(cronómetro, navegación de preguntas, cálculo de nota, resumen final).

Incluye también el registro simple (Apoderado + Perfiles de Alumno) y la selección de plan
de pago — ver `10-privacidad-y-datos-de-menores.md` y `09-modelo-de-negocio.md`.

**Esta fase, por sí sola, ya es un producto usable y lanzable** (equivalente al "estudiar y
practicar" de Wited, sin todavía la capa de seguimiento).

### Fase 1.2 — Registro de avances (historial y notas por materia) ✅ completa (2026-08-12)

Se agrega la capa de seguimiento: el Alumno (y el Apoderado) puede ver el historial completo
de guías revisadas, pruebas y exámenes rendidos, con su nota y fecha. Aparece la **nota por
asignatura** (agregada desde las pruebas de unidad rendidas) y una vista de "con qué nota se
presentaría hoy al examen real" — distinguiendo siempre esa nota de práctica de lo que
realmente indica si aprendió: el resultado del examen simulacro. Ver
`12-motor-de-evaluacion.md`, sección "Notas por materia y señal real de preparación".

### Fase 1.3 — Plan de estudio con horario ✅ completa (2026-08-13)

Se agrega la posibilidad de elegir una frecuencia de estudio (3, 4 o 5 días a la semana) y
la plataforma arma un cronograma que reparte el contenido pendiente en sesiones, para que el
alumno estudie de forma ordenada en vez de solo cuando quiere. Ver `13-plan-de-estudio.md`
para el diseño completo.

**Criterio de éxito de la Etapa 1 completa:** un grupo real de alumnos de 4° básico puede
estudiar de principio a fin con el material de la plataforma, siguiendo un horario, viendo su
avance y notas por materia, y llegar al examen simulacro con una idea realista de si está
preparado — sintiendo que cubre lo que el temario oficial exige.

## Etapa 2 — Activar el rol Profesor y Curso/Sección ✅ completa (2026-08-13)

- [x] Profesores pueden registrarse (auto-registro, cuenta nace `pendiente` hasta que un
      Administrador la aprueba desde `/admin/profesores` — revisión manual, sin verificación
      con documentos).
- [x] Profesores pueden crear Cursos/Secciones y agregar/quitar alumnos (el alumno no puede
      autoagregarse).
- [x] Alumnos dentro de un Curso/Sección ven la sección "Mi Curso" (nombre del curso, del
      profesor y comunicados recientes) en `/alumno/inicio`.
- [x] Comunicados de texto simple del profesor hacia su Curso/Sección.
- [x] Reportes de progreso a nivel de Curso/Sección para el Profesor (reutiliza la consulta
      de notas de Fase 1.2, una vez por alumno del curso).

**Verificación:** 122/122 tests backend (`cd backend && uv run pytest -q`), 35/35 tests E2E
(`cd frontend && npx playwright test --workers=1`, incluye `e2e/profesor.spec.ts`: registro
→ pendiente → aprobación por Admin → crear curso → agregar alumno → progreso → comunicado →
visible en `/alumno/inicio` → quitar alumno).

**Fuera de alcance de esta pasada** (documentado para no perderlo): chat/mensajería directa
apoderado↔profesor, evaluaciones propias publicadas por el profesor, verificación de
identidad con documentos, y un alumno perteneciendo a más de un Curso/Sección a la vez.

## Etapa 3 — Expandir a más niveles dentro del mismo régimen de examen

Confirmado con el análisis completo de los 12 temarios (`Temarios/analisis/
00-resumen-general.md`): **no hay 2 regímenes de examen (básica/media), hay 3**, y el corte
no coincide con el límite básica/media:

| Régimen | Cursos | Formato |
|---|---|---|
| A | 1°-4° básico | Prueba integrada única, 20 preguntas, 4 asignaturas |
| B | 5° básico - 2° medio | Prueba separada por asignatura, 25 preguntas c/u, se agrega Inglés |
| C | 3°-4° medio | Prueba separada por asignatura, asignaturas distintas (Ciencias para la Ciudadanía, Filosofía, Educación Ciudadana en vez de Cs. Naturales e Historia) |

Como 4° básico (el piloto) es Régimen A, el paso más simple para escalar es sumar **1°, 2°
y 3° básico** primero — mismo formato de examen (integrado, 4 asignaturas), reutilizando el
motor de contenido/evaluación sin cambios de fondo.

**Estado: ✅ Régimen A completo (2026-08-10)** en cuanto a contenido escrito. Los 4 cursos
(1°-4° básico) tienen contenido íntegro: 771 preguntas de autoevaluación en total, 121/121 OA
oficiales cubiertos en las 4 asignaturas de cada curso. Ver `contenido/00-estado-contenido.md`
para el detalle.

**Importado a la base de datos: ✅ los 4 cursos (2026-08-13).** Régimen A completo también
en base de datos, no solo en archivos — ver Etapa 6 para el detalle de la importación e
validación de los 12 cursos completos.

## Etapa 4 — Extender al Régimen B (5° básico en adelante)

Este salto sí requiere trabajo adicional, no es solo cargar más contenido:

- Soportar el formato de **prueba separada por asignatura** (distinto al integrado de
  Régimen A) — probablemente afecta la UX de autoevaluación y cómo se calcula/presenta el
  progreso.
- Agregar la asignatura **Inglés**, que no existe en 1°-4° básico.
- Considerar el cambio de decreto/nombre de asignaturas entre 6° y 7° básico (439/2012 →
  614/2013; "Lenguaje y Comunicación" → "Lengua y Literatura").

**Estado: ✅ Régimen B completo (2026-08-10).** Los 6 cursos (5° básico a 2° medio) tienen
contenido íntegro: 1.697 preguntas de autoevaluación, 246/246 OA oficiales cubiertos en las
5 asignaturas de cada curso (incluye Inglés desde 5° básico).

## Etapa 5 — Extender al Régimen C (3°-4° medio)

- Currículum de decreto **193/2019**, con asignaturas nuevas que no existen en ningún otro
  nivel (Ciencias para la Ciudadanía, Filosofía, Educación Ciudadana) — este contenido no es
  reutilizable de niveles anteriores, hay que crearlo desde cero.

**Estado: ✅ Régimen C completo (2026-08-10).** Los 2 cursos (3°-4° medio) tienen contenido
íntegro: 449 preguntas de autoevaluación, 41/41 OA oficiales cubiertos en las 6 asignaturas
de cada curso, incluyendo las 3 asignaturas nuevas del Plan Común.

## Etapa 6 — Cobertura completa (los 12 niveles)

- Los 12 niveles disponibles, cubriendo los 3 regímenes de examen.

**Estado: ✅ COMPLETA (2026-08-10) en contenido escrito, ✅ IMPORTADA A LA BASE DE DATOS
(2026-08-13).** Los 12 cursos (1° básico a 4° medio) tienen contenido de estudio íntegro:
**2.917 preguntas de autoevaluación, 408/408 Objetivos de Aprendizaje oficiales cubiertos**
— el 100% de lo extraído de los 12 temarios UCE/Mineduc. Ver `contenido/00-estado-contenido.md`
para el detalle curso por curso y asignatura por asignatura.

**Importación y validación completa (2026-08-13)**: a pedido del usuario ("necesito que
pruebes todos los cursos"), se importaron los 12 niveles a la base de datos local (antes
solo 3 estaban importados) y se corrió una validación automatizada + simulaciones reales con
Playwright (1° básico y 4° medio, cubriendo Régimen A y C) sobre el contenido completo. Esto
expuso y corrigió 3 bugs de parsing adicionales que no aparecían en los 3 cursos ya probados:
- Un tercer formato válido de pregunta ("1. *(Alternativas)*", cursiva, usado en 3°-4°
  medio) que el fix anterior de "negrita obligatoria" rechazaba por error.
- Verdadero/Falso con la explicación pegada a la respuesta en pruebas/exámenes
  ("Verdadero. Es una consecuencia porque...") — mismo problema que el ya corregido en el
  banco de autoevaluación, encontrado también acá.
- **Opciones de alternativas que se ajustan a dos líneas ("word-wrap")** sin repetir la
  letra — la línea de continuación se pegaba al ENUNCIADO en vez de a la opción, dejando
  preguntas con texto contaminado (ej. "...¿cuál de las siguientes NO corresponde? controlados.")
  y una opción truncada. Afectaba ambos parsers.

**Resultado tras corregir y reimportar los 12 cursos**: 2.491 preguntas de
alternativas/verdadero-falso en total, 2.427 (97.4%) con la respuesta ya correctamente
resuelta al texto real de la opción. El 2.6% restante son preguntas de tipo "emparejar"
("Une cada... con...") — mismo formato no soportado por la UI actual, documentado en
`22-analisis-de-brechas.md`, no un bug nuevo. Verificado en vivo con Playwright respondiendo
un examen completo de Filosofía (4° medio, Régimen C) con las respuestas correctas reales:
Nota 7, 16/16 correctas. 133/133 tests backend, 43/43 E2E.
`contenido/00-estado-contenido.md` para el detalle curso por curso y asignatura por
asignatura. Con esto se cumple la condición del usuario de tener "toda la materia lista
antes de comenzar" el desarrollo de la aplicación.

## Etapa 0.5 — Preparación para desarrollo (completa, 2026-08-12)

Con el contenido de los 12 cursos 100% listo, se cerraron las decisiones de producto que
faltaban para poder entregarle el proyecto a un agente/equipo de programación sin
ambigüedades:

- [x] Modelo de negocio definido — `09-modelo-de-negocio.md`.
- [x] Marco legal de privacidad de menores y modelo de registro (Apoderado-primero) —
      `10-privacidad-y-datos-de-menores.md`.
- [x] Rol Administrador confirmado (backoffice interno, no autoservicio en el MVP) —
      `01-roles-y-permisos.md`.
- [x] Especificación técnica completa del MVP (modelo de datos con campos, pantallas,
      flujos, reglas de negocio, fuera de alcance explícito) —
      `11-especificacion-mvp-para-desarrollo.md`.

**Con esto, la Etapa 1 (MVP) está lista para pasar a desarrollo real.**

## Etapa 7+ — Fuera de alcance de esta planificación (por ahora)

- Integración formal con "entidades examinadoras" reales (colegios designados por Mineduc
  que aplican el examen oficial) — podría ser valioso a futuro pero no es parte del MVP.
- Funcionalidades sociales/comunidad, gamificación avanzada, IA generativa para contenido
  personalizado, etc. (ver `06-ideas-futuras.md`).
- Activar cualquier capa de upsell del modelo de negocio (tutorías, acompañamiento en vivo)
  — se decide después de validar el MVP gratuito con usuarios reales.

---

## Curso piloto: 4° básico (decidido)

Se eligió **4° básico** como curso piloto para el MVP. El análisis completo de los temarios
ya está disponible en `Temarios/analisis/04-cuarto-basico.md`: Régimen A (prueba integrada
única, 20 preguntas, 4 asignaturas — Lenguaje y Comunicación, Matemática, Ciencias
Naturales, Historia/Geografía y Cs. Sociales), decreto 439/2012. Ese archivo detalla cada
Objetivo de Aprendizaje con sus indicadores — es la base directa para dimensionar el
material de estudio y el banco de preguntas de autoevaluación del MVP.
