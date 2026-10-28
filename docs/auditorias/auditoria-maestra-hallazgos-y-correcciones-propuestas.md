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
| P1 confirmado | 5 | Errores confirmados que pueden afectar claves, puntajes o interpretación de una evaluación (H-001, H-007, H-009, H-012 y H-013) |
| P1 provisional | 1 | Hallazgo pendiente de comprobar en el renderizado de la aplicación (H-006) |
| P2 | 7 | Problemas de explicación, precisión conceptual o presentación que requieren mejora |
| Pendiente/provisional | Varios | No son errores confirmados; requieren revisar renderizado, fuentes oficiales o material completo |

Estos números corresponden solo a los hallazgos consignados aquí, no a todos los problemas que puedan existir en los 12 cursos. Conteo verificado en la rama actual: 5 P1 confirmados (H-001, H-007, H-009, H-012 y H-013), 1 P1 provisional (H-006) y 7 P2 (H-002 a H-005, H-008, H-010 y H-011): 13 hallazgos en total. Nota de continuidad: el contexto de traspaso mencionaba 12 hallazgos, pero el archivo real de esta rama ya contiene H-013, un hallazgo documental distinto sobre la escala de conversión. Se conserva para no eliminar evidencia; por ello el resumen refleja 13.

---

## Registro de ejecución — lote Historia 5.º básico (2026-10-22)

- **Árbol inspeccionado:** `contenido/05-basico/examenes/` en `qa/fase-2-matriz-trazabilidad`.
- **Archivo encontrado y leído:** `contenido/05-basico/examenes/historia-geografia-y-cs-sociales-examen-forma-b.md`.
- **Forma A:** no aparece en el árbol de esta rama; por tanto, no es posible afirmar una comparación A/B de este examen en el estado actual del repositorio. No se infiere que el archivo no exista en otras ramas o en otra fuente.
- **Comprobación de Forma B:** se cotejaron los 25 enunciados con las 25 filas de pauta, las claves visibles, los puntajes individuales, la distribución por eje/OA y el total declarado.
- **Resultado verificable:** se mantienen H-009 (encabezado 30 puntos frente a 35 en pauta/distribución), H-012 (pregunta 5 con dos consecuencias defendibles según el enunciado amplio) y H-013 (escala referencial rotulada con exigencia 60%, pero incluye 18–20 puntos en el rango que comienza en nota 4,0; 60% de 35 equivale a 21).
- **Hallazgos nuevos confirmados en este lote:** ninguno añadido. Las discrepancias encontradas ya estaban registradas como H-009, H-012 y H-013.
- **Pendiente:** localizar una Forma A en la rama o confirmar una ruta/fuente alternativa; luego comparar equivalencia de OA, estímulos, dificultad, claves y pauta. La revisión documental no verifica todavía el renderizado ni la calificación en la aplicación.

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

## H-012 — Pregunta de Historia presenta dos alternativas defendibles como consecuencia de la conquista en América

- **Estado:** confirmado
- **Prioridad:** P1
- **Curso:** 5.º básico
- **Asignatura:** Historia, Geografía y Ciencias Sociales
- **Archivo:** [historia-geografia-y-cs-sociales-examen-forma-b.md](../../contenido/05-basico/examenes/historia-geografia-y-cs-sociales-examen-forma-b.md)
- **Ubicación exacta:** pregunta 5 y fila 5 de la pauta de corrección.
- **Evidencia:** pregunta: «¿Cuál de las siguientes consecuencias de la conquista corresponde principalmente a América?». La alternativa **b)** es «La incorporación de nuevos alimentos como la papa y el tomate»; la alternativa **c)** es «La fuerte disminución de la población originaria y la pérdida de sus estructuras políticas». La pauta elige c).
- **Problema:** ambas alternativas describen consecuencias históricas relacionadas con América. La pregunta no precisa si busca un impacto demográfico/político o un intercambio alimentario, por lo que la opción b también puede defenderse como correcta en el marco literal del enunciado.
- **Por qué importa:** un estudiante puede seleccionar una consecuencia válida y aun así ser marcado incorrecto; la ambigüedad afecta la validez de la evaluación.
- **Corrección propuesta para fase 2:** acotar el enunciado al ámbito que se quiere evaluar —por ejemplo, «¿Cuál alternativa describe principalmente una consecuencia demográfica y política de la conquista para los pueblos originarios de América?»— y revisar distractores para que solo una opción responda a ese foco.
- **Validación requerida:** revisar el OA y el propósito de la pregunta; comprobar que solo una alternativa sea defendible y actualizar pauta, importación y calificación.
- **Archivo fuente modificado en fase 1:** no.

## H-011 — Pregunta de rutina diaria tiene una alternativa que no responde al momento indicado

- **Estado:** confirmado
- **Prioridad:** P2
- **Curso:** 1.º básico
- **Asignatura:** Historia, Geografía y Ciencias Sociales
- **Archivo:** [examen-integrado-forma-a.md](../../contenido/01-basico/examenes/examen-integrado-forma-a.md)
- **Ubicación exacta:** pregunta 3; pauta de corrección, fila 3.
- **Evidencia:** el enunciado pregunta «¿Qué haces primero en la mañana?»; la clave indica «a) Dormir toda la noche».
- **Problema:** dormir toda la noche ocurre antes de la mañana y no es una acción que se haga primero durante ella. La respuesta no corresponde al marco temporal literal de la pregunta.
- **Por qué importa:** para un estudiante de 1.º básico, el desajuste entre «en la mañana» y «dormir toda la noche» puede convertir una pregunta de secuencia temporal en una adivinanza sobre la intención del autor.
- **Corrección propuesta para fase 2:** cambiar el enunciado a «¿Qué haces durante la noche, antes de comenzar un nuevo día?» o sustituir la alternativa correcta por una acción matutina clara y ajustar la pauta.
- **Validación requerida:** verificar que haya una única respuesta defendible, acorde con el OA de secuencia temporal y con la edad del curso.
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



## H-013 — Escala de conversión sugerida contradice el umbral de exigencia declarado

- **Estado:** confirmado documentalmente; confirmar la escala aprobada por el producto antes de cambiarla.
- **Prioridad:** P1
- **Curso:** 5.º básico
- **Asignatura:** Historia, Geografía y Ciencias Sociales
- **Archivo:** [historia-geografia-y-cs-sociales-examen-forma-b.md](../../contenido/05-basico/examenes/historia-geografia-y-cs-sociales-examen-forma-b.md)
- **Ubicación exacta:** sección «Escala de conversión sugerida (referencial)» al final de la pauta.
- **Evidencia:** la escala se describe como «exigencia 60%», pero asigna el rango «18-23 pts» a notas 4,0–5,2. Sobre 35 puntos, el 60% equivale a 21 puntos; por tanto, valores como 18, 19 y 20 puntos quedan bajo el umbral declarado y aun así aparecen dentro del rango que empieza en nota 4,0.
- **Problema:** el rango de aprobación no es coherente con la exigencia del 60% que declara la propia escala.
- **Por qué importa:** si la aplicación usa esta tabla, podría aprobar estudiantes que no alcanzan el umbral indicado o producir notas inconsistentes.
- **Corrección propuesta para fase 2:** confirmar la política de evaluación aprobada; después recalcular todos los intervalos para 35 puntos de modo que la nota 4,0 corresponda exactamente al umbral establecido y no haya huecos ni solapamientos. No asumir una conversión oficial de Mineduc a partir de esta tabla referencial.
- **Validación requerida:** prueba de límites (20/21/22 puntos), cobertura de 0 a 35 puntos, monotonicidad de notas y coincidencia entre tabla documental y función de conversión de la aplicación.
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


---

## Reconciliación de correcciones registradas — 2026-10-22

Las siguientes entradas dan un ID estable a cambios de la bitácora que aún no estaban vinculados a un encabezado H-###. Son **correcciones aplicadas pendientes de revalidación**, no hallazgos cerrados. La evidencia de implementación estaba en el registro de implementación (retirado en la consolidación documental; ver [ARCHIVOS-ELIMINADOS.md](ARCHIVOS-ELIMINADOS.md)); los commits del historial de Git son el rastro del cambio, no una prueba de regresión.

## H-014 — Tabla de frecuencias de Matemática 7.º básico corregida

- **Estado:** corregido pendiente de revalidación.
- **Prioridad:** P1 provisional hasta validar los datos y la tabla; la bitácora reporta la corrección aritmética.
- **Archivo:** `contenido/07-basico/matematica.md`.
- **Evidencia de la corrección registrada:** para 20 datos, la tabla quedó como 0 → 4 (20 %), 1 → 9 (45 %), 2 → 5 (25 %), 3 → 2 (10 %).
- **Validación requerida:** recalcular las frecuencias desde la lista original de datos; verificar suma de frecuencias = 20 y suma de porcentajes = 100 %; revisar explicación y render.
- **Commit de implementación:** `5034c79130eecbb950ecc070bf2e352db2255e8a`.

## H-015 — Cita de Lengua y Literatura 2.º medio restaurada

- **Estado:** corregido pendiente de revalidación.
- **Prioridad:** P3, errata textual/contextual salvo que la cita cambie la interpretación o la clave.
- **Archivo:** `contenido/02-medio/examenes/lengua-y-literatura-examen-forma-b.md`, pregunta 17.
- **Evidencia de la corrección registrada:** se restauró la cita «ya no hay vuelta atrás».
- **Validación requerida:** cotejar la cita con el texto fuente del instrumento, revisar que no altere la interpretación de la pregunta y confirmar pauta/alternativas.
- **Commit de implementación:** `9dea1fc2992c94b98612ad1e3ade9a3ae6f039e7`.

## H-016 — Diálogo de Inglés 5.º básico corregido

- **Estado:** corregido pendiente de revalidación.
- **Prioridad:** P2, coherencia pragmática y lingüística.
- **Archivo:** `contenido/05-basico/examenes/ingles-examen-forma-b.md`.
- **Evidencia de la corrección registrada:** se reordenó el diálogo para que quien rompe el lápiz se disculpe y la otra persona responda «That's OK, don't worry».
- **Validación requerida:** revisar la secuencia completa, los turnos, la naturalidad del inglés y que la clave siga correspondiendo al diálogo corregido.
- **ID operativo previo:** `LGS-5B-ING-001`.
- **Commit de implementación:** `e2f31eb49221cf718da346564d73fe5801c1a022`.

## H-017 — Explicación del efecto Doppler en Ciencias 1.º medio precisada

- **Estado:** corregido pendiente de revalidación.
- **Prioridad:** P2, precisión conceptual.
- **Archivo:** `contenido/01-medio/ciencias-naturales.md`.
- **Evidencia de la corrección registrada:** se separó el efecto Doppler del sonido (más agudo al acercarse y más grave al alejarse) del corrimiento de la luz (azul al acercarse y rojo al alejarse).
- **Validación requerida:** revisión disciplinar independiente, comprobar que el contexto del material no introduzca condiciones adicionales omitidas y revisar la explicación completa.
- **ID operativo previo:** `LGS-1M-CNT-011`.
- **Commit de implementación:** `50ac8feeec312f5533086d9e622a92e4255dd7b9`.

## H-018 — Errata en Historia 8.º básico corregida

- **Estado:** corregido pendiente de revalidación.
- **Prioridad:** P3, errata editorial.
- **Archivo:** `contenido/08-basico/historia-geografia-y-cs-sociales.md`.
- **Evidencia de la corrección registrada:** se cambió «population» por «población».
- **Validación requerida:** revisar contexto de la oración y hacer una búsqueda de erratas cercanas; el cambio aislado no equivale a una revisión integral del archivo.
- **Commit de implementación:** `4c64599d8227167741aa8cc1f67309715e288518`.

## H-019 — Errata en Lengua y Literatura 1.º medio corregida

- **Estado:** corregido pendiente de revalidación.
- **Prioridad:** P3, errata editorial.
- **Archivo:** `contenido/01-medio/lengua-y-literatura.md`.
- **Evidencia de la corrección registrada:** se cambió «information implícita» por «información implícita».
- **Validación requerida:** revisar contexto y buscar erratas similares; no implica revisión integral del material.
- **Commit de implementación:** `b1c48933cedecc8c1044a01ffc1b48eeb2e3af7f`.

## H-020 — Referencia temporal en Lengua y Literatura 8.º básico ajustada

- **Estado:** corregido pendiente de revalidación.
- **Prioridad:** P2 provisional, porque el cambio modifica contexto factual/histórico y retroalimentación.
- **Archivo:** `contenido/08-basico/lengua-y-literatura.md`.
- **Evidencia de la corrección registrada:** se cambió «madrugada» por «tarde» y se actualizó la retroalimentación sobre el terremoto de Valdivia del 22-05-1960.
- **Validación requerida:** contrastar el momento del sismo con fuente histórica fiable, releer el ítem completo y confirmar que la clave/retroalimentación siga siendo coherente.
- **ID operativo previo:** `LGS-8B-LEM-001`.
- **Commit de implementación:** `4bdf9c38fe97d9ff2abdd36fe40157b94fea101d`.

## H-021 — Nota editorial sobre razón en Matemática 6.º básico retirada

- **Estado:** corregido pendiente de revalidación.
- **Prioridad:** P3, claridad editorial.
- **Archivo:** `contenido/06-basico/matematica.md`.
- **Evidencia de la corrección registrada:** se retiró la nota «cuidado con el orden» y se mantuvo la explicación de amplificación de razón 5:3 a 15:9.
- **Validación requerida:** confirmar que el ejemplo y la explicación enseñen correctamente la equivalencia de razones, y que no se haya eliminado una advertencia necesaria para el estudiante.
- **ID operativo previo:** `MAT-CONT-002`.
- **Commit de implementación:** `739892d18df593fdf1bbf0232a0066cb34951923`.

**Nota de conteo:** estas entradas amplían el registro para que los cambios de la bitácora tengan IDs estables. No sumar cada alias operativo como un hallazgo independiente: conservar un único H-### canónico por problema y enlazar `LGS-*`/`MAT-*` como alias. H-001, H-003, H-007 y H-009 ya existían y siguen siendo los IDs canónicos para los tres problemas principales y la explicación del resto; esta adición no los duplica.
