# Registro maestro de documentos de auditoría — Logos School

**Corte del registro:** 28 de octubre de 2026  
**Rama:** `main`  
**HEAD de referencia:** `d6eca32`  
**Estado:** índice documental; no certifica la calidad de los materiales.

> **Rama de trabajo actual:** `main`, sincronizada con `origin/main`. La antigua rama `qa/fase-2-matriz-trazabilidad` se integró por el PR #8 y se conserva como referencia histórica.

## Reglas de uso

1. El [Centro de control único](00-CENTRO-DE-CONTROL-AUDITORIA.md) es la fuente de verdad para prioridades, cobertura y siguiente acción.
2. Este registro solo permite encontrar documentos y distinguir su función; contar informes no equivale a cobertura auditada.
3. La matriz de cobertura es la que determina si un archivo, pregunta, OA o recurso fue revisado; nunca se deduce del nombre del documento.
4. Antes de crear un informe nuevo, buscar en este índice y ampliar el informe existente si ya cubre el mismo curso, asignatura, archivo o pregunta.
5. Los documentos retirados en la consolidación no se recrean: su contenido se consulta en [AUDITORIA_MAESTRA.md](AUDITORIA_MAESTRA.md) o en [ARCHIVOS-ELIMINADOS.md](ARCHIVOS-ELIMINADOS.md).

## Documentos vigentes por función

| Función | Documento | Uso / precaución |
|---|---|---|
| Control vigente | [00 — Centro de control de auditoría](00-CENTRO-DE-CONTROL-AUDITORIA.md) | Fuente única de prioridades, estado y siguiente acción. Leer primero. |
| Auditoría consolidada | [AUDITORIA_MAESTRA.md](AUDITORIA_MAESTRA.md) | Cierre de contenido de los 50 exámenes, rúbricas, hojas de respuesta y evidencias. |
| Cobertura por archivo | [matriz maestra de estado por archivo (CSV)](matriz-maestra-estado-por-archivo.csv) | 290 rutas de `contenido/` y `Temarios/`; bytes y blob SHA al HEAD `d6eca32`. Los 50 exámenes y los 6 archivos no-examen están `revalidado`. |
| Cobertura por curso/asignatura | [matriz maestra de asignaturas de 12 cursos](matriz-maestra-asignaturas-12-cursos.md) | Mapa curricular por curso y asignatura; no sustituye la matriz por archivo ni certifica ítems. |
| Continuidad | [Handoff y bitácora maestra](HANDOFF-MAESTRO-AUDITORIA.md) | Contexto histórico y decisiones; sus recuentos antiguos no son métricas actuales. |
| Gobernanza / criterios | [Plan maestro de auditoría integral](auditoria-integral-educativa-plan-maestro.md) | Dimensiones, severidades y protocolo de revisión. |
| Gobernanza / criterios | [Protocolo de auditoría integral 100 %](protocolo-auditoria-integral-100.md) | Criterios de cierre y evidencia exigida. |
| Registro de hallazgos | [Auditoría maestra de hallazgos y correcciones propuestas](auditoria-maestra-hallazgos-y-correcciones-propuestas.md) | IDs H-### y correcciones aplicadas; no certifica el resto del contenido. |
| Registro de hallazgos | [Consolidación de hallazgos y controles de 12 cursos](consolidacion-hallazgos-y-controles-12-cursos.md) | Resumen histórico de hallazgos conocidos; verificar estado vigente en el centro de control. |
| Control mecánico | [Control de claves de simulacros 2.º y 3.º básico](control-mecanico-claves-simulacros-2b-3b.md) | Comprobación de letras de pauta; no certifica la semántica de las respuestas. |
| Inventario | [Inventario maestro de materiales 2026-10-21](inventario-maestro-materiales-2026-10-21.md) | Rutas de `contenido/` y `Temarios/`; regenerar cifras antes de usarlo como estado actual. |
| Inventario histórico | [Inventario reproducible del contenido educativo](inventario-reproducible-contenido-educativo.md) | Referencia histórica; no usar sus cifras como estado vigente. |
| Línea Matemática | [README de auditoría de Matemática](matematica/README.md) | Índice y guía de handover de la línea temática. |
| Línea Matemática | [01 — Inventario de auditoría](matematica/01-inventario-auditoria.md) | Conteos de la línea de Matemática en su corte. |
| Línea Matemática | [02 — Hallazgos consolidados](matematica/02-hallazgos-consolidados.md) | Fichas de hallazgos de Matemática por severidad. |
| Línea Matemática | [03 — Matriz curricular](matematica/03-matriz-curricular.md) | Contraste de OA oficiales con las guías de Matemática. |
| Línea Matemática | [04 — Auditoría de Matemática (CSV)](matematica/04-auditoria-matematica.csv) | Dataset de preguntas y análisis sintáctico. |
| Línea Matemática | [08 — Resumen ejecutivo](matematica/08-resumen-ejecutivo.md) | Síntesis de riesgos y prioridades de Matemática. |
| UX / accesibilidad | [Hallazgos UX/UI](ux-ui/hallazgos-ux.md) | Observaciones de experiencia de usuario y accesibilidad. |
| Registro documental | [Archivos eliminados](ARCHIVOS-ELIMINADOS.md) | Lista de los 33 documentos retirados, el archivo movido y su destino. |
| Plan de consolidación | [Plan de consolidación documental](../PLAN-CONSOLIDACION-DOCUMENTACION.md) | Qué se eliminó, qué se movió y por qué. |

## Documentos de calidad y planificación relacionados

| Función | Documento | Uso |
|---|---|---|
| Línea base de pruebas | [docs/qa/linea-base.md](../qa/linea-base.md) | Resultados documentados de pytest, Vitest y Playwright (corte 21-10-2026). |
| Inventario de suites | [docs/qa/inventario-suites.md](../qa/inventario-suites.md) | Módulos, rutas y funcionalidades cubiertas. |
| Plan de avance por curso | [docs/qa/plan-avance-12-cursos.md](../qa/plan-avance-12-cursos.md) | Protocolo E2E de los 12 cursos. |
| Plan de regresión | [docs/qa/06-plan-pruebas-regresion.md](../qa/06-plan-pruebas-regresion.md) | Casos de prueba requeridos y matriz de regresión. |
| Histórico QA | [docs/qa/historico/](../qa/historico/) | Reportes y resúmenes de ejecuciones anteriores. |
| Especificación de correcciones | [docs/planes/05-especificacion-correcciones.md](../planes/05-especificacion-correcciones.md) | Cambios técnicos aprobados. |
| Prompt de ejecución | [docs/planes/07-prompt-agente-ejecucion.md](../planes/07-prompt-agente-ejecucion.md) | Instrucciones para implementar correcciones. |
| Pendientes tecnológicos | [docs/planes/pendientes-voz-videos-juegos.md](../planes/pendientes-voz-videos-juegos.md) | Voz natural, videos y juegos por validar. |
| Backlog de producto | [docs/planes/backlog-producto-tutor-ia-y-lectura.md](../planes/backlog-producto-tutor-ia-y-lectura.md) | Tutor IA y evaluación de lectura; no implementados. |

## Documentos retirados en la consolidación

La reorganización del 28-10-2026 eliminó **33 archivos** y movió `AUDITORIA_MAESTRA.md` desde la raíz a `docs/auditorias/`. Entre los retirados están:

- los informes de lote de 1.º a 8.º básico y de 1.º a 4.º medio;
- las pasadas primera a cuarta;
- los informes preliminares y paralelos;
- la bitácora `registro-implementacion-correcciones-2026-10-22.md`;
- los informes `informe-preliminar-20-oct.md` y `09-segunda-revision-20-oct.md` de Matemática.

**No se recrean.** Su contenido quedó absorbido por [AUDITORIA_MAESTRA.md](AUDITORIA_MAESTRA.md), el centro de control y los commits de Git. La lista completa, con el destino de cada archivo, está en [ARCHIVOS-ELIMINADOS.md](ARCHIVOS-ELIMINADOS.md).

## Estado vigente de la matriz

La matriz CSV tiene **290 filas** y estos estados al 28-10-2026:

| Estado | Filas |
|---|---:|
| `pendiente_auditoria_sistematica` | 233 |
| `revision_parcial_documentada` | 1 |
| `corregido_pendiente_revalidacion` | 0 |
| `revalidado` | 56 |
| **Total** | **290** |

Los 50 exámenes y los 6 archivos no-examen están cerrados. Los 233 pendientes incluyen 156 pruebas de unidad y las guías de estudio. El denominador de guías debe reconciliarse: la matriz cuenta 48 y el árbol tiene 58 archivos de guía.

## Problemas de organización que siguen abiertos

1. Los documentos conservan cortes y fechas distintas; las cifras antiguas no deben presentarse como actuales.
2. El denominador de guías no coincide entre la matriz (48) y el árbol (58).
3. Los IDs de seguimiento `LGS-*` y `MAT-*` son alias de los IDs H-###; no son defectos adicionales.
4. Falta una matriz reproducible que relacione cada pregunta y cada OA con dimensiones revisadas, evidencia y pruebas.
5. El issue #7 todavía enlaza a la rama `qa/...`; debe actualizarse a `main`.
