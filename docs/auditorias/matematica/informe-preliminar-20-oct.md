# Auditoría de Matemática — Logos School
**Fecha de revisión:** 20 de octubre de 2026  
**Repositorio:** `rodrigogalvezpinto/logos-school`  
**Alcance de este informe:** revisión estática inicial y contrastación estructural de las 12 guías de Matemática. **No equivale todavía a una certificación completa** de cada cálculo, alternativa, retroalimentación ni pantalla.

## 1. Inventario comprobado

| Curso | OA en guía | Preguntas | Líneas | Palabras aprox. |
|---|---:|---:|---:|---:|
| 1.º básico | 10 | 59 | 841 | 6.030 |
| 2.º básico | 13 | 84 | 998 | 8.369 |
| 3.º básico | 13 | 87 | 1.013 | 8.521 |
| 4.º básico | 14 | 84 | 1.085 | 9.101 |
| 5.º básico | 17 | 102 | 1.237 | 12.159 |
| 6.º básico | 11 | 66 | 775 | 8.557 |
| 7.º básico | 9 | 72 | 779 | 8.637 |
| 8.º básico | 10 | 80 | 850 | 10.458 |
| 1.º medio | 7 | 56 | 671 | 7.901 |
| 2.º medio | 6 | 57 | 621 | 7.273 |
| 3.º medio | 3 | 56 | 529 | 7.325 |
| 4.º medio | 3 | 54 | 523 | 8.963 |
| **Total** | **116** | **857** | **9.922** | **103.294** |

Los recuentos se hicieron directamente sobre los 12 Markdown de `contenido/`, usando los encabezados de OA y pregunta. Son conteos de secciones y no una evaluación de la calidad pedagógica.

## 2. Contraste estructural con los temarios

Se compararon los números de OA de cada guía con la sección de Matemática de su archivo de análisis de temario (`Temarios/analisis/01-primero-basico.md` a `12-cuarto-medio.md`).

**Resultado estructural:** coincidencia de los identificadores OA en los 12 niveles. No aparecieron OA en las guías que no estuvieran en la sección de Matemática de su temario ni OA listados en esa sección que faltaran como encabezado en la guía.

**Límite importante:** esto verifica correspondencia de identificadores, no que cada explicación, ejemplo y pregunta cubra íntegramente el indicador oficial. Tampoco reemplaza la comprobación del PDF oficial vigente de cada examen.

## 3. Hallazgos que requieren seguimiento

### MAT-UI-001 — Evaluación literal de respuestas abiertas
- **Ubicación:** `frontend/src/app/shared/evaluacion-runner/evaluacion-runner.ts`, método `esCorrectaEnAutoevaluacion()`.
- **Evidencia:** compara `respuestas()[p.id]` con `p.respuesta_correcta` mediante igualdad de cadenas después de quitar espacios externos y convertir a minúsculas.
- **Riesgo:** una respuesta abierta válida puede mostrarse como incorrecta si no reproduce literalmente el texto esperado. El problema es especialmente relevante para preguntas de desarrollo que admiten varias formulaciones.
- **Estado:** defecto confirmado por inspección estática del código; falta reproducirlo en navegador y revisar cómo el backend representa cada tipo de pregunta.
- **Acción recomendada después de cerrar la auditoría:** no autocorregir desarrollo por igualdad literal; mostrar criterios/solución orientativa o implementar una corrección específica para respuestas cerradas.

### MAT-CONT-001 — División con reparto entre tres distribuidores no explicita el resto
- **Ubicación:** `contenido/06-basico/matematica.md`, pregunta sobre 24.600 botellas, en cajas de 12 para tres distribuidores.
- **Cálculo:** 24.600 ÷ 12 = 2.050 cajas; 2.050 ÷ 3 = 683 cajas por distribuidor y **sobra 1 caja**.
- **Evidencia textual:** la retroalimentación dice “2.050 ÷ 3 ≈ 683 cajas cada uno” sin explicar el resto.
- **Riesgo:** el aproximado oculta una condición relevante del problema de reparto discreto.
- **Estado:** omisión confirmada en el texto, no error en la primera división.
- **Corrección sugerida (no aplicada):** indicar “683 cajas para cada distribuidor y queda 1 caja sin repartir”, o aclarar expresamente que se pide una aproximación.

### MAT-CONT-002 — Redacción editorial dentro de una solución
- **Ubicación:** `contenido/06-basico/matematica.md`, pregunta de razón cuentos:ciencia 5:3.
- **Evidencia:** la respuesta esperada incluye la frase “cuidado con el orden” en medio del desarrollo.
- **Cálculo:** 15 cuentos corresponden a factor 3; ciencia = 3 × 3 = 9. El resultado es correcto.
- **Riesgo:** parece una nota editorial que quedó dentro de la respuesta final y puede confundir al estudiante.
- **Estado:** defecto editorial confirmado; no es un error matemático.

### MAT-CONT-003 — Convención de varianza no explicitada
- **Ubicación:** `contenido/03-medio/matematica.md`, ejemplos y preguntas de varianza.
- **Evidencia:** se calcula varianza como suma de desviaciones cuadráticas dividida por el número total de datos (por ejemplo, para `{2, 4, 6}`, se usa `8/3 ≈ 2,67`).
- **Riesgo:** el cálculo es correcto como varianza poblacional; si se interpreta como varianza muestral, el divisor sería `n−1`. El material debe explicitar qué convención está usando.
- **Estado:** requiere aclaración contextual; no se marca como error aritmético.

## 4. Observaciones de inventario que no deben confundirse con defectos

- Hay preguntas abiertas que no tienen una “respuesta esperada” única; su ausencia no es por sí sola un defecto. En la revisión inicial, las preguntas sin clave se concentran en tareas como inventar un problema, crear un patrón o fundamentar una opinión.
- Los archivos de 1.º básico contienen seis referencias Markdown a imágenes. La revisión estática confirma las referencias, pero no confirma por sí sola que los recursos gráficos existan y carguen en la aplicación.
- La existencia de preguntas, respuestas y retroalimentaciones en Markdown no demuestra que los datos importados a la base de datos sean idénticos ni que se muestren correctamente en pantalla.

## 5. Revisión de la interfaz: alcance comprobado hasta ahora

- `estudiar-oa.ts` muestra el contenido de la guía a través de `MarkdownPipe`, ofrece descarga PDF, lectura por voz, calificación por estrellas y navegación a la autoevaluación.
- `MarkdownPipe` transforma Markdown a HTML y usa `bypassSecurityTrustHtml`. El comentario del código afirma que el contenido es propio/confiable. Esto no se clasifica como defecto de Matemática; es una dependencia de seguridad que debe reevaluarse si en el futuro el contenido puede ser editado por usuarios o ingresado desde fuentes no confiables.
- `autoevaluacion.ts` obtiene las preguntas del endpoint y las pasa a `EvaluacionRunner`.
- `EvaluacionRunner` muestra retroalimentación en autoevaluación inmediatamente después de que existe una respuesta; la corrección literal de respuestas abiertas descrita en MAT-UI-001 necesita prueba funcional.
- **No se ha ejecutado la aplicación en navegador en esta revisión**, por lo que no se certifican diseño responsive, recursos gráficos, navegación real, PDF, lectura por voz ni persistencia end-to-end.

## 6. Estado de la auditoría

| Área | Estado |
|---|---|
| Inventario de 12 guías | Completado para conteos y estructura |
| Coincidencia de los 116 identificadores OA con archivos de análisis de temario | Completado a nivel estructural |
| Cálculos y procedimientos de todos los ejemplos | Pendiente de revisión exhaustiva |
| Todas las 857 preguntas, alternativas, claves y retroalimentaciones | Pendiente de revisión exhaustiva |
| Verificación integral contra cada PDF oficial vigente | Pendiente |
| Correspondencia Markdown → base de datos importada | Pendiente |
| Ejecución real de la aplicación y comprobación visual de los 12 cursos | Pendiente |
| Ejecución de suites actuales de tests | No ejecutada desde este entorno |

## 7. Conclusión provisional

La estructura de las guías coincide con los identificadores OA incluidos en los análisis de temario para los 12 niveles. Sin embargo, ya hay un defecto funcional identificable en la corrección de respuestas abiertas y dos mejoras de contenido confirmadas, además de una convención estadística que debe explicitarse.

**No debe interpretarse este documento como una certificación final ni como aprobación para publicar contenido sin cambios.** La siguiente fase debe verificar sistemáticamente cada bloque de pregunta/solución y contrastar la importación y visualización de esos datos. No se han modificado archivos del repositorio.
