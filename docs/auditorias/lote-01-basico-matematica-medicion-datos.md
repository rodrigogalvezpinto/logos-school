# Lote de auditoría — 1.º básico, medición y datos y probabilidades

**Fecha:** 21 de octubre de 2026  
**Archivo:** `contenido/01-basico/pruebas/matematica-unidad-medicion-datos-probabilidades.md`  
**Estado:** hallazgo documental confirmado; render de la aplicación pendiente.

## Hallazgo LGS-1B-MAT-001 — Ordenar objetos sin información suficiente sobre sus longitudes

### Evidencia de la fuente

El ítem 2 indica:

> Ordena estos tres objetos de más corto a más largo: una goma de borrar, un lápiz, y una regla.

No incluye medidas, imagen, dibujo a escala, ni una condición que especifique qué goma, lápiz y regla se están comparando. La pauta declara: «Goma de borrar (más corta), lápiz, regla (más larga)».

### Por qué es un problema

La respuesta depende de los objetos concretos: existen gomas de borrar, lápices y reglas de distintos tamaños. La secuencia propuesta suele ser plausible como ejemplo escolar, pero no se deduce necesariamente de la información proporcionada. En una evaluación, el estudiante no debería tener que adivinar el tamaño de objetos no representados ni especificados.

### Clasificación provisional

- **Severidad:** P1 provisional si el ítem se puntúa como una respuesta única; debe confirmarse el impacto en la evaluación publicada.
- **Dimensión:** suficiencia del estímulo, validez del ítem y justicia de la corrección.
- **Estado:** hallazgo documental reproducido; pendiente de verificar render/importación.
- **Corrección propuesta, no aplicada:** incluir una ilustración inequívoca con los tres objetos dibujados desde un mismo punto de referencia y longitudes claramente distinguibles, o proporcionar longitudes explícitas. La pauta debe coincidir con el estímulo definitivo.

## Otros controles del archivo

| Control | Resultado |
|---|---|
| Número de preguntas declarado | 8 |
| Preguntas enumeradas | 8 |
| Respuestas de la pauta presentes | 8 |
| Coherencia numérica de respuestas cerradas | Las preguntas 1, 4, 5, 6, 7 y 8 son consistentes con sus datos textuales; la 2 tiene el hallazgo descrito; la 3 no proporciona medidas absolutas pero sí permite comparar 8 pasos con 5 pasos |
| Render de imágenes y pictogramas en la aplicación | No verificado |
| Alineación OA con fuente oficial vigente | No verificada de forma independiente |
| Revisión pedagógica completa de la prueba | Pendiente |

## Próximos pasos para cierre

1. Inspeccionar la pantalla de la pregunta en la aplicación QA y comprobar si hay un recurso gráfico adicional que no aparece en Markdown.
2. Si no existe, aprobar y aplicar una corrección al estímulo o a las medidas.
3. Verificar que la pauta y la interfaz de corrección utilicen el mismo criterio.
4. Ejecutar una prueba de regresión sobre importación, render y calificación.
5. Cotejar el OA declarado y el nivel de dificultad con la fuente curricular oficial correspondiente.

**Conclusión:** la fuente Markdown, por sí sola, no aporta información suficiente para determinar una única secuencia de longitudes. No se certifica el ítem hasta completar la comprobación técnica y corregir o justificar el estímulo.
