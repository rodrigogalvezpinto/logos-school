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
