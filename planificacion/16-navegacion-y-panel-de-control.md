---
título: Navegación y panel de control (sidebar, login, estructura de pantallas)
estado: especificación de UX detallada (2026-08-12) — cierra el vacío antes de programar
última actualización: 2026-08-12
---

## Por qué este documento existe

Antes de escribir código, el usuario pidió explícitamente confirmar que la idea de la
aplicación está 100% clara — específicamente el login, el panel de control, y cómo se
navega (barra lateral con cursos, notas, configuración, perfil, etc.). Los documentos
anteriores (`11-especificacion-mvp-para-desarrollo.md`, `12-motor-de-evaluacion.md`)
listaban las pantallas y el modelo de datos, pero no la **estructura de navegación
persistente** (sidebar/panel) que envuelve a esas pantallas. Este documento cierra ese
vacío antes de empezar a construir.

## Login → selector de perfil → panel (flujo completo)

```
1. Landing pública (sin login)
        │
        ▼
2. Login (Apoderado) — email + password
        │
        ▼
3. Selector de perfil ────────────────────────┐
   (si el Apoderado tiene 1+ Perfiles de       │
   Alumno creados)                             │
        │                                      │
        ├── Elige "Entrar como [Alumno]" ──▶  PANEL ALUMNO (sidebar modo alumno)
        │
        └── Elige "Ver como Apoderado" ────▶  PANEL APODERADO (sidebar modo apoderado)

   (si el Apoderado NO tiene alumnos aún: salta directo a "Agregar alumno" — no tiene
   sentido mostrarle un selector vacío)
```

Un botón siempre visible en la barra superior de ambos paneles ("Cambiar de perfil")
devuelve al paso 3 sin tener que cerrar sesión — el Apoderado puede pasar de ver el
progreso de un hijo a estudiar como otro sin volver a loguearse.

## Panel del Alumno — barra lateral (sidebar)

```
┌─────────────────────────────────────┐
│  [Logo Logos]                        │
│                                       │
│  🏠  Inicio                          │
│  📚  Mis Asignaturas                 │
│  📝  Pruebas y Exámenes              │
│  📊  Mis Notas          (Fase 1.2)   │
│  📅  Plan de Estudio    (Fase 1.3)   │
│  ─────────────────────               │
│  ⚙️  Configuración                   │
│  🔄  Cambiar de perfil               │
└─────────────────────────────────────┘
```

- **Inicio**: resumen de bienvenida — "hoy te toca estudiar [tema]" (una vez que exista
  Plan de Estudio, Fase 1.3) o, en Fase 1.1 sin esa función aún, simplemente accesos
  directos a continuar donde quedó y un resumen de avance general.
- **Mis Asignaturas**: las 4 asignaturas de su Nivel (pantalla 7 de
  `11-especificacion-mvp-para-desarrollo.md`) — es la puerta de entrada a estudiar
  (Guía → Autoevaluación → Pruebas de unidad, pantallas 8-11).
- **Pruebas y Exámenes**: acceso directo y agrupado a todo lo evaluable (todas las pruebas
  de unidad pendientes/rendidas por asignatura, y el Examen simulacro) — para el alumno que
  ya estudió y solo quiere ir directo a rendir, sin navegar por la guía de nuevo.
- **Mis Notas** (aparece en Fase 1.2): historial + nota por asignatura + el resultado del
  examen simulacro destacado como "tu señal real" (ver `12-motor-de-evaluacion.md`).
- **Plan de Estudio** (aparece en Fase 1.3): calendario semanal (`13-plan-de-estudio.md`).
- **Configuración**: datos del propio perfil (nombre visible, preferencias simples).
- **Cambiar de perfil**: vuelve al selector (paso 3 del flujo de login).

En **modo examen simulacro**, la sidebar se oculta por completo (pantalla de examen a
ancho completo, sin distracciones ni forma de navegar a otro lado hasta terminar o agotar
el tiempo) — coherente con `15-diseno-visual-y-marca.md` (header oscuro, "se siente
distinto"). En pruebas de unidad y autoevaluación, la sidebar se mantiene visible pero
atenuada.

## Panel del Apoderado — barra lateral (sidebar)

```
┌─────────────────────────────────────┐
│  [Logo Logos]                        │
│                                       │
│  🏠  Inicio                          │
│  👨‍👩‍👧  Mis Alumnos                    │
│  📊  Progreso por Alumno (Fase 1.2)  │
│  💳  Plan y Pagos                    │
│  ─────────────────────               │
│  ⚙️  Configuración de cuenta         │
│  🔄  Cambiar de perfil               │
└─────────────────────────────────────┘
```

- **Inicio**: resumen general de todos sus Alumnos (cuántos tiene, estado de su plan).
- **Mis Alumnos**: lista de Perfiles de Alumno, botón "Agregar alumno" (pantalla 3),
  editar/eliminar un perfil (pantalla 14).
- **Progreso por Alumno**: entra al detalle de uno específico (pantalla 13).
- **Plan y Pagos**: ver/cambiar el Plan y Suscripción de cada Alumno (pantalla 4, revisitada
  después del registro inicial para renovar o cambiar de plan).
- **Configuración de cuenta**: datos del Apoderado, política de privacidad, exportar/
  eliminar datos (requisito de `10-privacidad-y-datos-de-menores.md`).

## Principio de diseño: sidebar extensible

La sidebar se implementa como una **lista de items configurable**, no items hardcodeados
uno por uno en el HTML — así, agregar una función nueva (ver "Crecimiento futuro" abajo) es
agregar un item a esa lista, no rediseñar la navegación. Esto es intencional para que el
crecimiento del proyecto no rompa lo ya construido.

## Crecimiento futuro (más allá de la Fase 1.1/1.2/1.3 — no se construye ahora)

El usuario preguntó explícitamente por escalabilidad (chat, voz, etc.). Registro esto como
**Etapa 2+/3+** del roadmap, no como parte de la primera salida, para que quede claro que
sí está contemplado sin comprometernos a construirlo ya:

1. **Chatbot conversacional** (item de sidebar "💬 Asistente"): ya existe un prototipo real
   funcionando hoy mismo dentro de Claude Code —
   `.claude/agents/experto-examenes-libres.md`— que sabe responder dudas de trámite Mineduc
   y de contenido de la plataforma. Convertirlo en una función dentro de la app (un chat
   embebido que llama a un modelo de lenguaje con ese mismo conocimiento) es la extensión
   más natural y de menor esfuerzo, porque el "cerebro" ya está diseñado y probado — falta
   solo la interfaz de chat y conectarlo a una API de modelo de lenguaje.
2. **Asistente de voz / evaluador de lectura en voz alta**: ya estaba anotado en
   `06-ideas-futuras.md` desde el inicio del proyecto (el niño lee un texto en voz alta, se
   evalúa fluidez/pronunciación) — encaja como función de la asignatura de Lenguaje en
   básica inicial.
3. **Rol Profesor y Curso/Sección** (Etapa 2 del roadmap, ya diseñado en el modelo de datos
   desde el inicio, ver `01-roles-y-permisos.md`) — agregaría un tercer tipo de sidebar
   ("Panel del Profesor": Mis Cursos, Mis Alumnos, Comunicados).
4. **Gamificación** (insignias, rachas, progreso visual tipo "camino") — anotado en
   `06-ideas-futuras.md`, encaja bien con el "modo básica inicial" más ilustrado de
   `15-diseno-visual-y-marca.md`.

**Nada de esto bloquea ni complica la Fase 1.1.** El motivo de documentarlo ahora es que el
modelo de datos y la estructura de sidebar de la Fase 1.1 ya están pensados para no tener
que rediseñarse cuando se agregue cada uno de estos ítems — se suman, no se reemplazan.

## Confirmación de alcance de la primera salida (Fase 1.1)

Para que quede sin ambigüedad qué sidebar/pantallas exactas se construyen primero: **de las
dos barras laterales de arriba, en la Fase 1.1 se construyen todos los ítems del Panel
Alumno excepto "Mis Notas" y "Plan de Estudio" (aparecen en Fase 1.2/1.3), y del Panel
Apoderado se construye todo excepto "Progreso por Alumno" en su versión completa (Fase
1.2)** — un apoderado en Fase 1.1 puede ver que su hijo existe y tiene un plan activo, pero
el historial/notas detallado llega en la fase siguiente. Esto es exactamente lo mismo que ya
estaba escrito en `03-roadmap-etapas.md` para las 3 fases, ahora expresado en términos de
qué aparece o no en cada sidebar, para que no haya ambigüedad al construir.
