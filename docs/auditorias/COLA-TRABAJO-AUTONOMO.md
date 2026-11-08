# Cola de trabajo autónomo

El usuario autorizó el 2026-11-07 que Claude decida qué falta y lo ejecute por su cuenta, con una
tarea programada que retoma el trabajo cada hora (también después de que se agote el límite de
uso). Este archivo es la fuente de verdad de esa cola: cada sesión toma la **primera tarea no
terminada**, la avanza, verifica, hace commit y push en `main` y actualiza su estado aquí.

## Reglas (no negociables)

- **No desplegar.** No crear cuentas ni usar servicios pagados. No usar APIs externas con datos.
- No pedir confirmaciones: decidir con criterio de experto e informar en el resumen.
- Responder al usuario en español.
- Cada cambio de contenido pasa por estos pasos:
  1. Validador `backend/scripts/validar_evaluaciones_markdown.py`: 0 discrepancias.
  2. Pruebas de backend, o al menos las de `scripts/tests` y las que toquen el cambio.
  3. Reimportar con `scripts/qa/reimportar_e2e.sh` (base aislada `logos_e2e_alternativas`) y
     levantar la SPA con `scripts/qa/levantar_spa.sh`.
  4. Validación en la app con `scripts/qa/validar_material.sh "<curso>"`. Por defecto usa **solo
     Chromium**, como sugirió el usuario el 2026-11-07: para un cambio de contenido basta un navegador.
     Con `NAVEGADORES=todos` corre en los 3, y se usa ante cambios de código de la interfaz o al cerrar
     una etapa.
- Commit por tarea, con el trailer `Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>`, y push.
- Registrar cada cierre en `AUDITORIA_MAESTRA.md` (§15.x siguiente).
- Las **reparaciones** (errores de contenido, defectos y deuda de la auditoría) van en `main`.
  Las **funcionalidades nuevas** van en una rama aparte, `feature/<nombre>`: se hace push de la
  rama, sin merge, y el usuario la revisa después.
- Lo que dependa de una cuenta externa o del usuario se **prepara al máximo**: código detrás de
  variables de entorno, `.env.example` y guía paso a paso. Lo que el usuario debe hacer se anota en
  `docs/PENDIENTES-USUARIO.md` (cuentas, claves y decisiones) y se pasa a la siguiente tarea.

## Entorno local (por si la sesión se reinicia)

- La API E2E corre en el puerto 8001 y la SPA en el 4300. Las herramientas están en `scripts/qa/`,
  dentro del repositorio: antes estaban en una carpeta temporal y se perdieron con el reinicio del
  2026-11-07.
- Para volver a compilar:
  `npx ng build --configuration development --define "LOGOS_API_URL='http://localhost:8001'"`.
- Para generar los audios: `DATABASE_URL=… scripts/voz/generar_audios.sh ["1° básico" …]`.

## Procedimiento de la tarea 7 (superposición entre pruebas y guías)

1. Correr `backend/.venv/bin/python backend/scripts/solapamiento_pruebas_guias.py <curso>`, que lista
   por archivo las preguntas repetidas.
2. Por cada archivo, reescribir **solo** las preguntas repetidas, manteniendo:
   - el mismo OA, el mismo tipo y la misma dificultad, con otro contexto, otros números u otro texto;
   - errores típicos como distractores, sin que la clave sea la más larga;
   - una posición de la clave variada.
3. Antes de escribir, comprobar con `grep` que la idea nueva no sea un ejemplo resuelto ni una
   autoevaluación de la guía.
4. **Declarar el OA de cada pregunta reescrita en `oa_por_pregunta`**, en el frontmatter. El
   importador lo deducía por coincidencia con la guía y, al reescribir, se pierde.
5. Actualizar la pauta, recalcular toda la Matemática y poner `ultima_actualizacion`.
6. Verificar:
   - validador: 0 discrepancias;
   - reimportación: 0 preguntas sin OA (`select count(*) from pregunta where oa_id is null`);
   - E2E del curso en los 3 navegadores.
7. Hacer commit por archivo o por asignatura. Orden: 4.° básico (piloto) → 1.°–3.° básico →
   5.°–8.° básico → media.

## ⚠️ Prioridad vigente: Fase 1 (desde el 2026-11-07, 20:30)

El usuario pidió **auditar primero el material en los archivos contra los temarios oficiales**,
después aplicarlo a la app una sola vez y dejar las mejoras para el final. Mientras la Fase 1 no
esté cerrada, **no avanzar las tareas 5 a 15** (reescrituras, Forma A, audio, imágenes y ramas).
El estado y los controles están en `docs/auditorias/fase1/00-ESTADO-FASE1.md`: tomar el primer
control pendiente.

## Tareas

| # | Tarea | Estado |
|---|---|---|
| 1 | Regenerar los audios con Kokoro «alex» (elegida por el usuario), verificar E2E 1.° básico y hacer commit | ✅ hecho 2026-11-07 |
| 2 | 1.° básico: reemplazar las ~20 descripciones `[Imagen: …]` y `::emoji::` que dan pistas o la respuesta (lápiz corto/largo, pollitos, materiales, secuencias) por dibujos (`::dibujo::`, `::contar::`, `::posicion::`, `::fila::`) o por un enunciado neutro | ✅ hecho 2026-11-07 |
| 3 | 2.° básico: el mismo barrido de descripciones de imagen que delatan la respuesta | ✅ hecho 2026-11-07 |
| 4 | 3.° y 4.° básico: el mismo barrido (más corto: hay menos imágenes) | ✅ hecho 2026-11-07 |
| 5 | Audio pregrabado para 3.° y 4.° básico (régimen A completo), con revisión de `texto-para-voz` sobre sus textos reales | pendiente |
| 6 | Segunda pasada a los sesgos de clave: distribución de letra correcta y de «la alternativa más larga» por curso, tras las correcciones del 2026-11-07 (§15.23–15.24) | ✅ hecho 2026-11-07 |
| 7 | Superposición del 79 % entre pruebas de unidad y autoevaluaciones de guía. Decisión de experto: una prueba no debe repetir textualmente lo ya practicado. Reescribir los ítems duplicados con contextos nuevos, el mismo OA y la misma dificultad, curso por curso, empezando por 4.° básico (piloto) | en curso: **4.° básico, 76 de 76 reescritas (0 % repetidas)**. Falta el E2E de 4.° básico, pendiente por la lentitud del Mac. **1.° básico, 0 de 85 repetidas** (antes 45). Falta el E2E de 1.° básico |
| 8 | Simulacros **Forma A** del régimen B/C (5.° básico a 4.° medio): uno por asignatura, mismo formato oficial que la Forma B (25 preguntas, alternativas), con otros ítems. Curso por curso, empezando por 5.° básico | pendiente |
| 9 | Reconciliar `matriz-maestra-estado-por-archivo.csv` con la revisión ítem por ítem (§15.26–15.28) y actualizar las cifras vigentes en `CLAUDE.md` (sacar los números históricos que ya no aplican) | pendiente |
| 10 | Accesibilidad: recorrido con axe en las pantallas de alumno (guía, autoevaluación, prueba y resultados) en los 3 navegadores; corregir lo que salga | pendiente |
| 11 | `docs/PENDIENTES-USUARIO.md`: lista de cuentas y claves que hacen falta (Neon, Render, Cloudflare Pages/R2, Resend, Google OAuth, Turnstile, Sentry, UptimeRobot, pasarela de pago, API de IA), con costo, paso a paso y dónde se configura cada una. También las decisiones abiertas | ✅ hecho 2026-11-07 (`docs/PENDIENTES-USUARIO.md`) |
| 12 | Preparar el despliegue sin desplegar: verificar `.env.example`, la configuración de producción, el CSP y los headers. Script para publicar los audios en R2 o en el build. Checklist de despliegue paso a paso. Va en `main` (es documentación y configuración) | ✅ hecho 2026-11-07 (`docs/DESPLIEGUE.md`, `render.yaml`, CORS configurable) |
| 13 | Rama `feature/juegos-practica`: juegos de práctica con el banco de preguntas (Fase 2 de Brincus, sin dependencias externas). Diseño en `planificacion/` y después la construcción, con pruebas | pendiente |
| 14 | Rama `feature/profesor-ia`: tutor con IA (Fase 2 de Brincus). Se construye detrás de una variable de entorno (sin clave queda desactivado), con salvaguardas para menores y un adaptador de pruebas. Se activa cuando el usuario entregue la clave | pendiente |
| 15 | Rama `feature/pasarela-pago`: adaptador de pagos (Flow, Mercado Pago o Webpay, a elegir por el usuario) con interfaz y modo de prueba. Queda detrás de una variable de entorno | pendiente |

## Bitácora

- 2026-11-08 (tarde): C.2 → 1.°, 2.°, 3.°, 5.° y 6.° básico en 0 % (4.° ya estaba). 7.° básico en curso: Lengua U1 y U2 reescritas con textos nuevos. Pendientes de 7.°: Ciencias, Historia, Inglés y Matemática (unas 125 preguntas). Luego 8.° básico y 1.° a 4.° medio.

- 2026-11-08: C.2 en curso. Cerrados 1.° y 2.° básico (0 % de copia). OA explícito en todas las pruebas. **Hallazgo:** lecturas no conectadas a sus preguntas en unas 12 pruebas y simulacros, y las pruebas de Lenguaje de 5.° básico remiten a textos de la guía (§15.37). **Siguiente:** mover el detector a `backend/scripts`, conectar los estímulos huérfanos y seguir C.2 con 3.° básico.

- 2026-11-07 23:40: Fase 1 → C.1 cerrado (0 % de copia en los 50 simulacros), C.3 al límite del formato, B aplicado (gráficos y mapas dibujados, §15.36). Base `logos_qa` del usuario recargada (tenía el material antiguo con preguntas de desarrollo). Contraste del resultado en modo examen corregido. **Siguiente:** C.2 (pruebas de unidad copiadas de la guía, 10 cursos) y luego D (imágenes, decisión del usuario).

- 2026-11-07: **Fase 1, control 4 cerrado:** indicadores revisados en los 12 cursos, ~1.398/1.437 (97 %). Lista consolidada en `docs/auditorias/fase1/correcciones-propuestas.md`, **pendiente de aprobación del usuario**. Siguiente control: el 5, exactitud de los cambios posteriores a `7ea9828`.

- 2026-11-07 18:35: PostgreSQL cierra las conexiones tras 1,5 a 2 min. Se interrumpió una reimportación, así que la base `logos_e2e_alternativas` puede haber quedado incompleta. **Al retomar:** si `psql` responde en menos de 1 s, ejecutar `reimportar.sh` completo; después, el E2E de 1.° y 4.° básico.

- 2026-11-07 18:30: 1.° básico, Matemática: 14 reescritas (Números 6, Patrones 3, Medición 2, Geometría 4 con dibujos nuevos de pastel, osito y perro). Diagnóstico de la lentitud: el disco estaba saturado (unas 4.400 operaciones por segundo, `kernel_task` sobre 200 %, un *checkpoint* de Postgres de 102 bloques tardó 13 s). Hay que reiniciar el Mac.

- 2026-11-07 17:35: 1.° básico, Historia (Formación Ciudadana 5, Geografía 4, Historia 2) y Lenguaje (U1 1, U2 4): 16 reescritas. Validador: 0 discrepancias. El E2E de 4.° básico volvió a fallar por la lentitud (6 fallas; la corrida de 1.° básico no terminó): sigue pendiente.

- 2026-11-07 16:40: 1.° básico, Ciencias Naturales: 14 preguntas reescritas (Vida 6, Físicas 5,
  Tierra 3), con OA explícitos. Reimportación: 6.150 preguntas, 0 sin OA. **E2E aún sin poder
  correrse** por la lentitud del sistema:
  - la conexión a PostgreSQL tardaba entre 3 y 7 s. Postgres se reinició (`brew services restart
    postgresql@16`) y también la API;
  - la carga del sistema vuelve a 40–55;
  - en la captura de una falla, la guía aparece bien cargada, solo tarde. No es un error de contenido.

  **Al retomar:**
  1. Si la carga está bajo 10, correr el E2E de 1.° y 4.° básico en los 3 navegadores y el backend
     completo.
  2. Si `psql` tarda más de 1 s, reiniciar Postgres y la API.

- 2026-11-07 16:20: se reescribieron las 39 preguntas que faltaban en 4.° básico: Ciencias
  (Físicas y Tierra), Historia (Formación Ciudadana, Geografía e Historia) y Lenguaje U2. Validador:
  0 discrepancias. **E2E pendiente:** el Mac está degradado (`kernel_task` sobre 190 %, sin aviso
  térmico y con 49 % de memoria libre); las pruebas de 14 s tardan más de 10 min. Posible causa:
  iCloud sincroniza `~/Documents` (141 MB de audios nuevos). Al retomar: si `uptime` muestra una
  carga baja, reimportar, correr el E2E de 4.° básico en los 3 navegadores y el backend completo.

- 2026-11-07 16:00: **Primero al retomar:**
  1. Repetir el E2E de 4.° básico en los 3 navegadores. La última corrida falló de forma
     intermitente porque el Mac se estaba frenando por temperatura (`kernel_task` alto, registro de
     más de 20 s) después de 2 horas de Kokoro, no por el contenido: antes de la última reescritura
     daba 54/54. Antes de correrlo, verificar que `uptime` muestre una carga baja.
  2. Regenerar los audios de forma incremental:
     `DATABASE_URL=… LIMPIAR_HUERFANOS=1 scripts/voz/generar_audios.sh`. Ahora usa la mitad de los
     núcleos. Hay que hacerlo porque cambiaron textos de 1.° básico (rebalanceo) y de 4.° básico
     (pruebas reescritas).

- 2026-11-07: tarea 6 cerrada (§15.32). Solo 1.° básico tenía sesgo (b 37,6 % → 30 %); el resto de los cursos queda entre 20 y 29 % por letra. La tarea 5 (audio de 3.° y 4.° básico) se está generando en segundo plano.

- 2026-11-07: tareas 1 a 4 cerradas (§15.31). Voz «alex» en 608 audios. Marcadores nuevos `::largo::`, `::regla::` y `::balanza::`. Barrido de 1.° a 4.° básico.

- 2026-11-07: cola creada. El usuario agregó: reparaciones en `main`, funcionalidades nuevas en
  ramas aparte, y avanzar al máximo lo que dependa de cuentas externas, con pendientes para él.
