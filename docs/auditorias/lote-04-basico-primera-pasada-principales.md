# Auditoría preliminar de contenido principal — 4.º básico

**Rama:** `qa/fase-2-matriz-trazabilidad`  
**Alcance:** primera inspección temática de las cuatro guías principales de 4.º básico: Matemática, Lenguaje y Comunicación, Ciencias Naturales e Historia, Geografía y Ciencias Sociales. Se buscaron afirmaciones universales, consistencia interna y errores evidentes en fragmentos de ejercicios y retroalimentación. No es una lectura ítem por ítem completa, ni certifica la alineación con los OA oficiales. No se modificó contenido fuente ni `main`.

## Observaciones para seguimiento

### LGS-4B-MAT-001 — La explicación de conteo por centenas puede inducir una regla de valor posicional imprecisa
- **Severidad provisional:** P3 (claridad matemática).
- **Evidencia:** en `matematica.md`, sección de secuencias de 100 en 100, la retroalimentación dice que “solo cambia el dígito de las centenas (y a veces las unidades de mil, si se pasa de 900 a 000)”.
- **Evaluación:** la intención es útil, pero la expresión “se pasa de 900 a 000” puede ser confusa porque los números conservan el valor posicional completo (por ejemplo, 2.900 → 3.000). Es preferible explicar el cambio de centena y de unidad de mil cuando se cruza el millar.
- **Recomendación:** ajustar en una fase posterior con ejemplos que incluyan 2.900 → 3.000 y 3.900 → 4.000; comprobar que la explicación no se interprete como pérdida de valor de las cifras.

### LGS-4B-LEN-001 — Los criterios de respuesta abierta deben aceptar variaciones justificadas
- **Severidad provisional:** P3 (evaluación de comprensión).
- **Evidencia:** la guía de Lenguaje contiene varias respuestas esperadas interpretativas —por ejemplo, inferir rasgos de personajes a partir de acciones y explicar lenguaje figurado— y algunas pautas ofrecen ejemplos extensos.
- **Evaluación:** los ejemplos son útiles como modelo, pero el futuro evaluador no debería exigir la redacción literal ni una única interpretación cuando el texto admite más de una respuesta fundamentada.
- **Recomendación:** en la matriz de auditoría, registrar para cada respuesta abierta: elementos mínimos, evidencia textual esperada, equivalencias aceptables y errores conceptuales que sí deben penalizarse.

## Comprobaciones de muestra

- En Matemática, los ejemplos visibles 7.352 (valor posicional de 7), 3.084 (8 decenas), descomposición de 9.207 y 428 + 357 = 785 son coherentes.
- En Ciencias Naturales, las muestras sobre seres vivos/no vivos, hibernación y adaptaciones estructurales no mostraron una contradicción obvia en los fragmentos examinados.
- En Historia, las muestras sobre civilizaciones americanas, clima tropical, desierto de Atacama y clima mediterráneo fueron internamente coherentes en los fragmentos inspeccionados.
- En Lenguaje, los ejemplos de inferencia y lenguaje figurado son plausibles en la muestra; la comprobación exhaustiva de cada texto y clave sigue pendiente.

## Pendientes para completar 4.º básico

1. Revisar cada OA, explicación, ejemplo, pregunta, clave y retroalimentación de las cuatro guías.
2. Revisar pruebas de unidad y simulacros, incluidas sus pautas y recursos visuales.
3. Construir trazabilidad OA → contenido → evaluación → clave → retroalimentación.
4. Verificar afirmaciones externas de historia y ciencias con fuentes confiables y revisar adecuación cultural y de edad.
5. Registrar duplicados entre guía, pruebas y simulacros y verificar que cada imagen referenciada se renderice realmente.

## Estado
**4.º básico: primera pasada preliminar de las guías principales; no auditado por completo ni certificado.** Las observaciones son provisionales y no autorizan cambios en los archivos fuente.
