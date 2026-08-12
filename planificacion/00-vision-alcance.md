---
título: Visión y alcance
estado: borrador vivo — actualizar a medida que se tomen decisiones
última actualización: 2026-08-10
---

# Visión

Plataforma web para apoyar el estudio y la preparación de niños, niñas y adolescentes que
rendirán los **Exámenes Libres de Validación de Estudios** del Ministerio de Educación de
Chile (Decreto Bases Curriculares N°439/2012 para básica y N°193/2019 para media),
abarcando los 12 niveles: 1° a 8° básico y 1° a 4° medio.

El objetivo final es que sea **accesible para todas las personas**, gratuita o de muy bajo
costo. **Actualización 2026-08-12:** el modelo de negocio, antes fuera de alcance, ya se
definió — ver `09-modelo-de-negocio.md`. El contenido de estudio central (guías,
autoevaluación, pruebas, exámenes simulacro) es y seguirá siendo 100% gratuito; cualquier
ingreso futuro vendría solo de servicios opcionales (tutorías, acompañamiento en vivo), sin
tocar el acceso al contenido.

## Fuente de verdad del contenido

Los 12 temarios oficiales de la Unidad de Currículum y Evaluación (UCE) del Mineduc, ubicados
en `/Users/rodrigogalvez/Documents/Logos/Temarios/`, son la base curricular. Ya se extrajeron
completos a formato estructurado en `Temarios/analisis/` (12 archivos por curso +
`00-resumen-general.md` con la vista comparativa). **408 Objetivos de Aprendizaje en total**,
entre 17 (4° medio) y 44 (6° básico) por curso.

### Hallazgos clave del formato oficial de examen (confirmado, los 12 cursos)

No son dos regímenes ("básica" vs. "media"), sino **tres**:

| Régimen | Cursos | Formato | Decreto |
|---|---|---|---|
| A | 1° a 4° básico | Prueba **integrada única**, 20 preguntas totales, 4 asignaturas (Lenguaje, Matemática, Ciencias Naturales, Historia/Geografía y Cs. Sociales) | 439/2012 |
| B | 5° básico a 2° medio | Prueba **separada por asignatura**, 25 preguntas c/u, máx. 2 pruebas/día. Se agrega **Inglés** desde 5° básico en adelante | 439/2012 (5°-6° básico) / **614/2013** (7° básico en adelante) |
| C | 3° y 4° medio | Prueba **separada por asignatura** (25 preguntas c/u). Cambian las asignaturas: desaparecen Ciencias Naturales e Historia/Geografía/Cs. Sociales, aparecen **Ciencias para la Ciudadanía**, **Filosofía** y **Educación Ciudadana** | **193/2019** (currículum completamente distinto) |

Otros datos relevantes:
- En ningún nivel existe eximición de asignaturas; el temario completo se debe estudiar
  aunque la prueba solo aborde una selección de los OA.
- Materiales permitidos: diccionario en Inglés, calculadora en Matemática (donde aplica).
- Entre 6° y 7° básico también cambia el **nombre y decreto** de algunas asignaturas
  (ej. "Lenguaje y Comunicación" → "Lengua y Literatura"; los ejes de Ciencias Naturales
  pasan de "Vida / Físicas y Químicas / Tierra y Universo" a simplemente
  "Biología / Física / Química").
- El banco de preguntas de Ciencias Naturales e Historia de 1°-2° medio **no es reutilizable**
  para 3°-4° medio, porque esas asignaturas directamente no existen ahí — son currículums
  distintos, no una simple extensión.

Esto implica que el **motor de contenido y evaluación debe ser flexible a 3 formatos
distintos** (no solo 2), y que expandir de un nivel a otro dentro de la "misma" etapa
(ej. de 4° a 5° básico) puede implicar más que solo agregar contenido — puede cambiar el
formato de examen completo. Ver `Temarios/analisis/00-resumen-general.md` para el detalle
completo por curso.

# Decisiones tomadas

| Decisión | Resultado | Fecha |
|---|---|---|
| Prioridad de desarrollo (MVP) | **Un curso piloto único**, no todos los niveles a la vez | 2026-08-10 |
| Curso piloto específico | **4° básico** | 2026-08-10 |
| Rol del profesor en el MVP | **Autoestudio primero**; el profesor humano se incorpora en una fase posterior | 2026-08-10 |
| Modelo de "curso" | **Dos niveles**: (1) *Nivel* = el año que cursa el alumno (ej. 6° básico), autoasignado al registrarse, da acceso al material de estudio; (2) *Curso/Sección* (ej. "6° básico A") = grupo con roster (~15 alumnos) creado y gestionado por un profesor — el alumno **no puede autoagregarse**, solo el profesor lo agrega | 2026-08-10 |
| Alcance de costos/monetización | Definido: freemium con núcleo gratuito no negociable + financiamiento mixto de arranque (ver `09-modelo-de-negocio.md`) | 2026-08-12 |
| Modelo de registro y verificación | "Apoderado-primero": el apoderado crea la cuenta raíz y perfiles de alumno dentro de ella; sin flujo de vinculación posterior (ver `10-privacidad-y-datos-de-menores.md`) | 2026-08-12 |
| Rol Administrador | Confirmado, opera como backoffice del propio equipo en el MVP (no autoservicio) | 2026-08-12 |

## Corrección importante sobre el proceso real de examinación (2026-08-11)

Investigación directa en ayudamineduc.cl/epja.mineduc.cl (ver
`planificacion/07-experto-examenes-libres.md`) corrige un supuesto que teníamos: **no es un
solo examen al año en octubre**. Hay **3 periodos de examinación** (abril-junio; solo 4°
medio en septiembre-octubre; el resto en octubre), y la **entidad examinadora la asigna
Mineduc automáticamente**, no la elige la familia. Esto es relevante para cualquier futura
funcionalidad de la app relacionada con recordatorios de fechas o inscripción.

# Pendiente de decidir

- Si existe o se planea una entidad formal detrás del proyecto (fundación, ONG, empresa) —
  relevante para cuál vía de financiamiento de `09-modelo-de-negocio.md` aplica (Start-Up
  Chile requiere empresa constituida; fondos filantrópicos suelen preferir fundación). No es
  bloqueante para empezar a desarrollar el MVP.
- Validar con un abogado los artículos exactos de la Ley 21.719 antes de operar con datos
  reales de usuarios menores de edad (ver `10-privacidad-y-datos-de-menores.md`).

# Índice de documentos de planificación

1. `00-vision-alcance.md` — este documento
2. `01-roles-y-permisos.md` — perfiles de usuario y qué puede hacer cada uno
3. `02-modelo-de-datos-conceptual.md` — entidades y relaciones (Nivel, Curso, Asignatura, Usuario…)
4. `03-roadmap-etapas.md` — etapas de construcción, desde el piloto hasta la cobertura completa
5. `09-modelo-de-negocio.md` — modelo de sostenibilidad financiera
6. `10-privacidad-y-datos-de-menores.md` — marco legal y modelo de registro de menores
7. `11-especificacion-mvp-para-desarrollo.md` — especificación técnica lista para desarrollo
8. `../Temarios/analisis/` — contenido curricular extraído y estructurado por curso
9. `../CLAUDE.md` — contexto persistente del proyecto para nuevas conversaciones
