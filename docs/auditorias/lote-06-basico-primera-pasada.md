# Auditoría preliminar de contenido y evaluaciones — 6.º básico

**Rama:** `qa/fase-2-matriz-trazabilidad`  
**Alcance:** inspección inicial de las cinco guías principales y revisión estructural de las pruebas de unidad y exámenes Forma B disponibles. Se verificaron ejemplos aritméticos visibles y afirmaciones que requieren precisión. No es una auditoría exhaustiva pregunta por pregunta, no certifica cobertura oficial de OA y no incluye ejecución de la aplicación. No se modificó contenido fuente ni `main`.

## Hallazgos

### LGS-6B-MAT-001 — El reparto de cajas omite el resto y puede sugerir una distribución exacta
- **Severidad:** P1 (exactitud de la respuesta esperada y significado del problema).
- **Archivo:** `contenido/06-basico/matematica.md`, OA 2, pregunta sobre 24.600 botellas embaladas en cajas de 12 y distribuidas entre 3 distribuidores.
- **Evidencia:** la guía calcula 24.600 ÷ 12 = 2.050 cajas y luego 2.050 ÷ 3 ≈ 683 cajas por distribuidor.
- **Comprobación:** 2.050 ÷ 3 = 683 con resto 1. La respuesta “683 cajas cada uno” no distribuye todas las cajas: quedarían una caja sin asignar.
- **Impacto:** si el problema exige repartir todas las cajas, debe indicarse qué ocurre con la caja sobrante o cambiar el dato para que el reparto sea exacto. La aproximación no es suficiente para un reparto discreto sin explicar el resto.
- **Recomendación:** en una fase de corrección posterior, explicitar cociente y resto, por ejemplo “683 cajas para cada distribuidor y sobra 1 caja”, o modificar los datos si el objetivo es un reparto equitativo sin sobrantes.

### LGS-6B-MAT-002 — El objetivo de calculadora debe distinguir estimación, resultado exacto y redondeo
- **Severidad provisional:** P3 (claridad de estrategia).
- **Evidencia:** en la misma guía, una retroalimentación estima 3.400 × 12.500 ≈ 42.500.000 y la compara con el resultado exacto de 3.420 × 12.500 = 42.750.000.
- **Evaluación:** los valores son coherentes como estimación y resultado exacto, pero debe mantenerse visible la diferencia conceptual para que no se confundan ambos.
- **Recomendación:** etiquetar explícitamente “estimación” y “resultado exacto” y explicar por qué se redondea el primer factor.

### LGS-6B-LEN-001 — El relato histórico-literario requiere distinguir ficción didáctica de fuente histórica
- **Severidad provisional:** P2 (contextualización y alfabetización histórica).
- **Archivo:** `contenido/06-basico/lenguaje-y-comunicacion.md`.
- **Evidencia:** el texto “Manuel” sitúa a un niño de doce años trabajando en la Oficina Salitrera Humberstone en 1920 y desarrolla una escena narrativa ficticia en un contexto histórico real.
- **Evaluación:** el recurso puede funcionar como ficción ambientada en el pasado, pero conviene declarar que los personajes y el episodio son ficticios, para no confundirlos con un testimonio o documento histórico.
- **Recomendación:** añadir una nota breve de género y revisar que las condiciones laborales infantiles descritas se contextualicen con fuentes históricas si se usan como evidencia factual.

### LGS-6B-HIST-001 — La explicación de la Independencia debe mantener la pluralidad de causas
- **Severidad provisional:** P3 (profundidad histórica).
- **Archivo:** `contenido/06-basico/historia-geografia-y-cs-sociales.md`.
- **Evidencia:** la guía presenta el cautiverio de Fernando VII como causa inmediata importante y también menciona ideas ilustradas y descontento criollo.
- **Evaluación:** la muestra revisada no muestra una clave errónea; el punto de control es asegurar que el desarrollo completo no convierta la crisis monárquica en explicación única.
- **Recomendación:** mantener diferenciadas causas estructurales, circulación de ideas, tensiones sociales y detonantes políticos.

## Comprobaciones de muestra

- (3.420 × 12.500 = 42.750.000): correcto.
- (156.000 ÷ 12 = 13.000): correcto.
- (45 × 185.000 − 350.000 = 7.975.000): correcto.
- ((1.240 × 6.500) + (890 × 3.200) = 10.908.000): correcto.
- En Ciencias Naturales, la pregunta “Solo las plantas son capaces de realizar fotosíntesis” tiene clave Falso, coherente con la explicación que incluye algas y algunos microorganismos.
- En Inglés, las claves de muestra sobre `can't`, preposiciones de lugar y horas en punto concuerdan con los textos visibles.
- Las comprobaciones de muestra no sustituyen la verificación de todos los ítems, alternativas y criterios de respuesta abierta.

## Pendientes para completar 6.º básico

1. Auditar todas las preguntas, claves, retroalimentaciones y rúbricas de las cinco asignaturas.
2. Revisar las 12 pruebas de unidad disponibles y los exámenes Forma B por asignatura; verificar la disponibilidad de Forma A y la equivalencia entre formas.
3. Validar operaciones, unidades, restos y redondeos mediante una matriz reproducible.
4. Construir trazabilidad OA oficial → explicación → práctica → evaluación → clave → retroalimentación.
5. Verificar en la interfaz que tablas, gráficos e imágenes referenciadas realmente se muestren.
6. Distinguir textos literarios ficticios, adaptaciones y fuentes documentales.

## Estado
**6.º básico: primera pasada preliminar documentada; auditoría parcial y abierta.** El reparto de 2.050 cajas entre tres distribuidores es un hallazgo concreto que debe resolverse antes de considerar certificada esa pregunta. No se modificaron los archivos fuente.
