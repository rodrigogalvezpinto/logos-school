# Cuarta pasada — control de consistencia de evaluaciones de 4.º medio

**Rama:** `qa/fase-2-matriz-trazabilidad`  
**Alcance:** control documental adicional de Forma B en seis asignaturas. Se contrastaron declaraciones de formato, tablas de puntaje y criterios visibles; no se hizo una comparación completa de Forma A con B porque en el repositorio consultado no se encontraron seis pares equivalentes en el mismo directorio.

## Hallazgos y controles

### LGS-4M-EVAL-006 — No afirmar equivalencia con la Forma A sin comparación reproducible
- **Severidad provisional:** P2.
- **Evidencia:** los archivos Forma B remiten a pruebas Forma A alojadas en `contenido/04-medio/pruebas/`, no como un conjunto paralelo de archivos “examen-forma-a” en el directorio `examenes`.
- **Evaluación:** esa organización no es un defecto por sí misma, pero impide dar por demostrada la promesa de preguntas diferentes solo a partir de los encabezados.
- **Recomendación:** generar un manifiesto con la ruta real de cada Forma A, sus 25 ítems, el identificador/OA y una huella normalizada del enunciado y estímulo. Comparar similitud exacta y semántica, documentando los casos que comparten texto base pero cambian la pregunta.

### LGS-4M-EVAL-007 — Inglés: hacer operativa la corrección de preguntas abiertas
- **Severidad provisional:** P2.
- **Archivo:** `contenido/04-medio/examenes/ingles-examen-forma-b.md`.
- **Evidencia:** la prueba declara 25 preguntas, de las cuales 6 son de selección múltiple y 19 son de respuesta abierta en formatos variados; las instrucciones señalan que todas las preguntas valen lo mismo.
- **Evaluación:** sin una regla común y visible, completar, emparejar, responder en inglés y producir un párrafo pueden quedar sometidos a criterios inconsistentes. Una misma ponderación puede ser válida si la pauta define qué cuenta como respuesta correcta y cómo tratar respuestas parcialmente correctas.
- **Recomendación:** especificar para cada tipo el crédito completo/parcial, respuestas equivalentes aceptables y tolerancia a errores lingüísticos cuando no impidan comprender el significado.

### LGS-4M-EVAL-008 — Educación Ciudadana: comprobar suma de puntajes contra la tabla completa
- **Severidad provisional:** P3 (verificación pendiente).
- **Archivo:** `contenido/04-medio/examenes/educacion-ciudadana-examen-forma-b.md`.
- **Evidencia:** el encabezado declara 25 preguntas y remite el puntaje total a la pauta; la pauta asigna 1 punto a selección múltiple/V-F/pareados, 2 a desarrollo breve y 3 a desarrollo extenso.
- **Evaluación:** la regla es explícita, pero para certificar la nota máxima se necesita sumar todos los renglones de la tabla y contrastar con el resumen final.
- **Recomendación:** automatizar el cálculo de puntaje máximo desde la pauta y fallar la validación si difiere del total declarado.

### LGS-4M-EVAL-009 — Control positivo de puntajes
- **Estado:** sin discrepancia en los resúmenes examinados.
- **Archivos:** Ciencias para la Ciudadanía y Filosofía, Forma B.
- **Comprobación:** Ciencias para la Ciudadanía: 7 + 4 + 14 + 21 = 46 puntos en 25 preguntas. Filosofía: 16 + 15 + 20 = 51 puntos en 25 preguntas.
- **Acción:** convertir estas sumas en pruebas automáticas para evitar regresiones cuando cambie la pauta.

## Prioridades consolidadas para 4.º medio
1. Mantener los diez recálculos de Matemática como pruebas de referencia y completar la revisión de los 25 ítems.
2. Añadir verificación automática de puntajes y cantidad de preguntas en los seis exámenes.
3. Auditar rúbricas de respuestas abiertas, especialmente Inglés, Filosofía y Educación Ciudadana.
4. Comparar las formas A/B a partir de las rutas reales y los textos completos, no solo por sus encabezados.
5. Completar trazabilidad curricular OA → contenido → práctica → evaluación.

## Estado
**4.º medio: auditoría de contenido principal y varias pasadas de evaluación documentadas, todavía parcial.** Los hallazgos marcados como pendientes requieren comprobación con la tabla completa o comparación automatizada; no se presentan como errores confirmados.
