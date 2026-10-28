# Protocolo de auditoría integral de calidad educativa — Logos School

**Versión:** 1.0  
**Fecha:** 21 de octubre de 2026  
**Rama de trabajo:** qa/fase-2-matriz-trazabilidad  
**Estado:** protocolo de trabajo; no constituye certificación de los materiales.

## 1. Objetivo y criterio de finalización

Auditar el 100 % de los materiales educativos publicados y utilizados por Logos School en los 12 niveles incluidos en el alcance: 1.º a 8.º básico y 1.º a 4.º medio. El universo se determinará desde el repositorio vigente y se contrastará con el contenido realmente importado y mostrado por la aplicación.

La auditoría solo podrá declararse completa cuando:
1. El inventario tenga una ruta y una clasificación para cada archivo y recurso educativo dentro del alcance.
2. Cada guía, lectura, explicación, ejercicio, pregunta, alternativa, clave, rúbrica y puntaje haya sido revisado o tenga una exclusión justificada y aprobada.
3. Cada evaluación tenga conciliación de puntajes y claves, y se haya comprobado su representación en la aplicación cuando corresponda.
4. La alineación curricular se haya contrastado con fuentes oficiales identificadas por curso, asignatura y objetivo.
5. Todos los hallazgos estén cerrados con evidencia o estén explícitamente aceptados como riesgo; ningún P1 puede quedar abierto para una certificación de publicación.
6. Los controles automáticos y las pruebas de regresión se hayan ejecutado en un entorno identificado, con resultados reproducibles.
7. Una revisión final independiente confirme el muestreo, las excepciones y las evidencias.

## 2. Alcance obligatorio

Incluir, si existen en el producto:
- Material de estudio, teoría, lecturas y resúmenes.
- Guías, actividades, ejercicios resueltos y ejercicios propuestos.
- Preguntas de selección múltiple, verdadero/falso, respuesta breve y desarrollo.
- Claves de respuestas, explicaciones, retroalimentación y rúbricas.
- Pruebas por unidad, tests, ensayos, simulacros y exámenes integrados.
- Formas A/B y bancos de preguntas.
- Imágenes, gráficos, tablas, mapas, diagramas, audios, videos y otros recursos referenciados.
- Metadatos de curso, asignatura, unidad, OA, dificultad, puntaje e identificadores.
- Proceso de importación, persistencia, presentación y corrección automática en la aplicación.

No asumir que un archivo Markdown representa todo lo que ve el estudiante: cotejar archivos fuente, recursos vinculados, datos importados y render cuando aplique.

## 3. Dimensiones de revisión

| Dimensión | Verificaciones mínimas |
|---|---|
| Exactitud disciplinar | Conceptos, hechos, definiciones, fórmulas, procedimientos, unidades y cálculos. |
| Respuesta y pauta | La clave existe, corresponde a una alternativa real y es correcta; las preguntas abiertas tienen criterios suficientes. |
| Puntajes | Suma de puntos por pregunta, puntajes parciales, rúbricas y total declarado. |
| Pedagogía y nivel | Lenguaje adecuado al curso, progresión, instrucciones claras, ejemplos y carga cognitiva razonable. |
| Currículum | OA declarado y evidencia concreta de cobertura; usar fuente oficial y registrar versión/URL/fecha de consulta. |
| Equidad y contexto | Evitar generalizaciones culturales, sesgos, estereotipos o afirmaciones históricas/científicas sin contexto. |
| Recursos | Todo recurso mencionado existe, se carga, es legible, corresponde al enunciado y contiene información suficiente. |
| Formas paralelas | Comparar enunciados, datos, estímulos, opciones, dificultad, OA y puntajes entre formas. |
| Integridad técnica | IDs estables, ausencia de duplicación accidental, importación íntegra y conservación de la relación pregunta-pauta. |
| Experiencia en aplicación | Enunciado y recursos se renderizan bien; alternativas seleccionables; corrección, feedback y puntaje coherentes. |

## 4. Flujo de trabajo por archivo

1. **Inventariar:** registrar ruta, curso, asignatura, tipo, forma, unidad, OA declarado, recursos dependientes y número de ítems.
2. **Leer completo:** no certificar a partir de muestras ni de resúmenes previos.
3. **Revisar contenido:** verificar conceptos, hechos, lenguaje y nivel educativo.
4. **Resolver independientemente:** resolver cada ejercicio matemático/científico y comprobar la respuesta; verificar claves de otras disciplinas contra el material y fuentes apropiadas.
5. **Revisar evaluación:** cotejar cada clave, alternativa, rúbrica, puntaje parcial y total.
6. **Comprobar recursos:** verificar archivos vinculados y render.
7. **Cotejar currículum:** registrar fuente oficial y evidencia por OA, sin inferir cobertura por una lista general.
8. **Registrar hallazgos:** citar archivo, sección/pregunta, evidencia, impacto, prioridad y acción propuesta.
9. **Verificar corrección:** tras una corrección autorizada, ejecutar regresión y volver a revisar el contexto afectado.
10. **Cerrar:** adjuntar evidencia de verificación y actualizar la matriz maestra.

## 5. Severidad

- **P0 — Bloqueante:** riesgo de seguridad, privacidad o integridad que impide publicar o usar el material.
- **P1 — Crítica:** clave incorrecta, respuesta ambigua sin criterio válido, cálculo/puntaje erróneo, recurso esencial ausente o error conceptual grave.
- **P2 — Mayor:** imprecisión disciplinar/curricular, instrucción confusa o problema pedagógico que puede conducir a aprendizaje incorrecto.
- **P3 — Menor:** redacción, consistencia editorial o mejora que no cambia sustancialmente la respuesta.
- **P4 — Observación:** mejora opcional o decisión de diseño que requiere deliberación.

## 6. Estados controlados

Cada ítem del inventario y cada hallazgo usará uno de estos estados:
- no_iniciado
- en_revision
- hallazgo_registrado
- requiere_render
- requiere_fuente_oficial
- requiere_revision_especialista
- correccion_propuesta
- corregido_pendiente_regresion
- cerrado_verificado
- no_aplica_justificado

Solo cerrado_verificado y no_aplica_justificado cuentan como resueltos para el cálculo de cierre, y las excepciones no_aplica deben incluir justificación. La existencia de un reporte o de un script no cambia automáticamente el estado de revisión de los archivos.

## 7. Evidencia mínima por hallazgo

- Identificador único.
- Curso, asignatura, ruta y versión/commit.
- Pregunta, sección o recurso afectado.
- Cita breve o referencia precisa al contenido.
- Resultado esperado y resultado observado.
- Resolución independiente o fuente de contraste.
- Severidad y justificación.
- Corrección propuesta, sin modificar contenido fuente durante la fase de diagnóstico.
- Prueba de regresión y evidencia de ejecución cuando se cierre.
- Estado, responsable y fecha de revisión.

## 8. Automatización: alcance y límites

Los scripts pueden detectar discrepancias estructurales, formatos inválidos, claves que no coinciden textualmente, totales declarados incompatibles, referencias a recursos sospechosas, duplicados y cambios de IDs. Deben tener pruebas positivas y negativas para reducir falsos positivos.

Los scripts por sí solos no certifican exactitud factual, adecuación pedagógica, alineación curricular, suficiencia de un gráfico ni validez de una rúbrica. Estas dimensiones requieren lectura humana, resolución independiente y fuentes verificables.

El validador Markdown inicial solo cubre un subconjunto de consistencia de claves y declaraciones explícitas de puntaje; debe considerarse experimental hasta ejecutar sus pruebas y compararlo con casos reales.

## 9. Tablero de cobertura y regla del 100 %

Mantener métricas separadas:
- Archivos inventariados / archivos identificados en el alcance.
- Archivos revisados completamente / archivos inventariados.
- Ítems revisados / ítems identificados.
- Evaluaciones con puntaje conciliado / evaluaciones que asignan puntaje.
- Preguntas de alternativa con clave verificada / preguntas de alternativa.
- Preguntas abiertas con rúbrica revisada / preguntas abiertas.
- Recursos verificados / recursos referenciados.
- OA con evidencia curricular / OA declarados.
- Hallazgos abiertos por severidad.
- Pruebas ejecutadas, aprobadas, fallidas y no ejecutadas.

No usar un único porcentaje para ocultar dimensiones pendientes. El 100 % requiere denominadores generados desde el estado vigente del repositorio y excepciones documentadas. Si un denominador no puede calcularse, reportar la métrica como desconocida, no como 100 %.

## 10. Límites operativos y protección de datos

Durante la fase de diagnóstico, trabajar en la rama QA, sin cambios en main, sin alterar contenido educativo ni ejecutar cambios sobre bases de datos. Antes de corregir contenido, preparar propuestas específicas y mantener historial de cambios. Las pruebas con base de datos deben utilizar un entorno QA identificado, nunca producción.

## 11. Primeras tareas de ejecución

1. Regenerar el inventario completo desde el commit actual: guías, evaluaciones, bancos, recursos y datos usados por la aplicación.
2. Confirmar el universo de archivos y los huecos entre repositorio, importador y aplicación.
3. Ejecutar y corregir las pruebas del validador inicial; documentar limitaciones y falsos positivos.
4. Reproducir los hallazgos P1 ya registrados y asociarlos con evidencia vigente.
5. Auditar evaluaciones restantes por curso y asignatura, pregunta por pregunta.
6. Completar guías y materiales de estudio con revisión disciplinar y curricular.
7. Incorporar render y pruebas de regresión, después de acordar un entorno seguro.
8. Emitir informe final solo cuando las métricas y los criterios de salida estén respaldados por evidencia.

---
**Declaración de estado:** este documento define el protocolo y el criterio de cierre. No afirma que el trabajo de auditoría esté completado.
