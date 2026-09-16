---
título: Plan de pruebas exhaustivo — QA con Playwright, casos felices y de borde
estado: inventario verificado (2026-08-16), ejecución en curso
---

## Por qué existe este documento

El usuario pidió, después de cerrar el nivel local de funcionalidad, un plan de pruebas
**exhaustivo** — casos felices, casos borde, casos de error — usando metodología de QA y
Playwright como herramienta de ejecución. Antes de escribir un solo caso nuevo se hizo un
inventario real de lo que ya existe (no se asumió nada): **30 archivos Playwright en
`frontend/e2e/`** y **33 archivos de test en `backend/tests/`**, leídos uno por uno. Este
documento es ese inventario, organizado por módulo, con los casos felices/borde/error que ya
están cubiertos, los que faltan de verdad, y el orden en que se van a cerrar.

Ver también `planificacion/26-qa-sistema-automatizado.md` (la infraestructura de QA ya
construida: matriz de permisos automática, QA semántico de contenido, `qa_completo.sh`) — este
documento no la repite, la complementa con la vista "caso por caso" que faltaba.

## Metodología

Cada módulo se evalúa en 4 dimensiones:

1. **Casos felices** — el flujo principal funciona con datos válidos.
2. **Casos borde** — límites (vacío, máximo, mínimo, duplicado, concurrente, fecha límite).
3. **Casos de error** — datos inválidos, recursos inexistentes, estados ilegales.
4. **Seguridad/permisos** — sin sesión, sesión de otro tipo de cuenta, acceso a datos ajenos.

La ejecución real es con Playwright (frontend, contra el backend real, no mocks — ver
`playwright.config.ts`) y `pytest` (backend, con `TestClient` de FastAPI contra Postgres real
de test). El comando único ya existe: `./scripts/qa_completo.sh`.

**Convención de la tabla**: 🟢 cubierto y verificado · 🟡 cubierto parcialmente (falta un caso
concreto, se detalla) · 🔴 gap real, no cubierto.

## Matriz por módulo

### Autenticación y cuentas (Apoderado)

| Dimensión | Estado | Detalle |
|---|---|---|
| Felices | 🟢 | Registro, login, logout, "yo" (`test_auth.py`, `flujos-principales.spec.ts`) |
| Borde | 🟢 | Email insensible a mayúsculas, logout no afecta otras sesiones, re-login tras logout |
| Error | 🟢 | Registro duplicado, password incorrecta, correo inexistente (mismo mensaje que password — no filtra qué existe), fecha de nacimiento futura, RUT inválido, RUT duplicado entre apoderados distintos, nivel inexistente |
| Seguridad | 🟢 | `/auth/yo` sin token, listar alumnos solo trae los propios |
| **Gap real** | 🔴 | **Rate limiting nunca se prueba.** `POST /auth/login` (5/min) y `/auth/registro` (10/min) tienen `@limiter.limit(...)` en el código pero cero test verifica que un 6° intento de login en el mismo minuto de verdad devuelva 429. Es un control de seguridad real (fuerza bruta) sin cobertura. |
| **Gap real** | 🔴 | Login con Google (`IniciarSesionConGoogle`) no tiene ningún test — ni el caso feliz ni "Google no configurado". Bajo impacto hoy porque no hay credenciales reales de Google en ningún ambiente, pero el código existe y no está probado. |

### Perfiles de Alumno / selector de perfil

| Dimensión | Estado | Detalle |
|---|---|---|
| Felices | 🟢 | Agregar alumno, selector de perfil con varios alumnos, elegir perfil (`registro.spec.ts`, `agregar-alumno-inline.spec.ts`) |
| Borde | 🟡 | Agregar alumno inline cubre RUT inválido y cancelar — falta el caso "mismo alumno agregado dos veces con el mismo RUT desde el flujo inline" (si existe esa restricción a nivel de UI, no solo backend) |
| Seguridad | 🟢 | `verificar_perfil_propio` cubierto transversalmente por la matriz de permisos automática |

### Contenido (guías, OA, búsqueda)

| Dimensión | Estado | Detalle |
|---|---|---|
| Felices | 🟢 | Ver guía, descargar PDF, búsqueda global, calificar con estrellas (`descarga-guia-pdf.spec.ts`, `busqueda-global.spec.ts`, `calificar-guia.spec.ts`) |
| Borde | 🟡 | Búsqueda global: falta el caso "0 resultados" explícito (hoy solo se prueba que SÍ encuentra) |
| Error | 🔴 | **No hay ningún test de OA inexistente** (`GET /contenido/objetivos/{id}` con id que no existe) ni de asignatura/nivel inexistente en el frontend — el backend probablemente da 404 pero no hay un caso que lo confirme end-to-end ni que confirme qué ve el alumno en pantalla (¿mensaje de error legible, o pantalla en blanco?). |
| Seguridad | 🟡 | El contenido de la guía se inyecta con `bypassSecurityTrustHtml` (`markdown.pipe.ts`) — hoy es seguro porque `contenido_guia` es contenido curado propio, nunca texto de un usuario. **No hay un test que documente/congele esa invariante** ("ningún endpoint de escritura de usuario puede llegar a `contenido_guia`") — si en el futuro se agrega edición de contenido por Profesor/Admin, este pipe se vuelve una vulnerabilidad XSS real sin que nada lo avise. |

### Evaluaciones (prueba de unidad, examen simulacro, autoevaluación)

| Dimensión | Estado | Detalle |
|---|---|---|
| Felices | 🟢 | Ciclo completo iniciar→responder→entregar, navegación libre, mapa de preguntas, resultado con detalle (`test_evaluaciones_intentos.py`, `casos-borde.spec.ts`, `detalle-y-reportar-error.spec.ts`) |
| Borde | 🟢 | **Muy fuerte**: entrega idempotente, reanudar el mismo intento en vez de duplicar, **concurrencia real probada** (`test_iniciar_intento_concurrente_no_crea_duplicados`), recargar a mitad de una prueba conserva respuestas, texto de respuesta demasiado largo (422), avisa si quedan preguntas sin responder |
| Error | 🟢 | Conjunto/perfil/intento inexistente → 404, no se puede responder un intento ya entregado |
| Seguridad | 🟢 | Alumno ajeno da 403, sin sesión da 401, el conjunto nunca expone la respuesta correcta antes de entregar |
| **Gap real** | 🔴 | **El cronómetro del examen simulacro no tiene un test que confirme el auto-envío al llegar a 0.** `evaluacion-runner.ts` tiene la lógica (`confirmarEnvio()` se llama cuando `tiempoRestanteSeg() === 0`), pero ningún Playwright espera el tiempo real ni lo simula (`page.clock`) para confirmarlo — es el único mecanismo "sin pausas" del examen y no está verificado end-to-end. |
| **Gap real** | 🔴 | Simulacro parcial: existe el caso feliz (cubrir 50% habilita el simulacro parcial) pero no el borde "exactamente en el umbral" (¿49.9% no habilita, 50.0% sí?) ni "cobertura baja a menos del umbral tras agregar más OA al temario". |

### Plan de Estudio

| Dimensión | Estado | Detalle |
|---|---|---|
| Felices | 🟢 | Crear plan, ver sesiones, marcar cumplida al revisar guías, reemplazar plan (`test_plan_estudio.py`, `plan-estudio.spec.ts`) |
| Borde | 🟢 | Días inválidos (no calzan con `dias_por_semana`), repaso de nivel anterior se agenda al final, sesión atrasada (backend, `test_sesion_con_fecha_pasada_y_no_cumplida_queda_marcada_atrasada`) |
| Error | 🟢 | Repasar el propio nivel da 422, repasar sin plan creado da 404 |
| Seguridad | 🟢 | Apoderado ajeno no puede crear plan para perfil ajeno |
| **Gap real** | 🔴 | **El chip "Atrasada" nunca se verificó en Playwright**, solo en `pytest` — no hay confirmación end-to-end de que el frontend efectivamente renderiza `.chip--atrasada` con el texto correcto (documentado como decisión consciente en su momento, pero sigue siendo un gap real, no una decisión final). |
| **Gap real** | 🔴 | Vista semanal/mensual: no hay caso de borde para un plan que cruza el cambio de año (diciembre→enero) ni para huso horario/medianoche exacta en el cálculo de "hoy" para `atrasada`. |

### Gamificación (XP, niveles, logros, avatares, racha)

| Dimensión | Estado | Detalle |
|---|---|---|
| Felices | 🟢 | XP por evaluación/guía, nivel, elegir avatar, catálogo completo de logros, estadísticas de uso (`test_gamificacion.py`, `test_gamificacion_dominio.py`, `gamificacion.spec.ts`) |
| Borde | 🟢 | Curva de niveles no lineal en los límites exactos (49 vs 50 vs 150 XP), racha no se infla el mismo día, saltarse un día corta la racha pero conserva el máximo, logro de nivel usa el máximo no el actual |
| Error | 🟢 | Avatar inválido da 400 |
| **Gap real** | 🔴 | **Cambio de año/huso horario en el cálculo de racha** (`registrar_actividad`) — el test usa fechas fijas en Python (`date(2026, 8, 10)`), nunca la hora real del servidor cerca de medianoche, que es el caso borde real ("¿cuenta como hoy o como ayer si el alumno estudia a las 23:58?"). |
| **Gap real** | 🟡 | Avatares con fondo tipo esfera (agregado hoy) — es un cambio puramente visual (CSS), no hay ni puede haber un test funcional que lo cubra más allá de "sin violaciones de accesibilidad" (ya cubierto). Documentado acá para que quede explícito que un cambio visual futuro en esa paleta no rompe nada automáticamente detectable — solo revisión manual/captura. |

### Notificaciones

| Dimensión | Estado | Detalle |
|---|---|---|
| Felices | 🟢 | Comunicado del curso, sesión atrasada, reporte de error resuelto aparecen como notificación (`test_notificaciones.py`) |
| Borde | 🟢 | Reporte pendiente (no resuelto) NO aparece — probado explícitamente |
| Error | 🟢 | Alumno ajeno da 403 |
| **Gap real** | 🔴 | El frontend (`notificaciones.spec.ts`) solo prueba que el panel abre — **nunca prueba con datos reales que una notificación real aparezca en la lista** (las 3 fuentes están cubiertas a fondo en backend, pero nadie confirmó que el frontend las pinta bien, con el ícono correcto por tipo). Mismo patrón de gap que "Atrasada". |

### Sugerencias, Reportar error, Calificaciones (estrellas)

| Dimensión | Estado | Detalle |
|---|---|---|
| Felices | 🟢 | Enviar, listar, calificar, recalificar (upsert) — bien cubierto en los 3 |
| Borde | 🟢 | Recalificar la misma guía actualiza en vez de duplicar, sugerencia vacía da 422, estrellas fuera de rango (0, 6) dan 422 |
| Seguridad | 🟢 | Alumno ajeno da 403 en los 3 |
| **Gap real** | 🟡 | Ninguno de los 3 tiene una bandeja de revisión de Admin (decisión de alcance documentada, no un gap de testing) — pero si algún día se construye, necesitará su propia matriz completa. |

### Plan Lector / Útiles Escolares (contenido estático curado)

| Dimensión | Estado | Detalle |
|---|---|---|
| Felices | 🟢 | Lista por nivel, agrupación por asignatura |
| Borde | 🟢 | Nivel sin libros/útiles devuelve lista vacía (no error) |
| Seguridad | 🟢 | Contenido público, sin sesión — verificado explícitamente que NO exige auth (a propósito) |
| — | — | Sin gaps identificados — superficie pequeña, bien cerrada. |

### Rol Profesor / Curso-Sección

| Dimensión | Estado | Detalle |
|---|---|---|
| Felices | 🟢 | Flujo completo registro→aprobación→crear curso→agregar alumno→progreso→comunicado (`profesor.spec.ts`, `test_curso_seccion.py`, `test_profesor_auth.py`) |
| Borde | 🟢 | No se puede agregar alumno de nivel distinto, cuenta pendiente no puede operar hasta aprobación |
| Error | 🟢 | Login incorrecto, sin sesión redirige |
| **Gap real** | 🔴 | **Quitar un alumno del curso** tiene caso de uso y endpoint (`DELETE /profesor/cursos/{id}/alumnos/{id}`) pero no hay Playwright que lo ejecute end-to-end (sí lo prueba `test_curso_seccion.py` en backend). |
| **Gap real** | 🔴 | Rechazar una cuenta de Profesor (`AprobarProfesor`/`RechazarProfesor`) — el backend tiene `test_admin_profesores.py` con 5 casos, pero no está confirmado si cubre "rechazar" o solo "aprobar" y "listar pendientes". A verificar y completar si falta. |

### Panel de Administrador (Planes, Descuentos, Cortesías, Métricas)

| Dimensión | Estado | Detalle |
|---|---|---|
| Felices | 🟢 | Login, crear/editar/desactivar plan, crear código de descuento, asignar cortesía (`admin.spec.ts`, `test_comercial.py`) |
| Borde | 🟢 | Precio negativo, descuento duplicado (400 no 500), descuento >100%, código vencido no vigente |
| Error | 🟢 | Editar/activar plan inexistente da 404, asignar cortesía a alumno inexistente da 404 |
| **Gap real** | 🔴 | **Métricas del dashboard solo se prueban "sin datos" (todo en cero)** (`test_metricas_sin_datos_devuelve_ceros`) — no hay un caso con datos reales que confirme que los números agregados (alumnos activos, ingresos, etc.) son correctos, no solo que no truenan. |

### Historial de pagos / Certificado / Informe de avance (PDF)

| Dimensión | Estado | Detalle |
|---|---|---|
| Felices | 🟢 | Los 3 devuelven un PDF real (`%PDF-` en los primeros bytes), autenticado |
| Error | 🟢 | Alumno ajeno da 403, perfil inexistente da 404 |
| **Gap real** | 🔴 | **Ningún test verifica el contenido del PDF, solo que empieza con `%PDF-`.** Un bug de contenido (nombre cortado, nota mal calculada, tabla vacía cuando debería tener datos) pasaría sin que ningún test lo note — ya pasó una vez en esta misma sesión con el bug del guion largo (encontrado porque el test SÍ ejercitaba datos reales, no por leer el PDF). Se podría extraer texto del PDF con una librería liviana (`pypdf`, ya puede que esté disponible via `fpdf2`'s ecosystem) y afirmar sobre el texto extraído en al menos los casos con datos reales. |

### Onboarding, Bienestar (check-in emocional), Ayuda contextual

| Dimensión | Estado | Detalle |
|---|---|---|
| Felices | 🟢 | Checklist de 4 pasos, se marcan al completar cada acción real, check-in con 7 opciones, ayuda contextual con tip por ruta |
| Borde | 🟢 | Check-in no vuelve a aparecer tras elegir un estado (persistencia diaria) |
| — | — | Sin gaps identificados — superficie bien acotada y ya verificada con datos reales. |

### Accesibilidad y Responsive

| Dimensión | Estado | Detalle |
|---|---|---|
| Cobertura | 🟢 | 17 páginas con axe-core (serious/critical), 8 casos de responsive/móvil |
| **Gap real** | 🔴 | **Ninguna página del rol Profesor ni del flujo de registro completo tiene chequeo de accesibilidad** (`profesor-dashboard`, `profesor-curso-detalle`) — sí están cubiertas landing/login/registro/selector-perfil/alumno/admin, pero el árbol de Profesor quedó fuera. |
| **Gap real** | 🟡 | Responsive solo prueba "no se desborda" — no prueba interacción táctil real (tap targets, scroll dentro de modales en pantallas chicas, como el modal de check-in emocional o el formulario de repaso). |

### Seguridad transversal

| Dimensión | Estado | Detalle |
|---|---|---|
| Cobertura | 🟢 | Matriz de permisos automática (`test_matriz_permisos.py`) — genera un caso por cada ruta protegida del árbol real de FastAPI, sin mantenimiento manual |
| **Gap real** | 🔴 | Rate limiting (ver Autenticación arriba) |
| **Gap real** | 🟡 | No hay un test de **inyección SQL/NoSQL** explícito — bajo riesgo real porque todo el acceso a datos usa SQLModel parametrizado (no hay SQL crudo concatenado en el proyecto, verificado por inspección), pero no hay un caso que lo *confirme* con un payload adversarial (`'; DROP TABLE--` en un campo de texto libre como `comentario` o `texto` de sugerencia). |

## Lista priorizada de gaps a cerrar

**P0 — seguridad, bajo costo, alto impacto: 🟢 cerrado (2026-08-16)**
1. 🟢 Rate limiting de login/registro (429 real al 6°/11° intento) —
   `test_registro_da_429_al_sexto_intento_en_un_minuto` / `..._login_..._onceavo_...` en
   `tests/test_auth.py`.
2. 🟢 Payload adversarial en campos de texto libre (sugerencia, comunicado, comentario de
   reporte) — confirmado en `test_sugerencias.py`, `test_reportar_error_pregunta.py`,
   `test_curso_seccion.py`: se guarda y se devuelve literal, sin ejecutarse (SQLModel
   parametrizado, Angular escapa por defecto salvo `contenido_guia`, ver ítem 11).

**P1 — gaps de "lo construimos hoy pero solo lo probamos en un lado": 🟢 cerrado (2026-08-16)**
3. 🟢 Chip "Atrasada" en Plan de Estudio — `e2e/plan-estudio-atrasada.spec.ts` (fecha
   backdateada vía `psql` directo, sin endpoint para forzarla por API).
4. 🟢 Notificaciones con datos reales — mismo archivo, confirma que una sesión atrasada
   real aparece en la campana con badge y texto correctos.
5. 🟢 Contenido real de los PDFs (certificado, informe de avance) — se agregó `pypdf` como
   dependencia de desarrollo y se extrae el texto real en `test_certificado_alumno_regular.py`
   / `test_informe_avance.py`, confirmando nombre/asignatura/nivel, no solo el header `%PDF-`.

**P2 — bordes genuinos no cubiertos: 🟢 cerrado (2026-08-16)**
6. 🟢 Auto-envío del examen simulacro al agotarse el tiempo —
   `e2e/examen-auto-envio.spec.ts`, con `page.clock` para saltar la duración completa sin
   esperar minutos reales.
7. 🟢 OA/asignatura/nivel inexistente — `e2e/recursos-inexistentes.spec.ts`. **Bug real
   encontrado y corregido**: `estudiar-oa.ts` llamaba `marcarGuiaRevisada` sin condicionar a
   que la guía hubiese cargado; con un `oa_id` inexistente el INSERT violaba la FK de
   `progreso_oa.oa_id`, producía un 500 sin manejar que el navegador reportaba como error de
   CORS (enmascarado, sin manejador de error en el `.subscribe()`). Corregido moviendo esas
   llamadas dentro del callback de éxito.
8. 🟢 Quitar alumno del curso — ya estaba cubierto end-to-end en `profesor.spec.ts` (paso 7)
   además del backend; este ítem estaba desactualizado en el plan.
9. 🟢 Accesibilidad del árbol de Profesor — casos nuevos en `accesibilidad.spec.ts`. **Bug
   real encontrado y corregido**: el `<select name="nivelId">` y varios `<input>`/`<textarea>`
   de "Crear curso" y "Comunicados" tenían `<label>` sin asociar (ni `for`/`id`, ni
   wrapping, ni `aria-label`) — violación WCAG crítica de nombre accesible. Corregido
   asociando labels con `for`/`id` y agregando `aria-label` al buscador de alumnos.
10. 🟢 Umbral exacto del simulacro parcial — `test_cobertura_justo_bajo_el_umbral_sigue_rechazando`
    en `test_evaluaciones_simulacro_parcial.py` (100 OA, 49% justo bajo el umbral de 50%,
    sigue rechazando); el caso de exactamente 50% ya existía.

**P3 — documentación/invariante: 🟢 cerrado (2026-08-16)**
11. 🟢 `tests/test_invariante_contenido_guia_sin_input_de_usuario.py` — en vez de solo un
    comentario, un test que introspecciona el árbol real de rutas de FastAPI (mismo mecanismo
    que `test_matriz_permisos.py`) y falla si algún endpoint de escritura llega a aceptar
    `contenido_guia`, o si aparece en una respuesta que no sea el único GET de lectura
    esperado — congela la invariante que hace seguro `bypassSecurityTrustHtml` en
    `estudiar-oa.ts` de forma verificable, no solo documental.
12. ⚪ Racha cerca de medianoche/cambio de año — **evaluado, decidido no escribir un test
    nuevo**. `registrar_actividad(hoy: date)` es una función pura ya cubierta a fondo en
    `test_gamificacion_dominio.py` (mismo día, día consecutivo, salto con corte de racha,
    incluyendo saltos largos) — la aritmética de `timedelta` de Python maneja cruces de
    mes/año sin casos especiales, sin riesgo ahí. La preocupación real (fecha UTC del
    servidor vs. fecha local del alumno cerca de medianoche en Chile) es una decisión de
    arquitectura ya tomada, no un bug — un test solo reafirmaría el comportamiento actual sin
    encontrar nada. Corregirlo de verdad requeriría guardar el timezone por alumno, que es un
    cambio de alcance de producto, no de testing.

## Cómo se ejecuta

```
cd backend && uv run pytest -q          # 434 tests (2026-08-16)
cd frontend && npx playwright test --workers=1   # ~342 tests, 3 navegadores (2026-08-16)
./scripts/qa_completo.sh                # ambos + build + validación de contenido
```

Cada gap cerrado debe sumar al menos un test nuevo (backend y/o Playwright), correr la suite
completa en verde, y quedar registrado en este documento moviendo la fila de 🔴/🟡 a 🟢.

## Cierre (2026-08-16)

Los 12 gaps priorizados (P0-P3) quedaron cerrados en una sola pasada, sin abrir una nueva
ronda de comparación con la competencia — honrando el feedback explícito del usuario de
"hazlo bien" la primera vez. En el camino se encontraron y corrigieron **4 problemas
reales** (no solo huecos de cobertura):

1. **500 enmascarado como CORS** al visitar una guía con `oa_id` inexistente —
   `estudiar-oa.ts` llamaba `marcarGuiaRevisada` sin condicionar a que la guía hubiese
   cargado; el INSERT violaba la FK de `progreso_oa.oa_id`. Corregido.
2. **Violación WCAG de labels sin asociar** en "Crear curso" y "Comunicados" del Profesor
   (`<select>`/`<input>`/`<textarea>` sin `for`/`id` ni `aria-label`). Corregido.
3. **Agotamiento estructural del pool de contenido "fresco"** en la cuenta compartida
   Sofía: de los 12+ conjuntos de prueba de unidad que `casos-borde.spec.ts` asumía
   disponibles, a Sofía le quedaba uno solo sin rendir, agotado por años de corridas
   acumuladas del suite contra la misma cuenta de la base de Desarrollo. Corregido migrando
   ese describe a una cuenta recién registrada por navegador, con nivel explícito ("5°
   básico", 14 conjuntos, margen real) en vez de depender del default del backend.
4. **Rate limit de producción aplicado sin diferenciar por entorno**: `/auth/registro`
   (5/minuto) y `/auth/login` (10/minuto) usaban valores fijos en el código — correctos para
   Producción, pero la suite Playwright completa (que registra decenas de cuentas de prueba
   en corridas rápidas de un solo worker) los superaba dentro de la misma ventana de un
   minuto, con fallas intermitentes en archivos sin relación entre sí. Corregido haciendo el
   límite configurable vía `settings.limite_registro_por_minuto` /
   `..._login_por_minuto` (default = valores de producción, sin cambio de comportamiento si
   no se toca nada) y agregando un `.env` local de Desarrollo con un valor relajado
   (200/minuto) — nunca en el `.env` de Producción, ver
   `planificacion/17-infraestructura-y-entornos.md`. `test_auth.py` verifica el mecanismo
   contra el valor configurado, no un número fijo, así que sigue siendo una prueba real del
   rate limit sea cual sea el valor activo en cada ambiente.

Los 4 son exactamente el tipo de defecto que este plan de pruebas exhaustivo existía para
encontrar — 2 bugs de producto, 2 problemas de infraestructura de pruebas que habrían
seguido interrumpiendo silenciosamente cualquier corrida futura del suite.

**Verificación final**: 437 tests backend + 351 Playwright (3 navegadores) en verde. Los
únicos "fallos" vistos en corridas completas fueron 2 timeouts de navegación en webkit al
final de una corrida de ~6 minutos (flakiness transitoria de recursos, confirmada
corriéndolos aislados sin ningún cambio — no una regresión).
