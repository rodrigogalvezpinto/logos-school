# Auditoría de evaluaciones de 2.º básico — tercera pasada

**Rama:** `qa/fase-2-matriz-trazabilidad`  
**Alcance de esta pasada:** revisión directa de las 12 pruebas de unidad listadas en `contenido/02-basico/pruebas/` y los dos simulacros integrados (`Forma A` y `Forma B`).  
**Límite:** revisión documental de contenido, consistencia pregunta-pauta y diseño; no se ejecutaron las pruebas en la aplicación ni se certificó alineación OA completa con documentos oficiales. No se modificó contenido fuente ni se tocó `main`.

## Hallazgos que requieren atención

### LGS-2B-EVAL-001 — Forma B afirma ser distinta, pero repite preguntas/contenidos casi idénticos a Forma A
- **Severidad provisional:** P2 (validez del segundo simulacro).
- **Evidencia:** ambas formas preguntan por diptongo con “cielo”; por la fiesta de Emilia y dónde vive; por el huemul; por el pueblo mapuche/ruka; por Argentina como frontera oriental más larga; por el agua que toma la forma del recipiente; por el ciclo del agua; por oración con mayúscula y punto; por pictograma con 4 pelotas × 3 goles en Forma A (el tema de pictogramas se repite en Forma B con otro dato); y por vías de evacuación. Además, Forma B repite casi literalmente varios ítems de las pruebas de unidad.
- **Impacto:** reduce la independencia entre simulacros y facilita memorizar respuestas, pese a que el encabezado promete un banco distinto.
- **Recomendación:** comparar semánticamente Forma A/B y asignar a cada ítem un identificador de origen; decidir si la intención es practicar objetivos comunes o evaluar con banco realmente alternativo. Ajustar la declaración del encabezado o reemplazar duplicados.

### LGS-2B-EVAL-002 — Clasificación histórica presupone que los pueblos indígenas precolombinos vivían exclusivamente en el campo
- **Severidad provisional:** P2 (representación histórica/cultural).
- **Evidencia:** en `historia-unidad-historia.md`, pregunta 4, se pide clasificar “Vivir exclusivamente en el campo, sin ciudades” como algo que “ha cambiado” respecto del período precolombino.
- **Problema:** la frase introduce como supuesto una condición uniforme para pueblos diversos y convierte una generalización en respuesta evaluable.
- **Recomendación:** eliminar esa alternativa o sustituirla por un cambio histórico concreto, contextualizado por pueblo y período, con fuente.

### LGS-2B-EVAL-003 — Pauta de Ciencias presenta como universal que los mamíferos no nacen de huevos
- **Severidad provisional:** P2 (precisión científica).
- **Evidencia:** en `ciencias-naturales-unidad-ciencias-de-la-vida.md`, pregunta 2, el enunciado generaliza sobre mamíferos y la pauta afirma que estos no salen de un huevo.
- **Problema:** existen mamíferos ovíparos (monotremas). Los ejemplos del enunciado incluyen guanaco y zorro chilla, pero la pauta amplía la afirmación a todos los mamíferos.
- **Recomendación:** restringir la afirmación a los animales concretos trabajados en el nivel o enseñar la excepción con un nivel de detalle adecuado. Evitar una regla universal falsa.

### LGS-2B-EVAL-004 — Ítem de evaporación usa una explicación causal demasiado cerrada
- **Severidad provisional:** P3 (precisión científica/pedagógica).
- **Evidencia:** en `ciencias-naturales-unidad-tierra-y-universo.md`, pregunta 5, la pauta atribuye que el charco desaparece al calor del día y afirma que el agua “subió al aire”.
- **Problema:** el fenómeno descrito es compatible con evaporación, pero el enunciado no controla otras condiciones (drenaje, absorción, limpieza) y la explicación podría enseñar que el calor es siempre la única causa.
- **Recomendación:** contextualizar explícitamente que el charco se evapora por el calor/energía del entorno, o formularlo como inferencia probable dentro de una actividad sobre evaporación.

### LGS-2B-EVAL-005 — Ítem de prueba depende de un gráfico que no está reproducido en el texto fuente
- **Severidad provisional:** P2 si el gráfico no se adjunta en la interfaz; P3 si se presenta correctamente como recurso visual.
- **Evidencia:** `matematica-unidad-medicion-datos-probabilidades.md`, preguntas 7 y 8, remiten a “ese mismo gráfico” y a alturas de barras, pero el Markdown inspeccionado no contiene el gráfico ni una tabla de datos.
- **Impacto:** la pregunta no es autónoma y podría ser imposible de responder si el recurso visual no se renderiza por separado.
- **Recomendación:** verificar el renderizado real; incluir imagen/tabla accesible o incorporar los datos al enunciado.

### LGS-2B-EVAL-006 — Categoría de vapor de agua puede inducir una concepción confusa
- **Severidad provisional:** P3.
- **Evidencia:** en `ciencias-naturales-unidad-fisicas-y-quimicas.md`, pregunta 4 y pauta, el vapor de agua se describe como “invisible y se mezcla con el aire”.
- **Problema:** es una simplificación habitual, pero puede confundirse el vapor de agua gaseoso invisible con la nube visible de gotitas condensadas.
- **Recomendación:** añadir una distinción breve entre vapor invisible y gotitas visibles de una nube, si el objetivo curricular lo permite.

## Comprobaciones satisfactorias en esta muestra

- En las pautas examinadas, las operaciones explícitas 45 + 32 = 77; 96 − 42 = 54; 8 + 5 = 13, y 15 − 6 = 9 son correctas.
- La secuencia del ciclo del agua (evaporación → condensación → precipitación) y la correspondencia entre recipientes y forma del agua son consistentes con los enunciados.
- Las preguntas de comprensión de “La fiesta sorpresa de Emilia” y de la carta de Matías tienen claves que coinciden con el texto presentado.
- Las pautas de ambas formas integradas distribuyen 5 preguntas por cada una de las cuatro asignaturas, para un total de 20 ítems. Esto verifica la distribución declarada, no la cobertura curricular completa.

## Pendientes para cerrar 2.º básico

1. Revisar exhaustivamente todas las preguntas y pautas de cada prueba, con una matriz pregunta → OA → fuente de contenido → respuesta → retroalimentación.
2. Verificar si los recursos visuales descritos entre corchetes existen realmente y son accesibles en la aplicación.
3. Comparar la cobertura OA con Bases Curriculares y programas oficiales vigentes, distinguiendo contenido existente de alineación demostrada.
4. Validar afirmaciones científicas e históricas/culturales con fuentes oficiales o especializadas.
5. Hacer análisis de duplicados entre bancos, pruebas de unidad y Formas A/B.
6. Mantener todos los hallazgos como pendientes hasta que se corrijan en una fase posterior; este informe no autoriza cambios en los archivos fuente.

## Estado
**2.º básico: auditoría parcial, ampliada a pruebas de unidad y simulacros; no certificada ni cerrada.** La pasada identificó riesgos concretos, pero no equivale a validar integralmente cada ítem, recurso visual, OA o comportamiento de la aplicación.
