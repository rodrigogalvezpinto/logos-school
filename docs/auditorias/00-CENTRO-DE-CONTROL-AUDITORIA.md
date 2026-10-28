# Centro de control único — Auditoría integral de Logos School

**Última actualización:** 28 de octubre de 2026  
**Rama de trabajo:** `main`  
**Alcance:** 1.º básico a 4.º medio; todas las asignaturas y recursos que el producto declara ofrecer o que se encuentren en el repositorio.  
**Estado global:** **EN CURSO — evaluaciones, guías y temarios cerrados (290/290 revalidados al 100 % en contenido/ y Temarios/)**.

> **Rama de trabajo actual:** `main`, sincronizada con `origin/main`. Si un cambio necesita aislamiento, se puede crear una rama desde `main`.

> Este documento es la fuente de verdad para orientarse y retomar el trabajo. Los informes de lotes fueron consolidados en `AUDITORIA_MAESTRA.md`; no son tableros independientes ni sustituyen la matriz maestra.

## 1. Reglas para mantener orden

1. **Una fuente de verdad:** actualizar este tablero y la matriz de cobertura al cerrar cada lote.
2. **No duplicar informes:** antes de crear uno nuevo, buscar si ya existe un informe del mismo curso, asignatura, archivo y pregunta. Si existe, ampliar ese informe o añadir una referencia cruzada.
3. **Separar los estados:** inventariado ≠ leído ≠ auditado por dimensión ≠ corregido ≠ revalidado.
4. **Rama de trabajo:** trabajar sobre `main`, sincronizada con `origin/main`. La antigua rama `qa/fase-2-matriz-trazabilidad` se integró por el PR #8 y solo se conserva como referencia histórica remota. Si un cambio necesita aislamiento, se puede crear una rama desde `main`.
5. **Durante el diagnóstico no se modifica contenido educativo sin registro.** Toda corrección se aplica en `main`, queda en la bitácora de implementación y permanece pendiente hasta su revalidación.
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

El árbol contiene 290 rutas de alcance educativo: 265 bajo `contenido/` y 25 bajo `Temarios/`. La distribución actual de estados en el CSV es de **290 archivos revalidados y 0 pendientes (100 % de archivos revalidados)**. El 100 % de los materiales educativos de estudio y evaluación bajo `contenido/` (50 exámenes simulacro, 156 pruebas de unidad, 58 guías de estudio y 1 tablero general) está auditado y revalidado con tamaño y SHA de blob actualizados. Las 25 rutas bajo `Temarios/` (12 PDFs UCE y 13 análisis Markdown) quedaron 100 % auditadas y revalidadas junto con los 410 OAs oficiales.

La matriz [estado por archivo (CSV)](matriz-maestra-estado-por-archivo.csv) contiene **290 rutas de alcance educativo**: 265 bajo `contenido/` (todas `revalidado`) y 25 bajo `Temarios/` (todas `revalidado`). El denominador de guías de estudio quedó reconciliado en 58 archivos. Estas categorías son de seguimiento y no equivalen a certificación integral. Los recursos consumidos por la aplicación, bancos de datos, importador y recursos externos aún deben reconciliarse con el inventario.

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
| Correcciones educativas | 265 archivos revalidados | Los 50 exámenes simulacro, las 156 pruebas de unidad, las 58 guías de estudio de 1.º básico a 4.º medio y el estado de contenido quedaron auditados y revalidados el 28-10-2026. La matriz ya no tiene filas en `corregido_pendiente_revalidacion` ni en `revision_parcial_documentada`. La evidencia completa se conserva en [AUDITORIA_MAESTRA.md](AUDITORIA_MAESTRA.md) §11 y §12. |
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

## 6. Informes de lotes — consolidados

Los informes de lote se consolidaron en [AUDITORIA_MAESTRA.md](AUDITORIA_MAESTRA.md) durante la reorganización documental del 28-10-2026. Sus archivos individuales ya no existen en el repositorio; el detalle de qué se retiró y por qué está en [ARCHIVOS-ELIMINADOS.md](ARCHIVOS-ELIMINADOS.md).

Informes retirados (evidencia absorbida por la auditoría maestra): 1.º básico (medición, datos y probabilidades), 4.º básico (examen integrado Forma B), 5.º básico (Historia Forma B), 1.º y 2.º medio (Matemática Forma B, recálculo), 1.º y 2.º medio (Ciencias Naturales Forma B), comparación Formas A/B de 3.º y 4.º básico, cribado transversal de Matemática y las pasadas primera a cuarta.

El único informe de lote que sigue existiendo como archivo independiente es el [control mecánico de claves de 2.º y 3.º básico](control-mecanico-claves-simulacros-2b-3b.md), que conserva su alcance acotado y no certifica la semántica de las respuestas.

## 7. Bitácora de correcciones autorizadas — 2026-10-22

Se aplicó la primera tanda de correcciones basada en la auditoría consolidada. La bitácora original (`registro-implementacion-correcciones-2026-10-22.md`) se retiró en la consolidación documental; su contenido quedó absorbido por [AUDITORIA_MAESTRA.md](AUDITORIA_MAESTRA.md) y por [ARCHIVOS-ELIMINADOS.md](ARCHIVOS-ELIMINADOS.md). Se corrigieron tres hallazgos P1 confirmados (clave 4B, puntaje 5B, inversa 2M) y ocho defectos de contenido/erratas verificadas. Los 50 exámenes fueron revalidados el 28-10-2026; los 6 archivos no-examen que siguen en `corregido_pendiente_revalidacion` conservan su estado hasta nueva evidencia.

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
- [x] Auditar todas las evaluaciones ítem por ítem (50 exámenes + 156 pruebas de unidad cerradas).
- [x] Auditar guías, explicaciones, actividades y recursos visuales (58 guías de estudio cerradas).
- [x] Contrastar cada OA con la fuente oficial aplicable (12 PDFs UCE y 410 OAs cotejados en Temarios/analisis/).
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
2. **Cobertura por archivo:** `matriz-maestra-estado-por-archivo.csv` (290 filas; estado vigente al 28-10-2026: 78 pendientes y 212 archivos revalidados).
3. **Hallazgos y correcciones:** `auditoria-maestra-hallazgos-y-correcciones-propuestas.md` y `registro-implementacion-correcciones-2026-10-22.md`; reconciliar IDs antes de contar hallazgos únicos.
4. **Evidencia:** ampliar informes existentes antes de crear otro informe para el mismo archivo/ítem.
5. **Validación técnica:** el workflow asociado al HEAD `77b9c15bb0f5bd29568d19d6e21702c000e3b9c9` terminó en éxito: [run 39871505287](https://github.com/rodrigogalvezpinto/logos-school/actions/runs/39871505287). Esto valida solo los pasos configurados.
6. **Siguiente tarea obligatoria:** reconciliar las 11 correcciones con la matriz CSV y el registro de hallazgos, y definir las regresiones que faltan. No abrir un lote nuevo hasta dejar esa reconciliación registrada.

**Advertencia de coherencia:** las secciones anteriores son el historial de decisiones. Si un checklist histórico contradice esta sección 12, prevalece el estado verificado de esta sección hasta la próxima actualización documentada.


## 13. Reconciliación de correcciones y línea base — 2026-10-22

### Línea base comprobada

- HEAD de código y contenido verificado antes de esta actualización: `e9d3dd5ffbeb9f6beb469476440202e6f2a100c2`.
- Árbol remoto: 937 archivos versionados; 290 rutas educativas bajo `contenido/` y `Temarios/`.
- La matriz CSV conserva 290 filas y sus tamaños/SHA de blob coinciden con el árbol remoto inspeccionado. Se actualizó la etiqueta `estado_inventario` de todas las filas para referir al HEAD `e9d3dd5`; esto identifica la línea base, no certifica revisión de contenido.
- CI: el run [39871558848](https://github.com/rodrigogalvezpinto/logos-school/actions/runs/39871558848) terminó en éxito para el HEAD `e9d3dd5`. Solo demuestra que los controles configurados pasaron.

### Conciliación de las 11 correcciones de la bitácora

| Archivo | Cambio registrado | ID maestro asociado | Estado correcto de seguimiento |
|---|---|---|---|
| `contenido/04-basico/examenes/examen-integrado-forma-b.md` | Clave P16: `c) 14` → `b) 14` | H-001 / LGS-4B-EVAL-001 | Corregido; regresión y QA de app pendientes |
| `contenido/05-basico/examenes/historia-geografia-y-cs-sociales-examen-forma-b.md` | Total de encabezado: 30 → 35 puntos | H-009 / LGS-5B-EVAL-001 | Corregido; escala de notas y regresión pendientes |
| `contenido/02-medio/examenes/matematica-examen-forma-b.md` | Inversa de `x+10` corregida a `x-10` | H-007 / LGS-2M-MAT-014 | Corregido; regresión y QA pendientes |
| `contenido/06-basico/matematica.md` | Explicación del resto y limpieza editorial de razón | H-003 / LGS-6B-MAT-001 y MAT-CONT-002 | Corregido; relectura y regresión pendientes |
| `contenido/07-basico/matematica.md` | Tabla de frecuencias corregida | LGS-7B-MAT-001 | Corregido; falta asignar/reconciliar ID H y ejecutar regresión |
| `contenido/02-medio/examenes/lengua-y-literatura-examen-forma-b.md` | Cita restaurada en P17 | Sin H-### identificado en el registro actual | Cambio de texto registrado; crear vínculo de hallazgo o clasificar como errata de baja severidad y validar |
| `contenido/05-basico/examenes/ingles-examen-forma-b.md` | Diálogo y turnos de disculpa corregidos | LGS-5B-ING-001; sin H-### identificado | Cambio registrado; revisar inglés y regresión |
| `contenido/01-medio/ciencias-naturales.md` | Distinción Doppler sonoro/luminoso | LGS-1M-CNT-011; sin H-### identificado | Cambio registrado; contraste disciplinar y regresión pendientes |
| `contenido/08-basico/historia-geografia-y-cs-sociales.md` | Errata «population» → «población» | Sin H-### identificado | Errata registrada; relectura pendiente |
| `contenido/01-medio/lengua-y-literatura.md` | Errata «information implícita» → «información implícita» | Sin H-### identificado | Errata registrada; relectura pendiente |
| `contenido/08-basico/lengua-y-literatura.md` | Contexto temporal «madrugada» → «tarde» y retroalimentación ajustada | LGS-8B-LEM-001; sin H-### identificado | Cambio registrado; verificación factual y regresión pendientes |

La matriz por archivo ya etiqueta estos 11 recursos como `corregido_pendiente_revalidacion` y enlaza la bitácora o el lote correspondiente. **No se deben contar las referencias H-###, LGS-* y MAT-* como defectos distintos cuando describen el mismo cambio.** A su vez, los cambios sin ID H-### deben incorporarse o vincularse en el registro maestro; no se inventa un ID retrospectivo sin actualizar dicho registro.

### Bloqueadores para continuar con nuevos lotes

1. Añadir o documentar las pruebas de regresión para las 11 correcciones, distinguiendo las pruebas automatizables de la revisión disciplinar.
2. Actualizar el registro maestro para vincular los 11 cambios con sus IDs estables, sin duplicar los hallazgos existentes.
3. Verificar el estado de los 11 fragmentos contra la versión remota actual; la bitácora de commits es evidencia de cambios, no evidencia suficiente de cierre.
4. Mantener la matriz en `corregido_pendiente_revalidacion` hasta que la prueba correspondiente pase y la revisión aplicable quede documentada.
5. No iniciar nuevos lotes sustantivos hasta completar esta reconciliación; después, continuar por prioridad P1 y con trazabilidad por archivo/pregunta/OA.

**Estado de organización:** inventario por archivo sincronizado; conciliación de cambios y sus IDs documentada; regresiones y revisión de app aún pendientes. La auditoría sigue en curso y no está certificada al 100 %.


## 14. Cierre de la reconciliación de IDs — 2026-10-22

La reconciliación documental de los 11 cambios de la bitácora ya se completó en [el registro maestro de hallazgos](auditoria-maestra-hallazgos-y-correcciones-propuestas.md): los cambios que no tenían encabezado H-### recibieron H-014 a H-021, y se conservaron H-001/H-003/H-007/H-009 para los problemas preexistentes correspondientes. Los identificadores operativos `LGS-*` y `MAT-*` se tratan como alias, no como defectos adicionales.

- La matriz por archivo sigue teniendo 290 filas; sus etiquetas de línea base apuntan al árbol inspeccionado `e9d3dd5`, y los 11 archivos cambiados conservan el estado `corregido_pendiente_revalidacion`.
- La última ejecución completada antes de la actualización del registro maestro fue [39871840806](https://github.com/rodrigogalvezpinto/logos-school/actions/runs/39871840806), con éxito. La ejecución de la actualización de IDs está en cola: [39871932321](https://github.com/rodrigogalvezpinto/logos-school/actions/runs/39871932321). No declarar esa ejecución como aprobada hasta consultar su resultado final.
- **La organización documental queda consolidada; la validación no.** Ninguno de los 11 cambios debe marcarse como cerrado hasta comprobar la fuente actual, ejecutar la regresión pertinente y registrar la evidencia.

### Próximo trabajo autorizado

1. Verificar el resultado de CI para el commit que añade H-014–H-021.
2. Diseñar y ejecutar regresiones específicas para los cambios cuantitativos y de clave (4B, 5B Historia, 2M Matemática, 6B Matemática, 7B Matemática) y revisiones lingüísticas/conceptuales para los restantes.
3. Actualizar los estados de la matriz solo cuando exista evidencia de revalidación.
4. Retomar auditoría sustantiva nueva únicamente después de cerrar esta etapa de regresión o registrar explícitamente qué no puede ejecutarse por falta de entorno QA.


## 15. Estado verificado al 28 de octubre de 2026 — rama `main`

Esta sección es la foto vigente y sustituye los recuentos de las secciones históricas anteriores. Se midió sobre `main` en el commit de contenido `22385ab`, después de integrar el PR #8, revalidar los 6 archivos no-examen y auditar las 156 pruebas de unidad de 1.º básico a 4.º medio.

### 15.1 Regla de trabajo

- **Rama de trabajo:** todo cambio se hace sobre `main`. Si un cambio necesita aislamiento, se puede crear una rama desde `main`.
- La rama `qa/fase-2-matriz-trazabilidad` quedó integrada y se conserva solo como referencia histórica remota. No se usa para trabajar.
- Cada cambio se registra en un commit con mensaje claro y se empuja a `origin/main`.

### 15.2 Contenido cerrado

| Comprobación | Resultado |
|---|---|
| Exámenes auditados y revalidados | **50 / 50** |
| Archivos no-examen revalidados | **6 / 6** |
| Pruebas de unidad revalidadas (1.º básico a 4.º medio) | **156 / 156** |
| Preguntas de prueba de unidad | 1.824 |
| Preguntas de examen | 1.210 |
| Alternativas | 635 |
| Desalineaciones enunciado ↔ alternativa ↔ pauta | 0 |
| Problemas de formato de pauta | 0 (validador estructural en 0 hallazgos sobre 265 archivos) |
| Claves con opción sobre 45 % | 0 |
| Anglicismos | 0 |
| Imprecisiones factuales | 0 |
| Rúbricas con suma igual al puntaje | 91 / 91 |
| Hoja de respuestas y tabla de especificaciones | 50 / 50 |
| Preguntas con tablas de datos que reformulan cifras | 13, sin alterar respuestas |
| Enlaces rotos dentro de `contenido/` | 0 |
| Menciones falsas a una «Forma A» inexistente | 0 (quedan 25 legítimas de 1.º–4.º básico) |

La matriz CSV quedó reconciliada: los 50 exámenes, los 6 archivos no-examen y las 156 pruebas de unidad de 1.º básico a 4.º medio pasaron a `revalidado`, con `estado_inventario` en `22385ab`, bytes y blob SHA regenerados, referencia a `AUDITORIA_MAESTRA.md` y observación con la evidencia de cierre.

### 15.3 Pendientes de contenido

1. **Pruebas de unidad: 156 en total, 156 revalidadas.** El cierre de 1.º a 8.º básico y de 1.º a 4.º medio quedó el 28-10-2026, con frontmatter normalizado y 1.824 preguntas verificadas.
2. **Guías de estudio: la matriz cuenta 48 y el árbol tiene 58.** Hay que reconciliar el denominador antes de declarar porcentajes; hoy 44 de las 48 filas de la matriz figuran pendientes. El resto de los 78 pendientes son temarios y documentos curriculares.
3. Los **6 archivos no-examen** que estaban en `corregido_pendiente_revalidacion` quedaron revalidados el 28-10-2026.
4. **55 marcadores `[Imagen: ...]` en 23 archivos** siguen sin ser imágenes reales (issue #2). Falta decidir estrategia: IA, banco libre, SVG/emoji o reescribir sin imagen.
5. **Componentes visuales de Matemática** (recta numérica, fracciones, figuras) siguen pendientes.
6. **18 de 50 exámenes no declaran `Puntaje total` y 49 de 50 no declaran escala**; el importador no lee esos campos. Es cosmético y no fue solicitado, pero conviene unificarlo.

### 15.4 Pendientes técnicos

- **Backend y E2E no se pudieron ejecutar** en esta sesión: el daemon de Docker estaba detenido y PostgreSQL no escuchaba en 5432. Línea base documentada: 491 pytest / 33 Vitest / 362 E2E (21-10-2026). El frontend unitario sí se ejecutó: **46/46 en verde** (10 archivos).
- **El CI solo valida contenido estructural** (`qa-auditoria-contenido.yml`). No ejecuta pytest, Vitest ni Playwright.
- Los issues **#3, #4, #5 y #6** quedaron cerrados el 28-10-2026 con comentario y evidencia.
- El issue **#7** quedó actualizado para apuntar a `main`; sigue abierto hasta cerrar la auditoría integral.
- Queda pendiente borrar la rama remota `ai/roadmap-inteligencia-educativa`: su contenido ya está integrado en `main`.

### 15.5 Próximos pasos, en orden

1. Reconciliar el denominador de guías (48 en matriz vs. 58 en árbol) y auditar las guías.
2. Decidir y ejecutar la estrategia de imágenes del issue #2.
3. Levantar PostgreSQL/Docker y correr backend + E2E.
4. Ampliar el CI a pytest, Vitest y Playwright.
5. Preparar producción (issue #1): Neon, Render, Cloudflare Pages, Sentry, UptimeRobot y credenciales.

**Conclusión:** el contenido de exámenes está cerrado y la matriz ya refleja ese cierre. La auditoría integral **sigue en curso**: faltan pruebas de unidad, guías, recursos visuales y la verificación técnica en entorno completo. No se declara 100 %.
