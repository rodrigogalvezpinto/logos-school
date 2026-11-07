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
  3. Reimportar con `reimportar.sh` (base aislada `logos_e2e_alternativas`).
  4. Validación E2E del curso afectado en los 3 navegadores.
- Commit por tarea, con el trailer `Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>`, y push.
- Registrar cada cierre en `AUDITORIA_MAESTRA.md` (§15.x siguiente).
- Las **reparaciones** (errores de contenido, defectos y deuda de la auditoría) van en `main`.
  Las **funcionalidades nuevas** van en una rama aparte, `feature/<nombre>`: se hace push de la
  rama, sin merge, y el usuario la revisa después.
- Lo que dependa de una cuenta externa o del usuario se **prepara al máximo**: código detrás de
  variables de entorno, `.env.example` y guía paso a paso. Lo que el usuario debe hacer se anota en
  `docs/PENDIENTES-USUARIO.md` (cuentas, claves y decisiones) y se pasa a la siguiente tarea.

## Entorno local (por si la sesión se reinicia)

- La API E2E corre en el puerto 8001. La SPA está compilada en `frontend/dist/frontend/browser`
  y se sirve en el 4300 con `servir_spa.mjs` del scratchpad de la sesión.
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

## Tareas

| # | Tarea | Estado |
|---|---|---|
| 1 | Regenerar los audios con Kokoro «alex» (elegida por el usuario), verificar E2E 1.° básico y hacer commit | ✅ hecho 2026-11-07 |
| 2 | 1.° básico: reemplazar las ~20 descripciones `[Imagen: …]` y `::emoji::` que dan pistas o la respuesta (lápiz corto/largo, pollitos, materiales, secuencias) por dibujos (`::dibujo::`, `::contar::`, `::posicion::`, `::fila::`) o por un enunciado neutro | ✅ hecho 2026-11-07 |
| 3 | 2.° básico: el mismo barrido de descripciones de imagen que delatan la respuesta | ✅ hecho 2026-11-07 |
| 4 | 3.° y 4.° básico: el mismo barrido (más corto: hay menos imágenes) | ✅ hecho 2026-11-07 |
| 5 | Audio pregrabado para 3.° y 4.° básico (régimen A completo), con revisión de `texto-para-voz` sobre sus textos reales | pendiente |
| 6 | Segunda pasada a los sesgos de clave: distribución de letra correcta y de «la alternativa más larga» por curso, tras las correcciones del 2026-11-07 (§15.23–15.24) | ✅ hecho 2026-11-07 |
| 7 | Superposición del 79 % entre pruebas de unidad y autoevaluaciones de guía. Decisión de experto: una prueba no debe repetir textualmente lo ya practicado. Reescribir los ítems duplicados con contextos nuevos, el mismo OA y la misma dificultad, curso por curso, empezando por 4.° básico (piloto) | en curso: 4.° básico, Geometría hecha (8 de 76) |
| 8 | Simulacros **Forma A** del régimen B/C (5.° básico a 4.° medio): uno por asignatura, mismo formato oficial que la Forma B (25 preguntas, alternativas), con otros ítems. Curso por curso, empezando por 5.° básico | pendiente |
| 9 | Reconciliar `matriz-maestra-estado-por-archivo.csv` con la revisión ítem por ítem (§15.26–15.28) y actualizar las cifras vigentes en `CLAUDE.md` (sacar los números históricos que ya no aplican) | pendiente |
| 10 | Accesibilidad: recorrido con axe en las pantallas de alumno (guía, autoevaluación, prueba y resultados) en los 3 navegadores; corregir lo que salga | pendiente |
| 11 | `docs/PENDIENTES-USUARIO.md`: lista de cuentas y claves que hacen falta (Neon, Render, Cloudflare Pages/R2, Resend, Google OAuth, Turnstile, Sentry, UptimeRobot, pasarela de pago, API de IA), con costo, paso a paso y dónde se configura cada una. También las decisiones abiertas | ✅ hecho 2026-11-07 (`docs/PENDIENTES-USUARIO.md`) |
| 12 | Preparar el despliegue sin desplegar: verificar `.env.example`, la configuración de producción, el CSP y los headers. Script para publicar los audios en R2 o en el build. Checklist de despliegue paso a paso. Va en `main` (es documentación y configuración) | ✅ hecho 2026-11-07 (`docs/DESPLIEGUE.md`, `render.yaml`, CORS configurable) |
| 13 | Rama `feature/juegos-practica`: juegos de práctica con el banco de preguntas (Fase 2 de Brincus, sin dependencias externas). Diseño en `planificacion/` y después la construcción, con pruebas | pendiente |
| 14 | Rama `feature/profesor-ia`: tutor con IA (Fase 2 de Brincus). Se construye detrás de una variable de entorno (sin clave queda desactivado), con salvaguardas para menores y un adaptador de pruebas. Se activa cuando el usuario entregue la clave | pendiente |
| 15 | Rama `feature/pasarela-pago`: adaptador de pagos (Flow, Mercado Pago o Webpay, a elegir por el usuario) con interfaz y modo de prueba. Queda detrás de una variable de entorno | pendiente |

## Bitácora

- 2026-11-07: tarea 6 cerrada (§15.32). Solo 1.° básico tenía sesgo (b 37,6 % → 30 %); el resto de los cursos queda entre 20 y 29 % por letra. La tarea 5 (audio de 3.° y 4.° básico) se está generando en segundo plano.

- 2026-11-07: tareas 1 a 4 cerradas (§15.31). Voz «alex» en 608 audios. Marcadores nuevos `::largo::`, `::regla::` y `::balanza::`. Barrido de 1.° a 4.° básico.

- 2026-11-07: cola creada. El usuario agregó: reparaciones en `main`, funcionalidades nuevas en
  ramas aparte, y avanzar al máximo lo que dependa de cuentas externas, con pendientes para él.
