# Auditoría maestra de contenido — Hallazgos y correcciones propuestas

- **Proyecto:** Logos School
- **Rama de trabajo:** `qa/fase-2-matriz-trazabilidad`
- **Fecha de inicio:** 2026-10-22
- **Propósito:** concentrar en un solo registro los defectos concretos detectados, su evidencia, impacto y propuesta de corrección para ejecutar las modificaciones en una fase posterior.
- **Regla de esta fase:** diagnóstico y propuesta. No se modifican archivos educativos originales.
- **Estados:** `confirmado` = evidencia directa en el archivo; `provisional` = depende de renderizado, fuente oficial o revisión adicional; `pendiente` = aún no inspeccionado en profundidad.

## Cómo leer y mantener este documento

Cada hallazgo debe identificar curso, asignatura, archivo, pregunta/sección, problema observado, por qué importa, corrección propuesta y validación necesaria. No se marcará un curso como auditado solo porque sus archivos estén inventariados o porque pase CI. Los hallazgos se agregan sin borrar el historial; al pasar a corrección se registra el cambio y la evidencia de regresión.

## Resumen ejecutivo

| Prioridad | Cantidad registrada en esta versión | Interpretación |
|---|---:|---|
| P1 | 4 | Errores confirmados que pueden afectar claves, puntajes o interpretación de una evaluación |
| P2 | 3 | Problemas de explicación, precisión conceptual o presentación que requieren mejora |
| Pendiente/provisional | Varios | No son errores confirmados; requieren revisar renderizado, fuentes oficiales o material completo |

Estos números corresponden solo a los hallazgos consignados aquí, no a todos los problemas que puedan existir en los 12 cursos.

---

## H-001 — Clave de respuesta inconsistente con la alternativa correcta

- **Estado:** confirmado
- **Prioridad:** P1
- **Curso:** 4.º básico
- **Asignatura:** Matemática
- **Archivo:** [examen-integrado-forma-b.md](../../contenido/04-basico/examenes/examen-integrado-forma-b.md)
- **Ubicación exacta:** pregunta 16 y fila 16 de la pauta de corrección.
- **Evidencia:** el enunciado es (x + 9 = 23). Las opciones son a) 32, b) 14, c) 13, d) 15. La pauta indica «c) 14» y explica (23 - 9 = 14).
- **Problema:** el valor calculado es correcto, pero la letra de alternativa es incorrecta. La alternativa b) contiene 14; la c) contiene 13.
- **Por qué importa:** una corrección basada en la letra puede marcar como incorrecta una respuesta matemáticamente correcta.
- **Corrección propuesta para fase 2:** cambiar la clave a **b) 14**, manteniendo la explicación si se confirma que el formato de la pauta admite esa notación.
- **Validación requerida:** prueba automatizada de consistencia entre letra, texto de alternativa y resultado; comprobar importación, respuesta guardada y puntuación en la aplicación.
- **Archivo fuente modificado en fase 1:** no.

## H-002 — Reutilización de estímulo entre las formas A y B

- **Estado:** confirmado
- **Prioridad:** P2 (subir a P1 solo si la política de evaluación exige formas completamente independientes)
- **Curso:** 3.º básico
- **Asignatura:** Lenguaje y Comunicación
- **Archivos:** [Forma A](../../contenido/03-basico/examenes/examen-integrado-forma-a.md) y [Forma B](../../contenido/03-basico/examenes/examen-integrado-forma-b.md)
- **Ubicación exacta:** Forma A, preguntas 4–5; Forma B, pregunta 4.
- **Evidencia:** ambas formas reutilizan el texto narrativo «El cometa de Joaquín». En la Forma A se usa para identificar la ciudad y describir a Antonia; en la Forma B se usa para un ítem de verdadero/falso sobre el cometa enredado en un espino.
- **Problema:** las preguntas son distintas, pero el estímulo no; esto contradice la promesa de la Forma B de practicar sin repetir contenido.
- **Por qué importa:** quien ya hizo la Forma A puede recordar el relato y tener una ventaja en la Forma B; las formas no son completamente independientes.
- **Corrección propuesta para fase 2:** crear un texto alternativo de dificultad y extensión comparables para Forma B, con preguntas y pauta propias; alternativa menos fuerte: ajustar las instrucciones para declarar que puede haber estímulos compartidos.
- **Validación requerida:** comparar estímulos, habilidades evaluadas, longitud, dificultad y claves A/B después del reemplazo.
- **Archivo fuente modificado en fase 1:** no.

## H-003 — Falta de explicación del resto en una división contextualizada

- **Estado:** confirmado en revisión previa
- **Prioridad:** P2
- **Curso:** 6.º básico
- **Asignatura:** Matemática
- **Archivo:** [matematica.md](../../contenido/06-basico/matematica.md)
- **Ubicación exacta:** pregunta 4 de la guía (confirmar encabezado/identificador exacto al preparar la corrección).
- **Evidencia:** el problema plantea 24.600 botellas, 12 por caja y reparto entre 3; el cálculo da 2.050 cajas y, al repartirlas, 683 para cada grupo con 1 caja restante.
- **Problema:** la retroalimentación señala aproximadamente 683 para cada grupo, pero no explica qué ocurre con la caja restante ni cómo interpretar el residuo en el contexto.
- **Por qué importa:** el estudiante puede no distinguir entre cociente y resto, o pensar que se puede repartir una fracción de caja cuando la unidad es una caja completa.
- **Corrección propuesta para fase 2:** explicar (2.050 ÷ 3 = 683) y resto 1; contextualizar qué representa la caja sobrante y preguntar si se puede dividir el contenido de esa caja, según lo que solicite el problema.
- **Validación requerida:** recalcular con el enunciado literal completo y comprobar que la interpretación coincide con la pregunta solicitada.
- **Archivo fuente modificado en fase 1:** no.

## H-004 — Términos científicos presentados como equivalentes

- **Estado:** confirmado en revisión previa; requiere cotejo del enunciado completo al corregir
- **Prioridad:** P2
- **Curso:** 1.º medio
- **Asignatura:** Ciencias Naturales
- **Archivo:** [ciencias-naturales-examen-forma-b.md](../../contenido/01-medio/examenes/ciencias-naturales-examen-forma-b.md)
- **Ubicación exacta:** pregunta 9, pauta y explicación.
- **Evidencia:** la pauta emplea «bioacumulación (o biomagnificación)» como si fueran intercambiables, mientras la explicación describe el aumento de concentración entre niveles tróficos.
- **Problema:** bioacumulación y biomagnificación son procesos relacionados, pero no sinónimos exactos.
- **Por qué importa:** el estudiante podría aprender una distinción científica incorrecta y recibir una explicación imprecisa.
- **Corrección propuesta para fase 2:** ajustar enunciado y pauta al concepto que realmente se evalúa; usar «biomagnificación» si el foco es el aumento a lo largo de niveles tróficos, y reservar «bioacumulación» para la acumulación en un organismo a través del tiempo.
- **Validación requerida:** cotejo con fuente científica/curricular confiable y revisión del contexto completo de la pregunta.
- **Archivo fuente modificado en fase 1:** no.

## H-005 — Definición incompleta del soluto en una explicación

- **Estado:** confirmado en revisión previa
- **Prioridad:** P2
- **Curso:** 2.º medio
- **Asignatura:** Ciencias Naturales
- **Archivo:** [ciencias-naturales-examen-forma-b.md](../../contenido/02-medio/examenes/ciencias-naturales-examen-forma-b.md)
- **Ubicación exacta:** pregunta 20, pauta/explicación.
- **Evidencia:** la clave identifica correctamente el azúcar como soluto en una solución de azúcar y agua, pero la explicación enfatiza demasiado que está en menor cantidad.
- **Problema:** la cantidad relativa puede ser habitual, pero no es por sí sola la definición de soluto.
- **Por qué importa:** puede consolidar una regla conceptual simplificada que falla en otros ejemplos.
- **Corrección propuesta para fase 2:** definir el soluto como la sustancia que se disuelve en el solvente; explicar el ejemplo azúcar/agua sin presentar «menor cantidad» como criterio universal.
- **Validación requerida:** revisar coherencia con el currículo del nivel y con los otros ejemplos de soluciones del material.
- **Archivo fuente modificado en fase 1:** no.

## H-007 — Clave de función inversa contradice la transformación algebraica

- **Estado:** confirmado en revisión previa; verificar la línea exacta antes de modificar
- **Prioridad:** P1
- **Curso:** 2.º medio
- **Asignatura:** Matemática
- **Archivo:** [matematica-examen-forma-b.md](../../contenido/02-medio/examenes/matematica-examen-forma-b.md)
- **Ubicación exacta:** pregunta 14 y pauta de corrección.
- **Evidencia:** el ítem pide la función inversa de (f(x)=x+10). La inversa se obtiene despejando (x): (y=x+10) implica (x=y-10), por tanto (f^{-1}(x)=x-10). La pauta consignada previamente indicaba (x+10).
- **Problema:** la clave propone la función original en lugar de la inversa.
- **Por qué importa:** puede calificar mal una respuesta correcta y enseñar una regla algebraica equivocada.
- **Corrección propuesta para fase 2:** cambiar la clave/explicación a (f^{-1}(x)=x-10), verificando que las alternativas contengan esa respuesta y que la letra coincida.
- **Validación requerida:** prueba algebraica independiente, revisión de opciones y prueba de regresión de importación/calificación.
- **Archivo fuente modificado en fase 1:** no.

## H-010 — La Forma B de 2.º básico reutiliza un texto de la Forma A pese a prometer preguntas distintas

- **Estado:** confirmado
- **Prioridad:** P2 (subir a P1 si el criterio de producto exige formas completamente independientes)
- **Curso:** 2.º básico
- **Asignatura:** Lenguaje y Comunicación
- **Archivos:** [Forma A](../../contenido/02-basico/examenes/examen-integrado-forma-a.md) y [Forma B](../../contenido/02-basico/examenes/examen-integrado-forma-b.md)
- **Ubicación exacta:** Forma A, pregunta 6; Forma B, pregunta 8.
- **Evidencia:** ambas formas incluyen el mismo texto «La fiesta sorpresa de Emilia», con la misma descripción de Emilia, sus amigos Benjamín y Constanza, la preparación de la fiesta, el queque de manzana y la reacción de Emilia. La Forma B declara que utiliza un banco de preguntas distinto y que permite practicar dos veces con contenido diferente.
- **Problema:** el estímulo de lectura se repite literalmente aunque las preguntas vinculadas no sean idénticas.
- **Por qué importa:** quien ya practicó la Forma A puede recordar el texto y responder la Forma B sin realizar una lectura nueva; esto reduce la independencia de las formas y contradice parcialmente la promesa de contenido diferente.
- **Corrección propuesta para fase 2:** reemplazar el texto de una de las formas por un estímulo nuevo de dificultad y extensión comparables, revisar sus preguntas y pauta, o ajustar la promesa si la reutilización deliberada está permitida.
- **Validación requerida:** comparar estímulos y preguntas de A/B semánticamente, no solo por igualdad de enunciados; comprobar clave, pauta, dificultad aproximada y renderizado del texto sustituto.
- **Archivo fuente modificado en fase 1:** no.

## H-008 — Enunciado de estado de la materia contiene la expresión «información líquida»

- **Estado:** confirmado
- **Prioridad:** P2
- **Curso:** 4.º básico
- **Asignatura:** Ciencias Naturales
- **Archivo:** [examen-integrado-forma-a.md](../../contenido/04-basico/examenes/examen-integrado-forma-a.md)
- **Ubicación exacta:** pregunta 15.
- **Evidencia:** el enunciado pregunta «¿Cuál de las siguientes es información líquida entre los siguientes materiales...?», mientras la pauta identifica el jugo de frutilla como respuesta.
- **Problema:** «información líquida» no corresponde al concepto evaluado y hace que el enunciado sea semánticamente incoherente.
- **Por qué importa:** el estudiante puede confundirse por un error de redacción en lugar de demostrar si reconoce un material en estado líquido.
- **Corrección propuesta para fase 2:** confirmar la intención y sustituir la expresión por una formulación directa, por ejemplo: «¿Cuál de los siguientes materiales se encuentra en estado líquido?». Conservar la clave solo tras volver a cotejar todas las opciones.
- **Validación requerida:** revisar el enunciado completo, las alternativas y la renderización en la aplicación.
- **Archivo fuente modificado en fase 1:** no.

## H-009 — Puntaje total declarado no coincide con la pauta del examen

- **Estado:** confirmado
- **Prioridad:** P1
- **Curso:** 5.º básico
- **Asignatura:** Historia, Geografía y Ciencias Sociales
- **Archivo:** [historia-geografia-y-cs-sociales-examen-forma-b.md](../../contenido/05-basico/examenes/historia-geografia-y-cs-sociales-examen-forma-b.md)
- **Ubicación exacta:** encabezado del examen y cierre de la pauta de corrección.
- **Evidencia:** el encabezado declara **30 puntos**; la suma de los 25 ítems, la tabla de pauta y la distribución por eje totalizan **35 puntos**.
- **Problema:** hay una diferencia de 5 puntos entre el total anunciado y la puntuación efectiva.
- **Por qué importa:** la aplicación podría calcular porcentajes, resultados o notas sobre un denominador incorrecto.
- **Corrección propuesta para fase 2:** si se confirma que los puntajes individuales y la distribución por eje son los aprobados, actualizar el encabezado a **35 puntos**; verificar además cualquier regla de conversión a nota.
- **Validación requerida:** automatizar la suma de puntos de ítems, pauta, encabezado y distribución por eje; probar importación y calificación en QA.
- **Archivo fuente modificado en fase 1:** no.

## H-006 — Estímulo visual descrito en Markdown, renderizado aún no comprobado

- **Estado:** provisional
- **Prioridad:** P1 provisional, sujeto a inspección de la aplicación
- **Curso:** 1.º básico
- **Asignatura:** Matemática
- **Archivo:** [matematica-unidad-medicion-datos-probabilidades.md](../../contenido/01-basico/pruebas/matematica-unidad-medicion-datos-probabilidades.md)
- **Ubicación exacta:** pregunta 2.
- **Evidencia:** el enunciado pide ordenar una goma, un lápiz y una regla, pero el Markdown inspeccionado no aporta dimensiones ni una imagen incrustada.
- **Problema posible:** si el renderizador no agrega un recurso visual, no hay información suficiente para determinar el orden esperado.
- **Por qué importa:** el estudiante podría responder sin datos observables, haciendo que el ítem sea ambiguo o imposible.
- **Corrección propuesta para fase 2:** primero comprobar el ítem en la aplicación. Si no existe imagen/medida accesible, añadir una ilustración inequívoca con longitudes claramente diferenciadas o reformular el enunciado para proporcionar los datos.
- **Validación requerida:** captura/render real de la pregunta y revisión en móvil/escritorio. No clasificar como error definitivo antes de esa comprobación.
- **Archivo fuente modificado en fase 1:** no.

---

## Hallazgos que no deben confundirse con errores confirmados

1. El inventario identificó 290 archivos entre `contenido/` y `Temarios/` (278 Markdown y 12 PDF en el corte registrado). Esto es un universo de revisión, no 290 archivos auditados.
2. En muestras de pruebas integradas de 3.º y 4.º básico, el conteo de preguntas y filas de pauta fue consistente en las cuatro formas. El conteo no valida el contenido de todas las claves.
3. En una revisión inicial, las preguntas de Matemática de 1.º medio Forma B se recalcularon y no se detectaron discrepancias numéricas en esa pasada; la validación curricular, la equivalencia A/B y la aplicación siguen pendientes.
4. En 2.º medio Matemática Forma B, pregunta 14, la clave de la inversa de (f(x)=x+10) contradice el resultado: la inversa es (x-10), mientras la pauta indicaba (x+10). **Hallazgo P1 registrado previamente; incorporar como H-007 y revisar el archivo exacto antes de corregir.**

## Plantilla para todos los siguientes hallazgos

Copiar esta estructura por cada problema nuevo:

- **ID:**
- **Estado:** confirmado / provisional / pendiente de fuente / requiere render / requiere especialista
- **Prioridad:** P0 / P1 / P2 / P3 / P4
- **Curso y asignatura:**
- **Archivo y ubicación exacta:**
- **Evidencia literal o cálculo reproducible:**
- **Problema identificado:**
- **Por qué es un problema:**
- **Corrección propuesta (sin aplicar):**
- **Prueba o fuente necesaria para validar:**
- **Regresión que debe añadirse:**
- **Estado de corrección:** no iniciada (fase 2)

## Plan de auditoría a continuación

1. Terminar la inspección completa de los exámenes y guías por lote, registrando cada hallazgo aquí con ubicación y propuesta concreta.
2. Revisar las 12 áreas de curso, no solo los ejemplos conocidos; cotejar claves, opciones, cálculos, puntajes, rúbricas, OA oficiales, fuentes y estímulos visuales.
3. Ampliar el inventario al contenido realmente consumido por la aplicación: bancos de preguntas, importadores, mapeo de alternativas, puntaje, persistencia y renderizado.
4. Preparar una lista de correcciones priorizada por riesgo y dependencias.
5. No comenzar la corrección masiva hasta que el diagnóstico esté suficientemente completo y se haya acordado el corte de fase 2.

**Importante:** este archivo es el registro maestro de hallazgos conocidos, no la certificación de que el resto del contenido está correcto. Todo elemento no revisado en profundidad permanece pendiente.
