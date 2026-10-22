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

En el HEAD vigente `a462ebef452b730628b0832c700f3e53a066489c`, el árbol contiene **937 archivos versionados** y 290 rutas de alcance educativo. La matriz CSV se regeneró en el commit `40bb7ce172ec5a50c24d7256ef68a6d5e3d95827`, actualizando tamaño y SHA de blob para las 290 rutas. La distribución actual de estados se recalculó directamente desde el CSV: 271 pendientes de auditoría sistemática, 8 con revisión parcial documentada y 11 corregidas pendientes de revalidación. El inventario de rutas está sincronizado; falta reconciliar recursos consumidos por la aplicación y expandir cobertura a preguntas/OA/recursos.

La matriz [estado por archivo (CSV)](matriz-maestra-estado-por-archivo.csv) contiene **290 rutas de alcance educativo**: 265 bajo `contenido/` y 25 bajo `Temarios/`. De esas filas, **271 están pendientes de auditoría sistemática, 8 tienen revisión parcial documentada y 11 figuran como corregidas pendientes de revalidación**. Estas categorías son de seguimiento y no equivalen a certificación. Los recursos consumidos por la aplicación, bancos de datos, importador y recursos externos aún deben reconciliarse con el inventario.

La matriz conserva ruta, curso/área preliminar, tipo de recurso, tamaño, SHA del blob, estado, informe de referencia y dimensiones pendientes. Los estados preliminares deben actualizarse con evidencia, no inferirse del nombre del archivo.

## 4. Matriz de estado global por dimensión

| Dimensión | Estado actual | Evidencia / brecha |
|---|---|---|
| Inventario de archivos | Parcial / reconciliación pendiente | Las rutas, tamaños y SHA del CSV se regeneraron; falta reconciliar estados heredados y recursos consumidos por la app. |
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
- [x] Regenerar el inventario de rutas, tamaños y SHA de blob para las 290 rutas de alcance educativo; HEAD actual: `a462ebef452b730628b0832c700f3e53a066489c`.
- [x] Crear el índice de informes y establecer el centro de control como punto único de entrada; los informes parciales/históricos quedan identificados para navegación.
- [ ] Crear una matriz por recurso/ítem/OA que vincule evidencia, dimensiones revisadas, hallazgos y regresiones. La matriz CSV actual solo cubre estado por archivo.
- [ ] Reconciliar IDs H-###, LGS-*, MAT-* y los issues, evitando contar el mismo defecto más de una vez.

### Fase B — Controles técnicos
- [x] Revisar las ejecuciones recientes de CI: el workflow de auditoría de contenido pasó en el HEAD `a462ebef452b730628b0832c700f3e53a066489c`.
- [ ] Documentar la cobertura y limitaciones exactas de cada control automatizado; CI verde no equivale a validación pedagógica.
- [ ] Añadir/confirmar regresiones específicas para las 11 correcciones aplicadas en QA y verificar importación/render cuando el entorno esté disponible.

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

- Se creó el [índice y registro de informes existentes](INDICE-REGISTRO-INFORMES.md), que clasifica los documentos de auditoría por función y advierte que el número de informes no es cobertura auditada.
- Se generó la [matriz maestra de estado por archivo (CSV)](matriz-maestra-estado-por-archivo.csv) con 290 filas de `contenido/` y `Temarios/`, con hashes actualizados desde el árbol del commit `c87604c3b9879d208c132bc5bd810a9c518c05f1`.
- Jerarquía vigente: **centro de control → matriz por archivo → registro maestro de hallazgos/bitácora de correcciones → informes de evidencia**. El índice y el handoff facilitan navegación; no sustituyen la matriz.
- **Regla de no proliferación:** antes de crear un informe, consultar el índice y ampliar el informe existente si cubre el mismo archivo/ítem.
- La matriz ya permite conocer un denominador de rutas versionadas educativas, pero aún falta expandirla a cada pregunta, OA y recurso visual y reconciliarla con la aplicación. Por tanto, todavía no hay porcentaje global de auditoría integral.


## 11. Reconciliación de inventario completada — 2026-10-22

- Se inspeccionó el árbol remoto actual: 937 archivos versionados y exactamente 290 rutas bajo `contenido/` y `Temarios/` (265 y 25, respectivamente).
- Se regeneraron las columnas de tamaño y SHA de blob del CSV [matriz maestra de estado por archivo](matriz-maestra-estado-por-archivo.csv) para las 290 rutas; commit de la matriz: `40bb7ce172ec5a50c24d7256ef68a6d5e3d95827`.
- **Límite importante:** se conservaron los estados heredados de seguimiento; actualizar hashes no significa que el archivo haya sido re-auditado. Las categorías 271 pendientes, 8 parciales y 11 corregidas pendientes de revalidación deben reconciliarse con la bitácora vigente, porque reflejan decisiones anteriores.
- El último workflow verificado para el HEAD anterior de documentación fue verde; debe consultarse el run asociado al nuevo HEAD después de esta actualización. CI verde no certifica la calidad pedagógica.
- Próximo paso: reconciliar los 13 hallazgos H-### con IDs LGS y otros identificadores de lote, y sincronizar estados de corrección/regresión antes de abrir otro lote sustantivo.


## 12. Reordenamiento y estado verificado — 2026-10-22, 20:22 CLT

Esta sección sustituye las instrucciones históricas que hayan quedado desactualizadas en otras secciones. Para continuar, usar este orden operativo:

1. **Punto de entrada:** este centro de control.
2. **Cobertura por archivo:** `matriz-maestra-estado-por-archivo.csv` (290 filas; estados recalculados: 271 pendientes, 8 revisión parcial, 11 corregidos pendientes de revalidación).
3. **Hallazgos y correcciones:** `auditoria-maestra-hallazgos-y-correcciones-propuestas.md` y `registro-implementacion-correcciones-2026-10-22.md`; reconciliar IDs antes de contar hallazgos únicos.
4. **Evidencia:** ampliar informes existentes antes de crear otro informe para el mismo archivo/ítem.
5. **Validación técnica:** el workflow asociado al HEAD `77b9c15bb0f5bd29568d19d6e21702c000e3b9c9` terminó en éxito: [run 39871505287](https://github.com/rodrigogalvezpinto/logos-school/actions/runs/39871505287). Esto valida solo los pasos configurados.
6. **Siguiente tarea obligatoria:** reconciliar las 11 correcciones con la matriz CSV y el registro de hallazgos, y definir las regresiones que faltan. No abrir un lote nuevo hasta dejar esa reconciliación registrada.

**Advertencia de coherencia:** las secciones anteriores son el historial de decisiones. Si un checklist histórico contradice esta sección 12, prevalece el estado verificado de esta sección hasta la próxima actualización documentada.
