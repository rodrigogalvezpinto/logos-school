---
título: Análisis de brechas — qué falta para que esto sea un producto real
estado: auditoría (2026-08-12), verificado contra el código y la base de datos reales
última actualización: 2026-08-12 (segunda pasada — Fase 1.1 + refactor hexagonal completos)
---

Este documento se generó revisando el estado real del repositorio y de la base de datos
(no de memoria) — cada punto está verificado con un comando concreto, no es una lista
genérica.

## ✅ Los 12 cursos importados y validados (2026-08-13)

A pedido explícito del usuario ("necesito que pruebes todos los cursos de primero básico a
cuarto medio"), se importaron los 9 cursos que faltaban (antes solo 4°/6° básico y 1° básico
estaban en la base de datos) y se corrió una validación de contenido automatizada sobre los
12 completos, más simulaciones reales con Playwright en 1° básico (Régimen A) y 4° medio
(Régimen C) respondiendo con las respuestas correctas reales.

Encontró 3 bugs de parsing adicionales (más allá de los ya documentados el mismo día en la
sección de arriba) que solo aparecían en cursos que todavía no se habían probado:
1. Un tercer formato válido de pregunta usado en 3°-4° medio ("1. *(Alternativas)*", en
   cursiva) que el fix de "negrita obligatoria" rechazaba por error, dejando 0 preguntas
   importadas en varias pruebas de 4° medio.
2. Verdadero/Falso con la explicación pegada a la respuesta en pruebas/exámenes (mismo
   problema ya visto en el banco de autoevaluación, pero en un parser distinto).
3. **Opciones que se ajustan a dos líneas ("word-wrap")** sin repetir la letra — la línea de
   continuación se pegaba al enunciado en vez de a la opción, contaminando la pregunta con
   texto suelto y truncando la opción real.

**Estado final**: 6.114 preguntas en la base de datos (los 12 cursos), 2.491 de
alternativas/verdadero-falso, 97.4% con la respuesta correctamente resuelta. El 2.6%
restante son preguntas de tipo "emparejar" (ver más abajo, sección de calidad/pulido) — un
formato de pregunta distinto, no un bug de parsing. 133/133 tests backend, 43/43 E2E, ambos
verificados después de cada fix. Scripts nuevos y reutilizables:
`scripts/reimportar_pruebas_y_examenes.py` y `scripts/reimportar_banco_autoevaluacion.py`
(reconstruyen ese contenido desde los `.md` fuente con el parser vigente — útiles si el
contenido se sigue editando).

## 🔴 CRÍTICO — encontrado y corregido (2026-08-13): la corrección de alternativas estaba rota en TODO el proyecto

El hallazgo más grave de todo el proyecto hasta ahora, encontrado a pedido explícito del
usuario ("pruebas más complejas"): se rindió un examen simulacro completo con las
**respuestas correctas reales** (no al azar) y dio **0 de 12 correctas**. Investigado a
fondo, la causa era doble, en los dos parsers de importación de contenido
(`parser_contenido.py` para el banco de autoevaluación de las guías, `parser_prueba_examen.py`
para pruebas de unidad y exámenes):

1. **La pauta de respuestas a veces solo trae la letra** ("Respuesta correcta: b.") y a veces
   la letra + el texto repetido ("Respuesta correcta: d) Unidad de mil.") — pero el alumno
   siempre responde con el **texto completo** de la opción que clickeó, nunca con la letra.
   `IntentoEvaluacion.entregar()` comparaba ambos con `==` directo — nunca podían calzar.
   Esto afectaba **todas** las preguntas de alternativas de **todo** el proyecto: banco de
   autoevaluación (2.917 preguntas), pruebas de unidad y exámenes simulacro, en los 3 cursos
   importados. Es decir: ningún alumno podía obtener nunca una respuesta de alternativas
   marcada como correcta, sin importar qué elegiera.
2. Bug relacionado, encontrado primero: las instrucciones numeradas al inicio de cada examen
   ("1. Este examen contiene 25 preguntas...", "2. Se permite calculadora...") se parseaban
   como preguntas falsas (`RE_Q_START` no exigía que la línea empezara en negrita, que es lo
   único que distingue una pregunta real de una instrucción) — desalineaba el conteo de
   preguntas (31 en vez de 25) y toda la pauta de respuestas quedaba corrida. Corregido
   exigiendo "**" obligatorio al inicio; reimportados los 9 exámenes afectados.

**Corrección**: ambos parsers ahora resuelven la letra al texto real de la opción en el
momento de parsear (fuente de verdad única), con normalización adicional para emojis de
viñeta que contaminaban la respuesta ("Falso 💬") y para respuestas bilingües del contenido
de Inglés ("True (Verdadero)" → "Verdadero"). Nuevos tests unitarios
(`test_parser_contenido.py`, `test_parser_prueba_examen.py`) fijan esto como regresión
permanente. Se corrigieron in-place las preguntas ya importadas
(`scripts/backfill_respuestas_correctas.py`, emparejando por enunciado exacto — no se
borraron ni recrearon filas, para no tocar IDs referenciados por intentos ya guardados): de
562 preguntas de alternativas/verdadero-falso en los 3 cursos importados, 534 quedaron
correctamente resueltas (el texto de `respuesta_correcta` calza exactamente con una opción).

**Verificado end-to-end**: se repitió la simulación del examen de Matemática 6° básico
respondiendo con las 12 respuestas correctas reales — pasó de "Nota: 1, 0/12 correctas" a
"Nota: 7, 12/12 correctas".

**Queda un residuo documentado, no bloqueante**: ~28 preguntas (de ~850 con alternativas)
siguen sin calzar exactamente. La mayoría son preguntas de **"emparejar"** ("Une cada
autoridad con..." / "Clasifica cada elemento como...") — un formato de pregunta que la UI
actual (opción única) no soporta bien; requieren o un tipo de pregunta nuevo en el frontend,
o reescribirse como alternativas simples. El resto es contenido en la base de datos que ya no
coincide exactamente con el archivo `.md` fuente actual (fue editado después de la
importación original) — se resolverá con una reimportación completa controlada cuando se
retome el trabajo de contenido, no con otro backfill puntual.

## ✅ Resuelto en esta sesión (ya no son brechas)

1. ~~El Front no está conectado al backend~~ — conectado con `HttpClient` real, JWT,
   `SesionService` persistido en `localStorage`, guards de ruta.
2. ~~Pruebas de unidad y Exámenes simulacro no importados~~ — parser nuevo
   (`scripts/parser_prueba_examen.py`) + importados: 4° básico 12 pruebas/108 preguntas +
   2 exámenes/56 preguntas, 6° básico 14 pruebas/170 preguntas + 5 exámenes/150 preguntas.
3. ~~Nada persiste un intento de evaluación~~ — ciclo completo iniciar/responder/entregar,
   idempotente, con cálculo de nota real server-side.
4. ~~Los Planes no calzan con lo decidido~~ — sembrados los 3 planes reales de
   `09-modelo-de-negocio.md` (mensual $19.990 / por periodo $89.900 / anual $159.900).
5. ~~Validación de RUT chileno~~ — módulo 11, en frontend y backend.
6. ~~Página de Privacidad y Términos~~ — existen y están enlazadas desde el registro.
7. ~~Arquitectura del backend~~ — refactor completo a hexagonal (dominio/aplicación/
   infraestructura), SOLID, patrones nombrados (Repository, Strategy, DI, Factory methods,
   Value Objects). Ver el commit "Refactor backend a arquitectura hexagonal".

Verificación end-to-end vigente: **51/51 tests de backend, 18/18 E2E de Playwright**.

## 🟠 Necesario antes de mostrarle esto a una familia real (no solo a ti)

1. **Pasarela de pago real.** Sigue mockeada — hay que elegir proveedor (Webpay/Transbank es
   el estándar en Chile) e integrarlo. Lo que sí se implementó (2026-08-13): la **prueba
   gratuita de 7 días** activa una `Suscripcion` real al elegir plan (sin cobrar), pero
   todavía no existe ningún gate que bloquee el acceso cuando la prueba vence sin plan
   pagado — eso se agrega junto con la pasarela real.
2. **Login con Google no tiene credenciales reales.** El código está listo y ahora detrás
   de un puerto (`VerificadorTokenGoogleAdapter`), pero `GOOGLE_CLIENT_ID` no existe — no
   hay `.env` real todavía, solo `.env.example`.
3. **Correo (Resend) sin API key real.** El adaptador existe (`infrastructure/
   notificaciones/`, pendiente de mover — ver Paso 5 diferido del refactor) pero no está
   cableado a ningún caso de uso ni tiene API key real.
4. **Nada está desplegado.** Todo corre en tu Mac (Postgres local, `uvicorn`, `ng serve`).
   Faltan las cuentas reales de Neon, Render y Cloudflare Pages
   (`planificacion/17-infraestructura-y-entornos.md`) — requieren tu información de
   contacto/pago, no las puedo crear yo.
5. **Cloudflare Turnstile (anti-bots)** no está implementado en registro/login, aunque ya
   está decidido en `planificacion/20-seguridad-y-casos-borde.md`.

## 🟡 Ya planificado, simplemente no construido todavía (no es una sorpresa)

6. ~~Fase 1.2 (historial y notas por materia)~~ — **completa (2026-08-12)**: nuevo bounded
   context `progreso`, endpoints `GET/POST /progreso/{perfil_alumno_id}`, páginas
   `/alumno/notas` y `/apoderado/progreso/:id`. 56/56 tests backend, 21/21 E2E.
7. ~~Fase 1.3 (plan de estudio con horario)~~ — **completa (2026-08-13)**: nuevo bounded
   context `plan_estudio` (cronograma round-robin puro y testeable, orientado a la fecha
   del examen o +8 semanas por defecto), simulacro parcial generado on-demand
   (`ConjuntoEvaluacion` dinámico acotado a las OA ya cubiertas, reutiliza el ciclo
   IniciarIntento/EntregarIntento sin cambios), habilitación progresiva de pruebas/exámenes
   y lista de "faltantes" en `/alumno/notas`, onboarding con selección de días y fecha
   objetivo. Páginas `/alumno/plan-estudio` y sección de faltantes en `/alumno/notas`.
   102/102 tests backend, 32/32 E2E.
8. ~~Panel de Administrador~~ — **completo (2026-08-13)**: nuevos bounded contexts `admin`
   (login separado del Apoderado, JWT con claim `tipo` propio para que un token nunca sirva
   de credencial del otro) y `comercial` (Planes, Códigos de descuento, cortesías,
   métricas). Páginas `/admin/login`, `/admin/dashboard`, `/admin/planes`,
   `/admin/descuentos`, `/admin/cortesias`. 76/76 tests backend, 29/29 E2E.
9. ~~Rol Profesor / Curso-Sección~~ — **completo (2026-08-13)**: nuevos bounded contexts
   `profesor` (auto-registro, `estado="pendiente"` hasta aprobación, JWT propio con claim
   `tipo="profesor"`) y `curso_seccion` (crear curso, agregar/quitar alumno, comunicados,
   progreso agregado del curso reutilizando `ObtenerHistorialYNotas` de Fase 1.2). Aprobación
   de cuentas reutiliza el panel Admin ya existente (`/admin/profesores`, protegido por
   `get_cuenta_admin_actual`), sin construir un cuarto sistema de auth. Páginas
   `/profesor/login`, `/profesor/dashboard`, `/profesor/cursos/:id`, `/admin/profesores`, y
   sección "Mi Curso" en `/alumno/inicio`. 122/122 tests backend, 35/35 E2E.

**Orden acordado con el usuario (2026-08-12): Fase 1.2 (✅) → Panel de Administrador (✅) →
Fase 1.3 (✅) → Rol Profesor (✅). Etapa 1 (MVP) + Etapa 2 completas.**

## 🟢 Calidad / pulido — no bloquea lanzar, pero se nota

10. ~~Lectura en voz alta~~ — **implementada (2026-08-13)**: `LectorVozService` +
    `BotonEscuchar`, conectado en guía de estudio y en cada pregunta (autoevaluación, prueba,
    examen). Ver `21-accesibilidad-lectura-y-contenido-visual.md`. **Componentes visuales de
    Matemática** (recta numérica, modelo de fracciones) siguen decididos, no implementados.
11. **Logo**: sigue siendo el concepto SVG simple, no una versión pulida final.
12. **CI/CD**: no hay ningún pipeline (GitHub Actions u otro) que corra los tests
    automáticamente en cada cambio — hoy dependen de correrlos a mano.
13. ~~Responsive/móvil~~ — **corregido (2026-08-13)**: exploración interactiva con Playwright
    en viewport móvil encontró el sidebar sin colapsar en los 3 shells (desbordaba el layout
    horizontalmente) y el nav de la landing dejando el CTA principal fuera de pantalla. Ambos
    corregidos (menú off-canvas con hamburguesa, nav simplificado en mobile). Ver
    `e2e/responsive.spec.ts`.
14. ~~Auditoría de accesibilidad~~ — **hecha (2026-08-13)** con axe-core (`@axe-core/playwright`):
    encontró y corrigió un bug real de contraste (botón "Crear cuenta" con texto oscuro sobre
    fondo índigo, por una colisión de especificidad CSS — no solo un tema de a11y, se veía
    mal), el par coral-sobre-coral-claro usado en varios chips/pills (nuevo token
    `--color-secundario-texto`), `<main>` landmark faltante en 7 páginas, y heading-order en
    `notas.ts`. Queda un ítem menor sin resolver a propósito: el contraste del texto
    secundario dentro de tarjetas de evaluación bloqueadas (`.fila-historial--bloqueada`,
    opacity 0.8) — WCAG exime a componentes de UI inactivos de este requisito. Ver
    `e2e/accesibilidad.spec.ts` (corre en cada suite, falla ante violaciones serias/críticas
    nuevas).
15. **Simulación real de un alumno de 1° básico (2026-08-13)** — a pedido del usuario, quien
    quería *verlo* funcionar (no solo revisar código): se importó 1° básico a la base de
    datos local (antes solo estaban 4° y 6° básico, aunque el contenido de los 12 cursos está
    100% escrito — ver `contenido/00-estado-contenido.md`) y se recorrió con Playwright en
    modo visible (`headless: false`) el viaje completo: registro → agregar alumno → prueba
    gratuita → estudiar guía → autoevaluación → prueba de unidad → Mis Notas → Plan de
    Estudio. Encontró 3 bugs reales que ningún test anterior detectaba porque nadie había
    mirado el contenido *renderizado*, no solo el flujo:
    - **El contenido de las guías se mostraba como Markdown crudo** (`###`, `**negrita**`
      literales) en vez de HTML formateado — afectaba a los 3 cursos importados, no solo a
      1° básico. Se agregó `MarkdownPipe` (usa `marked`) en `estudiar-oa.ts`.
    - **Los nombres de las pruebas de unidad perdían tildes y capitalizaban mal**
      ("Matematica Unidad Geometria" en vez de "Matemática — Geometría") — el importador los
      derivaba del nombre de archivo con `.title()` en vez de leer el encabezado real del
      `.md`. Corregido en `importar_contenido.py` (`_titulo_desde_encabezado`) +
      `scripts/backfill_nombres_prueba_unidad.py` para las 38 filas ya importadas (usando el
      enunciado de la primera pregunta como clave de re-matching, no el nombre, que en un
      primer intento de backfill quedó ambiguo entre cursos — corregido en el mismo pase).
    - **Una nota reprobada (1.0) se mostraba en verde** (color de éxito) en la pantalla de
      resultado de pruebas/exámenes — confundía visualmente aprobado con reprobado. Corregido
      en `evaluacion-runner.ts`/`.scss` (rojo si nota < 4.0).

    126/126 tests backend, 43/43 E2E (2 aserciones nuevas fijan estos hallazgos).

## Recomendación de orden

Con la Fase 1.1 funcionando de verdad end-to-end y el backend ya en arquitectura hexagonal,
el camino más corto a "esto ya sirve para una familia real" es: **(1) desplegar a
Neon+Render+Cloudflare Pages → (2) credenciales reales de Google/Resend → (3) pasarela de
pago → (4) Turnstile.** Con esos 4 pasos la app deja de vivir solo en tu Mac. El resto
(Fase 1.2/1.3, Admin panel, pulido visual) se puede ir sumando con la app ya en producción.
