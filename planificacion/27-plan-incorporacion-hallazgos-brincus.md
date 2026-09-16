---
título: Plan de incorporación — hallazgos de Brincus a Logos School
estado: planificación (2026-08-14) + segunda tanda de construcción en vivo (2026-08-15,
  comparando directo contra la cuenta de prueba real de Brincus), piloto en 4° básico
---

## Actualización 2026-08-15 — construido en vivo, comparando contra la cuenta real de Brincus

Con la cuenta de prueba real del usuario (día 1, todavía activa) se hizo un recorrido
completo por Brincus (4° básico) y uno equivalente por Logos, corrigiendo brechas reales
sobre la marcha. Piloto en 4° básico, pensado para replicar al resto de los cursos después de
validarlo. Construido y verificado (348 tests backend + 83 Playwright en verde):

- **"Estudiar" separado en 2 pasos explícitos** (Aprender → Practicar, con indicador visual
  de progreso) — antes era una sola página larga con la guía y el botón de practicar al
  final. Bonus: al quedar "Aprender" (explicación + ejemplos) como su propia pieza, ya es la
  unidad de contenido lista para usarse como guion si más adelante se generan videos.
- **Historial de intentos visible junto a cada prueba/examen** en "Pruebas y Exámenes" (antes
  había que ir a "Mis Notas" aparte) — `ConjuntoRespuesta.intentos_entregados`/`ultima_nota`.
- **Bug real corregido**: retomar una prueba/examen a medio hacer no restauraba las
  respuestas ya guardadas en el frontend (el backend sí las tenía) — el alumno veía todo en
  blanco de nuevo. Corregido en `EvaluacionRunner`.
- **Bug real corregido**: recargar la página a mitad de un examen reiniciaba el cronómetro al
  tiempo completo, contradiciendo el aviso "Sin pausas" — ahora usa `fecha_inicio` real del
  intento.
- **Explicación en lenguaje simple de "Prueba de unidad" vs. "Examen simulacro"**, visible en
  la propia pantalla de "Pruebas y Exámenes" (Brincus lo hace con sus 4 tipos de evaluación).
- **Buscador de contenido por palabra** dentro del temario de una asignatura.
- **Duración estimada visible por OA** ("~2 min de lectura") — adaptado de la duración de
  video que muestra Brincus; Logos no tiene video, así que se estima tiempo de lectura desde
  el propio `contenido_guia`, sin pedir nada nuevo al backend.
- **Plan Lector** — ver fila corregida en la tabla de auditoría más abajo: pasó de "No existe"
  a construido, piloto en 4° básico (`backend/app/routers/plan_lector.py`,
  `frontend/src/app/pages/plan-lector/`), 4 libros elegidos con criterio propio
  (`planificacion/04-modo-de-operacion.md`): Papelucho, El Principito, Matilda, Charlie y la
  fábrica de chocolate.
- Auditoría de accesibilidad (axe-core) extendida a todas las pantallas nuevas — encontró y
  corrigió contraste real en varias insignias de color nuevas.

**Deliberadamente NO se tocó hoy**: Biblioteca de recursos descargables (Fase 2 — a
diferencia del Plan Lector, que es solo información bibliográfica, una Biblioteca implica
decidir licencias de distribución de archivos, no es una decisión que corresponda tomar
solo) y el pulido visual "más lúdico" (paleta más saturada, ilustraciones) — el usuario pidió
explícitamente dejarlo para el final, después de la lista de funcionalidad.

## Actualización 2026-08-15 (segunda tanda) — cierre de las brechas de la evaluación honesta

Tras la tanda anterior, se hizo una evaluación honesta de qué faltaba frente a Brincus más
allá de video/juegos/IA (7 brechas). El usuario pidió cerrarlas todas ("necesito que
continues a fondo donde lo unico que nos quede de diferencias sea que no tenemos IA dentro
de la app, juegos, y videos"), autorizando usar librerías/skills si hacía falta. Se decidió
**no sumar ninguna librería nueva de iconos/insignias** — las 12 insignias del catálogo de
Logros usan emoji, consistente con el patrón de "Fase 1 sin dependencias externas" ya
aplicado en el resto de la app. Construido y verificado (370 tests backend + 270 Playwright
en verde, 3 navegadores):

1. **Gamificación — Logros/insignias por hábito** (`app/domain/gamificacion/entities.py`):
   catálogo de 12 logros (3 niveles × 4 categorías: racha de días seguidos, guías revisadas,
   evaluaciones entregadas, nivel de XP), racha calculada por fecha real de actividad (no
   inflable el mismo día), grilla de insignias en "Mis Logros" con las bloqueadas en
   grayscale (exceptuadas de axe-core con el mismo criterio ya usado para UI inactiva).
2. **Plan de Estudio — repaso de años anteriores**: nuevo flujo para agregar una sesión de
   repaso de un curso ya cursado al final del plan activo, sin tocar el resto. Al construirlo
   se encontró un bug de datos real y serio: `Nivel.id` no sigue el orden curricular en la
   base de Desarrollo (4° básico, el piloto, se importó primero y quedó con `id=1`, mientras
   1°-3° básico quedaron con ids más altos) — cualquier lógica que asumiera "id menor = curso
   anterior" fallaba silenciosamente, y de hecho fallaba para el propio piloto. Se agregó
   `Nivel.orden` (1=1° básico...12=4° medio) como único criterio válido de orden curricular,
   con migración de backfill y `scripts/importar_contenido.py` actualizado para futuros
   imports. La vista "Anual" propuesta originalmente se descartó por criterio propio: es
   redundante con la vista "Mensual" ya construida, no aporta suficiente diferenciación para
   justificar otra pestaña.
3. **"Ensayos" (facsímil anual)**: se verificó que esta brecha ya estaba cerrada sin saberlo
   — el "Examen integrado Forma A/B" de régimen A (4° básico, el piloto) ya es exactamente
   eso: un facsímil único, cronometrado, con las 4 asignaturas juntas, ya distinguido en la
   UI de "Prueba de unidad" desde la tanda anterior. No se construyó nada nuevo para no
   duplicar.
4. **Informe de avance en PDF para el Apoderado** (`generador_informe_avance.py`, endpoint
   `GET /auth/alumnos/{id}/informe-avance.pdf`, botón en "Mis Notas"): reutiliza los mismos
   datos que ya arma `ObtenerHistorialYNotas` — notas por asignatura, últimas evaluaciones,
   racha y logros — solo los empaqueta en PDF con la misma identidad de marca que el
   certificado de alumno regular. Bug real encontrado y corregido durante la verificación:
   un guion largo ("—") sin sanitizar en el marcador de nota ausente tumbaba la generación
   completa del PDF con `FPDFUnicodeEncodingException` (la fuente Helvetica core no soporta
   ese carácter) — el test que sí ejercitaba una evaluación entregada real lo detectó.
5. **Búsqueda global de contenido** (`shared/busqueda-global/`, visible en la topbar de
   cualquier página del Alumno): busca por código de OA, descripción o contenido de guía en
   todas las asignaturas del nivel a la vez, a diferencia del buscador ya existente en
   `asignatura-detalle.ts` que solo filtra dentro de una asignatura ya abierta. Sin backend
   de búsqueda de texto completo nuevo — carga y cachea el contenido del nivel una sola vez,
   igual volumen de datos que ya recorre el buscador por asignatura.
6. **Botón de ayuda contextual** (`shared/ayuda-contextual/`, sin IA): botón flotante con un
   tip corto según la página en la que está el usuario (Plan de Estudio, Evaluaciones, Notas,
   Logros, etc.) más un link a Preguntas Frecuentes. Se descartó deliberadamente un botón
   "Contactar soporte" con un correo — Logos School todavía no tiene un canal de soporte real
   operando, y un `mailto:` que nadie revisa sería peor que no ofrecer nada.
7. **Bug de test real encontrado y corregido en el camino** (Rol Profesor, Etapa 2, no parte
   de esta lista pero descubierto durante la verificación final): el selector de nivel al
   crear un Curso/Sección no tenía ningún valor por defecto garantizado (mismo bug de fondo
   que el punto 2 — sin `ORDER BY orden`, Postgres no garantiza qué nivel queda primero), y
   el test E2E de Profesor tenía además dos tablas con el mismo `tbody tr` sin distinguir
   (roster vs. resultados de búsqueda), lo que enmascaraba el fallo real. Se corrigió
   `listar_niveles()` para ordenar por `orden`, y el test para elegir el nivel explícito y
   distinguir ambas tablas.

**Estilo visual "más lúdico" (paleta más saturada, ilustraciones)**: sigue sin tocarse, tal
como pidió el usuario explícitamente — es lo único que queda pendiente de la lista original
de 7, además de video/juegos/IA que están fuera de alcance a propósito.

## Actualización 2026-08-15 (tercera tanda) — loop autónomo, comparando de nuevo contra Brincus

El usuario pidió explícitamente un ciclo autónomo: comparar contra Brincus, cerrar la
siguiente brecha de mayor costo/beneficio, verificar, volver a comparar, repetir sin
preguntar entre pasos — hasta que no quede nada razonable por cerrar salvo lo ya excluido a
propósito (IA, juegos, video, clases en vivo, Mis Tareas, comunicación 1 a 1, Biblioteca con
licencias). Brechas identificadas antes de empezar este loop (release honesto, ver Paso 12
de `planificacion/25-analisis-competencia-brincus.md`): centro de notificaciones, vista de
avance de contenido separada de notas, lista de Útiles Escolares, logros por tiempo de
sesión, estado "no finalizada" en Plan de Estudio.

1. **Útiles Escolares por nivel** (`app/domain/utiles_escolares/`, endpoint público
   `GET /utiles-escolares/nivel/{id}`, página `pages/utiles-escolares/`, entrada de sidebar
   🎒): lista curada de 10 materiales para 4° básico, agrupada por asignatura con
   "Materiales generales" primero. Mismo patrón que Plan Lector (solo lectura, sin sesión,
   sin dependencias externas). Verificado: 373 tests backend + Playwright (3 navegadores,
   accesibilidad incluida) en verde.
2. **Plan de Estudio — estado "no finalizada"** (`SesionRespuesta.atrasada`, calculado al
   vuelo en el router con `fecha_programada < hoy`, sin persistir): distingue una sesión
   vencida sin cumplir de una simplemente pendiente, con su propio chip rojo "Atrasada" —
   hallazgo comparando en vivo contra Brincus (Paso 12: "Finalizadas / Pendientes / No
   finalizadas"). Verificado: 374 tests backend en verde.
3. **Logros por tiempo dedicado** (3 nuevos: 30 min / 2 h / 5 h, categoría "tiempo" en el
   catálogo, ahora 15 logros): se mide con `tiempo_usado_seg`, el mismo dato que ya calcula
   `IntentoEvaluacion.entregar()` para el cronómetro — tiempo real invertido rindiendo
   pruebas/exámenes, sumado en `PerfilGamificacion.tiempo_evaluando_total_seg`. Deliberadamente
   NO es tiempo de sesión de toda la app (eso exigiría un heartbeat cliente→servidor
   periódico, infraestructura nueva no justificada todavía) — se prefirió un proxy honesto
   sobre datos que ya existían, en vez de construir tracking nuevo. Verificado: 377 tests
   backend + Playwright (3 navegadores) en verde.
4. **"Avance de contenido" separado de las notas** (sección nueva en "Mis Notas", antes de
   "Notas por asignatura", con barra de progreso por asignatura): hallazgo comparando en
   vivo contra Brincus (Paso 12: separa "Progreso"/Ruta de aprendizaje de "Calificaciones",
   con el lenguaje explícito "cuánto contenido llevo visto" vs. "qué notas tengo"). Sin
   backend nuevo — reutiliza `CoberturaAsignatura.cobertura_pct`, que `/progreso/{id}/faltantes`
   ya calculaba para habilitar el simulacro parcial. Solo visible para el propio alumno
   (mismo criterio ya aplicado a esa sección). Verificado: Playwright (3 navegadores,
   accesibilidad incluida) en verde.
5. **Centro de notificaciones** (`app/application/notificaciones/consultas.py`,
   `GET /notificaciones/{id}`, campana 🔔 en la topbar del Alumno con panel desplegable):
   hallazgo comparando en vivo contra Brincus (Paso 12: campana con Notificaciones /
   Preguntas y Respuestas / Errores reportados — la parte de "Preguntas y Respuestas" no
   aplica, requiere chat/IA, Fase 2). Deliberadamente NO es un agregado nuevo con estado
   leído/no-leído persistido — es una vista compuesta calculada al vuelo sobre 3 fuentes que
   ya existían: comunicados del curso (`ObtenerMiCurso`), sesiones de Plan de Estudio
   atrasadas (`ObtenerPlanActivo` + el campo `atrasada` del punto 2), y reportes de error
   propios ya resueltos (nuevo `RepositorioReportesError.listar_por_perfil`). Verificado:
   385 tests backend + 288 Playwright (3 navegadores, accesibilidad incluida) en verde.
6. **Buzón de sugerencias** (`app/domain/sugerencias/`, `POST/GET /sugerencias/{id}`,
   sección "Ideas para mejorar Logos School" en Configuración): segunda vuelta comparando
   contra Brincus tras cerrar la lista original — el Paso 13 del análisis (índice de
   Tutoriales) menciona "¿Cómo doy ideas para mejorar la plataforma?" como canal explícito y
   visible, no escondido en un correo de soporte. Mismo patrón que `ReporteError` — se
   guarda el dato, sin bandeja de revisión de Admin todavía (mismo alcance que ya tienen los
   reportes de error). Bug real de accesibilidad encontrado y corregido en el camino: el
   `<label>Nombre</label>` de "Mi perfil" en Configuración nunca estuvo asociado a su
   `<input>` (sin `for`/`id`) — nadie había corrido axe-core sobre esa página hasta ahora.
   Verificado: 394 tests backend + 297 Playwright (3 navegadores, accesibilidad incluida)
   en verde.

Este documento traduce `planificacion/25-analisis-competencia-brincus.md` (qué hace Brincus)
en un plan concreto de qué construir en Logos School, en qué orden, y contrastado línea por
línea contra lo que **ya existe hoy** en el código (verificado, no supuesto — ver auditoría
más abajo). Es un documento de planificación: no se construye nada de lo que sigue hasta que
el usuario apruebe el plan, salvo lo que ya se ejecutó y quedó marcado como hecho.

## 0. Confirmado con el usuario (2026-08-14)

- Logos y Brincus tienen el mismo objetivo de fondo (preparar Exámenes Libres), con una
  diferencia de alcance ya decidida: Logos no tendrá profesores humanos en vivo. En su lugar,
  la vía de "profesor" de Logos serán **Profesores IA por asignatura** — equivalente al
  "Profesor Virtual" de Brincus, pero es una pieza de Fase 2, no de la primera salida a
  producción.
- **Fase 2** (segunda pasada de producción, no bloquea el primer lanzamiento):
  1. Profesores IA por asignatura (equivalente al "Profesor Virtual" de Brincus).
  2. Juegos (11 juegos genéricos tipo Brincus).
  3. Biblioteca de recursos descargables tipo biblioteca real (libros/PDFs gratuitos para
     descargar, **distinta** del contenido de estudio que ya existe en `contenido/` — el
     usuario fue explícito: "solo tenemos como un tipo biblioteca de recursos pero es para
     estudiar sobre las materias", esto es un concepto nuevo y separado).
  4. Plan Lector (lista de libros recomendados por nivel).
- **Fase 1** (primera salida a producción): todo lo demás del análisis de Brincus, incluyendo
  **descarga/impresión de guías en PDF** (el usuario lo pidió explícitamente aparte de la
  Biblioteca de Fase 2 — es exportar el contenido de estudio que YA existe, no una biblioteca
  nueva).
- **Simulacro con fecha programada**: en Fase 1, resuelto por el Administrador (panel Admin
  ya existente) programando la fecha — no se espera al rol Profesor (que sigue siendo un plan
  aparte, ver `.claude/plans/eventual-strolling-gadget.md`, sin tocar en este plan).
- **Historial de pagos para el Apoderado**: en Fase 1, construir el modelo/UI con los datos
  que ya existen hoy (plan activo, fechas de renovación/inicio/término de la suscripción). El
  comprobante de pago real (PDF descargable con monto efectivamente cobrado) queda pendiente
  de la pasarela de pago real — no bloquea mostrar lo que sí se puede mostrar hoy.
- **Prueba gratuita: 5 días, no 7** — ✅ **ya ejecutado** en esta sesión (no se esperó a la
  aprobación del resto del plan, por ser un cambio aislado y explícitamente confirmado):
  - `backend/app/application/comercial/casos_de_uso.py:14` — `DURACION_PRUEBA_GRATIS_DIAS = 5`.
  - `frontend/src/app/pages/landing/landing.ts:160` y
    `frontend/src/app/pages/seleccion-plan/seleccion-plan.ts:15,46` — copy actualizado a "5 días".
  - `backend/tests/test_auth.py` — test renombrado y rango de días ajustado (4,5). Suite de
    auth verificada en verde (`uv run pytest tests/test_auth.py -k prueba_gratis` → 2 passed).
  - `planificacion/09-modelo-de-negocio.md` — actualizado para no quedar desincronizado del
    código.

## 1. Auditoría del estado actual (verificado en el código, no en documentación)

**Nota**: esta tabla es la foto del día 1 (2026-08-14), antes de construir Fase 1 — quedó
desactualizada a propósito, como bitácora de "qué faltaba al empezar" (ver CLAUDE.md para el
estado real y vigente: casi todo Fase 1 quedó construido y verificado esa misma sesión, y la
fila de Plan Lector se corrigió arriba porque se construyó recién el 2026-08-15).

| Área | Estado hoy | Ubicación |
|---|---|---|
| Motor de evaluación (tipos, intentos, retomar intento) | **Ya existe, y ya es mejor de lo que asumí en el análisis inicial** — `IntentoEvaluacion` con tipos `prueba_unidad`/`examen_simulacro`/`examen_simulacro_parcial`, historial de intentos, y **ya retoma un intento a medio hacer en vez de reiniciarlo** | `backend/app/domain/evaluaciones/entities.py:13`, `backend/app/application/evaluaciones/casos_de_uso.py:40-53` |
| Simulacro con fecha programada (evento, no % de cobertura) | No existe — todo se habilita por % de cobertura del temario, sin concepto de calendario | `backend/app/domain/evaluaciones/value_objects.py:69`, `backend/app/application/progreso/consultas.py:121` |
| Gamificación (Logros/XP/niveles/avatares) | No existe nada | — |
| Plan de estudio (vista semanal/mensual/anual, repaso de años anteriores) | Existe una versión más simple: lista de sesiones fechadas a 8 semanas, sin agrupación temporal ni repaso de años anteriores | `backend/app/domain/plan_estudio/entities.py:15,24,65` |
| Biblioteca de recursos (libros/PDFs/grabaciones descargables) | No existe | — |
| Plan Lector | **Construido 2026-08-15, piloto en 4° básico** (4 libros curados) | `backend/app/routers/plan_lector.py`, `frontend/src/app/pages/plan-lector/plan-lector.ts` |
| Certificado de alumno regular (PDF descargable) | No existe | — |
| Historial de pagos con comprobante (vista Apoderado) | No existe — solo agregados mensuales para Admin, y no hay pasarela de pago real todavía | `backend/app/domain/comercial/ports.py:33`, `backend/app/application/comercial/consultas.py:68-70` |
| Agregar alumno nuevo | Existe, pero como ruta separada (`/agregar-alumno`), no inline en el panel del apoderado | `frontend/src/app/app.routes.ts:41-42` |
| Check-in emocional / bienestar | No existe | — |
| Reportar error de contenido | No existe en código (solo mencionado como función futura del Admin en `planificacion/01-roles-y-permisos.md:115`) | — |
| Tutor/Profesor IA | No existe ninguna integración de IA | — |
| Descarga/impresión de guía en PDF | No existe (el contenido de estudio se sirve solo en pantalla) | — |

## 2. Fase 1 — primera salida a producción

**Confirmado con el usuario (2026-08-14): Fase 1 se acota a lo que se puede construir sin
depender de servicios externos** (nada que requiera cuenta/autenticación de un tercero, como
login con Google — eso queda fuera de Fase 1, ya estaba solo como decisión de infraestructura
futura en `planificacion/17-infraestructura-y-entornos.md`, no como compromiso de esta fase).
Se revisó ítem por ítem contra esta regla — el resultado (detalle en cada ítem abajo) es que
**los 10 ítems de Fase 1 son 100% construibles en local**, sin ninguna cuenta/API externa:
- La mayoría son solo backend + base de datos + frontend (sin ninguna librería ni servicio
  nuevo).
- Los que generan PDF (guía descargable y certificado) usan una **librería local** de
  generación de PDF (ej. WeasyPrint/ReportLab en Python, o jsPDF/pdf-lib en el navegador) —
  es un paquete que se instala, no un servicio externo con cuenta/autenticación. Nota
  importante: Brincus muestra sus guías con el **Adobe Document Cloud View SDK** (un servicio
  externo de pago/cuota) — Logos no necesita eso: basta con servir el PDF generado desde el
  propio backend y mostrarlo con el visor nativo del navegador (`<iframe>`/`<embed>` simple),
  cero dependencia externa.
- Lo único que sigue fuera de alcance por depender de un tercero (pasarela de pago real,
  envío de correo transaccional con Resend, verificación humana Turnstile) ya estaba marcado
  como pendiente desde antes (`planificacion/22-analisis-de-brechas.md`) y **no se toca en
  este plan** — donde un ítem de Fase 1 roza esto (ej. comprobante de pago real), se acota
  explícitamente a lo que sí se puede mostrar con datos que ya existen hoy, sin bloquear el
  resto.

Orden sugerido por costo/impacto, no obligatorio — a discutir si el usuario prefiere otro
orden:

### 2.1. Refinar el motor de evaluación ya existente (bajo costo, alto impacto directo) — 100% local
El motor ya es sólido (retoma intentos, historial). Lo que falta para igualar/superar la
experiencia de Brincus verificada en el Paso 11.5 del análisis:
- **Navegación libre entre preguntas** dentro de un intento en curso (saltar a cualquier
  pregunta, no solo avanzar linealmente) — a confirmar si el frontend actual ya lo permite o
  fuerza orden lineal.
- **Resumen final con detalle por pregunta** (correcta/incorrecta + link de revisión), no
  solo una nota agregada.
- **"Notificar error" a nivel de pregunta individual** dentro de un intento — reutiliza el
  mismo mecanismo del punto 2.6.
- **Simulacro con fecha programada por el Admin** (evento con `fecha_disponible_desde`, o
  rango de fechas) como tipo adicional o modalidad del `examen_simulacro` existente.

### 2.2. Gamificación (Logros/XP/niveles/avatares) — 100% local
Pieza más grande de Fase 1. Diseño a definir en detalle si se aprueba avanzar: mínimo viable
= puntos por acción (ver lista real de logros del análisis, Paso 12) + niveles + selección de
avatar simple (sin "avatares evolucionables" bloqueados por nivel en un primer corte, eso
puede ser un refinamiento). Premiar constancia (rachas de sesión) además de avance de
contenido, como hace Brincus.

### 2.3. Onboarding con checklist de primera sesión — 100% local
Checklist de pasos concretos al primer login del alumno (ver lista de 7 pasos de Brincus en
el análisis, Paso 7) — adaptado a lo que Logos sí tiene hoy (sin Clases en Vivo ni Profesor
Virtual todavía en Fase 1).

### 2.4. Check-in emocional diario (modal simple) — 100% local
Modal de ánimo al entrar (Feliz/Tranquilo/Cansado/Preocupado/etc.), guardado como dato simple
ligado al perfil del alumno — sin necesidad de que el apoderado lo vea todavía (a definir si
se quiere agregar visibilidad para el apoderado, eso sería una decisión de producto nueva).

### 2.5. Descarga/impresión de guía en PDF — local con librería (sin cuenta externa)
Exportar el contenido de estudio existente (guía por OA) a un PDF descargable/imprimible —
reutiliza contenido que ya existe en `contenido/`, es una funcionalidad de exportación, no
contenido nuevo.

**Verificado en Brincus (2026-08-14), dos decisiones a tomar antes de construir esto:**
- Brincus sirve sus PDFs de guía desde una URL pública (`/public/guias2025/...`), sin sesión
  ni login — se pudo descargar directo con `curl`. Es simple de implementar pero regala el
  contenido a cualquiera con el link. **Decisión pendiente**: ¿Logos sirve los PDF así
  también (bucket público, más simple) o con URL firmada/temporal (más trabajo, controla
  mejor el acceso de alumnos sin plan activo)?
- El formato real de guía de Brincus es una **hoja de ejercicios para imprimir** (título +
  ejercicios numerados con espacios en blanco/tablas para completar a mano + página final de
  "Resultados" con las respuestas) — no un documento explicativo. Si Logos exporta la guía de
  estudio actual (que sí tiene explicación + ejemplos, ver `contenido/00-estado-contenido.md`)
  tal cual a PDF, el resultado será distinto en propósito (material de lectura/estudio vs.
  hoja de práctica para imprimir) — vale la pena decidir cuál de los dos formatos se quiere,
  o si se ofrecen ambos.

### 2.5.1. Control de calidad de contenido (idea nueva, surgida de un bug real de Brincus) — 100% local
Al descargar y leer una guía real de Brincus se encontró un error de contenido propio de
ellos: una guía etiquetada "Números hasta 10.000" (4° básico) contenía ejercicios con números
de cientos de miles de millones, muy fuera del alcance declarado de la unidad — ver el
detalle en `planificacion/25-analisis-competencia-brincus.md`, Paso 11. Con 2.917 preguntas
en 12 cursos, vale la pena agregar a Fase 1 una validación automatizada simple (rango
numérico/dificultad declarada vs. contenido real de cada ítem) para no repetir este error en
Logos — bajo costo, evita un problema real que sí le pasó a un competidor en producción.

### 2.6. Reportar error de contenido — 100% local
Botón simple en guía/pregunta/video → formulario corto → llega al panel de Admin (que ya
tiene la intención de diseño documentada en `planificacion/01-roles-y-permisos.md:115`, pero
no implementada).

### 2.7. Certificado de alumno regular (PDF descargable) — local con librería (sin cuenta externa)
PDF simple (nombre, curso, fecha) generado on-demand desde el perfil del alumno — bajo costo,
no requiere backend nuevo más allá de un generador de PDF.

### 2.8. Historial de pagos (Apoderado) — con los datos que sí existen hoy — 100% local (el comprobante real queda fuera, no bloquea)
Vista para el Apoderado con plan activo, fecha de inicio y de término/renovación de la
suscripción actual, y las suscripciones pasadas si las hay. El comprobante de pago con monto
real queda marcado como pendiente hasta la pasarela de pago (mismo patrón que ya usa
`planificacion/22-analisis-de-brechas.md` para no prometer algo que no se puede cumplir aún).

### 2.9. Agregar alumno inline en el panel del Apoderado — 100% local
Mover el flujo de `/agregar-alumno` a un formulario inline (modal o sección expandible)
dentro del panel donde el apoderado ya ve a sus alumnos, en vez de una ruta aparte.

### 2.10. Plan de estudio — vista semanal/mensual (evaluar si entra en Fase 1) — 100% local
El plan de estudio actual ya funciona (sesiones fechadas a 8 semanas); agregar agrupación
visual por semana/mes es una mejora de UI sobre datos que ya existen, no un cambio de modelo.
A definir prioridad relativa frente al resto de la lista.

## 3. Fase 2 — segunda salida a producción

1. **Profesores IA por asignatura** (equivalente al "Profesor Virtual" de Brincus, probado en
   vivo con una pregunta real — funciona de verdad, no es una maqueta) — incluye definir
   personajes/nombres por asignatura, límite de preguntas por plan (Brincus limita a 5/mes en
   su plan más básico, como referencia de cómo un competidor controla costo de LLM), y el
   proveedor de IA a usar (pendiente de decidir). Verificado que en Brincus el chat no es un
   simple flujo de preguntas y respuestas: tiene **3 modos con propósito distinto** (Práctica
   guiada, Prueba de práctica, Aprender más) y una sección de **"Mis metas"** donde el alumno
   declara explícitamente qué quiere aprender/mejorar y el profesor virtual las usa para
   personalizar — vale la pena diseñar el Profesor IA de Logos con esta misma estructura desde
   el inicio, no como un chat plano de una sola modalidad.
2. **Juegos** (los 11 confirmados en el análisis: 2048, Ajedrez, Crucigrama, Damas,
   Pasapalabra, Dominó, Mahjong, Blockbuster Puzzle, Tic Tac Toe, Falling Cubes, Mill Game) —
   posiblemente vía librerías/embeds existentes en vez de construir cada uno desde cero, a
   evaluar.
3. **Biblioteca de recursos descargables** (libros/PDFs gratuitos, distinta del contenido de
   estudio) — implica además una decisión de contenido (qué libros/recursos ofrecer,
   licencias), no solo de ingeniería.
4. **Plan Lector** (lista curada de libros por nivel, con autor/editorial) — también requiere
   curaduría de contenido, similar en espíritu a como se armó `contenido/` para el currículum.

## 4. Lo que NO entra en ninguna fase por ahora (documentado para no perderlo)

- Clases en vivo con profesor humano real, Mis Tareas, Comunicación 1 a 1 alumno↔profesor,
  Comunidades de WhatsApp — decisión de alcance ya tomada (Logos es autoestudio + IA, no
  colegio con profesores humanos en vivo), ver `planificacion/00-vision-alcance.md`.
- Rol Profesor / Curso-Sección — plan aparte ya existente
  (`.claude/plans/eventual-strolling-gadget.md`), no se toca ni se mezcla con este plan.

## 5. Preguntas abiertas para antes de empezar a construir cualquier ítem de Fase 1

Estas quedaron sin resolver en la ronda de preguntas de esta sesión — se listan para no
asumir nada al momento de detallar el diseño de cada ítem:

1. **Gamificación**: ¿se quiere el sistema completo desde el inicio (niveles/avatares
   bloqueados progresivamente, como Brincus) o un MVP más simple (solo puntos + 1 nivel de
   avatar) para la primera salida, dejando la profundidad para después?
2. **Check-in emocional**: ¿el apoderado debería poder ver el historial de ánimo de su hijo,
   o es un dato solo para uso interno/futuro (ej. detectar patrones) sin superficie visible
   todavía?
3. **Simulacro con fecha programada por el Admin**: ¿es un simulacro único con fecha global
   para todos los alumnos de un nivel, o el Admin necesita poder programar fechas distintas
   por curso/región? (Afecta el diseño del modelo de datos.)
4. **Orden de prioridad dentro de Fase 1**: la lista de la sección 2 está en un orden
   sugerido por costo/impacto, no confirmado por el usuario — falta decidir si se quiere
   ese orden o uno distinto antes de empezar a construir el primer ítem.

No se empieza a construir ningún ítem de la sección 2 ni 3 hasta resolver esto y tener
aprobación explícita del plan completo.

**Nota (2026-08-15):** la sección 5 quedó obsoleta — las 4 preguntas ya se resolvieron sobre
la marcha durante la construcción (gamificación completa con racha/hábito, check-in sin
superficie para el apoderado todavía, simulacro con fecha única por nivel, y el orden de
prioridad terminó siendo iterativo vía el loop autónomo de las secciones siguientes). Se deja
el texto original como registro histórico de las preguntas abiertas al momento de planificar.

## Actualización 2026-08-15 (cuarta pasada) — identidad visual y hallazgos UX/Frontend/Backend

Cuarta entrada en vivo a la cuenta real de Brincus, esta vez con un análisis explícito en 3
roles (UX, Frontend, Backend) pedido por el usuario, con la instrucción de ser honesto sobre
qué se pudo y no se pudo revisar. Recorrido: login, selector de perfil, onboarding, "Mis
Asignaturas", el reproductor de clase completo (video + tabs Resumen/Evaluar/Errores +
temario con vistas Unidades/OA/Exámenes Libres), Plan de Estudio (calendario + gráficos de
avance), Logros (curva de XP, avatares, estadísticas de uso) y Mi Progreso. **No se pudo
revisar** (redirigen solas al dashboard sin aviso, aparentemente bloqueadas en la cuenta de
prueba gratis): Biblioteca, Ensayos, Mis Evaluaciones, Mis Tareas, Comunicación, Juegos,
detalle de Avatares.

### Decisiones de alcance para esta tanda

- **Paleta propia, no la de Brincus**: se usa un degradado con los colores de marca ya
  definidos (índigo `#5B4FE9` + coral `#FF6B4A`, ver `15-diseno-visual-y-marca.md`), nunca el
  naranja/rosa/morado literal de Brincus — el objetivo es que Logos se sienta más vivo, no que
  se vea como una copia.
- **Sin fotos de "profesores" por asignatura**: Brincus muestra una foto real de un profesor
  humano en cada card de curso (con nombre) — no aplica a Logos, que es autoestudio sin
  profesor asignado por defecto (el Rol Profesor es opcional vía Curso/Sección). Inventar
  personajes/fotos falsas sería engañoso.
- **Curva de XP no lineal**: Brincus documenta al alumno una curva creciente (nivel 2 = 50 XP,
  nivel 3 = 200 XP, nivel 4 máximo = 1500 XP) en vez de un múltiplo fijo — se adopta esa forma
  de curva (subir rápido al principio, exigente al final) en vez de la lineal actual de Logos
  (50 XP por nivel siempre, sin techo).
- **Deliberadamente NO se toca el reproductor de clase** (layout video-izquierda +
  temario-siempre-visible-derecha de Brincus): Logos ya decidió y construyó, hace pocas horas
  en esta misma sesión, separar "Estudiar" en 2 pasos explícitos (Aprender → Practicar) como
  mejora sobre el video único de Brincus — rehacerlo de nuevo sin que el usuario lo pida
  explícitamente sería revertir una decisión reciente y deliberada.
- **Deliberadamente NO se rediseñan las insignias con gráficos metálicos** (escudos/gemas tipo
  videojuego): implica encargar o generar arte gráfico custom (SVG/ilustración), lo que rompe
  el patrón "cero dependencias externas, cero licencias que gestionar" ya aplicado a avatares
  y asignaturas con emoji. Queda como idea para una futura inversión de diseño, no para hoy.

### Construido en esta tanda

1. **Degradado de marca en el selector de perfil y la bienvenida** — más energía visual sin
   salir de la paleta de Logos.
2. **Countdown de prueba gratuita en el dashboard del alumno** — el dato ya existía
   (`GET /auth/alumnos/{id}/suscripcion` con `fecha_termino`), solo faltaba mostrarlo; Brincus
   lo tiene fijo bajo el avatar en todo momento.
3. **Curva de niveles no lineal en gamificación** (nivel 2 = 50 XP, nivel 3 = 200 XP, nivel 4
   máximo = 1500 XP, con techo — antes era lineal e infinita).
4. **Estadísticas de uso visibles para el propio alumno en Mis Logros** ("¿sabías que…":
   racha máxima, tiempo total dedicado a evaluaciones, evaluaciones entregadas, guías
   revisadas) — dato que ya existía en el dominio de gamificación, solo faltaba mostrarlo como
   "dato curioso" al alumno, igual que hace Brincus.
5. **Calificación con estrellas por guía** (☆☆☆☆☆, "¿Qué te pareció esta guía?"), señal de
   calidad de contenido distinta y más liviana que "Reportar error" — mismo patrón de captura
   de dato sin bandeja de revisión de Admin todavía que ya se usó para reportes y sugerencias.

**Bug real corregido en el camino**: `progresoNivelPct()` en el frontend calculaba el
progreso de la barra de nivel con `xp % 50` — un resto que solo tenía sentido bajo la curva
lineal anterior. Al cambiar a la curva no lineal quedó matemáticamente incorrecto (la barra
habría mostrado un progreso sin relación con el umbral real del nivel); se corrigió para usar
la misma fórmula `25 * (nivel-1) * nivel` que ahora usa el backend.

Verificado: 405 tests backend + 309 Playwright (3 navegadores, accesibilidad incluida) en
verde.

## Actualización 2026-08-15/16 (quinta pasada, cierre) — 100% local salvo lo explícitamente excluido

Última ronda antes de cerrar el nivel local por completo. El usuario marcó explícitamente
que la comparación iterativa contra Brincus (4 rondas en un mismo día) empezaba a sentirse
sin fin — diagnóstico honesto: cada "vuelvo a comparar" abre una actividad sin fondo, porque
Brincus tiene ~16 secciones de menú con decenas de sub-detalles, así que siempre aparece algo
más que notar. El problema no era que faltara trabajo real, era usar "comparar de nuevo" como
gatillo recurrente de más trabajo en vez de fijar una línea de cierre. Esta ronda cierra esa
línea: se completan los 2 pendientes conocidos de la ronda anterior y no se vuelve a abrir una
sexta ronda de comparación.

1. **Degradado de marca también en la tarjeta de onboarding de Inicio** ("Primeros pasos") —
   quedó pendiente de la ronda anterior (solo se había aplicado al selector de perfil).
2. **Avatares con fondo tipo "esfera/gema"** (`radial-gradient` + sombras internas para
   simular brillo, sin arte gráfico externo) en vez de círculos de color plano — salto de
   calidad visual real logrado solo con CSS, mismo criterio de "cero dependencias, cero
   licencias" ya aplicado con emoji.

**Nivel local: 100% completo salvo lo explícitamente excluido** (IA dentro de la app, Juegos,
Videos, Clases en vivo con profesores reales, Biblioteca con contenido de licencia de
terceros) — ver la lista de decisiones de alcance al inicio de la Actualización cuarta pasada,
más lo que requiere credenciales/cuentas reales (pasarela de pago, Google OAuth, Resend,
Turnstile, despliegue) que no es "nivel local" por definición. Verificado: suite completa
backend + Playwright (3 navegadores) en verde.

## Marcadores de roadmap "próximamente" (2026-08-16)

El usuario pidió, después de cerrar el nivel local, dejar visibles en el sidebar los 3 ítems
explícitamente excluidos (Profesor IA, Juegos, Videos) con un badge "pronto" en vez de
ocultarlos — mismo patrón ya usado antes para Plan de Estudio mientras no estaba construido
(`sidebar.ts`, `[routerLink]="item.proximamente ? null : item.ruta"`). No navegan a ningún
lado todavía, no prometen nada roto.

**Bug real encontrado y corregido en el camino**: el `opacity: 0.55` que apagaba visualmente
todo el ítem "próximamente" diluía también el color del badge "pronto" (que ya usaba
`--color-alerta-texto`, elegido específicamente para cumplir contraste AA sobre
`--color-alerta-suave`) — con 3 ítems fijos en pantalla a la vez (antes solo había uno,
transitorio, nunca se topó con axe-core en ese estado) el contraste cayó a 2.14:1, muy por
debajo del mínimo 4.5:1. Se corrigió aplicando la opacidad solo al ícono, no al texto ni al
badge. Verificado: 405 tests backend + 312 Playwright (3 navegadores, accesibilidad incluida)
en verde.

## Predicción sin IA: 2 de 3 ideas diferenciadoras (2026-08-16)

Con el nivel local ya cerrado, el usuario pidió pensar en algo innovador que la competencia
no tenga. Se propusieron 3 ideas basadas en aritmética/heurísticas transparentes sobre datos
que la app ya recolecta — **sin IA/LLM** — y el usuario eligió las 3: Nota estimada del
Examen Libre, Alerta temprana de ritmo de estudio, Mapa de calor por eje temático. Documentado
aquí a medida que cada una se completa y verifica (arquitectura hexagonal completa, no un
prototipo).

1. **Nota estimada del Examen Libre** (`app/application/prediccion/consultas.py`,
   `EstimarNotaExamen`) — en Mis Notas, antes de "Avance de contenido": una estimación de la
   nota que el alumno sacaría si rindiera el Examen Libre hoy, por asignatura y general, con
   nivel de confianza (sin_datos/baja/media/alta) según cuánta cobertura de OA tiene evaluada.
   Fórmula: 65% nota de simulacro + 35% nota de práctica cuando existen ambas; degrada a solo
   la que exista, o "sin datos" si no hay ninguna. Reutiliza `ObtenerHistorialYNotas` y
   `ObtenerFaltantes` sin duplicar lógica. Endpoint `GET
   /prediccion/{perfil_alumno_id}/nota-estimada`.
2. **Alerta temprana de ritmo de estudio** (`EvaluarRitmoDeEstudio`) — en Mis Notas: si el
   Plan de Estudio tiene fecha objetivo, compara el ritmo real de OA revisados/día contra el
   ritmo necesario para llegar a tiempo, y avisa antes de que sea tarde en vez de solo mostrar
   "atrasada" cuando ya se atrasó. Endpoint `GET
   /prediccion/{perfil_alumno_id}/ritmo-de-estudio`.

   **Bug real de aislamiento de test encontrado y corregido**: el primer intento de
   `e2e/alerta-ritmo.spec.ts` usaba la cuenta compartida de desarrollo "Sofía" para el caso
   que marca todas las guías del plan como revisadas — progreso permanente e irreversible en
   `/progreso/.../revisada` que contaminó la cuenta para las corridas siguientes de otros
   casos del mismo archivo. Al corregirlo con una cuenta nueva por caso (3 registros × 3
   navegadores = 9 registros por corrida) se topó con un segundo problema real:
   `POST /auth/registro` está limitado a 5/minuto por IP (`app/routers/auth.py`, protección
   legítima contra fuerza bruta), así que 9 registros en menos de un minuto empezaban a
   devolver 429 y el formulario de registro se quedaba trabado. Se corrigió registrando **una
   sola cuenta por navegador** en `test.beforeAll` (3 registros por corrida, no 9) y corriendo
   los 3 casos en modo serial sobre esa misma cuenta, dejando el caso que deja estado
   permanente al final. Confirmado con corridas repetidas.
3. **Mapa de calor por eje temático** (`ObtenerMapaDeCalorPorEje`) — en Mis Notas: cruza
   todas las respuestas de los intentos ya entregados contra el eje temático de la OA de cada
   pregunta (ej. en Ciencias Naturales: "Seres Vivos", "Materia y Energía"), mostrando el %
   de correctas por eje agrupado por asignatura — más granular que la nota por asignatura,
   para saber en qué tema específico reforzar. Solo cuenta preguntas autocorregibles
   (alternativas/verdadero_falso) con `oa_id` vinculado y `eje_tematico` poblado; si el mismo
   eje aparece en más de un intento, se acumula (no se queda solo con el último). Endpoint
   `GET /prediccion/{perfil_alumno_id}/mapa-calor`.

   **Hallazgo real de calidad de datos (no un bug, documentado para no sorprenderse
   después)**: al verificar esta feature con datos reales, la cuenta de prueba "Sofía" dio un
   mapa de calor vacío — sus intentos entregados resultaron ser, por azar, todos de preguntas
   sin `oa_id` vinculado. Se confirmó por qué: las preguntas de `prueba_unidad` tienen un
   vínculo "best effort" a un OA (ver comentario en `orm_models.py::Pregunta`) que en la
   práctica falla para buena parte del banco (771 de 2051 preguntas "alternativas" sin
   `oa_id`, y las `desarrollo_breve` de todas formas quedan excluidas por no ser
   autocorregibles), mientras que las de `examen_simulacro` tienen mucha mejor cobertura. En
   la práctica esto significa que el mapa de calor será más rico para un alumno que ya rindió
   algún examen simulacro que para uno que solo ha rendido pruebas de unidad — comportamiento
   esperado dado el estado real del contenido, no algo que arreglar en esta pasada (ya estaba
   así antes de esta feature, solo que nada lo hacía visible). El test E2E se verificó
   entonces contra un examen simulacro real y estable del dev DB (conjunto 1987, "Examen
   Ciencias Naturales Forma B") en vez de la cuenta Sofía.

Verificado: 428 tests backend + 327 Playwright (3 navegadores) en verde — confirmado con una
corrida completa; 3 fallos puntuales en esa corrida (rate-limit de `/auth/registro` y un
timeout de recursos en webkit al final de una corrida larga de ~5.4 min) se confirmaron como
flakiness transitoria de entorno, no regresiones: los 3 casos pasan limpio al correrlos de
nuevo de forma aislada.

**Las 3 ideas diferenciadoras de predicción quedaron completas y verificadas de punta a
punta**: Nota estimada del Examen Libre, Alerta temprana de ritmo de estudio, Mapa de calor
por eje temático.

## Boceto de 9 ideas psicológico/pedagógicas y 7 construidas (2026-08-17)

A pedido del usuario, se hizo un análisis con enfoque psicológico y pedagógico (teoría de la
autodeterminación, mentalidad de crecimiento de Dweck, reducción de ansiedad ante exámenes,
calibración metacognitiva, sistemas familiares) para proponer ideas nuevas más allá de lo ya
construido. Se publicó primero un boceto visual (Artifact, sin código) con mockups de 9
ideas para validar la experiencia antes de construir — el usuario pidió construir 7 de las 9
(excluyendo "Estadísticas como vista propia" no, esa sí se construyó; se excluyeron
"Planes segmentados por profundidad de funcionalidad" —decisión de negocio, no de
ingeniería— y "Desglose visual de tareas tipo tablero").

Las 7 construidas, con arquitectura hexagonal completa y tests (backend + Playwright):

1. **Lenguaje "todavía no"** — copy de mentalidad de crecimiento (Dweck) en el Mapa de
   Calor, la Nota Estimada y el resultado de una prueba, cuando el desempeño es bajo.
   **Bug de marca corregido en el camino**: el Mapa de Calor usaba rojo (`--color-error`)
   para ejes con bajo desempeño — exactamente lo que `planificacion/15-diseno-visual-y-marca.md`
   prohíbe explícitamente ("el rojo en contexto escolar se asocia a error/castigo y
   desmotiva"). Corregido a ámbar con más énfasis visual (borde), no un color de alarma.
2. **Coaching a la madre según el momento** — antes de que el Apoderado vea las notas de un
   hijo con al menos una nota reprobada, un tip breve sobre cómo reaccionar sin presión, con
   un botón "Ver la nota" que las revela. Nunca aparece en la vista del propio alumno.
3. **Cruce sueño / horario de estudio** — cruza la hora real (UTC-3 fijo, mismo criterio ya
   aceptado en el proyecto para no modelar timezone por alumno) de las últimas sesiones de
   estudio; si 3+ de las últimas 7 fueron después de las 21:00, un aviso — solo visible para
   el Apoderado, nunca para el alumno (evita sentirse como vigilancia).
4. **"Estadísticas" — vista propia del Apoderado** — un ítem nuevo en el sidebar (solo con
   2+ alumnos; con uno solo, "Mis Notas" ya cumple ese rol) que junta a todos los hijos en
   una sola pantalla: cobertura, racha y estado de ritmo, antes de entrar al detalle de
   ninguno.
5. **Metas familiares compartidas** — con 2+ alumnos, "la familia estudió N días combinados
   esta semana" en vez de comparar el rendimiento de un hermano con otro — mismo cuidado de
   evitar comparación directa que ya se aplica entre alumnos de toda la plataforma.
6. **Agenda familiar del domingo** — 3 preguntas (o menos) armadas con datos reales del
   alumno (eje temático más flojo del Mapa de Calor, racha, estado de la Alerta de Ritmo),
   con un botón "Ya conversamos" que la oculta hasta la semana siguiente (persistido por
   `perfil_alumno_id` + semana en una tabla nueva, `agenda_familiar_conversada`).
7. **"Racha de la casa" / jardín semanal** — la más deliberada de las 7: el boceto original
   proponía una planta que se marchita al perder la racha, pero eso **contradice el
   principio "todavía no"** recién aplicado en el ítem 1 (un castigo visual). Se construyó
   la variante recomendada: cada semana (últimas 8) suma una plantita nueva al jardín
   acumulado, en 5 estados (semilla/brote/crecimiento/floreciendo/flor completa) según los
   días activos esa semana — si una semana tuvo poca actividad esa plantita queda más chica,
   pero el jardín completo nunca desaparece ni se marchita. Ilustración propia en SVG (sin
   arte externo, mismo criterio de "cero dependencias" ya aplicado a avatares) con
   degradado, tierra y sombra de piso — no un ícono plano — en `shared/planta-jardin/`,
   visible en "Mis Logros" junto al 🔥 de racha ya existente (sin reemplazarlo).

**Hallazgos reales adicionales en el camino**: (a) el servidor de desarrollo tenía el build
roto por una carrera de compilación (el router importaba un archivo antes de que existiera)
que hacía caer cualquier ruta nueva a la landing vía el wildcard `**` — no era un bug de
código, solo necesitaba un rebuild; (b) confirmado que `Pregunta`/`ProgresoOA` etc. ya
seguían el patrón de fechas UTC-3 fijo sin timezone por alumno, reutilizado acá para el
cruce de horario en vez de inventar un mecanismo nuevo.

**Verificación final**: 472 tests backend + 372 Playwright (3 navegadores) en verde. Una
primera corrida completa tuvo 2 fallos puntuales (`plan-estudio-atrasada.spec.ts` en
chromium y firefox, esperando la campana de notificaciones) — una carrera de timing con el
modal de check-in emocional en `/alumno/inicio`, confirmada como flakiness transitoria al
pasar limpio de forma aislada. A pedido explícito de una segunda confirmación ("100%
seguro?"), se corrieron ambas suites completas **desde cero una vez más**: backend 472/472
y Playwright 372/372, las dos en una sola pasada limpia, sin ningún fallo — certeza real,
no inferida.

## Auditoría de seguridad — rate limiting y flood/DoS (2026-08-17)

A pedido explícito del usuario ("si alguien quisiera hacer algo malicioso... botarla,
ralentizarla, llenarnos de datos"), se hizo una auditoría con enfoque de ciberseguridad y
arquitectura sobre el backend completo.

**Hallazgo central**: de más de 30 endpoints de escritura (`POST`/`PUT`/`PATCH`) en toda la
app, solo 3 (`/auth/registro`, `/auth/login`, `/auth/login-google`) tenían protección de
rate limiting. El resto no tenía ninguna — incluido **el login de Admin, la cuenta de mayor
privilegio de todo el sistema**, completamente abierto a fuerza bruta sin límite. Además,
`ComunicadoRequest` (comunicados del Profesor) no tenía `max_length` en `titulo`/`cuerpo` —
único endpoint de texto libre del proyecto sin ese tope, a diferencia de sugerencias (2000)
y comentario de reporte (1000).

**Corrección estructural** (no solo parches puntuales): se agregó `default_limits` al
`Limiter` de slowapi + `SlowAPIMiddleware` en `main.py` — una red de seguridad por defecto
que protege *cualquier* endpoint, presente o futuro, aunque nadie se acuerde de decorarlo a
mano. Los endpoints ya decorados (auth) siguen usando su límite más estricto, que reemplaza
al default solo en esa ruta — el patrón exacto que ya evita el problema de fondo: un
endpoint nuevo que se agregue mañana ya nace protegido.

**Correcciones puntuales** en los 6 endpoints de mayor riesgo específico (fuerza bruta o
inundar la base de datos con filas), todas configurables por entorno vía `.env` (mismo
patrón ya establecido con `LIMITE_REGISTRO_POR_MINUTO`: valor de producción por defecto,
relajado solo en el `.env` de Desarrollo para no chocar con la suite Playwright completa):

1. `/admin/auth/login` — sin ninguna protección antes. `LIMITE_ADMIN_LOGIN_POR_MINUTO` (5).
2. `/profesor/auth/registro` y `/profesor/auth/login` — mismo riesgo que apoderado, sin
   cubrir. `LIMITE_REGISTRO_PROFESOR_POR_MINUTO` (5) / `LIMITE_LOGIN_PROFESOR_POR_MINUTO` (10).
3. `/auth/alumnos` (agregar alumno) — sin límite, una cuenta autenticada podía inundar
   `PerfilAlumno` con miles de filas. `LIMITE_AGREGAR_ALUMNO_POR_MINUTO` (10).
4. `/sugerencias/{id}` — buzón de sugerencias sin límite de cantidad (sí tenía
   `max_length=2000` por request). `LIMITE_SUGERENCIA_POR_MINUTO` (5).
5. `/evaluaciones/preguntas/{id}/reportar-error` — mismo riesgo de spam.
   `LIMITE_REPORTAR_ERROR_POR_MINUTO` (10).
6. `/profesor/cursos/{id}/comunicados` — sin límite de cantidad NI de tamaño de texto
   (`max_length` agregado: 200 en título, 2000 en cuerpo). `LIMITE_COMUNICADO_POR_MINUTO` (10).

Cada límite tiene un test que verifica el mecanismo contra el valor configurado (no un
número fijo), mismo criterio que `test_auth.py` — sigue siendo una prueba real del rate
limit sea cual sea el valor activo en cada ambiente.

**Verificado**: 480 tests backend + 372 Playwright (3 navegadores) en verde tras el
reinicio del servidor de desarrollo con los nuevos límites — el único "fallo" visto (la
misma carrera de timing con el modal de check-in emocional ya documentada arriba) se
reconfirmó como flakiness transitoria, no relacionada con los cambios de seguridad.

**Hallazgo adicional, a pedido de un resumen de "riesgos hasta ahora"**: `jwt_secret` tenía
un valor por defecto hardcodeado en el código fuente (público en el repo) sin ningún
chequeo — si la app arrancara en Producción sin un `JWT_SECRET` propio configurado en su
`.env`, cualquiera que leyera el repo podría forjar tokens válidos de cualquier cuenta.
Corregido con un `model_validator` en `Settings`: la app directamente **no arranca** si
`ENTORNO=produccion` y `jwt_secret` sigue siendo el valor inseguro por defecto — mejor
fallar fuerte en el arranque que correr insegura en silencio. 3 tests nuevos en
`test_config_seguridad.py`. Verificado: 483 tests backend en verde.

**Riesgos residuales identificados, deliberadamente no corregidos ahora** (documentados
para no perderlos, no son omisiones):
- `get_remote_address` (base del rate limiting) no maneja `X-Forwarded-For` — al desplegar
  detrás de un proxy (Render/Cloudflare) hay que revisar esto específicamente, o todos los
  usuarios podrían compartir "una IP" (la del proxy) entre sí.
- CORS solo permite `localhost` — correcto para hoy, pendiente de actualizar al dominio real
  en el despliegue.
- Sin captcha (Turnstile), sin verificación de email al registrarse, sin requisito de
  complejidad de contraseña (solo largo 8-128) — decisiones de producto ya tomadas
  (registro sin fricción, modelo Wited) o pendientes de credenciales reales, no bugs.
- Sin monitoreo/alertas (Sentry, UptimeRobot) — ya en el plan de infraestructura, pendiente
  de desplegar.

**Frontend — cabeceras de seguridad del navegador** (misma auditoría, pregunta de
seguimiento "¿el front es propenso a vulnerabilidades? yo fácilmente podría atacar a
Brincus"): el front no tenía ninguna cabecera de seguridad HTTP propia. Corregido en dos
capas: `SecurityHeadersMiddleware` (`backend/app/core/security_headers.py`, nuevo
`BaseHTTPMiddleware`) agrega `X-Content-Type-Options: nosniff`, `X-Frame-Options: DENY`
(anti-clickjacking), `Referrer-Policy: strict-origin-when-cross-origin` y
`Permissions-Policy` a toda respuesta del API; y `frontend/public/_headers` (convención
Cloudflare Pages, se copia tal cual a `dist/frontend/browser/` en el build) agrega las mismas
cabeceras más una Content-Security-Policy completa al sitio estático — sin verificar aún
contra un despliegue real, porque el proyecto no está desplegado. Hallazgo colateral al
revisar esto: `ng build --configuration production` estaba roto (nunca se había corrido en
toda la sesión, solo `ng serve`) porque `landing.scss` superaba el presupuesto de tamaño de
`angular.json`; corregido subiendo el umbral de 4kB/8kB a 6kB/12kB. 2 tests nuevos en
`test_security_headers.py`.

## Borrado de cuenta/datos de un alumno (2026-08-17)

Hallazgo de la misma auditoría de seguridad, esta vez de privacidad más que de DoS: no
existía ninguna forma de que un Apoderado pidiera eliminar los datos de un hijo —
brecha real de Ley 19.628 para una app que maneja datos de menores (RUT, fecha de
nacimiento, historial académico completo). El usuario decidió explícitamente (vía
`AskUserQuestion`) construirlo ahora y **no** cifrar RUT/fecha de nacimiento a nivel de
aplicación por ahora (se apoya en el cifrado en reposo del disco de Neon como mitigación
práctica contra el escenario "robo de backup").

**Backend**: `DELETE /auth/alumnos/{perfil_alumno_id}` (protegido con
`verificar_perfil_propio`, el mismo guard ya usado en el resto de endpoints por-alumno).
`EliminarAlumno` (caso de uso) → `RepositorioPerfilesAlumnoSQLModel.eliminar_en_cascada`,
que borra en orden (con `commit()` intermedios por la restricción de FK ya conocida de
`reemplazar_plan`): sesiones de estudio → plan de estudio → las 10 tablas hijas restantes
(`Suscripcion`, `IntentoEvaluacion`, `ProgresoOA`, `PerfilGamificacion`,
`ProgresoOnboarding`, `RegistroAnimo`, `AgendaFamiliarConversada`, `Sugerencia`,
`CalificacionGuia`, `ReporteError`) → el propio `PerfilAlumno`. 4 tests nuevos en
`test_eliminar_alumno.py` (borra todo, 403 si el alumno es de otra cuenta, 401 sin sesión,
404 si no existe).

**Frontend**: botón 🗑️ en cada tarjeta de alumno del panel del Apoderado
(`dashboard-apoderado.ts`), con confirmación inline ("¿Eliminar a {{nombre}}?... no se puede
deshacer") antes de llamar a `AuthService.eliminarAlumno`. `frontend/e2e/eliminar-alumno.spec.ts`
verifica que Cancelar no borra nada, que confirmar sí borra, y que el borrado persiste tras
recargar la página (prueba de que es un borrado real en el servidor, no solo de la UI).

**Verificado (corrida limpia y serial, 2026-08-17)**: 491/491 tests backend, suite Playwright
completa relanzada tras el cambio.
