---
título: Estado de avance del contenido de estudio
última actualización: 2026-10-26
---

> **Estado real verificado en base de datos (2026-10-26, `logos_qa`):** 12 cursos con
> guía de estudio y banco de autoevaluación; **408 OA** oficiales; **6.130 preguntas**;
> **156 pruebas de unidad**; **50 conjuntos de examen simulacro**. La auditoría maestra
> de octubre 2026 (ver `../docs/auditorias/AUDITORIA_MAESTRA.md`) corrigió claves, pautas, sesgos y
> erratas en los 50 exámenes; los validadores de contenido dan 0 hallazgos.
>
> **Exámenes simulacro — estado real:** Régimen A (1°-4° básico) tiene **Forma A y B**
> integradas (8 archivos, 2 por curso). Régimen B y C (5° básico-4° medio) tienen
> **solo Forma B** por asignatura (42 archivos); la **Forma A de esos regímenes no está
> construida**.
>
> **Nota de diseño:** las pruebas de unidad se guardan con `nivel_id = NULL` y
> `asignatura_id` asignada; el frontend las lista por asignatura
> (`conjuntos/asignatura/:id`). Los exámenes integrados de Régimen A se listan por nivel
> (`conjuntos/nivel/:id`). No "normalizar" ese `nivel_id`: rompería el contrato de
> listados.
>
> La sección "Pruebas por materia" de más abajo es **histórica**: esas 58 pruebas fueron
> reemplazadas por las 156 pruebas de unidad el 2026-08-11 (ver el rediseño siguiente).

Ver criterio de "materia lista" en `../planificacion/04-modo-de-operacion.md`.

## ✅ Rediseño completo (2026-08-11): pruebas de unidad reemplazan a las "pruebas por materia"

Ver decisión completa en `../planificacion/08-diseno-pruebas-vs-examenes.md`. Las 58
"pruebas por materia" (20-25 preguntas, tamaño del examen real) se reemplazaron por **pruebas
de unidad más cortas** (8-15 preguntas según edad, una por eje temático/bloque de OA), para
no abrumar a los niños y porque el examen real no tiene ese formato. Los **exámenes
simulacro** (Forma A/B, tablas más abajo) NO cambiaron — ya están validados contra el texto
oficial del Mineduc (20 preguntas integradas en básica, 25 por asignatura desde 5° básico).

**✅ Los 12 cursos completos — 156 pruebas de unidad en total**, siguiendo la calibración por
edad de `planificacion/08-diseno-pruebas-vs-examenes.md`:

| Curso | Preguntas/unidad objetivo | Estado |
|---|---|---|
| 1°-2° básico | 6-8 | ✅ completo |
| 3°-4° básico | 8-10 | ✅ completo |
| 5°-6° básico | 10-12 | ✅ completo |
| 7°-8° básico, 1°-2° medio | 12-15 | ✅ completo |
| 3°-4° medio | 12-15 | ✅ completo |

Nota: en un puñado de casos (ejes/OA con muy poco banco fuente — p. ej. Matemática 6° básico
ejes de un solo OA, Geografía/Formación Ciudadana en varios cursos de Historia) el banco
original no alcanzaba el mínimo del rango objetivo; se completó con preguntas nuevas del
mismo estilo y nivel, sin inventar contenido curricular fuera del OA correspondiente, dejando
explícito en cada archivo cuándo esto ocurrió.

## Régimen A (1°-4° básico) — prueba integrada

| Curso | Lenguaje/Comunicación | Matemática | Cs. Naturales | Historia/Geo/Cs. Sociales | Estado curso |
|---|---|---|---|---|---|
| 4° básico (piloto) | ✅ listo (27 preg.) | ✅ listo (84 preg.) | ✅ listo (48 preg.) | ✅ listo (36 preg.) | ✅ **listo (195 preg., 32/32 OA)** |
| 1° básico | ✅ listo (36 preg.) | ✅ listo (59 preg.) | ✅ listo (41 preg.) | ✅ listo (36 preg.) | ✅ **listo (172 preg., 10/10 OA Mat.)** |
| 2° básico | ✅ listo (28 preg.) | ✅ listo (84 preg.) | ✅ listo (48 preg.) | ✅ listo (48 preg.) | ✅ **listo (208 preg., 32/32 OA)** |
| 3° básico | ✅ listo (29 preg.) | ✅ listo (87 preg.) | ✅ listo (42 preg.) | ✅ listo (38 preg.) | ✅ **listo (196 preg., 29/29 OA)** |

**✅ Régimen A (1°-4° básico) completo: 771 preguntas de autoevaluación, 121/121 OA oficiales cubiertos, en las 4 asignaturas de los 4 cursos.**

## Régimen B (5° básico - 2° medio) — prueba separada, se agrega Inglés

| Curso | Lenguaje/Lengua | Matemática | Cs. Naturales | Historia/Geo/Cs. Sociales | Inglés | Estado curso |
|---|---|---|---|---|---|---|
| 5° básico | ✅ listo (42 preg.) | ✅ listo (102 preg.) | ✅ listo (42 preg.) | ✅ listo (55 preg.) | ✅ listo (32 preg.) | ✅ **listo (273 preg., 43/43 OA)** |
| 6° básico | ✅ listo (42 preg.) | ✅ listo (66 preg.) | ✅ listo (54 preg.) | ✅ listo (78 preg.) | ✅ listo (34 preg.) | ✅ **listo (274 preg., 44/44 OA)** |
| 7° básico | ✅ listo (42 preg.) | ✅ listo (72 preg.) | ✅ listo (49 preg.) | ✅ listo (78 preg.) | ✅ listo (36 preg.) | ✅ **listo (277 preg., 39/39 OA)** |
| 8° básico | ✅ listo (42 preg.) | ✅ listo (80 preg.) | ✅ listo (56 preg.) | ✅ listo (72 preg.) | ✅ listo (38 preg.) | ✅ **listo (288 preg., 40/40 OA)** |
| 1° medio | ✅ listo (48 preg.) | ✅ listo (56 preg.) | ✅ listo (70 preg.) | ✅ listo (78 preg.) | ✅ listo (38 preg.) | ✅ **listo (290 preg., 40/40 OA)** |
| 2° medio | ✅ listo (48 preg.) | ✅ listo (57 preg.) | ✅ listo (63 preg.) | ✅ listo (90 preg.) | ✅ listo (37 preg.) | ✅ **listo (295 preg., 40/40 OA)** |

**✅ Régimen B (5° básico - 2° medio) completo: 1.697 preguntas de autoevaluación, 246/246 OA oficiales cubiertos, en las 5 asignaturas de los 6 cursos.**

## Régimen C (3°-4° medio) — currículum 193/2019, asignaturas nuevas

| Curso | Lengua y Lit. | Matemática | Cs. Ciudadanía | Filosofía | Inglés | Educ. Ciudadana | Estado curso |
|---|---|---|---|---|---|---|---|
| 3° medio | ✅ listo (36 preg.) | ✅ listo (56 preg.) | ✅ listo (33 preg.) | ✅ listo (34 preg.) | ✅ listo (31 preg.) | ✅ listo (42 preg., 6/6 OA) | ✅ **listo (232 preg.)** |
| 4° medio | ✅ listo (33 preg.) | ✅ listo (54 preg.) | ✅ listo (33 preg.) | ✅ listo (32 preg.) | ✅ listo (32 preg.) | ✅ listo (33 preg.) | ✅ **listo (217 preg., 17/17 OA)** |

**✅ Régimen C (3°-4° medio) completo: 449 preguntas de autoevaluación, 41/41 OA oficiales cubiertos, en las 6 asignaturas de los 2 cursos.**

**🔧 Corrección de calidad (2026-08-10):** una auditoría encontró que 5 de las 12 asignaturas
de este régimen (Lengua y Literatura, Ciencias para la Ciudadanía, Filosofía x2, Inglés x2,
Educación Ciudadana) tenían menos preguntas por OA de lo esperado para este régimen (pocos OA
por asignatura, requieren más cobertura). Se engrosaron todas a **15 preguntas por OA**. El
total de preguntas del Régimen C subió de 449 a aproximadamente 555 (pendiente de recalcular
el total exacto consolidado).

## Pruebas por materia (formato real Mineduc: alternativas + preguntas abiertas + pauta de corrección) — HISTÓRICO

> **Histórico:** esta sección describe las 58 "pruebas por materia" originales, que fueron
> reemplazadas por las 156 pruebas de unidad el 2026-08-11. Se conserva como registro; el
> estado vigente es el de la sección de rediseño al inicio del documento.

Investigación en mineduc.cl confirmó el formato real: mezcla de alternativas (4 opciones) y
preguntas abiertas, con estímulo/contexto y una Pauta de Corrección final. Se está
construyendo una "prueba" de práctica por asignatura (`contenido/{curso}/pruebas/`),
reutilizando el banco de preguntas de autoevaluación ya existente.

| Curso | Estado |
|---|---|
| 1° básico | ✅ listo — 4/4 (Lenguaje 14, Matemática 17, Cs. Naturales 13, Historia 13) |
| 2° básico | ✅ listo — 4/4 (Lenguaje 16, Matemática 20, Cs. Naturales 15, Historia 15) |
| 3° básico | ✅ listo — 4/4 (Lenguaje 16, Matemática 20, Cs. Naturales 14, Historia 13) |
| 4° básico (piloto) | ✅ listo — 4/4 (Lenguaje 16, Matemática 22, Cs. Naturales 16, Historia 14) |
| **Régimen A** | **✅ completo — 16/16 pruebas** |
| 5° básico | ✅ listo — 5/5 (Lenguaje 25, Matemática 25, Cs. Naturales 25, Historia 25, Inglés 25) |
| 6° básico | ✅ listo — 5/5 (todas 25 preg.) |
| 7° básico | ✅ listo — 5/5 (todas 25 preg.) |
| 8° básico | ✅ listo — 5/5 (todas 25 preg.) |
| 1° medio | ✅ listo — 5/5 (todas 25 preg.) |
| 2° medio | ✅ listo — 5/5 (todas 25 preg.) |
| **Régimen B** | **✅ completo — 30/30 pruebas** |
| 3° medio | ✅ listo — 6/6 (todas 25 preg.) |
| 4° medio | ✅ listo — 6/6 (todas 25 preg.) |
| **Régimen C** | **✅ completo — 12/12 pruebas** |

## 🎓 PRUEBAS POR MATERIA: proyecto completo (los 12 cursos)

| Régimen | Cursos | Pruebas | Preguntas por prueba |
|---|---|---|---|
| A — integrada | 1°-4° básico | 16 (4 cursos × 4) | 12-22 (submuestra, examen real es integrado) |
| B — separada | 5° básico-2° medio | 30 (6 cursos × 5) | 25 exactas (match con examen real) |
| C — Plan Común | 3°-4° medio | 12 (2 cursos × 6) | 25 exactas (match con examen real) |
| **Total** | **12/12 cursos** | **58 pruebas** | — |

Cada prueba: formato real Mineduc (alternativas + preguntas abiertas, estímulo/contexto,
Pauta de Corrección con clave y referencia a OA), 100% contenido original (no copia
instrumentos reales de Mineduc, solo su formato — ver nota de propiedad intelectual en
`planificacion/05-tipos-de-contenido.md`).

## Exámenes tipo simulacro acumulativo

**✅ Régimen A completo (2026-08-10):** examen integrado real (20 preguntas mezclando las 4
asignaturas, tal como especifica el temario oficial), 2 formas por curso para variedad, en
`contenido/{curso}/examenes/examen-integrado-forma-a.md` y `-forma-b.md`.

| Curso | Estado |
|---|---|
| 1° básico | ✅ listo — Forma A y B (20 preg. c/u) |
| 2° básico | ✅ listo — Forma A y B (20 preg. c/u) |
| 3° básico | ✅ listo — Forma A y B (20 preg. c/u) |
| 4° básico (piloto) | ✅ listo — Forma A y B (20 preg. c/u) |

**⚠️ Régimen B y C — estado real:** el examen real de estos cursos es separado por
asignatura (25 preguntas c/u). En el producto existe **solo la Forma B** por asignatura:
42 archivos (Régimen B: 30, Régimen C: 12) en
`contenido/{curso}/examenes/{asignatura}-examen-forma-b.md`. Las antiguas "pruebas por
materia" que se habían pensado como Forma A fueron **reemplazadas por las pruebas de
unidad** (2026-08-11) y ese reemplazo no generó una Forma A de examen: **la Forma A de
Régimen B y C sigue pendiente de construir**.

## Auditoría pedagógica (2026-08-11) — ¿el material prepara realmente para aprobar?

Además de la auditoría de fidelidad curricular (contra los temarios), se hizo una segunda
auditoría con mirada de experto en educación chilena, evaluando si el material realmente
prepara a un niño/joven para aprobar, dado que **no hay segunda oportunidad si repruebas
dentro del mismo periodo** (ver `planificacion/07-experto-examenes-libres.md`). Veredicto
por régimen: **sí prepara**, con hallazgos concretos ya corregidos y algunos pendientes:

- **Corregido:** 3 casos donde la "Forma B" de un examen reciclaba literalmente los mismos
  textos/escenarios que la Forma A (Matemática 6° básico — mismo problema con otros números;
  Lenguaje 5° básico y Lenguaje del examen integrado de 4° básico — mismos cuentos/poemas).
  Esto le restaba valor real a tener "dos formas", ya que el alumno ya conocía el texto.
- **Riesgo conocido, no verificado en todos los archivos:** el patrón de "Forma B = mismo
  problema con otros números" podría repetirse en otras asignaturas de Matemática y Lenguaje
  no muestreadas por la auditoría (se revisaron 2-3 cursos por régimen, no los 12). Inglés e
  Historia mostraron buena variación genuina en las muestras revisadas. Recomendación: si se
  detecta el mismo patrón en otro curso, aplicar la misma corrección (reescribir con
  escenario distinto, no solo cifras distintas).
- **Mejoras sugeridas, no bloqueantes:** agregar una tercera forma de examen en asignaturas
  con pocos OA (mayor riesgo de "aprenderse las 25 preguntas"); incluir guía de manejo del
  tiempo por pregunta en las instrucciones; glosario acumulado en asignaturas nuevas sin
  precedente (Régimen C).

---

# 🎓 PROYECTO COMPLETO: los 12 cursos tienen contenido de estudio íntegro (guía + banco de
preguntas + pruebas de unidad + exámenes simulacro)

| Régimen | Cursos | Preguntas (banco) | OA cubiertos | Exámenes simulacro |
|---|---|---|---|---|
| A — prueba integrada | 1°-4° básico | 771 | 121/121 | 8 (2 formas × 4 cursos, integrado) |
| B — prueba separada + Inglés | 5° básico - 2° medio | 1.697 | 246/246 | 30 (solo Forma B) |
| C — Plan Común 193/2019 | 3°-4° medio | 449 | 41/41 | 12 (solo Forma B) |
| **Total** | **12/12 cursos** | **2.917** | **408/408** | **50 archivos de examen** |

Los 408 OA cubiertos coinciden exactamente con el total de Objetivos de Aprendizaje extraídos
en el análisis inicial de los 12 temarios oficiales (`Temarios/analisis/00-resumen-general.md`)
— confirma que no quedó ningún OA oficial sin cubrir.

Cada curso/asignatura tiene: explicación pedagógica por OA, ejemplos o actividades resueltas,
y un banco de preguntas de autoevaluación con retroalimentación, alineado a los Indicadores de
Evaluación oficiales del Mineduc/UCE. Ver `planificacion/04-modo-de-operacion.md` para el
criterio de "materia lista" aplicado.

**Siguiente paso natural (fuera de esta etapa de planificación):** con la materia lista, el
proyecto puede pasar a la fase de desarrollo de la aplicación (Etapa 1+ del roadmap en
`planificacion/03-roadmap-etapas.md`), empezando por el MVP del curso piloto (4° básico).

Leyenda: ⏳ pendiente · 🔄 en progreso · ✅ listo (cumple los 4 criterios de "materia lista")
