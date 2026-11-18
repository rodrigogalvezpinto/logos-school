# Juegos de práctica (Fase 2, tarea 13) — 2026-11-18

Rama `feature/juegos-practica` (sin unir a `main` hasta que el dueño lo apruebe).

## Qué es

Una página **Juegos** en el menú del alumno (antes marcada «pronto»), con dos modos que usan el **banco de
autoevaluación** de la asignatura elegida, mezclando todos sus OA:

| Modo | Regla | Para qué sirve |
|---|---|---|
| **Contrarreloj** | Responder la mayor cantidad de preguntas correctas en 90 segundos | Repaso rápido y fluidez |
| **Racha** | Responder seguido hasta el primer error | Precisión y concentración |

Cada respuesta muestra al instante si fue correcta y la explicación de la pauta (lo mismo que la autoevaluación).
No hay nota ni intento: es práctica. El mejor puntaje por asignatura y modo se guarda solo en el navegador.

## Decisiones

- **Solo preguntas cerradas** (alternativas, verdadero o falso, varias correctas), corregidas con la misma regla que
  la autoevaluación (`esRespuestaCorrecta`, todo o nada en «varias correctas»).
- **Solo el banco de autoevaluación**: se excluyen las preguntas de pruebas de unidad y simulacros, para no gastarlas.
- **Preguntas autosuficientes**: se excluyen las que remiten a un texto, tabla o ejemplo de la guía sin traerlo
  citado («Según el cuento…», «la tabla del Ejemplo 1»). Es una heurística (`sirve_para_juego`); no detecta, por
  ejemplo, preguntas que nombran a un personaje de una lectura. Mejora posible: marcar en el contenido las preguntas
  que dependen de un estímulo de la guía.
- **Cronómetro contra hora de término** (no resta por tic), igual que el examen.
- **Sin dependencias externas** y sin datos personales nuevos: el endpoint entrega preguntas del banco, como
  `/evaluaciones/autoevaluacion/{oa_id}`.

## Piezas

- Backend: `GET /evaluaciones/juego/asignatura/{asignatura_id}?cantidad=40` y
  `RepositorioPreguntas.buscar_banco_por_asignatura`. Tests en `tests/test_contenido_y_evaluaciones.py`.
- Frontend: `pages/juegos/juegos.ts` (ruta `/alumno/juegos`), test unitario de la corrección y `e2e/juegos.spec.ts`.

## Posibles siguientes pasos (no hechos)

- Otorgar XP por aciertos en los juegos, con tope diario, a través de gamificación.
- Un modo «Repaso de errores» con las preguntas falladas en autoevaluaciones y pruebas.
- Lectura en voz alta de la pregunta en 1.° y 2.° básico (el componente `BotonEscuchar` ya existe).
