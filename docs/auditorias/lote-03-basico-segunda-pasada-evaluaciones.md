# Auditoría de evaluaciones de 3.º básico — segunda pasada

**Rama:** `qa/fase-2-matriz-trazabilidad`  
**Alcance:** revisión de las 12 pruebas de unidad y de las Formas A/B del examen integrado de 3.º básico, con inspección de claves visibles y comparación directa entre simulacros. Es una revisión documental; no se ejecutó la aplicación ni se certificó alineación completa con OA oficiales. No se modificaron archivos fuente ni `main`.

## Hallazgos

### LGS-3B-EVAL-001 — Forma B repite estímulos y preguntas de la Forma A pese a declarar que todas son distintas
- **Severidad provisional:** P1 para la promesa del producto de ofrecer dos simulacros sin repetir contenido; P2 para validez de evaluación.
- **Evidencia directa:**
  - Ambas formas reutilizan literalmente el cuento **“El cometa de Joaquín”**, su ilustración y preguntas asociadas. Forma A pregunta la ciudad y cómo es Antonia; Forma B pregunta si el cometa quedó enredado en el espino.
  - Ambas formas reutilizan el poema **“La huerta de mi tía”** y la misma ilustración. Forma A evalúa la afirmación de que las abejas bailan; Forma B pregunta por la ciudad y la expresión “los tomates duermen colorados”.
  - Ambas formas reutilizan el texto informativo **“Los pingüinos de Humboldt”** y la misma ilustración. Forma A pregunta por su alimentación; Forma B pregunta qué subtítulo permite ubicar información sobre el peligro de la especie.
  - Ambas formas repiten la imagen del grupo de pingüinos y la imagen de la tía y su sobrino en la huerta; también aparece la misma ilustración del niño que trepa el espino.
- **Declaraciones en conflicto:** los encabezados de Forma A y Forma B dicen que las preguntas son distintas y que permiten practicar sin repetir contenido.
- **Recomendación:** decidir si “sin repetir contenido” significa no repetir preguntas exactas o tampoco textos/estímulos. Si la promesa es no repetir contenido, sustituir estímulos duplicados y comprobar semánticamente el conjunto; si se permiten textos compartidos con preguntas distintas, corregir la promesa para describirlo con precisión.

### LGS-3B-EVAL-002 — Prueba de Geografía usa una definición ambigua de “continentes”
- **Severidad provisional:** P2 (consistencia curricular/convención geográfica).
- **Evidencia:** `historia-unidad-geografia.md`, pregunta 3, pregunta cuántos continentes hay y la pauta establece **seis**.
- **Evaluación:** seis es una convención común en Chile y otros países hispanohablantes, pero existen modelos de seis y siete continentes según cómo se agrupen Europa/Asia y América. Sin especificar la convención utilizada en la guía, la pregunta puede penalizar a quien aprendió otro modelo válido.
- **Recomendación:** nombrar la convención utilizada en el material y mantenerla consistente en guía, pregunta, alternativas y pauta.

### LGS-3B-EVAL-003 — La guía de Geografía simplifica las estrategias de vivienda por zona climática
- **Severidad provisional:** P3 (riesgo de estereotipo cultural).
- **Evidencia:** `historia-unidad-geografia.md`, pregunta 8, asocia de forma directa zona fría con iglú, zona cálida con viviendas abiertas/elevadas y zona templada con calefacción/ventilación.
- **Evaluación:** son ejemplos didácticos posibles, pero la redacción de “vivienda típica” puede sugerir una solución universal y no distingue adaptación local, cultura, materiales disponibles ni época.
- **Recomendación:** presentarlas como ejemplos de ciertas comunidades y regiones, no como características universales de cada zona.

## Comprobaciones aritméticas y de claves

En la muestra examinada, las claves explícitas de Matemática que se comprobaron son correctas, entre ellas:
- 347 + 265 = 612.
- 725 − 358 = 367.
- 9 × 6 = 54.
- 42 ÷ 7 = 6.
- $890 × 5 = $4.450.
- En medición: perímetros de 18 cm y 40 cm frente a 36 cm; 2 kg + 500 g = 2.500 g; pictograma con 35 mascotas.
- En patrones: 215, 225, 235, 245, 255; y 27 más dos filas de diez = 47.

Las claves revisadas en las pruebas de Ciencias sobre reflexión del sonido, rotación/traslación, fases de la Luna y reciclaje coinciden con los enunciados visibles. Esto no certifica la totalidad de cada banco.

## Pendientes

1. Construir una matriz de cada pregunta de cada prueba de unidad y cada simulacro: enunciado, tipo, clave, explicación, OA y fuente de respaldo.
2. Comprobar la renderización efectiva de cada marcador `[Imagen: ...]` y que el recurso exista en la aplicación; el Markdown por sí solo no demuestra que la imagen se muestre.
3. Revisar exhaustivamente los simulacros por duplicados exactos y semánticos, no solo por número de pregunta.
4. Verificar alineación con fuentes curriculares oficiales vigentes y comprobar que la columna OA de cada pauta corresponda a la pregunta.
5. Revisar con fuentes especializadas las afirmaciones históricas/científicas que no puedan verificarse solo con consistencia interna.

## Estado
**3.º básico: auditoría ampliada de evaluaciones, todavía parcial.** Se identificó una contradicción comprobable entre la promesa de las Formas A/B y la reutilización de textos e ilustraciones. No se corrigió el contenido fuente en esta fase.
