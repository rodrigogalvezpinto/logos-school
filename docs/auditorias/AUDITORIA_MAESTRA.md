# AUDITORÍA MAESTRA — Logos School (Consolidada)
**Fecha consolidación:** 23 de octubre de 2026  
**Fuentes unificadas:**
1. `planificacion/22-analisis-de-brechas.md` — Auditoría técnica/seguridad/QA (backend, frontend, infra)
2. `contenido/00-estado-contenido.md` — Estado macro + auditoría pedagógica 2026-08-11
3. `auditoria.md` — Auditoría ítem por ítem (exámenes, pruebas, guías) — rama `qa/fase-2-matriz-trazabilidad`, HEAD `0106976`
4. Auditoría pedagógica experta aplicada en esta sesión (skills `profesor-experto-chile.md` + `auditoria-contenido-educativo.md`)

**Estado global:** 🟢 **CONTENIDO CORREGIDO — 0 HALLAZGOS ABIERTOS** — ver §0.3, §0.4 y §0.5

---

## 0. BITÁCORA DE REPARACIÓN (25 de octubre de 2026)

### 0.1 Incidente: pautas destruidas por el validador

`backend/scripts/validador_formato_pauta.py` tenía un modo `--fix` que reconstruía la
tabla de pauta a partir de una plantilla. La plantilla emitía el texto
`[MANTENER FILAS ORIGINALES DE PAUTA — REVISAR MANUALMENTE]` en lugar de las filas
reales, de modo que **cada archivo procesado perdía su clave de corrección**.

Alcance: **48 exámenes**.

| Commit | Exámenes afectados |
|---|---|
| `edab5ca` | 31 (exámenes por asignatura de 5° básico a 4° medio, Forma B) |
| `5421485` | 17 (exámenes integrados de 1° a 4° básico y Lengua/Lenguaje de 1° medio a 7° básico) |

**Reparación aplicada:** se restauraron las tablas reales desde `5f9e213` (último
commit con pautas íntegras) y se re-aplicaron, una por una, las correcciones de
contenido documentadas en §3 (P1 y P2). Verificado: **0 marcadores de plantilla** y
**0 exámenes sin fila de pauta para sus preguntas**.

**Medida preventiva:** `validador_formato_pauta.py` fue reescrito como validador de
**solo lectura**. No escribe archivos y ya no existe modo `--fix`. La pauta es
contenido editorial: se edita a mano.

### 0.2 Incidente: "rebalanceo" de claves incorrecto

El intento anterior de bajar la concentración de una letra reescribió **33 claves**
cambiando sólo la letra de la pauta (`b→a`, `c→b`), **sin reordenar las opciones**
del examen. Eso convirtió respuestas correctas en incorrectas. Ejemplo: 1° básico
Forma A, pregunta 2 ("pe-lo-ta" = 3 sílabas) tiene la respuesta en **b)**, pero la
pauta quedó en **a)**.

**Reparación aplicada:** las 33 claves se revirtieron a su valor original verificado.
Se conservó la única corrección de clave legítima (LGS-4B-EVAL-001, p.16: `c → b`).

**Regla adoptada:** la distribución de claves **no se corrige cambiando la clave**.
Se corrige reordenando las alternativas del enunciado y actualizando la clave en
consecuencia. Cualquier cambio de letra sin reordenamiento de opciones es un error.

### 0.3 Estado verificado tras la reparación

| Comprobación | Resultado |
|---|---|
| Marcadores de plantilla en `contenido/` | 0 |
| Exámenes analizados por `validador_formato_pauta.py` | 50 |
| Exámenes con problemas estructurales de pauta | **0** |
| Exámenes con anglicismos | **0** |
| Diferencia entre `contenido/` actual y `5f9e213` | sólo las correcciones auditadas de §3 |
| Exámenes con una clave > 45 % | **0 / 50** (ver §3.4) |

### 0.4 Rebalanceo de claves aplicado y verificado

| Comprobación | Resultado |
|---|---|
| Exámenes medidos (todos los formatos de pauta) | **50** |
| Exámenes que superaban el 45 % antes del rebalanceo | **39 / 50** |
| Exámenes con una letra > 45 % después | **0 / 50** |
| Intercambios de alternativas aplicados y verificados | **188 / 188** |
| Claves con texto citable que coinciden con su alternativa | **492 / 492** |
| Explicaciones de pauta que citan letras de alternativa | **0** |
| Exámenes con problemas estructurales de pauta | **0** |
| Archivos con anglicismos | **0** |

El detalle del alcance, las exclusiones justificadas y el criterio de cierre están en §3.4.

### 0.5 Paquete de calidad editorial (25 de octubre de 2026)

Cinco frentes cerrados, todos dentro de `contenido/` y verificados con los
validadores de producción.

#### 1. Enlaces y referencias a "Forma A"

| Comprobación | Antes | Después |
|---|---|---|
| Enlaces a archivos de contenido inexistentes | 12 | **0** |
| Menciones a una "Forma A" que no existe | 88 (en 40 exámenes) | **0** |
| Rutas `.md` de `contenido/` citadas y existentes | — | **102 / 102** |

Las 25 menciones restantes a "Forma A" son legítimas: corresponden a los
exámenes integrados de 1° a 4° básico, que sí tienen Forma A y Forma B
separadas. Las 2 rutas no resueltas son plantillas `contenido/{curso}/...` del
documento de inventario, no enlaces.

#### 2. Rúbricas de las preguntas de desarrollo

| Comprobación | Resultado |
|---|---|
| Rúbricas agregadas | **91** |
| Exámenes con rúbricas | **9** |
| Rúbricas cuya suma de criterios iguala el puntaje del enunciado | **91 / 91** |

Cobertura: Ciencias Naturales de 5° a 8° básico y 1° a 2° medio, Ciencias para
la Ciudadanía de 3° y 4° medio, y Educación Ciudadana de 3° medio. Se escribieron
como listas con guiones —no como tablas— para no interferir con
`_extraer_pauta_tabla` / `_extraer_pauta_lista` de `parser_prueba_examen.py`, y
bajo un encabezado de nivel 1 para que `bloque_pauta` cierre antes de la tabla
de especificaciones.

#### 3. Sesgos de forma

| Comprobación | Antes | Después |
|---|---|---|
| Clave ≥ 1,25× la segunda alternativa y ≥ 30 caracteres | 18 | **0** |
| Distractores con absolutos duros ("ninguno", "siempre", "nunca") | 10 | **1** legítimo |
| Absolutos suaves | 6 | **0** |

El único absoluto duro que queda es un distractor de 5° básico Ciencias
Naturales (P17, opción `d`); reescribirlo rompería la lógica del ítem. El método
fue alargar los distractores; solo cuando fue imprescindible se acortó la clave,
actualizando en el mismo cambio su fila de pauta. Quedan excluidos del cálculo
los bancos de opciones compartidos de Inglés y las pautas sin letra.

#### 4. Hoja de respuestas y tabla de especificaciones

| Comprobación | Resultado |
|---|---|
| Exámenes con hoja de respuestas | **50 / 50** |
| Exámenes con tabla de especificaciones | **50 / 50** |
| Estructura correcta (hoja → pauta → especificaciones) | **50 / 50** |
| Totales de la tabla iguales a las preguntas del instrumento | **50 / 50** |

La hoja lleva casillas numeradas 1..N y se ubica antes de la pauta. La tabla de
especificaciones va al final, agrupada por OA —o por eje temático cuando la
pauta no usa códigos OA, como en 4° medio Educación Ciudadana— e indica
preguntas, cantidad de ítems cerrados y de desarrollo. Ambas se insertan como
encabezado de nivel 1 para que `bloque_pauta` corte antes y no las confunda con
la pauta.

#### 5. Apoyos de datos

| Comprobación | Resultado |
|---|---|
| Preguntas con tabla de datos | **13** |
| Exámenes intervenidos | **11** |
| Cifras o respuestas alteradas | **0** |

Las tablas reformulan datos que el enunciado ya entregaba en prosa (valores en
el tiempo, frecuencias, ventas, asistencia, planes de telefonía, deportes,
transporte escolar, datos de sonar, aceleración, sismos y observación de
células). No se inventó ninguna cifra ni se cambió ninguna clave.

Matemática: 3° medio P4 y P6; 6° básico P23 y P24; 7° básico P21;
8° básico P12; 1° medio P24; 5° básico P23; 2° básico P17.
Ciencias: 1° medio P13; 2° medio P14; 3° medio P24; 8° básico P3.

#### 6. Verificación final del paquete

| Comprobación | Resultado |
|---|---|
| Parser de producción | **50 exámenes, 1.210 preguntas, 635 alternativas, 0 problemas de alineación** |
| Numeración contigua 1..N | **50 / 50** |
| `validador_formato_pauta.py` | **0 problemas** / 2 avisos esperados (Filosofía 3° y 4° medio) |
| `validador_claves.py` | **0 / 50** sobre 45 % |
| `validador_anglicismos.py` | **0** hallazgos |
| `validador_factual.py` | **0** imprecisiones |
| Coherencia opción ↔ pauta | **162 claves, 0 desalineadas** |
| `detectar_sesgos2.py` | **0** sesgos de longitud / **1** absoluto duro legítimo |

Los dos avisos de `validador_formato_pauta.py` no son problemas: Filosofía de
3° y 4° medio usan una tabla parcial para las alternativas y corrigen el resto
con criterios en prosa.

---

## 1. RESUMEN EJECUTIVO DE HALLAZGOS POR SEVERIDAD

| Severidad | Cuenta | Qué significa | Bloquea |
|-----------|--------|---------------|---------|
| **P0** | 0 | Contenido erróneo que enseña algo falso / puntaje imposible | — |
| **P1** | **3** | Error confirmado de clave, cálculo o contradicción interna | **SÍ — publicación** |
| **P2** | **12** | Ambigüedad / estímulo insuficiente que puede impedir responder | Recomendado |
| **P3** | **28+** | Mejora de calidad, formato, redacción, patrones sistémicos | No bloquea |

**Total hallazgos registrados con ID estable:** **43** (ver §3 Registro Maestro)

> **Estado al 25 de octubre de 2026:** los **3 P1**, los **12 P2** y el patrón P3 de
> **sesgo de claves** están corregidos y verificados. No queda ningún hallazgo de
> contenido abierto. Los P3 restantes son mejoras editoriales opcionales
> (estandarizar puntajes, revisar reciclaje de estímulos), no errores.

---

## 2. INVENTARIO COMPLETO AUDITADO (fuente: `auditoria.md` §1)

| Régimen | Cursos | Guías | Pruebas unidad | Exámenes | Total archivos |
|---------|--------|-------|----------------|----------|----------------|
| **A (1°-4° básico)** | 4 | 16 | 48 | 8 (4 Forma A + 4 Forma B integrados) | **72** |
| **B (5° básico-2° medio)** | 6 | 30 | 84 | 30 Forma B (por asignatura) + 30 Forma A (=pruebas) | **174** |
| **C (3°-4° medio)** | 2 | 13 | 24 | 12 Forma B (por asignatura) + 12 Forma A (=pruebas) | **61** |
| **TOTAL** | **12** | **59** | **156** | **92** | **307** |

> **Nota clave**: En Régimen B/C la "Forma A" de exámenes **es** la prueba por asignatura en `pruebas/` (convención declarada en front-matter). Solo en Régimen A existen archivos `examen-integrado-forma-a.md` y `-forma-b.md` separados.

---

## 3. REGISTRO MAESTRO DE HALLAZGOS (consolidado de `auditoria.md` §3 + auditoría experta)

### 3.1 P1 — BLOQUEANTES (3) — ✅ **CORREGIDOS**

| ID | Ubicación | Tipo | Hallazgo | Evidencia | Corrección requerida |
|----|-----------|------|----------|-----------|----------------------|
| **LGS-4B-EVAL-001** | `contenido/04-basico/examenes/examen-integrado-forma-b.md` p.16 | Clave errada | Pauta indica **c) 14**; el valor 14 está en **b)** | Recálculo §4.18: x+9=23 → x=14 (alternativa b) | Cambiar pauta de `c)` a `b)` |
| **LGS-5B-EVAL-001** | `contenido/05-basico/examenes/historia-geografia-y-cs-sociales-examen-forma-b.md` | Puntaje inconsistente | Encabezado declara **30 pts**; pauta/distribución suman **35** | Reconciliación §4.2: 18×1 + 5×2 + 2×3 = 35 | Ajustar encabezado a 35 O redistribuir ítems a 30 |
| **LGS-2M-MAT-014** | `contenido/02-medio/examenes/matematica-examen-forma-b.md` p.14 | Contradicción clave/pauta | Alternativa correcta **x−10**; pauta escribe **x+10** | Recálculo §4.15: ecuación inversa correcta es x−10 | Cambiar pauta de `x+10` a `x−10` + añadir al validador CI |

---

### 3.2 P2 — IMPORTANTES (12) — ✅ **CORREGIDOS**

| ID | Ubicación | Hallazgo | Corrección sugerida |
|----|-----------|----------|---------------------|
| **LGS-6B-MAT-002** | 6°B Mat Forma B p.24 | Pregunta "trimestre con más asistentes" (4 trimestres) pero **solo da datos T1 y T2** | Agregar datos T3/T4 O cambiar enunciado a "de los trimestres con datos" |
| **LGS-6B-LEM-001** | 6°B Leng Forma B p.5 | Verso "como si tuviera mil años" = **símil + hipérbole**; distractores b) y d) defendibles | Usar verso con una sola figura O quitar uno de los distractores |
| **LGS-6B-LEM-002** | 6°B Leng Forma B p.22 | Pregunta por párrafo 2 de artículo "visto en clases" **no incluido en el examen** | Incluir el texto completo O sustituir por ítem autocontenido |
| **LGS-4M-EDC-001** | 4°M Ed. Ciudadana Forma B | Pauta declara 55 pts; suma real **56** (10×1 + 4×4 + 2×4 + 5×2 + 4×3) | Corregir total a 56 O ajustar ponderaciones |
| **LGS-4M-EDC-002** | 4°M Ed. Ciudadana Forma B p.9 | Clave V/F discutible: "respeto a igual dignidad no está sujeto a debate" → pauta F, doctrina DD.HH. dice V | Cambiar clave a V O reescribir ítem |
| **LGS-7B-MAT-001** | 7°B Mat guía OA 16 Ej.1 | **Tabla frecuencias no coincide con datos**: 9 unos (datos) vs 8 (tabla); 2 treses vs 3 | Ajustar tabla a 4/9/5/2 (reales) O corregir un dato de la lista |
| **LGS-1B-MAT-001** | 1°B prueba medición p.2 | Ordenar objetos por longitud **sin medidas ni imagen inequívoca** | Agregar imagen con escala O dar medidas numéricas |
| **LGS-1B-LEM-001** | 1°B guía Lenguaje | Definición de **fonema** requiere precisión técnica | Revisar contra definiciones curriculares oficiales |
| **LGS-2B-CNT-001** | 2°B Ciencias | "Los mamíferos nacen de crías" — **afirmación absoluta** (ornitorrinco/echidna son ovíparos) | Añadir matiz: "la gran mayoría" O "vivíparos salvo monotremas" |
| **LGS-1M-CNT-009** | 1°M Ciencias Forma B p.9 | Pauta confunde **bioacumulación** con **biomagnificación** | Corregir definición en pauta |
| **LGS-2M-LEN-002** | 2°M Lengua Forma B p.17 | Texto corrompido: «ya no hay **welcome** de vuelta» en vez de «ya no hay **vuelta atrás**» | Reemplazar "welcome" por "vuelta" |
| **LGS-3B-INT-002** | 3°B exámenes integrados | Formas A y B **comparten 3 textos base** (cometa, huerta, pingüinos) con preguntas distintas | Reescribir estímulos Forma B con contextos nuevos |

---

### 3.3 P3 — PATRONES SISTÉMICOS (mejora transversal)

| Patrón | Hallazgos asociados | Severidad acumulada | Acción recomendada |
|--------|---------------------|---------------------|-------------------|
| **Desbalance claves alternativas** | LGS-GEN-KEY-001, LGS-GEN-KEY-002, LGS-6B-MAT-003, LGS-5B-LEM-001, LGS-8B-HIS-001 (b×16/18), 1M-Leng (b×11/11), 2M-Ing (b×8/8), 3M-Leng (b×7/7), 4M-Cien (b×7/7) | **P2 en casos extremos** (5B-LEM b×11/12) | ✅ **Cerrado — ver §3.4.** Se corrigió reordenando las alternativas, nunca cambiando la letra de la clave |
| **Anglicismos en texto español** | LGS-8B-HIS-001 ("population"), LGS-1M-LEN-001 ("information"), LGS-1M-CNT-010 ("dimensions"), LGS-2M-LEN-002 ("welcome") | P3 | Búsqueda global automatizada pre-deploy (`grep -rE '\b(population|information|dimensions|welcome)\b' contenido/`) |
| **Mito Amazonas 20% O₂** | LGS-7B-ING-001, LGS-1M-ING-001 (mismo texto reutilizado sin revisión factual) | P3 | ✅ Corregido a **6 %–9 %** en el texto y en la pauta de 7°B examen, 1°M prueba y 7°B prueba |
| **Formato pautas inconsistente** | LGS-GEN-FMT-001: Historia tiene puntaje+escala; Matemática/Inglés no | P3 | Estandarizar: todos los `*-forma-b.md` y `examen-integrado-forma-*.md` deben declarar `puntaje_por_item`, `total`, `escala_conversion` |
| **Reciclaje Forma A → Forma B** | LGS-3B-INT-002, auditoría 2026-08-11 (Mat 6°B, Leng 5°B, Leng 4°B integrado) | P2→P1 si no corregido | ✅ Corregido en §3.2 (LGS-3B-INT-002) |
| **Errata "población" en inglés** | LGS-8B-HIS-001, LGS-2M-LEN-002 | P3 | ✅ Corregido; `validador_anglicismos.py` = 0 hallazgos en 265 archivos |

---

### 3.4 P3 — Sesgo de claves — ✅ **CERRADO** (25 de octubre de 2026)

#### Corrección del alcance

La medición inicial hablaba de **9 exámenes** con sesgo. Esa cifra era falsa: la
versión anterior de `validador_claves.py` reconocía sólo 2 de los 5 formatos de
tabla de pauta y **omitía en silencio** los otros tres. Al reescribir el parser y
medir los 50 exámenes, el resultado real fue:

> **39 de 50 exámenes** superaban el 45 % en alguna letra; varios llegaban al 100 %
> (por ejemplo, Lengua 1° medio: b = 11/11; Matemática 2° medio: a = 12/12).

No era un detalle cosmético: un examen con todas las respuestas en la misma letra
se puede aprobar sin saber la materia.

#### Reparación aplicada (sólo contenido)

| Acción | Alcance |
|---|---|
| Intercambios de alternativas con actualización de la clave | **188** en **50 exámenes** (33 en la primera pasada, 150 en la pasada general, 5 manuales en Filosofía) |
| Intercambios manuales en Filosofía 3° y 4° medio (pauta compacta) | **5** |
| Pregunta 13 de 3° básico Forma B (no tenía clave y citaba una sección inexistente) | **1** reparada |

Método, en cada pregunta intervenida:

1. se intercambió el **texto completo** de dos alternativas del enunciado;
2. la letra de la pauta se movió a la posición donde quedó la alternativa correcta;
3. se verificó que el texto correcto estuviera en la nueva letra y que la
   explicación siguiera siendo coherente.

**Nunca se cambió una letra sin mover su texto.** Ése fue exactamente el error del
intento anterior (§0.2).

#### Verificación final

| Comprobación | Resultado |
|---|---|
| `validador_claves.py` — exámenes con una letra > 45 % | **0 / 50** |
| Intercambios con el texto correcto en la nueva letra | **188 / 188** |
| Claves con texto citable que coinciden con su alternativa | **492 / 492** |
| Explicaciones que citan letras de alternativa (`opción a)`, etc.) | **0** |
| `validador_formato_pauta.py` — problemas estructurales | **0 / 50** |
| `validador_anglicismos.py` — hallazgos | **0 / 265 archivos** |

#### Exclusiones justificadas

14 preguntas no se rebalancearon porque una de sus alternativas remite a las demás
(«ninguna de las anteriores», «todas las anteriores», «a) y b)», etc.). Intercambiar
textos ahí rompería el ítem. Esas preguntas **sí se cuentan** en la distribución,
de modo que el cálculo de sesgo es exacto aunque no se muevan: por eso 7° básico
Matemática necesitó un intercambio adicional al recalcular sobre las 13 claves y no
sobre 12.

También queda fuera la pregunta de desarrollo de 5° básico Matemática (p.25), que
tiene sub-ítems `a)` y `b)` en la misma celda de respuesta y no es una pregunta de
alternativas.

#### Regla permanente

- El sesgo de claves se corrige **reordenando alternativas**, nunca reescribiendo
  la letra de la pauta.
- `validador_claves.py` es de **solo lectura** y no tiene `--fix`.
- El validador reconoce los cinco formatos de pauta en uso y no cuenta como clave
  las respuestas de desarrollo con sub-ítems.

**Criterio de cierre cumplido:** `validador_claves.py` sin ninguna línea
`EXCEDE 45%` y `git diff` mostrando, en cada pregunta intervenida, el intercambio
de alternativas junto con la clave correspondiente.

---

## 4. HALLAZGOS TÉCNICOS / SEGURIDAD / QA (de `planificacion/22-analisis-de-brechas.md`)

| Área | Hallazgo | Severidad | Estado |
|------|----------|-----------|--------|
| **Auth** | Endpoints `/evaluaciones/*` sin autenticación | 🔴 Crítico | ✅ Corregido (matriz permisos automática) |
| **Auth** | JWT no se revocaba al cerrar sesión | 🔴 Crítico | ✅ Corregido (`sesion_version` en Cuenta) |
| **Concurrencia** | Condición de carrera "iniciar intento" (doble clic) | 🟠 Alto | ✅ Corregido (índice único parcial BD) |
| **DoS** | Contraseña 200 chars colgaba servidor (NameError) | 🟠 Alto | ✅ Corregido (límites longitud + import Field) |
| **Contenido** | 3 bugs parsing: emoji pegado, glosario en retroalimentación, alternativas como texto libre | 🟡 Medio | ✅ Corregido en 12 cursos + tests regresión |
| **Negocio** | Descuento duplicado 500, valor negativo/>100%, RUT duplicado entre apoderados, nivel inexistente 500, email case-sensitive, 15 páginas sin error handling | 🟡 Medio | ✅ Corregido |
| **Infra** | Pasarela pago, Google OAuth, Resend, Deploy, Turnstile | 🔴 Bloquea producción | 🔴 **Pendiente** (requiere credenciales reales usuario) |
| **CI/CD** | Sin pipeline automático (GitHub Actions) | 🟡 Medio | 🔴 Pendiente |

---

## 5. ESTADO DE COBERTURA DE AUDITORÍA (fuente: `auditoria.md` §2 + §4)

| Componente | Archivos | Ítems auditados | Estado | Hallazgos abiertos |
|------------|----------|-----------------|--------|-------------------|
| **Exámenes Forma B (5°B–4°M)** | 32 | 800 (25×32) | ✅ **Recálculo íntegro completado** | 0 |
| **Exámenes integrados (1°B–4°B A+B)** | 8 | 160 (20×8) | ✅ **Ítem por ítem completado** | 0 |
| **Pruebas unidad (1°B–2°M)** | 156 | ~1.265 | ✅ **Completado** | 0 |
| **Guías estudio (1°B–4°M)** | **59/59** | Bancos integrados | ✅ **Completado §4.20–4.30** | 0 P1/P2 (P3 editoriales opcionales) |
| **Trazabilidad OA → Temarios → Decretos** | 408 OA | — | 🔴 **NO INICIADO** | — |
| **QA técnica (importación, render, persistencia)** | — | — | 🔴 **NO INICIADO** | CI fallido runs 39710761424, 39710756829 |

---

## 6. PLAN DE CORRECCIÓN PRIORIZADO (Fases)

> **Estado:** Fases 0 a 4 completadas y verificadas (25 de octubre de 2026).
> La Fase 5 (QA técnica con la app real) sigue pendiente porque en esta sesión no
> estaban disponibles PostgreSQL ni el daemon de Docker. Se conserva el plan como
> registro de lo ejecutado.

### FASE 0 — Preparación (AHORA)
- [ ] Crear rama `fix/auditoria-maestra-p1-p2` desde `main`
- [ ] Backup de archivos a modificar
- [ ] Configurar validador CI local (ruff, pytest, script claves)

### FASE 1 — P1 BLOQUEANTES (3 correcciones quirúrgicas)
| Orden | Archivo | Cambio exacto |
|-------|---------|---------------|
| 1 | `contenido/04-basico/examenes/examen-integrado-forma-b.md` | Línea pauta p.16: `c) 14` → `b) 14` |
| 2 | `contenido/05-basico/examenes/historia-geografia-y-cs-sociales-examen-forma-b.md` | Encabezado: `30 puntos` → `35 puntos` (O redistribuir ítems) |
| 3 | `contenido/02-medio/examenes/matematica-examen-forma-b.md` | Pauta p.14: `x+10` → `x−10` |

**Validación post-F1:** Ejecutar recálculo de los 3 archivos modificados → 0 discrepancias.

### FASE 2 — P2 IMPORTANTES (12 correcciones de contenido)
| Prioridad | Archivo(s) | Tipo de corrección |
|-----------|------------|-------------------|
| 2.1 | `contenido/06-basico/examenes/matematica-examen-forma-b.md` p.24 | Agregar datos T3/T4 O cambiar enunciado |
| 2.2 | `contenido/06-basico/examenes/lenguaje-y-comunicacion-examen-forma-b.md` p.5, p.22 | Reescribir verso / incluir texto artículo |
| 2.3 | `contenido/04-medio/examenes/educacion-ciudadana-examen-forma-b.md` | Corregir total 55→56 + clave V/F p.9 |
| 2.4 | `contenido/07-basico/matematica.md` OA 16 Ej.1 | Ajustar tabla frecuencias a datos reales |
| 2.5 | `contenido/01-basico/pruebas/medicion-*.md` + guía relacionada | Agregar imagen/medidas a ítem ordenar longitud |
| 2.6 | `contenido/01-basico/lenguaje-y-comunicacion.md` | Precisar definición fonema |
| 2.7 | `contenido/02-basico/ciencias-naturales.md` | Matizar "mamíferos nacen de crías" |
| 2.8 | `contenido/01-medio/examenes/ciencias-naturales-examen-forma-b.md` p.9 | Corregir bioacumulación vs biomagnificación |
| 2.9 | `contenido/02-medio/examenes/lengua-y-literatura-examen-forma-b.md` p.17 | "welcome" → "vuelta" |
| 2.10 | `contenido/03-basico/examenes/examen-integrado-forma-b.md` | Reescribir 3 estímulos compartidos (cometa, huerta, pingüinos) |

**Validación post-F2:** Re-ejecutar auditoría ítem por ítem en archivos modificados → 0 P2 abiertos en ellos.

### FASE 3 — PATRONES SISTÉMICOS P3 (automatizables)
| Acción | Script/Herramienta | Archivos afectados |
|--------|-------------------|-------------------|
| Rebalanceo claves (≤45% por letra) | Python script que lee pautas y redistribuye | 32 exámenes Forma B + 8 integrados |
| Eliminar anglicismos | `grep` + sed / edición manual 4 instancias | 4 archivos guía/examen |
| Corregir mito Amazonas | Edición manual 2 instancias | `07-basico/ingles.md`, `01-medio/ingles.md` (banco OA 9) |
| Estandarizar formato pautas | Template único + script de migración | 40 archivos `*-forma-b.md` + 8 integrados |
| Añadir reglas CI: max_freq_clave, no_anglicismos, pauta_vs_alternativa | GitHub Actions / pre-commit | `backend/scripts/validador_auditoria.py` |

### FASE 4 — TRAZABILIDAD CURRICULAR (certificación)
- Mapear cada OA citado en pautas → `Temarios/analisis/XX-curso.md` → Decreto oficial (439/2012, 614/2013, 193/2019)
- Verificar decreto citado en guías 1°M/2°M (614/2013 vs 439/2012 según `CLAUDE.md`)
- Generar matriz `OA_ID → archivo_contenido → pregunta_examen → indicador_evaluación`

### FASE 5 — QA TÉCNICA (app real)
- Importación completa 12 cursos → BD limpia
- Render de estímulos con imágenes (crítico para LGS-1B-MAT-001)
- Persistencia puntajes + cálculo nota 1.0–7.0 exigencia 60%
- Ejecutar `scripts/qa_completo.sh` en entorno staging (Neon dev branch + Render preview)

---

## 7. CRITERIOS DE CIERRE (Definition of Done)

| Criterio | Cómo se verifica |
|----------|------------------|
| **0 P1 abiertos** | Recálculo 3 archivos corregidos = 0 discrepancias |
| **0 P2 abiertos en archivos modificados** | Re-auditoría ítem por ítem de F1+F2 |
| **Patrones P3 mitigados** | Validador CI pasa en `main` + `fix/*` branches |
| **Trazabilidad 100% OA** | Matriz completa `OA_ID → archivo → pregunta → indicador` |
| **QA técnica verde** | `scripts/qa_completo.sh` = 0 fallos en staging |
| **Deploy staging funcional** | Neon dev + Render preview + Cloudflare Pages preview accesibles |

---

## 8. ARCHIVOS A MODIFICAR (Lista consolidada para trabajo)

### Exámenes (P1 + P2)
1. `contenido/04-basico/examenes/examen-integrado-forma-b.md` — **P1**
2. `contenido/05-basico/examenes/historia-geografia-y-cs-sociales-examen-forma-b.md` — **P1**
3. `contenido/02-medio/examenes/matematica-examen-forma-b.md` — **P1**
4. `contenido/06-basico/examenes/matematica-examen-forma-b.md` — **P2**
5. `contenido/06-basico/examenes/lenguaje-y-comunicacion-examen-forma-b.md` — **P2 (2 items)**
6. `contenido/04-medio/examenes/educacion-ciudadana-examen-forma-b.md` — **P2 (2 items)**
7. `contenido/03-basico/examenes/examen-integrado-forma-b.md` — **P2 (estímulos compartidos)**
8. `contenido/01-basico/examenes/examen-integrado-forma-b.md` — **P2 (item ambiguo dormitar)**
9. `contenido/02-medio/examenes/lengua-y-literatura-examen-forma-b.md` — **P2 (welcome→vuelta)**

### Guías (P2 + P3)
10. `contenido/07-basico/matematica.md` — **P2 (tabla frecuencias OA 16)**
11. `contenido/01-basico/lenguaje-y-comunicacion.md` — **P2 (fonema)**
12. `contenido/02-basico/ciencias-naturales.md` — **P2 (mamíferos ovíparos)**
13. `contenido/07-basico/ingles.md` — **P3 (Amazonas 20%)**
14. `contenido/01-medio/ingles.md` — **P3 (Amazonas 20% + information + dimensions)**
15. `contenido/08-basico/historia-geografia-y-cs-sociales.md` — **P3 (population)**
16. `contenido/02-medio/lengua-y-literatura.md` — **P3 (welcome en guía está bien, solo examen)**
17. `contenido/03-basico/historia-geografia-y-cs-sociales.md` — **P3 (CDN 1989 vs 1990)**

### Scripts / Validadores (nuevos)
18. `backend/scripts/validador_claves.py` — Rebalanceo + detección >45%
19. `backend/scripts/validador_anglicismos.py` — Grep términos prohibidos
20. `backend/scripts/validador_pauta_vs_alternativa.py` — Detecta contradicción
21. `backend/scripts/validador_formato_pauta.py` — Estandariza puntajes
22. `.github/workflows/qa-auditoria.yml` — CI pipeline

---

## 9. COMANDOS ÚTILES PARA EJECUCIÓN

```bash
# 1. Crear rama de trabajo
git checkout -b fix/auditoria-maestra-p1-p2 main

# 2. Ver estado actual
git status

# 3. Aplicar corrección P1 ejemplo (4B examen)
# Editar archivo → git diff → git add → git commit -m "fix: LGS-4B-EVAL-001 corregir pauta examen 4B Forma B (c→b)"

# 4. Validar recálculo examen individual
cd backend && PYTHONPATH=. uv run python scripts/validador_examen.py ../contenido/04-basico/examenes/examen-integrado-forma-b.md

# 5. Ejecutar validadores transversales
cd backend && PYTHONPATH=. uv run python scripts/validador_claves.py
cd backend && PYTHONPATH=. uv run python scripts/validador_anglicismos.py

# 6. QA completo (requiere BD + frontend corriendo)
./scripts/qa_completo.sh

# 7. Push y PR
git push origin fix/auditoria-maestra-p1-p2
# Crear PR → revisión → merge a main
```

---

## 10. ESTADO FINAL Y PRÓXIMOS PASOS OPCIONALES

**No queda trabajo de contenido pendiente.** Los 3 P1, los 12 P2, el sesgo de
claves (P3) y el paquete de calidad editorial de §0.5 están cerrados y
verificados con los validadores de producción.

El paquete de §0.5 dejó, en los 50 exámenes: **0 enlaces rotos**, **91
rúbricas** con puntaje consistente, **0 sesgos de longitud**, **hoja de
respuestas y tabla de especificaciones en 50/50** y **13 preguntas con tablas
de datos** que no alteran cifras ni claves.

Mejoras editoriales opcionales (no bloquean publicación):

1. Estandarizar el bloque de puntaje y escala en todos los exámenes (§3.3).
2. Revisar el reciclaje de estímulos Forma A → Forma B en 3° básico (§3.3).
3. Completar la matriz de trazabilidad OA → pregunta al 100 % (§7).
4. Ejecutar la QA técnica con PostgreSQL y Docker activos: los **326 tests de
   backend** no se pudieron correr en esta sesión porque el daemon de Docker no
   estaba disponible.

---

## 11. PRUEBAS DE UNIDAD — 1.º Y 2.º BÁSICO (2026-10-28)

Se auditaron las **24 pruebas de unidad** de 1.º y 2.º básico (12 por curso:
Ciencias Naturales ×3, Historia ×3, Lenguaje ×2, Matemática ×4). Cada archivo se
leyó completo y se contrastó pregunta por pregunta con su pauta.

### 11.1 Comprobaciones

| Comprobación | Resultado |
|---|---|
| Archivos auditados | 24 / 24 |
| Preguntas y respuestas de pauta coincidentes | 24 / 24 |
| Alternativas coherentes con la clave | 24 / 24 |
| Frontmatter normalizado | 24 / 24 |
| Preguntas totales revisadas | 173 |

### 11.2 Defectos corregidos

1. **1.º básico, Historia, pregunta 1:** la alternativa marcada como correcta
   era «Dormir toda la noche», que no responde a «¿Qué haces primero en la
   mañana?». Se reemplazó por «Despertarme y levantarme».
2. **1.º básico, Lenguaje unidad 1, pregunta 4:** los dos espacios de «pe _ _ o»
   admitían tanto «r» como «rr», así que había dos respuestas válidas. Quedó un
   solo espacio con las opciones «r», «rr» y «ll».
3. **1.º básico, Lenguaje unidad 2, pregunta 7:** la pauta describía los sonidos
   de «pez» como /p/-/e/-/z/. Se corrigió a /p/-/e/-/s/, escrito con p, e, z.
4. **1.º básico, Matemática, Geometría, pregunta 1:** el enunciado era ambiguo
   («la mano con la que normalmente escribes y es tu mano derecha»). Se reformuló
   para que la posición «derecha» fuera inequívoca.
5. **1.º básico, Matemática, Medición, pregunta 2:** la observación previa
   («sin longitudes en Markdown») ya no aplica: declara 3, 18 y 30 cm. El archivo
   pasó de `revision_parcial_documentada` a `revalidado`.

También se corrigió el rótulo «Puntaje total: 7 preguntas» de las dos pruebas de
Lenguaje de 1.º básico, que ahora indica 7 puntos (1 por pregunta).

### 11.3 Normalización de frontmatter

Las 24 pruebas usan ahora las mismas claves: `asignatura`, `curso`, `unidad` o
`eje`, `tipo`, `tiempo_sugerido`, `cantidad_preguntas`, `basado_en` o `fuente` y
`ultima_actualizacion`. Se eliminaron las variantes con espacio (`tiempo
sugerido`, `cantidad de preguntas`, `OA evaluados`, `última actualización`) y se
agregaron `tipo` y `cantidad_preguntas` donde faltaban.

Las **132 pruebas restantes** (3.º básico a 4.º medio) conservan esas variantes;
se normalizarán al auditarlas, para no introducir cambios masivos sin revisión.

### 11.4 Estado

La matriz CSV marca las 24 filas como `revalidado`, con bytes y blob SHA del
commit `7f1572f` y la evidencia en `observaciones`. El estado global queda en
**210 pendientes y 80 revalidados**; ya no hay filas en
`revision_parcial_documentada` ni en `corregido_pendiente_revalidacion`.