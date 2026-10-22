# Handoff y bitácora maestra de auditoría — Logos School

**Última actualización:** 2026-10-21  
**Rama de trabajo:** `qa/fase-2-matriz-trazabilidad`  
**Repositorio:** `rodrigogalvezpinto/logos-school`  
**Propósito:** permitir que cualquier agente humano o de IA retome la auditoría con el contexto, las evidencias, las decisiones y los pendientes sin depender de la memoria de una conversación.

## 1. Estado ejecutivo

La auditoría integral está **en curso**. No se ha certificado la calidad curricular ni pedagógica de todos los cursos. El inventario de archivos es una descripción del repositorio, no una prueba de cobertura curricular.

Objetivo: revisar los 12 niveles (1.º básico a 4.º medio) y todas las asignaturas que efectivamente estén presentes o que el producto declare ofrecer, con criterios apropiados para el nivel escolar chileno. Mantener separadas estas dimensiones:
- alineación con Bases Curriculares y Objetivos de Aprendizaje oficiales;
- exactitud disciplinar;
- progresión didáctica y adecuación etaria;
- calidad de preguntas, claves, explicaciones y retroalimentación;
- experiencia de usuario, accesibilidad, carga cognitiva y seguridad emocional;
- funcionamiento técnico, trazabilidad y persistencia de resultados.

No presentar la revisión automatizada como evaluación clínica ni como sustituto de una validación docente especializada.

## 2. Documentos de referencia existentes

1. [Plan maestro de auditoría integral](auditoria-integral-educativa-plan-maestro.md): marco, dimensiones y criterios.
2. [Inventario reproducible inicial](inventario-reproducible-contenido-educativo.md): inventario estático del árbol Git; el documento registra 891 archivos, 12 carpetas de curso y 13 documentos de análisis curricular, cifras que no demuestran cobertura.
3. [Hallazgos preliminares de 1.º básico](hallazgos-preliminares-1-basico.md): primeras observaciones en materiales de Lenguaje, Matemática, Ciencias e Historia.
4. [Segunda pasada de pruebas de 1.º básico](segunda-pasada-pruebas-1-basico.md): revisión parcial de pruebas y simulacros.
5. [Revisión ampliada de pruebas de 1.º y lectura inicial de 2.º](revision-ampliada-pruebas-1-y-lectura-2-basico.md): incluye, entre otros, una pregunta de longitud sin medidas/imagen suficiente y una pregunta sobre rutina matinal que presupone una respuesta universal.
6. [Informe paralelo curricular de Matemática de 2.º básico](informe-paralelo-curricular-2-basico-matematica.md): revisión inicial de brechas y de materiales de 2.º básico.
7. [Matriz de trazabilidad de Fase 2](../fase-2-matriz-trazabilidad.md): consultar si existe en la rama; verificar su ruta antes de depender de ella.

Los informes parciales no deben describirse como auditorías completas ni como certificados.

## 3. Hallazgos iniciales que requieren seguimiento

- En material de Matemática de 1.º básico se detectó una regla verbal engañosa sobre los nombres de los números del 11 al 19: solo 16–19 empiezan con «dieci-».
- En Lenguaje de 1.º básico hay una definición de fonema que requiere precisión conceptual.
- En Ciencias e Historia se identificaron formulaciones para contrastar con fuentes disciplinares y curriculares.
- En una prueba de Matemática de 1.º básico se pide ordenar objetos por longitud sin proporcionar dimensiones ni una representación que determine el orden.
- En otra pregunta se presupone una rutina matinal universal.
- En un cuento de simulacro, un personaje da leche a un gato encontrado en la calle; se recomendó reformular la acción para priorizar agua, seguridad y ayuda adulta.
- En Ciencias de 2.º básico se observó una afirmación demasiado absoluta sobre mamíferos y nacimiento de crías, pendiente de contraste contextual.

Antes de convertir una observación preliminar en defecto confirmado, volver al archivo y contexto exactos, contrastar fuentes confiables y registrar la evidencia literal y la propuesta.

## 4. Protocolo obligatorio para cada hallazgo

Cada hallazgo nuevo debe registrar:
- ID estable y único;
- curso, asignatura, recurso y ubicación (ruta + pregunta/sección);
- evidencia textual breve o descripción exacta;
- tipo: error confirmado, riesgo/ambigüedad, brecha curricular, mejora sugerida o pendiente de validar;
- fundamento y fuente oficial/disciplina cuando corresponda;
- impacto educativo y adecuación a la edad;
- severidad y justificación;
- corrección recomendada;
- estado: por revisar, validado, corregido, revalidado o descartado;
- prueba de regresión o criterio para comprobar la corrección;
- agente/fecha/commit de revisión.

No modificar el contenido educativo de producción durante la fase de auditoría sin registrar la autorización y el cambio por separado. Evitar cambiar `main`; trabajar en la rama indicada y preferir commits pequeños, revisables y con mensajes claros.

## 5. Plan de continuación

1. Verificar el estado actual de la rama y los documentos; no asumir que una afirmación de la conversación equivale a una acción confirmada en GitHub.
2. Cerrar de manera sistemática la revisión de pruebas de 1.º básico: enunciado, clave, justificación, objetivo curricular, ambigüedad y retroalimentación.
3. Completar 2.º básico por asignatura, ampliando más allá de los cuatro ramos principales cuando existan materiales adicionales.
4. Generar un inventario estructurado por cada uno de los 12 niveles y todas las asignaturas que estén en el repositorio; distinguir “no existe material” de “no se ha revisado”.
5. Contrastar cada asignatura/nivel con el currículum chileno vigente aplicable y documentar la fuente y el OA específico.
6. Revisar por lotes paralelos cuando sea posible, pero mantener una matriz central de cobertura para evitar omisiones o duplicaciones.
7. Después de los primeros niveles, ampliar a los demás cursos y mantener el estado global actualizado.
8. Solo cuando el contenido esté revisado y las pruebas correspondientes existan, preparar un resumen de riesgos y un plan de corrección priorizado. La auditoría no queda cerrada por terminar un lote.

## 6. Criterios de estado

- **No iniciado:** recurso identificado, aún sin revisión.
- **En revisión:** lectura y contraste incompletos.
- **Revisado con hallazgos:** revisión documentada, con pendientes explícitos.
- **Validado sin hallazgos conocidos:** se aplicó el protocolo y no se detectaron problemas en el alcance revisado; no implica garantía absoluta.
- **Corregido pendiente de revalidación:** cambio aplicado, aún no verificado.
- **Revalidado:** cambio y regresión comprobados con evidencia.
- **No evaluable:** falta material, fuente, contexto o herramienta; indicar qué falta.

Nunca usar “aprobado” o “certificado” si la evidencia solo cubre una muestra o una comprobación sintáctica.

## 7. Decisión de alcance pendiente

Hay que confirmar si Logos School busca:
- preparar a estudiantes para exámenes libres con una selección de asignaturas, o
- cubrir el plan de estudios chileno integral.

Hasta resolverlo, auditar todas las asignaturas presentes en el repositorio y registrar como brecha cualquier área oficial que no tenga material, sin asumir que el producto ya prometió cubrirla.

## 8. Cómo retomar desde otra IA

Leer primero este archivo y el plan maestro; después revisar el estado real de la rama y el último commit. Leer la matriz de cobertura y los informes enlazados antes de empezar una tarea nueva. Actualizar este handoff al cerrar cada lote, con fecha, commit, archivos revisados, hallazgos nuevos, pruebas ejecutadas y siguiente acción. No confiar únicamente en resúmenes de chat; las rutas, commits y resultados del repositorio son la fuente de verdad.

## 9. Limitaciones y transparencia

Una sesión conversacional no implica ejecución continua en segundo plano. Todo avance que deba sobrevivir a la sesión tiene que quedar registrado en GitHub. No afirmar que se ejecutaron pruebas, se leyeron archivos o se publicó un documento si no hay resultado verificable. La revisión educativa automatizada apoya el trabajo, pero los casos de alto impacto deben recibir validación de especialistas humanos.


## 10. Bitácora — avance del 21 de octubre de 2026

- Añadido `docs/auditorias/lote-01-medio-matematica-examen-forma-b-recalculo.md`: recálculo independiente de los 25 ítems del examen de Matemática de 1.º medio, Forma B. Se cotejaron las 12 claves de alternativa; no se encontraron discrepancias numéricas/de letra en esta pasada. OA oficiales, rúbricas de desarrollo, comparación con Forma A y QA siguen pendientes.
- Añadido `docs/auditorias/lote-01-basico-matematica-medicion-datos.md`: suficiencia del estímulo en el ítem de longitud de 1.º básico, pendiente de render QA.
- La ejecución de CI `39708460420` terminó con pruebas unitarias del validador aprobadas (8 passed) y el control estructural falló por dos hallazgos de contenido conocidos: clave de 4.º básico Forma B y total de 30/35 puntos en Historia de 5.º básico. No es un fallo de las pruebas unitarias.
- La auditoría global sigue abierta; no se editó contenido educativo ni `main`.

### Siguiente acción
Continuar con recálculo de exámenes por curso y asignatura, extendiendo controles estructurales para clave, puntaje total y formas paralelas. Mantener una matriz de cobertura que distinga revisión documental, revisión pedagógica, contraste curricular y verificación técnica.


### Avance — revisión de Matemática de 2.º medio Forma B (2026-10-21)

- Se creó `docs/auditorias/lote-02-medio-matematica-examen-forma-b-recalculo.md`.
- Se revisaron los 25 ítems de `contenido/02-medio/examenes/matematica-examen-forma-b.md`: se encontró una contradicción P1 en la pregunta 14. La alternativa a) da la inversa correcta `x-10`, mientras la pauta escribe `x+10`.
- Los otros 24 ítems no presentaron discrepancias de cálculo en esta pasada. Aún faltan cotejo oficial de OA, rúbricas de desarrollo, comparación Forma A y QA de importación/render/puntuación.
- CI run [39710128188](https://github.com/rodrigogalvezpinto/logos-school/actions/runs/39710128188) terminó en `failure`; los dos hallazgos estructurales anteriores de 4.º y 5.º básico siguen abiertos. No interpretar el fallo como fallo de pruebas unitarias sin inspeccionar los logs del job correspondiente.
- No se modificó el contenido educativo ni `main`.

**Siguiente paso:** continuar con otro examen de curso distinto y ampliar después el validador para detectar contradicciones entre la respuesta de la alternativa y la respuesta explicada en la pauta, sin falsos positivos en preguntas abiertas.


### Avance adicional — cribado transversal de Matemática (2026-10-22)

- Se creó `docs/auditorias/lote-transversal-matematica-3medio-8basico-cribado.md`.
- Se revisaron cálculos seleccionados de las pautas de Matemática Forma B de 3.º y 4.º medio y 5.º–8.º básico. Los ítems efectivamente recalculados coincidieron con sus respuestas esperadas. No afirmar que todos los ítems o el currículo estén validados.
- Se comprobó la pregunta 2 de 6.º básico: $39.500.000 / $4.300.000 permite 9 buses completos y deja $800.000; es coherente con el enunciado presupuestario, así que no se registra como error.
- Hallazgo P1 confirmado en 2.º medio: la pregunta 14 presenta una contradicción entre la alternativa correcta `x-10` y la pauta `x+10`. El validador actual aún no detecta este tipo de contradicción semántica.
- CI runs recientes consultados: [39710761424](https://github.com/rodrigogalvezpinto/logos-school/actions/runs/39710761424), [39710756829](https://github.com/rodrigogalvezpinto/logos-school/actions/runs/39710756829), ambos con conclusión `failure`. Antes de afirmar qué job falló, revisar los logs; los fallos estructurales conocidos siguen pendientes.
- No se modificaron preguntas originales ni `main`.

**Siguiente paso:** ampliar la revisión disciplinar a Ciencias, Historia, Inglés y Lengua y Literatura y mejorar el validador para detectar discrepancias entre la alternativa y su explicación en la pauta.


### Avance — Ciencias Naturales 1.º medio Forma B (2026-10-22)

- Nuevo informe: `docs/auditorias/lote-01-medio-ciencias-naturales-forma-b.md`.
- Hallazgo P2: pregunta 9 confunde bioacumulación y biomagnificación en la pauta; la explicación corresponde principalmente a biomagnificación. Verificar enunciado antes de corregir.
- Reconciliación de puntaje confirmada: 15×1 + 4×2 + 6×3 = 41 puntos, 25 preguntas.
- Los cálculos seleccionados de transferencia energética, sonar y estequiometría coinciden con la pauta bajo los supuestos declarados.
- Pendiente cotejar OA oficiales, comparar Forma A/B y probar importación/render/puntuación. No se modificó contenido educativo ni `main`.
