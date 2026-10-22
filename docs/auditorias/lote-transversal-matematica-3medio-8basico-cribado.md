# Lote transversal — cribado de exámenes de Matemática de 3.º medio a 8.º básico

**Fecha:** 2026-10-22  
**Rama:** `qa/fase-2-matriz-trazabilidad`  
**Alcance:** lectura de claves y recálculo de una selección de operaciones de los exámenes Forma B. Se revisaron las pautas completas de 3.º medio, 4.º medio, 5.º básico y 6.º básico; en 7.º y 8.º básico se hizo un cribado de cálculos seleccionados. No incluye revisión pedagógica exhaustiva, cotejo curricular oficial, comparación con Forma A, recursos visuales ni ejecución dentro de la app.  
**Estado:** cribado documental; no es certificación.

## Hallazgo P1 incorporado desde el lote de 2.º medio

En `contenido/02-medio/examenes/matematica-examen-forma-b.md`, pregunta 14, la alternativa a) indica correctamente que la inversa de \(f(x)=x+10\) es \(x-10\), pero la pauta declara \(x+10\). La evidencia completa está en [Lote 2.º medio — recálculo de examen de Matemática Forma B](lote-02-medio-matematica-examen-forma-b-recalculo.md).

## Cribado de operaciones por curso

| Curso / archivo | Comprobaciones realizadas | Resultado de esta pasada |
|---|---|---|
| 3.º medio — `matematica-examen-forma-b.md` | Modelos exponenciales/logarítmicos, ángulos y cuerdas, tangente-secante, varianza, desviación estándar y probabilidades | Los cálculos de la pauta que se recalcularon coinciden; sin discrepancia numérica identificada en esta pasada. |
| 4.º medio — `matematica-examen-forma-b.md` | Interés compuesto, TEA, variación de poder adquisitivo, función potencia, trigonometría periódica, binomial y regla empírica normal | Los cálculos revisados coinciden con la pauta. No se revisó la validez curricular de cada OA ni la pertinencia de supuestos de los modelos. |
| 5.º básico — `matematica-examen-forma-b.md` | Valor posicional, multiplicación/división con resto, vuelto, fracciones, decimales, ecuaciones, área, volumen, porcentajes y lectura de datos | Las operaciones revisadas coinciden con la pauta. Esta pasada no sustituye un análisis de estímulos, edad o OA. |
| 6.º básico — `matematica-examen-forma-b.md` | Multiplicación, presupuesto dividido en buses completos, razones, porcentajes, fracciones, operaciones, ángulos, áreas/volúmenes y datos | La pregunta 2 es coherente: con $39.500.000 y buses de $4.300.000 se pueden arrendar 9 buses completos (costo $38.700.000) y sobran $800.000. La redacción pregunta por buses que el presupuesto permite arrendar, no por transportar un número dado de personas. |
| 7.º básico — `matematica-examen-forma-b.md` | Operaciones con enteros, fracciones, porcentajes, expresión de secuencia, ecuación, área de círculo y lectura de datos | Los ítems revisados coinciden con sus resultados declarados. |
| 8.º básico — `matematica-examen-forma-b.md` | Potencias, raíz cuadrada, área/perímetro equivalente, ecuaciones, pendiente, Pitágoras, traslaciones y cuartiles | Los ítems revisados coinciden con sus resultados declarados. |

## Interpretación y límites

- “Sin discrepancia identificada” se refiere solo a las operaciones efectivamente recalculadas; no significa que el examen completo esté aprobado.
- En 3.º medio, la pregunta 6 usa una secuencia observada de 80, 96, 115 y 138. Las razones son aproximadamente 1,20; por redondeo de los datos, la conclusión exponencial es una aproximación, no una igualdad exacta.
- En 4.º medio, la TEA de una tasa nominal anual del 20% capitalizada mensualmente es aproximadamente 21,94%; el monto compuesto de $900.000 al 4% durante cinco años es aproximadamente $1.094.990 según el redondeo presentado.
- En 6.º básico, el enunciado de presupuesto permite interpretar “buses completos” como cociente entero; no es un error que la respuesta sea 9, dado que no se indica una cantidad de pasajeros que deba transportarse.
- Las afirmaciones de equivalencia entre Forma A y B, originalidad de las preguntas y alineación con los OA requieren comprobaciones separadas.

## Próximos pasos

1. Añadir al validador un control de consistencia semántica para las claves de desarrollo y las explicaciones de las alternativas; el hallazgo de 2.º medio demuestra que una verificación solo de letra-opción no basta.
2. Continuar con recálculo independiente de exámenes de Ciencias, Historia, Inglés y Lengua y Literatura.
3. Reconciliar el inventario de recursos con la importación y el render de la aplicación.
4. Registrar fuentes curriculares oficiales por OA y curso.

**Conclusión:** este cribado amplía el alcance a varios niveles de Matemática, pero no permite certificar el conjunto de exámenes ni los 12 cursos.
