# Auditoría de evaluaciones de 4.º básico — primera pasada ampliada

**Rama:** `qa/fase-2-matriz-trazabilidad`  
**Alcance:** revisión documental de las 12 pruebas de unidad y los dos exámenes integrados Forma A/B de `contenido/04-basico/`, con atención a consistencia entre enunciado, alternativas y pauta, exactitud matemática y disponibilidad de los recursos referenciados. No se ejecutó la aplicación ni se certificó la alineación completa con los OA oficiales. No se modificó contenido fuente ni se tocó `main`.

## Hallazgos prioritarios

### LGS-4B-EVAL-001 — La clave de la ecuación en Forma B apunta a la alternativa equivocada
- **Severidad:** P1 (error verificable de pauta).
- **Archivo:** `contenido/04-basico/examenes/examen-integrado-forma-b.md`, pregunta 16.
- **Evidencia:** el enunciado pide resolver (x + 9 = 23). Las alternativas son a) 32, b) 14, c) 13, d) 15. La pauta declara **“c) 14”**.
- **Resultado:** el valor correcto es 14, pero corresponde a **b)**, no a c). Si el evaluador utiliza la letra de la pauta, podría marcar incorrectamente a un estudiante que respondió bien.
- **Acción recomendada:** corregir la clave en una fase de corrección posterior y agregar una prueba automatizada que contraste valor de respuesta y letra de alternativa.

### LGS-4B-EVAL-002 — La pregunta sobre estado de la materia contiene un término erróneo
- **Severidad:** P2 (claridad del enunciado).
- **Archivo:** `contenido/04-basico/examenes/examen-integrado-forma-a.md`, pregunta 15.
- **Evidencia:** el enunciado pregunta “¿Cuál de las siguientes es información líquida entre los siguientes materiales...?”.
- **Problema:** “información líquida” no tiene sentido en este contexto; el objetivo parece ser identificar la **materia** o el material en estado líquido.
- **Acción recomendada:** confirmar el sentido previsto y corregir el enunciado sin alterar la clave correcta (jugo de frutilla).

### LGS-4B-EVAL-003 — La Forma A y la Forma B tienen formatos de respuesta distintos; debe verificarse su coherencia con la promesa del producto
- **Severidad:** P2 (consistencia de experiencia y comparación).
- **Evidencia:** Forma A declara 20 preguntas de alternativas, cuatro opciones cada una. Forma B incluye preguntas abiertas y alternativas, y su instrucción también distingue ambos tipos.
- **Evaluación:** no es necesariamente un defecto si las formas tienen propósitos distintos, pero sí impide tratarlas como equivalentes sin una decisión explícita sobre comparabilidad, puntuación y condiciones de aplicación.
- **Acción recomendada:** definir una especificación común de evaluación (cantidad por asignatura, tipos de ítem, puntaje, tiempo y criterios de corrección) o documentar por qué las formas difieren.

### LGS-4B-EVAL-004 — Pregunta de Geografía combina un mapa hipotético con una pauta que repite el mismo río
- **Severidad:** P2 (diseño del ítem).
- **Archivo:** `contenido/04-basico/pruebas/historia-unidad-geografia.md`, pregunta 3.
- **Evidencia:** la pregunta describe cuatro ubicaciones numeradas y pide asignar Amazonas, Mississippi o Biobío; la pauta asigna Biobío tanto a (2) como a (4), con una nota que dice que un número puede repetir país.
- **Evaluación:** la repetición puede ser intencional y está anunciada, pero la descripción de (2) como “un río largo que recorre el sur de Chile” no identifica con precisión el Biobío y no hay un mapa visual real en el archivo, sino una instrucción para imaginarlo.
- **Acción recomendada:** incluir un mapa real y verificable o proporcionar pistas geográficas suficientes para cada río; confirmar si se desea evaluar localización, reconocimiento de nombres o lectura cartográfica.

## Comprobaciones correctas en la muestra

- Forma A, pregunta 5: 347 + 486 = 833, clave b correcta.
- Forma A, pregunta 9: 96 ÷ 8 = 12, clave b correcta.
- Forma A, pregunta 13: $2.000 − ($1.350 + $290) = $360, clave b correcta.
- Forma A, pregunta 18: un rectángulo no cuadrado tiene dos ejes de simetría, clave c correcta.
- Forma B, pregunta 3: 124 × 6 = 744, clave c correcta.
- Forma B, pregunta 7: 9 de 24 estudiantes equivale a 9/24 si el ítem solicita representar la fracción de quienes llevan fruta.
- En la prueba de Matemática de Medición y Datos, las conversiones, áreas y lecturas del pictograma/gráfico visibles son coherentes con la pauta.

## Observaciones sobre recursos visuales

En la prueba de Geografía, pregunta 3, el mapa está descrito en texto como algo que el estudiante debe imaginar; no hay un recurso cartográfico incrustado en ese Markdown. La prueba de Matemática de Medición y Datos, en cambio, sí incorpora tablas de símbolos que permiten responder las preguntas de pictograma y gráfico sin depender de una imagen externa.

Debe verificarse en la aplicación que todos los recursos visuales de las otras pruebas y de los simulacros existan y se rendericen; esta revisión de Markdown no permite certificar su presentación en la interfaz.

## Pendientes para cerrar 4.º básico

1. Revisar uno a uno todos los ítems y sus pautas de las 12 pruebas y ambos simulacros; esta pasada no certifica cada pregunta.
2. Validar cada clave tanto por valor como por letra de alternativa.
3. Comprobar los OA declarados contra las Bases Curriculares y el programa de estudio oficial vigente.
4. Revisar duplicados entre guías, pruebas de unidad y simulacros.
5. Verificar que los criterios de respuesta abierta permitan equivalencias válidas y que el sistema pueda corregirlas adecuadamente.
6. Inspeccionar la interfaz real para confirmar que tablas, mapas e imágenes estén presentes y sean accesibles.

## Estado
**4.º básico: auditoría parcial ampliada a evaluaciones; no cerrada ni certificada.** El hallazgo LGS-4B-EVAL-001 es un error inequívoco de clave y debe priorizarse en la fase de corrección posterior. En esta fase solo se documenta; no se modifica el contenido fuente.
