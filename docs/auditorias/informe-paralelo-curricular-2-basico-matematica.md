# Informe de avance paralelo — revisión curricular, 2° básico y consistencia transversal

**Rama:** `qa/fase-2-matriz-trazabilidad`  
**Fecha de revisión:** 2026-10-21  
**Tipo:** informe de trabajo con evidencia estática; no es certificación final.  
**Alcance paralelo de esta etapa:** (A) contraste de cobertura declarada con la oferta curricular oficial, (B) lectura de los cuatro materiales principales de 2° básico, (C) lectura transversal de metadatos de Matemática de 3° básico a 4° medio.

## A. Riesgo de alcance curricular: no confundir “banco de validación” con currículo escolar completo

La página oficial del Currículum Nacional presenta, para 1°–6° básico, áreas como Artes Visuales, Ciencias Naturales, Educación Física y Salud, Historia/Geografía/Ciencias Sociales, Lenguaje, Matemática, Música, Orientación y Tecnología; también contempla Inglés, Religión y Lengua y Cultura de los Pueblos Originarios Ancestrales en sus respectivas condiciones y marcos curriculares. Fuente: https://www.curriculumnacional.cl/curriculum/1o-6o-basico y https://aprendoenlinea.mineduc.gob.cl/1o-6o-basico.

Los documentos de estado del repositorio describen un alcance más acotado en los cursos iniciales y materias adicionales a partir de ciertos niveles, y los archivos principales que se leyeron en 2° básico son Matemática, Lenguaje, Ciencias e Historia. Esto **no demuestra por sí solo un incumplimiento**: parte del producto se describe como preparación para Exámenes Libres de Validación de Estudios, que tienen temarios y formatos propios. Sí establece una decisión de producto que debe quedar explícita:

- **Modo “preparación de examen de validación”:** auditar contra el temario oficial del examen específico, nivel, convocatoria y versión.
- **Modo “currículo escolar integral”:** auditar contra todas las asignaturas y OA que correspondan a nivel, modalidad y marco oficial, registrando las áreas que no están implementadas.
- No etiquetar como “cobertura de todo el currículum escolar” una cobertura diseñada para un temario de examen más estrecho.

Para 3°–4° medio, además, hay que identificar si el alcance es Plan Común/General, Humanístico-Científico o Técnico-Profesional antes de comparar cobertura; la fuente oficial separa bases y planes por niveles/modalidades: https://www.curriculumnacional.cl/Curriculum/Bases_Curriculares.

**Prioridad de auditoría:** P1 de alcance/producto, pendiente de confirmar el posicionamiento exacto que Logos School quiere declarar. No es una afirmación de que el producto esté incumpliendo la normativa.

## B. 2° básico — revisión de cuatro materiales principales

Se consultaron los cuatro archivos completos desde GitHub y se inspeccionaron sus encabezados y fragmentos temáticos, preguntas y retroalimentaciones. Esta lectura detecta candidatos a revisión, pero no reemplaza un cotejo OA por OA ni una verificación de todas las claves.

| ID | Archivo / ubicación | Evidencia | Evaluación | Severidad provisional | Próximo paso |
|---|---|---|---|---|---|
| LS-2B-LEN-001 | `contenido/02-basico/lenguaje-y-comunicacion.md`, explicación inicial de diptongo | El ejemplo “cielo” se segmenta como “cie-lo” y se identifica “ie” como diptongo. | El ejemplo es coherente: “ie” se pronuncia en una misma sílaba. En la misma sección, el texto también explica “leemos” como hiato. No se detecta error en estos ejemplos inspeccionados. | Sin hallazgo; verificación parcial | Mantener provisionalmente; revisar el resto de las reglas y ejemplos, en especial acentuación y casos con h intercalada. |
| LS-2B-CN-001 | `contenido/02-basico/ciencias-naturales.md`, ciclo de vida de animales | El texto afirma que “solo los mamíferos crecen dentro del cuerpo de su madre”; clasifica aves, anfibios e insectos como animales que nacen de huevos. | La frase puede ser demasiado absoluta como generalización zoológica: existen mamíferos ovíparos (monotremas). Para el objetivo escolar y los ejemplos del documento puede bastar una regla simplificada, pero “solo los mamíferos” es una formulación problemática y la clasificación merece precisión. | P2 — medio, revisar adecuación curricular y nivel de simplificación | Cambiar a “muchos mamíferos, como el guanaco y el zorro, se desarrollan dentro de la madre; las aves y los insectos de estos ejemplos nacen de huevos”, o redacción equivalente que no universalice. Confirmar contra OA/temario y no sobrecargar 2° básico con excepciones que no sean necesarias. |
| LS-2B-HIS-001 | `contenido/02-basico/historia-geografia-y-cs-sociales.md`, preguntas sobre pueblos originarios | Se observan preguntas sobre pueblos canoeros australes, We Tripantu, culturas y movilidad; las respuestas incluyen algunas generalizaciones sobre modos de vida. | La presencia de pueblos diversos es una fortaleza. Las afirmaciones históricas sobre prácticas y subsistencia deben asociarse a pueblo, territorio y periodo, evitando describir una cultura entera como homogénea o exclusivamente dependiente de una sola actividad. La lectura parcial no permite señalar una clave específica errónea. | P2 — vigilancia de precisión cultural | Revisar enunciado por enunciado con fuente curricular e histórica fiable; distinguir evidencia documentada de simplificación didáctica. |
| LS-2B-MAT-001 | `contenido/02-basico/matematica.md`, encabezado y ámbito declarado | El documento declara ámbito numérico 0–100, sumas/restas sin reserva, tablas del 2, 5 y 10 y 13 OA seleccionados. | Son afirmaciones curriculares verificables y específicas; no se confirma aquí que todos los ejercicios respeten el ámbito declarado. | Pendiente de auditoría exhaustiva | Buscar ítems fuera del rango, algoritmos con reserva, multiplicaciones fuera de tablas previstas y claves que no correspondan a los enunciados. |

## C. Lectura transversal de Matemática, 3° básico a 4° medio

Se recuperaron los encabezados de los 10 archivos de Matemática de 3° básico a 4° medio. Declaran marcos normativos diferentes por tramo: Decreto 439/2012 en 1°–6° básico, Decreto 614/2013 en 7° básico–2° medio y Decreto 193/2019 para el Plan Común de 3°–4° medio. La segmentación es plausible según los propios documentos, pero el encabezado no acredita que cada OA o actividad esté correctamente vinculado a la fuente.

| Curso | OA declarados en el encabezado | Marco declarado en archivo | Estado |
|---|---:|---|---|
| 3° básico | 13 | Decreto 439/2012 | Conteo declarado; pendiente de cotejo OA por OA |
| 4° básico | 14 | Decreto 439/2012 | Conteo declarado; pendiente de cotejo OA por OA |
| 5° básico | 17 | Decreto 439/2012 | Conteo declarado; pendiente de cotejo OA por OA |
| 6° básico | 11 | Decreto 439/2012 | Conteo declarado; pendiente de cotejo OA por OA |
| 7° básico | 9 | Decreto 614/2013 | Conteo declarado; pendiente de cotejo OA por OA |
| 8° básico | 10 | Decreto 614/2013 | Conteo declarado; pendiente de cotejo OA por OA |
| 1° medio | 7 | Decreto 614/2013 | Conteo declarado; pendiente de cotejo OA por OA |
| 2° medio | 6 | Decreto 614/2013 | Conteo declarado; pendiente de cotejo OA por OA |
| 3° medio | No confirmado en esta pasada | Decreto 193/2019, “Plan Común” | Debe aclararse modalidad y selección curricular |
| 4° medio | No confirmado en esta pasada | Decreto 193/2019, “Plan Común” | Debe aclararse modalidad y selección curricular |

La diferencia entre “OA seleccionados para el temario de validación” y “todos los OA de las Bases Curriculares” debe conservarse en los reportes, sin presentarlos como equivalentes.

## D. Trabajo paralelo completado y límites

En esta etapa se trabajó simultáneamente en: alcance oficial de asignaturas, lectura inicial de 2° básico en cuatro materias y revisión de encabezados de Matemática en diez niveles. Se documentaron observaciones, no se modificaron materiales educativos y no se ejecutaron pruebas automatizadas.

## E. Próximos lotes

1. Revisar todas las preguntas de Matemática de 2° básico buscando conflictos con el ámbito numérico/operacional declarado.
2. Revisar bancos y simulacros de 2° básico en paralelo con Ciencias e Historia; verificar claves contra enunciados.
3. Auditar Matemática de 3°–4° básico por límites de rango, cálculo y solución paso a paso.
4. Construir matriz de asignaturas implementadas vs. temario de validación vs. currículo escolar integral, separando explícitamente los tres alcances.
5. Continuar por lotes de archivos y registrar los resultados en informes pequeños para evitar que el trabajo se convierta en una afirmación genérica de “100% cubierto”.
