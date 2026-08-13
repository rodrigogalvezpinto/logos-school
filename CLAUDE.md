# Proyecto Logos School — Plataforma de estudio para Exámenes Libres (Chile)

> Este archivo se carga automáticamente al iniciar una conversación de Claude Code en esta
> carpeta. Su función es dar contexto persistente entre conversaciones. Mantenerlo
> actualizado a medida que avanza el proyecto — es la memoria del proyecto, no un historial
> de conversación literal.

**Nombre oficial del producto: "Logos School"** (no solo "Logos") — usar este nombre en
copy de cara al usuario, textos legales, y cualquier lugar donde se nombre la marca.

## Qué es este proyecto

Aplicación web para apoyar el estudio y preparación de niños, niñas y adolescentes que
rendirán los **Exámenes Libres de Validación de Estudios** del Ministerio de Educación de
Chile, de 1° a 8° básico y de 1° a 4° medio. Objetivo: accesible para todos, gratuita o de
muy bajo costo.

**Estado actual: 🚧 Etapa 1 (MVP) + Etapa 2 (Rol Profesor) construidas y verificadas
localmente (2026-08-13), todavía sin desplegar.** Los 12 cursos (1° básico a 4° medio) tienen
contenido de estudio 100% completo: guía de estudio (explicación + ejemplos por OA), banco de
preguntas de autoevaluación (2.917 preguntas, 408/408 OA oficiales), **156 pruebas de
unidad** calibradas por edad (6-15 preguntas según ciclo, ver `planificacion/
08-diseno-pruebas-vs-examenes.md`) y **exámenes tipo simulacro** que imitan exactamente el
formato real de Mineduc (20 preguntas integradas en 1°-4° básico, 25 por asignatura desde 5°
básico — confirmado en los 12 temarios oficiales, 2 formas por curso/asignatura).

Sobre ese contenido ya se construyó la aplicación completa para el curso piloto (4° básico):
backend FastAPI en arquitectura hexagonal + frontend Angular, cubriendo estudiar y rendir
evaluaciones (Fase 1.1), historial y notas por materia (Fase 1.2), Panel de Administrador
comercial (Planes, Descuentos, Cortesías, Métricas), plan de estudio con horario y
habilitación progresiva (Fase 1.3), y el rol Profesor con Curso/Sección (Etapa 2) — ver
`planificacion/03-roadmap-etapas.md` y `planificacion/22-analisis-de-brechas.md` para el
detalle verificado de qué está hecho y qué falta (sobre todo: desplegar a Neon/Render/
Cloudflare Pages, credenciales reales de Google/Resend, pasarela de pago, Turnstile — nada de
esto bloquea seguir desarrollando funcionalidad en local).

**Nota de proceso:** el usuario dio feedback explícito (2026-08-10, ver memoria global
`feedback_no_pedir_confirmaciones`) de no pedir confirmaciones sí/no — actuar con criterio
propio e informar después. Aplica en todo este proyecto.

## Dónde está todo

- `Temarios/` — los 12 temarios oficiales UCE/Mineduc en PDF (fuente de verdad curricular),
  uno por curso, de 1° básico a 4° medio.
- `Temarios/analisis/` — extracción estructurada completa de los 12 PDFs (408 Objetivos de
  Aprendizaje totales, con indicadores de evaluación). Revisar `00-resumen-general.md` ahí
  dentro para la vista comparativa de los 12 niveles.

  **Hallazgo clave:** no son 2 regímenes de examen ("básica" vs. "media"), son **3**, y el
  corte no coincide con el límite básica/media:
  - **Régimen A** (1°-4° básico): prueba integrada única, 20 preguntas, 4 asignaturas,
    decreto 439/2012.
  - **Régimen B** (5° básico-2° medio): prueba separada por asignatura, 25 preguntas c/u,
    se agrega Inglés; decreto 439/2012 (5°-6°) o 614/2013 (7° básico en adelante).
  - **Régimen C** (3°-4° medio): prueba separada por asignatura, currículum de decreto
    193/2019 con asignaturas propias (Ciencias para la Ciudadanía, Filosofía, Educación
    Ciudadana) que no existen en ningún otro nivel — contenido no reutilizable de niveles
    anteriores.
- `planificacion/` — documentos de planificación de producto:
  - `00-vision-alcance.md` — visión, decisiones tomadas, pendientes.
  - `01-roles-y-permisos.md` — perfiles Alumno / Apoderado / Profesor / Administrador
    (propuesto) y qué puede hacer cada uno.
  - `02-modelo-de-datos-conceptual.md` — entidades (Nivel, Asignatura, OA, Curso/Sección,
    Usuario, Progreso) y sus relaciones.
  - `03-roadmap-etapas.md` — etapas de construcción, desde el piloto de un solo curso hasta
    la cobertura completa de los 12 niveles.
  - `04-modo-de-operacion.md` — **leer siempre**: define que opero de forma autónoma como
    profesor/educador experto, produciendo contenido pedagógico con criterio propio y
    preguntando al usuario solo lo mínimo indispensable. Explica qué decido solo y qué no.
  - `05-tipos-de-contenido.md` — define 3 tipos de contenido por curso: guía, pruebas por
    materia y exámenes tipo simulacro (Forma A/B). Todo completo.
  - `07-experto-examenes-libres.md` — base de conocimiento del **trámite administrativo**
    real de los Exámenes Libres (inscripción, 3 periodos al año —no solo octubre—, entidad
    examinadora asignada automáticamente, qué pasa si repruebas, recorrección, certificado).
    Fuente de verdad para responder dudas de apoderados.
  - `08-diseno-pruebas-vs-examenes.md` — separación entre pruebas de unidad (formativas,
    tamaño calibrado por edad) y exámenes simulacro (imitan exactamente el examen real).
  - `09-modelo-de-negocio.md` — Logos **tendrá planes de pago** (no es un modelo
    "siempre gratis"), modelado sobre Wited (plataforma chilena real investigada en
    profundidad: planes Basic/Lite/Full ~$89.000-$194.000/mes). Sin publicidad dirigida a
    menores en ningún caso.
  - `10-privacidad-y-datos-de-menores.md` — registro **simple, sin verificación de
    identidad** (modelo Wited): el apoderado —o cualquier adulto que matricule— crea la
    cuenta y agrega alumnos con nombre, apellidos, fecha de nacimiento y RUT. Logos no es un
    colegio legalizado ante Mineduc, es una plataforma de ayuda de estudio — el registro no
    debe tener fricción de trámite gubernamental (ver nota de feedback en memoria global).
  - `11-especificacion-mvp-para-desarrollo.md` — **punto de partida para desarrollo**:
    modelo de datos con campos concretos, pantallas, flujos y reglas de negocio del MVP
    (4° básico, Alumno + Apoderado, con planes de pago).
  - `12-motor-de-evaluacion.md` — flujo de "rendir" una prueba/examen (cronómetro,
    navegación pregunta a pregunta, autosave, cálculo de nota escala 1.0-7.0 con exigencia
    60%, resumen final con desglose por OA/asignatura).
  - `13-plan-de-estudio.md` — horario de estudio (3/4/5 días por semana), reparte el
    contenido pendiente en sesiones para que el alumno estudie de forma ordenada.
  - `14-preguntas-frecuentes-apoderados.md` — copy base de ventas/landing (qué responder a
    un apoderado sobre cobertura, evaluación y seguimiento de avance).
  - `15-diseno-visual-y-marca.md` — paleta de colores, tipografía y criterio UX (índigo
    `#5B4FE9` + coral `#FF6B4A`, Poppins/Inter, un solo sistema que "madura" visualmente
    entre básica inicial y media, sin tocar la identidad).
  - `16-navegacion-y-panel-de-control.md` — flujo de login → selector de perfil → panel,
    estructura completa de la barra lateral (sidebar) de Alumno y Apoderado, y el camino de
    crecimiento futuro (chatbot, voz, rol Profesor, gamificación) sin romper lo construido.
  - `22-analisis-de-brechas.md` — auditoría verificada contra el código real de qué falta:
    Front sin conectar al backend, pruebas/exámenes sin importar, pagos/Google/correo con
    credenciales pendientes, nada desplegado todavía. Léelo antes de asumir que algo "ya
    funciona".
  - `21-accesibilidad-lectura-y-contenido-visual.md` — lectura en voz alta gratuita (Web
    Speech API) para 1°-2° básico, y componentes visuales propios (recta numérica, modelo
    de fracciones, figuras geométricas) para Matemática, en vez de imágenes sueltas.
  - `24-reforzamiento-con-profesores.md` — investigación (no implementado, el usuario pidió
    explícitamente solo planificar) de un posible marketplace de clases pagadas con
    profesores, inspirado en wited.com/cl/reforzamiento — preguntas de negocio abiertas
    (marketplace abierto vs. curado, pagos, seguridad del menor en videollamada 1-a-1) antes
    de diseñar nada.
  - `17-infraestructura-y-entornos.md` — **regla no negociable: ambientes Desarrollo y
    Producción separados desde el día uno**, cada uno con su propia base de datos (Neon,
    Postgres con branches). Backend en Render, frontend Angular en Cloudflare Pages, correo
    con Resend, monitoreo con Sentry + UptimeRobot — todo con plan gratuito para partir.
    Login con Google además de email/contraseña.

  **Stack técnico decidido (2026-08-12):** Python (FastAPI) + Angular + PostgreSQL — ver
  `11-especificacion-mvp-para-desarrollo.md`. **Empresa** (no fundación) — ver
  `09-modelo-de-negocio.md`, que incluye los planes de pago concretos (tope $19.990 CLP/mes,
  con opción por periodo de examinación y anual con descuento). Pasarela de pago: pendiente
  de definir, no bloquea el resto del desarrollo.

  **Construcción de la app en 3 fases dentro de la Etapa 1 (MVP)** — ver
  `03-roadmap-etapas.md`: **Fase 1.1** estudiar + rendir evaluaciones (lanzable sola),
  **Fase 1.2** historial y notas por materia, **Fase 1.3** plan de estudio con horario.
- `.claude/agents/experto-examenes-libres.md` — agente experto (trámite + contenido del
  proyecto) invocable con el Agent tool; prototipo del futuro chatbot de la aplicación.
- `contenido/` — el contenido de estudio real (explicaciones, ejemplos, bancos de preguntas
  de autoevaluación) para cada curso/asignatura, producido siguiendo `04-modo-de-operacion.md`.
  **Completo para los 12 cursos.** Ver `contenido/00-estado-contenido.md` para el detalle
  curso por curso y asignatura por asignatura (2.917 preguntas, 408/408 OA).

## Regla no negociable: toda la materia lista antes de construir la app

El usuario fue explícito: **no se construye la aplicación hasta que el contenido de estudio
esté completo**. Esa condición **ya se cumplió** (2026-08-10): los 12 cursos tienen contenido
íntegro. El desarrollo de software (Etapa 1+ del roadmap) puede comenzar cuando el usuario lo
indique — no asumir que debe iniciarse automáticamente solo porque el contenido está listo,
ya que construir la app es un cambio de fase que probablemente el usuario quiera confirmar
explícitamente (elección de stack técnico, etc.).

**Empezar cualquier conversación nueva sobre este proyecto leyendo `planificacion/
00-vision-alcance.md`** para entender el estado y las decisiones vigentes.

## Decisiones ya tomadas (no volver a preguntar salvo que el usuario quiera revisarlas)

1. **MVP = un curso piloto único: 4° básico** (no los 12 niveles a la vez). Formato de
   examen esperado (a confirmar en `Temarios/analisis/`): prueba integrada, 4 asignaturas
   (Lenguaje, Matemática, Ciencias Naturales, Historia/Geografía y Cs. Sociales).
2. **Autoestudio primero**: el MVP no tiene profesores humanos activos. El rol Profesor se
   diseña desde ahora en el modelo de datos, pero se activa en una etapa posterior.
3. **Modelo de "curso" de dos niveles**:
   - *Nivel* = el año que cursa el alumno (ej. "6° básico"). Autoasignado libremente por el
     alumno al registrarse. Da acceso al material de estudio de ese nivel.
   - *Curso/Sección* (ej. "6° básico A", ~15 alumnos) = grupo con roster gestionado
     exclusivamente por un Profesor. El alumno **no puede autoagregarse** — solo un
     profesor lo agrega. Es opcional, no bloquea el estudio individual.
4. **Modelo de negocio definido (2026-08-12)**: Logos es una **empresa** (no fundación),
   con planes de pago (tope $19.990 CLP/mes, opción por periodo de examinación y anual con
   descuento) — ver `planificacion/09-modelo-de-negocio.md` para el detalle completo.

## Cómo colaborar en este proyecto

- El usuario prefiere avanzar en **etapas**, con cimientos sólidos antes de construir.
- Está autorizado crear carpetas y archivos sin pedir permiso cada vez.
- El público objetivo son **menores de edad** — cualquier decisión de datos personales,
  verificación de identidad (apoderados, profesores) o privacidad debe tratarse con
  cuidado explícito, no como detalle técnico tardío (ver la sección de seguridad/privacidad
  en `planificacion/01-roles-y-permisos.md`).
- Cuando se tome una decisión de producto nueva, registrarla en la tabla de "Decisiones
  tomadas" de `planificacion/00-vision-alcance.md` y reflejarla aquí si es lo bastante
  central para el contexto general del proyecto.
