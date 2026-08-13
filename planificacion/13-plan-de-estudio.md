---
título: Plan de estudio con horario (Fase 1.3)
estado: especificación lista para desarrollo (2026-08-12)
última actualización: 2026-08-12
---

## Problema que resuelve

Sin estructura, un alumno estudia "solo cuando quiere" — irregular, sin cobertura
garantizada del temario antes del examen. El Plan de Estudio ordena eso: reparte el
contenido pendiente en sesiones según una frecuencia que la familia elige, para que el
avance sea constante y predecible.

## Cómo funciona

1. **Elegir frecuencia**: el Apoderado o el Alumno elige cuántos días a la semana va a
   estudiar — **3, 4 o 5 días**. Se puede elegir además qué días de la semana (ej. lunes,
   miércoles, viernes) o dejar que el sistema los sugiera de forma pareja.
2. **Generar el cronograma**: el sistema toma todo el contenido pendiente del Alumno (OA no
   dominados aún, de las asignaturas de su Nivel) y lo reparte en sesiones, una por cada día
   de estudio elegido, hasta cubrir el temario completo. Reparto simple, sin IA:
   - Se calcula cuántos OA/unidades quedan pendientes en total.
   - Se dividen equitativamente entre las sesiones disponibles hasta una fecha objetivo (si
     se conoce la fecha del examen real del Alumno) o en un plazo por defecto razonable
     (ej. 8-10 semanas) si no se conoce.
   - Cada sesión asigna una asignatura y uno o más OA específicos a estudiar ese día, más,
     cuando corresponda, una prueba de unidad de cierre de eje.
   - Se van rotando las asignaturas entre sesiones (no todo Matemática seguido) para
     mantener variedad, salvo que el Alumno prefiera concentrarse en una que le cuesta más
     (ajuste manual, no automático en el MVP).
3. **Vista de calendario**: el Alumno ve su semana con las sesiones programadas, y puede
   marcar cada una como cumplida (o el sistema la marca automáticamente si el Alumno estudió
   ese contenido ese día).
4. **Recordatorio del día**: al entrar a la plataforma en un día de estudio programado, se
   muestra de forma destacada "hoy te toca: Matemática — Geometría" con acceso directo,
   antes que cualquier otra cosa.
5. **Flexibilidad**: si un día no se cumple, el sistema reordena las sesiones siguientes
   (no se pierde contenido, se corre el cronograma) — no debe sentirse punitivo ni rígido.

## Qué necesita el modelo de datos (agregar a `11-especificacion-mvp-para-desarrollo.md`)

```
PlanDeEstudio
  id
  perfil_alumno_id      (FK → PerfilAlumno)
  dias_por_semana        (3 | 4 | 5)
  dias_elegidos           (lista de días de la semana, ej. ["lunes","miércoles","viernes"])
  fecha_inicio
  fecha_objetivo          (nullable — fecha del examen real, si se conoce)

SesionEstudio
  id
  plan_estudio_id        (FK → PlanDeEstudio)
  fecha_programada
  asignatura_id           (FK → Asignatura)
  oa_ids                  (lista de OA a cubrir ese día)
  incluye_prueba_unidad   (bool — si esta sesión cierra con una prueba de unidad)
  estado                  ("pendiente" | "cumplida" | "reprogramada")
```

## Requisitos adicionales del usuario (2026-08-13, a incorporar al diseño detallado)

El usuario adelantó, antes de que le tocara el turno a esta fase, tres piezas que se deben
diseñar juntas porque son la misma funcionalidad vista desde ángulos distintos:

1. **Cronograma orientado a la fecha del examen real** (no solo un plazo por defecto).
2. **Simulacro parcial**: a medida que el alumno avanza (ej. llega a la mitad del temario),
   debe poder rendir un examen simulacro acotado al % de materia ya cubierta — no el
   simulacro completo Forma A/B. Requiere que el motor de evaluación pueda generar un
   `ConjuntoEvaluacion` dinámico acotado a un subconjunto de OA (hoy los conjuntos son
   fijos, importados desde contenido estático).
3. **Habilitación progresiva + lista de "faltantes"**: las pruebas de unidad y exámenes no
   deberían estar todos disponibles desde el día uno — se van habilitando según el avance
   del alumno (mismo motor de "en qué momento se habilita" que decide cuándo el simulacro
   parcial del punto 2 está disponible). La vista de notas (`/alumno/notas`, Fase 1.2) debe
   mostrar no solo lo ya rendido sino también qué pruebas/exámenes faltan y cuáles ya están
   habilitados para rendir — esto se construye junto con la habilitación progresiva, no
   antes, para no armar la lista de pendientes dos veces.
4. Onboarding: el apoderado elige los días de estudio (mínimo 3/semana) y el sistema
   calcula cuántas horas por asignatura corresponden esos días.

## Fuera de alcance de esta especificación

- Notificaciones push/email del recordatorio de estudio — se puede sumar en una iteración
  posterior de esta misma fase; lo esencial es que el calendario exista dentro de la app.
- Ajuste automático inteligente del ritmo según desempeño (ej. "va lento en Matemática,
  darle más sesiones") — versión simple primero (reparto parejo), esto queda como mejora
  futura en `06-ideas-futuras.md`.
- Coordinación con la fecha real de inscripción al examen Mineduc (que requiere que el
  Apoderado haya hecho el trámite real, fuera de la plataforma) — el campo
  `fecha_objetivo` existe para cuando se quiera conectar esto, pero no es parte del MVP de
  esta fase.
