# Centro de control único — Auditoría integral de Logos School

**Última actualización:** 22 de octubre de 2026  
**Rama de trabajo:** `qa/fase-2-matriz-trazabilidad`  
**Alcance:** 1.º básico a 4.º medio; todas las asignaturas y recursos que el producto declara ofrecer o que se encuentren en el repositorio.  
**Estado global:** **EN CURSO — NO CERTIFICADA AL 100 %**.

> Este documento es la fuente de verdad para orientarse y retomar el trabajo. Los informes de lotes conservan la evidencia detallada; no son tableros independientes ni sustituyen la matriz maestra.

## 1. Reglas para mantener orden

1. **Una fuente de verdad:** actualizar este tablero y la matriz de cobertura al cerrar cada lote.
2. **No duplicar informes:** antes de crear uno nuevo, buscar si ya existe un informe del mismo curso, asignatura, archivo y pregunta. Si existe, ampliar ese informe o añadir una referencia cruzada.
3. **Separar los estados:** inventariado ≠ leído ≠ auditado por dimensión ≠ corregido ≠ revalidado.
4. **No mezclar ramas:** este tablero describe la rama QA indicada arriba. Los documentos de otras ramas son evidencia relacionada, no se asume que estén incorporados aquí hasta comprobarlo.
5. **Durante el diagnóstico no se modifica contenido educativo.** La auditoría consolidada aportada el 22-10-2026 autoriza iniciar correcciones en esta rama QA. No cambiar `main`; cada cambio debe quedar en la bitácora de implementación y permanecer pendiente hasta revalidación.
6. **Cada hallazgo tiene un ID estable** y debe tener ruta, ubicación, evidencia, tipo, severidad, recomendación, prueba de regresión y estado.
7. **Una ejecución CI verde no certifica el contenido educativo.** Solo demuestra que los trabajos configurados para ese commit pasaron.

## 2. Entrada recomendada — leer en este orden

1. **Este tablero:** alcance, estado y siguiente acción.
2. [Índice y registro de informes](INDICE-REGISTRO-INFORMES.md): catálogo de los documentos existentes; consultar antes de crear informes nuevos.
3. [Handoff y bitácora maestra](HANDOFF-MAESTRO-AUDITORIA.md): contexto, decisiones, continuidad.
4. [Plan maestro educativo](auditoria-integral-educativa-plan-maestro.md): dimensiones, severidades y protocolo.
5. [Matriz maestra de asignaturas de 12 cursos](matriz-maestra-asignaturas-12-cursos.md): mapa por curso y asignatura.
6. [Inventario maestro de materiales](inventario-maestro-materiales-2026-10-21.md): listado de rutas de `contenido/` y `Temarios/`.
7. [Inventario reproducible histórico](inventario-reproducible-contenido-educativo.md): referencia histórica; sus cifras deben regenerarse antes de usarlas como estado actual.
8. [Consolidación de hallazgos](consolidacion-hallazgos-y-controles-12-cursos.md): resumen de hallazgos conocidos y enlaces a lotes.
9. [Issue de seguimiento #7](https://github.com/rodrigogalvezpinto/logos-school/issues/7): checklist de fases y criterio de cierre.

## 3. Estado de inventario — no confundir con cobertura de auditoría

En la rama QA, el árbol consultado en el commit previo contenía **933 archivos versionados**; el siguiente corte detectó 934 antes de añadir el índice documental, por lo que se debe regenerar el conteo al actualizar la matriz. La carpeta `docs/auditorias/` incluye numerosos informes de diferentes fechas, pasadas y ámbitos. Por ello, los recuentos de documentos no son una métrica de cobertura educativa.

El inventario maestro anterior identificó **290 archivos** dentro de `contenido/` y `Temarios/` (265 y 25 respectivamente) en su corte. Esa cifra es una línea base histórica que debe regenerarse desde el commit actual y reconciliarse con bancos de datos, importador, recursos externos y contenido mostrado por la aplicación.

**Revisión completa registrada en la matriz de ese inventario: 0 al momento de su corte.** Esto no invalida los lotes parciales posteriores; significa que no se ha demostrado el cierre sistemático de cada fila del inventario.

## 4. Matriz de estado global por dimensión

| Dimensión | Estado actual | Evidencia / brecha |
|---|---|---|
| Inventario de archivos | Parcial / requiere regeneración | Hay inventarios con cortes distintos; falta una única exportación del HEAD actual y reconciliación con recursos consumidos por la app. |
| Catálogo de cursos y asignaturas | Parcial | Hay una matriz de 12 cursos, pero debe cotejarse con alcance del producto y fuentes oficiales vigentes. |
| Exactitud disciplinar | Parcial, por lotes | Existen recálculos y hallazgos específicos; no hay revisión completa de todos los ítems. |
| Claves y puntajes | Parcial + validador estructural | Se conocen discrepancias P1; el control no detecta todos los errores semánticos. |
| Calidad pedagógica y adecuación al nivel | Parcial | Informes preliminares; falta revisión sistemática por archivo y actividad. |
| Alineación curricular oficial | No certificada | Hay análisis previos; falta trazabilidad exhaustiva fuente oficial → OA → recurso → evaluación. |
| Recursos visuales y accesibilidad | No certificada | Falta cotejar referencias y render de la aplicación. |
| Importación, puntuación y persistencia en app | No certificada | Se requiere entorno QA, pruebas reproducibles y contraste fuente/salida. |
| Correcciones educativas | Primera tanda aplicada en rama QA | 11 cambios de contenido/documentación de ítems aplicados; todos pendientes de regresión y revalidación. Ver [bitácora de implementación](registro-implementacion-correcciones-2026-10-22.md). |
| Certificación final | No iniciada | Requiere denominadores conocidos, estados por unidad, hallazgos cerrados/aceptados y pruebas relevantes. |

## 5. Hallazgos de alto impacto conocidos

Estos son puntos de seguimiento conocidos, no la lista completa de todos los defectos posibles.

| ID de seguimiento | Curso / recurso | Hallazgo | Estado |
|---|---|---|---|
| LGS-1B-MAT-001 | 1.º básico, prueba de medición, pregunta 2 | Orden de objetos por longitud sin medidas ni estímulo visual inequívoco en el Markdown | Documentado; verificar render |
| LGS-4B-EVAL-001 | 4.º básico, examen integrado Forma B, pregunta 16 | La pauta indicaba c) 14; el 14 está en b) | Corregido en QA; regresión pendiente |
| LGS-5B-EVAL-001 | 5.º básico, Historia Forma B | Encabezado declaraba 30 puntos frente a pauta/distribución de 35 | Corregido encabezado a 35 en QA; revisar escala de nota y regresión |
| LGS-6B-MAT-001* | 6.º básico, guía de Matemática, pregunta 4 | Retroalimentación sobre 2.050 botellas en cajas de 12 y reparto entre 3 distribuidores no explicaba el residuo | Aclarado en QA; regresión pendiente |
| LGS-2M-MAT-014* | 2.º medio, Matemática Forma B, pregunta 14 | Pauta daba x+10 como inversa de f(x)=x+10; la inversa correcta es x−10 | Corregido en QA; regresión pendiente |

`*` IDs de seguimiento internos para este tablero; si el informe fuente usa otra identificación, conservarla y reconciliarla en la matriz de hallazgos antes de asignar IDs definitivos.

## 6. Informes de lotes — usar los existentes

- [1.º básico: medición, datos y probabilidades](lote-01-basico-matematica-medicion-datos.md)
- [Control mecánico de claves: Formas A/B de 2.º y 3.º básico](control-mecanico-claves-simulacros-2b-3b.md)
- [4.º básico: examen integrado Forma B](lote-04-basico-examen-integrado-forma-b.md)
- [5.º básico: Historia Forma B](lote-05-basico-historia-examen-forma-b.md)
- [1.º medio: Matemática Forma B, recálculo](lote-01-medio-matematica-examen-forma-b-recalculo.md)
- [2.º medio: Matemática Forma B, recálculo](lote-02-medio-matematica-examen-forma-b-recalculo.md)
- [1.º medio: Ciencias Naturales Forma B](lote-01-medio-ciencias-naturales-forma-b.md)
- [2.º medio: Ciencias Naturales Forma B](lote-02-medio-ciencias-naturales-forma-b.md)
- [Comparación Formas A/B de 3.º y 4.º básico](lote-comparativo-formas-a-b-3b-4b.md)
- [Cribado transversal de Matemática](lote-transversal-matematica-3medio-8basico-cribado.md)

También existen informes de primera, segunda, tercera y cuarta pasada. No deben interpretarse como lotes completados integralmente si su propio alcance indica cribado o revisión parcial.

## 7. Bitácora de correcciones autorizadas — 2026-10-22

Se aplicó la primera tanda de correcciones basada en la auditoría consolidada. Ver [registro de implementación](registro-implementacion-correcciones-2026-10-22.md) para IDs, rutas y commits. Se corrigieron tres hallazgos P1 confirmados (clave 4B, puntaje 5B, inversa 2M) y ocho defectos de contenido/erratas verificadas. **Ninguno se considera cerrado** hasta ejecutar regresión, comprobar importación/render y actualizar el registro de hallazgos. No se modificó `main` ni la base de datos.

## 8. Próxima secuencia obligatoria

### Fase A — Orden y línea base reproducible
- [ ] Regenerar el inventario desde el HEAD actual con rutas, tamaños/tipos y hash de commit.
- [ ] Identificar y etiquetar informes históricos, duplicados, pasadas parciales y fuentes vigentes.
- [ ] Crear una matriz única por recurso/ítem que vincule el informe de evidencia y el estado por dimensión.
- [ ] Reconciliar IDs de hallazgos y enlaces a issues.

### Fase B — Controles técnicos
- [ ] Revisar las ejecuciones recientes de CI y documentar qué pasos ejecutan realmente.
- [ ] Ampliar el validador para detectar los formatos de clave/puntaje reales sin introducir falsos positivos.
- [ ] Añadir regresiones específicas para los hallazgos confirmados, sin corregir contenido fuente todavía.

### Fase C — Auditoría sustantiva completa
- [ ] Auditar todas las evaluaciones ítem por ítem.
- [ ] Auditar guías, explicaciones, actividades y recursos visuales.
- [ ] Contrastar cada OA con la fuente oficial aplicable y registrar URL, título, versión/fecha y evidencia.
- [ ] Verificar render/importación/calificación en QA.

### Fase D — Correcciones autorizadas y certificación
- [ ] Presentar propuesta priorizada de correcciones.
- [ ] Aplicar solo tras autorización, en cambios pequeños y revisables.
- [ ] Ejecutar regresión técnica, disciplinar y curricular.
- [ ] Publicar cobertura por dimensión y curso, riesgos residuales y excepciones.
- [ ] Certificar solo cuando los criterios del protocolo estén satisfechos.

## 9. Regla de cierre del 100 %

No declarar 100 % por el número de archivos leídos, por contar informes o porque CI pase. Cada unidad del inventario debe tener estado y evidencia: revisada y revalidada, o excepción justificada. Deben conocerse los denominadores de archivos, ítems, claves, rúbricas, OA y recursos. Los hallazgos P0/P1 deben estar resueltos o tener una decisión explícita de bloqueo/no publicación; los cambios deben contar con regresión. Las dimensiones que requieran especialistas humanos deben identificarse como tales.

**Conclusión vigente:** el trabajo previo es aprovechable y contiene hallazgos reales, pero está distribuido en informes de diferentes pasadas y todavía no prueba cobertura integral. A partir de este tablero, toda continuación debe actualizar el registro maestro y evitar crear documentos paralelos innecesarios.


## 10. Orden documental aplicado — 2026-10-22

- Se añadió el [índice y registro de informes existentes](INDICE-REGISTRO-INFORMES.md), que clasifica 48 documentos Markdown bajo `docs/auditorias/` por función y advierte que el número de informes no es cobertura auditada.
- Se reafirma la jerarquía: este centro de control > matriz de cobertura por archivo/ítem (pendiente de generar) > registro maestro de hallazgos > informes de evidencia por lote. El índice y el handoff facilitan navegación, pero no sustituyen esas fuentes.
- **Regla de no proliferación:** antes de crear un nuevo informe, revisar el índice y ampliar el documento existente si ya cubre el mismo archivo/ítem.
- **Próxima tarea de orden:** generar una matriz reproducible del árbol vigente, con estado por archivo y dimensiones; reconciliar sus filas con hallazgos H-###, issues y evidencias existentes. Hasta entonces, la cobertura total continúa sin calcularse.
