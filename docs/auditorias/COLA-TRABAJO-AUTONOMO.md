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
- Las tareas que requieran una decisión del usuario se marcan **⏸ espera al usuario** y se pasa a
  la siguiente.

## Entorno local (por si la sesión se reinicia)

- La API E2E corre en el puerto 8001. La SPA está compilada en `frontend/dist/frontend/browser`
  y se sirve en el 4300 con `servir_spa.mjs` del scratchpad de la sesión.
- Para volver a compilar:
  `npx ng build --configuration development --define "LOGOS_API_URL='http://localhost:8001'"`.
- Para generar los audios: `DATABASE_URL=… scripts/voz/generar_audios.sh ["1° básico" …]`.

## Tareas

| # | Tarea | Estado |
|---|---|---|
| 1 | Regenerar los audios con Kokoro «alex» (elegida por el usuario), verificar E2E 1.° básico y hacer commit | en curso |
| 2 | 1.° básico: reemplazar las ~20 descripciones `[Imagen: …]` y `::emoji::` que dan pistas o la respuesta (lápiz corto/largo, pollitos, materiales, secuencias) por dibujos (`::dibujo::`, `::contar::`, `::posicion::`, `::fila::`) o por un enunciado neutro | pendiente |
| 3 | 2.° básico: el mismo barrido de descripciones de imagen que delatan la respuesta | pendiente |
| 4 | 3.° y 4.° básico: el mismo barrido (más corto: hay menos imágenes) | pendiente |
| 5 | Audio pregrabado para 3.° y 4.° básico (régimen A completo), con revisión de `texto-para-voz` sobre sus textos reales | pendiente |
| 6 | Segunda pasada a los sesgos de clave: distribución de letra correcta y de «la alternativa más larga» por curso, tras las correcciones del 2026-11-07 (§15.23–15.24) | pendiente |
| 7 | Superposición del 79 % entre pruebas de unidad y autoevaluaciones de guía. Decisión de experto: una prueba no debe repetir textualmente lo ya practicado. Reescribir los ítems duplicados con contextos nuevos, el mismo OA y la misma dificultad, curso por curso, empezando por 4.° básico (piloto) | pendiente |
| 8 | Simulacros **Forma A** del régimen B/C (5.° básico a 4.° medio): uno por asignatura, mismo formato oficial que la Forma B (25 preguntas, alternativas), con otros ítems. Curso por curso, empezando por 5.° básico | pendiente |
| 9 | Reconciliar `matriz-maestra-estado-por-archivo.csv` con la revisión ítem por ítem (§15.26–15.28) y actualizar las cifras vigentes en `CLAUDE.md` (sacar los números históricos que ya no aplican) | pendiente |
| 10 | Accesibilidad: recorrido con axe en las pantallas de alumno (guía, autoevaluación, prueba y resultados) en los 3 navegadores; corregir lo que salga | pendiente |
| 11 | Fase 2 de Brincus sin dependencias externas: juegos de práctica con el banco de preguntas. Primero diseño en `planificacion/` y después la construcción | pendiente |
| — | Profesor con IA, pasarela de pago, Google, Resend y despliegue | ⏸ espera al usuario (servicios o credenciales externas) |

## Bitácora

- 2026-11-07: cola creada.
