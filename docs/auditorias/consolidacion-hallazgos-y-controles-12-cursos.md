# Consolidación de hallazgos preliminares — auditoría de 12 cursos

**Fecha de corte:** 21 de octubre de 2026  
**Repositorio:** rodrigogalvezpinto/logos-school  
**Rama:** qa/fase-2-matriz-trazabilidad  
**Estado:** consolidación parcial de reportes existentes; no es certificación integral.  
**Regla de alcance:** diagnóstico documental solamente. No se modifican guías, preguntas, aplicación ni base de datos.

## 1. Cómo interpretar este informe

Los hallazgos aquí listados se recogieron en revisiones parciales de archivos y muestras. La ausencia de un hallazgo para un curso o asignatura **no** significa que esté aprobada. Los niveles de prioridad son preliminares y deben confirmarse al reproducir el caso en la fuente y, cuando corresponda, en la aplicación.

- **P1:** posible error que afecta respuesta correcta, puntaje o validez de una evaluación.
- **P2:** posible imprecisión conceptual, factual, curricular o de diseño que puede inducir a error.
- **P3:** claridad, contextualización, trazabilidad o mejora pedagógica.
- **Pendiente de reproducir:** no debe tratarse como defecto confirmado hasta verificar la ruta y el contexto exactos.

## 2. Hallazgos de mayor prioridad para reproducir primero

| ID provisional | Curso / archivo | Prioridad | Hallazgo observado | Próxima verificación |
|---|---|---:|---|---|
| LGS-4B-EVAL-001 | 4.º básico, examen integrado Forma B | P1 | En pregunta con x + 9 = 23, el valor 14 aparece como alternativa b), pero la clave reportada indica c) 14. | Abrir archivo vigente, comprobar opciones y clave; agregar prueba de regresión de clave-opción. |
| LGS-5B-EVAL-001 | 5.º básico, Historia Forma B | P1 | Encabezado declara 30 puntos, pero la distribución reportada suma 35. | Recalcular puntaje desde todas las preguntas y criterios de corrección. |
| LGS-1B-MAT-001 | 1.º básico, prueba de medición/datos | P1 | Una pregunta pide ordenar objetos por longitud sin medidas ni imagen que permita comparar. | Confirmar enunciado completo y render de la prueba; determinar si falta un recurso visual. |
| LGS-6B-MAT-001 | 6.º básico, guía de Matemática | P1 | 24.600 botellas en cajas de 12 dan 2.050 cajas; repartidas entre 3 distribuidores son 683 por distribuidor y sobra 1 caja. La retroalimentación reportada no explica el resto. | Confirmar si el contexto exige reparto entero, sobrante o distribución no uniforme; ajustar solo en fase de corrección autorizada. |
| LGS-4B-EVAL-002 | 4.º básico, Ciencias Forma A | P2 | Aparece la expresión «información líquida» donde el sentido esperado parece ser materia/material en estado líquido. | Confirmar literalidad, contexto y posible efecto en la respuesta. |
| LGS-5B-EVAL-002 | 5.º básico, Historia | P2 | La disminución de población indígena se atribuye principalmente a enfermedades introducidas por europeos sin suficiente contextualización multifactorial. | Revisar explicación, periodo y región; comprobar que no reduzca un proceso histórico complejo a una sola causa. |

**Nota:** los IDs son identificadores de seguimiento usados en reportes parciales; no representan tickets creados en GitHub salvo que se indique expresamente.

## 3. Resumen de cobertura documental por curso

| Curso | Reportes parciales localizados | Hallazgos/áreas principales que requieren seguimiento | Estado real |
|---|---|---|---|
| 1.º básico | Hallazgos preliminares, segunda pasada y revisión ampliada | Números 11–19; fonema/grafema; pregunta de longitud sin medidas; clave de rutina diaria; instrucciones y contextualización | Parcial; no certificado |
| 2.º básico | Tres pasadas, incluyendo evaluación | Forma A/B con ítems repetidos; claves de Historia/Ciencias; pupas/capullos; generalizaciones culturales; gráfico posiblemente externo | Parcial; no certificado |
| 3.º básico | Guías principales y evaluación | Reutilización de textos/ilustraciones entre formas A/B; convención de seis/siete continentes; criterios de inferencias abiertas | Parcial; no certificado |
| 4.º básico | Guías principales y evaluación | Posible desajuste clave-opción en Matemática; terminología científica; comparabilidad de formas; mapa geográfico insuficientemente especificado | Parcial; no certificado |
| 5.º básico | Evaluaciones | Suma de puntaje inconsistente en Historia Forma B; contextualización histórica; trazabilidad pregunta-OA | Parcial; no certificado |
| 6.º básico | Primera pasada | Reparto con resto omitido en Matemática; distinción entre estimación y cálculo exacto; ficción histórica y trabajo infantil | Parcial; no certificado |
| 7.º básico | Guías principales | Encuentros culturales presentados como siempre beneficiosos; categorías de sexualidad que pueden solaparse; inferencias con evidencia textual | Parcial; no certificado |
| 8.º básico | Guías principales | Procedencia de texto literario; simplificación de célula vegetal/animal; transición medieval-moderna no monocausal | Parcial; no certificado |
| 1.º medio | Guías principales | Distinguir tradición cultural de hecho verificado; contextualizar límites históricos de ideales republicanos; ampliar evidencia curricular | Parcial; no certificado |
| 2.º medio | Guías principales | Separar evidencia explícita de inferencia; matizar impacto internacional de crisis de 1929; completar verificación de Matemática | Parcial; no certificado |
| 3.º medio | Guías principales | Varianza poblacional/muestral; argumentos basados en evidencia; procedencia textual; rúbrica para respuestas filosóficas abiertas | Parcial; no certificado |
| 4.º medio | Guías principales y cuatro pasadas de evaluación/Matemática | Supuestos de tasas financieras; puntajes de Ciencias/Filosofía; rúbricas de Inglés; suma total de Educación Ciudadana; 10 cálculos de Matemática verificados, no el examen completo | Parcial; no certificado |

## 4. Controles automatizables propuestos

Estos controles son una propuesta de trabajo, no una afirmación de que ya estén implementados.

### C1. Consistencia de puntajes
- Extraer puntaje declarado en encabezado.
- Sumar puntajes asignados a cada pregunta y rúbrica.
- Marcar discrepancia entre total declarado y suma calculada.
- Incluir casos de puntaje parcial y preguntas de desarrollo para evitar falsos positivos.

### C2. Integridad de clave y alternativas
- Para cada pregunta de selección múltiple, verificar que la clave coincida exactamente con una alternativa existente.
- Marcar claves duplicadas, opciones ausentes, letra que no corresponde al texto de la respuesta y preguntas sin clave.
- Para preguntas abiertas, no forzar una clave de opción múltiple: exigir rúbrica o criterios.

### C3. Referencias a recursos
- Detectar expresiones como «observa el gráfico», «según la imagen», «en el mapa» o «lee el texto» y comprobar que exista un recurso adjunto o una referencia explícita.
- Clasificar el resultado como «recurso no encontrado en Markdown» hasta inspeccionar el render y los recursos externos.

### C4. Comparación de Forma A/B
- Normalizar espacios, signos y formato de Markdown para comparar enunciados.
- Comparar también textos base, alternativas, datos numéricos e ilustraciones referenciadas.
- Informar similitudes para revisión humana; no declarar duplicación inválida solo por coincidencia de formato.

### C5. Trazabilidad OA
- Generar tabla por pregunta: curso, asignatura, archivo, ID de pregunta, OA declarado y evidencia textual.
- Comparar los OA declarados en el encabezado con los OA realmente vinculados a preguntas.
- No inferir cobertura curricular completa a partir de una lista de OA.

### C6. Coherencia de contenido fuente y parser
- Ejecutar fixtures para patrones de opción múltiple, verdadero/falso, respuesta abierta, rúbricas, tablas y recursos multimedia.
- Incluir una prueba negativa para la palabra «alternativas» usada en sentido ordinario (por ejemplo, «alternativas de ahorro»), para evitar falsos positivos del parser.
- Comparar cantidad e IDs de preguntas antes y después de importar.

### C7. Preguntas de Matemática con cálculo reproducible
- Para cada ejercicio numérico, registrar fórmula, sustitución, resultado y unidad.
- Separar resultado exacto, aproximación, estimación y redondeo.
- No intentar validar semánticamente toda la matemática con regex; combinar pruebas automáticas con resolución independiente y revisión humana.

## 5. Orden de ejecución recomendado

1. **Reproducir P1** en 1.º, 4.º, 5.º y 6.º básico; documentar si cada uno se confirma o se descarta.
2. Construir fixtures y pruebas de regresión para consistencia de puntajes y clave-opción.
3. Auditar de forma sistemática las evaluaciones de los cursos restantes, no solo las guías principales.
4. Completar la verificación de preguntas de Matemática de 4.º medio; los diez cálculos verificados hasta ahora no equivalen a validar las 25 preguntas.
5. Regenerar inventario desde el HEAD vigente y resolver discrepancias históricas de conteos.
6. Hacer cotejo curricular oficial por curso y asignatura, registrando versión/URL y evidencia.
7. Solo después de cerrar diagnóstico, preparar una propuesta separada de correcciones y regresión.

## 6. Criterios de salida para cada hallazgo

Cada hallazgo debe terminar en uno de estos estados:

- confirmado: reproducción en archivo vigente con evidencia precisa.
- descartado: la lectura completa o el render demuestra que no hay defecto.
- depende del render/recurso: requiere revisar la aplicación o un archivo externo.
- requiere fuente curricular: requiere cotejo oficial o fuente primaria.
- corregido pendiente de verificación: la corrección existe, pero falta comprobarla.
- cerrado verificado: corrección y prueba de regresión confirmadas.

No marcar como «cerrado» un hallazgo solo porque se haya redactado una recomendación.

## 7. Limitaciones actuales

- Esta consolidación utiliza reportes de auditoría parciales, no una lectura nueva y completa de los 52 archivos principales ni de todos los bancos y exámenes.
- No se ha demostrado aún cobertura oficial del currículo completo de cada nivel.
- Las cantidades históricas de archivos, preguntas y pruebas requieren regeneración desde el HEAD vigente.
- No se modificó contenido educativo, lógica de la aplicación ni base de datos.

## 8. Evidencia de control automático y reproducción documental — 2026-10-21

Se ejecutó el workflow de GitHub Actions sobre la rama `qa/fase-2-matriz-trazabilidad`.

- Última ejecución verificada: https://github.com/rodrigogalvezpinto/logos-school/actions/runs/39690867855
- Pruebas unitarias del validador: **8 aprobadas** en esa ejecución.
- Control estructural: **2 hallazgos detectados**; el job termina en fallo intencional para impedir que las inconsistencias pasen inadvertidas.
- Hallazgo 1: `contenido/04-basico/examenes/examen-integrado-forma-b.md`, pregunta 16. La pauta declara `c) 14`, mientras que la alternativa c es 13 y la alternativa b es 14.
- Hallazgo 2: `contenido/05-basico/examenes/historia-geografia-y-cs-sociales-examen-forma-b.md`. Se declaran 30 puntos al inicio y 35 puntos en la pauta final.

La mejora del patrón de lectura de puntajes permite reconocer declaraciones que incluyen negrita Markdown. La detección automática aporta evidencia estructural, pero no cierra los hallazgos: ambos requieren corrección propuesta, aprobación y regresión. La prueba unitaria adicional para puntajes con formato Markdown se añadió en el commit `531e696eeadd2cbd6c88ab0086c8301c1d899608`; en la ejecución más reciente, las ocho pruebas unitarias pasaron, mientras el control estructural volvió a fallar al detectar los dos hallazgos esperados.


## 9. Reproducción documental adicional — 2026-10-21

Se volvieron a abrir los archivos vigentes de la rama QA y se contrastaron los siguientes casos. Esta comprobación es de fuente Markdown; no sustituye la inspección del render ni la verificación de recursos externos.

| Caso | Evidencia reproducida | Estado | Siguiente paso |
|---|---|---|---|
| LGS-1B-MAT-001 | En `contenido/01-basico/pruebas/matematica-unidad-medicion-datos-probabilidades.md`, la pregunta 2 pide ordenar goma, lápiz y regla por longitud, pero el enunciado no proporciona medidas ni declara una imagen. La pauta presupone un orden único. | Confirmado en la fuente; pendiente verificar render y recursos externos. | Inspeccionar la prueba en QA y comprobar si existe una ilustración asociada fuera del Markdown. No modificar hasta autorización. |
| LGS-4B-EVAL-001 | En `contenido/04-basico/examenes/examen-integrado-forma-b.md`, el control automático reproduce que la pauta de la pregunta 16 dice `c) 14`, mientras la alternativa c es 13 y la b es 14. | Confirmado documental y automáticamente. | Proponer corrección de la letra de la clave, solicitar aprobación y añadir regresión antes de editar contenido. |
| LGS-5B-EVAL-001 | En `contenido/05-basico/examenes/historia-geografia-y-cs-sociales-examen-forma-b.md`, el encabezado declara 30 puntos; el control detecta otra declaración de 35 puntos. La suma de los 25 puntajes declarados en los encabezados de pregunta da 35; la suma de los 25 puntajes de la tabla de pauta también da 35. El encabezado de 30 puntos es la declaración discrepante. | Discrepancia confirmada y suma de ítems/pauta reproducida en 35 puntos; pendiente aprobación para corregir el encabezado de 30. | Sumar todos los puntajes de preguntas y rúbricas y contrastarlos con el total declarado. |
| LGS-6B-MAT-001 | En `contenido/06-basico/matematica.md`, 24.600 ÷ 12 = 2.050 cajas y 2.050 ÷ 3 = 683 cajas por distribuidor con resto 1. La retroalimentación usa `≈ 683` pero no explica el resto. | Confirmado en la fuente; la gravedad depende de la intención didáctica y del contexto de reparto. | Determinar si se esperan cajas enteras y cómo se distribuye la caja restante; revisar la solución pedagógica. |

No se ha comprobado todavía el render real de la prueba de 1.º básico. En 5.º básico, la suma documental de los 25 ítems y de la pauta se reprodujo en 35 puntos, pero la corrección del encabezado requiere aprobación. Estos casos permanecen abiertos y no deben contarse como cerrados.

**Estado de certificación:** no certificado al 100 %. No se ha completado la revisión manual de todos los materiales, el cotejo curricular oficial ni la verificación integral del render e importación en la aplicación.
