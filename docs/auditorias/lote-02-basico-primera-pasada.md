# Auditoría sustantiva por lote — 2.º básico (primera pasada)

**Fecha:** 21 de octubre de 2026  
**Rama:** `qa/fase-2-matriz-trazabilidad`  
**Alcance revisado en este lote:** lectura directa de las cuatro guías principales de 2.º básico:
- `contenido/02-basico/lenguaje-y-comunicacion.md`
- `contenido/02-basico/matematica.md`
- `contenido/02-basico/ciencias-naturales.md`
- `contenido/02-basico/historia-geografia-y-cs-sociales.md`

**Limitación:** revisión de primera pasada sobre el contenido textual inspeccionado. No es una certificación completa de las cuatro guías, ni de todos los bancos, pruebas y exámenes del curso. No se modificó el contenido fuente.

## Resumen del lote

| Guía | Resultado de esta pasada | Estado |
|---|---|---|
| Lenguaje y Comunicación | Detectada una afirmación potencialmente incorrecta sobre los colores de contenedores de reciclaje en Chile | Hallazgo por verificar con norma/fuente local |
| Matemática | En los fragmentos revisados, las respuestas y retroalimentaciones de los ejemplos de lectura y comparación numérica examinados son coherentes | Revisión parcial; resto pendiente |
| Ciencias Naturales | Detectada una generalización taxonómica absoluta sobre mamíferos que requiere precisión | Hallazgo confirmado a nivel científico general; ajustar al objetivo y edad |
| Historia, Geografía y Ciencias Sociales | Detectada una síntesis amplia de roles de género en pueblos originarios; requiere fuente específica y tratamiento más contextualizado | Hallazgo pedagógico probable, no error factual confirmado |

## Hallazgos

### LGS-2B-LEN-001 — Colores de contenedores: atribución de latas al amarillo

- **Archivo:** `contenido/02-basico/lenguaje-y-comunicacion.md`
- **Ubicación:** texto no literario “El reciclaje en la escuela”.
- **Fragmento:** “El contenedor amarillo es para los plásticos y las latas.”
- **Tipo:** exactitud factual / contextualización chilena.
- **Prioridad provisional:** P2 (importante; puede enseñar una regla práctica equivocada).
- **Evidencia observada:** el material presenta los colores como regla general para escuelas de Chile, pero agrupa plásticos y latas en amarillo. La separación por colores depende de la norma y del sistema local; en la codificación de reciclaje usada comúnmente en Chile, papel/cartón se identifica con azul, plásticos con amarillo y metales con gris. No debe afirmarse que las latas van siempre al amarillo sin precisar la norma/sistema.
- **Recomendación:** verificar contra la versión vigente de la norma chilena de colores y/o instrucción oficial del sistema local. Reformular, por ejemplo: “El color puede variar según el sistema de reciclaje; revisa el símbolo y las instrucciones del punto limpio. En el código de colores de referencia, el amarillo se usa para plásticos y el gris para metales”. No aplicar el cambio hasta guardar la fuente oficial exacta.
- **Prueba de cierre:** la afirmación corregida coincide con una fuente normativa/oficial y no generaliza un esquema local a todas las escuelas.

### LGS-2B-CIEN-001 — “Solo los mamíferos” como regla absoluta sobre desarrollo

- **Archivo:** `contenido/02-basico/ciencias-naturales.md`
- **Ubicación:** OA 3, preguntas de autoevaluación 2 y 3 y sus retroalimentaciones.
- **Fragmentos:** “Recuerda que solo los mamíferos crecen dentro del cuerpo de su madre” y “Los mamíferos crecen dentro del cuerpo de la madre”.
- **Tipo:** exactitud científica / formulación demasiado absoluta.
- **Prioridad provisional:** P2.
- **Evidencia observada:** la mayoría de los mamíferos son vivíparos, pero los monotremas (por ejemplo, ornitorrinco y equidnas) ponen huevos. Por tanto, no es correcto describir a todos los mamíferos como animales que necesariamente crecen dentro del cuerpo materno y nacen vivos. El ejemplo de guanaco y zorro sí es adecuado para el contexto local, pero la regla universal no.
- **Recomendación:** conservar el ejemplo local y acotar: “Muchos mamíferos, como el guanaco y el zorro, se desarrollan dentro del cuerpo de la madre y nacen vivos. En cambio, aves, anfibios y muchos insectos nacen de huevos”. Para 2.º básico, no es necesario introducir monotremas en detalle; basta evitar “todos/solo” como universal si no se enseña la excepción.
- **Prueba de cierre:** la explicación y las claves siguen siendo adecuadas al OA y ya no afirman una regla universal falsa.

### LGS-2B-HIST-001 — Generalización sobre roles de género de pueblos originarios

- **Archivo:** `contenido/02-basico/historia-geografia-y-cs-sociales.md`
- **Ubicación:** OA 1, párrafo sobre roles de hombres y mujeres.
- **Fragmento:** “En general, hombres y mujeres tenían roles distintos pero complementarios”, seguido de ejemplos amplios sobre caza, pesca, agricultura, tejido, cocina y cuidado infantil.
- **Tipo:** rigor histórico / inclusión / simplificación cultural.
- **Prioridad provisional:** P2, sujeto a revisión especializada.
- **Evidencia observada:** el párrafo reconoce que había variación entre pueblos, lo cual es positivo; aun así, reúne sociedades distintas en una generalización binaria y no cita ejemplos por pueblo ni fuentes. El OA pide describir modos de vida, incluyendo roles de hombres y mujeres; la síntesis necesita evidencia específica y evitar presentar una división uniforme.
- **Recomendación:** aportar ejemplos contextualizados por pueblo y período, atribuidos a una fuente confiable, y redactar como patrones documentados que variaban entre comunidades, no como regla común a todos los pueblos originarios.
- **Prueba de cierre:** cada ejemplo tiene respaldo histórico/educativo y la redacción deja explícita la diversidad cultural y temporal.

## Observaciones sin hallazgo confirmado en esta pasada

### Matemática — 2.º básico

En los fragmentos iniciales revisados:
- 47 se lee “cuarenta y siete”; 68 “sesenta y ocho”; 92 “noventa y dos”.
- 8 decenas y 3 unidades representan 83.
- 84 es mayor que 79.
- Dos monedas de $50 equivalen a una moneda de $100.
- Los órdenes ascendente y descendente examinados tienen claves coherentes.

Esto solo certifica esos ejemplos/preguntas concretos, no la guía completa ni los 13 OA. La revisión de las secciones restantes, preguntas abiertas, gráficos, medición, geometría, patrones y claves debe continuar.

### Lenguaje y Comunicación — 2.º básico

Las explicaciones inspeccionadas sobre “cielo” como “cie-lo”, “leemos” como “le-e-mos”, grupos consonánticos y las claves del cuento “La fiesta sorpresa de Emilia” parecen coherentes en los ejemplos observados. La guía completa y los ejercicios no inspeccionados siguen pendientes.

## Siguiente lote recomendado

1. Verificar LGS-2B-LEN-001 contra una fuente normativa/oficial chilena antes de confirmarlo definitivamente.
2. Revisar los apartados restantes de las cuatro guías de 2.º básico y sus bancos de preguntas.
3. Inspeccionar los archivos de pruebas de unidad y simulacros del curso, comparando enunciados, claves y pautas.
4. Registrar cada pregunta examinada con identificador, resultado y evidencia; no inferir que un documento completo está validado por una muestra.

## Estado de cierre

**Lote parcialmente completado.** Se registran dos hallazgos sustantivos (uno científico y uno contextual de reciclaje pendiente de fuente primaria) y una observación pedagógico-histórica que requiere investigación. No se modificó el contenido educativo. La auditoría integral de 2.º básico y la auditoría global de los 12 cursos permanecen abiertas.
