# Continuidad del trabajo — Logos School

**Para quién:** cualquier agente (Devin, Claude u otro) o persona que retome el trabajo sin acceso a
conversaciones anteriores. Este archivo es el **punto de entrada único**: dice qué es el proyecto, qué
reglas puso el dueño, cómo verificar, en qué estado está todo y qué sigue, paso a paso.

**Última actualización:** 2026-11-16 · **Último commit de referencia:** ver `git log -1`.
**Regla de mantenimiento:** cada vez que se termina una tarea, actualizar la sección 5 (estado) y la
sección 6 (pendientes) de este archivo **en el mismo commit**.

---

## 1. Qué es el proyecto

Plataforma web de estudio para niños, niñas y adolescentes que rinden los **Exámenes Libres de
Validación de Estudios** del Mineduc (Chile), de 1.° básico a 4.° medio. Nombre de marca: **Logos
School** (usarlo completo en todo texto visible al usuario).

- `contenido/` — el material, en Markdown: por curso, una **guía** por asignatura (`contenido/NN-curso/*.md`),
  **pruebas de unidad** (`pruebas/`) y **simulacros** de examen (`examenes/`). 265 archivos, 6.181 preguntas.
- `Temarios/` — los 12 temarios oficiales en PDF (fuente de verdad curricular); `Temarios/analisis/` los resume.
- `backend/` — FastAPI (arquitectura hexagonal) + PostgreSQL. `backend/scripts/importar_contenido.py`
  carga `contenido/` en la base usando `parser_contenido.py` (guías) y `parser_prueba_examen.py` (pruebas/simulacros).
- `frontend/` — Angular. Pruebas E2E con Playwright en `frontend/e2e/`.
- `docs/auditorias/` — registros de la auditoría (ver sección 7).

## 2. Reglas del dueño del proyecto (obligatorias)

1. **Responder y documentar en español.**
2. **No desplegar** a producción (Neon, Render, Cloudflare, etc.) hasta que el dueño lo pida.
3. Trabajar en la rama **`main`**; las funcionalidades nuevas grandes van en ramas `feature/*`.
4. **No pedir confirmaciones sí/no**: decidir con criterio y luego informar.
5. Hacer commit y push del avance como checkpoint. Terminar cada mensaje de commit con la línea de coautoría del agente que trabaja (en esta etapa se usó `Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>`).
6. **Sin servicios pagados.** Las claves de API van solo en `.env` (nunca en el chat ni en el repo).
7. A APIs externas solo se envía **texto de contenido**, nunca datos de alumnos.
8. **Todo el material es de preguntas cerradas**: alternativas (una correcta), «varias correctas» (todas o nada)
   y verdadero/falso. **No reintroducir preguntas de desarrollo.** Las abiertas originales están en `docs/banco-preguntas-abiertas/`.
9. Prioridad vigente: **Fase 1** (auditar el material en archivos contra los temarios) → **Fase 2** (aplicar a la
   app y validar en 3 navegadores) → mejoras.
10. Validación: **Chromium** basta para cambios de contenido; **los 3 navegadores** para cambios de interfaz o al cerrar una etapa.
11. Público menor de edad: cuidado explícito con datos personales, privacidad y contenido sensible.

## 3. Entorno y comandos

Requisitos usados: Python 3.14 (`backend/.venv`), PostgreSQL 16, Node 22, Playwright (`frontend/node_modules`).
Los scripts de `scripts/qa/` son **zsh** y asumen macOS; en Linux, instalar zsh o traducir los pasos (son cortos).
`backend/.env` (copiar de `backend/.env.example`) debe tener `DATABASE_URL` hacia un Postgres local.

| Paso | Comando (desde la raíz) | Qué hace |
|---|---|---|
| Reimportar base aislada | `scripts/qa/reimportar_e2e.sh` | Recrea la base `logos_e2e_alternativas` desde `contenido/`, siembra datos, exporta el fixture E2E y levanta la API en el puerto 8001. Debe terminar con `preguntas sin OA: 0 de 6181`. |
| Levantar la web | `scripts/qa/levantar_spa.sh` | Compila Angular contra la API 8001 y la sirve en 4300. |
| Validar material en la app | `scripts/qa/validar_material.sh "3° medio"` (o sin argumentos, los 12) | Playwright recorre guías, pruebas y simulacros y marca cada clave. `NAVEGADORES=todos` usa Chromium, Firefox y WebKit. Tarda ~1,5 min por curso. |
| Pruebas backend | `cd backend && .venv/bin/python -m pytest -q` | ~6 min; incluye las guardas del corpus. |
| Validador del Markdown | `backend/.venv/bin/python backend/scripts/validar_evaluaciones_markdown.py` | Debe decir «Sin discrepancias». |
| Copias de la guía (C.2) | `backend/.venv/bin/python backend/scripts/solapamiento_pruebas_guias.py [NN-curso]` | Exactas, casi copias y lecturas copiadas: todo debe ser 0. |
| Explicaciones vacías (C.4) | `cd backend && .venv/bin/python scripts/explicaciones_pobres.py` | Debe decir 0. |
| Lecturas desconectadas | `cd backend && .venv/bin/python scripts/estimulos_huerfanos.py` | Lecturas que no llegan a ninguna pregunta. |

**Suite E2E completa (no solo el material):** algunas pruebas (`plan-estudio-atrasada.spec.ts` y otras que usan
`ejecutarSqlPrueba`) modifican la base por SQL y, por seguridad, solo aceptan `LOGOS_E2E_DATABASE_URL` apuntando a
`logos_auditoria_test` en localhost. Para correrlas hay que importar el contenido en esa base y levantar la API contra ella
(adaptar `reimportar_e2e.sh` cambiando el nombre de la base). En el entorno `logos_e2e_alternativas` fallan por diseño.

**No tocar la base `logos_qa`** (es la del dueño para probar a mano en 4200/8000) sin antes respaldarla con `pg_dump`
en `~/Documents/Logos-respaldos/`.

**Antes de cada commit de contenido:** validador sin discrepancias → `pytest -k "parser or corpus or contenido or importar"`
en verde → reimportar → `validar_material.sh` del curso tocado en verde.

## 4. Cómo está escrito el material (lo mínimo para editarlo sin romperlo)

- **Pregunta:** `**N. (Alternativas)** enunciado` (también `**Pregunta N.**`, `N. *(…)*`), seguida de `a) … b) …`.
  La etiqueta define el tipo: «Verdadero o falso», «Varias correctas» (con «Marca **todas** las correctas»).
- **Pauta** al final, en tabla `| N | … |` o lista `N. …`. La primera letra/alternativa es la clave; **el resto de la línea es la
  explicación que ve el alumno** en el resumen final (no dejarla vacía: hay una guarda en pytest).
- **Lecturas compartidas:** una línea `*(Lee el texto y responde las preguntas 1 a 5.)*` (o `Lee … preguntas X a Y`) antes del
  texto citado con `>`. Sin esa línea, el texto no llega a las preguntas en la app.
- **OA de cada pregunta de prueba:** `oa_por_pregunta` en el frontmatter (JSON). Mantenerlo al reescribir.
- **Marcadores visuales** que la app dibuja: `::barras::`, `::linea::`, `::circular::`, `::caja::`, `::mapa::…`, `::contar::`,
  `::emoji::`, `::dibujo::`, `::fila::`, `::largo::`, `::posicion::`, etc. (ver `frontend/src/app/shared/graficos.ts`, `mapas.ts`).
- Tablas, citas y títulos **dentro** de una pregunta se conservan como bloques (parser corregido el 2026-11-15).

**Herramientas de edición asistida:** `backend/scripts/herramientas_auditoria/README.md` (`ver`, `explicar`, `rehacer`).
Verifican con el parser antes de escribir y conservan la letra de la clave, para no crear sesgos de posición.

## 5. Estado actual (Fase 1 — auditoría del material)

| Control | Estado |
|---|---|
| Cobertura de los 408 OA de los temarios | ✅ |
| Formato de los 50 simulacros (preguntas y duración) | ✅ |
| Indicadores de evaluación cubiertos | ✅ ~97 % (vacíos listados en `docs/auditorias/fase1/correcciones-propuestas.md`) |
| C.1 / C.2 — pruebas y simulacros no repiten la guía (exactas, casi copias, lecturas) | ✅ 0 en los 12 cursos (guarda en pytest) |
| C.3 — cada OA aparece en algún simulacro | ✅ al límite del formato (ver `fase1/00-ESTADO-FASE1.md`) |
| C.2 tercera pasada — «misma pregunta y clave» y «escenario repetido» | ✅ 0 en los 12 cursos (guarda en pytest) |
| C.4 — toda pregunta explica su clave | ✅ 0 vacías (guarda en pytest) |
| C.4b — retroalimentaciones de guía que explican la respuesta | ✅ 260 reescritas (guarda en pytest) |
| C.4c — explicaciones de pruebas no genéricas | ✅ 50 reescritas (guarda en pytest) |
| C.5 — sin sesgo de posición en «varias correctas» | ✅ 256 rotadas (guarda: ningún patrón > 30 %) |
| C.6 — sin sesgo de longitud | ✅ 528 corregidas; 3 excepciones de citas textuales (guarda en pytest) |
| Letra de la clave y V/F | ✅ equilibradas (alternativas 23–29 % por letra en pruebas y guías) |
| Defectos de texto en pautas (letras falsas, huérfanas, «Retroalimentación:», títulos en estímulos) | ✅ corregidos (guardas en pytest) |
| Solo preguntas cerradas; instrucciones sin «desarrollo» | ✅ |
| Tablas/citas se ven bien en la app | ✅ (Chromium 12/12; 3 navegadores en 1.° básico y 3.° medio) |
| B — gráficos y mapas dibujados | ✅ (mapas de otras regiones pendientes, ver 6.4) |
| D — 21 marcadores `[Imagen: …]` en 1.° a 3.° básico (contados 2026-11-16) | ⏳ **espera decisión del dueño** sobre la fuente de las ilustraciones |
| Revisión docente por muestreo | ⏳ muestra regenerada y revisada por mí en los 12 cursos (lo hallado, corregido); falta un profesor |
| Control 6 — tag Git «material aprobado» | ⏳ pendiente |

Detalle histórico y hallazgos: `docs/auditorias/AUDITORIA_MAESTRA.md` §15.35–15.40.

## 6. Pendientes, en orden (con pasos)

### 6.1 ✅ Defecto de horario (resuelto 2026-11-15)
Las fechas de calendario (hoy, esta semana, sesión atrasada) se calculaban en UTC. Ahora el backend usa
`app/domain/shared/fechas.py` → `fecha_local()` (zona `America/Santiago`) en todos los routers y casos de uso, y el
frontend usa `Intl.DateTimeFormat(…, { timeZone: 'America/Santiago' })` en `plan-estudio.ts`. Las marcas de tiempo se
siguen guardando en UTC. Dependencia `tzdata` agregada. Prueba: `tests/test_fechas_chile.py`. **Regla para código nuevo:
nunca usar `.date()` sobre un instante ni `toISOString().slice(0, 10)` para «hoy»; usar `fecha_local`.**

### 6.1b ✅ RESUELTO (2026-11-16) — C.2, tercera pasada: «misma pregunta y misma clave»
La revisión de la muestra docente mostró casi copias que los criterios anteriores no veían (enunciado reformulado,
un `[Imagen: …]` agregado, o los mismos datos del «Ejemplo 1» de la guía). `solapamiento_pruebas_guias.py` ahora informa
«misma pregunta y clave» (≥ 0,6 de similitud, 3 o más alternativas iguales y la misma respuesta correcta) y
«escenario de la guía repetido» (una oración de situación o con datos, de 50 o más caracteres, idéntica a la guía).
Se revisaron las ~221 candidatas de los 12 cursos: **140 preguntas rehechas** (incluidos un cuento copiado en 1.° básico,
un artículo nuevo en el simulacro B de 2.° básico y un gráfico propio en Medición de 4.° básico) y **unas 90 plantillas**
registradas, con comentario, en `REVISADAS_A_MANO`. Los 12 cursos dan 0 en los seis reportes, y la guarda
`test_pruebas_y_simulacros_no_repiten_la_guia` ahora exige también `misma_clave` y `escenarios_copiados`.
**Sesgo de longitud:** las rehechas que dejaban la correcta notoriamente más larga (41) se corrigieron alargando
distractores con `ajustar_distractores.aplicar_en` (sin tocar la clave); 0 rehechas sesgadas.
Verificación: backend 734 pasan, `validar_evaluaciones_markdown.py` sin discrepancias, C.4 en 0, Chromium en los 12
cursos (18/18 en 1.° a 4.° básico, 24/24 en 5.° básico a 2.° medio, 25/25 en 3.° medio y 23/23 en 4.° medio).
**Cómo decidir cada una** (con `match.match(archivo, n)` de `herramientas_auditoria`):
- **Copia → rehacer** (`rehacer(...)`) si pregunta lo mismo con los mismos datos o la misma situación: misma flor, misma palabra,
  mismos números de la tabla o del pictograma, misma opción correcta por la misma razón.
- **Plantilla válida → `REVISADAS_A_MANO`** (en el detector) si cambian los datos y la respuesta coincide por casualidad, o si
  pregunta por otro personaje u otro texto con alternativas genéricas (por ejemplo, «¿a qué personaje tipo corresponde…?»).
Regla para material nuevo: si el detector marca una pregunta, decidir con este mismo criterio; si es plantilla, registrarla
en `REVISADAS_A_MANO` con un comentario que diga qué cambia; y revisar el sesgo de longitud de toda pregunta rehecha.

### 6.1c ✅ RESUELTO (2026-11-16) — C.4b: retroalimentaciones de GUÍA que no explican la respuesta
Al revisar la muestra docente aparecieron retroalimentaciones de guía de «reflexión» que no dicen por qué la respuesta es
correcta («Cada fenómeno óptico tiene una explicación física específica.»). Detector: `backend/scripts/retro_guia_pobres.py
[curso]` (heurística: la retroalimentación no comparte ninguna raíz de palabra con la respuesta correcta; 374 candidatas
al empezar, con falsos positivos). Flujo por curso, desde `backend/`:
```
.venv/bin/python -c "import sys; sys.path[:0]=['scripts/herramientas_auditoria','scripts']; from retro_guia import ver; ver('03-basico')"
.venv/bin/python -c "import sys; sys.path[:0]=['scripts/herramientas_auditoria','scripts']; from retro_guia import cambiar; cambiar('03-basico/x.md', 'inicio de la retro actual', 'Texto nuevo que explica.')"
```
- Si **no explica** → `cambiar(...)`: explicar por qué la clave es correcta (y, si cabe, el error de un distractor típico).
- Si **sí explica con otras palabras** → agregar `(archivo, inicio del enunciado)` a `REVISADAS_A_MANO` del detector.
Cerrado en los 12 cursos: **260 retroalimentaciones reescritas** y 116 revisadas como válidas. Guarda en pytest:
`test_las_retroalimentaciones_de_guia_explican_la_respuesta`. Material nuevo: misma regla (explicar por qué la clave es correcta).

### 6.1d ✅ RESUELTO (2026-11-16) — C.4c: explicaciones de PRUEBAS y SIMULACROS genéricas
La revisión de las muestras mostró explicaciones de pruebas que no explican la clave («La sostenibilidad tiene dimensiones
técnica, económica y social.»). C.4 solo detectaba las que repiten la clave. Medición (2026-11-16): unas 298 candidatas
(la explicación, sin el «x) clave.» inicial, no comparte raíces con la clave), con muchos falsos positivos. Método: igual que
C.4b (detector + `REVISADAS_A_MANO` + reescritura con verificación de que cambió la pregunta buscada); para reemplazar
una explicación de prueba, `rehacer(..., solo_explicacion=True)` (ver README de herramientas). Cerrar con guarda en pytest.
Detector: `backend/scripts/explicaciones_genericas.py [curso]` (258 candidatas al empezar). Cerrado en los 12 cursos: **50 explicaciones reescritas** (incluidas 11 de 4.° medio que eran solo «a, b y c.») y 209
revisadas como válidas. Guarda: `test_las_explicaciones_de_pruebas_no_son_genericas`. `explicaciones_pobres.py` (C.4) ahora
detecta también explicaciones de solo varias letras.

### 6.1e ✅ RESUELTO (2026-11-16) — C.5: sesgo de posición en «varias correctas»
El 46 % de las «varias correctas» de pruebas y simulacros tenía a, b y c correctas y la última incorrecta (igual en guías),
y la app baraja preguntas pero **no** alternativas. Herramienta: `backend/scripts/herramientas_auditoria/reordenar_varias.py`
(rota las alternativas, actualiza las letras de la clave y verifica con el parser que no cambien respuestas, enunciado ni
explicación). Rotadas 256; saltadas 12 que mencionan letras en su explicación u opciones (4.° medio, simulacros de Ciencias
para la Ciudadanía, Educación Ciudadana y Lengua; 8.° básico Inglés U2 14) o cuyo formato no se reconoció (7.° básico guía
OA 5 #3, prueba de Biología 10; 6.° básico simulacro de Ciencias 25). Guarda: `test_varias_correctas_sin_sesgo_de_posicion`
(ningún patrón > 30 %). Material nuevo: no poner siempre las correctas primero.

### 6.1f ✅ RESUELTO (2026-11-16) — C.6: sesgo de longitud reintroducido por las reescrituras de C.2
El 2026-11-06 (§15.24) el sesgo de longitud quedó casi en 0. Las reescrituras posteriores de C.2 (1.277 preguntas)
lo reintrodujeron: al 2026-11-16 hay **495 de 2.570** preguntas de alternativas de pruebas y simulacros donde la correcta
es claramente la más larga (criterio `ajustar_distractores.sesgada`), y 33 en guías. Por curso (evaluaciones): 1.° básico 8,
2.° 15, 3.° 20, 4.° 30, 5.° 34, 6.° 35, 7.° 34, 8.° 70, 1.° medio 53, 2.° medio 60, 3.° medio 79, 4.° medio 57.
Método: alargar distractores con errores plausibles (sin tocar la clave) con `ajustar_distractores.aplicar_en(ruta, [D(n,
{'a': '…'})], estricto=True)`; listar con `python scripts/ajustar_distractores.py listar <archivo>`. Empezar por 4.° básico
(curso piloto). Al terminar, guarda en pytest (umbral bajo, p. ej. ≤ 2 %).
Cerrado: **495 alternativas de evaluaciones y 33 de guías corregidas** (distractores alargados con errores plausibles, sin
tocar la clave). Quedan 3 excepciones legítimas (las alternativas son citas textuales: versos o frases del texto), listadas en
la guarda `test_alternativas_sin_sesgo_de_longitud`. Pendientes en el futuro: `backend/scripts/herramientas_auditoria/
sesgo_longitud_pendientes.py "<curso>/pruebas/*.md"`. Al alargar distractores, correr también el detector de copias (C.2):
en 3.° medio un distractor alargado quedó idéntico al de la guía.

### 6.2 Revisión de fondo propia (mientras no haya profesor)
Leer la muestra `docs/auditorias/fase1/muestra-docente/NN-curso.md` y aplicar los 5 criterios de `00-INSTRUCCIONES.md`.
Corregir con `rehacer`/`explicar` lo que falle y registrar en AUDITORIA_MAESTRA. La muestra se regeneró el 2026-11-16
(`backend/scripts/muestra_revision_docente.py`). Revisadas las 12 muestras (2026-11-16); lo encontrado quedó corregido (ver AUDITORIA_MAESTRA §15.40). Sigue pendiente la revisión por un profesor real.

### 6.3 D — imágenes (requiere decisión del dueño)
`grep -rn "\[Imagen" contenido/0[1-3]-basico` lista los 32 casos. Opciones a proponer al dueño: dibujos SVG propios,
marcadores `::emoji::`/`::dibujo::` existentes, o ilustraciones generadas. No elegir sin él.

### 6.4 Mapas de otras regiones (6.° y 7.° básico)
`frontend/src/app/shared/mapas-datos.ts` solo tiene `america`, `sudamerica` y `chile`
(generados por `scripts/mapas/generar_mapas.py` desde Natural Earth). Faltan Europa/Mediterráneo y Mesoamérica para Historia.

### 6.5 Cierre de Fase 1
1. Validación en los 3 navegadores de los 12 cursos (`NAVEGADORES=todos scripts/qa/validar_material.sh`).
2. Regenerar audios de lectura en voz alta (solo 1.° a 4.° básico, régimen A): `DATABASE_URL=<base con el contenido final> scripts/voz/generar_audios.sh`. Usa Kokoro (gratis, local; la primera vez descarga ≈350 MB en `~/.cache/logos-voz`) y solo genera los que faltan; con la lista completa de niveles, `LIMPIAR_HUERFANOS=1` borra los de textos que ya no existen. Salida en `frontend/public/audio/es/` (no versionada).
3. Recargar `logos_qa` del dueño con el contenido final (respaldo antes).
4. Tag Git `material-aprobado-AAAA-MM-DD` con un informe breve por curso.

### 6.6 Fase 2 y mejoras (después)
Ver la tabla de tareas de `docs/auditorias/COLA-TRABAJO-AUTONOMO.md` (accesibilidad con axe, juegos de práctica,
tutor IA detrás de variable de entorno, pasarela de pago detrás de variable de entorno) y `docs/PENDIENTES-USUARIO.md`
(cuentas y claves que debe crear el dueño).

## 7. Dónde registrar cada avance

| Archivo | Qué va ahí |
|---|---|
| **este archivo** | Estado y pendientes vigentes (siempre al día). |
| `docs/auditorias/AUDITORIA_MAESTRA.md` §15.x | Hallazgos y correcciones con detalle (agregar una sección nueva por bloque de trabajo). |
| `docs/auditorias/COLA-TRABAJO-AUTONOMO.md` → Bitácora | Una línea por sesión: qué se hizo y qué sigue. |
| `docs/auditorias/fase1/00-ESTADO-FASE1.md` | Tabla de controles de la Fase 1. |

## 8. Lecciones (trampas ya pisadas)

- **Un control que da 0 puede estar ciego.** El detector de copias comparaba la pregunta junto con su lectura y nunca coincidía;
  se corrigió para comparar solo la pregunta. Antes de declarar algo cerrado, probar el control con un caso conocido.
- **Verificar antes de escribir.** Un ayudante guardaba el archivo antes de validar; se corrigió. Revisar con `git diff` tras cada lote.
- **Las pruebas de regresión fijan textos literales.** Al reescribir material, algunas pruebas de `backend/tests/test_parser_prueba_examen.py`
  fallan: actualizarlas conservando lo que verifican (no borrarlas).
- **Fechas y datos:** comprobar los hechos (por ejemplo, Chile firmó la Convención sobre los Derechos del Niño en 1990; el voto
  municipal femenino es de 1934 y se ejerció en 1935). Las cifras inventadas deben declararse ficticias.
- **Coherencia entre instrumentos:** un texto nuevo no debe repetir el de otra prueba o simulacro del mismo curso.
- **Mantener la letra de la clave** al reescribir, para no desbalancear la posición de las respuestas correctas.
- **`rehacer` toma como clave la opción que quede en la letra original.** Si pones la correcta en otra letra, la clave
  queda FALSA y `rehacer` dice «ok». Pasó dos veces (2026-11-16). Ahora, si la explicación empieza con «x)», `rehacer`
  verifica esa letra y aborta si no coincide; y la guarda `test_la_explicacion_no_contradice_ni_repite_la_letra_de_la_clave`
  lo revisa en todo el material. Escribe la explicación sin repetir «x) clave»: `rehacer` ya la antepone.
- **`rehacer` dejaba restos del texto anterior** cuando la entrada de pauta ocupaba varias líneas (solo reemplazaba la
  primera). Corregido: ahora reemplaza la entrada completa y verifica que la pauta termine en la explicación nueva.
  Guardas: `test_la_pauta_no_tiene_restos_huerfanos_de_explicaciones_anteriores` y
  `test_la_explicacion_no_incluye_la_etiqueta_retroalimentacion`.
- **Al limpiar texto con expresiones regulares, mirar lo que queda:** una limpieza quitó el sujeto de 5 explicaciones
  («El petróleo. tardó…»). Revisar siempre una muestra del `git diff` y buscar oraciones que empiecen en minúscula.
- **Dos textos pueden empezar igual.** `retro_guia.cambiar` reemplazó una vez la retroalimentación de otra pregunta que
  compartía las primeras palabras; ahora exige una ubicación única y verifica que cambió la pregunta buscada.
- **Revisar el sesgo de longitud de lo rehecho:** la correcta tiende a quedar más larga y detallada. Medir con
  `ajustar_distractores.sesgada` y alargar distractores con `aplicar_en` (sin tocar la clave).
