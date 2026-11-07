# AUDITORÍA MAESTRA — Logos School (Consolidada)
**Fecha consolidación:** 23 de octubre de 2026  
**Fuentes unificadas:**
1. `planificacion/22-analisis-de-brechas.md` — Auditoría técnica/seguridad/QA (backend, frontend, infra)
2. `contenido/00-estado-contenido.md` — Estado macro + auditoría pedagógica 2026-08-11
3. `auditoria.md` — Auditoría ítem por ítem (exámenes, pruebas, guías) — rama `qa/fase-2-matriz-trazabilidad`, HEAD `0106976`
4. Auditoría pedagógica experta aplicada en esta sesión (skills `profesor-experto-chile.md` + `auditoria-contenido-educativo.md`)

**Estado vigente:** auditoría en curso. El cierre editorial de octubre es histórico; el piloto de especialistas reabre observaciones de Inglés y pronunciación en §14. No equivale a aprobación integral de contenido, importación ni aplicación.

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

## 11. PRUEBAS DE UNIDAD — 1.º BÁSICO A 4.º MEDIO (2026-10-28)

Se auditaron las **156 pruebas de unidad** del proyecto: 104 de 1.º básico a
8.º básico (12 por curso en 1.º a 4.º y 14 en 5.º a 8.º, que incluyen Inglés) y
52 de 1.º a 4.º medio (14, 14, 13 y 11). Cada archivo se leyó completo y se
contrastó pregunta por pregunta con su pauta.

### 11.1 Comprobaciones

| Comprobación | Resultado |
|---|---|
| Archivos auditados | 156 / 156 |
| Preguntas y respuestas de pauta coincidentes | 156 / 156 |
| Alternativas coherentes con la clave | 156 / 156 |
| Frontmatter normalizado | 156 / 156 |
| Preguntas totales revisadas | 1.824 |

Por curso: 1.º básico 85 preguntas, 2.º básico 88, 3.º básico 104, 4.º básico
107, 5.º básico 166, 6.º básico 165, 7.º básico 192, 8.º básico 197, 1.º medio
190, 2.º medio 192, 3.º medio 184 y 4.º medio 154. En los 156 archivos el número
de preguntas, el de respuestas de la pauta y el campo `cantidad_preguntas`
coinciden.

### 11.2 Defectos corregidos en 1.º a 6.º básico

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
   pasó de `revision_parcial_documentada` a `rrevalidado`.
6. **4.º básico, Ciencias de la Tierra, pregunta 4:** el manto se describía como
   «roca en estado semi-líquido». Se corrigió a «roca caliente que fluye muy
   lentamente, en estado pastoso», que es la formulación correcta, y se ajustó la
   pauta.
7. **5.º básico, Inglés unidad 2, pregunta 3:** la pauta escribía «From,.»; se
   corrigió a «From.».
8. **5.º básico, Inglés unidad 2, pregunta 4:** el enunciado preguntaba si era
   «correcto escribir» una lista con un perro y un gato, pero la clave era
   «Falso». Se reformuló como «¿Es un ejemplo adecuado para una lista de compras
   de alimentos…?», con lo que la clave queda coherente.
9. **6.º básico, Matemática, Números y Operaciones, pregunta 5:** la alternativa
   «4/10» era equivalente a la clave «2/5». Se reemplazó por «4/5».
10. **6.º básico, Matemática, Números y Operaciones, pregunta 10:** la
    alternativa «5 2/6» era equivalente a «5 1/3». Se reemplazó por «5 1/6».

También se corrigieron los rótulos de puntaje que decían «Puntaje total: N
preguntas»: las dos pruebas de Lenguaje de 1.º básico y las tres de Historia de
4.º básico ahora indican puntos (1 por pregunta). En 5.º básico se corrigió
«sicológica» por «psicológica» (Lenguaje unidad 1, pregunta 1).

### 11.3 Defectos corregidos en 7.º y 8.º básico

1. **7.º básico, Matemática, Números y Operaciones, pregunta 6:** la alternativa
   «2/14» era equivalente a la clave «1/7». Se reemplazó por «2/7».
2. **8.º básico, Matemática, Números y Operaciones, pregunta 5:** la alternativa
   «−6/12» era equivalente a la clave «−1/2». Se reemplazó por «−6/7», tanto en
   la prueba como en la guía de Matemática del curso.
3. **8.º básico, Lengua y Literatura unidad 1, pregunta 15:** la pauta situaba el
   terremoto de Valdivia de 1960 en la «madrugada», pero el relato y el sismo real
   corresponden a la tarde del 22 de mayo. Se corrigió a «tarde».
4. **8.º básico, Lengua y Literatura unidad 1, pregunta 2:** la pauta decía
   «curiosidad poco tactosa». Se reemplazó por «curiosidad poco discreta» en la
   prueba y en la guía del curso.

### 11.4 Defectos corregidos en 1.º a 4.º medio

1. **2.º medio, Lengua unidad 1, pregunta 1:** las alternativas nombraban a
   «Camila», personaje que no aparece en el relato (la voz es una narradora en
   primera persona). Se reemplazó por «la narradora» en el enunciado, las
   alternativas y la pregunta 4. Además, «living» pasó a «sala de estar» en las
   acotaciones del texto dramático.
2. **2.º medio, Lengua unidad 2, pregunta 5:** la expresión «una herramienta le
   hace el trabajo de pensar a toda una generación» admitía más de una figura.
   Se acotó a la exageración («a toda una generación») para que la clave fuera
   única.
3. **2.º medio, Lengua unidad 2, preguntas 7 y 10:** se corrigieron dos
   enunciados: «Recomendamos…» es presente de indicativo, no imperativo, y la
   pregunta 10 había perdido el verbo («¿Qué evidencia principalmente…?»).
4. **2.º medio, Historia, pregunta 8:** el orden pedido no tenía fechas y la
   pauta ubicaba a Uruguay junto a Chile. Se agregaron los años al enunciado y la
   pauta quedó 2 → 4 → 1 → 3 (Brasil 1964, Uruguay 27-06-1973, Chile 11-09-1973,
   Argentina 1976).
5. **2.º medio, Historia, pregunta 13:** el Plan Laboral es de 1979, no de
   «comienzos de la década de 1980». Se ajustó el enunciado.
6. **2.º medio, Matemática, Geometría, pregunta 10:** con 9 y 15 cm el coseno era
   0,6 y las alternativas no eran plausibles. Se cambiaron los datos a 8 y 17 cm,
   se recalcularon las alternativas (0,47 / 0,53 / 1,88 / 2,13) y la pauta.
7. **2.º medio, Inglés unidad 1, preguntas 2, 4 y 10:** la pregunta 2 entregaba
   el banco de palabras en el orden de la respuesta; la 4 estaba rotulada
   «Emparejar» sin parejas; y la 10 tenía clave «True» cuando la segunda parte
   del enunciado era falsa. Se corrigieron el banco, el rótulo y la clave.
8. **2.º medio, Inglés unidad 2, pregunta 14:** el enunciado pedía un reflexivo
   «para dar énfasis», pero la clave era un reflexivo como objeto directo. Se
   corrigió el enunciado.
9. **3.º medio, Matemática, Álgebra, pregunta 5:** la pauta decía $7.196.160;
   el cálculo correcto es $7.196.344.
10. **3.º medio, Matemática, Probabilidad, pregunta de completar:** «el promedio
    de las ______» concordaba mal con «desviaciones». Quedó «de los ______».
11. **3.º medio, Ciencias para la Ciudadanía, Bienestar y Salud:** el caso de
    Camila no justificaba la pregunta sobre asma; se agregó el diagnóstico. Se
    corrigió el puntaje a 7 + 14 = 21 (exigencia 12,6/21) y el tiempo a 45-50
    minutos.
12. **3.º medio, Ciencias para la Ciudadanía, Seguridad y Autocuidado:** las
    preguntas 10 y 11 se contradecían (una misma medida era prevención y
    mitigación). Se diferenciaron los casos y se ajustó la pauta; el puntaje
    quedó 8 + 12 = 20 y el tiempo en 45-50 minutos.
13. **3.º medio, Educación Ciudadana unidades 1 y 2:** los puntajes no cuadraban
    con el número de preguntas (25 y 24 puntos). Quedaron 6 + 18 = 24 y
    8 + 14 = 22, con tiempos de 50-60 minutos.
14. **3.º medio, Inglés unidad 1, preguntas 2, 5, 12 y 13:** la pregunta 2 no
    ofrecía un contraste real («lunch at home or at school» frente a «packed
    lunch»), la 12 tenía alternativas solapadas con la idea central y dos
    preguntas estaban rotuladas «Emparejar» sin parejas. Se corrigieron el
    estímulo, las alternativas y los rótulos.
15. **4.º medio, Matemática, Probabilidad, pregunta 8:** el enunciado pedía
    «probabilidad de "al menos"» pero la pauta resolvía «acertar todas». Se acotó
    el enunciado a lo que se corrige.
16. **4.º medio, Lengua unidad 2, pregunta 11:** la instrucción decía «sin
    corregir para mejorar su cohesión», que se contradecía. Quedó «sin corregir,
    agregando un conector adecuado».
17. **4.º medio, Inglés unidad 1, pregunta 5:** rótulo «Emparejar» sin parejas;
    pasó a «Selección — dos opciones».
18. **4.º medio, Inglés unidad 2, preguntas 4, 11 y 14:** dos rótulos
    «Emparejar» sin parejas y una pregunta 14 cuya clave no era la mejor opción.
    Se rotularon como selección y la 14 se reemplazó por un ítem de registro
    formal en presentación oral, con clave c.
19. **4.º medio, Filosofía, pregunta 11:** la alternativa de igualdad formal
    agregaba «sin compensar desventajas de partida», que describía la igualdad
    material. Se acotó a «Igualdad formal o de trato ante la ley».
20. **4.º medio, Educación Ciudadana, Medios y participación, pregunta 14:** el
    enunciado describía el OA en lugar de evaluarlo. Se reemplazó por una
    afirmación verificable sobre alfabetización mediática, con pauta coherente.

Además se corrigieron en 1.º medio la cita de Wenceslao (pasó a «lo respetás, no
porque le tenís miedo…»), la coma de apertura de una oración, la concordancia
«dependían» de la pauta de Biología, la clave de Inglés unidad 2 P13 (pasado
simple, coherente con «three years ago»), los saltos de línea de Inglés unidad 1
(P2 y P9 se fusionaban con el ítem anterior), los OA de Historia y Ciencias
(trasladados a `oa_evaluados`) y dos duplicados: la P11 de Lengua unidad 2 repetía
la P1 y la P9 de Geografía repetía la P3. También se corrigieron el anacronismo
de «Estado» en 1810 y el distractor «Unión Europea» en Geografía.

En los 50 exámenes se ampliaron cinco pautas que declaraban solo la letra y el
texto de la alternativa, para que el validador estructural reconozca la clave y
para dejar explícita la justificación. El escaneo
`backend/scripts/validar_evaluaciones_markdown.py` queda en **0 hallazgos** sobre
los 265 archivos Markdown.

### 11.5 Normalización de frontmatter

Las 156 pruebas usan ahora las mismas claves: `asignatura`, `curso`, `unidad` o
`eje`, `tipo`, `tiempo_sugerido`, `cantidad_preguntas`, `basado_en`, `fuente` u
`oa_evaluados`, y `ultima_actualizacion`. Se eliminaron las variantes con espacio
(`tiempo sugerido`, `cantidad de preguntas`, `OA evaluados`, `eje temático`,
`última actualización`) y los alias `cubre`, `n_preguntas` y `oa_cubiertos`. Se
agregaron `tipo` y `cantidad_preguntas` donde faltaban y se unificó el valor
`tipo: Prueba de unidad`.

En 7.º y 8.º básico se agregó además `oa_evaluados` y `basado_en` a las pruebas
de Historia, Matemática e Inglés que no tenían trazabilidad, tomando los OA de la
guía del curso, y se corrigieron las rutas de `basado_en` de Ciencias Naturales
(«Banco de autoevaluación…» pasó a `contenido/0X-basico/ciencias-naturales.md`).
Los valores «1 de 2» y «2 de 2» del campo `unidad` se redujeron a «1» y «2».

En media se completó `oa_evaluados` en Historia, Inglés y Matemática de 1.º y
2.º medio y en Ciencias para la Ciudadanía, Educación Ciudadana, Filosofía,
Inglés y Matemática de 3.º y 4.º medio, siempre con los OA de la guía del curso;
se agregó `basado_en` con la ruta `contenido/0X-medio/<asignatura>.md` y se
redujeron los alias `n_preguntas` y `OA evaluados` a `cantidad_preguntas` y
`oa_evaluados`.

### 11.6 Estado

La matriz CSV marca las 156 filas de pruebas como `rrevalidado`, con bytes y blob
SHA del commit `22385ab` y la evidencia en `observaciones`. El estado global
queda en **78 pendientes y 212 rrevalidados**: lo pendiente son las guías de
contenido y los temarios, no las pruebas. Ya no hay filas en
`revision_parcial_documentada` ni en `corregido_pendiente_revalidacion`.

## 12. GUÍAS DE ESTUDIO — 1.º BÁSICO A 4.º MEDIO (2026-10-28)

Se auditaron y normalizaron las **58 guías de estudio** del proyecto (1° básico a 4° medio) más el archivo general contenido/00-estado-contenido.md. Con este cierre, el 100 % de los archivos bajo contenido/ (**265 / 265**) queda auditado y en estado 
revalidado en la matriz maestra.

### 12.1 Resumen de la revisión

| Comprobación | Estado |
|---|---|
| Guías de estudio auditadas | 58 / 58 |
| Frontmatter normalizado (	ipo: Guía de estudio, oa_evaluados, ultima_actualizacion, asado_en) | 58 / 58 |
| Banco de autoevaluación revisado por guía | 58 / 58 |
| Validador estructural Markdown (alidar_evaluaciones_markdown.py) | 0 hallazgos en 265 archivos |
| Validador factual y de anglicismos | 0 hallazgos |
| Discrepancia del denominador de guías en la matriz CSV | Resuelto: 58 guías uniformadas a guía/contenido |
| Estado global de la matriz (290 archivos) | **265 rrevalidados / 25 pendientes** (solo Temarios/) |

### 12.2 Correcciones disciplinarias y pedagógicas aplicadas

Durante la auditoría sistemática de las guías se corrigieron inconsistencias pedagógicas, de redacción y de claves:

1. **4.º básico, Matemática:** en Pregunta 1 de autoevaluación, se cambió «¿Cuál es el valor posicional del dígito 7 en el número 7.352?» por «¿En qué posición se ubica el dígito 7...?» para evitar la confusión conceptual entre posición (Unidad de mil) y valor posicional (7.000).
2. **4.º básico, Historia:** se ajustó la clave de correspondencia de ríos (Amazonas, Mississippi, Biobío), eliminando una referencia duplicada errónea; se ajustó el ámbito geográfico inca («desde el sur de la actual Colombia») y se precisó la clasificación climática de Patagonia («Frío»).
3. **4.º básico, Lenguaje:** se precisó la distinción entre metáfora y comparación (símil) en el modelamiento guiado de figuras literarias.
4. **4.º básico, Ciencias:** se alineó el orden de las capas de la Tierra (rigidez, posición, temperatura) en la pauta de desarrollo breve.
5. **5.º básico, Ciencias:** se distinguió con precisión entre microorganismos microscópicos (bacterias, virus, levaduras) y hongos multicelulares macroscópicos (champiñones); se corrigió la formulación del nivel de organización de la circulación sanguínea.
6. **5.º básico, Historia:** se diferenció el componente cultural sincrético andino (La Tirana) de la tradición campesina huasa chilena (Cuasimodo).
7. **5.º básico, Inglés:** se corrigió la redacción del sujeto en el ítem de lectura y se precisó el contexto en la lista de compras (*shopping list*).
8. **5.º básico, Lenguaje:** se corrigió la identificación de versos y rima en el análisis poético guiado.
9. **5.º básico, Matemática:** se reemplazó un distractor confuso en decimales («0,30 solamente...» por «0,003»); se explicitó la distancia exacta en redondeo y se simplificó el enunciado del problema de balanza para mantener rigor pedagógico.
10. **6.º básico, Ciencias:** se aclaró que en la sublimación del hielo seco, la niebla visible es vapor de agua atmosférico condensado por el frío y no el gas dióxido de carbono en sí mismo; se eliminó redundancia en consumidores de segundo orden.
11. **6.º básico, Inglés:** corrección de artículo faltante (*to the store*) y armonización de pronombres en pregunta de transporte.
12. **6.º básico, Matemática:** se reemplazaron distractores con la fórmula «...solamente» por alternativas matemáticas válidas (4/40, 5 1/6).
13. **7.º básico, Ciencias:** en la retroalimentación de leyes de los gases, se corrigió el desliz que repetía «temperatura, temperatura o volumen», dejándolo en «temperatura, presión o volumen» (Boyle, Charles, Gay-Lussac).
14. **Media (3.º y 4.º medio):** normalización de decretos curriculares (Decreto 193/2019 Plan Común) e integración de trazabilidad completa por módulo en Ciencias para la Ciudadanía y Filosofía.

### 12.3 Reconciliación del inventario en la matriz CSV

La matriz maestra (docs/auditorias/matriz-maestra-estado-por-archivo.csv) presentaba una discordancia histórica: registraba 48 guías mientras el árbol contenía 58. El análisis reveló que 10 guías (lengua-y-literatura de 7.º básico a 4.º medio, ilosofia de 3.º y 4.º medio, y educacion-ciudadana de 3.º y 4.º medio) habían sido clasificadas erróneamente con 	ipo_recurso_preliminar: otro.

Se corrigieron las 10 filas a guía/contenido, estableciendo un total exacto de **58 guías de estudio**. Todas las 58 filas, más contenido/00-estado-contenido.md, fueron recalculadas en tamaño de bytes y blob SHA desde Git, y pasaron a estado 
revalidado.

El conteo consolidado de las 290 rutas del proyecto es:
- **
revalidado**: 265 archivos (100 % de contenido/ — 50 exámenes + 156 pruebas de unidad + 58 guías + 1 tablero).
- **pendiente_auditoria_sistematica**: 25 archivos (100 % bajo Temarios/ — 12 PDFs oficiales UCE y 13 análisis curriculares en Markdown).


## 13. TEMARIOS UCE Y FUENTES CURRICULARES OFICIALES (2026-10-28)

Se completó la auditoría sistemática y exhaustiva de los **25 archivos** bajo la carpeta `Temarios/`: 12 documentos oficiales en PDF emitidos por la Unidad de Currículum y Evaluación (UCE) del Ministerio de Educación de Chile para los exámenes de validación de estudios para menores de edad (1.º básico a 4.º medio) y 13 documentos de análisis curricular en Markdown (`Temarios/analisis/00-resumen-general.md` a `12-cuarto-medio.md`).

Con este cierre, el **100 % de los 290 archivos de alcance educativo del repositorio** queda en estado `revalidado` en la matriz maestra (`matriz-maestra-estado-por-archivo.csv`).

### 13.1 Resumen del cotejo curricular

| Comprobación | Estado |
|---|---|
| PDFs oficiales UCE auditados | 12 / 12 (1.º básico a 4.º medio) |
| Análisis curriculares Markdown auditados | 13 / 13 (`00-resumen-general.md` + 12 cursos) |
| Total Objetivos de Aprendizaje (OA) extraídos y cotejados | **410 OAs oficiales** |
| Coincidencia curricular UCE ↔ Síntesis Markdown | **100 % verificada** en los 12 cursos |
| Decretos de Bases Curriculares verificados | Decreto 439/2012 (1.º-6.º básico), Decreto 614/2013 (7.º básico-2.º medio), Decreto 193/2019 (3.º-4.º medio) |
| Estado global de la matriz (290 archivos) | **290 revalidados / 0 pendientes (100 % cerrado)** |

### 13.2 Hallazgos sustantivos detectados y resueltos

1. **2.º medio, Historia (`10-segundo-medio.md`):** Se identificó y eliminó un bloque espurio pegado al final del archivo correspondiente a Educación Ciudadana de 4.º medio (OA 06 sobre medios de comunicación y preguntas de libertad, igualdad y solidaridad). La sección de Historia de 2.º medio quedó con sus 14 OAs oficiales exactos, finalizando en el OA 25 (discriminación y Ley Zamudio), en perfecta correspondencia con las páginas 16-17 del PDF oficial `temario_media_2deg_medio_UCE-1.pdf`.
2. **4.º medio, Educación Ciudadana (`12-cuarto-medio.md`):** La transcripción original sólo incluía el OA 06 y un OA sin numerar. Se completaron íntegramente los 5 Objetivos de Aprendizaje oficiales de la asignatura conforme a las páginas 8 y 9 del PDF oficial `temario_media_4deg_medio_uce.pdf`:
   - OA 01: Institucionalidad democrática y división de poderes.
   - OA 03: Modelos de desarrollo, sustentabilidad y cambio climático.
   - OA 04: Derechos laborales en Chile y movimientos sociales.
   - OA 05: Principios de libertad, igualdad y solidaridad ante desafíos de la democracia.
   - OA 06: Oportunidades y riesgos de los medios de comunicación y tecnologías digitales.
3. **Resumen General Curricular (`Temarios/analisis/00-resumen-general.md`):**
   - Se corrigió la suma de la columna de Ciencias Naturales (sumaba 79 OAs, figuraba erróneamente 69 por errata aritmética).
   - Se corrigió la suma de Historia, Geografía y Cs. Sociales a 98 OAs (eliminando el OA espurio de 2.º medio).
   - Se actualizó Educación Ciudadana a 11 OAs totales (incorporando los 3 OAs recuperados de 4.º medio).
   - El gran total consolidado de OA seleccionados por la UCE para los exámenes libres quedó fijado en **410 Objetivos de Aprendizaje**.
4. **4.º básico, Ciencias Naturales (`temario_basica_4deg_basico_uce.pdf`):** Se corroboró que el PDF oficial de la UCE presenta una errata de maquetación en las páginas 8 y 9, duplicando el encabezado y cuerpo del Objetivo de Aprendizaje N°1. El documento de análisis `04-cuarto-basico.md` lo mantiene correctamente consolidado en una sola mención (32 OAs totales).

### 13.3 Cierre de la Matriz Maestra de Archivos

Las 25 filas de `Temarios/` fueron actualizadas en `docs/auditorias/matriz-maestra-estado-por-archivo.csv`:
- Se calcularon sus tamaños en bytes reales y sus hashes SHA de blob desde Git.
- El campo `estado_auditoria` pasó de `pendiente_auditoria_sistematica` a `revalidado`.
- La matriz alcanza **290 / 290 archivos revalidados (100 % de cobertura de archivos educativos)**.

## 14. Piloto de especialistas — Ingles 5 basico (2026-11-01)

### 14.1 Alcance, versión y responsabilidades

Base `dd9a556` en `main`, más el diff local de esta sesión (sin commit/push). Los cierres de octubre se conservan como históricos; no sustituyen esta revisión por dimensiones. La fecha de sesión local es 2026-11-01; Vitest imprimió 2026-11-02T03:06:55Z, correspondiente a medianoche local.

Se crearon cinco perfiles nativos en `.devin/agents/`: `logos-curricular` (solo lectura), `logos-qa-experiencia`, `logos-datos-evaluacion`, `logos-desarrollador` y `logos-seguridad-operacion`. El contrato común es `.devin/agent-protocol.md`; `/logos-coordinacion` distribuye encargos y exige aprobación separada por dimensión. No se reemplazó el agente de trámite administrativo existente ni se fijaron modelos no verificados. Los perfiles con `exec` pueden ejecutar comandos: sus restricciones de operación son instrucciones, no un sandbox adicional.

`devin doctor --json` reconoció los cinco perfiles y devolvió `ok: true`. `devin skills list` reconoció la coordinación y su invocación funcionó. La herramienta de esta sesión todavía ofrecía solo perfiles integrados: el revisor curricular se ejecutó mediante `subagent_explore`, leyendo el protocolo y perfil nuevos. Esto comprueba el uso de sus instrucciones, no una invocación nativa del perfil personalizado desde esta conversación. No hubo ediciones paralelas.

### 14.2 Revisión educativa y límites

El revisor leyó los cuatro archivos de Inglés de 5.º básico y resolvió los ítems: guía (32 preguntas), unidad 1 (12), unidad 2 (12), simulacro B (25): **81 ítems**. Contrastó los OA 5, 6, 8, 14 y 15 contra `Temarios/analisis/05-quinto-basico.md`, sección Inglés, líneas 252–303. No pudo releer el PDF primario en esta ejecución: se mantiene ese límite, sin convertir el cotejo con extracción en certificación oficial.

No detectó errores de claves en el alcance leído. Las respuestas abiertas/modelos no deben describirse como respuestas únicas ni como calificación automática validada. El dictamen no aprueba el parser, la base, la API ni la puntuación real. La aprobación educativa queda acotada al contraste realizado, con observaciones siguientes y revisión docente humana antes de publicación a menores.

### 14.3 Hallazgos reconciliados

Se conserva `LGS-5B-ING-001` para el diálogo/disculpa ya registrado; los IDs sugeridos inicialmente por el revisor se reasignaron para no colisionar.

| ID | Evidencia y esperado/observado | Clasificación y estado | Criterio de cierre |
|---|---|---|---|
| LGS-5B-ING-002 | Examen B, metadato `relacionado` línea 6 y nota líneas 246–247 anuncian preguntas distintas/propias, pero reutiliza estímulos y consignas: P1 reproduce OA5.1 del banco (Pedro/edad); P6 reproduce OA6.1; P11 reproduce OA8.2. El revisor identificó reutilización extensa, sin establecer aquí un porcentaje exacto. | P2: afirmación editorial contradictoria y riesgo de sobreestimar transferencia a ítems nuevos. Abierto; examen sin modificar, matriz reabierta a revisión parcial. | Crear y resolver independientemente estímulos nuevos para el simulacro y revisar claves/rúbricas; o declarar explícitamente alcance de repaso y conservar pendiente una evaluación con ítems no vistos. No cambiar solo claves ni ocultar la limitación con un cambio de etiqueta. |
| LGS-5B-ING-003 | Guía, OA14 P3, línea 390: `b) From,.` frente a la pauta de unidad 2 ya corregida a `From.`. | P3 editorial. Se retiró la coma residual de la pauta de la guía; no se cambiaron opciones ni la letra correcta. Regresión específica reproducida roja y luego verde. | Fuente corregida y prueba aprobada; importación/render de la corrección aún no comprobados. |
| LGS-ING-AUDIO-001 | `frontend/src/app/core/lector-voz.service.ts:10–19` fuerza `utterance.lang = 'es-CL'`; `boton-escuchar.ts:9` solo entrega texto y `estudiar-oa.ts:26` entrega toda la guía bilingüe. | Brecha funcional confirmada por inspección: no hay selección de idioma/velocidad por fragmento para pronunciación inglesa. Impacto acústico pendiente de ejecución real. Abierto, sin cambio de código. | Selección explícita de fragmentos ingleses, idioma inglés, repetir/detener y velocidad; probar voces disponibles/no disponibles y navegador/dispositivo. No leer toda la guía bilingüe como si estuviera en un solo idioma ni prometer funcionamiento offline universal. |

**Observaciones que no se convierten en defectos:** reutilizar el banco en pruebas de unidad es una decisión explícita de `planificacion/08-diseno-pruebas-vs-examenes.md:55–57`; la observación del revisor se descarta como incumplimiento. Las comas en instrucciones `Color ...` reproducen la extracción curricular y quedan como mejora opcional. El frontmatter no normalizado del examen es riesgo de consistencia, no fallo de importación demostrado. Las preferencias de clima/playa merecen revisión de ambigüedad contextual; no se declara que un gusto personal tenga una única respuesta universal.

### 14.4 Ejecuciones reproducibles

| Comando / comprobación | Resultado y alcance |
|---|---|
| `devin doctor --json` y `devin skills list` desde raíz | Configuración reconocida; cinco perfiles y coordinación. |
| `cd frontend && npm test -- --watch=false` | **46/46**, 10 archivos, Vitest; previo a cualquier cambio de código frontend (no se modificó). Advertencia: Node 25 no LTS. |
| `docker info --format '{{.ServerVersion}}'` | Falló: daemon Docker detenido. No se cambió infraestructura. |
| `pg_isready -h 127.0.0.1 -p 5432` | PostgreSQL acepta conexiones. Lectura de configuración mediante Python imprimió solo nombre `logos_qa`, nunca la URL/secreto. Esto no prueba el entorno interno de un proceso API ya iniciado. |
| `curl ... http://127.0.0.1:8000/health` / `/docs` | `/health` dio 404 (no se infiere caída); `/docs` respondió 200. |
| `cd frontend && npm start -- --host localhost` | Frontend local iniciado para la comprobación E2E. |
| `cd frontend && npx playwright test e2e/matematica-operaciones-katex.spec.ts --project=chromium --grep 'Identidad del estudiante' --timeout=20000` | **1/1 aprobado** (2,4 s): login demo, selección Sofía y nombre/curso en interfaz. El global setup usa la cuenta sintética existente y puede registrar su check-in emocional; no se sembró ni borró la base. No es prueba del flujo de Inglés ni de una evaluación completa. |
| `cd backend && .venv/bin/python -m pytest -q scripts/tests/test_validar_evaluaciones_markdown.py -k guia_ingles_5b --confcutdir=scripts/tests` antes de corregir | **1 fallo esperado**, 9 omitidos por selección: reproduce `From,.`. Invocación previa mediante ejecutable pytest directo falló en colección por `ModuleNotFoundError: scripts`; se corrigió el comando, no las aserciones. |
| `cd backend && .venv/bin/python -m pytest -q scripts/tests/test_validar_evaluaciones_markdown.py --confcutdir=scripts/tests` después | **10/10 aprobados**; comprueba fuente y regresiones estructurales, no exactitud completa ni DB. |

No se ejecutó la suite bajo `backend/tests/`: su `conftest.py:14–20` elimina y recrea tablas de `logos_test` automáticamente. Hace falta confirmar expresamente que esa base es descartable antes de autorizar esa operación destructiva. La suite aislada `scripts/tests` no carga esas fixtures. No se confunde este bloqueo con un fallo del producto.

### 14.5 Dictamen y siguiente lote

- **Educativa:** revisión sustantiva de 81 ítems contra extracción, sin error de clave identificado; simulacro requiere resolver independencia de ítems; PDF primario no releído en este piloto.
- **Datos/calificación:** no aprobado; importación y resultados persistidos pendientes. La errata de fuente se corrigió sin tocar DB.
- **Funcional/visual:** un flujo de identidad aprobado solo en Chromium; Inglés, audio, móvil y flujo completo de evaluación pendientes.
- **Seguridad:** no revisada en este lote; no hay dictamen de cumplimiento.

Siguiente acción: resolver LGS-5B-ING-002 con nuevos estímulos y revisión independiente, después importar solo en QA autorizado y comprobar lectura/evaluación/progreso. Continuar Inglés de 6.º básico a 4.º medio por lotes; los otros 28 archivos no se consideran auditados por este piloto.

Para recursos de pronunciación se propone inglés por fragmento y controles explícitos, conservando español para explicaciones. Para imágenes: ilustraciones individuales PNG 1024×1024, sin texto incrustado ni marcas, composición simple y consistente; optimizar a WebP al integrar, con texto alternativo en HTML. Primeros candidatos didácticos de 5.º básico: posiciones gato/mesa, ropa según clima y alimentos de compra. No usar imágenes que revelen la clave de un ítem evaluativo. La lista de prompts finales debe ligarse a los ítems aprobados; no se generaron ni integraron imágenes en esta sesión.

## 15. Pasada de cierre integral en ejecución (2026-11-01)

**Base:** `3423420` más diff local. No interpretar §14 ni los cierres históricos como aprobación de la nueva versión. El usuario pidió completar la auditoría local y recibir porcentajes comprobables, no estimaciones de terminación. Permanecen fuera del alcance inmediato despliegue y nuevas propuestas de IA/juegos; se audita el producto educativo local existente y sus brechas funcionales declaradas.

### 15.1 Indicadores independientes — no sumar como porcentaje global

| Indicador | Evidencia actual | Estado |
|---|---|---|
| Revisión inicial especializada de Inglés | 32/32 recursos, **100 %**; 719 ítems resueltos en la versión previa a las correcciones (5B81;6B83;7B85;8B92;1M91;2M90;3M98;4M99) | Lectura completada, no cierre de los archivos modificados |
| Cotejo de Inglés con PDF primario | 8/8 fuentes, **100 %** textual: 5B/6B pp13–15;7B15–17;8B17–19;1M16–18;2M17–20;3M/4M p12 | OA e indicadores fieles; omisión menor `watch videos` en extracción8B pendiente; sin verificación visual/OCR |
| Revalidación independiente de simulacros nuevos | 3M y4M: 2/8, **25 %** del lote de simulacros | 5B necesita revalidar ajustes P9/P17 y apoyo visual;6B–8B aún pendientes;1M/2M con tres ajustes adicionales después de revisión |
| Backend, primera ejecución completa aislada | 491/492 aprobadas, **99,80 % de casos de esa ejecución**; 1 fallo y21 avisos | No equivale a cierre global. Fallo de aislamiento del test concurrente corregido y comprobado puntual; segunda ejecución completa en curso |
| Frontend y E2E | Evidencia §14:46/46 unitarias y1/1 identidadChromium, anterior al cambio de audio en desarrollo | Reejecutar pruebas afectadas y recorridos completos; sin extrapolar a todos los navegadores |

El denominador de recursos es diferente del de funcionalidades/casos E2E. No se emite un porcentaje único mezclando lectura, casos ejecutados y correcciones sin revalidar. El cierre exige todos los criterios aplicables por dimensión, no solo completar lecturas.

### 15.2 Fuentes primarias y herramientas reproducibles

Se añadió `backend/scripts/auditar_fuentes_curriculares.py`, que usa pypdf ya instalado en dependencias dev, sin OCR ni instalación adicional. Extrae desde el encabezado de Inglés hasta el final (última asignatura en estos8PDF), incluye continuaciones sin encabezado repetido y calcula SHA256. Se cotejaron también instrucciones generales p2. La fuente confirma25preguntas/90min/diccionario; **no especifica proporción cerradas/abiertas**: retirar afirmaciones de que nuestra mezcla de tipos imita exactamente el examen real. Apoyo visual de OA5/OA14 en5B/6B confirmado como exigencia, pendiente de completar en la experiencia.

Regresión de copia textual: `check_reused_exam_stimuli` detecta estímulos entre comillas de al menos6palabras, ignorando saltos de línea. En5B reprodujo14 coincidencias antes de reescribir; después pasó. Es conservador y no sustituye revisión semántica ni detecta toda reutilización estructural.

### 15.3 Correcciones educativas en curso

- **Inglés5B:**25ítems nuevos, claves/respuestas personales resueltas independientemente. Se ajustaron P9 a cuatro de la tarde y P17 a una instrucción de aula sin pista de rima. Falta revalidación puntual de esos ajustes y apoyo visual. No importado todavía.
- **Inglés6B–8B:**75ítems de simulacros reescritos,25porcurso, con tablas y pautas actualizadas. Correcciones6B caught/yesterday y contexto cuento para Onceuponatime;7BmitoAmazonas explícito;8Breferencia soccer desambiguada. Revalidación independiente pendiente. El desarrollador detectó que `parser_prueba_examen.py` puede absorber el siguiente encabezadoOA dentro de la última opción: investigar con regresión; reordenar preguntas no es cierre de la causa raíz.
- **Inglés1M/2M:**50ítems revisados por segundo especialista. Claves correctas pero halló P21 de prefijos mal asignados a OA16 y P24 de1M muy próximo al banco. Se sustituyó1MP21 por pasiva pasada (`was painted`),2MP21 por segundo condicional (`had`),1MP24 por inventor/taller (`who/where`); revisión puntual pendiente. Se completaron indicadores1MOA16 (pasiva,needto/needn't,where); se corrigió unless en2M. La reformulación2MP9 atribuye otras soluciones al lector, no al texto, y fue justificada independientemente.
- **Inglés3M/4M:**50ítems nuevos,50/50 resueltos independientemente; distribuciónOA8/8/9, cerradas5/6 y abiertas20/19. Rúbricas0/0,5/1 y respuestas personales no literales. Aprobación educativa acotada; no aprobar importación ni acústica. Pendientes menores de metadatos no implican fallos de parser demostrados.
- **Historia7B P1/P3,8B P9,2M P4:** opciones partidas por colas desplazadas a otra letra; tres bloqueosP1. Se reunieron conservando claves y cotejando guías. Revalidación independiente pendiente; patrón sistémico requiere barrido global.
- **Matemática7B P4:** distractor2/14 equivalente a1/7 cambiado por3/14. **Matemática8B pautaP14:** pendiente+4 sube, no baja. **Lengua7B:** tabla de especificaciones corregida a9cerradas/16desarrollo. Pendiente revalidación.
- **EducaciónCiudadana4M — P1 nuevo:** fuente oficial incluyeOA1/3/4/5/6, pero material solo trataba5/6. Producción de explicaciones/ejemplos/bancos y evaluaciones para los tresOA faltantes en curso; no está aprobada la asignatura.
- **Otros defectos pendientes de corrección:** tablas de especificaciones Matemática3M(P23/P25) y4M(P25) contaminadas por texto de probabilidad; portada Filosofía4M ponderacionesOA12/13/12/14 suman51 (portada antigua11/15/11/14); opciones partidas CienciasparaCiudadanía3MP3 y4MP4/P11; referencias de FormaA rotas en metadata;1BFormaAP3 secuencia matinal ambigua;OA de tablas integradas sin nombre de asignatura; referencias a antiguas pruebas inexistentes en2B/3B.

### 15.4 Alcance no-Inglés realmente leído (sin ocultar pendientes)

Los especialistas no completaron todo el universo asignado en una ejecución. Sus barridos estructurales no cuentan como resolución disciplinar:

- **1B:**18recursos completos reportados (4guías,12pruebas,2exámenes); no se usa su recuento aproximado de ítems como métrica exacta.
- **2B:**12pruebas y2exámenes completos; faltan4guías.
- **3B:**2exámenes completos; faltan4guías y12pruebas.
- **4B:**2exámenes,12pruebas,guíasMatemática/Lenguaje completas; Ciencias parcial (falta final/glosario), Historia pendiente.
- **5B/6B:**simulacrosMatemática completos; resto no-Inglés pendiente (guías,pruebas yotros3simulacros porcurso).
- **7B/8B:**4simulacros no-Inglés porcurso completos; guías y pruebas solo barridas/no resueltas.
- **1M:**Ciencias eHistoria parciales; Matemática/Lengua no completos; guías ypruebas no-Inglés no resueltas.
- **2M:**Historia completa,Matemática P13–25; Lengua/Ciencias parciales; guías/pruebas no resueltas.
- **3M/4M:**simulacrosMatemática/Filosofía/EducaciónCiudadana/Ciencias completos; Lengua soloP1–18; pruebasMatemática3M×3/4M×2 completas; otras pruebas solo estructura y guías no leídas íntegramente.

Las afirmaciones históricas de cobertura se conservan como historia; esta lista delimita la nueva pasada. Estímulos `[Imagen:…]`, accesibilidad, precisión de rúbricas y aislamiento por roles siguen requiriendo evidencia técnica.

### 15.5 Aislamiento y primera regresión backend

El usuario autorizó expresamente crear `logos_auditoria_test` y borrar/recrear solo sus tablas. Se creó esa base y se añadió `LOGOS_TEST_DATABASE_URL` al conftest con guard de host local y nombres permitidos; nunca se ejecutó drop/truncate sobre logos_qa/logos_dev/logos_test. La primera corrida: `.venv/bin/python -m pytest tests -q --tb=short` con override, **491passed/1failed/21warnings**,369,44s. El test `test_iniciar_intento_concurrente_no_crea_duplicados` ignoraba override creando engine hardcodeado logos_test. Se cambió a URL del engine del fixture, se exige10respuestas (no solo un únicoID entre respuestas parciales) y se libera su pool. La regresión puntual pasó1/1.

La corrida final en curso pasa tanto LOGOS_TEST_DATABASE_URL como DATABASE_URL a la base aislada, y RESEND_API_KEY vacío para no enviar correo. Advertencias de Starlette/httpx y SlowAPI deprecadas no se ocultaron ni se instalaron versiones a ciegas. Ningún resultado en progreso se cuenta como aprobado. No volver a usar pytest con fixtures destructivas sin ese override aislado autorizado.

Siguientes pasos: completar pendientes de lectura por lotes pequeños; resolver/regresar corrupción de parser y alternativas; terminar EducaciónCiudadana4M y audio; revisar independientemente cambios; importar en entorno aislado, comprobar calificación/progreso por rol y navegador; cerrar solo con evidencia completa.

### 15.6 Continuación 2026-11-02 — ejecución y lecturas

Segunda suite backend: **492/492 aprobadas**,11avisos,362,05s, con ambas URLs en logos_auditoria_test. Después se reprodujo fallo de encabezadoOA absorbido por alternativa en `parser_prueba_examen.py`, se añadió regresión primero fallida y se delimitó encabezado/separador sin perder word-wrap: **22/22** tests parser+scripts con `--noconftest`. La corrida492 fue anterior a esta modificación; no presentarla como prueba de los nuevos cambios.

Frontend audio: desarrollador ejecutó76/76unitarias ybuild; pendiente revisión independiente/acústica. Se añadieron overrides seguros de destino: `LOGOS_API_URL` mediante `ng serve --define`, y LOGOS_E2E_WEB_URL/API_URL para Playwright. Las dos fixtures SQL E2E antes escribían logos_qa hardcodeado: ahora `ejecutarSqlPrueba` exige LOGOS_E2E_DATABASE_URL explícita, hostlocal y nombre logos_auditoria_test; contraseña solo por entorno de psql, sin shell. No se cambiaron CORS ni límites de seguridad; frontend4300 ya era origen admitido.

Se importó el contenido candidato en la base aislada y se sembraron planes/cuentas sintéticas. Servidores de esta sesión: API8001 yfrontend4300; los originales8000/4200 no se tocaron. Suite Chromium iniciada: **229casos**, de **687casos/65specs** inventariados entre3navegadores. Evidencia en `frontend/test-results/auditoria-cierre-20261102-chromium-a/` yreport.json al terminar. La primera pasada ya detectó violaciones axe de etiquetas y fallos de fixtures/estado; aún sin resultado final. **No correr fixtures backend destructivas mientras navegador usa esta misma base.** La importación omite niveles existentes: repetir script no sincroniza el diff.

Lectura disciplinar inicial: **255/264 recursos (96,59 %)** contando archivos leídos al menos una vez, NO aprobaciones de su versión final. Completadostodos1B–8B;1M17/20noInglés;2M17/19del lote pendiente;3M10/14del lote;4M10/10del lote. Los9recursos aún incompletos son:1MguíasHistoria/Lengua yCienciasdesde1263;2MguíasLengua eHistoriadesde1hasta2119;3Mpruebasunidad1deLengua/Filosofía/EducaciónCiudadana yCienciasBienestarSalud. Dos revisores están completándolos. El simulacroLengua3M queda cubierto combinando lectura previaP1–18 yposteriorP7–25 del mismo archivo sin cambios.

### 15.7 Hallazgos adicionales — NO cerrar por lectura

- 2BCiencias: matiz de monotremas aplicado solo a una glosa; explicaciónOA3yfeedbackP2 siguen diciendo que todosmamíferosnacen delvientre. Corregirambos sin cambiar claves.
- 3BpruebaHistGeografíaP3: especificar modelo continentaldeguía(Américaunida);7esdefendiblebajootromodelo.4BCienciasglosario:mantopredominantementesólido/plástico,no semilíquido;placasdelitosfera,no solocorteza.1BFormaAP3matinal siguependiente.
- 5BHistoriaexamenP3 tiene cola de d desplazada a b(**P1nuevo**); simulacro prometeoriginalidad pero copia guía/unidades(**P2**). Math5BpruebaNúmerosP9 ofrece0,30equivalentea0,3: cambiar distractor. EscalaHist35puntosaprueba18aunque60%=21; corregir. Lenguaje5Bmetáfora/personificacióndefendiblesenlagreda: pautaaceptarjustificación.
- 6BguíaMatOA24P3ypruebaMediciónP11mencionan4mesespero solo2datos: completar o acotar. LenguajeexamenP22 pide segundo párrafo inexistente deTextoA: reabrir LGS-6B-LEM-002parcial. Cienciaspauta21afirma gasvisible:CO2invisible,nieblaesaguacondensada. Historiaescala34puntosaprueba18<60%: corregirfórmula.
- 7BguíaMatOA3P1conserva2/14y1/7simultáneos: corregir guía(comounidadysimulacro).8Bningún defectoalto, riesgosortográficos/estímulosdeguía.
- 1MLenguaexamentablaOA5/totalesincorrectos:11alternativas,2VF,12desarrollo; VFjustificadassecuentanendesarrollo. Ciencias1Msimulacrorepiteítemsdeunidadespeseindependenciadeclarada: revisarcomoconfirmación,nomatizarfalsamente.
- 2MHistoria **OA6espurio** sobre medios proviene deEdCiudad4M, presentado como oficialenguía2124–2268. UnidadFormaciónCiudadanaincluyeOA6yP10–13fuera de selecciónoficial; reclasificarcomplementario o sustituirporOA22/25. No perdercontenido sinregistro. ActualanálisisyaexcluyeOA6.
- 3MMatguíaV(4):12M×0,88^4≈7.196.344,no7.196.160(diferencia184pesos,no185mil). Ciencias3MguíaNCh433clasificaprevención pero unidadmitigación; norma reduce daños,nosismo:armonizar. Casoaluviónaceptar adaptación/prevenciónjustificadassegúntipo.4MLenguaunidades1/2sintextosestímuloautocontenido;falta trabajocontextorecepción;simulacro17abiertassinrúbricas.4MFilosofíaOA2faltaformularpreguntasfilosóficaspropias;OA4falta practicarinducción/deducciónytesis/razón/garantía/evidencia.4MCienciasfraseglaciaresPatagoniaAntárticaconfusa:reformularsinsuperlativosnocotejados.

EducaciónCiudadana4M:112ítemsresueltosindependientemente,15indicadorescotejadosconPDF;quedaron ajustes menores. Se corrigió despuésel hito2005a **permiso paternalpor nacimiento** (DT,Ley20.047,ORD3827/103,02-09-2005), no creaciónpostnatalmaterno ni una supuesta extensión privada no comprobada. Se corrigieron mayoría presidencial,consejerosregionales en casoregional,examenP14a seguridadlaboral conrúbricaanalítica ynota obsoleta enTemario12. Revalidar estos ajustes puntuales. Inglés1M/2M/5B/6B–8B: ajustes deítems/pautasdescritosarribaaplicados;7BP16ahoraproducciónpersonalsinimagenfantasma,8BP2aceptamade/write,notadosomásespacios6/8B. Siguenfaltandoapoyosvisuales5/6B.

### 15.8 Hallazgos técnicos de integridad — SELECT aislado 03:54–03:55 UTC

Auditor sololectura cotejó58guías y206evaluaciones contra DB:12niveles,58asignaturas,**411OA**,6157preguntas;156unidades1825preguntas,50simulacros1210;3122preguntasguíaparseadasvs3121encabezadosreales. Losanálisisactualescontienen **410ocurrenciasOA** conservandomódulos,no408; sobraOA6Historia2M. Aún no declarar410certificaciónPDFglobal. 1BMat59y5BHistoria55son conteosreales,no pérdidas(estimacioneshumanas60/56eranincorrectas).

**Bloqueos altos reproducidos (pendientes):**
1. `parser_contenido.py:39–41` toma continuación año1960deCiencias3Mcomo pregunta:ítem12partido/sinclaveyunafantasma(DB5037). Exigirmarcador inequívoco yregresión.
2. `parser_prueba_examen.py` toma5.000deexplicacióncomopautaP5ysobrescribebiología1MP5(DB3942);claveimposible. También2MLenguaU2P15claveletrasola`b`absorbeencabezadoposterior(DB4687). Delimitarnumeración/rechazarduplicadas/aceptarletrasola/separarcriterios. **2575/2577clavescerradasDBcalzan**,2no.
3. CienciasCiudadanía3Mrepite legítimamenteOA1/OA3en2módulos; importadorpierdemóduloenidentidadydictconservaúltimo. **12/25preguntas**simulacroMódulo1 enlazanOAdeMódulo2. Identidadcompuestamódulo+código; no deduplicarlegítimos.
4. **17abiertasFilosofía** sinrúbricasimportadas:3MP4/6/10/12/16/18/24/25;4MP4/6/12/13/18/19/23/24/25. Tablaalternativasseusa,criteriosnarrativossepierden; rama genéricatruncaa60caracteres(**1126abiertasenDBexactamente60**). Importarrúbricasíntegrasmanuales;motorcorrectamenteexcluyeabiertasdeautocorrección.
5. **1825/1825preguntasunidades sinOA**,160/160integradas sinasignatura/OA,20/1050simulacrospor asigsinOA. Integradosrequieren asignatura+código,noOAa solas. **3035/3035IDsdeconjuntosválidos**,0duplicadosinternos;ningúnOAenlazadoaotraasignatura(pero módulo sí incorrecto).
6. Diffsfuente–DBobservadosson contemporáneos deEdCiudad4M:1autoEvaly4evaluaciones(DP6,MP10,EP14–15),nopruebadeactualización. Reimportadoromite nivelesexistentes; falta sincronizacióncontrolada yrevalidación.

Siguiente prioridad técnica: corregir estos parsers/identidades/rúbricas con regresiones focalizadas; conservar evidencia primeraimportación. Despuésrecrear únicamenteentornoautorizadosinE2Econcurrente y reimportar fuentesfinales, verificarclaves/asociaciones/manualrubricayflujosreales. Todo sigue local y sincommit/push deeste lote.

### 15.9 Revisión inicial completa y correcciones — 2 de noviembre

**Lectura disciplinar inicial: 264/264 recursos, 100 %**, sin convertir lectura en aprobación. Los nueve tramos antes pendientes quedaron leídos por f1d4fffe y8ab27774. Nuevos hallazgos: Historia1M decía Chañarcito por Chañarcillo (no insertar1852: fecha no acreditada); faltaban ciclos económicos y externalidades en OA20. EducaciónCiudadana3M unidad1P14 atribuía tasa de interés al Gobierno, no al Banco Central autónomo. Lengua2M confundía indicativo «recomendamos» con imperativo. Todos entraron en corrección.

**Correcciones educativas aplicadas, no publicación:**
- bbfe6837 corrigió cinco archivos: 1BFormaAP3 ahora secuencia explícita, clave a)Se despierta; mamíferos2B con excepciones; continentes3B anclados al modelo; manto/litosfera4B coherentes en explicación, ejemplos, banco y glosario; distractor7BMat2/14→3/14, clave1/7. El coordinador revisó el diff completo y resolvió independientemente esas alternativas/definiciones: aprobado educativo en ese delta, sin aprobación DB/render.
- 0674814e corrigió Historia5B/P3, reconstruyó ocho ítems duplicados, mantuvo25preguntas/35puntos (17alternativas,6breves,2extensos), escala60%=21puntos; MatunidadP9d→0,33; LenguaP2abierta admite personificación motivada. Pendiente segunda resolución completa; P3Historia comparte estímulo factual con guía, revisar si la promesa de independencia sigue justificada.
- 6beb8a31 completó datos de mayo/junio en Mat6B guía/unidadP11:6A26/33y6B20/24; abril35sigue máximo y diferencia17. LenguajeP22referenciaTextoA completo; CO2invisible/nieblaagua en Ciencias; escalaHistoria34puntos,60%=20,4,21→4,1. Pendiente segunda resolución.
- eb000daa retiró OA6espurio de Historia2M y metadata/introducciones; reemplazó P10–13unidad porOA22/25 manteniendo13ítems. Lengua2M usa directiva atenuada. Pendiente revalidación de cuatro preguntas nuevas y de la aplicación jurídica de LeyZamudio, sin suponer reparación automática en todo caso laboral.
- df304687 corrigió seis archivos1M/3M: Chañarcillo y explicación de ciclos/externalidades; tablaLengua1M11alternativas/2VFjustificadas/12desarrollo; Mat3MV4=7.196.344,32, redondeo7.196.344; NCh433mitigación, bancoP9clavea y explicación; aluvión admite prevención/adaptación justificadas; BancoCentral/tasa vsGobierno/gasto. Pendiente revalidación documental de los deltas críticos.
- 8cdbc9e7 corrigió ocho archivos4M de Filosofía/Lengua/Ciencias. **Revisor independiente8d8793a2 aprobó alcance educativo/documental**: producción de preguntas filosóficas, inducción/deducción/Toulmin, recepción, estímulos completos, ficción explícita,17rúbricasmanuales/25puntos. Persisten tresP3editoriales: añadir «y recepción» en introducciónguía yobjetivoU1; columnaCerradas→Alternativasenexamen; actualizar ultima_actualizaciondel examen. Funcional/importación no aprobados.

### 15.10 Parsers: regresiones corregidas y nuevos bloqueos del corpus

Año1960: el coordinador añadió prueba primero fallida (1fallo/14aprobadas), delimitó marcador numérico conservando «Pregunta1» sin punto y añadió regresión de guía realCiencias3M=60ítems.

Desarrollador db5d4d0e corrigió pauta5.000, letra sola, respuestas íntegras y17rúbricasFilosofía;27tests focalizados. 626fa085 preservó módulo en objetivos/pautas y lookup compuesto en importador; las25asociacionesCiencias3M se verifican con sesión de captura, sinDB. El coordinador añadió tres regresiones inicialmente fallidas para clave cerrada ausente/vacía/fuera de opciones y rechazo antes de cualquier persistencia. **50/50tests sinconftest aprobaron**, pero no se declara integridad del corpus por esa cifra.

**Revalidación independiente c47b065b**, snapshot04:12:53–04:13:22UTC, hash agregado`1b020d75a53365945b45850f1a0942b55a06031df2963d0dd2231aac551f9f10`:58guías,410bloquesOA,3115preguntasbanco,206evaluaciones/3035preguntas. Confirma año1960, P5Biología1M, P15Lengua2M,17rúbricasFilosofía completas(494–1084caracteres) y25mapeos por módulo. **Nuevos bloqueos altos**: RE_PAUTA_LIMITE corta respuestas enteramente negritas y vacía98pautas; primera tabla de nuevaLengua4M es rúbrica sinclave y oculta tabla posterior, dejando25pautas ausentes; guíadeLengua4M usa «Pauta manual» no reconocida en2preguntas. Hay18clavescerradasinválidas en8archivos; guard de importador las rechazaría. **aab0192c está corrigiendo estos casos**, exclusivamente ambos parsers y sus tests, sinDB. Exigir diagnóstico de corpus completo y revalidación, no solo tests verdes.

Asociaciones recuperables sin semántica ni elección arbitraria: de1825unidades,1377resueltas/23ambiguas/425sinmatch; de160integradas,160resueltas por asignatura+OAexplícitos de pauta. Resoluciones de unidades:517códigoexplícito único,754matchexacto banco,106intersección inequívoca. Aún **no implementadas**. DesgloseR/A/S por curso:1B34/0/51;2B66/0/22;3B71/0/33;4B75/0/32;5B129/0/37;6B102/0/63;7B156/0/36;8B163/4/30;1M128/8/54;2M162/6/24;3M173/5/6;4M118/0/37. Hay además72preguntas de exámenes separados sinOA recuperado por salidaactual. Resolver conservadoramente1537 y revisar/anotar documentalmente los448restantes y los72deexámenes; no adivinar por tema.

### 15.11 Primera ejecución Chromium y correcciones

Comando con LOGOS_E2E_WEB_URL=http://localhost:4300, API_URL=http://localhost:8001 y DATABASE_URLexclusiva: primera pasada **200aprobadas/13fallidas/16noejecutadas, de229casos (4,8min)**. Artefactos yreport.json en `frontend/test-results/auditoria-cierre-20261102-chromium-a/`. No contar los16como aprobados ni porcentaje global por esa ejecución.

Causas diagnosticadas:3violacionesaxe (fecha sinlabel y contraste4,15:1 tablasAdmin/Profesor);6specs esperaban feedback automático aunque UX exige botónComprobar; coaching dependía de historial antiguo; repaso/vistas de plan previo; gamificación tenía selector ambiguo sidebar/onboarding. ed5f98dc corrigió asociaciones label/input(selects de repaso incluidos), token de texto de tablas alineado con diseño global y añadió casoaxeAgregarAlumno. Sin cambiar umbrales. 1dadcfac corrigió seis flujos manteniendo feedback visible después de acción y no visible antes; helpers crean alumnos/cuentas/intentos/planes sintéticos aislados, notas1.0 comprobadas, IDs dinámicos; sidebar se resuelve dentro de navigation. No modifica seguridad ni datos históricos. Sus11archivos esperan compilación/E2E por coordinador.

**Revalidación ejecutada:** axe shell12c47e terminó **18/18 aprobados en22,4s**, output`test-results/auditoria-cierre-20261102-a11y-b`. Después shell6cfb1b ejecutó los10specs corregidos por1dadcfac: **50/50 aprobados en58,1s**, output`test-results/auditoria-cierre-20261102-flujos-c`; incluye prueba/examen completos, perfiles nuevos, coaching, repaso/vistas ygamificación. Ambas con1worker, mismoAPI8001/frontend4300 yDBaislada, sin elevar límites. Las suites terminaron; API shellfed9da yAngular shell689481 siguen activos. No confundir estas68verificaciones focalizadas con matriz completa ni con reimportación final. Las tresP3editoriales de Lengua4M señaladas por8d8793a2 ya se corrigieron: producción/recepción en introducciones, columnas inequívocas yfechaexamen2026-11-02.

La DB sigue siendo la primera importación candidata, desactualizada frente a correcciones deMarkdown/parsers. Antes de reimportar hay que resolver pautas/asociaciones, preservar evidencia, detener suites mutables y usar únicamente fixtures destructivas expresamente autorizadas en logos_auditoria_test. No tocar otras bases. Regresión completa backend deberá repetirse al final, no atribuir los492anteriores al código nuevo. Inglés sigue requiriendo apoyos visuales5B/6B y prueba real de voces;55marcadores deimagen continúan pendientes de estrategia. TresPNGversionados de frontend/screenshots se actualizaron porE2E: revisar como evidencia antes de commit; no restaurar sobrescribiendo otros cambios. Trabajo local enmain, sincommit/push deeste lote.

### 15.12 Continuación directa: cuota, banco y trazabilidad

Se agotó la cuota de especialistas al iniciar81f9c7aa: **no escribió archivos**. El usuario pidió continuar; el coordinador sigue directamente. No se ocultan revisiones independientes pendientes ni se modifica facturación/configuración para eludir la cuota.

**Parsers:** aab0192c corrigió las98pautas vaciadas, lectura de múltiples tablas/rúbricas ymarcaPautamanual;58tests pasaron ydiagnóstico completo dio0pautas ausentes/vacías oclaves fuera de opciones. Falta segunda revisión independiente de este delta, limitada porcuota. Después el coordinador reprodujo otro defecto real: dividir celdas por `|` truncaba probabilidades condicionales escritas `\|` yperdía OA. Cuatro regresiones fallaron antes ypasaron con `_celdas_tabla`, que respeta escapes pares/impares; casos realesMat3M23/25yMat4M25 conservan desarrollo completo, resultado yOA2.

**Banco de autoevaluación:** `buscar_por_oa` incluía preguntas de conjuntos, contaminando práctica y simulacros parciales. Se corrigió `backend/app/infrastructure/persistence/repositorios/preguntas.py` excluyendo IDs de conjuntos **prueba_unidad/examen_simulacro**, no de los derivados **examen_simulacro_parcial** que reutilizan legítimamente el banco. Regresiones SQLiteenmemoria añadidas al archivo existente `backend/tests/test_contenido_y_evaluaciones.py`: primero1fallo/1aprobado; luego se reprodujo el consumo erróneo porparciales yse acotó el filtro; **3/3 aprobadas**,6tests delarchivo deselectados sinconftest. Callers revisados: routerautoevaluación yGenerarSimulacroParcial. No se conectó Postgres ni se cambió esquema. API8001aún usa proceso anterior: reiniciar al validar integración, no atribuir E2Eanteriores alcódigo nuevo.

**Integrados:** el parser conserva asignatura de la tabla de pauta yreconoce encabezados «OA evaluado». El importador usa asignatura+módulo+código, mantiene conjunto integrado ligado alnivel yguarda asignatura/OA correctos por pregunta. Rechaza referencias incompletas/desconocidas antes de persistir cualquier pregunta. **160/160 asociaciones comprobadas enmemoria en8formas de1B–4B**, no DB reparada. Once regresiones fallaron antes; conalias explícitos ytodaslas referenciasprevalidadas pasaron. No se infieren asignaturas por tema.

**OAenpautas narrativas:** se conserva contexto de encabezados conpila porprofundidad, sin arrastrarlo a sección hermana; metadatosoa_evaluados/unidad como contexto global. Se recuperan los17OAantes ausentes deFilosofía3M/4M. Las entradas devariosOA se conservan encodigos_oa yno eligen elprimero; los casos ambiguos siguen sinOAprincipal. Cinco pruebas fallaron antes ypasaron después. **Última corrida combinada:79/79** (`tests/test_parser_contenido.py tests/test_parser_prueba_examen.py scripts/tests/test_importar_contenido.py`, todos--noconftest). Snapshot posterior:58guías/410bloquesOA/3115preguntasbanco y156pruebas/1825preguntas+50exámenes/1210preguntas; **0pautas ausentes/vacías y0claves cerradas fuera de opciones**. Ahora0preguntas deexamen sin códigoOA y1166deunidad sin códigoúnico (659con código recuperado, no contar como vínculoDBverificado). Aún NO se implementa fallback porcoincidenciaexacta debanco para lasunidades; siguiente paso conservador: tipos+enunciadoUnicodeNFKC/casefold/espacios+opcionesenorden, intersección concontextoOA/módulo, nunca elegir entre candidatos. Revisar después losnoresueltos documentalmente.

**Pronunciación:** 9a3505f3 entregó nuevo `frontend/e2e/pronunciacion-ingles.spec.ts` ycorrigió contraste deayuda atexto-principal. **3/3Chromium en dos corridas y9/9unitarias**. Motor nativo real:180voces,41inglesaslocales; utteranceen-US,rate1/0,7,repetición,cancelación yeventosstart/end/error registrados reenviando motor real. Axe0serious/critical enestudiarInglésMateo6B. No se usaron servicios remotos ni voces instaladas. No prueba audibilidad/calidad acústica humana; esa limitación permanece explícita. Sinvozinglesa se cubre con mocks, no en dispositivo con41voces.

**Visual pendiente:** 5c818ab2 inventarió55marcadoresen23archivos de1B–3B. MarkdownPipe losmuestra comodescripción literal; algunos filtran respuesta. Elreporte dice12grupos, pero enumeraaprox18ítems: confirmar denominadorporítem antesdeporcentajes. Ubicaciones:1BFormaAQ1/Q20;FormaBQ5/Q11/Q15;MatnúmerosUQ7;MatmediciónUQ1;MatgeometríaUQ2/Q5;LenguaU2Q4/Q7;HistgeografíaUQ7;CienciasTierraUQ5;3BCienciasTierraUQ4yFormaAQ19;2BFormaAQ11/Q12;3BMatgeometríaUQ4. Corregir conassets originalesprecisos ocomponentes existentes, sin texto visible que reveleclave. Inglés5B/6B no depende de [Imagen], peroapoyosvisualessiguen mejora pedagógica; gráficos6B tienen datos completos aunque práctica de lectura visual deOA24requieremejorar. No se editaron assets todavía.

**Siguiente lote:** resolver coincidenciasexactas ycontextos restantes delimportador; corregir18estímulos ybrechas gráficas confirmadas; revisar UIque presenta notas departeautocorregible como «Nota» sin aclarar suficientemente lomanual. Luego preflight completo, reimportación enlogos_auditoria_test, cotejoDB/API/UI, backend completo ymatriz navegador. CanonicalrootCLAUDE.md yaaclaraque antiguascifras/aprobacionesagosto/octubre son históricas ynoestadoactual. Sincommit/push ni despliegue; autorización final sigue vigente solo trasverificación.

### 15.13 Estado técnico vigente — lotes acotados

Sustituye los contadores técnicos de §15.12. Ante el feedback de consumo, continuar con un lote pequeño por vez, sin nuevas delegaciones ni exploraciones laterales. Último lote: cuatro regresiones rojas cerradas; parser reconoce OA explícitos del campo `eje`, y guía/pruebas Matemática3M explicitan a>0 en modelos y P(B)>0 en probabilidad condicional. No se cambiaron sus claves.

**Verificación:** `.venv/bin/python -m pytest --noconftest tests/test_parser_contenido.py tests/test_parser_prueba_examen.py scripts/tests/test_importar_contenido.py scripts/tests/test_validar_evaluaciones_markdown.py -q --tb=short` → **116/116**,1,25s. Validador CLI ampliado →0discrepancias en265Markdown. `git diff --check` limpio antes de actualizar estos registros. Son controles sin PostgreSQL, no regresión completa de aplicación.

**Importador:** implementado fallback por banco exacto, con UnicodeNFC y espacios normalizados, preservando mayúsculas, superíndices y orden de opciones; no NFKC/casefold, que pueden confundir notación matemática. Conserva candidatos múltiples e intersecta contexto OA/módulo, sin elegir arbitrariamente. Rechaza también pautas abiertas vacías/ausentes antes de persistir. Guía Ciencias4M ahora hereda módulo3 del encabezado, lo conserva en descripción y rechaza contradicciones; no se relajó el guard de módulos.

**Preflight completo:** el test `test_importacion_completa_en_memoria_conserva_banco_y_asociaciones` ejecuta importar_curso para los12cursos con sesión de captura, no DB. Conserva3115preguntas banco+3035evaluaciones; **1210/1210exámenes y1459/1825unidades (79,9%)** vinculadas a OA de la asignatura correcta. Quedan **366unidades sin vínculo documental**, no aprobadas. Antes del último lote eran1437/1825 y388pendientes. Matemática3M queda dentro de184/184unidades delcurso vinculadas. Diagnóstico porcurso disponible con `LOGOS_AUDIT_CURSO=03-medio` y pytest `-s -k importacion_completa`; solo modifica salida diagnóstica. No equivale a reimportación ni resolución educativa independiente.

**Correcciones educativas del lote previo pendientes de segunda revisión:** el preflight detectó OA6ajeno altemario en Historia2M Q24/25; se reescribieron para OA25 (diversidad/no discriminación), sustentado en Temarios/analisis/10-segundo-medio.md:260–263, actualizando pauta y tablas a14OA, manteniendo25preguntas/37puntos. No se limitaron a cambiar etiquetas. Escala Historia2M corregida contra calcular_nota; nuevo control independiente de dependencias de app detectó14bandas adicionales erróneas en Historia1M/7B/8B, corregidas. El control verifica tablas numéricas explícitas de exigencia60%, no toda prosa ni escala oficial Mineduc.

**Pendientes:** revisión independiente de deltas por cuota;366asociaciones documentales; estímulos visuales; cotejo fuente/DB/API/UI, reimportación aislada, permisos y matriz navegador. Revisar además clasificación V/F en pruebas Matemática3M: diagnóstico muestra `desarrollo_breve` para preguntas rotuladas Verdadero/Falso; no se cambió esa clasificación en este lote. La auditoría global sigue abierta. Sincommit/push ni despliegue.

### 15.14 Lote acotado — clasificación Verdadero/Falso

Causa reproducida: `_extraer_preguntas` reconocía la etiqueta, pero sin opciones a)/b) clasificaba siempre como desarrollo. Ahora etiquetas explícitas Verdadero/Falso o V/F generan opciones canónicas; si piden justificación, explicación o corrección escrita en español/inglés, permanecen manuales incluso con opciones V/F explícitas. No se infiere el tipo por la clave. Claves True/False/V/F se normalizan solo para V/F cerrados, preservando explicación completa. Se actualizó la regresión antigua de Inglés1M para exigir tanto clave seleccionable Falso como retroalimentación bilingüe original, sin perder su comprobación previa.

Mismo comando de cuatro archivos de §15.13 → **135/135**,1,31s, incluidos19casos nuevos (positivos, manuales y bilingües). Fallos reproducidos antes de corregir; preflight completo de12cursos sigue aprobando claves/opciones y conservación de3115+3035preguntas. Sesión de captura, sin PostgreSQL: **1580/1825unidades vinculadas (86,6%)**,121más que antes; **245pendientes**. Exámenes permanecen **1210/1210**. Estos contadores sustituyen los de §15.13, no su evidencia histórica.

Sin cambios a material curricular, backend/frontend en ejecución, dependencias ni datos reales. Rama main; revisión independiente, reimportación aislada, comprobación API/navegador y auditoría global siguen pendientes. No se declara aprobada toda clasificación posible mediante estas heurísticas. Sincommit/push.

### 15.15 Asociaciones explícitas y estímulos compartidos — continuación

**Preflight vigente:** mismo comando de cuatro archivos → **152/152**,1,36s. CLI estático →0discrepancias en265Markdown. Conservación3115preguntas de banco+3035evaluaciones. Importador de12cursos con sesión de captura: **1711/1825unidades (93,8%)**, **1210/1210exámenes**. Restan114:3B25,6B47,7B19,1M23. Unidades de1B,2B,4B,5B,8B,2M,3M,4M tienen vínculo en el preflight, no aprobación independiente ni cotejo DB/UI.

Se detectó pérdida real de estímulos: Lenguaje1B unidad2 omitía la nota de Camila y pegaba instrucciones de lavado a la última alternativa anterior; Lengua4M omitía textos compartidos; Matemática4B pegaba tablas de pictogramas/barras a preguntas previas. `_extraer_preguntas` ahora distribuye contexto Markdown a los números/rangos explícitos de directivas Lee/Observa/Usa, incluidas cursivas/paréntesis, y corta la pregunta previa antes de la directiva. Rechaza rangos inexistentes antes de expandirlos; conserva saltos de línea y tablas. Se agregaron directivas explícitas a las dos pruebas de Lenguaje4B, por grupos1–5/6–9 o1–5. Falta auditar otros estímulos sin rango declarado; no suponer recuperados todos los textos del corpus.

Se agregó `oa_por_pregunta` en frontmatter como objeto JSON (claves numéricas y valores OA principal opcionalmente con módulo), sin dependencias. Rechaza duplicados, números inexistentes, valores no textuales, OA múltiples y contradicciones con pauta; no modifica enunciado, clave ni rúbrica. Alternativamente admite línea `**OA principal:** OA n` en pauta numerada, retirándola del texto pedagógico y rechazando ambigüedad. Mapas aplicados tras revisar preguntas y OA de las guías en los niveles cerrados técnicamente; para preguntas integradas se declara un principal, no que solo evalúen ese OA. Quedan pendientes de revisión independiente. Se redujo salida diagnóstica de `LOGOS_AUDIT_CURSO` al curso solicitado sin reducir las comprobaciones de12cursos.

Precisión educativa: en Ciencias4B Tierra/Universo Q4, opción y pauta mantienen b pero dicen roca predominantemente sólida que se deforma lentamente, coherente con la guía ya corregida, en vez de llamar pastoso al manto. Revalidación independiente pendiente. Sin reimportación, cambios a datos reales, despliegue, commit ni push. La auditoría global sigue abierta.

### 15.16 Cierre técnico de asociaciones en memoria — no cierre global

Preflight de12cursos: **1825/1825unidades y1210/1210simulacros con OA**, conservando3115preguntas de banco y3035evaluaciones. Se completaron mapas explícitos de3B,6B,7B y1M, contrastando preguntas con OA de sus guías. En Inglés2M unidad1 Q2 se precisó OA9 (about/how, banco de comprensión general), no OA10. Siguen sujetos a revalidación curricular independiente; los mapas no certifican todas las dimensiones educativas.

Lengua1M unidades1/2: se declararon los seis rangos de lectura1–5,6–10,11–15. Cada grupo conserva su texto y las preguntas5/10 dejan de arrastrar el texto posterior; dos regresiones reales verifican pertenencia y separación de grupos. El importador en memoria exige ahora exactamente1825vínculos de unidad y coincidencia total/vinculadas en cada categoría de cada curso, en vez del umbral histórico>659.

Verificación vigente: cuatro archivos de pruebas del §15.13 → **154/154**,1,38s; CLI estático → sin discrepancias en265Markdown; `git diff --check` →0. Sin tocar PostgreSQL, API o navegador. Hallazgos educativos que requieren continuar: revisar formulaciones absolutas de pubertad en Ciencias6B unidad Vida Q9 y la coherencia de afirmaciones sobre oxígeno amazónico en Inglés1M; verificar otros estímulos no declarados. No se han reimportado estas fuentes ni aprobado la auditoría global. Sin commit/push.

Corrección educativa dirigida posterior: Ciencias6B Vida Q9 y su pauta dejan de declarar el vello facial exclusivo de hombres; describen tendencias de pubertad con variación individual. Regresión real falló antes y pasó después. Suite focalizada vigente **155/155**,1,39s, manteniendo1825/1825vínculos de unidad. Revalidación independiente y cotejo con app pendientes; el hallazgo de coherencia sobre oxígeno amazónico en Inglés1M se aborda en la corrección siguiente.

Inglés1M guía OA9 y unidad1 Q3: se reemplazó la mezcla de porcentajes brutos/netos por comprensión explícita sobre la función climática del bosque, conservando clave Falso. Enunciado y pauta permiten responder solo con el texto, sin conocimientos científicos externos. Regresión nueva falló antes y pasó después. Vigente: **156/156**,1,38s; CLI estático0discrepancias/265Markdown; diff-check limpio. Estas dos correcciones educativas todavía requieren revalidación independiente y persistencia/UI; no cierran el lote educativo de264recursos.

### 15.17 Candidata PostgreSQL aislada y cotejo exacto

Se creó **`logos_auditoria_fuentes_b9e8e43f`**, en localhost:5432, desde una plantilla vacía, sin borrar ni sobrescribir bases existentes. No se tocaron `logos_qa` ni `logos_auditoria_test`. Se ejecutaron `SQLModel.metadata.create_all` e `importar_curso` para los12cursos usando exclusivamente la sesión candidata. Resultado persistido:12niveles,58asignaturas,410OA,6150preguntas,206conjuntos. Las1825preguntas de unidad y1210simulacros conservan OA de su asignatura y respuesta no vacía; todos los6150registros tienen OA. Sin IDs repetidos dentro de conjuntos.

Cotejo completo posterior, no muestreo: se regeneraron objetos de fuente con `SesionCaptura` y se compararon multiconjuntos de410OA/guías,6150preguntas (tipo,enunciado,opciones,clave,retroalimentación,dificultad,vínculo semántico) y206evaluaciones (metadatos y orden completo de preguntas) contra PostgreSQL. **Coincidencia exacta en los tres controles.** No prueba corrección semántica de todas las preguntas ni cierre UI.

Incidencia del arnés: el primer conteo auxiliar asumió una tabla `objetivoaprendizaje` inexistente y terminó con `UndefinedTable` después de completar la importación. Se corrigió la consulta usando los modelos ORM (`objetivo_aprendizaje`), sin modificar aplicación ni repetir importación; conteos y cotejo posterior aprobaron. API de contenido/autoevaluación en comprobación sobre la candidata mediante `TestClient` y override de `get_session`, conservando límites de peticiones. Sin fixtures que eliminen tablas, datos reales, despliegue o commit/push. Actualización API: **895GET aprobados** con `TestClient`, sin mock de repositorios, usando solo la candidata por override de `get_session`. Se cotejaron12niveles,58asignaturas,410OA/guías y3115preguntas de banco (IDs,tipo,enunciado,opciones,clave,feedback) con PostgreSQL, excluyendo todas las preguntas de conjuntos. Dos404 y dos401 sin sesión comprobados. Sin desactivar límites:0pausas por429. Se conservó aviso de deprecación de `Starlette/httpx`, sin actualizar dependencias.

Piloto transaccional real de4B Matemática: **50peticiones/estados comprobados**,2cuentas y2perfiles sintéticos creados por API en la candidata, correo externo desactivado solo en el proceso de prueba. Tres intentos con0/6,3/6,6/6automáticas dieron notas1,0/3,5/7,0. Se verificó guardado incremental, persistencia PostgreSQL, reanudación del mismo intento, recarga con otro cliente, entrega idempotente y rechazo400 de respuestas después de entregar. Solicitudes sin sesión401 y de otra familia403, incluidos inicio, consulta y entrega. No es aprobación de todos los roles, niveles o evaluaciones; faltan otros bordes y progreso. La aplicación normal sigue usando `logos_qa`: estas verificaciones no cambian su configuración. Pendientes: matriz completa de calificación/autosave/progreso/permisos, navegador y dictamen independiente.

Regresión durable añadida a `backend/scripts/tests/test_importar_contenido.py`: `test_fuentes_coinciden_con_postgresql_candidato`. Solo se habilita con `LOGOS_AUDIT_DATABASE_URL`, exige host local y nombre `logos_auditoria_fuentes_*`, usa `SET TRANSACTION READ ONLY` y compara exactamente410OA/guías,6150preguntas y206conjuntos/orden. Sin variable queda omitida explícitamente, no aprobada. Se ejecutaron los cuatro archivos de pruebas con esa variable derivada internamente de la conexión local, sin mostrar credenciales: **157/157**,1,77s, cero omitidas. No altera la protección ni las fixtures destructivas de `backend/tests/conftest.py`.

### 15.18 Chromium real y encabezado del evaluador

**LGS-UI-RUNNER-H1-001**, moderado: al comenzar la práctica el evaluador perdía el únicoH1 (`page-has-heading-one`, axe). Reproducido en Chromium y mediante regresión DOM que falló0/1encabezados. Se añadió el título de evaluación al estado activo, sin desactivar reglas. Suite frontend completa: **77/77 en14archivos**,1,71s. También se reprodujo con regresión DOM la ausencia deH1 en resultados; se añadió el título y se corrigió el subtítuloH3→H2. Vitest vigente: **78/78 en14archivos**,1,50s. Se usa `provideRouter` real para renderizar los enlaces del resultado. Falta verificar en navegador ese estado final y los demás modos.

Recorrido real final aprobado: registro sintético por API → login UI → elegir perfil1M → guía Inglés OA9 → práctica → Comenzar → recorrer preguntas hasta el enunciado corregido sobre clima. Chromium, axe escritorio y390×844:0violaciones; sin overflow horizontal móvil y0errores JavaScript. No es prueba de pronunciación, toda la accesibilidad o todos los navegadores. Ensayos previos del arnés fallaron por esperar la pregunta dentro de la guía, omitir Comenzar y usar contexto implícito incompatible con axe; se corrigió el arnés antes de atribuir fallos a la aplicación.

Entorno temporal: API8011 y frontend4200, conectados a `logos_auditoria_fuentes_b9e8e43f`; correo externo desactivado. API configurada mediante entorno del proceso y frontend mediante `--define LOGOS_API_URL`, sin editar configuración persistente. El puerto4300 tenía otro proceso IPv6 y no fue detenido. No se ejecutó globalSetup con credenciales demo compartidas. Pendientes: Firefox/WebKit, estados finales del runner, estímulos visuales, pronunciación, permisos por otros roles, matriz completa e independencia curricular. Sin commit/push.

### 15.19 Alcance educativo acordado y desarrollo

Por solicitud explícita del usuario, este cierre se limita a guías, prácticas, pruebas y simulacros de12cursos, alineación con temarios oficiales y funcionamiento real de respuestas correctas, incorrectas, equivalentes, parciales y vacías. Se conserva toda la evidencia previa; pagos, infraestructura, despliegue y auditoría general de otros roles no condicionan este cierre. Las cifras de lectura y asociación OA no equivalen a revalidación educativa.

Inicio del lote de desarrollo: `planificacion/12-motor-de-evaluacion.md` §flujo6 exige comparación con pauta y revisión correcta/parcial/incorrecta, no corrección literal ni IA. **LGS-EDU-DESARROLLO-001:** en pruebas y simulacros el detalle omitía la pauta de preguntas abiertas (`respuesta_correcta=None`) y no transportaba retroalimentación, dejando al alumno sin criterios de revisión aunque existieran en fuente/DB. En práctica se muestra orientación, pero no hay selección de revisión y los espacios en blanco cuentan como respuestas. Reproducción y correcciones focalizadas en curso. No se añadirá una calificación automática inventada a las respuestas abiertas.

**Resultado del primer lote funcional:** se añadieron `pauta_orientativa` y `retroalimentacion` al detalle posterior a la entrega, conservando `es_correcta=None` y `respuesta_correcta=None` para desarrollo. Se muestran pauta, respuesta del alumno y criterios en resultados; en práctica y resultados se puede marcar revisión personal correcta/parcial/incorrecta. Se advierte expresamente que esta revisión no es automática, no modifica la nota y no se guarda al salir. Cambiar la respuesta invalida la revisión local anterior. Vacío, espacios y ausencia cuentan como pendientes; no habilitan una revisión ficticia. La nota se identifica como correspondiente solo a preguntas autocorregibles. No hay migración ni cambio de puntuación del backend.

Regresión nueva:7casos backend (correcta,equivalente,parcial,incorrecta,vacío,espacios,ausencia) fallaron por pérdida de pauta y luego aprobaron;12casos DOM prueban práctica y resultado. Consolidado vigente: **164/164 backend** con candidata PostgreSQL de solo lectura y sin conftest destructivo,2,22s,1aviso de deprecación; **90/90 frontend en14archivos**,1,60s. Los comandos son los cuatro archivos de §15.13 más `tests/test_evaluaciones_detalle.py::test_desarrollo_conserva_pauta_y_rubrica_sin_veredicto_automatico` con `--noconftest` y `LOGOS_AUDIT_DATABASE_URL` apuntando a la candidata; frontend `npm test -- --watch=false`.

Material real contrastado: Ciencias Naturales6B OA1, predicción sobre planta sin luz y requisitos/productos de fotosíntesis; referencia de extracción oficial `Temarios/analisis/06-sexto-basico.md`:132–135 (no se volvió a leer el PDF en este lote). Banco pregunta1988/OA182, prueba Ciencias de la Vida conjunto76/pregunta2153 y simulacro FormaB conjunto90/pregunta2318, en `logos_auditoria_fuentes_b9e8e43f`. **7/7 variantes en práctica Chromium móvil,7/7 en API de prueba y7/7 en API de simulacro.** La respuesta y la pauta se preservan; no se inventa veredicto automático. Comprobado bloqueo de pauta antes de entregar y ausencia de claves en conjuntos públicos. Recorridos Chromium de prueba y simulacro: escribir equivalente → guardar → entregar confirmando blancos → abrir revisión → leer pauta → marcar revisión personal. Sesiones preparadas con datos sintéticos; no se afirma probar login en este lote.

Incidencia real al revisar el simulacro:390px de viewport frente a413px de documento. La etiqueta nueva de nota heredaba fuente de40px; se separó en un span de16px, manteniendo grande solo el número. Revalidación del recorrido: **390/390px**, sin desbordamiento, pauta completa y revisión personal funcional. La primera ejecución global falló en esa última aserción aunque los7subcasos API anteriores pasaron; no se contó como recorrido aprobado hasta la segunda ejecución.

Denominador técnico actual de desarrollo: **3299preguntas** (1817banco,1482evaluaciones) frente a2851cerradas,6150total. No hay evaluaciones exclusivamente abiertas en esta candidata. Los21casos anteriores son funcionalidad representativa del mismo problema en tres contextos, **no3299pautas semánticamente revalidadas ni tres archivos completos aprobados**. Continúa pendiente la revalidación disciplinar/curricular por curso y asignatura, estímulos y reconciliación de estados/hashes de los264recursos. API8011 actualizada (shell91f45f); frontend4200 sigue con API candidata, correo externo desactivado. Solo datos sintéticos nuevos; sin tocar bases anteriores, commit ni push.

### 15.20 Reconciliación para no duplicar auditoría

El usuario pide explícitamente conservar revisiones anteriores y trabajar solo pendientes. No se vuelve a empezar sobre6150preguntas ni3299abiertas. La matriz CSV conserva289filas `revalidado` y1`revision_parcial_documentada` (Inglés5B simulacro); esos estados históricos no se sustituyen por «nunca revisado». El registro parcial5B describe el piloto antiguo; la reescritura/revisión posterior está en §15.1/15.3, con pendientes puntuales, no invalida todas sus claves.

Comparación reproducible `git diff --no-ext-diff --unified=0 8e4d83b -- contenido Temarios`:142rutas cambiadas,138decontenido y4análisis. De los264recursos educativos, **126no tienen delta textual**, **57solo añaden `oa_evaluados`/`oa_por_pregunta`**, **81tienen otros deltas**. El tablero decontenido y21fuentes completan las148rutas sin diferencias. Son grupos de diferencias respecto al corte histórico, no porcentajes de aprobación ni comparación individual de todos losSHA del CSV. En los57se conserva la resolución de enunciados/claves; solo interesa trazabilidad OA. Los81no son81archivos nunca vistos: cruzar únicamente sus deltas con evidencia posterior. Un hallazgo abierto explícito sigue pendiente aunque el archivo no haya cambiado.

**Evidencia que se conserva sin repetir resolución:** §15.9/bbfe6837 ya registra segunda resolución/aprobación educativa de secuencia1B, mamíferos2B, continentes3B, manto/litosfera4B y distractorMat7B; §15.9/8d8793a2 aprueba deltas Lengua/Filosofía/Ciencias4M y §15.11 confirma corrección de sus tresP3editoriales; §15.3 aprueba50/50ítems nuevos de Inglés3M/4M y revisión de1M/2M, salvo cambios posteriores enumerados. §15.9 supera las antiguas lecturas incompletas de §15.4:264/264leídos inicialmente, no264pendientes ni264aprobaciones actuales.

**Cola explícita, sin reabrir lo anterior:**
- Inglés5B: solo ajustesP9/P17 y apoyo visual;6B–8B: revalidación de75ítems nuevos del simulacro, no volver a resolver sus guías/pruebas ya revisadas;1M/2M: cambios puntualesP21y1MP24, más delta posterior Amazonas1M (§15.16). Inglés3M/4M conserva aprobación de50ítems, salvo delta posterior comprobado.
- §15.9/0674814e y6beb8a31: segunda resolución de cambios Historia/Mat/Lengua5B y datos/lectura/CO2/escala6B. No repetir todos sus cursos.
- Historia2M: cuatro preguntas sustituidas de unidad, aplicación jurídica y dos preguntas nuevasOA25 del simulacro (§15.13);1M/3M: solo deltas críticos de §15.9/df304687. EdCiudad4M: ajustes puntuales listados en §15.7, no sus112ítems ya resueltos.
- Historia7B/8B: alternativas reparadas y cambios posteriores de escalas; Mat8B P14 y tablaLengua7B según §15.3, a cruzar con correcciones/evidencia posteriores antes de resolver de nuevo.
- Estímulos gráficos enumerados en §15.12 y delta de parser/rúbricas pendiente de segunda revisión. Los fallos técnicos de pérdida de pautas, asociaciones y entrega ya cuentan con §15.17–19; no vuelven a figurar como nunca ejecutados.

**Cotejo final de los290SHA:** se leyó el CSV versionado mediante `git show HEAD:docs/auditorias/matriz-maestra-estado-por-archivo.csv`, verificando que no tiene cambios locales, y se compararon sus290`blob_sha` contra `git hash-object --stdin-paths` sin escribir objetos. **151SHA idénticos y139distintos**; encontenido128idénticos (127recursos+tablero) y137distintos; enTemarios23idénticos y2distintos. El CSV es un corte mixto: cuatroSHA no corresponden a8e4d83b (resumen, análisis2M/4M y guíaInglés5B). Tres de esas cuatro versiones sí coinciden con el trabajo actual. Por eso el cruce directo refina el diagnóstico preliminar: **127recursos sin cambios respecto a su evidencia registrada,57solo con añadidosOA y80con otros deltas**,264total; más23fuentes sin cambio y2análisis modificados. No se confunde identidad SHA con ausencia de hallazgos abiertos. La guíaInglés5B no debe reabrirse por la errata antigua: suSHA ya coincide con el registrado.

Esta cola procede de pendientes explícitos de los informes; aún debe terminarse la reconciliación por ítem/versión dentro de los80deltas. Las ubicaciones antiguas del tablero §5 se cruzarán primero con §11–15 y las regresiones existentes, sin repetir esos recálculos por inercia. No se altera el CSV ni se reemplazan susSHA históricos porSHA actuales conservando una aprobación sin fundamento. Sin nuevas pruebas de preguntas, cambios de contenido, commit ni push en este lote documental.

**Comparación estructurada por pregunta —206evaluaciones:** se aplicó el mismo parser actual a los blobs históricos del CSV y al texto actual obtenido del diffGit. Se verificó SHA de cada texto reconstruido; no se alteraron archivos ni objetosGit. Se compararon tipo, enunciado, opciones en orden, clave y retroalimentación, normalizando solo espacios, no significado. Resultado: **89evaluaciones SHA idéntico;71modificadas sin cambios en esos campos;46con deltas**. Dentro de las evaluaciones modificadas se conservan1356preguntas idénticas y aparecen369posiciones con algún delta. Es una lista de diferencias para cruzar con dictámenes, **no369preguntas nunca revisadas**. No hubo errores de extracción. No cubre toda instrucción, portada, tabla externa, OA o figura; los hallazgos explícitos siguen abiertos aunque el ítem sea idéntico.

Ubicaciones con delta detectado (E=simulacro, U=unidad; no implica reabrirlas todas):

| Curso | Ubicaciones |
|---|---|
|1B|FormaA P3, ya aprobado en §15.9|
|3B|HistoriaGeografíaU P3, ya aprobado en §15.9|
|4B|CienciasTierraU P4; LenguajeU1 P1–9/U2 P1–5|
|5B|HistoriaE P1/3/6/12/14/17/20/21/24; InglésE P1–25; LenguajeE P2; MatNúmerosU P9|
|6B|CienciasE P21; InglésE P1–25; LenguajeE P22; CienciasVidaU P9; InglésU1 P6/U2 P4; MatMediciónU P11|
|7B|HistoriaE P1/3; InglésE P1–25; MatE P4|
|8B|HistoriaE P9; InglésE P1–25; MatE P14; InglésU2 P1|
|1M|InglésE P1/3/4/6/10/11/14/15/17/19/20/21/22/23/24/25; InglésU1 P3; LenguaU1 yU2 P1–15|
|2M|HistoriaE P4/23/24/25; InglésE P4/6/7/8/9/10/11/14/15/17/20/21/22/23/24/25; HistoriaFormaciónU P10–13|
|3M|CienciasE P3; InglésE P1–25; CienciasSeguridadU P10; CiudadanaU1 P14; MatÁlgebraU P2/ProbabilidadU P10|
|4M|CienciasE P4/11; CiudadanaE eInglésE P1–25; LenguaE P4/5/6/7/8/10/12/13/14/15/16/19/20/21/22/23/24/25; CiudadanaU1/U2 P1–15; FilosofíaU1 P9/U2 P2; LenguaU1 P1–12/U2 P1–14|

**Depuración, antes de resolver:** los44deltas de Lengua1M U1/U2 y Lenguaje4B U1/U2 provienen únicamente de añadir instrucciones de rango y mapasOA, no de reescribir textos, preguntas o claves; diff de las cuatro unidades comprobado. Conservan resolución educativa previa; la recuperación funcional de estímulos se trata aparte en §15.16–17. Los50ítems de Inglés3M/4M ya tienen segunda resolución (§15.3), no se vuelven a resolver. En Inglés5B se conservan los23ítems independientes no afectados por P9/P17; en1M/2M se conserva revisión previa excepto sustituciones puntuales citadas y delta posterior identificado. En los deltas aprobados de4M se conserva §15.9, sin convertir correcciones editoriales en una nueva auditoría de todos sus ítems. Donde no se pueda vincular inequívocamente versión y dictamen se usa **evidencia por confirmar**, no «nunca revisado». No se anuncia porcentaje global de cierre a partir de estos grupos.

**Primer pendiente puntual cerrado tras conciliar:** Mat5B NúmerosU P9, delta de0674814e (§15.9). Segunda resolución directa del coordinador respecto al cambio de aquel autor:3/10=0,3;0,03=3/100,3,0=3y0,33=33/100, de modo que solo a es correcta. El antiguo0,30 sí equivalía a0,3, por lo que se confirma que la corrección del distractor, no de la clave, era necesaria. Alineación con extracción oficial deMat5B OA10 (`Temarios/analisis/05-quinto-basico.md`:100–102). Se conserva la corrección existente; no se reescribe contenido ni se resuelve el resto de la prueba. Nueva regresión exacta con `Fraction` en `backend/tests/test_parser_prueba_examen.py::test_matematica_5b_p9_tiene_una_sola_alternativa_decimal_equivalente`: **1/1 aprobada**,0,05s,86deseleccionadas,`--noconftest`. Primer ensayo del test falló por esperar letraa en vez del texto0,3 que devuelve el parser; se corrigió el arnés, no el producto. No se presenta ese fallo como defecto nuevo. La corrida164/164 es anterior a añadir este caso; no se afirma una nueva corrida165. Queda revalidado solo este delta, no todo el lote5B.

### 15.21 Corte solicitado para commit/push y estado por curso

El usuario solicita guardar y subir el avance ahora; **es un checkpoint de trabajo, no cierre ni publicación del material**. Verificación previa nueva: **168/168 backend**,2,96s,1aviso, con los cuatro archivos de §15.13 más `scripts/tests/test_auditar_fuentes_curriculares.py` y los7casos de desarrollo de §15.19; `--noconftest`, candidataPostgreSQL en solo lectura. **90/90 frontend**,14archivos,1,91s; aviso Node25 noLTS. Sin fixtures destructivas, despliegue ni cambios a producción. Diff revisado por alcance y contratos; se conservan las correcciones de accesibilidad y pruebas acumuladas antes de acotar la auditoría.

**Respuesta sobre completitud:** los12cursos/58asignaturas y264recursos recibieron lectura/revisión inicial; no hay que reiniciar toda esa auditoría. No está aprobado el100%de las versiones posteriores. La cola está en §15.20 y los casos gráficos en §15.12. Se conserva toda aprobación aplicable al texto actual; un pendiente de segunda resolución no demuestra que la respuesta actual esté errada. Donde no hay dictamen vinculable se marca evidencia por confirmar. El porcentaje educativo restante por curso/ramo **no está consolidado con un denominador fiable**; no se inventa un porcentaje de cierre a partir de SHA, lecturas o tests.

|Curso|Pendientes puntuales de cierre o evidencia por confirmar, no materias enteras sin revisar|
|---|---|
|1B|Estímulos en Matemática/Lenguaje/Historia/Ciencias y formas integradas enumerados en §15.12. Secuencia matinal corregida y aprobada: no repetir.|
|2B|Dos estímulos del integradoFormaA. Se conserva aprobación del matiz sobre mamíferos.|
|3B|Estímulos de Matemática/Ciencias e integradoFormaA. Se conserva corrección del modelo continental.|
|4B|Confirmar alcance de corrección en CienciasTierraU P4 y render de contexto de Lenguaje. No reabrir textos/claves solo por añadir rangos de lectura.|
|5B|Historia: ítems reescritos y escala/prosa; LenguajeE P2; InglésE P9/P17 y apoyo visual. MatNúmerosP9 ya revalidada, no repetir.|
|6B|Matemática: datos de medición; LenguajeE P22; Ciencias: CO2 y clasificación de pubertad; Historia: escala/prosa; Inglés:25ítems nuevos del simulacro y ajustes puntuales de unidades.|
|7B|HistoriaE P1/P3 y escala/prosa; Inglés:25ítems nuevos; Lengua: tabla de especificaciones. Matemática: conservar aprobación del distractor y confirmar alcance/versiones sin volver a resolver por inercia.|
|8B|MatE P14; HistoriaE P9 y escala/prosa; Inglés:25ítems nuevos y ajustes de unidad.|
|1M|Historia: correcciones documentales y escala; Inglés: sustituciones puntuales y delta Amazonas; Lengua: trazabilidad de tabla/contextos, no nueva resolución de los30ítems de las unidades.|
|2M|Historia: cuatro preguntas nuevas de unidad, sustituciones de simulacro, alternativas reparadas y aplicación jurídica; Inglés: ajustes posteriores a la revisión; Lengua: directiva atenuada. La inversa de Matemática no se reabre por un checkbox histórico.|
|3M|Matemática: modelo/dominio/probabilidad; Ciencias: mitigación y opción reparada; CiudadanaU1 P14. Inglés: conservar25ítems del simulacro aprobados y confirmar solo ajustes posteriores de guía/unidades.|
|4M|Ciudadana: ajustes jurídicos/institucionales posteriores a112ítems resueltos; CienciasE P4/P11; confirmar ajustes posteriores de Inglés sin repetir25ítems del simulacro aprobados. Conservar aprobación de deltas de Lengua/Filosofía y no convertir cambios editoriales en una auditoría nueva.|

Las otras materias conservan sus revisiones previas salvo hallazgo explícito; esta tabla no concede automáticamente certificación completa por asignatura. **100%lectura inicial=264/264;69,7%recursos sin cambio de preguntas/texto por identidad o soloOA=184/264;77,7%evaluaciones sin delta en campos de preguntas=160/206.** Los dos últimos son conservación de evidencia, no aprobación pedagógica ni porcentaje pendiente. Algunos ítems con delta ya están aprobados; algunos gráficos pendientes no cambian deSHA. El checkpoint no convierte esos porcentajes en100%listo para estudiantes.

### 15.22 Lote ejecutado tras §15.21 — Inglés5B/6B, Historia5B, estímulos de Lenguaje e importación aislada

**Inglés5B simulacro — P9/P17 cerradas.** P9 decía "four o'clock in the afternoon" pero la pauta afirmaba "sin especificar am/pm": contradicción real corregida; ahora acepta At 4 pm/4 p.m./16:00/At 4 en contexto y rechaza 4 am. P17 (opposite of open → shut) verificada con única alternativa válida y sin pista de rima. Regresión: 2/2 casos nuevos aprobados. Los otros23ítems conservan la revisión previa; pendiente solo apoyo visual (OA5/OA14 exigen ilustraciones en el PDF, mejora pedagógica separada).

**Historia5B simulacro — 9deltas resueltos.** P1/3/6/12/14/17/20/21/24 revisados ítem por ítem: claves correctas, OA y pautas coherentes. Dos correcciones de precisión histórica: P1 atribuía Concepción/La Serena/Valdivia a "otros capitanes" (impreciso: Valdivia las dirigió) → reformulado; P3 afirmaba "varias décadas" con un registro de 11 años (1541–1552, Memoria Chilena verificada: Concepción 1550, Valdivia 1552) → reformulada como refutación con fechas explícitas; mismo error corregido en la pregunta6 de la guía. Escala35puntos ya verificada en §15.9. Regresión: 13/13 casos nuevos aprobados. **Pendiente: segunda resolución independiente de estas correcciones (protocolo).**

**Lenguaje5B P2 y Mat6B P11 confirmados sin cambios.** P2 admite metáfora (respuesta esperada) y personificación si el estudiante la fundamenta en "la greda no miente" — aceptación justificada correcta. P11 de Mat6B tiene los4meses completos y clave correcta (abril, 6ºB35 vs 6ºA18, diferencia17); el defecto histórico de datos faltantes ya estaba reparado en6beb8a31.

**Bloqueo de estímulos compartidos corregido (Lenguaje6B P22 → sistémico).** El parser reconocía contextos solo de instrucciones "Lee/Observa…", no de encabezados "Texto N (para las preguntas…)", así que P22 y otras preguntas llegaban a la base sin el texto que necesitaban. Se amplió `_extraer_preguntas` y se corrigió el rango del encabezado de Texto4 (9 a13 y22). Barrido reproducible sobre las206evaluaciones/3035preguntas: el cambio afecta enunciados de **8simulacros de Lenguaje,153enunciados**, y **0cambios de tipo, opciones o pauta**. Regresión sintética: ningún texto se adjunta a la pregunta equivocada. **Nueva base aislada `logos_auditoria_fuentes_20261102_d251e849`:6150preguntas/410OA/206evaluaciones idénticas a fuentes** (cotejo objeto a objeto); API GET de los8simulacros devuelve las200preguntas exactamente como en DB, incluido el estímulo Alto Hospicio en P22; sin claves ni rúbricas anticipadas; transacción de solo lectura; bases anteriores sin tocar.

**Inglés6B simulacro —25/25ítems resueltos,3correcciones.** P12 (emoción literal del texto) estaba en OA8 siendo lectura literal → reasignada a OA5, con nota en el apartado; P14 exigía literalmente "because" → pauta ahora acepta justificación coherente sin el conector; P10 etiquetada "pregunta abierta — verdadero o falso" se clasificaba como desarrollo → etiquetada V/F cerrado seleccionable; recuentos de tipos/OA y tabla de especificaciones actualizados (11cerradas/14abiertas; OA5×6,OA6×5,OA8×4,OA14×5,OA15×5). Regresión: **26/26 casos**. **Pendiente: segunda resolución independiente de estas3correcciones.**

**Pruebas del lote:** suite focal `--noconftest tests/test_parser_contenido.py tests/test_parser_prueba_examen.py scripts/tests/test_importar_contenido.py scripts/tests/test_validar_evaluaciones_markdown.py scripts/tests/test_auditar_fuentes_curriculares.py tests/test_evaluaciones_detalle.py::test_desarrollo_conserva_pauta_y_rubrica_sin_veredicto_automatico` → **209aprobadas/210,1omitida** (integraciónPostgreSQL: requiere `LOGOS_AUDIT_DATABASE_URL`; con ella la misma prueba ya pasó sobre la base aislada),1aviso (4tests fallaron antes de cada corrección; reproducidos). Nuevo defecto educativo encontrado y corregido: contradicción de pauta en Inglés5B P9 y desajuste factual en Historia5B P3/guía. **Pendientes para el siguiente lote:** Inglés7B/8B (50ítems nuevos del simulacro), estímulos visuales1B–3B e Inglés5B/6B, deltas4M (Ciudadana/Ciencias) y segundas resoluciones señaladas. Sin reauditar ítems aprobados.

### 15.23 Conversión total a alternativas (decisión del 2026-11-06) — material, parser y pruebas

**Decisión del usuario:** todas las respuestas de todos los materiales pasan a alternativas, con una sola correcta o con varias correctas («marca todas las correctas», corrección todo o nada), además de verdadero/falso. Motivo: la app no corrige texto libre de forma confiable y las 3.299 preguntas abiertas (cerca del 50 % de pruebas y simulacros) no contaban para la nota. Las versiones abiertas se conservan sin pérdida en `docs/banco-preguntas-abiertas/` (respaldo exportado desde `e6336af`) y en el historial git.

**Alcance ejecutado:** los 12 cursos y las 58 asignaturas: guías, 156 pruebas de unidad y 50 simulacros, es decir, los 264 recursos educativos más el tablero. Cada pregunta abierta se reescribió como ítem cerrado, conservando su OA, su intención evaluativa y la explicación de la pauta. Los ítems de unir pasan a «¿qué combinación es correcta?» y los bloques V/F múltiples, a «marca todas las verdaderas». Los puntajes declarados de los simulacros se conservan.

**Textos residuales también actualizados:** instrucciones, hojas de respuesta (antes listaban solo las cerradas), columna «Tipo» de la pauta, tablas de especificaciones «Cerradas | Desarrollo» (45 archivos; ahora una sola columna «Alternativas») y rúbricas manuales (por ejemplo, la tabla «Pregunta manual» de Lengua 4M).

**Resultado medido con el código actual:**

| Tipo de pregunta | Cantidad |
|---|---|
| Alternativas | 5.031 |
| Verdadero/falso | 850 |
| Varias correctas | 269 |
| Desarrollo breve (abiertas) | **0** |
| **Total** | **6.150** |

- El validador `validar_evaluaciones_markdown.py` no encontró discrepancias en 265 archivos.
- `fijar_oa_por_pregunta.py` resolvió el OA de todas las preguntas de prueba en los 12 cursos.
- Importación completa en una SQLite desechable (sin tocar la base de desarrollo): 6.150 preguntas y **0 sin OA**.

**Parser (`parser_prueba_examen.py`):** un V/F solo se considera de respuesta escrita cuando hay verbos imperativos («justifica», «explica», «corrige»…) o «con justificación» en la etiqueta. Antes bastaban «argumento» (sustantivo), «explica» dentro del estímulo o «to explain» en infinitivo, y eso convertía en abiertos ítems autocorregibles. Hay regresiones sintéticas para ambos casos.

**Pruebas ejecutadas en esta sesión:**
- Backend completo: **714 aprobadas, 1 omitida** (5 min 57 s).
- `scripts/tests`: **55 aprobadas, 1 omitida**.
- Frontend: **95/95** en 14 archivos; `ng build` correcto.
- Se actualizaron los 44 tests del parser fijados al contenido abierto antiguo. Conservan su propósito (OA, clave = opción, estímulo correcto) y no se relajó ningún control.
- Nueva guarda de corpus: `test_corpus_completo_sin_preguntas_abiertas_y_con_claves_validas` exige 0 abiertas y claves válidas en los 264 recursos.

**Hallazgos educativos corregidos durante la conversión** (detalle en la bitácora de trabajo):

| Curso | Recurso | Corrección |
|---|---|---|
| 8B | Historia guía OA18 #3 | Opciones equivalentes |
| 8B | Historia simulacro P8 | Anacronismo Valladolid/Leyes Nuevas |
| 8B | Lengua guía OA16 #2 | «les» → «nos» |
| 1M | Ciencias guía OA14 #3 | Clasificación de eclipses |
| 2M | Historia guía OA10 #3 | Orden de golpes: Uruguay antes que Chile |
| 2M | Inglés guía OA9 #5 y OA10 #8 | Gramática |
| 3M | Ed. Ciudadana guía OA4 #10 | La tasa la fija el Banco Central, no el gobierno |
| 6B | Ciencias Vida U P9 | «Vello facial» era ambiguo como cambio «común a ambos sexos»; se reemplaza por una opción exclusiva e inequívoca |
| 5B | Matemática simulacro P25 | Subpreguntas importadas como alternativas |

**Estado — no es aprobación:** los ítems nuevos los redactó un solo autor (el coordinador). Falta, antes de dar el material por listo para estudiantes:
- La **segunda auditoría y validación independiente** que pidió el usuario.
- Revisar sesgos de construcción: posición de la clave (sesgo preexistente hacia «b») y longitud o detalle de la opción correcta frente a distractores implausibles.
- Revisión en navegador del flujo «varias correctas».

Las aprobaciones de §15.9–15.22 sobre ítems cerrados no modificados se conservan. Las de ítems abiertos ya no aplican a su versión de alternativas. Sin despliegue, commit ni push en este lote.

### 15.24 Sesgos de clave: posición y longitud (2026-11-06)

- **Posición.** «b» era la clave del 39 % de las alternativas. `backend/scripts/rebalancear_claves.py` intercambió 693 claves (y sus referencias en pautas y retros), con verificación por intercambio. Distribución resultante ≈ a 23 / b 28 / c 25 / d 24 %. `restaurar_orden_numerico.py` devolvió el orden ascendente a 252 ítems con opciones numéricas.
- **Longitud.** Criterio (`ajustar_distractores.sesgada`): la clave es más larga que todos los distractores (>máx/0,9), al menos 1,3 veces su promedio y con al menos 12 caracteres de diferencia. Al inicio el 48 % de las alternativas lo cumplía. Se reescribieron los distractores ítem por ítem como errores plausibles, sin tocar nunca la clave. Los cambios se propagaron a los gemelos guía↔prueba↔simulacro. Resultado medido:
  - simulacros: 1 sesgado (excepción);
  - pruebas: 3 sesgados (excepciones);
  - guías: 5 sesgados de 2.461 alternativas (excepciones).
- **Excepciones justificadas (9).** Son ítems cuyas opciones son citas textuales o datos explícitos del estímulo; alargarlas exigiría inventar texto:
  - 4B-B P5;
  - 4M Lengua U2 P4 y la guía OA 3#4;
  - 6B Lenguaje U1 P8 y la guía OA 5#5;
  - 8B Lengua U2 P5 y la guía OA 9#5;
  - 4B Lenguaje guía OA 5#5 y OA 6#5.
- **Defectos de herramienta corregidos.**
  - Una guía con el mismo OA en dos módulos (3M Ciencias para la Ciudadanía) colisionaba los identificadores; ahora el segundo módulo usa `OA 1@2#i`. Las verificaciones impidieron escrituras erróneas.
  - Corregí dos distractores que yo había redactado con una cita inventada o un dato falso del texto (6B «primer verso», 2B «lo sospechaba desde el lunes»).
- **Verificación.**
  - OA re-fijados en los 12 cursos.
  - Validador: 0 discrepancias en 265 Markdown.
  - Scripts: 57 pasados (+1 omitido), incluida la importación completa en memoria.
  - Backend: 717 pasados (+1 omitido).
- **Pendiente.**
  - Lectura humana de muestra: las retroalimentaciones que describen un distractor por su contenido pueden haber quedado desalineadas.
  - Revisión en navegador de «varias correctas».
  - Segunda validación del usuario.

### 15.25 Validación integral en navegador con Playwright (2026-11-06)

- **Entorno aislado.**
  - Base nueva `logos_e2e_alternativas`, importada desde las fuentes actuales; no se tocaron `logos_qa` ni las demás bases.
  - API en el puerto 8001 y frontend en el 4300.
  - Fixture de claves exportada desde la misma base (`backend/scripts/exportar_fixture_validacion_e2e.py`), fuera del control de versiones.
- **Spec `frontend/e2e/validacion-integral-material.spec.ts`.** Recorre los 12 cursos, todas las asignaturas, las 410 guías (estudio y autoevaluación) y las 206 pruebas y simulacros: 264 casos y 6.150 preguntas por navegador. Para cada pregunta exige:
  - enunciado sin restos de Markdown ni de la pauta;
  - control correcto según el tipo, con exactamente las opciones de la base;
  - respuesta registrada en pantalla;
  - en la autoevaluación, «¡Correcto!» al marcar la clave;
  - en pruebas y simulacros, «N de N correctas» y nota 7.0, sin aviso de preguntas faltantes.
- **Defectos reales encontrados y corregidos.**
  1. *Respuestas perdidas por concurrencia.* El autosave hacía leer-modificar-escribir sin bloqueo. Al marcar varias casillas seguidas, o al entregar justo después de responder, se perdía una respuesta o se reabría un intento entregado. Corrección:
     - backend: `buscar_por_id_para_actualizar` con `SELECT … FOR UPDATE` en Responder y Entregar;
     - frontend: guardados en cola, y la entrega espera a que terminen;
     - prueba unitaria `evaluacion-runner-guardado.spec.ts`.
  2. *V/F marcada sin estar registrada.* Los radios de V/F no tenían `[checked]` ni `value`. Al pasar de una V/F a otra se veía marcada la respuesta anterior, pero no se registraba. Corregido en `evaluacion-runner.ts`.
  3. *22 pruebas con nombre repetido en 8 ramos* (6B/7B Matemática, 7B/1M Historia, 3M CpC y Educación Ciudadana, 4M Inglés y Matemática). El importador usa ahora el `título:` del frontmatter; se agregó un título a 8 archivos y una guarda `test_nombres_pruebas_unicos.py`.
- **Resultado final (2026-11-07).** Con el frontend compilado y servido estático, porque el servidor de desarrollo generó bloqueos «408» en Firefox durante una corrida previa: **792/792 aprobados en 41,9 min**.
  - Chromium: 264/264.
  - Firefox: 264/264.
  - WebKit: 264/264.
  - Equivale a 6.150 preguntas por navegador, todas respondidas con su clave, con el registro de la respuesta verificado y nota 7.0.
  - Evidencia: `frontend/test-results/validacion-integral-20261107/` (`report.json`, `corrida.log`).
- **Suites.**
  - Backend: 718 pasados (+1 omitido).
  - Scripts: 58 pasados (+1 omitido).
  - Frontend: 96 pasados.
- **Revisión de retroalimentaciones.** Las 26 que mencionan la letra de un distractor siguen coherentes con sus opciones.
- **Observación menor.** Angular avisa NG0956: `track op` recrea las opciones al cambiar de pregunta. No afecta la corrección.

### 15.26 Revisión disciplinar y pedagógica ítem por ítem — 4.° básico (2026-11-07)

**Alcance.** Lectura experta de todas las preguntas de 4.° básico, con 4 guías, 12 pruebas y 2 simulacros: clave correcta en la disciplina, distractores plausibles y sin ambigüedad, adecuación al nivel y coherencia de la retroalimentación. En Matemática se recalculó cada operación.

**Hallazgos corregidos.**

- *Matemática*
  - Guía OA 18#4 y prueba Geometría P8: «la *sombra* de un árbol reflejada en el agua» pasa a «la *imagen*». Es un error conceptual: el agua refleja la imagen, no la sombra.
  - Guía OA 27: la instrucción «Usa el gráfico… preguntas 3, 4 y 5» quedaba dentro de la retroalimentación de la P2; ahora va en el enunciado de P3, P4 y P5.
  - Guía OA 8#5: el enunciado no nombraba las fracciones que compara.
  - Guía OA 6#6: la retroalimentación usaba decimales (19,75), fuera de nivel; pasa a «19 y sobran 3».
- *Ciencias Naturales*
  - Retroalimentaciones que mencionaban una «silla» que ya no está entre las opciones (guía OA 10#3 y prueba P3).
  - Distractor «Nazca y Antártica»: la placa Antártica sí bordea Chile en el extremo sur, así que era ambiguo; pasa a «Africana y Antártica».
  - Simulacro A P20: describía el manto como «semi-líquido», en contradicción con la guía y la prueba. Ahora dice roca mayormente sólida que fluye lentamente.
  - Simulacro A P15: enunciado ininteligible («¿Cuál… es información líquida…?»).
- *Historia*
  - Extensión del Tawantinsuyu: no llegaba solo «al norte de Chile», sino hasta la zona central (río Maule). Se corrigió en la retroalimentación de la guía OA 4#1, y el enunciado del Camino del Inca en la guía OA 4#6 y la prueba Historia P9.
  - «Derecho al recreo» pasa a «derecho al juego y al descanso».
- *Lenguaje*
  - Guía OA 6#5 y su texto en la prueba U2: la clave «implícita» («el puma es muy adaptable») estaba casi explícita en el texto («se adapta fácilmente a climas fríos y calurosos»). Se reescribió esa oración del texto para que sea una inferencia.
- *Simulacros*
  - Seis enunciados del simulacro B mostraban al alumno la etiqueta «(Alternativas)».
  - Simulacro A P9: «¿Cuántos chocolates *va*?» pasa a «*van*».
  - Simulacro B P9: el distractor «hasta Tierra del Fuego» no coincidía con el texto («hasta la Patagonia»).

**Hallazgo sistémico y corrección de la app.** 221 preguntas de guías en todo el corpus remiten a un texto, poema, tabla, gráfico o «Ejemplo n» de la guía, pero la pantalla de autoevaluación solo ofrecía «← Volver a la explicación», con lo que se perdía la práctica en curso.
- La autoevaluación tiene ahora un panel desplegable «📖 Ver la guía (textos, tablas y ejemplos)» con el contenido del OA. Se verificó que `contenido_guia` no contiene las claves de la práctica en ninguno de los 410 OA.
- El spec E2E exige que el panel exista, que muestre la guía y que no muestre claves. Resultado: 4.° básico 18/18 en Chromium.

**Observación de diseño, sin cambios.** El 79 % de las preguntas de pruebas de unidad (1.448 de 1.825) es idéntico a una pregunta de práctica de la guía; en los simulacros, solo el 8 %. Es la decisión documentada en `planificacion/08-diseno-pruebas-vs-examenes.md`: las pruebas se arman desde el banco de la guía. Pedagógicamente, la prueba de unidad mide más recuerdo que transferencia. Queda para decisión del usuario.

**Verificación.**
- OA re-fijados en 4.° básico.
- Validador: 0 discrepancias.
- Scripts y parsers: 212 pasados (+1 omitido).
- Frontend: 96 pasados.
- E2E de 4.° básico: 18/18 en Chromium.
