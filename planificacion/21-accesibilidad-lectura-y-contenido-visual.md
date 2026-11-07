---
título: Accesibilidad de lectura (1°-2° básico) y contenido visual de Matemática
estado: decisión de diseño (2026-08-12)
última actualización: 2026-08-12
---

## El problema

El usuario planteó dos preguntas legítimas al ver el prototipo visual: (1) ¿cómo usa la
plataforma un niño de 1° básico que todavía no sabe leer bien?, y (2) ¿cómo se explica
Matemática, que es más difícil de transmitir solo con texto?

## 1. Lectura en voz alta para 1°-2° básico (no reemplaza al `06-ideas-futuras.md`, lo complementa)

El currículum oficial de 1° básico chileno asume que el niño **aprende a leer durante ese
mismo año** — no es un defecto del contenido, es una condición real de ese ciclo que la
interfaz debe asumir desde el diseño, no arreglar después.

**✅ Implementado (2026-08-13)**: `LectorVozService` (`frontend/src/app/core/lector-voz.service.ts`,
envuelve `window.speechSynthesis`, `es-CL`) + componente `BotonEscuchar` reutilizable
(`frontend/src/app/shared/boton-escuchar/`), conectado en `estudiar-oa.ts` (guía completa) y
en `evaluacion-runner.ts` (enunciado de cada pregunta — autoevaluación, prueba de unidad y
examen simulacro, los 3 modos usan el mismo componente). Sin cambios de backend: es texto que
ya viene en la respuesta de la API. 35/35 E2E siguen en verde, con una aserción nueva que
confirma que el botón aparece en guía y en pregunta.

**Decisión original**: botón "🔊 Escuchar" en toda guía y toda pregunta, usando la **Web Speech API**
(función de texto-a-voz nativa de los navegadores modernos) — gratuita, sin costo de
licencia, sin necesidad de grabar voces humanas para miles de preguntas. Es la opción
correcta para partir, coherente con el criterio de tecnología gratuita del proyecto
(`17-infraestructura-y-entornos.md`). Si más adelante se quiere una voz chilena de mejor
calidad, se puede evaluar un servicio de texto-a-voz pagado (Google Cloud TTS, ElevenLabs)
sin cambiar el resto del diseño — el botón "Escuchar" simplemente cambiaría de motor.

**✅ Actualización (2026-11-07) — voz más natural, sin costo:**
- **Qué se lee.** `shared/texto-para-voz.ts` convierte el contenido en texto hablable. Antes se
  leía el Markdown crudo: asteriscos, nombres de emojis y los marcadores visuales. Un dibujo
  como `::posicion::🐱::debajo::mesa::` se oía «gato debajo mesa», o sea, la respuesta. Ahora
  los dibujos no se leen (el niño los mira). En las preguntas se leen también las alternativas,
  con su letra. Los símbolos se dicen con palabras («mayor que»).
- **Voz del dispositivo.** Se elige la mejor voz local en español: primero las de calidad
  («Mejorada», «Premium», «Natural»), y a igual calidad Chile, luego América y luego España. Se
  descartan voces novedad y eSpeak. La lectura va por frases: pausas naturales y sin el corte de
  Chrome en textos largos. Nunca se usan voces remotas, para que el texto no salga del equipo.
- **Audio pregrabado con voz neuronal libre.** Se usa Kokoro-82M con la voz `em_alex`
  (licencia Apache-2.0, permite uso comercial). El usuario la eligió el 2026-11-07 tras
  escuchar las 8 muestras. `scripts/voz/generar_audios.sh` genera un
  `.m4a` por texto (AAC mono, 32 kbps) en `frontend/public/audio/es/`, más un
  `manifest.json`. El lector lo usa si existe el audio del texto exacto (clave FNV-1a de 64
  bits, `core/audio-pregrabado.ts`); si no, usa la voz del dispositivo. Por ahora cubre
  1.° y 2.° básico.
  - **No se versiona** (≈55 MB): al desplegar hay que ejecutar el generador antes del build, o
    subir la carpeta a un almacenamiento estático (p. ej. Cloudflare R2, que tiene plan gratuito).
  - Al cambiar un texto, su audio deja de coincidir y se vuelve a la voz del dispositivo hasta
    que se regenera. El generador solo crea lo que falta.
- **Voces comparadas el 2026-11-07.** Piper (claude, daniela, ald, davefx), Kokoro (dora, alex)
  y las voces del Mac (Paulina, Mónica). Ninguna voz libre tiene acento chileno. Elegida: Kokoro «alex».

Complementa (no reemplaza) la idea ya anotada en `06-ideas-futuras.md` de un "evaluador de
lectura en voz alta" — esa función evalúa *cómo lee* el niño; esta nueva función *le lee a
él* cuando todavía no puede leer solo. Son dos necesidades distintas del mismo ciclo etario.

Otras medidas ya alineadas con esto (reforzando lo ya definido en
`15-diseno-visual-y-marca.md`): menos texto por pantalla, más íconos, botones grandes, y
asumir que un adulto puede estar acompañando en este ciclo — no es una falla del alumno, es
esperable.

## 2. Contenido visual para Matemática (y Geometría/Ciencias en general)

Texto solo no alcanza para representar bien una recta numérica, un modelo de fracciones, o
una rotación de una figura geométrica.

**Decisión: componentes visuales propios y reutilizables (Angular), no imágenes sueltas por
pregunta.** Se construyen una vez, reciben datos como parámetros, y se reutilizan en
cientos de preguntas distintas — mucho más mantenible que diseñar una imagen para cada
pregunta, y coherente con la estrategia de ilustraciones SVG propias ya definida en
`15-diseno-visual-y-marca.md` (evita el mismo riesgo: una imagen genérica que no calce con
lo que se pregunta).

Ejemplos de componentes a construir cuando se llegue a esa parte del desarrollo:
- `RectaNumerica`: dibuja una recta numérica entre dos valores y marca uno o más puntos.
- `ModeloFraccion`: representa una fracción como área dividida (círculo o rectángulo).
- `FiguraGeometrica`: dibuja figuras y sus transformaciones (traslación, rotación, reflejo)
  — relevante para el eje de Geometría de 4° básico que ya está en el contenido.
- `GraficoBarras` / `GraficoLineal`: para el eje de Datos y Probabilidades.

**Cómo se conecta con el contenido ya escrito**: el campo `contenido_guia` y las preguntas
del modelo de datos (`11-especificacion-mvp-para-desarrollo.md`) necesitan un campo
adicional opcional para indicar qué componente visual usar y con qué parámetros (ej.
`recurso_visual: { tipo: "recta_numerica", desde: 0, hasta: 20, marcar: [7] }`), en vez de
forzar todo a texto plano. Esto se agrega al modelo de datos cuando se empiece el desarrollo
real del backend (Fase 1.1) — no bloquea el prototipo visual actual.

## No bloquea el prototipo visual de hoy

Ninguna de estas dos decisiones necesita implementarse en el Front navegable actual (que es
solo para revisar la sensación general) — quedan documentadas para construirse como parte
del desarrollo real de la Fase 1.1, especialmente antes de cargar contenido real de cursos
de básica inicial (1°-2° básico) y de las unidades de Geometría/Datos de Matemática.
