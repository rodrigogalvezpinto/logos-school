---
título: Tipos de contenido de estudio por curso
estado: vigente — define qué debe existir para cada curso además de la explicación por OA
última actualización: 2026-08-10
---

El usuario pidió ampliar el alcance del contenido: no basta con explicación + ejemplos +
banco de preguntas por Objetivo de Aprendizaje (lo que ya está completo para los 12 cursos).
Cada curso debe tener, además, **guías**, **pruebas por materia** y **exámenes** tipo
simulacro. Este documento define cada uno y su estado.

## 1. Guía de estudio — ✅ ya cubierta

Lo que se produjo en `contenido/{curso}/{asignatura}.md` (explicación pedagógica por OA +
ejemplos resueltos + glosario) **cumple la función de guía de estudio**. No es un tipo de
contenido nuevo por construir — es lo que ya está completo para los 12 cursos. Si el usuario
quisiera un formato de guía distinto (ej. un resumen/cheat-sheet más corto, o un PDF
imprimible), eso sería una variante de presentación del mismo contenido, no contenido nuevo
— a definir si se necesita más adelante.

## 2. Pruebas por materia — pendiente de construir

Además del banco de preguntas de autoevaluación organizado por OA (que ya existe y es apto
para practicar objetivo por objetivo), falta una **prueba por asignatura**: un conjunto de
preguntas seleccionadas del banco existente, presentado como una prueba única con formato
similar al examen real de esa asignatura (mismo número de preguntas y tipo de cobertura que
usa el Mineduc para esa asignatura en ese curso), para que el alumno practique "como si
fuera la prueba real" de una sola asignatura, no solo OA por OA.

**Se puede construir ahora** reutilizando el banco de preguntas ya creado, porque el formato
base (N° de preguntas por asignatura) ya se conoce por curso desde el análisis de los
temarios (`Temarios/analisis/00-resumen-general.md`):
- Régimen A (1°-4° básico): la "prueba por materia" no aplica igual, ya que el examen real
  no separa por asignatura — ver punto 3.
- Régimen B y C (5° básico en adelante): 25 preguntas por asignatura.

Aun así, se ajustará el formato una vez el usuario entregue ejemplos reales (ver punto 3).

## 3. Exámenes tipo simulacro — ✅ decisión tomada, en construcción

Este es un contenido distinto a las pruebas por materia: un **examen acumulativo** que
simula el examen real de fin de año, con la estructura oficial exacta de ese curso:

- **1°-4° básico (Régimen A)**: **un solo examen integrado**, con preguntas de las 4
  asignaturas mezcladas en una sola prueba (20 preguntas totales, confirmado textualmente en
  los propios temarios oficiales: *"Las asignaturas mencionadas serán evaluadas en una sola
  fecha de examinación y de forma integrada en una sola prueba global... consta de 20
  preguntas en total incluidas las cuatro asignaturas"*). **Este es el contenido genuinamente
  nuevo que falta** — las "pruebas por materia" ya construidas son por asignatura separada,
  no mezclada.
- **5° básico en adelante (Régimen B y C)**: el examen real YA es separado por asignatura, 25
  preguntas cada una — exactamente el formato que ya tienen las "pruebas por materia"
  construidas en el punto 2. Es decir, **para estos cursos, cada "prueba por materia" ya
  cumple la función de un examen simulacro** (misma estructura que el examen real). Se
  etiquetan como "Forma A" de cada asignatura.

**Decisión (2026-08-10, el usuario liberó la espera de ejemplos reales — "no necesitas que
yo te pase los simulacros... tú mismo puedes generarlo"):**

1. **Régimen A** — construir el examen integrado (2 versiones/"Formas" por curso, para que
   el alumno pueda repetir la práctica sin memorizar respuestas), mezclando preguntas de las
   4 asignaturas ya creadas. Distribución usada: 5 preguntas por asignatura (20 total),
   criterio propio razonable ya que el Mineduc no especifica una distribución exacta por
   asignatura dentro de la prueba integrada — no hay evidencia oficial de otra proporción.
2. **Régimen B y C** — las "pruebas por materia" ya construidas se reclasifican como
   **"Forma A"** del examen simulacro de cada asignatura (mismo formato, 25 preguntas). Queda
   como trabajo siguiente (no bloqueante, de menor prioridad) construir una "Forma B" por
   asignatura para dar variedad — es recombinación del banco existente, no contenido
   pedagógico nuevo, así que se puede hacer rápido más adelante.
3. Ya no se espera ningún ejemplo externo — la fuente de verdad es el texto oficial de los
   12 temarios (`Temarios/analisis/`), que ya especifica el formato de examen exacto por
   curso.

## Hallazgo de investigación en mineduc.cl (2026-08-10)

El Mineduc publica en `epja.mineduc.cl/validacion-de-estudios/material-apoyo-la-examinacion/`
"preguntas de ejemplo" oficiales con pauta de corrección — pero corresponden al programa de
**Validación de Estudios Adultos (mayores de 18 años)**, decretos 257/2009 y DS 10, que
agrupa cursos en "Niveles" (Nivel Básico 1/2/3, Nivel Medio 1/2), **distinto** del programa
"para Menores de Edad" que usa nuestro proyecto (decretos 439/2012, 614/2013, 193/2019, por
curso individual). Confirmado: la sección específica de menores de edad
(`epja.mineduc.cl/.../examenes-libres-menores-de-18-anos/cuales-son-los-temarios-...`) enlaza
exactamente a los mismos 12 PDF que ya tenemos en `Temarios/`, sin un repositorio propio de
"preguntas de ejemplo" separado — no hay un accesible online para menores de edad al momento
de esta búsqueda.

Aun así, el material de adultos revela información valiosa y transferible sobre el **formato
real** que Mineduc usa (probablemente compartido entre ambos programas, mismo organismo):
- Las pruebas reales combinan **alternativas de 4 opciones** y **preguntas abiertas** de
  respuesta breve o extensa — no son solo alternativas, como habíamos asumido.
- Las preguntas suelen apoyarse en un **contexto o estímulo** (texto, ilustración, gráfico,
  tabla, mapa, esquema, noticia adaptada).
- Cada examen real termina con una **Pauta de Corrección**: tabla con N° de pregunta, clave
  (o criterio de respuesta correcta/incorrecta para preguntas abiertas) y referencia al
  contenido/indicador del temario que evalúa esa pregunta.
- **Aviso legal importante**: las pruebas reales están protegidas por Ley N°17.336
  (Propiedad Intelectual) y N°20.285 (Transparencia) como material confidencial — no se
  deben reproducir preguntas reales textualmente. Nuestro banco de preguntas ya es contenido
  original propio, así que esto no es un problema, pero conviene tenerlo presente si en el
  futuro se recibe un ejemplo real de examen: usarlo como referencia de formato/estilo, no
  copiar su contenido literal.

**Decisión (sin esperar más confirmación, seguir el modo de operación autónomo):** se
incorpora este formato real (mezcla de alternativas + preguntas abiertas + Pauta de
Corrección) a las "pruebas por materia" (punto 2), que ya se puede empezar a construir ahora
reutilizando el banco de preguntas existente. Se mantiene en espera solo la estructura fina
de los "exámenes" acumulativos (punto 3) hasta que lleguen los ejemplos reales que el usuario
ofreció enviar, ya que esos sí definen la distribución exacta de preguntas por curso.

## Resuelto

- "Cinco exámenes" que mencionó el usuario para 1° medio en adelante = las 5 asignaturas del
  Régimen B (Lenguaje/Lengua, Matemática, Ciencias Naturales, Historia, Inglés). En Régimen C
  son 6 (se agregan Ciencias para la Ciudadanía/Filosofía/Educación Ciudadana en vez de
  Ciencias Naturales/Historia, más Inglés) — el usuario habló en términos generales de
  Régimen B, coherente con lo ya confirmado en los temarios.
- Distribución de las 20 preguntas del examen integrado de básica: sin evidencia oficial de
  una proporción específica por asignatura — se usó 5 preguntas por asignatura (criterio
  propio razonable, documentado arriba).
- Formato de presentación: un archivo Markdown por examen/forma, en
  `contenido/{curso}/examenes/`, con encabezado tipo prueba real (instrucciones, tiempo,
  fecha de aplicación única para básica) y Pauta de Corrección final, mismo patrón que las
  pruebas por materia.
