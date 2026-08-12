---
título: Especificación del MVP lista para desarrollo
estado: lista para entregar a un agente/equipo de programación (2026-08-12)
última actualización: 2026-08-12
---

## Propósito de este documento

Este es el documento de entrega técnica: reúne todas las decisiones de producto ya tomadas
en `planificacion/` en una especificación concreta y accionable, para que quien programe la
aplicación (humano o agente experto en desarrollo) pueda empezar sin tener que volver a
tomar decisiones de producto ni pedirlas de vuelta. Fija el stack técnico (ver más abajo),
qué hay que construir, qué datos maneja, y qué reglas de negocio aplican.

**Alcance de esta especificación: Etapa 1 del roadmap únicamente** — el MVP piloto de
**4° básico**, modo autoestudio, roles Alumno y Apoderado (sin Profesor/Curso-Sección
activo todavía, ver `03-roadmap-etapas.md`).

## Stack técnico (decidido 2026-08-12)

- **Backend: Python con FastAPI.** Se prefiere sobre Django porque el proyecto no necesita
  admin panel ni ORM pesado desde el día uno — FastAPI es más liviano, tipado (encaja bien
  con el modelo de datos ya definido campo por campo abajo), y rápido de levantar como API
  que consume el frontend Angular.
- **Frontend: Angular.**
- **Base de datos: PostgreSQL**, no MongoDB. El modelo de datos de este documento es
  **fuertemente relacional** (Cuenta → PerfilAlumno → Suscripción; Nivel → Asignatura → OA →
  Pregunta → ConjuntoEvaluacion; IntentoEvaluacion con múltiples llaves foráneas) — es
  exactamente el caso de uso para el que una base relacional es más simple y segura (
  integridad referencial, JOINs directos para armar el dashboard de progreso) que un
  documento NoSQL, sin perder liviandad: PostgreSQL corre perfectamente en un plan de
  hosting económico para el volumen de usuarios esperado en el MVP.
- **ORM sugerido:** SQLAlchemy (o SQLModel, que combina bien con FastAPI) para mapear
  directamente las entidades ya definidas más abajo.
- **Importación de contenido semilla:** un script Python que parsea los archivos Markdown ya
  escritos en `contenido/04-basico/` y los carga a las tablas `Nivel`/`Asignatura`/
  `ObjetivoAprendizaje`/`Pregunta`/`ConjuntoEvaluacion` — se ejecuta una vez por curso que se
  agregue, no es parte de la app en producción.

## Orden de lectura recomendado para quien programe

1. `00-vision-alcance.md` — qué es el proyecto y por qué.
2. `01-roles-y-permisos.md` — roles y qué puede hacer cada uno.
3. `02-modelo-de-datos-conceptual.md` — entidades a nivel conceptual.
4. `10-privacidad-y-datos-de-menores.md` — restricciones legales no negociables.
5. `09-modelo-de-negocio.md` — por qué sí hay pagos en el MVP y cómo están estructurados los planes.
6. **Este documento** — la traducción de todo lo anterior a pantallas, flujos y modelo de
   datos concreto.
7. `12-motor-de-evaluacion.md` — el flujo detallado de "rendir" una guía/prueba/examen
   (cronómetro, navegación, cálculo de nota) — es el corazón interactivo de la Fase 1.1.
8. `13-plan-de-estudio.md` — el horario de estudio (3/4/5 días por semana) de la Fase 1.3.
9. `Temarios/analisis/04-cuarto-basico.md` y `contenido/04-basico/` — el contenido real que
   hay que servir en la app (ya escrito, no hay que generarlo).

**Nota sobre fases:** este documento describe el modelo de datos y pantallas del MVP
completo (4° básico). La Fase 1.1 (`03-roadmap-etapas.md`) puede lanzarse solo con las
pantallas 1-12 de abajo, dejando 13-14 y el Plan de Estudio para las Fases 1.2/1.3.

## Modelo de datos (campos concretos, no solo entidades)

Nomenclatura en español para que coincida con el resto del proyecto; los tipos son
orientativos, no impone un motor de base de datos específico.

```
Cuenta (Apoderado — o cualquier adulto que matricula, no necesariamente padre/madre)
  id
  email                 (único, usado para login)
  password_hash
  nombre
  comuna_o_region        (opcional, solo para estadística agregada de zona geográfica)
  pais                   (opcional, mismo fin)
  fecha_creacion

PerfilAlumno
  id
  cuenta_apoderado_id   (FK → Cuenta)
  nombre
  apellidos
  fecha_nacimiento
  rut
  nivel_id               (FK → Nivel; fijo a "4° básico" en el MVP, pero el campo existe
                           desde ya para no rediseñar al expandir a otros niveles)
  plan_id                 (FK → Plan; ver más abajo — sin plan activo, acceso restringido)
  fecha_creacion

Plan
  id
  nombre                 ("Entrada", "Completo" — nombres/montos finales por definir,
                           ver 09-modelo-de-negocio.md)
  nivel_de_acceso         ("entrada" | "completo") — determina qué contenido desbloquea

Suscripcion               (dato vivo — el pago real de un PerfilAlumno a un Plan)
  id
  perfil_alumno_id        (FK → PerfilAlumno)
  plan_id                 (FK → Plan)
  fecha_inicio
  fecha_termino            (nullable si sigue activa)
  estado                  ("activa" | "vencida" | "cancelada")

Nivel                    (datos semilla, se cargan una vez desde Temarios/analisis/)
  id
  nombre                 ("4° básico")
  regimen                ("A" | "B" | "C")
  decreto                ("439/2012")
  formato_examen         ("integrado" | "separado_por_asignatura")
  num_preguntas_examen   (20 para Régimen A; 25 para B/C)
  duracion_examen_min    (90)
  materiales_permitidos  (texto libre, ej. "calculadora desde 5° básico")

Asignatura               (datos semilla)
  id
  nivel_id               (FK → Nivel)
  nombre                 ("Matemática", "Lenguaje y Comunicación", ...)

ObjetivoAprendizaje (OA) (datos semilla)
  id
  asignatura_id          (FK → Asignatura)
  codigo_oficial          (ej. "OA 7")
  descripcion
  eje_tematico            (nullable — no todas las asignaturas tienen ejes)
  contenido_guia          (el texto explicativo + ejemplos, importado de contenido/{curso}/{asignatura}.md)

Pregunta                 (datos semilla, del banco ya escrito en contenido/)
  id
  oa_id                  (FK → ObjetivoAprendizaje)
  tipo                   ("alternativas" | "verdadero_falso" | "desarrollo_breve" | "clasificar" | ...)
  enunciado
  opciones               (json, nullable — solo para alternativas)
  respuesta_correcta
  retroalimentacion
  nivel_dificultad        ("simple" | "intermedio" | "desafiante", si el banco lo distingue)

ConjuntoEvaluacion       (una "prueba de unidad" o un "examen simulacro")
  id
  tipo                   ("prueba_unidad" | "examen_simulacro")
  asignatura_id           (FK → Asignatura; nullable si es examen integrado de Régimen A)
  nivel_id                (FK → Nivel; usado cuando el examen es integrado, no por asignatura)
  nombre                  ("Matemática — Unidad: Geometría", "Examen integrado Forma A")
  forma                   ("A" | "B" | null — solo aplica a exámenes simulacro)
  pregunta_ids            (lista ordenada de Pregunta)
  tiempo_sugerido_min

IntentoEvaluacion         (dato vivo — lo genera el uso real; ver 12-motor-de-evaluacion.md)
  id
  perfil_alumno_id        (FK → PerfilAlumno)
  conjunto_evaluacion_id  (FK → ConjuntoEvaluacion)
  fecha_inicio
  fecha_termino
  respuestas              (json: pregunta_id → respuesta dada)
  puntaje                 (calculado)
  nota                    (calculado, escala 1.0-7.0, solo para prueba_unidad/examen_simulacro;
                            null para autoevaluación formativa — ver fórmula en
                            12-motor-de-evaluacion.md)
  tiempo_usado_seg

ProgresoOA                (dato vivo, derivado o materializado desde IntentoEvaluacion)
  perfil_alumno_id        (FK → PerfilAlumno)
  oa_id                   (FK → ObjetivoAprendizaje)
  estado                  ("no_iniciado" | "en_progreso" | "dominado")
  ultimo_intento_fecha

PlanDeEstudio / SesionEstudio   (Fase 1.3 — ver 13-plan-de-estudio.md para el detalle completo)
```

**Nota de implementación:** `Nivel` → `Asignatura` → `ObjetivoAprendizaje` → `Pregunta` →
`ConjuntoEvaluacion` son datos semilla que ya existen como contenido escrito en Markdown
(`contenido/04-basico/*.md`, `contenido/04-basico/pruebas/*.md`,
`contenido/04-basico/examenes/*.md`). No hay que redactar contenido nuevo para el MVP — hay
que **parsear/importar** ese contenido ya validado pedagógicamente a esta estructura. Vale
la pena escribir un script de importación una sola vez en vez de traspasar todo a mano.

## Pantallas y flujos (MVP)

1. **Landing pública** (sin login) — explica qué es Logos y sus planes, un solo CTA:
   "Crear cuenta".
2. **Registro de Apoderado** — email, contraseña, nombre (modelo Wited, ver
   `10-privacidad-y-datos-de-menores.md`: registro simple, sin verificación de identidad).
3. **Agregar alumno(s)** — indicar cuántos alumnos se van a inscribir y completar por cada
   uno: nombre, apellidos, fecha de nacimiento, RUT, nivel (en el MVP, fijo a "4° básico").
4. **Selección de plan y pago** — por cada Perfil de Alumno creado, elegir Plan (Entrada o
   Completo, ver `09-modelo-de-negocio.md`) y completar el pago antes de habilitar el
   acceso. Sin Suscripción activa, el Perfil queda creado pero sin acceso al contenido.
5. **Dashboard del Apoderado** — lista de Perfiles de Alumno, estado de su Plan/Suscripción,
   botón "Agregar otro alumno".
6. **Selector de perfil** (patrón tipo Netflix) — al entrar a la cuenta, elegir con qué
   Perfil de Alumno continuar, o entrar como Apoderado a ver progreso.
7. **Vista Alumno — Home** — las 4 asignaturas de 4° básico (Lenguaje y Comunicación,
   Matemática, Ciencias Naturales, Historia/Geografía y Cs. Sociales), con indicador visual
   de avance por asignatura.
8. **Vista Alumno — Asignatura** — lista de OA de esa asignatura, con estado
   (no_iniciado/en_progreso/dominado) y acceso a: Guía, Autoevaluación, Pruebas de unidad.
9. **Vista Alumno — Estudiar OA** — contenido de la guía + ejemplos (ya escrito en
   `contenido/04-basico/{asignatura}.md`, importado como `contenido_guia`).
10. **Vista Alumno — Autoevaluación por OA** — preguntas del banco de ese OA específico,
    feedback inmediato pregunta a pregunta (no cronometrado, es formativo).
11. **Vista Alumno — Prueba de unidad** — modo cronometrado (~15-25 min según
    `planificacion/08-diseno-pruebas-vs-examenes.md`), sin feedback hasta el final, pauta de
    respuestas completa al terminar.
12. **Vista Alumno — Examen simulacro** — modo cronometrado estricto (90 min), 20 preguntas
    integrando las 4 asignaturas (formato real Régimen A), sin pausas, resultado final con
    desglose por asignatura al terminar. Debe sentirse deliberadamente distinto/más serio
    que una prueba de unidad — es el ensayo de la condición real.
13. **Vista Apoderado — Progreso de [Alumno]** — resumen visual de avance por asignatura y
    por OA, historial de intentos (pruebas y exámenes rendidos, puntajes).
14. **Configuración de cuenta** — editar datos del Apoderado, gestionar Plan/Suscripción de
    cada Alumno, ver/exportar/eliminar los datos de cada Alumno vinculado, eliminar un
    Perfil de Alumno.

## Reglas de negocio clave (no delegar la decisión, ya están tomadas)

- El acceso al contenido (Guía, Autoevaluación, Pruebas de unidad, Exámenes simulacro) está
  ligado al **Plan/Suscripción activa** de cada Perfil de Alumno — sí hay sistema de pagos
  en el MVP (ver `09-modelo-de-negocio.md`). Los montos y si existe un nivel gratuito de
  entrada quedan por definir; la infraestructura de planes debe existir desde el inicio.
- Un Alumno **no puede** autoagregarse ni existir sin una Cuenta de Apoderado que lo haya
  creado — pero el registro en sí es simple, sin verificación de identidad adicional (ver
  `10-privacidad-y-datos-de-menores.md`).
- Las Pruebas de unidad **no** deben verse ni sentirse como el examen real (distinto de los
  Exámenes simulacro) — son más cortas, formativas, sin la presión de tiempo estricta del
  examen real. Mantener esta diferencia de tono en la UI, no solo en la cantidad de
  preguntas.
- Ningún dato de un Alumno se usa para publicidad ni tracking de terceros con fines
  comerciales (ver `10-privacidad-y-datos-de-menores.md`) — esto no cambia por tener planes
  pagos: los ingresos vienen de las suscripciones, no de vender datos ni de publicidad.

## Explícitamente fuera de alcance del MVP

Para que quien programe no se desvíe agregando cosas no pedidas todavía:

- Plan "con acompañamiento" (tutorías humanas, corrección personalizada) — es fase
  posterior; el MVP solo necesita los planes de autoestudio (Entrada/Completo).
- Rol Profesor y Curso/Sección (Etapa 2 del roadmap — el modelo de datos de `Nivel` ya
  soporta agregarlo después sin romper lo existente, pero no se construye su UI ahora).
- Más de un Nivel (solo 4° básico; el modelo de datos ya es multi-nivel para no tener que
  rediseñar, pero el contenido semilla a cargar en el MVP es solo el de 4° básico).
- Gamificación, insignias, evaluador de lectura en voz alta u otras ideas de
  `06-ideas-futuras.md` — quedan en el backlog, no en el MVP.
- Chatbot conversacional (existe un prototipo de agente experto en
  `.claude/agents/experto-examenes-libres.md`, pero convertirlo en feature de producto
  dentro de la app es una decisión posterior, no del MVP).

## Criterio de éxito del MVP

El mismo ya definido en `03-roadmap-etapas.md`: un grupo real de alumnos de 4° básico puede
estudiar de principio a fin con el material de la plataforma (guía → autoevaluación →
pruebas de unidad → examen simulacro) y sentir que cubre lo que el temario oficial exige,
con sus apoderados pudiendo seguir el progreso sin fricción.
