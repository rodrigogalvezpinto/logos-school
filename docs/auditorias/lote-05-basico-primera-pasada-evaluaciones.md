# Auditoría preliminar de evaluaciones — 5.º básico, primera pasada

**Rama:** `qa/fase-2-matriz-trazabilidad`  
**Alcance:** inspección inicial de las cinco guías principales (Matemática, Lenguaje y Comunicación, Ciencias Naturales, Historia, Geografía y Ciencias Sociales e Inglés) y de las Formas B disponibles para las asignaturas que tienen examen en `contenido/05-basico/examenes/`. Se revisaron consistencia interna, algunas claves y estructura de puntuación. No es una auditoría exhaustiva de cada pregunta, no certifica alineación OA oficial y no implica que se hayan comparado todos los bancos Forma A/B. No se modificó contenido fuente ni `main`.

## Hallazgos

### LGS-5B-EVAL-001 — El examen de Historia tiene un puntaje total incompatible con la suma de su pauta
- **Severidad:** P1 (integridad de la evaluación y calificación).
- **Archivo:** `contenido/05-basico/examenes/historia-geografia-y-cs-sociales-examen-forma-b.md`.
- **Evidencia:** el encabezado declara **30 puntos**. La pauta asigna 1 punto a cada pregunta de alternativas, 2 a desarrollo breve y 3 a desarrollo extenso; la tabla final suma **35 puntos** (y la pauta contiene 25 preguntas con una distribución explícita de puntajes).
- **Impacto:** si el sistema califica sobre 30 pero la pauta suma 35, los porcentajes, la conversión a nota y el resultado mostrado pueden ser incorrectos.
- **Recomendación:** fijar un único total oficial, verificar la suma mediante prueba automatizada y recalcular cualquier escala de conversión solo después de definir la regla de calificación.

### LGS-5B-EVAL-002 — La prueba de Historia presenta una simplificación causal fuerte sobre el descenso demográfico indígena
- **Severidad provisional:** P2 (precisión histórica y tratamiento de un tema sensible).
- **Archivo:** `contenido/05-basico/examenes/historia-geografia-y-cs-sociales-examen-forma-b.md`, pregunta 6.
- **Evidencia:** pregunta por la causa “principal” de la fuerte disminución de población indígena y la pauta señala las enfermedades traídas por europeos.
- **Evaluación:** las epidemias fueron un factor central, pero el ítem no distingue entre regiones y períodos ni reconoce que guerras, desplazamientos, explotación y alteraciones sociales también contribuyeron. La formulación de una única causa puede enseñar una explicación demasiado reducida.
- **Recomendación:** validar con fuentes históricas confiables y decidir si el objetivo es reconocer el impacto de epidemias o explicar la caída demográfica como proceso multifactorial. Ajustar en una fase posterior.

### LGS-5B-EVAL-003 — La prueba de Matemática declara 17 OA cubiertos, pero su resumen solo enumera 14 identificadores OA distintos
- **Severidad provisional:** P2 (trazabilidad curricular).
- **Archivo:** `contenido/05-basico/examenes/matematica-examen-forma-b.md`.
- **Evidencia:** el encabezado afirma cubrir los mismos 17 OA que la Forma A. El resumen por eje enumera OA 1, 3, 4, 6, 7, 10, 11, 13, 14, 15, 17, 18, 19, 22, 23, 24 y 26: son 17 identificadores, aunque la tabla compacta de cobertura omite algunos dentro de la lista de OA por eje (por ejemplo, OA 5, 8, 9, 12, 16, 20, 21 y 25 no aparecen). El número “17 OA” puede referirse al conjunto total curricular seleccionado, no necesariamente a 17 OA efectivamente evaluados.
- **Estado:** inconsistencia de trazabilidad por resolver, no prueba por sí sola que falte contenido en la guía.
- **Recomendación:** generar cobertura automáticamente desde las preguntas y comprobar que la afirmación “cubre los mismos 17 OA” se refiera a los OA realmente evaluados en ambas formas.

## Comprobaciones de muestra

- Matemática Forma B: 52 × 38 = 1.976; 187 ÷ 5 = cociente 37 y resto 2; 245 ÷ 9 requiere 28 buses; 6 × $890 = $5.340 y el vuelto de $10.000 es $4.660; el orden de 89.500, 908.005, 980.050 y 980.500 es coherente con la pauta.
- Inglés Forma B: las claves examinadas para comprensión literal, vocabulario cotidiano, conectores y expresiones breves concuerdan con los estímulos. En respuestas abiertas, deben aceptarse equivalentes gramaticales adecuados cuando la tarea no exige una forma única.
- Historia Forma B: la cronología de Almagro, Valdivia, fundación de Santiago y desastre de Curalaba concuerda con el orden esperado en la pauta; el examen requiere revisar la suma de puntajes antes de usarlo para calificar.
- Ciencias Naturales Forma B: el documento declara 25 preguntas y un máximo de 36 puntos; la tabla de distribución suma 17 preguntas de alternativas (17 puntos), 5 desarrollos breves (10) y 3 extensos (9), total 36, consistente internamente en esa parte.

## Pendientes para completar 5.º básico

1. Revisar todas las preguntas y pautas de cada prueba de unidad y cada examen Forma A/B disponible.
2. Verificar todas las claves de alternativa tanto por valor como por letra, y recalcular operaciones y unidades.
3. Comprobar que las respuestas abiertas tengan rúbricas y que el motor de evaluación las corrija de forma compatible.
4. Contrastar cada OA con fuentes curriculares oficiales y generar una matriz reproducible de cobertura.
5. Comparar semánticamente Forma A y Forma B para verificar que las afirmaciones de “preguntas distintas” sean ciertas.
6. Verificar recursos visuales y tablas en la interfaz real; un marcador textual no prueba que la imagen esté disponible.

## Estado
**5.º básico: primera pasada preliminar ampliada a evaluaciones; no cerrada ni certificada.** El desajuste de puntaje del examen de Historia es el hallazgo prioritario de esta entrega. El documento se registra como diagnóstico; no se corrigen todavía los archivos fuente.
