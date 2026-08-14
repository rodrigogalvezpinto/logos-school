---
título: Sistema de QA automatizado — qué existe, qué cubre, cómo usarlo
estado: construido y verificado (2026-08-14)
---

## Por qué existe este documento

El usuario pidió, después de una larga sesión de pruebas manuales encontrando bugs uno por
uno: *"necesito que crees algo que me solucione el tener que estar yo probando"*. Antes de
construir nada se hizo un análisis explícito (ver conversación del 2026-08-14) de qué existía
y qué haría falta para un QA autónomo y exhaustivo con tres dimensiones — funcional/técnico,
roles y permisos, y coherencia del contenido educativo. Este documento registra qué se
construyó, con qué alcance real, y cómo se usa de acá en adelante.

## Qué se construyó

### 1. Matriz de permisos automática — `backend/tests/test_matriz_permisos.py`

No es una lista de casos escritos a mano. Lee `app.routes` en tiempo real (el árbol de
dependencias de FastAPI de cada endpoint) y genera un caso por cada ruta protegida:

- **Sin ningún token → debe dar 401/403.**
- **Con un token de un tipo de cuenta distinto al exigido (Apoderado/Profesor/Admin) →
  debe dar 401/403.**
- **Toda ruta sin ningún guardia de sesión debe estar en una lista blanca explícita**
  (`RUTAS_PUBLICAS_A_PROPOSITO`, con el motivo de por qué es pública) — si no está ni
  protegida ni en la lista blanca, el test falla solo, sin que nadie tenga que acordarse de
  agregar un caso.

**Por qué importa**: nació de un bug de seguridad real encontrado exactamente así —
`/evaluaciones/*` (iniciar, responder y entregar una prueba) no tenía NINGUNA autenticación.
Cualquiera, sin sesión, podía responder o entregar la evaluación de cualquier alumno
adivinando su id. Ninguna prueba manual lo había encontrado en toda la sesión, porque el
frontend siempre manda un token válido — hacía falta mirar el grafo de dependencias, no un
flujo de usuario real. Ya corregido (los 5 endpoints ahora exigen que el `perfil_alumno_id`,
directo o a través del `intento_id`, pertenezca a la cuenta autenticada) y cubierto por 81
casos generados automáticamente + 2 tests específicos de la regla de propiedad.

Se ejecuta con el resto del backend: `cd backend && uv run pytest -q`.

### 2. QA semántico de contenido — `backend/scripts/qa_extraer_para_coherencia.py`

Extrae de la base de datos, para un curso dado, cada pregunta vinculada a su Objetivo de
Aprendizaje (guía + enunciado + alternativas + respuesta correcta + retroalimentación), en un
JSON agrupado por asignatura y OA, listo para que un revisor (Claude, en una sesión de
trabajo, o un humano) juzgue coherencia semántica — algo que ningún test tradicional puede
hacer, porque requiere criterio, no comparación de strings.

```
cd backend
uv run python scripts/qa_extraer_para_coherencia.py --listar-niveles
uv run python scripts/qa_extraer_para_coherencia.py "4° básico" > /tmp/qa_4basico.json
```

**Prueba real ya hecha (2026-08-14)**: se corrió sobre el curso piloto completo — 4° básico,
195 preguntas, 32 OA, 4 asignaturas — revisando cada guía contra cada pregunta, alternativa,
respuesta correcta y retroalimentación. Encontró **3 bugs sistemáticos de parsing** (no de
contenido pedagógico — el contenido en sí resultó factualmente correcto y coherente en las
195 preguntas revisadas):

1. **Emoji "✅" pegado a una alternativa incorrecta**: en todo el archivo de Historia,
   Geografía y Cs. Sociales, el marcador "✅ Respuesta correcta:" del `.md` fuente dejaba el
   ✅ pegado a la ÚLTIMA alternativa listada (casi siempre la incorrecta), porque
   `RE_RESPUESTA_MARCA` era el único de los tres regex de marcador que no toleraba un emoji
   de prefijo (`RE_RETRO_MARCA` y `RE_PAUTA_MARCA` sí, desde un fix anterior). Un alumno
   viendo esa pregunta habría visto un check ✅ junto a una alternativa incorrecta.
2. **Glosario final pegado a la retroalimentación de la última pregunta**: el parser no
   reconocía el heading `## Glosario` como cierre del bloque de preguntas, así que todo el
   glosario (15-20 términos) quedaba pegado al campo `retroalimentacion` de la última
   pregunta de cada asignatura.
3. **Preguntas de alternativas reales mostradas como texto libre**: preguntas rotuladas con
   una etiqueta distinta a "(Alternativas)" (ej. "(reconocer la operación)") pero con
   opciones a)/b)/c)/d) reales en el cuerpo quedaban clasificadas como `desarrollo_breve` —
   el alumno nunca veía las alternativas, y la "respuesta esperada" mostrada era un
   fragmento sin sentido como `"b) Sustracción"`.

Los tres, corregidos en `parser_contenido.py` con tests de regresión
(`test_parser_contenido.py`, 8/8) y aplicados a los 12 cursos completos reimportando el banco
de autoevaluación y las pruebas/exámenes desde los archivos fuente (scripts ya existentes:
`reimportar_banco_autoevaluacion.py` + `reimportar_pruebas_y_examenes.py`). Verificado
después de la reimportación: 0 casos de los 3 patrones en 4° básico completo.

**Alcance real, sin adornar**: se revisó a fondo un curso completo (4° básico) como prueba de
que la herramienta funciona y tiene valor real — no los 12 cursos completos (serían más de
6.000 preguntas, un esfuerzo de varias sesiones). El fix del parser es global (aplica a los
12 cursos al reimportar), pero la revisión semántica línea por línea de los otros 11 cursos
queda pendiente de correr — la herramienta ya está lista para eso, ver "Cómo seguir" abajo.

### 3. Runner único — `scripts/qa_completo.sh`

Un solo comando que corre, en orden, todo lo que antes había que acordarse de correr a mano:

```
./scripts/qa_completo.sh
```

1. Backend: `pytest` completo (incluye la matriz de permisos).
2. Frontend: build de producción (atrapa errores de compilación/tipos).
3. Frontend: suite Playwright E2E completa, contra el backend real.

Requiere que `uvicorn` (puerto 8000) y `ng serve` (puerto 4300) ya estén corriendo — no los
levanta él mismo, para no cortar el flujo de desarrollo normal con `--reload`. Termina con un
resumen de una línea por etapa y código de salida 0/1 (listo para un futuro pipeline de CI).

## Qué NO resuelve este sistema (alcance honesto)

Del análisis de las 3 dimensiones pedidas (funcional/técnico, roles y permisos, coherencia de
contenido) más la de "descubrimiento autónomo":

- **No hay un crawler que descubra páginas/botones/forms solos.** Con ~40-50 páginas y rutas
  conocidas, seguir extendiendo Playwright a mano (como se hizo toda esta sesión, con 6 bugs
  reales de seguridad/datos encontrados) tiene mejor costo/beneficio que construir un agente
  de descubrimiento genérico — reconsiderar si la app crece a cientos de páginas.
- **La revisión semántica de contenido no es un test automático que corra en cada `pytest`**:
  requiere razonamiento (de Claude o de un humano), no una aserción. Se corre como una tarea
  puntual con `qa_extraer_para_coherencia.py` + revisión, no como parte de `qa_completo.sh`.
- **No hay scoring de cobertura de contenido** más allá de "preguntas revisadas ÷ preguntas
  totales" — hoy: 195/~2.900 (4° básico completo, el resto pendiente).

## Cómo seguir (para la próxima sesión)

1. Correr `qa_extraer_para_coherencia.py` para cada uno de los 11 cursos restantes y hacer la
   misma revisión semántica que se hizo con 4° básico — es mecánico, solo toma tiempo.
2. Si se agrega un endpoint nuevo con datos sensibles, la matriz de permisos avisa sola si
   falta el guardia de sesión — no hace falta acordarse de nada extra, solo dejar que
   `test_matriz_permisos.py` corra con el resto del suite.
3. Si el proyecto crece a un tamaño donde ya no es viable conocer el mapa de la app de
   memoria, ahí sí vale la pena reconsiderar un crawler/agente de descubrimiento autónomo
   (opción D del análisis original) — hoy no es el cuello de botella.
