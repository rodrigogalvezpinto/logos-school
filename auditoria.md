# Auditoría consolidada — Logos School (archivo único de continuación)

**Fecha de este corte:** 22 de octubre de 2026
**Rama:** `qa/fase-2-matriz-trazabilidad` — HEAD `0106976`
**Propósito:** continuar la auditoría integral en **un solo documento**. Consolida el estado conocido (centro de control, handoff e informes de lotes existentes), regenera el inventario desde el HEAD actual y registra los **nuevos lotes auditados en esta sesión** con sus hallazgos.
**Estado global:** **EN CURSO — NO CERTIFICADA AL 100 %.**

> Reglas de este documento (heredadas del centro de control):
> - No se modifica contenido educativo ni `main` durante el diagnóstico.
> - Cada hallazgo tiene ID estable (formato `LGS-<curso>-<asig>-<n>`), evidencia, tipo, severidad, recomendación, estado y criterio de regresión.
> - Severidades: **P0** bloquea publicación / contenido erróneo que enseña algo falso o puntaje imposible; **P1** error confirmado de clave, cálculo o contradicción interna; **P2** ambigüedad o insuficiencia de estímulo que puede impedir responder; **P3** mejora de calidad, formato o redacción.
> - Estados: por revisar / validado / corregido pendiente de revalidación / revalidado / descartado / no evaluable.
> - "Revisado" aquí significa lo que cada lote declara explícitamente; no implica certificación total.

---

## 1. Inventario regenerado desde HEAD `0106976`

Conteo de archivos Markdown bajo `contenido/` por curso (guías de estudio = `.md` en la raíz del curso; pruebas de unidad = `pruebas/`; exámenes simulacro = `examenes/`):

| Curso | Guías de estudio | Pruebas de unidad | Exámenes | Régimen | Asignaturas presentes |
|---|---|---|---|---|---|
| 1.º básico | 4 | 12 | 2 (integrado Forma A + Forma B) | A — integrado 20 ítems | Lenguaje, Matemática, Ciencias, Historia |
| 2.º básico | 4 | 12 | 2 | A | ídem |
| 3.º básico | 4 | 12 | 2 | A | ídem |
| 4.º básico | 4 | 12 | 2 | A | ídem |
| 5.º básico | 5 | 14 | 5 (por asignatura, Forma B) | B — 25 ítems/asignatura | + Inglés |
| 6.º básico | 5 | 14 | 5 | B | ídem |
| 7.º básico | 5 | 14 | 5 | B | ídem |
| 8.º básico | 5 | 14 | 5 | B | ídem |
| 1.º medio | 5 | 14 | 5 | B | Lengua y Literatura, Matemática, Ciencias, Historia, Inglés |
| 2.º medio | 5 | 14 | 5 | B | ídem |
| 3.º medio | 6 | 13 | 6 | C — Decreto 193/2019 | + Filosofía, Ed. Ciudadana, Ciencias para la Ciudadanía |
| 4.º medio | 6 | 11 | 6 | C | ídem |

**Observación de inventario:** en 5.º básico–4.º medio solo existe **Forma B** de los exámenes en `examenes/`; la "Forma A" de cada asignatura vive en `pruebas/` como prueba por asignatura (convención declarada en los front-matter, p. ej. 6.º básico Matemática). En 1.º–4.º básico sí existen `examen-integrado-forma-a.md` y `-forma-b.md`. Esto es consistente con el diseño, pero cualquier comparación "Forma A vs Forma B" en Régimen B/C debe mapearse a `pruebas/<asignatura>-prueba.md`, no a un archivo `forma-a` inexistente.

---

## 2. Matriz de cobertura de auditoría por curso × asignatura

Dimensiones: **Claves/puntaje** = recálculo de respuestas y reconciliación de puntajes; **Pedagógica** = adecuación, ambigüedad, estímulos; **Curricular** = trazabilidad OA oficial → ítem; **Técnica** = importación/render/puntuación en app.

Estados: ✅ verificado en el alcance declarado · ◐ parcial (pasada o muestra) · ⬜ no iniciado · ⚠️ verificado con hallazgos abiertos.

### 1.º básico (Régimen A)
| Asignatura | Guía | Pruebas | Examen integrado A | Examen integrado B | Notas |
|---|---|---|---|---|---|
| Lenguaje | ◐ preliminar | ◐ 2.ª pasada | ⬜ | ⬜ | Definición de fonema requiere precisión (handoff §3) |
| Matemática | ◐ | ⚠️ | ⬜ | ⬜ | LGS-1B-MAT-001 abierto; regla verbal engañosa "dieci-" (16–19) |
| Ciencias | ◐ | ◐ | ⬜ | ⬜ | Formulaciones por contrastar |
| Historia | ◐ | ◐ | ⬜ | ⬜ | Ambigüedad temporal registrada (commit 0277d78) |
| Curricular / Técnica | ⬜ | ⬜ | ⬜ | ⬜ | |

### 2.º básico
| Asignatura | Guía | Pruebas | Examen integrado A | Examen integrado B |
|---|---|---|---|---|
| Lenguaje | ◐ | ⬜ | ⚠️ control mecánico de claves (2B/3B) | ⚠️ ídem |
| Matemática | ◐ informe paralelo | ⬜ | ⚠️ | ⚠️ |
| Ciencias | ◐ (mamíferos, afirmación absoluta) | ⬜ | ⚠️ | ⚠️ |
| Historia | ⬜ | ⬜ | ⚠️ | ⚠️ |
| Todos: curricular/técnica | ⬜ | ⬜ | ⬜ | ⬜ |

### 3.º básico
| Asignatura | Guía | Pruebas | Examen A | Examen B |
|---|---|---|---|---|
| Todas (4) | ◐ 3 pasadas | ◐ 2.ª pasada evaluaciones | ⚠️ control mecánico + comparativo A/B | ⚠️ ídem |
| Curricular/Técnica | ⬜ | ⬜ | ⬜ | ⬜ |

### 4.º básico
| Asignatura | Guía | Pruebas | Examen A | Examen B |
|---|---|---|---|---|
| Todas (4) | ◐ 2 pasadas | ◐ | ⚠️ comparativo A/B | ⚠️ **LGS-4B-EVAL-001 confirmado** (clave p.16: pauta dice c), el 14 está en b)) |
| Curricular/Técnica | ⬜ | ⬜ | ⬜ | ⬜ |

### 5.º básico — **completo en exámenes Forma B (esta sesión)**
| Asignatura | Guía | Pruebas | Examen Forma B |
|---|---|---|---|
| Lenguaje | ⬜ | ⬜ | ⚠️ 25/25 revisados; claves correctas; **LGS-5B-LEM-001** (11/12 claves "b") §4.5 |
| Matemática | ⬜ | ⬜ | ✅ recálculo íntegro 25/25 sin discrepancias (§4.4); claves a×7 |
| Ciencias | ⬜ | ⬜ | ✅ 25/25 revisados; puntaje 36 reconciliado (§4.6); claves b×13 |
| Historia | ⬜ | ◐ 1.ª pasada | ⚠️ **LGS-5B-EVAL-001 confirmado** (encabezado 30 pts vs pauta 35) |
| Inglés | ⬜ | ⬜ | ⚠️ 25/25 revisados; **LGS-5B-ING-001** P2 (p.8 pide disculpa en el hablante equivocado) §4.7 |

### 6.º básico — **exámenes Forma B completos (esta sesión)**
| Asignatura | Guía | Pruebas | Examen Forma B |
|---|---|---|---|
| Lenguaje | ⬜ | ⬜ | ⚠️ 25/25 revisados; **LGS-6B-LEM-001** p.5 ambigua (símil vs hipérbole) y **LGS-6B-LEM-002** p.22 cita artículo no incluido (§4.9) |
| Matemática | ◐ (LGS-6B-MAT-001, mejora guía p.4) | ⬜ | ⚠️ **Recálculo íntegro de 25/25 ítems (lote nuevo, §4.1)** — 2 hallazgos P2/P3 |
| Ciencias | ⬜ | ⬜ | ✅ 25/25 revisados; puntaje 38 reconciliado; sin hallazgos (§4.10) |
| Historia | ⬜ | ⬜ | ✅ Reconciliación de puntaje verificada 34/34 (§4.2) |
| Inglés | ⬜ | ⬜ | ✅ 25/25 revisados; sin hallazgos propios (§4.11); formato sin puntaje total → LGS-GEN-FMT-001 |

### 7.º básico — **exámenes Forma B completos (esta sesión)**
| Asignatura | Guía | Pruebas | Examen Forma B |
|---|---|---|---|
| Lengua y Literatura | ⬜ | ⬜ | ✅ 25/25 revisados; sin hallazgos (§4.12) |
| Matemática | ⬜ | ⬜ | ✅ recálculo íntegro 25/25 sin discrepancias (§4.12) |
| Ciencias | ⬜ | ⬜ | ✅ 25/25 revisados; puntaje 39 reconciliado (§4.12) |
| Historia | ⬜ | ⬜ | ✅ 25/25 revisados; puntaje 36 reconciliado (§4.12) |
| Inglés | ⬜ | ⬜ | ✅ 25/25 revisados; sin hallazgos (§4.12) |

### 8.º básico — **exámenes Forma B completos (esta sesión)**
| Asignatura | Guía | Pruebas | Examen Forma B |
|---|---|---|---|
| Lengua y Literatura | ⬜ | ⬜ | ✅ 25/25 revisados; sin hallazgos (§4.13) |
| Matemática | ⬜ | ⬜ | ✅ recálculo íntegro 25/25 sin discrepancias (§4.13) |
| Ciencias | ⬜ | ⬜ | ✅ 25/25 revisados; puntaje 39 reconciliado (§4.13) |
| Historia | ⬜ | ⬜ | ✅ 25/25 revisados; puntaje 34 reconciliado (§4.13); claves b×16/18 → LGS-GEN-KEY-001 |
| Inglés | ⬜ | ⬜ | ✅ 25/25 revisados; sin hallazgos (§4.13) |

### 1.º medio — **exámenes Forma B completos**
| Asignatura | Guía | Pruebas | Examen Forma B |
|---|---|---|---|
| Lengua y Literatura | ⬜ | ◐ 1.ª pasada principales | ✅ 25/25 revisados; sin hallazgos de contenido; **claves b×11/11** (§4.14) |
| Matemática | ⬜ | ⬜ | ✅ recálculo 12 claves de alternativas sin discrepancias (lote 1M-mat) |
| Ciencias | ⬜ | ⬜ | ⚠️ recalculado; **LGS-1M-CNT-009** P2 (bioacumulación vs biomagnificación) |
| Historia | ⬜ | ⬜ | ✅ 25/25 revisados; puntaje 34 reconciliado (§4.14) |
| Inglés | ⬜ | ⬜ | ✅ 25/25 revisados; sin hallazgos; **claves b×8/8** (§4.14) |

### 2.º medio — **exámenes Forma B completos**
| Asignatura | Guía | Pruebas | Examen Forma B |
|---|---|---|---|
| Lengua y Literatura | ⬜ | ◐ | ⚠️ 25/25 revisados; **LGS-2M-LEN-002** P2 (texto corrompido p.17, §4.15) |
| Matemática | ⬜ | ⬜ | ⚠️ recálculo 25 ítems; **LGS-2M-MAT-014 P1** (pauta x+10 vs inversa correcta x−10) |
| Ciencias | ⬜ | ⬜ | ✅ puntaje 38 reconciliado; P3 explicación soluto p.20 |
| Historia | ⬜ | ⬜ | ✅ 25/25 revisados; puntaje 37 reconciliado (§4.15) |
| Inglés | ⬜ | ⬜ | ✅ 25/25 revisados; **claves b×8/8** (§4.15) |

### 3.º medio — **exámenes Forma B completos**
| Asignatura | Guía | Pruebas | Examen Forma B |
|---|---|---|---|
| Matemática | ⬜ | ⬜ | ✅ 25/25 recalculados ítem por ítem; sin hallazgos (§4.16) |
| Lengua y Literatura | ⬜ | ◐ | ✅ 25/25 revisados; **claves b×7/7** (§4.16) |
| Ciencias p/la Ciudadanía | ⬜ | ⬜ | ✅ 25/25 revisados; puntaje 42 reconciliado; **claves b×11/13** (§4.16) |
| Filosofía | ⬜ | ⬜ | ✅ 25/25 revisados; puntaje 49 reconciliado (§4.16) |
| Ed. Ciudadana | ⬜ | ⬜ | ✅ 25/25 revisados; puntaje 124 reconciliado (§4.16) |
| Inglés | ⬜ | ⬜ | ✅ 25/25 revisados; distribución de claves sana (§4.16) |

### 4.º medio — **exámenes Forma B completos**
| Asignatura | Guía | Pruebas | Examen Forma B |
|---|---|---|---|
| Matemática | ⬜ | ⬜ | ✅ 25/25 recalculados ítem por ítem; sin hallazgos (§4.17) |
| Lengua y Literatura | ⬜ | ◐ | ✅ 25/25 revisados; sin hallazgos (§4.17) |
| Ciencias p/la Ciudadanía | ⬜ | ⬜ | ✅ 25/25 revisados; puntaje 46 reconciliado; **claves b×7/7** (§4.17) |
| Filosofía | ⬜ | ⬜ | ✅ 25/25 revisados; puntaje 51 reconciliado (§4.17) |
| Ed. Ciudadana | ⬜ | ◐ 4.ª pasada consistencia | ⚠️ 25/25 revisados; **2 hallazgos P2** (§4.17) |
| Inglés | ⬜ | ⬜ | ✅ 25/25 revisados; **claves b×5/6** (§4.17) |

### 1.º–4.º básico — **exámenes integrados completos (8 archivos)**
| Curso | Forma A | Forma B |
|---|---|---|
| 1.º básico | ✅ 20/20 correctas; obs. menor §4.18 | ✅ 20/20 correctas (§4.18) |
| 2.º básico | ✅ 20/20 correctas; **claves b×15/20** | ✅ 20/20 correctas (§4.18) |
| 3.º básico | ✅ 20/20 correctas | ✅ 20/20 correctas; estímulos compartidos con Forma A (§4.18) |
| 4.º básico | ✅ 20/20 correctas; **claves b×16/20** | ⚠️ 19/20; **LGS-4B-EVAL-001 P1 reconfirmado** (§4.18) |

### Pruebas de unidad — **1B–1M completas (104 archivos, ~1.265 ítems)**
| Curso | Pruebas | Resultado |
|---|---|---|
| 1.º básico | 12/12 | ✅ ~85 ítems correctos; LGS-1B-INT-001 también aparece en `historia-unidad-historia.md` p.1 (propagación del ítem ambiguo) |
| 2.º básico | 12/12 | ✅ ~87 ítems correctos; sin hallazgos |
| 3.º básico | 12/12 | ✅ ~95 ítems correctos; sin hallazgos |
| 4.º básico | 12/12 | ✅ ~85 ítems correctos; sin hallazgos (la prueba de patrones usa x+6=14 marcada correctamente — el error del examen no viene de aquí) |
| 5.º básico | 14/14 | ✅ ~140 ítems correctos; sin hallazgos |
| 6.º básico | 14/14 | ✅ ~150 ítems correctos; sin hallazgos |
| 7.º básico | 14/14 | ✅ ~185 ítems correctos; sin hallazgos |
| 8.º básico | 14/14 | ✅ ~190 ítems correctos; sin hallazgos |
| 1.º medio | 14/14 | ✅ ~190 ítems correctos; sin hallazgos |
| 2.º medio | 14/14 | ✅ ~195 ítems correctos; sin hallazgos |
| 3.º medio | 13/13 | ✅ ~185 ítems correctos; sin hallazgos |
| 4.º medio | 11/11 | ✅ ~160 ítems correctos; sin hallazgos |

**Lectura honesta de la matriz:** quedan revisados ítem por ítem **los 40 exámenes + 104 pruebas de unidad (1B–1M)**. Pendientes: pruebas de 2M–4M (38 archivos), guías de estudio con bancos integrados (55 archivos), trazabilidad OA→temario oficial y validación pedagógica por especialistas.

---

## 3. Registro maestro de hallazgos (consolidado)

| ID | Curso / recurso | Tipo | Sev. | Hallazgo | Estado |
|---|---|---|---|---|---|
| LGS-1B-MAT-001 | 1B, prueba medición p.2 | Estímulo insuficiente | P2 | Ordenar objetos por longitud sin medidas ni imagen inequívoca | Documentado; verificar render |
| LGS-1B-LEM-001 | 1B, guía Lenguaje | Precisión conceptual | P2 | Definición de fonema requiere precisión | Por revisar |
| LGS-1B-MAT-002 | 1B, guía Matemática | Error de redacción | P2 | Regla "números del 11 al 19 empiezan con dieci-" — solo aplica a 16–19 | Por revisar |
| LGS-1B-HIS-001 | 1B, Historia | Ambigüedad temporal | P2 | Registrada en commit 0277d78 | Por revisar |
| LGS-1B-PCD-001 | 1B, simulacro (cuento) | Seguridad/modelado | P3 | Personaje da leche a gato callejero; reformular hacia agua + ayuda adulta | Por revisar |
| LGS-2B-CNT-001 | 2B, Ciencias | Afirmación absoluta | P3 | "Los mamíferos nacen de crías" sin matices (ornitorrinco/echidna) | Por revisar |
| LGS-2B-EST-001 | 2B, evaluación | Reutilización de estímulo | P3 | Registrada en commit e3a9ea0 | Por revisar |
| LGS-4B-EVAL-001 | 4B, examen integrado Forma B p.16 | Clave errada | **P1** | Pauta indica c) 14; el valor 14 está en b) | Confirmado; corrección + regresión pendientes |
| LGS-5B-EVAL-001 | 5B, Historia Forma B | Puntaje inconsistente | **P1** | Encabezado declara 30 puntos; pauta/distribución suman 35 | Confirmado; corrección + regresión pendientes |
| LGS-5B-HIS-001 | 5B, Historia | Ambigüedad de alcance | P3 | Registrada en commit 584cf92 | Por revisar |
| LGS-6B-MAT-001 | 6B, guía Matemática p.4 | Retroalimentación incompleta | P3 | División con residuo (2.050 botellas, cajas de 12, 3 distribuidores) no explica el resto | Documentado |
| LGS-6B-MAT-002 | 6B, Matemática Forma B p.24 | Estímulo insuficiente | **P2** | Pregunta por "el trimestre con más asistentes de Música" sobre 4 trimestres, pero el enunciado solo entrega datos de los trimestres 1 y 2; la pauta responde T2 sin poder descartar T3/T4 | **Nuevo — confirmado en §4.1** |
| LGS-6B-MAT-003 | 6B, Matemática Forma B | Distribución de claves | P3 | 10 de las 12 preguntas de alternativas tienen clave "a" (patrón detectable por estudiantes) | **Nuevo — confirmado en §4.1** |
| LGS-2M-MAT-014 | 2M, Matemática Forma B p.14 | Contradicción clave/pauta | **P1** | Alternativa correcta x−10; pauta escribe x+10 | Confirmado; añadir al validador |
| LGS-2M-LEN-002 | 2M, Lengua Forma B p.17 | Texto corrompido | **P2** | La pregunta cita la expresión «ya no hay welcome de vuelta» donde el texto dice «ya no hay vuelta atrás»; palabra en inglés insertada por error | **Nuevo — confirmado en §4.15** |
| LGS-4M-EDC-001 | 4M, Ed. Ciudadana Forma B | Puntaje inconsistente | **P2** | Pauta declara total 55 puntos; la suma de la propia tabla da 56 (10×1 + 4×4 V/F + 2×4 pareados + 5×2 breve + 4×3 extenso) | **Nuevo — confirmado en §4.17** |
| LGS-4M-EDC-002 | 4M, Ed. Ciudadana Forma B p.9 | Clave V/F discutible | **P2** | Pauta marca F a «el respeto a la igual dignidad no está sujeto al mismo tipo de debate que las políticas económicas», cuando la doctrina de DD.HH. (y otras preguntas del propio examen, p. ej. nota de neutralidad) la tratan como piso no negociable → debería ser V o el ítem debe reescribirse | **Nuevo — confirmado en §4.17** |
| LGS-1B-INT-001 | 1B, examen integrado Forma A p.3 | Enunciado confuso | P3 | «¿Qué haces primero en la mañana?» con clave «Dormir toda la noche» — técnicamente es lo que precede al día, no lo primero de la mañana; un niño puede confundirse | **Nuevo — §4.18** |
| LGS-3B-INT-001 | 3B, examen integrado Forma A p.20 | Precisión histórica menor | P3 | «En 1989… incluido Chile, firmaron» la Convención sobre los Derechos del Niño: Chile la firmó/ratificó en 1990; para el nivel el ítem funciona, pero la fecha incluida al país es imprecisa | **Nuevo — §4.18** |
| LGS-3B-INT-002 | 3B, exámenes integrados | Estímulos compartidos entre formas | P3 | Formas A y B reutilizan los mismos 3 textos base (cometa de Joaquín, huerta de mi tía, pingüinos de Humboldt) con preguntas distintas; reduce el valor de «segunda práctica independiente» | **Nuevo — §4.18** |
| LGS-GEN-KEY-002 | 2B, 4B, varios cursos | Distribución de claves | P3 | Sesgo global de claves «b» confirmado en todo el corpus: 2B-A b×15/20, 4B-A b×16/20, 1M-Lengua b×11/11, 2M-Inglés b×8/8, 3M-Lengua b×7/7, 4M-Ciencias b×7/7, entre otros | **Nuevo — patrón sistémico** |
| LGS-1M-CNT-009 | 1M, Ciencias Forma B p.9 | Confusión conceptual | P2 | Pauta confunde bioacumulación con biomagnificación | Confirmado; verificar enunciado |
| LGS-2M-CNT-020 | 2M, Ciencias Forma B p.20 | Explicación imprecisa | P3 | "Menor cantidad" no define soluto por sí sola; clave correcta | Por revisar |
| LGS-GEN-FMT-001 | Transversal exámenes | Inconsistencia de formato | P3 | Historia (5B/6B) incluye columna Puntaje + escala de nota; Matemática e Inglés (6B) no incluyen puntaje por ítem ni total. Criterio de asignación de puntaje no uniforme entre asignaturas del mismo curso | **Nuevo — documentado en §4.3** |
| LGS-5B-LEM-001 | 5B, Lenguaje Forma B | Distribución de claves | P2 | 11 de 12 preguntas de alternativas tienen clave "b" (1 es "c"); patrón trivialmente explotable por el estudiante | **Nuevo — confirmado en §4.5** |
| LGS-5B-ING-001 | 5B, Inglés Forma B p.8 | Ítem inconsistente | P2 | El diálogo "— I broke your pencil. — ___, don't worry" ubica la disculpa en el hablante equivocado: quien rompió el lápiz es el primer hablante; la pauta "I'm sorry" no calza con "don't worry" del mismo turno | **Nuevo — confirmado en §4.7** |
| LGS-6B-LEM-001 | 6B, Lenguaje Forma B p.5 | Ítem ambiguo | P2 | El verso "como si tuviera mil años de viaje" combina "como si" (símil) con "mil años" (hipérbole); b) y d) son defendibles. Pauta elige b) sin justificar por qué no es hipérbole | **Nuevo — confirmado en §4.9** |
| LGS-6B-LEM-002 | 6B, Lenguaje Forma B p.22 | Estímulo faltante | P2 | La pregunta evalúa el segundo párrafo del artículo "El pudú…" que **no está incluido** en el examen ("visto en clases"); el ítem no es respondible en forma autónoma | **Nuevo — confirmado en §4.9** |
| LGS-GEN-KEY-001 | Transversal exámenes | Distribución de claves | P3 | Desbalance sistemático de letras correctas observado en todas las Formas B revisadas: 6B-MAT a×10/12; 5B-MAT a×7, d×0; 5B-LEM b×11/12; 5B-CNT b×13/17; 5B-ING b×7/10. Riesgo acumulado de adivinanza por patrón | **Nuevo — consolidado en §4.8** |
| LGS-4B-LEM-001 | 4B, guía Lenguaje OA 5 | Inconsistencia interna | P3 | El Ejemplo 2 clasifica «sus laderas verdes parecen un poncho» como **metáfora**, pero la autoevaluación p.5 lo clasifica (correctamente) como **comparación** por usar «parecen» — el propio material se contradice sobre el mismo verso | **Nuevo — §4.21** |
| LGS-7B-MAT-001 | 7B, guía Matemática OA 16 Ej.1 | Tabla inconsistente con datos | **P2** | Los datos listados (20 valores) contienen 9 unos y 2 treses, pero la tabla de frecuencias declara 8 unos y 3 treses (frecuencias relativas correspondientes también erradas: 40%/15% vs reales 45%/10%). El ejemplo "resuelto" no se reproduce al contar los datos | **Nuevo — §4.24** |
| LGS-7B-ING-001 | 7B y 1M, guías de Inglés (7B OA 9 banco p.2; 1M OA 9 banco p.3) | Precisión factual menor | P3 | Ambas guías repiten la afirmación «The Amazon rainforest produces about 20% of the world's oxygen» — mito popular: la contribución neta del Amazonas al O₂ atmosférico es cercana a cero (su ecosistema consume la mayor parte del que produce); la cifra del ~20% aun siendo bruta está sobreestimada (~6-9% de la fotosíntesis global). Funciona para el ejercicio de lectura, pero enseña un dato científicamente impreciso; además sugiere reutilización del mismo texto entre cursos sin revisión factual | **Nuevo — §4.25, ampliado §4.27** |
| LGS-8B-LEM-001 | 8B, guía Lengua OA 8 texto "La noche del río" | Precisión factual menor | P3 | El relato ambienta la acción «la madrugada del 22 de mayo de 1960» en Valdivia, pero el terremoto de mayor magnitud registrado ocurrió a las ~15:11 hora local (tarde), no de madrugada. Como la guía explícitamente lo presenta como «hecho histórico real» para el análisis de contexto, la hora inventada contradice el dato real que se enseña | **Nuevo — §4.26** |
| LGS-8B-HIS-001 | 8B, guía Historia OA 4 autoevaluación p.1 | Errata en inglés | P3 | La opción d) dice «Por la cantidad de **population** que vivía en sus ciudades» — palabra en inglés dentro de una alternativa en español (debe ser «población»). Distractor incorrecto de todos modos, pero la errata es visible para el estudiante | **Nuevo — §4.26** |
| LGS-1M-LEN-001 | 1M, guía Lengua OA 3 Ej.1 | Errata en inglés | P3 | El análisis del padre dice «su acción… ante el tema —**information** implícita—» en vez de «información» — misma clase de errata que LGS-8B-HIS-001 y LGS-2M-LEN-002; sugiere un patrón de generación de texto | **Nuevo — §4.27** |
| LGS-1M-CNT-010 | 1M, guía Ciencias OA 8 retro p.5 | Errata en inglés | P3 | La retroalimentación dice «Evaluar una acción humana desde sus tres **dimensions**» en vez de «dimensiones» — tercera aparición del patrón de erratas en inglés | **Nuevo — §4.27** |
| LGS-1M-CNT-011 | 1M, guía Ciencias OA 11 banco p.7 | Imprecisión física | P3 | La respuesta modelo compara el efecto Doppler sonoro con el lumínico y escribe «más agudo/**rojo** al acercarse, más grave/rojo al alejarse»: al acercarse el corrimiento es hacia el **azul**, no al rojo (rojo solo al alejarse). El propio Ejemplo 3 del OA lo explica correctamente | **Nuevo — §4.27** |
| LGS-2M-ING-001 | 2M, guía Inglés OA 13 Ej.3 | Uso ilógico de conector | P3 | El ejemplo de «unless» dice «she has achieved real change **unless** the government ignores her proposals» — la lógica queda invertida (debería ser «because» o «even if»; «unless» significa «a menos que», lo que da un sentido contraproducente). Gramaticalmente bien formado pero semánticamente enseña un uso erróneo del conector | **Nuevo — §4.28** |
| LGS-2M-CNT-022 | 2M, guía Ciencias OA 10 explicación | Errata de tipeo | P3 | «la **fuerza neta** (o fuerza resultante):la suma vectorial» — falta espacio tras los dos puntos. Trivial, sin efecto pedagógico | **Nuevo — §4.28** |
| LGS-3M-ING-001 | 3M, guía Inglés retroalimentación p.14 | Errata léxica | P3 | La retroalimentación dice «"**común** practice"» en vez de «common practice» — mezcla la palabra española «común» dentro de una frase en inglés (variante inversa del patrón de anglicismos: aquí es hispanismo dentro de inglés). Gramática de la guía correcta en todo lo demás | **Nuevo — §4.29** |

Hallazgos P0: **ninguno conocido**. P1 abiertos: **3** (4B-EVAL-001, 5B-EVAL-001, 2M-MAT-014).

---

## 4. Lotes nuevos auditados en esta sesión

### 4.1 Lote — 6.º básico, Matemática, examen Forma B (recálculo íntegro)

**Archivo:** `contenido/06-basico/examenes/matematica-examen-forma-b.md`
**Método:** recálculo independiente de los 25 ítems contra su pauta; conteo de tipos de pregunta y cobertura de OA.

**Resultado por ítem:**

| N° | Pauta | Recálculo | Veredicto |
|---|---|---|---|
| 1 | a) 5.460.000 | 1.560 × 3.500 = 5.460.000 | ✅ |
| 2 | 9 buses, sobran $800.000 | 39.500.000 ÷ 4.300.000 = 9,18 → 9; 9×4,3M = 38,7M; resto 800.000 | ✅ |
| 3 | b) 5:3 | 20:12 ÷ 4 | ✅ |
| 4 | 20 botones | 8÷2=4; 5×4=20 | ✅ |
| 5 | c) 3/4 | 75/100 ÷ 25 | ✅ |
| 6 | a) $1.600 | 0,2 × 8.000 | ✅ |
| 7 | 99 | 0,55 × 180 | ✅ |
| 8 | a) 4 3/4 | 19÷4 = 4 r3 | ✅ |
| 9 | 3 2/3 | 33÷9 = 3 r6 → 3 6/9 = 3 2/3 | ✅ |
| 10 | a) 7 1/2 | 5 4/6 + 1 5/6 = 6 9/6 = 7 1/2 | ✅ |
| 11 | 17.750 kg (encargado erró) | 32,400 − 14,650 = 17,750 | ✅ |
| 12 | a) 54 | 100 − 46 | ✅ |
| 13 | x = 37 | 52 − 15, comprobación 37+15=52 | ✅ |
| 14 | b) 118° | 180 − 62 (ángulos adyacentes suplementarios) | ✅ |
| 15 | 58°, 122°, 122° | opuestos por vértice iguales; adyacentes suplementarios | ✅ |
| 16 | a) 486 cm² | 6 × 9² = 486 | ✅ |
| 17 | 248 cm² | 2(60)+2(40)+2(24) = 248 | ✅ |
| 18 | 1.350 cm² | 6 × 15² | ✅ |
| 19 | a) 125 cm³ | 5³ | ✅ |
| 20 | 35 m³ | 5 × 3,5 × 2 | ✅ |
| 21 | a) 40 | 160 ÷ 4 sectores equiprobables | ✅ |
| 22 | 6 | 3 × 2 | ✅ |
| 23 | a) 110 | 0,44 × 250 | ✅ |
| 24 | T2, +22 | 52 − 30 = 22 — **pero ver LGS-6B-MAT-002** | ⚠️ |
| 25 | 720.000 / 630.000 / 450.000 | 40/35/25% de 1,8M; suma 1.800.000 ✓ | ✅ |

**Chequeos estructurales:** 25 preguntas declaradas = 25 presentes; tipos 12 alternativas + 13 desarrollo = 25 ✓; tabla de cobertura suma 11+2+2+10 = 25 y 11 OA distintos ✓.

**Hallazgos nuevos:**
- **LGS-6B-MAT-002 (P2):** pregunta 24 afirma que el gráfico compara "durante 4 trimestres" pero el enunciado solo da datos de T1 y T2. La pauta responde "trimestre 2" sin datos de T3/T4. Corrección sugerida: indicar "de los trimestres con datos" o agregar T3/T4 al enunciado. Regresión: ítem respondible de forma inequívoca solo con lo impreso.
- **LGS-6B-MAT-003 (P3):** distribución de claves de alternativas: a×10, b×2, c×1, d×0 (de 12). Riesgo de patrón explotable; sugerido rebalancear en una corrección autorizada. Regresión: ninguna clave > ~40 % del total.

**Pendiente en este archivo:** cotejo de OA citados contra Bases Curriculares oficiales, comparación de dificultad con la Forma A (`pruebas/matematica-prueba.md` aún no existe como archivo `forma-a` en `examenes/`), y QA de importación/render.

### 4.2 Lote — 6.º básico, Historia/Geografía/Cs. Sociales, examen Forma B (reconciliación de puntaje)

**Archivo:** `contenido/06-basico/examenes/historia-geografia-y-cs-sociales-examen-forma-b.md`
**Método:** verificación del mismo defecto confirmado en 5B (LGS-5B-EVAL-001): encabezado vs. pauta vs. distribución.

**Resultado:** encabezado declara **34 puntos**; pauta suma 18 alternativas × 1 + 5 desarrollo breve × 2 + 2 desarrollo extenso × 3 = 18+10+6 = **34**; tabla de distribución por eje suma 34 puntos y 25 preguntas. **Consistente — sin hallazgo.** La escala de conversión es referencial y está correctamente rotulada como tal.

**Pendiente:** corrección disciplinar ítem por ítem (contenido histórico) y cotejo de OA.

### 4.4 Lote — 5.º básico, Matemática, examen Forma B (recálculo íntegro)

**Archivo:** `contenido/05-basico/examenes/matematica-examen-forma-b.md` — 25 ítems recalculados uno a uno. **Resultado: 25/25 correctos, sin hallazgos de exactitud.** Verificados: valor posicional (centena de mil para el 8 en 5.847.900), orden y descomposición, 52×38=1.976, 187÷5=37 r2, 245÷9→28 buses, vuelto $4.660, gasto $14.340, equivalencia 4/6, comparación 10/15>9/15, decimal 0,75, orden de decimales (6,02<6,2<6,205<6,25), 2,85 km, secuencia +7→40, x=220, x−480=650→1.130, caras paralelas, rotación congruente, 32 mm=3,2 cm=0,032 m, área triángulo 40 cm², trapecio 80 m², promedio 6,0, jueves $15.000, "poco posible" (2/9), abril y total 95. Cobertura 13+3+2+7=25, 17 OA ✓. Distribución de claves: a×7, b×4, c×1, d×0 — se suma a LGS-GEN-KEY-001.

### 4.5 Lote — 5.º básico, Lenguaje y Comunicación, examen Forma B

**Archivo:** `contenido/05-basico/examenes/lenguaje-y-comunicacion-examen-forma-b.md` — 25 ítems revisados contra sus textos de estímulo. Claves de alternativas correctas (rima asonante casa/cama ✓, metáfora "el cielo es un lienzo" ✓, kril ✓, ballena franca Biobío julio-octubre ✓, propósito del afiche ✓). Ítems de desarrollo con criterios de pauta adecuados. Conteos: 12 alternativas + 7 breve + 6 extenso = 25 ✓; distribución OA 4+4+5+4+4+4=25 ✓.
**Hallazgo LGS-5B-LEM-001 (P2):** 11 de 12 claves son "b". Regresión sugerida: ninguna letra > ~40 %.
Nota positiva: los dos cuentos de estímulo modelan conducta segura (no alimentar al animal silvestre, acudir a adulta experta) — corrige el patrón criticado en LGS-1B-PCD-001.

### 4.6 Lote — 5.º básico, Ciencias Naturales, examen Forma B

**Archivo:** `contenido/05-basico/examenes/ciencias-naturales-examen-forma-b.md` — 25 ítems revisados. Claves correctas en los 17 ítems de alternativas (niveles de organización, nutrientes, tabaco, microorganismos, conductores/aisladores, agua dulce, contaminación). Puntaje reconciliado: 17×1+5×2+3×3=36 = declarado ✓. Distribución 4+4+3+4+4+3+3=25 ✓.
Observación menor (no registrada como hallazgo): p.9 presenta el asma como enfermedad "relacionada con el consumo de tabaco"; aunque el tabaco es desencadenante y no causa única, la alternativa es la única respiratoria plausible y el distractor funciona. Claves: b×13, c×4 — se suma a LGS-GEN-KEY-001.

### 4.7 Lote — 5.º básico, Inglés, examen Forma B

**Archivo:** `contenido/05-basico/examenes/ingles-examen-forma-b.md` — 25 ítems revisados. 24/25 correctos o con criterio de pauta adecuado.
**Hallazgo LGS-5B-ING-001 (P2):** p.8 "— I broke your pencil. — ___, don't worry." La disculpa corresponde al primer hablante (quien rompió el lápiz); el segundo turno debería ser una expresión de tranquilidad ("It's OK", "No problem"). La pauta acepta "I'm sorry", que produce un diálogo incoherente ("I'm sorry, don't worry"). Corrección sugerida: invertir los turnos o aceptar "That's OK". Claves MC: b×7, c×2, d×1, a×1 — se suma a LGS-GEN-KEY-001. Puntaje: "todas valen igual" — criterio válido aunque no hay total declarado (ver LGS-GEN-FMT-001).

### 4.8 Observación transversal — desbalance sistemático de claves (LGS-GEN-KEY-001)

En las 5 Formas B recalculadas ítem por ítem hasta ahora, la letra correcta se concentra fuertemente en una o dos opciones: 6B-MAT a×10/12 · 5B-MAT a×7/12, d×0 · 5B-LEM b×11/12 · 5B-CNT b×13/17 · 5B-ING b×7/10. Un estudiante que marca la letra dominante acertaría 60–90 % de las alternativas sin saber el contenido. **Severidad P3 global / P2 en casos extremos (5B-LEM).** Recomendación: incluir en la corrección autorizada un rebalanceo de claves y añadir al validador CI una regla de frecuencia máxima por letra (p. ej. ≤ 45 %).

### 4.9 Lote — 6.º básico, Lenguaje y Comunicación, examen Forma B

**Archivo:** `contenido/06-basico/examenes/lenguaje-y-comunicacion-examen-forma-b.md` — 25 ítems revisados contra sus estímulos. Conteos: 11 alternativas + 2 V/F + 6 breve + 6 extenso = 25 ✓; OA 4+4+5+4+4+4=25 ✓. Cálculo de tabla verificado: (120+310+280+90)/4 = 200 litros ✓.
- **LGS-6B-LEM-001 (P2):** p.5 ofrece como distractores "Comparación (símil)" e "Hipérbole" para un verso que contiene ambas ("como si" + "mil años"). Corrección: quitar una de las dos opciones o usar un verso con una sola figura.
- **LGS-6B-LEM-002 (P2):** p.22 pregunta por el segundo párrafo de un artículo sobre el pudú "visto en clases" que no se incluye en el documento. Un postulante sin ese material no puede verificar la clave b). Corrección: incluir el texto o sustituir por un ítem autocontenido.
Claves MC: a×4, b×7 — parcialmente balanceado.

### 4.10 Lote — 6.º básico, Ciencias Naturales, examen Forma B

**Archivo:** `contenido/06-basico/examenes/ciencias-naturales-examen-forma-b.md` — 25 ítems revisados. Correctos: fotosíntesis (algas/cianobacterias, glucosa como producto), niveles tróficos (tiburón C3 ✓), pubertad (estirón común ✓), energía, geotérmica renovable ✓, condensación ✓, evaporación vs ebullición ✓, atmósfera ✓, erosión eólica ✓. Puntaje reconciliado: 16×1+5×2+4×3=38 = declarado ✓. Distribución 7×3+2×2=25 ✓. **Sin hallazgos.** Claves: b×10/16.

### 4.11 Lote — 6.º básico, Inglés, examen Forma B

**Archivo:** `contenido/06-basico/examenes/ingles-examen-forma-b.md` — 25 ítems revisados: todas las claves y respuestas modelo correctas (swim, between…, can/can't, at 5 pm, once upon a time, are playing, geese, but, eighteen). Estructura 10 MC + 15 abiertas = 25 ✓, 5 OA × 5 ✓. **Sin hallazgos propios.** No declara puntaje total (ver LGS-GEN-FMT-001). Claves: b×7, c×3.

### 4.12 Lote — 7.º básico, las 5 asignaturas, exámenes Forma B

**Matemática** (`07-basico/examenes/matematica-examen-forma-b.md`): recálculo íntegro 25/25 — todos correctos (−450 m; $18.000; 1.285 m; 1/7; 24; 10 porciones; $7.000; $540.000; $58.650 tras alza+descuento sucesivos; 2x+7; 4n+1; 22 y 23; $15.000; proporción inversa; 4 días; 7 cm; 314 cm²; 706,5 m²; Cuadrante III; (−4,1); 25%; tallo y hojas; tabla de frecuencias 42,9/28,6/14,3/14,3; 1/8; 80%). Cobertura 9+6+5+5=25, 9 OA ✓. Observación menor: la suma de porcentajes redondeados de la p.23 da 100,1 %; la pauta lo declara como aproximado, aceptable.
**Lengua y Literatura**: 25/25 revisados; claves correctas (conflicto del violín, flashback, olfato, personificación, Valdivia 1960, postura de la columna, prejuicio etario, función de conectores). V/F y desarrollos bien criteriados. Conteos 9+2+8+6=25 ✓.
**Ciencias Naturales**: 25/25 revisados; correctos (aspecto social de la sexualidad; preservativo como barrera; días fértiles ~11–16 en ciclo de 28; Penicillium como hongo; roce-rugosidad; límite divergente; Gay-Lussac a volumen constante; sustancia pura). Puntaje 15+12+12=39 reconciliado ✓.
**Historia**: 25/25 revisados; correctos (neolítico multipoligenético; excedente; oligarquía; esclavitud romana; tradición germana; mayas→canales / chinampas→aztecas como distractor correcto; república romana; tolerancia religiosa Roma/Inca). Puntaje 16×1+7×2+2×3=36 reconciliado ✓.
**Inglés**: 25/25 revisados; correctos (main idea pingüinos; three years; instructions; cause-effect; Last summer; learned; quietly; Those books are; are). Estructura 8 MC + 17 abiertas = 25 ✓, 4 OA ✓.
**Sin hallazgos nuevos en 7.º básico.** Claves MC: MAT b×7/13 · LEN b×7/9 · CNT b×12/15 · HIS b×11/16 · ING b×5/8 — persiste el sesgo hacia "b" (LGS-GEN-KEY-001).

### 4.13 Lote — 8.º básico, las 5 asignaturas, exámenes Forma B

**Matemática** (`08-basico/examenes/matematica-examen-forma-b.md`): recálculo íntegro 25/25 — todos correctos (−54; −$34.000; 0,9; −6 m/min; 5²; 10⁴=10.000; √169=13; √110 entre 10 y 11; lado 8 m y perímetro 32 m; x=12; x=9; 20 gigas; f(5)=−4; pendiente 4 corte (0,−7); S(7)=$151.500; hipotenusa 17; 12 m; 10-24-26 rectángulo; N'(−2,−2); S'(−6,−2); percentil 80; Q1=24 y Q3=40; interpretación de bigotes; gráfico circular; eje truncado). Cobertura 9+6+5+5=25, 10 OA ✓. Claves a×9/11.
**Lengua y Literatura**: 25/25 revisados; correctos (conflicto imagen/saber oculto; personaje tipo sabio; narrador≠autor; personificación; Chaitén 2008 real; postura e imperativo/subjuntivo de la columna; 24.000 habitantes; registro informal vs formal; corrección "se maquillaron a sí mismas / nos explicó / las tareas estaban mal hechas / rehacerlas"). Conteos 10+2+7+6=25 ✓.
**Ciencias Naturales**: 25/25 revisados; correctos (núcleo/ADN; procarionte sin núcleo; ósmosis; fotosíntesis solo de día; nefrón; leucocitos; proteínas=constructor; 200 V; serie se interrumpe; I=5 A; radiación sin medio; Thomson=electrón; Rutherford núcleo denso; metales conductores; CaBr₂ iónico). Puntaje 15+12+12=39 reconciliado ✓.
**Historia**: 25/25 revisados; correctos (Lutero 1517; Galileo; burocracia real; proteccionismo; monopolio a la metrópoli; de las Casas; encomienda; transculturación; malones; Rousseau; secularización/Voltaire; cargos peninsulares; San Martín; Patagonia por factores físicos; migración joven→escasez laboral; aislamiento y salud; ventaja comparativa; soberanía en la nación; DDHH 1789 y límites). Puntaje 18×1+5×2+2×3=34 reconciliado ✓; escala de nota presente. **Claves: b×16/18 — el desbalance más extremo observado hasta ahora** (LGS-GEN-KEY-001).
**Inglés**: 25/25 revisados; correctos (video tutorials; about/by; False resumen; Italy/13/painting; expand question; persuade; so; True condición; lighter; discussion; also=adds info; prefer/to; traveled/was; a lot of; is going to rain; get off/arrive at). 7 MC + 18 abiertas = 25 ✓.
**Sin hallazgos nuevos de contenido en 8.º básico.**

### 4.14 Lote — 1.º medio, Lengua/Historia/Inglés, exámenes Forma B

**Lengua y Literatura** (`01-medio/examenes/lengua-y-literatura-examen-forma-b.md`): 25/25 revisados; claves y criterios correctos (conflicto Antonia; abuela como mentora; efecto 3.ª persona; símbolo del horno; pañuelo; presagios; mito de la Pincoya; sobreexplotación pesquera; tesis de la columna IA; propósito implícito municipal; coherencia temática). Conteos 11+2+7+5=25 ✓. **Claves MC: b×11/11 — 100 % una sola letra**, el peor caso de la auditoría (LGS-GEN-KEY-001).
**Historia**: 25/25 revisados; correctos (abolicionismo Chile 1823/GB 1833; libre asociación; unificación italiana; crisis de la idea de progreso; pelucones/estanqueros; trigo a California y Australia; salitre capital-intensivo; Temuco 1881; Bolivia sin litoral; tensión salitrera; ausencia de legislación laboral; Santa María de Iquique 1907; Gay/Domeyko; monopolio; inflación; socialcristianismo; Rapa Nui; lluvia ácida). Puntaje 18×1+5×2+2×3=34 reconciliado ✓. Claves b×12/18.
**Inglés**: 25/25 revisados; correctos (Franklin explícito; about/how; False abejas; 1930 Uruguay; Chilean/1889/Nobel; infer context; persuade; However; True problema-solución; irresponsible; artist; both…and; In my opinion; studied/enjoyed; two million; has taught since; disappear; who/which; has been a firefighter). **Claves MC: b×8/8 — 100 %** (LGS-GEN-KEY-001).

### 4.15 Lote — 2.º medio, Lengua/Historia/Inglés, exámenes Forma B

**Lengua y Literatura** (`02-medio/examenes/lengua-y-literatura-examen-forma-b.md`): 25/25 revisados; claves correctas en su contenido. **Hallazgo LGS-2M-LEN-002 (P2)**: la pregunta 17 contiene un texto corrompido — dice "la expresión «ya no hay welcome de vuelta»" donde debía decir "ya no hay vuelta atrás" (palabra en inglés "welcome" insertada por error); la pauta sí cita el texto correcto. Confunde al estudiante al citar una frase que no existe en la columna. Conteos 9+2+8+6=25 ✓. Claves b×8/9.
**Historia**: 25/25 revisados; correctos (Gran Depresión 1929; DUDH 1948; radio/cine/deporte; Muro de Berlín 1961; Guerra Fría ideológica; Revolución Cubana 1959; Perestroika/Glasnost; interpretaciones golpe 1973; desaparición forzada; supresión Estado de Derecho; Plan Laboral; crisis 1982; Comisión Rettig; continuidad transición; mortalidad infantil/callampas; universalidad DD.HH.; discriminación por nacionalidad; oportunidades tecnología). Puntaje 15×1+8×2+2×3=37 reconciliado ✓. Manejo cuidadoso del eje dictadura (instrucción 7).
**Inglés**: 25/25 revisados; correctos (prótesis 3D explícito; about/how; False turbinas; 1971 email; Goodall; infer context; persuade; Unless; problema-solución; inconvenient; illegal; neither/nor; In my opinion; I'd rather; studied/found; ejemplo Suecia; resumen ingeniero; few; presente perfecto continuo; impatient; pasado perfecto; Every weekend; had painted; himself). **Claves MC: b×8/8 — 100 %** (LGS-GEN-KEY-001).

### 4.16 Lote — 3.º medio (Régimen C), 6 exámenes Forma B

**Matemática**: 25/25 recalculados ítem por ítem — todos correctos (decibeles L=10·log(100)=20; b=1 constante; crecimiento compuesto; razones ≈1,2; 0,75⁴≈0,3164→57 mg; log(0,5)/log(0,88)≈5,4 años; arcos y ángulos 130/70/48/60; cuerdas 5·8=4·x→10; secantes (150−50)/2=50; tangente²=8·18=144; tangente²=6·15=90→√90; rango 11; varianza 8/3; σ=√5≈2,24; 5/8·4/7=5/14; 70/115; prob. total 0,124).
**Filosofía**: 25/25 revisados; correctos (quehacer desde lo cotidiano; ontología materialismo; epistemología dogmático/escéptico/crítico; inducción; ornitorrinco inválido; falsa dicotomía; apelación a autoridad; fenomenología/mayéutica). Puntaje 17×1+4×3+4×5=49 reconciliado ✓.
**Lengua y Literatura**: 25/25 revisados; correctos (personificación "devoraba"; reportaje vs noticia; rol @profe_x; cohesión/progresión temática). **Claves b×7/7 — 100 %**.
**Ciencias p/la Ciudadanía**: 25/25 revisados; correctos (transgénicos consenso; influenza deriva antigénica; benzodiazepinas+alcohol; SENAPRED Ley 21.364; origen antropogénico incendios). Puntaje 13+14+15=42 reconciliado ✓. Observación menor: p.19 clasifica simulacros como "mitigación" (otros marcos los llaman "preparación") — aceptable pero revisable.
**Ed. Ciudadana**: 25/25 revisados; correctos (soberanía popular; CAJ vs Defensoría Penal; Corte Suprema; indivisibilidad; deber de proteger; comunitarismo/republicanismo; plan regulador; Delegado Presidencial Provincial; censo). Puntaje 16×4+6×6+3×8=124 reconciliado ✓. Escala de logro incluida.
**Inglés**: 25/25 revisados; correctos (whereas; although; dates back to; friluftsliv; fast fashion; On the other hand; oración temática; voz pasiva "are organized"; that/which; is celebrated). Distribución de claves variada (a×1, b×3, c×1) — la mejor de la auditoría.

### 4.17 Lote — 4.º medio (Régimen C), 6 exámenes Forma B

**Matemática**: 25/25 recalculados ítem por ítem — todos correctos (interés simple lineal; TEA 21,94%; CAE; 900.000×1,04⁵≈1.094.990; sueldo +4% vs IPC 6%; 5x⁴ → factor 81; 1.200/d²; T(t)=3cos+27 → máx 30/mín 24/período 24; normal 95%; μ=np=5; C(8,6)/2⁸=10,94%; σ=√8,73≈2,95; μ±3σ=36–84; prob. total 0,078).
**Filosofía**: 25/25 revisados; correctos (alcances/límites filosofía; mérito vs igualdad sustantiva; utilitarismo; libertad positiva; falacias generalización apresurada + falsa dicotomía; sesgo algorítmico; dogmatismo). Puntaje 16×1+5×3+4×5=51 reconciliado ✓.
**Lengua y Literatura**: 25/25 revisados; correctos (contexto salitrero/pulperías; comparación libertad vs control; intención explícita/implícita; rol del enunciador; adecuación género video corto). Conteos 8+4+9+4=25 ✓. Distribución de claves razonable.
**Ciencias p/la Ciudadanía**: 25/25 revisados; correctos (eficiencia energética; residuos peligrosos; corredor biológico; riego por goteo; retroceso glaciar evidencia; biodiversidad y velocidad del cambio; efecto invernadero antropogénico). Puntaje 11×1+7×2+7×3=46 reconciliado ✓. **Claves b×7/7 MC**.
**Ed. Ciudadana**: 25/25 revisados; contenido correcto salvo **2 hallazgos**: LGS-4M-EDC-001 (puntaje declarado 55 vs suma real 56) y LGS-4M-EDC-002 (clave V/F p.9 discutible sobre dignidad no debatible).
**Inglés**: 25/25 revisados; correctos (dystopia tema; entertaining/informative; reported speech "he had been"; must have walked; might have been asleep; lexico belonging; According to/Meanwhile/suggest; is supported; cierre tercer condicional). **Claves b×5/6**.

### 4.18 Lote — Exámenes integrados 1.º–4.º básico (Formas A y B, 8 archivos)

**1B Forma A**: 20/20 correctas (11 pelotas; pe-lo-ta; ser vivo; /m/; 12=7+5; tacto; Santiago; 5+3=8; pan; Pacífico; corcho; debajo de un auto; patrón círculo; hielo se derrite; mirar ambos lados; uva 7; el Sol; hospital; «luna»). Obs. menor LGS-1B-INT-001 (p.3 «dormir toda la noche» como primera actividad de la mañana). El texto «Pepa y el gato perdido» repite el caso de la leche al gato ya registrado en LGS-1B-PCD-001.
**1B Forma B**: 20/20 correctas (copihue; 16>12; casa; jueves; 10+6=16; ll→pollo; cordillera; vuelvo a las 6; 9−4=5; +2→8; mojar las manos; noche; levantar la mano; pictograma 6).
**2B Forma A**: 20/20 correctas (cielo diptongo; 83; sedentario; huevo→renacuajo→rana; 45+32=77; Puerto Montt; huemul; ruka mapuche; sumar 8; Argentina; agua toma forma; Rancagua; 4 lados/4 vértices; fiordo; evaporación→condensación→precipitación; mayúscula+punto; 4×3=12 goles; granizo; vías de evacuación). **Claves b×15/20** (LGS-GEN-KEY-002).
**2B Forma B**: 20/20 correctas (corazón bombea sangre; culturas se adaptan; «grande» grupo consonántico; 57<75; mestizo; corazón se fortalece; 96−42=54; Verdadero fiesta; inmigración alemana; azúcar se disuelve; 13<14; contenedor azul; centímetros; zona centro; 15−6=9; verano; «Las niño» concordancia; medios de comunicación).
**3B Forma A**: 20/20 correctas (628; copihue; ágora; Vallenar; Antonia cautelosa; 604−237=367; oxígeno; democracia ateniense; abejas V; 48÷8=6; vitaminas; hemisferios; anchovetas/sardinas; +10→354; eco; zona templada; invitar a abuelo; 1 kg>850 g; luna llena; CDN). Obs. LGS-3B-INT-001 (fecha 1989 de la firma chilena de la CDN).
**3B Forma B**: 20/20 correctas (ínsula→departamentos; 591>519; cactus norte/araucaria sur; cometa en espino V; 743→40; Juegos Olímpicos continuidad; Chillán; tomates figurado; 9×6=54; América-Pacífico; colación no saludable; subtítulo «especie en peligro»; 2.350÷5=470; párrafos; pirámide base cuadrada; rotación; derecho a la alimentación). Obs. LGS-3B-INT-002 (estímulos compartidos con Forma A).
**4B Forma A**: 20/20 correctas (6.813→unidad de mil; mayas/aztecas Zona A; piedras no vivas; buscar redes en la orilla; 347+486=833; clima tropical; oruga consumidor primario; metáfora «aguas son cristales»; 96÷8=12; cobre no renovable; tendón; subtítulo «¿Qué come?»; 2.000−1.640=360; atrapanieblas; jugo líquido; registro formal; vocabulario variado; 2 líneas de simetría; Congreso; manto). **Claves b×16/20** (LGS-GEN-KEY-002).
**4B Forma B**: 19/20 correctas + **P1 reconfirmado** en p.16: ecuación x+9=23 → x=14, el valor 14 está en la alternativa **b)**, pero la pauta indica «**c) 14**» — el estudiante que resuelva bien será marcado incorrecto si sigue la pauta. Resto de ítems correctos (ambiente campo Chillán; adaptación estructural; 124×6=744; mayas/incas común; personificación; columna vertebral; 9/24; corriente de Humboldt; implícita rol ecosistema; subducción; ×4 mesas/sillas; derechos del niño; damasco capas; tsunami; metro; veda sostenible).

### 4.19 Lote — Pruebas de unidad 1.º–6.º básico (76 archivos)

**1B (12 pruebas, ~85 ítems):** todas las claves verificadas — Números (8), Geometría (6), Medición (8), Patrones (6), Lenguaje U1/U2 (7 c/u), Ciencias Vida (8), Físicas (7), Tierra (7), Historia F.C./Geo/Hist (7 c/u). El ítem «¿Qué haces primero en la mañana?»→«Dormir toda la noche» de `historia-unidad-historia.md` p.1 es el mismo del examen integrado: **LGS-1B-INT-001 se propaga a la prueba de unidad y también al banco de la guía `01-basico/historia-geografia-y-cs-sociales.md` OA 2 p.1** (corregir las tres juntas). El cuento de la leche al gato también aparece aquí (LGS-1B-PCD-001).
**2B (12 pruebas, ~87 ítems):** todas correctas — incluye aritmética (34+52=86, 96−34=62, 40−15=25), patrones, geometría, hiato/diptongo, ciclo de la mariposa, emparejamientos de geografía e historia.
**3B (12 pruebas, ~95 ítems):** todas correctas — 347+265=612, 725−358=367, 9×6=54, 890×5=4.450, perímetros (18 cm, 7 m, 40 vs 36 cm), rotación/traslación, ágora/democracia, zonas climáticas, derechos del niño.
**4B (12 pruebas, ~85 ítems):** todas correctas — 428+357=785, 612−345=267, 91÷7=13, fracciones (1/8<1/4<1/2, 3/10+4/10=7/10, 9/10−4/10=5/10), área 21 cm²/40 m², simetrías, placas Nazca-Sudamericana, civilizaciones americanas.
**5B (14 pruebas, ~140 ítems):** todas correctas — 23×15=345, 156÷7=22r2, 46 bandejas, $3.550 vuelto, $263.400, 1/3+1/6=1/2, área triángulo 30 cm²/trapecio 55 cm², promedios, ecuaciones x=222/1.750/45, Inglés U1/U2 consistentes.
**6B (14 pruebas, ~150 ítems):** todas correctas — 3.420×12.500=$42.750.000, razón 15:10→3:2, 40%=2/5, 13/5=2 3/5, 12,846+0,097=12,943, ángulos opuestos por el vértice, área cubo 96 cm²/volumen 48 m³, ecuaciones 2x−7=15→11, x+3x=48.

### 4.20 Lote — Guías de estudio (autoevaluación incluida) 1.º–2.º básico (8 archivos)

| Guía | Resultado |
|---|---|
| `01-basico/matematica.md` | ✅ correcta |
| `01-basico/lenguaje-y-comunicacion.md` | ✅ correcta |
| `01-basico/ciencias-naturales.md` | ✅ correcta |
| `01-basico/historia-geografia-y-cs-sociales.md` | ✅ correcta; contiene en su banco el ítem ambiguo LGS-1B-INT-001 (ver §4.19 — corregir las 3 instancias juntas) |
| `02-basico/matematica.md` | ✅ correcta — aritmética íntegra verificada (34+52=86, 96−34=62, 40−15=25, 5×4=20, 4×5=20, 6×10=60, 12÷2=6), patrones, balanza 4+7=5+6, pictograma escala ×2 consistente, monedas $50×2=$100 |
| `02-basico/lenguaje-y-comunicacion.md` | ✅ correcta — «aire» diptongo, «leemos» hiato, «grande» grupo consonántico, güe/güi diéresis, cuento «Fiesta sorpresa de Emilia» (secuencia 2-1-4-3 ✓), carta de Rancagua, contenedor azul=papel |
| `02-basico/ciencias-naturales.md` | ✅ correcta — ciclo mariposa huevo→oruga→crisálida→mariposa, rana branquias→pulmones, huemul/picaflor de Arica/rana de Darwin zonas correctas, órganos-función, ciclo del agua, estaciones |
| `02-basico/historia-geografia-y-cs-sociales.md` | ✅ correcta — pueblos originarios (aymara altiplano, atacameños, diaguitas cerámica, mapuche ruka/mapudungun, canoeros, selk'nam, rapa nui), Perú norte/Bolivia noreste/Argentina este, inmigración alemana/palestina, CONAF, vías de evacuación |

**Sin hallazgos nuevos.** 8/8 guías verificadas ítem por ítem del banco de autoevaluación.

### 4.21 Lote — Guías de estudio 3.º–4.º básico (8 archivos)

| Guía | Resultado |
|---|---|
| `03-basico/matematica.md` | ✅ correcta — aritmética verificada (redondeo, estimación, tablas de multiplicar, división con resto, fracciones equivalentes, perímetros, ángulos) |
| `03-basico/lenguaje-y-comunicacion.md` | ✅ correcta — diptongo/hiato, personificación/metáfora/comparación consistentes, texto «El cóndor de Los Andes», fábula «La cigarra y la hormiga», biografía de Violeta Parra |
| `03-basico/ciencias-naturales.md` | ✅ correcta — plantas (partes, fotosíntesis, reproducción), reducir/reutilizar/reciclar, grupos de alimentos, sonido (vibración/pitch/volumen), Sistema Solar, rotación/traslación terrestre |
| `03-basico/historia-geografia-y-cs-sociales.md` | ✅ correcta — griegos y romanos (ágora, democracia ateniense, patricios/plebeyos), hemisferios/trópicos/continentes/océanos, derechos del niño. Nota: dice CDN «firmada en 1989… incluyendo Chile» — vinculada a LGS-3B-INT-001 (Chile ratificó en 1990) |
| `04-basico/matematica.md` | ✅ correcta — aritmética íntegra verificada (sumas con reserva, multiplicación 1.000×, división con cociente, fracciones de igual denominador, ecuaciones x±k=c, m↔cm, área 6×4=24/5×5=25, pictograma escala ×2 y gráfico ■=5: totales 85 y 20−10=10 correctos) |
| `04-basico/lenguaje-y-comunicacion.md` | ✅ correcta con 1 hallazgo — **LGS-4B-LEM-001 (P3)**: inconsistencia interna metáfora/comparación sobre el verso «sus laderas verdes parecen un poncho» (Ejemplo 2 = metáfora; autoevaluación = comparación, que es la clasificación correcta). Resto: explícita/implícita, ambiente, organizadores del texto, registro, punto aparte — todo correcto |
| `04-basico/ciencias-naturales.md` | ✅ correcta — ecosistemas (bióticos/abióticos), adaptaciones estructurales/conductuales, cadenas alimentarias (fitoplancton→anchoveta→pingüino→lobo marino), músculos/huesos/tendones/articulaciones, sistema nervioso, estados de la materia, capas de la Tierra (modelo damasco), subducción Nazca-Sudamericana |
| `04-basico/historia-geografia-y-cs-sociales.md` | ✅ correcta — mayas/aztecas/incas (mesoamericano vs andino, politeístas, monarquías, chinampas vs terrazas, Camino del Inca/Qhapaq Ñan en Chile), climas de América (tropical/mediterráneo/polar/desértico), ríos (Amazonas/Mississippi/Biobío), recursos renovables/no renovables (cobre, vedas), atrapanieblas/riego, autoridades (Presidente/ministros/senadores/diputados/alcaldes), derechos del niño |

**Un hallazgo nuevo:** LGS-4B-LEM-001. Guías 1B–4B completadas: **16/16**.

### 4.22 Lote — Guías de estudio 5.º básico (5 archivos)

| Guía | Resultado |
|---|---|
| `05-basico/matematica.md` | ✅ correcta — aritmética íntegra verificada (descomposición 4.582.170, aproximaciones 39.000/130.000, 34×26=884, 23×15=345, 47×36=1.692, 62×19≈1.200, 156÷7=22r2, 275÷6→46 bandejas, 190÷8=23r6, 438÷5=87r3, 3×4.500→6.500 vuelto, 5×1.290→3.550, 18×8.500+12×9.200=263.400, 3.250×7.500=24.375.000, 52.000−10.000÷3.500=12 semanas, fracciones 1/3+1/6=1/2, 3/4−1/2=1/4, decimales 0,8>0,75 y 3,099<3,1, áreas (8×5)/2=20, 12×6=72, (14+8)×5/2=55, promedios 45/5=9 y 60−37=23, secuencia 2+14×3=44, ecuación x=350−128=222, unidades mm/cm/m, gráficos de línea 1,5 kg) |
| `05-basico/lenguaje-y-comunicacion.md` | ✅ correcta — metáfora/comparación/personificación manejadas con precisión (contrasta con el hallazgo 4B-LEM-001: aquí «el cielo es un manto» se clasifica correctamente como metáfora y la guía misma explica la diferencia), rima asonante/consonante, emisor/propósito/destinatario, conflicto narrativo, artículo informativo con fuentes |
| `05-basico/ingles.md` | ✅ correcta — reading (explicit info, propósito, cognados), reacción y comparación (like/prefer/different from), writing (shopping list, postales, rimas). **Confirmación cruzada:** la guía usa el diálogo «— I'm sorry, I broke your pencil. — That's OK, don't worry» **bien armado**, lo que reconfirma que LGS-5B-ING-001 es un error del examen, no del material fuente |
| `05-basico/ciencias-naturales.md` | ✅ correcta — niveles de organización célula→tejido→órgano→sistema, nutrientes, tabaco (respiratorio vs circulatorio), microorganismos benéficos/dañinos, conductores/aisladores, agua dulce ~3% vs salada ~97%, ciclo del agua, impacto humano en reservas hídricas |
| `05-basico/historia-geografia-y-cs-sociales.md` | ✅ correcta — conquista de América y Chile (Almagro 1535-37, Valdivia 1540, Santiago 1541, Michimalonco, Lautaro, Curalaba 1598), impactos en Europa/América, Colonia (metrópoli, Virreinato del Perú, Capitanía General, sincretismo), Guerra de Arauco/parlamentos (Quillín 1641)/encomienda/vida fronteriza Biobío, 5 zonas naturales, recursos renovables/no renovables (cobre, hierro, forestales, marítimos), derechos humanos universales y deberes |

**Sin hallazgos nuevos.** Guías acumuladas verificadas: **21/21** (1B–5B completos).

### 4.23 Lote — Guías de estudio 6.º básico (5 archivos)

| Guía | Resultado |
|---|---|
| `06-basico/matematica.md` | ✅ correcta — aritmética íntegra verificada (48.500.000/2.350.000=20 cuadras sobran 1.500.000, 3×12.480+8.750=46.190−39.200=6.990, 3.420×12.500=42.750.000, 156.000/12=13.000, 45×185.000−350.000=7.975.000, 1.240×6.500+890×3.200=10.908.000, razones 15:10→3:2, 3:7→9:21, 5:3→15:9, 3:1→9:3, porcentajes 25%=1/4, 20% de 150=30, 10% de 480→144, 25% de 12.000=3.000, 45% de 200=90, 65/100, mixtos 11/4=2 3/4, 3 2/5=17/5, 22/6=3 2/3, 17/5=3 2/5, 1 3/4=7/4, 8/6=1 1/3, sumas 2 1/4+1 1/2=3 3/4, 3 1/3+2 1/6=5 1/2, 8/3−1/6=2 1/2, decimales 5,240−1,875=3,365, 4,500−2,375=2,125, 12,846+0,097=12,943, 2 3/4−1 1/2=1 1/4, 15,500−8,750=6,750, ecuaciones x+18=45→27, 4x=52→13, 3x+5=26→7, x+34=90→56, x+3x=48→12, 2x−7=15→11, x−8.500=17.300→25.800, ángulos 40/62/96/148, áreas cubo 6×25=150, 24+16+12=52, 6×16=96, 6×2.500=15.000, 4+6+3=13, 80+48+30=158, volúmenes 4³=64, 5×3×2=30, 20×6=120, 3³=27, 10×4×2=80, 7×5×4=140, 10³=1.000 mm³, 8×4×1,5=48, probabilidad 300/6=50, 2×2×2=8, 6×6=36, 7:3, gráficos 0,4×150=60, 25%×40=10, 45%−30% de 60=9, 25% de 320=80). **Reconfirma LGS-6B-MAT-001** (P3 ya registrado): autoevaluación OA 2 p.4, 24.600÷12=2.050 cajas ÷3 distribuidores = 683 con resto 1 caja sin repartir — la retroalimentación dice "≈683" sin explicar el sobrante |
| `06-basico/lenguaje-y-comunicacion.md` | ✅ correcta — causa-consecuencia y motivaciones (textos Humberstone/minga de Chiloé), **hipérbole correctamente distinguida de comparación** ("mis ojos pesan más que una montaña" = hipérbole; contraste con hallazgo de examen LGS-6B-LEM-001, que queda confinado al examen), aliteración/onomatopeya, comparación de dos fuentes (atrapanieblas Texto A/B, 310−90=220), emisor/propósito/destinatario (ciclovía Ñuñoa), referentes claros, artículo informativo con síntesis (pudú 35-45 cm — dato verídico) |
| `06-basico/ingles.md` | ✅ correcta — can/can't, direcciones (in front of/next to/between), presente vs pasado (went/visited), horas (o'clock), expresiones (have lunch, catch a cold, What's the matter), I think/because, presente continuo (is/are+-ing), plurales irregulares (children, sheep, geese), posesivo 's, preguntas who/how many/can/where |
| `06-basico/ciencias-naturales.md` | ✅ correcta — fotosíntesis (agua+CO₂+luz→azúcar+O₂; Ingenhousz, Priestley, Calvin correctamente atribuidos), cadenas/redes tróficas (productor→consumidor 1°/2°/3°→descomponedores), pubertad (cambios biológicos/conductuales, menarquia), higiene/actividad física, energía (tipos, origen solar directo/indirecto), recursos renovables/no renovables y potencial chileno (Atacama), cambios de estado (fusión/evaporación/ebullición/condensación/solidificación/sublimación a nivel particulado), capas de la Tierra (atmósfera/litósfera/hidrósfera), erosión (agua, viento, actividad humana; río Loa) |
| `06-basico/historia-geografia-y-cs-sociales.md` | ✅ correcta — todas las fechas verificadas: independencia americana (malestar criollo, Ilustración, EE.UU. 1776, cautiverio Fernando VII 1808), proceso chileno (cabildo 18-sep-1810, Rancagua 1814, Chacabuco 1817, Declaración 12-feb-1818, Maipú 5-abr-1818, Patria Vieja/Reconquista/Patria Nueva 1810-14/14-17/17-23), Constitución 1833, leyes laicas (Matrimonio Civil 1884), Fuerte Bulnes 1843, ocupación Araucanía ~1860-1880, Guerra del Pacífico 1879-1883 (Tarapacá/Antofagasta), Rapa Nui 1888, voto femenino municipal 1935/presidencial 1949, golpe 11-sep-1973, plebiscito 1988, retorno 1990, DUDH 1948 art. 26, regiones y 8 ambientes naturales, división de poderes, derechos/deberes |

**Sin hallazgos nuevos.** Guías acumuladas verificadas: **26/26** (1B–6B completos).

### 4.24 Lote — Guía Matemática 7.º básico (hallazgo nuevo)

`07-basico/matematica.md` (778 líneas): verificada íntegramente — números enteros (−8+5=−3, 6−(−2)=8, −12+20=8, 4−9=−5, −4+11=7, −32.000+50.000=18.000, −300−150=−450, 1.200−(−85)=1.285), fracciones (2/3×3/5=2/5, 4/5÷2/3=6/5, 1/2×2/7=1/7, 3/4÷1/2=1 1/2, 3/4×5=15/4, 5/6÷1/12=10), decimales (3,5×0,25=0,875, 12,6÷4=3,15, 4,2×0,5=2,1, 9,6÷0,4=24, 980,5×32,4=31.768,2, 8,4÷0,15=56), porcentajes (IVA 19%: 59.500 y 380.800, descuentos 28.000 y 27.000, 8%→540.000, 60.000+15%−15%=58.650≠60.000), álgebra (3x+5, 3n+1, 4n+1, 3x−4=26→10, 2x+6=40→17, 500+300x→6 h, 2x+1=45→22 y 23), proporciones (3.000×5=15.000, 4×12=8×6, 980×n, 5×8=40÷10=4, 320÷4×7=560), círculo (P=3,14×10=31,4, A=3,14×36=113,04, 3,14×400=1.256, r=7, P=25,12, 56,52, A=314, 3,14×12.756≈40.053,84, 706,5, área se cuadruplica al duplicar radio: 50,24 vs 200,96, 2πr≈6,28r), cuadrantes y traslaciones ((−4,3)=CII, (−5,−2)=CIII, (3,−5), (−4,1), 4 cuadrantes, (8,−5)), probabilidades (1/6≈16,7%, 27/50=54%, 3/10=30%, 1/8, 9/60=15%, 5/20=25%, 32/40=80%, 3:20=15%, 3/6=1/2, 112/200=56%, 24/80=3/10).

**Un hallazgo nuevo:** LGS-7B-MAT-001 (P2) — OA 16, Ejemplo 1 (líneas ~600-607): la tabla de frecuencias **no coincide con los datos listados**. Los 20 datos son `0,1,1,2,1,0,3,1,2,1,0,2,1,1,3,0,2,1,1,2`, que contienen **nueve "1" y dos "3"** (frecuencias reales: 4, 9, 5, 2 → 20%, 45%, 25%, 10%), pero la tabla declara ocho "1" y tres "3" (4, 8, 5, 3 → 20%, 40%, 25%, 15%). El estudiante que cuente los datos encontrará un resultado distinto al del ejemplo resuelto. Corrección sugerida: ajustar la tabla a 4/9/5/2 o corregir un dato de la lista. (Nótese que la Pregunta 4 del mismo OA —dado lanzado 15 veces— sí reconcilia exactamente: 2,2,5,2,2,2=15.)

Guías acumuladas: **27/27** verificadas; **2 hallazgos de contenido** acumulados en guías (LGS-4B-LEM-001, LGS-7B-MAT-001), además del ya conocido LGS-6B-MAT-001.

### 4.25 Lote — Guías de estudio 7.º básico (4 archivos restantes — curso completo)

| Guía | Líneas | Resultado |
|---|---|---|
| Lengua y Literatura | 579 | ✅ Correcta (conflicto, narrador vs. personajes, flashback/analepsis, Matanza Escuela Santa María 1907, hecho/opinión, prejuicio de género, participio "resuelto", concordancia) |
| Inglés | 620 | ⚠️ **LGS-7B-ING-001 (P3)**: texto de práctica afirma «The Amazon rainforest produces about 20% of the world's oxygen» — cifra popular pero científicamente imprecisa (contribución neta del Amazonas al O₂ global ≈ 0; cifra bruta real ~6-9%). Gramática toda correcta (past continuous, must/mustn't, prefijo un-, sufijos -ing/-ly, too...to, there is/are + much/many, causales con if) |
| Ciencias Naturales | 948 | ✅ Correcta (ovulación ~día 14, fecundación en trompas de Falopio, procariota/eucariota, virus requiere huésped, roce estático/cinético, subducción Nazca-Sudamericana, leyes de Boyle/Charles/Gay-Lussac bien enunciadas y cálculo 2 atm × 4 L ÷ 2 L = 4 atm correcto) |
| Historia | 1.833 | ✅ Correcta en su totalidad (Revolución neolítica, rasgos de las primeras civilizaciones, ciudadanía ateniense restringida, romanización, caída de Roma 476 d.C., síntesis grecorromana-judeocristiana-germana, transformaciones desde s. XII, chinampas/milpa, palabras de origen árabe: almohada/aceite/azúcar/alcalde, tolerancia religiosa romana e incaica) |

**Curso 7.º básico cerrado: 5/5 guías auditadas** (Matemática ya constaba en §4.24). Hallazgos del curso: LGS-7B-MAT-001 (P2), LGS-7B-ING-001 (P3).

Guías acumuladas: **32/32** verificadas; 4 hallazgos de contenido acumulados (LGS-4B-LEM-001, LGS-7B-MAT-001, LGS-7B-ING-001, LGS-6B-MAT-001).

### 4.26 Lote — Guías de estudio 8.º básico (5 archivos — curso completo)

| Guía | Líneas | Resultado |
|---|---|---|
| Matemática | 849 | ✅ Correcta, aritmética íntegra verificada (enteros y signos, racionales, potencias, raíces, ecuaciones 1er grado, función afín, Pitágoras, transformaciones isométricas, cuartiles/percentiles) |
| Lengua y Literatura | 589 | ⚠️ **LGS-8B-LEM-001 (P3)**: texto de práctica «La noche del río» ambienta el terremoto de Valdivia «la madrugada del 22 de mayo de 1960», pero el evento real ocurrió ~15:11 de la tarde; la propia guía lo presenta como «hecho histórico real». Resto correcto (narrador/protagonista, figuras literarias, contexto de la obra, argumentación, corrección de estilo) |
| Inglés | 687 | ✅ Correcta (going to vs will con evidencia, prefer + to, comparativo/superlativo, sufijos -er/-ion, «creater» correctamente marcado como no-palabra, nacionalidades, preposiciones on/in/at, get off/arrive at, frecuencia y conectores de secuencia) |
| Ciencias Naturales | 1.152 | ✅ Correcta (estructura celular, ósmosis/xilema/estomas, sistemas del cuerpo y nefrón, Ley de Ohm V=I×R → 200 V y P=V×I → 5 A, calor vs temperatura, conducción/convección/radiación, K=°C+273 y °F=°C×1,8+32 → 68°F y 310 K/98,6°F, modelos Dalton-Thomson-Rutherford-Bohr, tabla periódica grupos/periodos, enlaces iónico/covalente polar y apolar, 220 V red domiciliaria chilena) |
| Historia | 1.805 | ⚠️ **LGS-8B-HIS-001 (P3)**: errata «cantidad de population» en vez de «población» en autoevaluación OA 4 p.1. Contenido histórico correcto (Lutero 1517, Concilio de Trento 1545-63, proceso de Galileo 1633, Gutenberg ~1450, debate de Valladolid 1550-51, Parlamento de Quilín 1641, crisis monárquica 1808, Junta 1810 → Reconquista 1814-17 → Chacabuco 1817 → Independencia 12-02-1818, Declaración 1789, DUDH 1948, IDH y desarrollo sustentable) |

**Curso 8.º básico cerrado: 5/5 guías auditadas.** Hallazgos del curso: LGS-8B-LEM-001 (P3), LGS-8B-HIS-001 (P3) — ambos menores.

Guías acumuladas: **37/37** verificadas; 6 hallazgos de contenido acumulados (LGS-4B-LEM-001, LGS-6B-MAT-001, LGS-7B-MAT-001, LGS-7B-ING-001, LGS-8B-LEM-001, LGS-8B-HIS-001).

### 4.27 Lote — Guías de estudio 1.º medio (5 archivos — curso completo)

| Guía | Líneas | Resultado |
|---|---|---|
| Matemática | 670 | ✅ Correcta íntegramente (conjuntos, valor absoluto, potencias/notación científica, raíces, logaritmos, funciones afín/cuadrática, sistemas de ecuaciones, semejanza, probabilidades) |
| Lengua y Literatura | 604 | ⚠️ **LGS-1M-LEN-001 (P3)**: errata «—**information** implícita—» en OA 3 Ej.1 (debe ser «información»). Contenido correcto (géneros narrativo/dramático/lírico, Caleuche chilota, Kai Kai y Trentren mapuches, *Sub terra* de Blest Gana 1904, contexto de producción, información explícita/implícita, oratoria y argumentación) |
| Inglés | 740 | ✅ Gramática correcta (will/going to, present perfect, first/second conditional, reported speech, passive voice, modal verbs). Reaparece el mito del Amazonas (banco OA 9 p.3) → **LGS-7B-ING-001 ampliado a transversal (7B + 1M)** |
| Ciencias Naturales | 1.555 | ⚠️ 2 hallazgos P3: **LGS-1M-CNT-010** (errata «tres **dimensions**» en retro OA 8 p.5 — mismo patrón que «population» e «information») y **LGS-1M-CNT-011** (banco OA 11 p.7: analogía Doppler dice «rojo» al acercarse; debe ser azul — el propio Ejemplo 3 lo explica bien). Resto correcto y riguroso: evolución/selección natural/especiación, ecología poblacional, bioacumulación vs biomagnificación correctamente distinguidas (a diferencia del examen LGS-1M-CNT-009), ciclos biogeoquímicos, eficiencia trófica 10%, sonido (eco 340 m, Doppler), luz (refracción, reflexión total interna, corrimiento al rojo), Tierra-Luna-Sol (fases, eclipses, estaciones ~23,5°), astronomía en Chile, reacciones químicas, estequiometría (N₂+3H₂→2NH₃; fotosíntesis 6CO₂+6H₂O→C₆H₁₂O₆+6O₂) |
| Historia | 2.034 | ✅ Correcta en fechas y contenido (ensayos constitucionales, pipiolos/pelucones, Lircay 1830, Constitución 1833 y ciudadanía restringida, ciclos trigo/plata/salitre, inquilinaje, unificaciones Italia 1861-70 y Alemania 1871, Grecia y Bélgica 1830, Gran Colombia disuelta 1830, PGM 1914-18 con imperialismo/armamentismo/alianzas y detonante Sarajevo 1914, Revolución rusa 1917, Temuco 1881, Guerra del Pacífico 1879-83 y pérdida del litoral boliviano, cuestión social, Santa María de Iquique 1907, Gay y Domeyko, U. de Chile 1842, Isla de Pascua anexada 1888, Kawéskar/Yagán austral, mercado/monopolio/colusión/inflación/deflación/aranceles, respuestas políticas a la cuestión social, desarrollo sostenible) |

**Curso 1.º medio cerrado: 5/5 guías auditadas.** Hallazgos del curso: LGS-1M-LEN-001, LGS-1M-CNT-010, LGS-1M-CNT-011 (todos P3, menores) + ampliación de LGS-7B-ING-001 a transversal.

Guías acumuladas: **42** verificadas; 9 hallazgos de contenido acumulados (los 6 anteriores + LGS-1M-LEN-001, LGS-1M-CNT-010, LGS-1M-CNT-011). **Patrón sistémico detectado:** erratas con palabras en inglés dentro del texto en español ya van en 4 cursos distintos (8B «population», 1M «information», 1M «dimensions», más LGS-2M-LEN-002) — sugiere correr una búsqueda global de anglicismos antes del cierre. **Ejecutada:** la búsqueda global sobre todo `contenido/` arrojó exactamente esas 4 instancias; no hay más anglicismos pendientes de registro.

### 4.28 Lote — Guías de estudio 2.º medio (5 archivos — curso completo)

| Guía | Líneas | Resultado |
|---|---|---|
| Matemática | 620 | ✅ Correcta íntegramente |
| Lengua y Literatura | 617 | ✅ Correcta (verificado que «ya no hay vuelta atrás» está bien redactado aquí — reconfirma que la corrupción «welcome» de LGS-2M-LEN-002 es exclusiva del examen Forma B p.17) |
| Inglés | 765 | ⚠️ **LGS-2M-ING-001 (P3)**: Ej.3 del OA 13 usa «unless» con lógica invertida («she has achieved real change unless the government ignores her proposals»). Resto de gramática correcto |
| Ciencias Naturales | 1.399 | ⚠️ **LGS-2M-CNT-022 (P3, trivial)**: falta espacio en «resultante):la suma». Contenido correcto y riguroso: reproducción y desarrollo, mitosis/meiosis/trisomía 21, biotecnología/transgénicos/ética, cinemática MRU-MRUA (90÷1,5=60 km/h; 20÷5=4 m/s²; adición Galileo 105 km/h; relativa 20 km/h × 2 h = 40 km), leyes de Newton (F=ma → 20×0,5=10 N; 15−5=10 N, 10÷5=2 m/s²), modelos del Universo y Big Bang 13.800 Ma, soluciones (%m/m: 20/200=10%; 15/300=5%), hidrocarburos y carbono tetraédrico |
| Historia, Geografía y Cs. Sociales | 2.310 | ✅ Correcta en fechas y contenido (Gran Depresión 1929 y salitre, totalitarismos, New Deal, ONU 1945, DUDH 1948, voto femenino municipal 1934 y presidencial 1949, Muro de Berlín 1961/1989, crisis misiles 1962, Sputnik 1957, Luna 1969, Cuba 1959, golpes Brasil 1964/Chile y Uruguay 1973/Argentina 1976/Stroessner 1954, Perestroika-Glasnost, disolución URSS 1991, golpe 11-09-1973, DINA 1974-77→CNI, Comité Pro Paz 1973-75→Vicaría 1976, Plan Laboral años 80, crisis 1982, protestas 1983, Acuerdo Nacional 1985, plebiscito 1988 No ~56% («más del 54%»), elecciones 1989, Aylwin 1990, Rettig 1991, Pinochet Cmdte. en Jefe hasta 1998, boinazo 1993, INDH, Ley Zamudio 20.609 de 2012, poblaciones callampas y segregación urbana) |

**Curso 2.º medio cerrado: 5/5 guías auditadas.** Hallazgos del curso: LGS-2M-ING-001 (P3), LGS-2M-CNT-022 (P3, trivial) — ambos menores.

Guías acumuladas: **47** verificadas; 11 hallazgos de contenido acumulados (los 9 anteriores + LGS-2M-ING-001 + LGS-2M-CNT-022).

### 4.29 Lote — Guías de estudio 3.º medio (6 archivos — curso completo)

| Guía | Líneas | Resultado |
|---|---|---|
| Matemática | 528 | ✅ Correcta íntegramente (función cuadrática y vértice, exponencial/logarítmica, interés compuesto 1,04⁵ y (0,88)⁴ verificados, vida media, probabilidad condicional, geometría de cuerpos) |
| Lengua y Literatura | 558 | ✅ Correcta (vanguardismos, realismo mágico, *Cien años de soledad* 1967, argumentación y ensayo, análisis de discurso) |
| Inglés | 735 | ⚠️ **LGS-3M-ING-001 (P3)**: retroalimentación p.14 dice «"común practice"» por «common practice». Gramática correcta en todo lo demás (third conditional, wish/if only, passive reporting, phrasal verbs) |
| Filosofía | 1.157 | ✅ Correcta (asombro/doxa, ontología: idealismo/materialismo/dualismo, epistemología: dogmatismo/escepticismo/criticismo, lógica: deducción/inducción, verdad vs validez, falacias ad hominem/autoridad/falsa dicotomía/pendiente resbaladiza, mayéutica/experimento mental/fenomenología/axiomática — ejemplos lógicos todos válidos, incl. cisnes negros y ballena como afirmación del consecuente) |
| Ciencias para la Ciudadanía | 1.096 | ✅ Correcta y rigurosa (factores biológicos/ambientales/sociales, corto vs largo plazo, transgénicos con postura científica correcta del consenso, vías de transmisión influenza/VIH/hepatitis B/hantavirus colilargo, PNI, OPS-2016 sarampión, cloro+amoníaco→cloraminas, bicarbonato+vinagre correctamente identificado como inofensivo, paracetamol hepatotoxicidad, riesgo/prevención/mitigación/adaptación, NCh433, incendios 2017, Valdivia 1960 M9,5 / Maule 2010 M8,8 / Iquique 2014 M8,2, Ley 20.606 etiquetado, Ley 19.925 alcohol, Ley 21.364 SENAPRED) |
| Educación Ciudadana | 1.620 | ✅ Correcta (fundamentos vs atributos de la democracia con criterio de Dahl, Fiscalía/Defensoría Penal/CAJ correctamente distinguidas, funciones económicas del Estado, probidad/Contraloría, 5 principios DD.HH. con DUDH 1948, republicanismo/liberalismo/comunitarismo, escalas territoriales con Gobernador electo vs Delegado designado, plan regulador, justicia ambiental/zonas de sacrificio — cobertura exacta de los 6 OA declarados) |

**Curso 3.º medio cerrado: 6/6 guías auditadas.** Único hallazgo: LGS-3M-ING-001 (P3).

Guías acumuladas: **53** verificadas; 12 hallazgos de contenido acumulados (los 11 anteriores + LGS-3M-ING-001).

### 4.30 Lote — Guías de estudio 4.º medio (6 archivos — curso completo)

| Guía | Líneas | Resultado |
|---|---|---|
| Matemática | 522 | ✅ Correcta íntegramente. Recálculo completo: interés simple 500.000×1,18=590.000 y compuesto (1,06)³≈595.508; TEA (1,02)¹²−1≈26,82% y (1,03)⁴−1≈12,55%; UF 15×38.500=577.500; potencia inversa 800/d², ley del inverso del cuadrado; modelos periódicos T=2π/B (12 h mareas, h=15 temperatura máxima); binomial C(5,4)×0,8⁴×0,2=40,96% y 6×0,09×0,49≈26,46%; normal regla 68-95-99,7; complemento 1−(0,9)³=27,1% |
| Lengua y Literatura | 368 | ✅ Correcta (3 OA: interpretación comparada con textos originales sobre exilio 1975 vs migración actual, evaluación crítica de columna de opinión sobre royalty minero con distinción intención explícita/implícita y veracidad vs retórica, producción de textos con adecuación género/audiencia) |
| Inglés | 765 | ✅ Gramática correcta íntegramente (propósito/audiencia/contexto, skim vs scan, reported speech con cambios de tiempo correctos, must/might/can't have + participio, síntesis de dos fuentes, léxico apropiado para identidad cultural) |
| Filosofía | 1.254 | ✅ Correcta (alcances y límites del filosofar; ética vs moral; utilitarismo vs deontología kantiana con imperativo categórico y «fin en sí misma» correctamente explicados; justicia según mérito/necesidad/igualdad; libertad negativa/positiva; igualdad formal/sustantiva; evaluación de argumentos: tesis/contraargumento/supuestos, referentes teóricos/empíricos/sentido común, falacias ad hominem/autoridad/falsa dicotomía/pendiente resbaladiza/generalización apresurada, argumento sólido; ontología-epistemología-ética aplicadas a IA, deepfakes, big data, trabajo remoto, arte generativo) |
| Ciencias para la Ciudadanía | 739 | ✅ Correcta y rigurosa (5 criterios de proyectos sostenibles, jerarquía 3R, «greenwashing», riego por goteo vs inundación; CO₂ ~280→420+ ppm, núcleos de hielo, acidificación oceánica y carbonato de calcio, blanqueamiento de corales por zooxantelas correcto, mitigación vs adaptación bien distinguidas, justicia climática, megasequía, hidroeléctrica con efectos secundarios, validación de modelos/IPCC) |
| Educación Ciudadana | 731 | ✅ Correcta (2 OA: libertad-igualdad-solidaridad ante desafíos democráticos con libertad negativa/positiva e igualdad de trato/oportunidades; medios y TIC: cámaras de eco, desinformación, concentración de medios, microsegmentación, Ley de Protección de la Vida Privada, alfabetización mediática). Nota: la guía declara transparentemente que el extracto oficial del primer OA aparece cortado en la fuente y su número no consta — buena práctica documental |

**Curso 4.º medio cerrado: 6/6 guías auditadas. Cero hallazgos nuevos.**

Guías acumuladas: **59** verificadas; 12 hallazgos de contenido acumulados (sin cambios respecto del lote anterior).

**PASADA DE GUÍAS DE ESTUDIO COMPLETADA: 59/59 archivos de `contenido/` revisados íntegramente.** Hallazgos de guías: 12 (1 P2: LGS-7B-MAT-001; 11 P3). Patrones sistémicos cerrados: anglicismos/hispanismos (5 instancias, incl. «común practice» de 3M) y reutilización del mito del Amazonas (7B+1M).

### 4.3 Observación transversal — formato de puntajes en exámenes (LGS-GEN-FMT-001)

Al comparar `06-basico/examenes/`: `historia-…-forma-b.md` incluye columna **Puntaje**, total declarado y escala de conversión a nota; `matematica-…-forma-b.md` e `ingles-…-forma-b.md` **no** declaran puntaje por ítem ni total. Si la app calcula nota por puntaje, la asignatura sin puntajes no tiene criterio de ponderación documentado. **Severidad P3** (consistencia/operabilidad), no bloquea corrección manual. Recomendación: definir un estándar único de pauta (puntaje por ítem, total, escala) y aplicarlo a los 46 archivos `*-forma-b.md` + `examen-integrado-forma-*.md`.

---

## 5. Cola de trabajo priorizada (continuación)

1. **P1 abiertos (3):** preparar propuesta de corrección para LGS-4B-EVAL-001, LGS-5B-EVAL-001 y LGS-2M-MAT-014; no aplicar hasta autorización. Ampliar el validador CI para detectar contradicción alternativa↔pauta (caso 2M-MAT-014) y desbalance de claves (caso 6B-MAT-003).
2. ~~**Recálculo de exámenes restantes (Régimen B/C)**~~ — ✅ **CERRADO**: los 32 archivos de examen por asignatura recalculados ítem por ítem (5B–4M, ambas formas donde aplica).
3. ~~**Exámenes integrados 1B–4B**~~ — ✅ **CERRADO**: 8/8 archivos auditados ítem por ítem.
4. ~~**Guías y pruebas de unidad**~~ — ✅ **CERRADO**: 156/156 pruebas de unidad y **59/59 guías de estudio** revisadas íntegramente, curso por curso y asignatura por asignatura (§4.20–4.30). Bancos de autoevaluación revisados como parte de cada guía (son secciones del mismo archivo, no archivos separados).
5. **Trazabilidad curricular (pendiente):** para cada OA citado en pautas, verificar número y texto contra `Temarios/analisis/` y la fuente oficial (Decretos 439/2012, 614/2013, 193/2019). Pendiente también: inconsistencia de decreto citado en guías 1M/2M (614/2013 vs 439/2012 según CLAUDE.md para esos niveles — verificar en la fuente).
6. **QA técnica (pendiente):** importación, render de estímulos (crítico para ítems que dependen de imagen, p. ej. LGS-1B-MAT-001) y persistencia de puntajes. CI fallido sin investigar (runs 39710761424, 39710756829).

**Criterio de cierre recordatorio:** no declarar cobertura por archivos leídos ni por CI verde; cada fila del inventario requiere estado + evidencia, y los P0/P1 deben estar resueltos o con decisión explícita de bloqueo.
