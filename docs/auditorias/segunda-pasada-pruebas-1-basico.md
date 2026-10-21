# Segunda pasada — pruebas y simulacros de 1° básico

**Rama:** `qa/fase-2-matriz-trazabilidad`  
**Archivos inspeccionados en esta pasada:** 14 archivos de pruebas de unidad y dos simulacros integrados (Forma A y Forma B), además de volver a comprobar las claves y metadatos de los simulacros.  
**Método:** inspección estática del contenido recuperado desde GitHub. No se ejecutaron tests de aplicación ni se verificó el temario oficial completo en esta pasada.

## Verificaciones positivas

- Los simulacros Forma A y Forma B contienen 20 preguntas cada uno y una pauta de corrección numerada del 1 al 20.
- Ambos declaran 5 preguntas por asignatura para Lenguaje, Matemática, Ciencias Naturales e Historia/Geografía/Ciencias Sociales.
- La Forma A usa tres alternativas en las preguntas de selección múltiple mostradas en el archivo; también incluye preguntas de respuesta breve, como indican sus instrucciones.
- La prueba de unidad de Matemática — Números y Operaciones declara 8 preguntas y contiene 8 ítems con una pauta de respuesta correspondiente.
- La prueba de unidad de Matemática — Geometría declara 6 preguntas y contiene 6 ítems con pauta.

Estas verificaciones de estructura no equivalen a una certificación de validez curricular ni de todas las claves.

## Nuevos hallazgos

| ID | Archivo / ubicación | Evidencia observada | Riesgo | Severidad provisional | Acción recomendada |
|---|---|---|---|---|---|
| LS-1B-CN-EXA-001 | `contenido/01-basico/examenes/examen-integrado-forma-a.md`, pregunta 13, cuento “Pepa y el gato perdido” | El relato indica que Pepa encuentra un gato mojado y “Le dio leche tibia”. | Puede transmitir a niños la idea de que la leche de vaca es una bebida apropiada para gatos. Muchos gatos no toleran bien la lactosa y la leche no es necesaria como cuidado general. El problema no es la ficción en sí, sino presentar la acción como cuidado positivo sin matiz. | **P2 — Medio**, por ser un ejemplo incidental pero educativo | Cambiar por agua limpia y un lugar cálido/seguro, o explicitar que un animal encontrado debe recibir ayuda de un adulto y, si está enfermo, de un veterinario. Revisar las demás historias para evitar consejos accidentales de cuidado animal o seguridad. |
| LS-1B-EXAM-001 | Simulacros Forma A/B | La instrucción de cada prueba dice “3 opciones” para alternativas; el formato incluye además respuestas breves y una pregunta de escritura abierta. | La redacción puede interpretarse como si todas las preguntas tuvieran tres opciones, aunque la intención parece referirse solo a las preguntas de alternativas. | **P3 — Bajo** | Ajustar a “Las preguntas de selección múltiple tienen tres alternativas; también hay preguntas de respuesta breve o abierta”. Revisar la coherencia de instrucciones y metadatos en los 12 cursos. |
| LS-1B-CUR-001 | Pruebas de unidad de 1° básico, metadatos | Los archivos de Matemática declaran una cantidad de preguntas en YAML; otros archivos de unidad no siempre declaran el mismo campo. | El inventario automatizado podría no poder verificar uniformemente la cantidad de ítems por unidad si faltan metadatos o si se usan formatos distintos. | **P3 — Bajo**, hallazgo de trazabilidad, no error de aprendizaje confirmado | Estandarizar metadatos (cantidad de preguntas, OA, duración y fuente) y comprobar que coincidan con los ítems reales y su pauta. |

## Límites de la revisión

- No se han comprobado todas las respuestas de los 14 bancos de unidad una por una frente a cada enunciado.
- No se ha realizado aún el cotejo completo de cada OA con la fuente oficial vigente.
- La frase sobre leche se registra como riesgo de consejo incidental, no como conclusión de que el material enseñe explícitamente nutrición animal.
- Los niveles P2/P3 son provisionales y pueden cambiar tras la revisión completa.

## Próximas acciones

1. Revisar la correspondencia enunciado–clave–retroalimentación en todos los ítems de las pruebas y simulacros.
2. Comprobar que Forma A y Forma B midan objetivos comparables sin repetir las mismas preguntas ni introducir claves ambiguas.
3. Revisar el nivel lector y la duración propuesta de cada instrumento para 1° básico.
4. Contrastar cobertura y redacción de OA con las fuentes oficiales aplicables.
5. Continuar con 2° básico manteniendo el mismo registro de evidencias y severidad.
