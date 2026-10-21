# Auditoría preliminar de contenido principal — 3.º medio

**Rama:** `qa/fase-2-matriz-trazabilidad`  
**Alcance:** primera pasada de las seis guías principales existentes para 3.º medio: Matemática, Lengua y Literatura, Ciencias para la Ciudadanía, Filosofía, Inglés y Educación Ciudadana. Se revisaron fragmentos representativos de conceptos y retroalimentación. No se verificaron exhaustivamente todos los ítems ni la cobertura de OA oficiales. No se modificó contenido fuente ni `main`.

## Observaciones para seguimiento

### LGS-3M-MAT-001 — Especificar si la varianza se calcula como poblacional o muestral
- **Severidad provisional:** P2 (precisión matemática y reproducibilidad).
- **Archivo:** `contenido/03-medio/matematica.md`.
- **Punto de control:** los ejercicios de varianza deben declarar si los datos corresponden a toda la población o a una muestra.
- **Evaluación:** la elección afecta el divisor de la fórmula (n o n−1) y, por tanto, el resultado numérico. Sin esa convención, dos procedimientos distintos pueden parecer contradictorios.
- **Recomendación:** verificar cada ejemplo, respuesta esperada y retroalimentación de estadística; explicitar la convención y el motivo.

### LGS-3M-CIUD-001 — Evitar que ejemplos de bienestar reduzcan problemas de salud a una sola dimensión
- **Severidad provisional:** P3 (enfoque biopsicosocial y lectura de casos).
- **Archivo:** `contenido/03-medio/ciencias-para-la-ciudadania.md`.
- **Evidencia:** la guía indica que un mismo problema de salud casi siempre combina dimensiones y presenta preguntas sobre factores ambientales, como radiación UV.
- **Evaluación:** el enfoque multifactorial es adecuado como marco general. La auditoría completa debe comprobar que las preguntas de alternativa no contradigan ese marco presentando causas complejas como exclusivamente genéticas, ambientales o individuales cuando el caso no lo justifique.
- **Recomendación:** revisar cada caso y distractor según la evidencia proporcionada en el enunciado, no por una regla universal.

### LGS-3M-LEN-001 — Verificar atribución y contexto de textos literarios
- **Severidad provisional:** P3 (trazabilidad textual).
- **Archivo:** `contenido/03-medio/lengua-y-literatura.md`.
- **Evidencia:** se presenta “Las manos de mi padre” como fragmento de cuento.
- **Evaluación:** la muestra es compatible con una lectura literaria sobre trabajo minero, familia y metáfora. La revisión debe comprobar si es creación didáctica o texto publicado, y señalarlo de forma transparente.
- **Recomendación:** registrar autoría y procedencia de cada lectura, así como cualquier adaptación.

### LGS-3M-FILO-001 — Asegurar que las respuestas filosóficas se evalúen por razones y argumentos
- **Severidad provisional:** P3 (criterios de evaluación).
- **Archivo:** `contenido/03-medio/filosofia.md`.
- **Evidencia:** los ejemplos distinguen una opinión no examinada de una postura fundamentada y mencionan a Platón y Aristóteles.
- **Evaluación:** el enfoque es pertinente; falta comprobar que las claves no reduzcan cuestiones filosóficas debatibles a una única postura moral sin argumentación.
- **Recomendación:** para preguntas abiertas, definir criterios de coherencia, razones, uso de conceptos y consideración de objeciones, sin exigir que el estudiante adopte una conclusión predeterminada.

## Comprobaciones de muestra

- Matemática: el factor 0,85 está entre 0 y 1, por lo que un modelo exponencial con ese factor representa decrecimiento.
- Educación Ciudadana: la respuesta que rechaza la superioridad de un partido como fundamento democrático concuerda con la explicación visible sobre soberanía popular y pluralismo.
- Ciencias para la Ciudadanía: la muestra de radiación UV como factor del entorno físico es coherente con la retroalimentación visible.
- Estas comprobaciones son puntuales y no certifican todas las preguntas.

## Pendientes para completar 3.º medio

1. Revisar todos los cálculos y criterios estadísticos, incluyendo varianza, supuestos y redondeo.
2. Auditar claves, distractores, puntajes y retroalimentaciones de las seis asignaturas.
3. Verificar la atribución de textos, noticias, casos y materiales de lectura.
4. Comprobar que las evaluaciones de Filosofía valoren argumentos y no solo coincidencia con una respuesta cerrada.
5. Trazar cada OA oficial a explicación, ejemplos, práctica y evaluación.
6. Revisar exámenes y pruebas por asignatura, su disponibilidad y equivalencia entre formas.

## Estado
**3.º medio: primera pasada preliminar documentada; auditoría parcial y abierta.** Los puntos de estadística, salud y evaluación filosófica quedan como verificaciones prioritarias; no se declaran errores definitivos sin contrastar los ejercicios completos. No se modificaron los archivos fuente.
