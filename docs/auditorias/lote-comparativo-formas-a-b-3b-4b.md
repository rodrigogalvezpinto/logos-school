# Auditoría comparativa de pruebas integradas: 3.º y 4.º básico

- **Rama revisada:** `qa/fase-2-matriz-trazabilidad`
- **Fecha de revisión:** 2026-10-22
- **Alcance:** lectura de las cuatro pruebas completas, conteo de preguntas y filas de pauta, comparación inicial entre formas A/B y comprobación manual de discrepancias visibles.
- **Límite:** esta pasada no constituye validación curricular completa, revisión de todos los estímulos visuales renderizados ni certificación pedagógica.

## Archivos y evidencia revisada

| Curso | Forma A | Forma B |
|---|---|---|
| 3.º básico | [Examen integrado A](../../contenido/03-basico/examenes/examen-integrado-forma-a.md) | [Examen integrado B](../../contenido/03-basico/examenes/examen-integrado-forma-b.md) |
| 4.º básico | [Examen integrado A](../../contenido/04-basico/examenes/examen-integrado-forma-a.md) | [Examen integrado B](../../contenido/04-basico/examenes/examen-integrado-forma-b.md) |

## Resultados

### 3.º básico

- Ambas formas declaran 20 preguntas y tienen 20 filas de pauta.
- El contenido de lectura **«El cometa de Joaquín»** se reutiliza en ambas formas. En Forma A sirve para las preguntas 4 y 5; en Forma B vuelve a aparecer en la pregunta 4 de verdadero/falso. Por tanto, la afirmación de que la Forma B contiene preguntas distintas no se cumple en sentido estricto: al menos un estímulo y contenido evaluado se repiten.
- En esta pasada no se detectó una pregunta completa idéntica al comparar los bloques numerados; la reutilización del texto compartido sí quedó confirmada manualmente.
- **Acción recomendada:** reemplazar el estímulo repetido de Forma B o declarar de manera explícita que la segunda forma conserva algunos textos de la primera. Si se reemplaza, recalcular la pauta y repetir regresión de claves/puntajes.

### 4.º básico

- Ambas formas contienen 20 preguntas y 20 filas de pauta.
- **Hallazgo P1 confirmado en Forma B, pregunta 16:** el enunciado es «x + 9 = 23» y las alternativas son a) 32, b) 14, c) 13, d) 15. La pauta marca **c) 14**, pero el valor 14 corresponde a **b)**. La explicación también calcula correctamente (23 - 9 = 14), lo que deja una contradicción interna entre letra y valor.
- **Impacto:** una corrección automatizada o manual que use la letra de la pauta puede penalizar una respuesta correcta. No se modificó el examen fuente durante esta auditoría.
- **Acción recomendada:** corregir la clave a **b) 14** y añadir una prueba de regresión que compare letra, valor y explicación. Después revisar cómo importa y califica esta pregunta la aplicación.

## Estado de cierre

| Control | Estado |
|---|---|
| Conteo de preguntas y pauta (4 archivos) | Revisado: 20 preguntas por forma; 20 filas de pauta por forma |
| Comparación exhaustiva de dificultad y equivalencia A/B | Pendiente |
| Verificación de todas las claves y cálculos de 3.º básico | Pendiente |
| Verificación curricular contra fuentes oficiales Mineduc | Pendiente |
| Renderizado de imágenes/estímulos y revisión en la aplicación | Pendiente |
| Pruebas de importación, puntuación y persistencia en la aplicación | Pendiente |
| Corrección de la clave de 4.º básico Forma B Q16 | Hallazgo registrado; fuente sin modificar |
| Repetición del estímulo de 3.º básico entre formas | Hallazgo registrado; fuente sin modificar |

**Conclusión:** este lote encontró una discrepancia P1 de clave en 4.º básico Forma B y una reutilización de estímulo entre las formas de 3.º básico. El resto de los controles señalados como pendientes no debe interpretarse como aprobado.
