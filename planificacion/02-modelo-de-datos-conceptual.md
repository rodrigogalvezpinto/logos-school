---
título: Modelo de datos conceptual
estado: borrador — entidades y relaciones a nivel conceptual, no es un esquema de base de
  datos todavía
última actualización: 2026-08-10
---

Este documento describe las entidades principales y cómo se relacionan, en lenguaje simple,
como insumo para el futuro diseño técnico (no es aún un modelo entidad-relación formal).

# Entidades principales

## Nivel
Uno de los 12 niveles fijos del sistema escolar chileno: 1° a 8° básico, 1° a 4° medio.
Es contenido **fijo y base**, definido por los temarios UCE. No lo crean los profesores ni
los administradores vía la app (al menos no en el MVP) — viene de la fuente curricular
oficial en `Temarios/analisis/`.

Cada Nivel tiene:
- Un decreto de bases curriculares asociado.
- Un formato de examen (integrado o separado por asignatura; N° de preguntas; duración;
  materiales permitidos) — ver el análisis por curso.
- Una o más **Asignaturas**.

## Asignatura
Pertenece a un Nivel (ej. "Matemática — 6° básico"). Contiene:
- Ejes temáticos.
- Objetivos de Aprendizaje (OA), cada uno con sus Indicadores de Evaluación — esta es la
  unidad mínima de contenido curricular sobre la que se construye material de estudio y
  preguntas de autoevaluación.

## Curso/Sección
Grupo con roster (ej. "6° básico A"), creado y administrado por un **Profesor**. Pertenece a
un único Nivel. Tiene una lista de Alumnos miembros, agregados exclusivamente por el
Profesor (o eventualmente un Administrador).

Importante: el Curso/Sección es **opcional** para el Alumno — no es requisito para estudiar,
solo habilita seguimiento por parte de un profesor.

## Usuario
Entidad base con rol: **Alumno**, **Apoderado**, **Profesor** o **Administrador** (ver
`01-roles-y-permisos.md`). Un mismo correo/cuenta probablemente tiene un solo rol principal
(a confirmar si una persona podría tener más de un rol, ej. un profesor que también es
apoderado de su propio hijo en la plataforma — es un caso real y probable, vale la pena
diseñar el modelo de usuario para permitir múltiples roles desde el inicio aunque el MVP
solo use uno).

## Progreso / Resultado
Registro de la actividad de estudio y desempeño de un Alumno: qué contenido revisó, qué
autoevaluaciones rindió, qué OA domina o le falta reforzar. Es la base para los reportes que
verá el propio Alumno, su Apoderado, y (fase 2) su Profesor.

# Relaciones

| Relación | Cardinalidad | Notas |
|---|---|---|
| Alumno — Nivel | 1 Alumno → 1 Nivel (a la vez) | Autoasignado por el alumno al registrarse o cambiar de año. |
| Alumno — Curso/Sección | 1 Alumno → 0 o 1 Curso/Sección | Solo el Profesor agrega al alumno; el alumno no puede autoagregarse. |
| Profesor — Curso/Sección | 1 Profesor → 0..N Cursos/Secciones | Un profesor puede tener varios cursos, incluso en distintos niveles. |
| Curso/Sección — Nivel | 1 Curso/Sección → 1 Nivel | Un curso pertenece a un único nivel (ej. no se mezcla 6° y 7° en la misma sección). |
| Apoderado — Alumno | 1 Apoderado → 1..N Alumnos | Un apoderado puede tener varios hijos/pupilos vinculados. Mecanismo de verificación del vínculo: pendiente de definir (ver `01-roles-y-permisos.md`). |
| Nivel — Asignatura | 1 Nivel → N Asignaturas | Fijo, viene del temario oficial (4 en básica, 6 en media, a confirmar variaciones por curso específico). |
| Asignatura — OA | 1 Asignatura → N Objetivos de Aprendizaje | Fijo, viene del temario oficial. |
| Alumno — Progreso | 1 Alumno → N registros de Progreso | Uno por interacción/evaluación relevante. |

# Diagrama conceptual (texto)

```
Administrador (backoffice, gestiona contenido base y verifica Profesores)
        │
        ▼
   Nivel (1..12) ──< Asignatura ──< Objetivo de Aprendizaje (+ indicadores)
        │
        ├──< Curso/Sección (creado por Profesor) >── Profesor (0..N cursos)
        │            │
        │            └──< Alumno (agregado solo por el Profesor)
        │
        └──< Alumno (autoasignado, con o sin Curso/Sección)
                     │
                     ├──< Progreso/Resultado
                     └──< Apoderado (1..N por alumno, vínculo verificado)
```

# Notas para el diseño técnico futuro (no bloqueantes ahora)

- El contenido curricular (Nivel → Asignatura → OA → Indicadores) es esencialmente
  **datos semilla** que se cargan una vez desde `Temarios/analisis/` y cambian poco (solo si
  Mineduc actualiza el decreto). Vale la pena modelarlo separado del contenido "vivo" que se
  genera dentro de la app (ejercicios, preguntas, material propio).
- El "banco de preguntas/ejercicios" para autoevaluación es contenido adicional que **no
  viene en los temarios** (los temarios solo dan OA e indicadores, no preguntas de examen
  reales) — hay que crearlo como parte del desarrollo de contenido, alineado a cada OA.
