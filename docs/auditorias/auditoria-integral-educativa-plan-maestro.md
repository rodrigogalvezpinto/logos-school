# Auditoría integral educativa de Logos School — Plan maestro

**Estado:** diseño de auditoría y línea de investigación; no constituye todavía una certificación curricular ni clínica.  
**Rama:** `qa/fase-2-matriz-trazabilidad`  
**Alcance:** contenido, evaluación, experiencia del alumno, accesibilidad y consistencia técnica para los 12 niveles (1° básico a 4° medio).

## 1. Propósito y principio de evidencia

Auditar todos los cursos y asignaturas presentes en el repositorio, verificando cada recurso contra fuentes curriculares oficiales vigentes y contra criterios didácticos apropiados para la edad. No se considerará una materia «aprobada» solo porque exista un archivo, un OA esté citado o una prueba automatizada pase.

Cada hallazgo deberá incluir: identificador, curso, asignatura, archivo y ubicación, evidencia literal o reproducible, criterio de evaluación, severidad, impacto en el aprendizaje, recomendación, prueba de corrección y estado. Distinguir siempre:
- **Verificado:** evidencia directa suficiente.
- **Hallazgo probable:** señal que requiere revisión manual o ejecución.
- **No verificable aún:** falta fuente, contexto, entorno o evidencia.
- **No aplica:** justificación explícita.

No inventar OA, decretos, expectativas de edad ni resultados de pruebas. Registrar versión y fecha de la fuente consultada. Una coincidencia de códigos OA no demuestra por sí sola cobertura, profundidad, precisión ni calidad pedagógica.

## 2. Dimensiones de auditoría

| Código | Dimensión | Preguntas que debe responder la auditoría |
|---|---|---|
| CUR | Fidelidad curricular | ¿Corresponde al curso, asignatura, OA y programa oficial vigente? ¿La fuente oficial está identificada y versionada? |
| DIS | Dominio disciplinar | ¿Son correctos conceptos, datos, procedimientos, explicaciones, soluciones y claves? |
| DID | Calidad didáctica | ¿Existe progresión, andamiaje, modelado, práctica guiada e independiente, transferencia y recuperación de conocimientos previos? |
| EDAD | Adecuación evolutiva | ¿La extensión, vocabulario, abstracción, instrucciones, carga de memoria y autonomía son razonables para el nivel? La edad real puede variar; el curso no basta para diagnosticar capacidad individual. |
| EVA | Evaluación | ¿Cada pregunta mide el objetivo declarado? ¿Clave, distractores, rúbrica y puntaje son defendibles? ¿Hay sesgos, ambigüedad o más de una respuesta válida? |
| RET | Retroalimentación | ¿Explica por qué una respuesta es correcta/incorrecta y qué hacer después, sin humillar ni inducir indefensión? |
| INC | Inclusión y accesibilidad | ¿Hay lenguaje claro, apoyos multimodales pertinentes, contraste, navegación por teclado, lectores de pantalla y alternativas razonables sin bajar arbitrariamente el objetivo? |
| UX | Experiencia infantil | ¿El flujo es predecible, legible, de baja fricción, con instrucciones claras, control de avance, guardado y errores recuperables? |
| SOC | Bienestar y privacidad | ¿Los mensajes de motivación, rachas, ranking, notas y check-in evitan vergüenza, presión indebida, etiquetado y exposición de datos sensibles? |
| TEC | Integridad técnica | ¿El recurso se carga correctamente, mantiene relación contenido-OA, acepta los tipos de respuesta esperados y registra resultados de forma consistente? |
| TRA | Trazabilidad | ¿Se puede rastrear fuente oficial → OA → guía/actividad → pregunta → clave/rúbrica → retroalimentación → prueba automatizada/manual? |

## 3. Matriz de alcance por nivel

La matriz inicial refleja las asignaturas que el archivo `contenido/00-estado-contenido.md` declara para cada régimen. **Es un inventario declarado por el proyecto, no una confirmación independiente de que cada ramo esté completo o sea oficial.** Durante la auditoría se debe comparar con las Bases Curriculares, programas y planes de estudio oficiales vigentes para cada nivel y modalidad.

| Nivel | Asignaturas declaradas en el estado del proyecto | Revisión requerida |
|---|---|---|
| 1° básico | Lenguaje/Comunicación, Matemática, Ciencias Naturales, Historia/Geografía/Ciencias Sociales | Confirmar oferta oficial, objetivos, progresión inicial, lectura emergente, numeración, instrucciones y duración apropiada. |
| 2° básico | Lenguaje/Comunicación, Matemática, Ciencias Naturales, Historia/Geografía/Ciencias Sociales | Confirmar continuidad con 1°, fluidez y comprensión, estrategias de cálculo y vocabulario. |
| 3° básico | Lenguaje/Comunicación, Matemática, Ciencias Naturales, Historia/Geografía/Ciencias Sociales | Revisar transición a mayor autonomía, problemas multietapa y comprensión de textos informativos. |
| 4° básico | Lenguaje/Comunicación, Matemática, Ciencias Naturales, Historia/Geografía/Ciencias Sociales | Revisar consolidación de básica inicial, interpretación de datos, fuentes y explicación escrita. |
| 5° básico | Lengua/Lenguaje, Matemática, Ciencias Naturales, Historia/Geografía/Ciencias Sociales, Inglés | Auditar transición a asignaturas separadas, vocabulario académico, lectura de consignas y exigencia evaluativa. |
| 6° básico | Lengua/Lenguaje, Matemática, Ciencias Naturales, Historia/Geografía/Ciencias Sociales, Inglés | Revisar progresión vertical y prerrequisitos para 7°. |
| 7° básico | Lengua y Literatura, Matemática, Ciencias Naturales, Historia/Geografía/Ciencias Sociales, Inglés | Verificar cambio de ciclo, abstracción, carga de tareas y alineación de programas por asignatura. |
| 8° básico | Lengua y Literatura, Matemática, Ciencias Naturales, Historia/Geografía/Ciencias Sociales, Inglés | Revisar progresión y preparación hacia enseñanza media sin enseñar anticipadamente contenidos fuera de alcance. |
| 1° medio | Lengua y Literatura, Matemática, Ciencias Naturales, Historia/Geografía/Ciencias Sociales, Inglés | Confirmar plan de estudios y distinción entre Ciencias, Física, Química o Biología según programa/organización adoptada. |
| 2° medio | Lengua y Literatura, Matemática, Ciencias Naturales, Historia/Geografía/Ciencias Sociales, Inglés | Verificar continuidad curricular y preparación para electividad/especialización posterior. |
| 3° medio | Lengua y Literatura, Matemática, Ciencias para la Ciudadanía, Filosofía, Inglés, Educación Ciudadana | Revisar plan común vigente, asignaturas diferenciadas/electivas y precisión de nombres/planes. |
| 4° medio | Lengua y Literatura, Matemática, Ciencias para la Ciudadanía, Filosofía, Inglés, Educación Ciudadana | Verificar continuidad, profundidad, pertinencia de actividades y exigencias de egreso según modalidad aplicable. |

**Regla de alcance:** no asumir que esta lista es el catálogo exhaustivo de ramos del currículum chileno. Se contrastará con los documentos oficiales aplicables al curso y con el alcance real que Logos School declara ofrecer. Se documentarán las asignaturas omitidas, optativas, diferenciadas o no implementadas.

## 4. Protocolo de revisión por asignatura y curso

1. **Inventariar:** listar todos los archivos de guías, contenidos, bancos de preguntas, pruebas de unidad, exámenes Forma A/B, rúbricas y recursos complementarios.
2. **Identificar fuente:** registrar Bases Curriculares, programa de estudio, decreto/plan aplicable, OA y versión oficial. Cuando la fuente no esté disponible, el resultado queda pendiente, no se infiere.
3. **Construir mapa OA:** fuente oficial → OA → indicador/criterio observable → recurso → actividad → pregunta → solución/clave → feedback.
4. **Revisión disciplinar:** comprobar individualmente cálculos, hechos, definiciones, cronología, mapas, experimentos, gramática, traducciones, interpretación textual, argumentos y fuentes.
5. **Revisión didáctica y etaria:** evaluar prerequisitos, progresión, claridad, ejemplos, carga cognitiva, longitud, accesibilidad, práctica y transferencia.
6. **Revisión evaluativa:** comprobar validez, alineación, dificultad, distractores, redacción, rúbrica, criterios de puntuación, consistencia de Forma A/B y cobertura de OA.
7. **Pruebas técnicas:** parseo, renderizado, integridad de IDs, carga de recursos, guardado, puntuación y retroalimentación; no usar la aprobación técnica como sustituto de la revisión pedagógica.
8. **Triangulación:** contrastar hallazgos entre guía, banco, evaluación, implementación del frontend/backend y pruebas existentes.
9. **Informe por ramo:** resumen ejecutivo, tabla de hallazgos, evidencias por archivo/pregunta, cobertura OA, riesgos, correcciones propuestas y verificación posterior.
10. **Cierre:** solo marcar «aprobado para revisión final» cuando los bloqueantes estén resueltos y exista evidencia verificable. La certificación definitiva de alineación curricular debe tener revisión humana experta.

## 5. Severidad e impacto

- **P0 — Crítico:** error factual/conceptual que enseña algo falso; clave incorrecta con perjuicio relevante; contenido inadecuado o riesgoso; filtración de datos; evaluación que invalida sistemáticamente el resultado.
- **P1 — Alto:** desalineación importante con OA/curso, ambigüedad que cambia la respuesta, error de puntuación, barrera seria de accesibilidad o retroalimentación engañosa.
- **P2 — Medio:** explicación incompleta, andamiaje insuficiente, distractores débiles, progresión irregular o dificultad descalibrada que afecta a un subconjunto de alumnos.
- **P3 — Bajo:** erratas, formato, consistencia editorial o mejora de usabilidad sin impacto sustancial demostrado.

Priorizar por impacto y alcance, no por cantidad de errores ni por facilidad de arreglo.

## 6. Rúbrica común de calidad

Calificar cada dimensión de 0 a 3, siempre con evidencia:
- **0 — No cumple / evidencia de error sustantivo.**
- **1 — Cumple parcialmente; requiere cambios importantes.**
- **2 — Cumple en lo esencial; requiere mejoras acotadas.**
- **3 — Evidencia suficiente de cumplimiento para el criterio evaluado.**
- **NE — No evaluable con la evidencia disponible.**

No convertir NE en cero ni calcular porcentajes de «calidad total» cuando hay dimensiones no evaluables. Los promedios no pueden ocultar un P0/P1: cualquier hallazgo crítico bloquea la aprobación del ramo.

## 7. Experiencia de usuario y desarrollo infantil

Evaluar por separado 1°–2°, 3°–4°, 5°–6°, 7°–8° básico y 1°–2° / 3°–4° medio, evitando tratar a todos los alumnos de un curso como iguales. Revisar:
- instrucciones breves y específicas, una acción principal por pantalla cuando sea posible;
- lectura, tipografía, espaciado, contraste y legibilidad en móvil;
- ejemplos resueltos y pistas progresivas antes de revelar la respuesta;
- feedback centrado en la estrategia y el siguiente paso, no en etiquetas personales («eres malo», «no eres inteligente»);
- reintentos y corrección de errores con explicación;
- duración real de actividad y pausas razonables, sin premiar simplemente permanecer conectado;
- rachas/gamificación sin castigos por ausencias, comparaciones humillantes ni presión;
- check-in emocional opcional, no diagnóstico, con privacidad y rutas de ayuda apropiadas; no inferir salud mental a partir de una respuesta aislada;
- lector de pantalla, teclado, zoom, subtítulos/transcripción cuando aplique, y alternativas a audio/color;
- participación de niños y apoderados solo con consentimiento y salvaguardas apropiadas. No recoger datos sensibles innecesarios.

## 8. Hallazgos de consistencia que ya requieren verificación

La documentación del repositorio contiene afirmaciones de completitud que no equivalen a una auditoría independiente. Por ejemplo:
- `contenido/00-estado-contenido.md` declara cursos, asignaturas, OA y pruebas «completos», y también señala totales consolidados pendientes de recalcular.
- `docs/qa/plan-avance-12-cursos.md` declara 886 pruebas y 100% de cobertura, mientras que la línea base de QA distingue pruebas actuales de resultados E2E históricos. Se debe ejecutar o verificar el pipeline actual antes de repetir esos números como hechos vigentes.
- El inventario de suites debe cotejarse con los archivos reales y con el código que implementa las rutas y evaluaciones.
- La presencia de PDFs curriculares en `Temarios/` es útil, pero debe comprobarse si son las fuentes oficiales pertinentes y vigentes para cada asignatura/nivel; no basta con que el archivo exista.

Estos son **riesgos de trazabilidad y afirmaciones por validar**, no prueba automática de que el contenido sea incorrecto.

## 9. Entregables de la auditoría

1. **Inventario de cobertura:** nivel × asignatura × OA × tipo de recurso, con conteos calculados desde archivos reales.
2. **Ficha individual por curso y asignatura:** evidencias, puntuación por dimensión, hallazgos y decisión.
3. **Registro maestro de hallazgos:** IDs únicos, severidad, responsable, dependencia, estado y evidencia de cierre.
4. **Mapa de progresión vertical:** prerrequisitos y continuidad entre niveles, identificando repetición, saltos y lagunas.
5. **Auditoría de evaluación:** exactitud de claves, rúbricas, dificultad, duplicación y cobertura.
6. **Auditoría UX/a11y:** hallazgos reproducibles por dispositivo, edad objetivo y necesidad de apoyo.
7. **Informe ejecutivo:** riesgos de lanzamiento, prioridades y decisiones pendientes.
8. **Plan de remediación:** cambios por lotes, pruebas de regresión y criterios de aceptación.

## 10. Orden de ejecución recomendado

- **Fase A — Inventario reproducible:** recorrer el repositorio completo y generar el catálogo real de cursos, asignaturas, OA, guías, bancos, evaluaciones, rutas y tests.
- **Fase B — Fuentes curriculares:** contrastar nombres, planes, OA y versiones con fuentes oficiales del Ministerio de Educación y Currículum Nacional.
- **Fase C — Auditoría por ramo:** procesar cada asignatura de cada curso, empezando por riesgos de exactitud y evaluación; no limitarse a Matemática.
- **Fase D — UX y accesibilidad:** revisar componentes compartidos y después flujos por etapa etaria.
- **Fase E — Verificación técnica:** ejecutar tests disponibles en entorno seguro y registrar comandos, fecha, commit y resultados reales.
- **Fase F — Correcciones y cierre:** arreglar hallazgos priorizados en lotes pequeños; revisar diff y pruebas antes de proponer PR.

## 11. Restricciones y seguridad

- No modificar automáticamente grandes volúmenes de contenido educativo sin revisión de evidencia.
- No borrar ni regenerar IDs de OA, preguntas, respuestas o registros que puedan estar referenciados por la base de datos.
- No ejecutar migraciones, SQL destructivo ni pruebas sobre producción.
- No afirmar que se ejecutaron pruebas si solo se inspeccionó documentación o código.
- No declarar «100% alineado con Mineduc» sin mapa completo y validación de fuentes.
- Separar correcciones mecánicas (ortografía/formatos) de cambios sustantivos en contenido o clave.
- Mantener todo el trabajo en rama aislada y preparar PR; no fusionar en `main` sin revisión.

## 12. Criterio de aceptación global

La auditoría estará lista para revisión final cuando:
- todos los archivos educativos estén inventariados, incluidos los que no se pudieron parsear;
- cada curso y ramo declarado tenga una ficha con estado explícito;
- cada OA aplicable tenga trazabilidad o una brecha documentada;
- todas las alertas P0/P1 tengan resolución comprobada o bloqueo explícito;
- los conteos de preguntas, evaluaciones y tests se recalculen desde los artefactos reales;
- la suite técnica actual esté ejecutada o sus limitaciones estén declaradas;
- exista un informe de cobertura con incertidumbres, fuentes, commit y fecha;
- las conclusiones no excedan la evidencia reunida.
