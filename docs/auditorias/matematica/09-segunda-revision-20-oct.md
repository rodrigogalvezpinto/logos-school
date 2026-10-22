# Segunda revisión de auditoría — Matemática de Logos School

**Fecha:** 20 de octubre de 2026  
**Repositorio revisado:** `rodrigogalvezpinto/logos-school`  
**Alcance:** segunda lectura de los 12 archivos Markdown de Matemática; recuento reproducible de estructura, revisión dirigida de casos señalados y comprobaciones aritméticas puntuales.  
**Estado:** diagnóstico actualizado; todavía no equivale a una certificación exhaustiva de cada cálculo ni a una prueba de la interfaz desplegada.

## 1. Conclusión ejecutiva

La segunda revisión confirma que hay motivos válidos para mejorar la experiencia pedagógica y que existe al menos un defecto editorial concreto y un caso de reparto que requiere aclaración. También detectó dos imprecisiones en el informe anterior: el archivo de 4.º básico tiene **14**, no 15, secciones «Ejemplos resueltos»; y el archivo de 1.º básico contiene **6** imágenes Markdown, no una. Estos recuentos corregidos sustituyen los del primer informe.

No encontré, en las comprobaciones puntuales hechas en esta segunda pasada, una base suficiente para afirmar que existan errores matemáticos generalizados en los 12 cursos. Tampoco sería correcto afirmar que todos los ejercicios están correctos: esa verificación requiere revisar cada solución, pregunta y alternativa una por una.

## 2. Inventario corregido

Los recuentos se calcularon directamente sobre el contenido actual recuperado del repositorio. «Palabras» cuenta tokens separados por espacios en el Markdown fuente; no equivale a la cantidad de texto que el alumno ve en pantalla.

| Curso | Palabras aprox. | Líneas | OA | Secciones de ejemplos | Secciones de autoevaluación | Imágenes Markdown |
|---|---:|---:|---:|---:|---:|---:|
| 1.º básico | 6.029 | 841 | 10 | 10 | 10 | 6 |
| 2.º básico | 8.368 | 998 | 13 | 13 | 13 | 0 |
| 3.º básico | 8.520 | 1.013 | 13 | 13 | 13 | 0 |
| 4.º básico | 9.100 | 1.085 | 14 | 14 | 14 | 0 |
| 5.º básico | 12.158 | 1.237 | 17 | 17 | 17 | 0 |
| 6.º básico | 8.556 | 775 | 11 | 11 | 11 | 0 |
| 7.º básico | 8.636 | 779 | 9 | 9 | 9 | 0 |
| 8.º básico | 10.457 | 850 | 10 | 10 | 10 | 0 |
| 1.º medio | 7.900 | 671 | 7 | 7 | 7 | 0 |
| 2.º medio | 7.272 | 621 | 6 | 6 | 6 | 0 |
| 3.º medio | 7.324 | 529 | 3 | 3 | 3 | 0 |
| 4.º medio | 8.962 | 523 | 3 | 3 | 3 | 0 |
| **Total** | **103.282** | **9.922** | **116** | **116** | **116** | **6** |

### Interpretación de los datos

- La plantilla es muy consistente: cada OA identificado tiene una sección de ejemplos y una de autoevaluación. Esto ayuda a la navegación, aunque conviene que la actividad y el tipo de explicación se adapten al objetivo en vez de repetir siempre la misma fórmula.
- 5.º básico es el archivo más extenso por palabras y líneas. 1.º y 2.º básico también requieren atención especial a la carga de lectura, pero el volumen del Markdown por sí solo no prueba que la interfaz sea demasiado densa.
- La fuente de 1.º básico incluye seis imágenes Markdown. Los otros archivos no incluyen imágenes con esa sintaxis; sí pueden contener tablas, fórmulas o componentes propios de la aplicación. Esto no permite concluir por sí solo que carezcan de recursos visuales.
- Los archivos de 3.º y 4.º medio tienen tres OA cada uno. Eso no demuestra falta de cobertura: los temarios de validación seleccionan objetivos específicos. Hay que contrastar el contenido con el temario oficial exacto aplicable a cada nivel y año.

## 3. Hallazgos de segunda revisión

### H-01 — Reparto de cajas con resto no explicado
**Curso:** 6.º básico  
**Ubicación:** `contenido/06-basico/matematica.md`, alrededor de la línea 84.

El ejercicio indica que hay 24.600 botellas, con 12 por caja, para repartir las cajas entre 3 distribuidores. El texto calcula correctamente:

- 24.600 ÷ 12 = 2.050 cajas.
- 2.050 ÷ 3 = 683 cajas por distribuidor, con **1 caja sobrante**.

La retroalimentación original dice aproximadamente «683 cajas cada uno» y omite qué sucede con la caja restante. El cálculo aproximado no es incorrecto, pero la situación queda incompleta si el reparto debe ser exacto.

**Corrección recomendada:** «Se obtienen 2.050 cajas. Al repartirlas entre 3 distribuidores, cada uno recibe 683 cajas y queda 1 caja sin repartir (porque 683 × 3 = 2.049)». Alternativamente, cambiar el dato inicial si el objetivo es que no haya resto.

**Clasificación:** mejora/corrección pedagógica confirmada; prioridad media.

### H-02 — Texto editorial dentro de la respuesta esperada
**Curso:** 6.º básico  
**Ubicación:** `contenido/06-basico/matematica.md`, alrededor de la línea 152.

La respuesta incluye la frase «cuidado con el orden» dentro de una solución que el estudiante podría leer como respuesta modelo. La razón final es correcta: cuentos:ciencia = 5:3; si hay 15 libros de cuentos, el factor es 3 y corresponden 9 libros de ciencia. La redacción intermedia mezcla una advertencia editorial con la operación.

**Corrección recomendada:** «La razón cuentos:ciencia es 5:3. Si 5 partes corresponden a 15 libros de cuentos, cada parte vale 15 ÷ 5 = 3. Entonces, los libros de ciencia son 3 × 3 = 9».

**Clasificación:** defecto editorial confirmado; prioridad media.

### H-03 — El informe anterior tenía dos recuentos equivocados
- **4.º básico:** el conteo reproducido ahora da 14 encabezados «Ejemplos resueltos», igual que los 14 OA. La afirmación anterior de que había 15 fue un error de conteo y queda retirada.
- **1.º básico:** el archivo contiene seis referencias Markdown a imágenes. La afirmación anterior de que se detectó una sola imagen fue incorrecta. Esto no verifica si las rutas existen ni si cargan en producción.

**Clasificación:** correcciones del propio informe; resueltas en esta versión.

### H-04 — Posible exceso de texto y plantilla repetida
Los 12 archivos repiten secciones de explicación, ejemplos y autoevaluación por OA. Es una estructura útil para mantener consistencia, pero en cursos iniciales debe comprobarse si cada bloque es legible, visual y adecuado a la edad. Los archivos más largos son 5.º básico (12.158 palabras), 8.º básico (10.457) y 4.º básico (9.100), mientras 1.º básico contiene 6.029 palabras.

**No es un error confirmado de contenido.** La densidad real debe evaluarse en la interfaz, midiendo el texto visible por pantalla, el uso de imágenes, el tamaño de los párrafos y la secuencia de interacción.

**Clasificación:** riesgo pedagógico por validar; prioridad alta para 1.º–2.º básico y alta para revisar 5.º básico por extensión.

### H-05 — Las respuestas están en el mismo documento fuente que las preguntas
En los archivos revisados, las respuestas y la retroalimentación aparecen después de las preguntas dentro del Markdown. Eso es adecuado si la aplicación las oculta hasta que el estudiante responde; si el renderizado muestra todo de inmediato, se pierde parte del valor de la autoevaluación.

**No está confirmado que la aplicación las muestre prematuramente.** Es una verificación de interfaz, no una conclusión que pueda extraerse solo del archivo.

**Clasificación:** riesgo funcional/pedagógico pendiente de prueba en la aplicación.

### H-06 — Supuestos estadísticos que conviene explicitar
En 3.º medio, el ejemplo de dispersión calcula varianza como suma de desviaciones al cuadrado dividida por el número de datos (`n`): 10/5 = 2 y 160/5 = 32. Los cálculos son correctos si se trata a los cinco valores como la población de interés. Si se pretendiera estimar la varianza de una población a partir de una muestra, la fórmula muestral suele usar `n−1`.

**Corrección recomendada:** indicar que el ejemplo usa varianza poblacional porque considera todos los tiempos observados del ejercicio; o presentar la distinción entre varianza poblacional y muestral según el objetivo curricular.

**Clasificación:** precisión conceptual recomendada; no es un error aritmético confirmado.

## 4. Comprobaciones aritméticas puntuales realizadas

Estos ejemplos fueron recalculados manualmente en la segunda pasada. Son muestras, no una validación de todos los ejercicios.

| Curso/archivo | Comprobación | Resultado de la revisión |
|---|---|---|
| 6.º básico | 3.420 × 12.500 | 42.750.000; correcto |
| 6.º básico | 156.000 ÷ 12 | 13.000; correcto |
| 6.º básico | 45 × 185.000 − 350.000 | 7.975.000; correcto |
| 6.º básico | 24.600 ÷ 12 y luego ÷ 3 | 2.050 cajas; 683 para cada uno y sobra 1; falta explicitar el resto |
| 6.º básico | Razón 12:18 | Se simplifica a 2:3; correcto |
| 6.º básico | Razón 5:2 con 20 autos | 8 motos; correcto |
| 6.º básico | Razón 5:3 con 15 libros de cuentos | 9 libros de ciencia; resultado correcto, redacción editorial mejorable |
| 3.º medio | Varianzas 10/5 y 160/5 | 2 y 32; aritméticamente correctas bajo convención poblacional |
| 3.º medio | P(enfermo y positivo) = 0,02 × 0,90 | 0,018 = 1,8%; correcto |
| 4.º medio | Interés simple: $500.000 al 6% por 3 años | $590.000; correcto |
| 4.º medio | Interés compuesto: $500.000 al 6% por 3 años | Aproximadamente $595.508; correcto |
| 4.º medio | TEA de 24% nominal capitalizada mensualmente | Aproximadamente 26,82%; correcto |
| 4.º medio | $2.000.000 al 4% compuesto por 6 años | Aproximadamente $2.530.600; correcto por redondeo |
| 4.º básico | 450 cm a metros | 4,5 m; correcto |
| 5.º básico | Promedio de 5 datos 8, 10, 12, 6, 9 | 9; correcto |

## 5. Qué sigue sin estar certificado

Esta segunda revisión **no** permite afirmar que:

1. Se haya recalculado cada solución de los 116 OA y todas sus preguntas, alternativas y retroalimentaciones.
2. Se haya comparado cada OA con el PDF oficial exacto de su curso y convocatoria.
3. Se haya verificado que todas las imágenes, fórmulas y rutas de recursos cargan en producción.
4. Se haya comprobado el comportamiento real de la autoevaluación en la interfaz.
5. Se haya medido la carga de lectura desde el punto de vista de un estudiante en pantalla.

Por lo tanto, el informe debe considerarse una **auditoría estructural con verificación matemática por muestreo y hallazgos concretos**, no una certificación completa del contenido.

## 6. Plan recomendado para cerrar la auditoría

1. **Prueba de interfaz:** revisar una página real por curso y confirmar cómo se muestran preguntas, respuestas, tablas, fórmulas e imágenes.
2. **Auditoría matemática exhaustiva:** crear una matriz por OA con cada ejemplo, pregunta, opción correcta y retroalimentación; recalcular todos los resultados y marcar cada elemento como correcto, incorrecto o ambiguo.
3. **Auditoría curricular:** comparar los 12 archivos con los temarios oficiales de validación correspondientes, distinguiendo objetivos exigidos, objetivos incluidos y contenido adicional.
4. **Auditoría pedagógica:** evaluar edad, carga de lectura, progresión, ejemplos concretos, práctica guiada, variedad y accesibilidad visual.
5. **Informe final:** priorizar por severidad y probabilidad de afectar el aprendizaje; corregir solo después de aprobar los hallazgos.

## 7. Fuentes oficiales para la validación curricular

- Mineduc / EPJA, información sobre los temarios de Exámenes Libres para menores de 18 años: https://epja.mineduc.cl/validacion-de-estudios/examenes-libres-menores-de-18-anos/cuales-son-los-temarios-que-se-utilizaran-en-la-examinacion/
- Currículum Nacional, Matemática 1.º básico: https://www.curriculumnacional.cl/curriculum/1o-6o-basico/matematica/1-basico
- Currículum Nacional, Matemática 4.º básico: https://www.curriculumnacional.cl/curriculum/1o-6o-basico/matematica/4-basico
- Currículum Nacional, Matemática 1.º medio: https://www.curriculumnacional.cl/curriculum/7o-basico-2o-medio/matematica/1-medio
- Currículum Nacional, Matemática 4.º medio, Formación General: https://www.curriculumnacional.cl/curriculum/3o-4o-medio/matematica-4o-medio/4-medio-fg

**Importante:** las páginas curriculares son referencias para orientar la comparación. Para dar por validado cada curso, debe cotejarse contra el temario oficial exacto aplicable a la examinación de ese nivel.

---
**Integridad del trabajo:** esta segunda revisión fue de solo lectura. No se modificó ningún archivo del repositorio ni se publicó ningún cambio.