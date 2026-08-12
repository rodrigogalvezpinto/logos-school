---
título: Diseño visual y marca — paleta, tipografía, criterio UX
estado: decisión de diseño (2026-08-12), lista para implementar
última actualización: 2026-08-12
---

## El desafío de diseño real

El público va de **6 a 18 años** — un niño que recién aprende a leer y un adolescente a un
año de ser adulto usan la misma plataforma. El error más común en edtech es elegir un
extremo: o queda infantil (colores primarios saturados, mascotas, tipografía redonda por
todas partes — un joven de 2° medio lo encuentra vergonzoso) o queda fría/corporativa (mucho
azul genérico tipo "app de banco" — aburre a un niño de 7 años y no genera ganas de volver).

**Decisión: un sistema de marca único que "madura" visualmente según el ciclo, no dos marcas
distintas.** Mismos colores base y misma tipografía en los 12 cursos — lo que cambia es la
densidad de ilustración y el tamaño de los elementos, no la identidad.

## Paleta de colores

| Rol | Color | Hex | Por qué |
|---|---|---|---|
| **Primario** | Índigo violeta vivo | `#5B4FE9` | Transmite "enfoque, inteligencia, creatividad" sin caer en el azul genérico de apps corporativas ni en el celeste "app de guagua". Funciona igual de bien en la pantalla de un niño de 7 años que en la de un joven de 17. |
| **Secundario / CTA** | Coral cálido | `#FF6B4A` | Para botones de acción ("Comenzar prueba", "Estudiar ahora") — cálido, invita a hacer clic, contrasta fuerte contra el índigo sin ser un color "de niño chico" (no es el naranja fluorescente de apps de juegos). |
| **Éxito / dominado** | Verde | `#22C55E` | Universal para "correcto"/"OA dominado" — moderno, no neón. |
| **Reforzar / en progreso** | Ámbar | `#F59E0B` | Para "en progreso" o "necesitas reforzar" — deliberadamente **no rojo**: el rojo en contexto escolar se asocia a error/castigo y desmotiva; el ámbar comunica "atención" sin sentirse punitivo. |
| **Error puntual** | Rojo apagado | `#EF4444` | Uso mínimo y solo funcional (ej. últimos segundos del cronómetro en examen simulacro) — nunca como color de fondo de una mala nota. |
| **Fondo claro** | Gris muy claro | `#FAFAFA` | No blanco puro — reduce fatiga visual en sesiones de estudio largas. |
| **Texto principal** | Gris casi negro | `#1F2937` | Buen contraste (cumple WCAG AA) sin el cansancio visual del negro puro sobre blanco. |
| **Fondo modo examen** | Azul-índigo oscuro | `#14132B` | Ver "Distinción visual práctica vs. examen" abajo. |

## Tipografía

- **Titulares y marca: Poppins** (Google Fonts, gratis) — geométrica, amigable pero no
  infantil, escala bien desde un título grande en la pantalla de un niño de 1° básico hasta
  el texto de un menú en la vista de un alumno de 4° medio.
- **Cuerpo de texto y preguntas: Inter** (Google Fonts, gratis) — altísima legibilidad a
  tamaños chicos, crítico porque los alumnos van a **leer preguntas completas bajo
  cronómetro** — no es el lugar para una fuente "creativa".
- Una sola pareja tipográfica para los 12 cursos — lo que varía es el tamaño/peso, no la
  fuente, para no complicar la implementación.

## Cómo "madura" el diseño por ciclo (mismo sistema, distinta densidad)

| | 1°-4° básico (6-10 años) | 5° básico-4° medio (10-18 años) |
|---|---|---|
| Formas | Esquinas redondeadas marcadas, botones grandes | Esquinas redondeadas sutiles, más compactas |
| Ilustración | Presencia visual fuerte (íconos ilustrados por asignatura, progreso con elementos visuales tipo "camino"/mapa) | Mínima — iconografía simple, más espacio para datos (notas, gráficos de avance) |
| Uso del coral/ámbar | Liberal, para celebrar avances | Más contenido, reservado sobre todo para estados/CTAs |
| Tono de textos | Cercano, exclamativo ("¡Bien hecho!") | Directo, informativo ("Correcto — dominas este OA") |

Un desarrollador puede implementar esto como **tokens de diseño** (mismo set de variables
CSS/tema de Angular Material) con dos "densidades" — no son dos apps distintas.

## Distinción visual práctica vs. examen (refuerza `12-motor-de-evaluacion.md`)

- **Autoevaluación / estudio**: fondo claro (`#FAFAFA`), colores completos, tono relajado.
- **Examen simulacro**: la interfaz cambia a un header oscuro (`#14132B`) con el cronómetro
  destacado — comunica sin palabras "esto es distinto, esto es en serio", igual que en
  `12-motor-de-evaluacion.md` se pidió que el examen "se sienta deliberadamente distinto" de
  una prueba de unidad. El cronómetro pasa a ámbar en los últimos 5 minutos y a rojo apagado
  en el último minuto.

## Logo (concepto, no arte final)

Un ícono simple: **un libro abierto cuyas páginas forman una flecha o un camino ascendente**
(no una montaña literal, algo más abstracto/geométrico) — comunica "conocimiento que te hace
avanzar" sin usar los clichés típicos del rubro (birrete de graduación, búho, lápiz). En
color primario (`#5B4FE9`), junto al nombre "Logos" en Poppins semi-bold. Debe verse bien en
monocromático (para favicon, apps) y a tamaño chico.

## Estrategia de imágenes e ilustraciones (decisión 2026-08-12, para ser autónomo sin pedir descargas manuales)

El usuario pidió que yo mismo consiga o genere las imágenes necesarias, con cuidado de que
sean coherentes con el contenido (no una imagen genérica desconectada de lo que muestra).

**Decisión: ilustraciones propias en SVG como opción principal, no fotos de stock.** Razón:
para una app de estudio infantil/juvenil, un sistema de ilustraciones planas hechas a medida
(estilo flat-illustration, muy usado en edtech moderno) en la paleta de marca ya definida
(índigo/coral/verde/ámbar) es más coherente, más liviano de cargar, se ve más "producto
terminado" que fotos de banco de imágenes, y elimina por completo el riesgo que preocupaba
al usuario (una foto de stock que no calce con el contexto — ej. un paisaje donde debería
ir algo de matemáticas). Cada ilustración se construye expresamente para lo que representa
(ej. un ícono de libro+lápiz para Lenguaje, de regla+compás para Geometría, de hoja+lupa
para Ciencias Naturales, de mapa/bandera para Historia) usando los colores de marca — no hay
ambigüedad de contenido porque se diseña a propósito, no se busca y adapta.

**Fuentes libres a usar cuando haga falta una imagen que no tenga sentido dibujar a mano**
(ej. una foto real para la sección "quiénes somos" más adelante, o un mockup de dispositivo):
- **Unsplash** (unsplash.com) y **Pexels** (pexels.com) — bancos de fotos gratuitos, sin
  atribución obligatoria, licencia comercial permitida.
- **unDraw** (undraw.co) — ilustraciones vectoriales gratuitas, con la ventaja de que
  permiten cambiar el color principal para que calcen con la paleta de marca — buena opción
  intermedia entre "dibujar todo a mano" y "usar una foto".
- **Iconos**: **Heroicons** o **Lucide** (ambos gratuitos, open source, se integran directo
  como componentes en Angular) para toda la iconografía de la interfaz (sidebar, botones).

**Regla de uso**: antes de insertar cualquier imagen de estas fuentes, verificar que el tema
de la imagen corresponda exactamente a lo que ilustra (nunca una imagen "parecida" o
genérica) — si no hay un resultado que calce bien, se prefiere una ilustración SVG propia
simple antes que una foto que no encaje.

## Logo (decisión final, no solo concepto)

Además del concepto ya descrito arriba (libro abierto cuyas páginas forman un camino
ascendente), el logo se construye como **archivo SVG propio** (no una foto ni un ícono de
stock) apenas se inicie el desarrollo del frontend — es información vectorial simple
(geometría de un libro + una flecha), perfectamente viable de construir a mano en SVG con
las herramientas de este proyecto, sin depender de un diseñador externo ni de una
herramienta de generación de imágenes por separado. Se entrega en al menos 2 variantes:
ícono solo (favicon, apps) y logo completo con el nombre "Logos" en Poppins semi-bold junto
al ícono (header de la app, landing).

## Accesibilidad (no negociable dado el rango de edad)

- Contraste mínimo AA de WCAG en todo texto sobre fondo.
- Nunca comunicar únicamente con color (ej. "correcto/incorrecto" siempre con ícono +
  color, no solo color, por daltonismo).
- Tamaños de texto y botones generosos en el ciclo de básica inicial (dedos/motricidad fina
  de niños de 6-8 años en pantallas táctiles).
