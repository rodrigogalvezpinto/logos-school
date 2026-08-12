---
título: Diseño diferenciado — pruebas de unidad vs. exámenes simulacro
estado: decisión tomada (2026-08-11), en ejecución
última actualización: 2026-08-11
---

## El problema detectado

El usuario notó, con buen criterio, que nuestras "pruebas por materia" (58 archivos, uno por
asignatura/curso) tenían el mismo tamaño que el examen real (20-25 preguntas). Eso está mal
en dos sentidos:
1. **No imita nada real** — el examen real de Mineduc no tiene un formato "prueba
   intermedia", así que copiarle el tamaño no tiene justificación pedagógica.
2. **Abruma a los niños pequeños** — una prueba de 20-25 preguntas para un niño de 6-8 años
   que recién termina una unidad es una carga cognitiva y de tiempo desproporcionada, y no
   corresponde a cómo se evalúa a esa edad en el sistema escolar real (pruebas cortas,
   frecuentes, por unidad).

## Decisión (autoridad pedagógica + psicoevolutiva, sin más consulta)

Se separan definitivamente dos funciones que antes se mezclaban:

### A. Exámenes simulacro — imitan EXACTAMENTE el examen real
Sin cambios, ya están correctos y validados contra el texto oficial de los temarios:
- **1°-4° básico**: 20 preguntas, prueba única integrando las 4 asignaturas (así es el
  examen real — Mineduc: *"La prueba global consta de 20 preguntas en total incluidas las
  cuatro asignaturas"*).
- **5° básico-4° medio**: 25 preguntas por asignatura, pruebas separadas (Mineduc: *"Cada
  prueba consta de 25 preguntas por cada asignatura"*).
- Se rinden pocas veces (idealmente cerca de la fecha real), simulando la condición real:
  tiempo, formato, sin ayuda.

### B. Pruebas de unidad — NO imitan el examen, sirven para ir chequeando avance
Se reestructuran las 58 "pruebas por materia" actuales (que serán reemplazadas) en
**varias pruebas más cortas por asignatura, una por cada eje temático o bloque de
Objetivos de Aprendizaje**, del tamaño que corresponda a la edad — no al examen.

**Tabla de calibración por edad (criterio propio, sin evidencia oficial de un tamaño
"correcto" porque Mineduc no define pruebas intermedias — esto es una decisión pedagógica
nuestra):**

| Ciclo | Cursos | Edad | Preguntas por prueba de unidad | Unidad = |
|---|---|---|---|---|
| Básica inicial | 1°-2° básico | 6-8 años | **6-8 preguntas** | 1-2 OA agrupados (sesión corta, ~15 min) |
| Básica media | 3°-4° básico | 8-10 años | **8-10 preguntas** | Eje temático completo |
| Básica media-superior | 5°-6° básico | 10-12 años | **10-12 preguntas** | Eje temático completo |
| Básica superior / media inicial | 7°-8° básico, 1°-2° medio | 12-16 años | **12-15 preguntas** | Eje temático completo |
| Media superior | 3°-4° medio | 16-18 años | **12-15 preguntas** | Eje o módulo (pocos OA por asignatura en este régimen, así que a veces "unidad" = la asignatura casi completa) |

**Por qué esta progresión:** sigue el principio pedagógico estándar de carga cognitiva
progresiva (capacidad de atención sostenida y tolerancia a la evaluación aumenta con la
edad), y es coherente con cómo el propio sistema escolar chileno evalúa por unidad en la
práctica (pruebas cortas y frecuentes en básica inicial, más extensas en media).

**Cómo se arma cada prueba de unidad:** se reutiliza el banco de preguntas ya existente por
OA (`contenido/{curso}/{asignatura}.md`), agrupando por eje temático donde ya existe esa
estructura (Matemática, Ciencias Naturales, Historia) o por bloques de 2-3 OA donde no hay
ejes explícitos (Lenguaje, Inglés, y las asignaturas del Régimen C con pocos OA). No se
inventa contenido pedagógico nuevo — es reorganización + selección de lo ya creado, mismo
principio de bajo riesgo que se usó para construir la Forma B de los exámenes.

## Qué pasa con los 58 archivos "prueba" actuales

Se reemplazan por la nueva estructura de pruebas de unidad (varios archivos más cortos por
asignatura, en `contenido/{curso}/pruebas/{asignatura}-unidad-{N}.md`). El contenido de las
"pruebas" actuales no se pierde — la mayoría de esas preguntas ya provienen del banco por OA,
así que se redistribuyen en las nuevas pruebas de unidad más pequeñas.

## Estado de ejecución

Ver `contenido/00-estado-contenido.md` para el avance curso por curso.
