# Inventario reproducible inicial de contenido educativo — Logos School

**Commit base auditado:** `f43d67d368389492ba1d3da8d4843df9413d30bb`  
**Rama de trabajo:** `qa/fase-2-matriz-trazabilidad`  
**Método:** inventario estático del árbol GitHub; se cuentan rutas versionadas, no se valida aún la calidad ni el contenido completo de cada archivo.  
**Estado:** Fase de inventario inicial. Las cifras describen archivos, no cobertura curricular demostrada.

## 1. Resumen del árbol

- Archivos versionados totales en el árbol: **891**.
- Archivos Markdown de análisis por nivel en `Temarios/analisis/`: **13**.
- Carpetas de curso detectadas en `contenido/`: **12**.
- Rutas dentro de `contenido/` que no pertenecen a esas 12 carpetas de curso: **1**.

## 2. Inventario por curso

| Curso | Archivos bajo carpeta | Archivos principales de asignatura (MD) | Pruebas de unidad (rutas) | Exámenes (rutas) | Archivos principales detectados |
|---|---:|---:|---:|---:|---|
| 1° básico | 18 | 4 | 12 | 2 | ciencias-naturales, historia-geografia-y-cs-sociales, lenguaje-y-comunicacion, matematica |
| 2° básico | 18 | 4 | 12 | 2 | ciencias-naturales, historia-geografia-y-cs-sociales, lenguaje-y-comunicacion, matematica |
| 3° básico | 18 | 4 | 12 | 2 | ciencias-naturales, historia-geografia-y-cs-sociales, lenguaje-y-comunicacion, matematica |
| 4° básico | 18 | 4 | 12 | 2 | ciencias-naturales, historia-geografia-y-cs-sociales, lenguaje-y-comunicacion, matematica |
| 5° básico | 24 | 5 | 14 | 5 | ciencias-naturales, historia-geografia-y-cs-sociales, ingles, lenguaje-y-comunicacion, matematica |
| 6° básico | 24 | 5 | 14 | 5 | ciencias-naturales, historia-geografia-y-cs-sociales, ingles, lenguaje-y-comunicacion, matematica |
| 7° básico | 24 | 5 | 14 | 5 | ciencias-naturales, historia-geografia-y-cs-sociales, ingles, lengua-y-literatura, matematica |
| 8° básico | 24 | 5 | 14 | 5 | ciencias-naturales, historia-geografia-y-cs-sociales, ingles, lengua-y-literatura, matematica |
| 1° medio | 24 | 5 | 14 | 5 | ciencias-naturales, historia-geografia-y-cs-sociales, ingles, lengua-y-literatura, matematica |
| 2° medio | 24 | 5 | 14 | 5 | ciencias-naturales, historia-geografia-y-cs-sociales, ingles, lengua-y-literatura, matematica |
| 3° medio | 25 | 6 | 13 | 6 | ciencias-para-la-ciudadania, educacion-ciudadana, filosofia, ingles, lengua-y-literatura, matematica |
| 4° medio | 23 | 6 | 11 | 6 | ciencias-para-la-ciudadania, educacion-ciudadana, filosofia, ingles, lengua-y-literatura, matematica |

**Interpretación:** el conteo de archivos en `pruebas/` y `examenes/` no representa número de preguntas, número de OA cubiertos ni validación de respuestas. Los archivos principales se identifican por estar directamente bajo la carpeta del curso; puede haber otras modalidades o recursos en subdirectorios.

## 3. Riesgos que el inventario no resuelve

1. Un archivo existente no demuestra alineación con las Bases Curriculares o el programa de estudio vigente.
2. Un OA citado no demuestra que el recurso lo enseñe con suficiente profundidad ni que la evaluación mida ese OA.
3. El conteo de preguntas debe recalcularse a partir de la estructura real y validarse contra el parser usado en producción.
4. Hay que distinguir material de práctica, pruebas de unidad, exámenes Forma A/B, preguntas de desarrollo, rúbricas y respuestas.
5. La lista de asignaturas implementadas debe contrastarse con la oferta declarada por Logos School y los planes oficiales aplicables a cada nivel.
6. Los conteos de tests automatizados deben verificarse en ejecución; los documentos de QA por sí solos no prueban que el commit actual pase.

## 4. Siguiente etapa

- Parsear cada archivo de contenido y evaluación con su formato real, sin descartar secciones que el parser no reconozca.
- Extraer identificadores y referencias OA, conteos de preguntas, tipos de pregunta, soluciones, rúbricas y claves.
- Comparar con las fuentes curriculares oficiales pertinentes, registrando URL, título, versión/fecha y nivel.
- Generar una ficha por cada combinación curso-asignatura con estado explícito: verificado, hallazgo probable, no verificable o no aplica.
- Revisar primero los errores de exactitud y evaluación con potencial de perjudicar el aprendizaje; después progresión, claridad, accesibilidad y experiencia.
