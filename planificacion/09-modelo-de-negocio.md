---
título: Modelo de negocio y sostenibilidad
estado: revisado (2026-08-12) — modelo de planes pagos, corrige la versión "siempre gratis"
última actualización: 2026-08-12
---

## Corrección de enfoque (2026-08-12)

La primera versión de este documento fijó "el contenido central siempre 100% gratuito" como
regla no negociable. El usuario corrigió esto: **Logos va a tener planes de pago**, igual
que las plataformas chilenas reales que uso como referencia directa (Lumbreras, y
especialmente Wited, que sí se pudo investigar en profundidad). No está cerrado si existirá
además algún nivel gratuito de entrada — eso se define más adelante — pero la
**infraestructura de planes/pagos sí es parte del proyecto desde ahora**, no algo que se
posterga indefinidamente.

## Referencia directa: Wited (investigado 2026-08-12)

Wited (wited.com/cl) es una plataforma chilena real con dos líneas: reforzamiento escolar y
"Colegio Online/Homeschool" orientado a Exámenes Libres del Mineduc — el competidor más
directo y mejor documentado encontrado. Su modelo:

- Registro: una cuenta de apoderado agrega N alumnos (nombre, fecha de nacimiento, RUT,
  curso) — ver `10-privacidad-y-datos-de-menores.md`, es la referencia de registro que
  Logos adopta.
- **Planes por intensidad de servicio**, pago mensual (admisión 2026, 4 cuotas):

| Plan | Precio mensual | Qué incluye |
|---|---|---|
| Basic | $89.470 | Clases grupales (hasta 20/mes), soporte docente por chat, contenido y clases grabadas, ensayos, cuenta de supervisión parental |
| Lite | $147.790 (oferta) | Hasta 40 clases grupales/mes, resto igual que Basic |
| Full | $194.440 (oferta) | Hasta 60 clases grupales/mes + 5 tutorías 1:1 anuales + 5 sesiones de apoyo psicopedagógico anuales |

No confirmamos si el precio es por alumno o por familia (el sitio pide especificar cantidad
de alumnos al pagar, lo que sugiere por alumno, pero no está confirmado textualmente).

Otros competidores identificados en la investigación anterior, para contexto de rango de
precios del mercado: Entreser ($250.000 CLP pago único por curso completo), Preparación
Ética ($20.000 matrícula + $19.000/mes). Lumbreras no se pudo investigar en profundidad
(sitio no renderizable con las herramientas de búsqueda disponibles) — pendiente de revisión
manual por el usuario si se quiere usar como referencia adicional.

## Decisión: modelo de planes por nivel de acceso/servicio, inspirado en Wited

Logos no compite ofreciendo clases en vivo con profesores (al menos no en el MVP, que es
autoestudio puro) — compite con **contenido de estudio propio, ya construido y validado
contra los temarios oficiales de los 12 niveles** (guías, banco de preguntas, pruebas de
unidad, exámenes simulacro). El modelo de planes debe reflejar esa diferencia, no copiar la
estructura de Wited campana por campana.

**Estructura de planes propuesta (nombres y montos por definir más adelante, la estructura
de niveles sí queda fijada):**

1. **Plan de entrada** — acceso a la guía de estudio y autoevaluación de un curso/nivel.
   Sirve como punto de conversión (quien lo prueba, ve el valor y pasa al plan completo).
   Si termina siendo gratis o un precio simbólico bajo, es una decisión de pricing a tomar
   con datos reales de conversión una vez que haya usuarios — no se fija ahora.
2. **Plan completo** — acceso a todo el contenido del nivel: guía, autoevaluación, pruebas
   de unidad y exámenes simulacro completos, para las asignaturas de su curso.
3. **Plan con acompañamiento** (fase posterior, no en el MVP) — igual que el plan completo,
   más servicios humanos: tutorías puntuales, corrección personalizada de ensayos/escritura,
   reportes de avance más detallados para el apoderado. Es el equivalente al "Full" de
   Wited, pero no se construye en el MVP.

**Qué sí se define ahora para no rehacer el modelo de datos después:**
- Un Alumno pertenece a un Plan (o no tiene ninguno activo → acceso restringido).
- El pago lo gestiona el Apoderado, no el Alumno.
- Si hay más de un Alumno en la misma cuenta de Apoderado, cada uno puede tener su propio
  Plan (igual que Wited, que cobra según cantidad de alumnos inscritos).

## Planes de pago (decidido 2026-08-12, tope fijado por el usuario: $19.990 CLP)

El usuario definió el techo de precio: **máximo $19.990 CLP**. Es deliberadamente muy por
debajo de Wited ($89.470-$194.440/mes, incluye clases en vivo) y de Preparación Ética
($20.000+$19.000/mes) porque Logos en el MVP es **autoestudio puro, sin clases en vivo ni
tutorías** — el precio debe reflejar exactamente lo que se entrega, no más. Estructura de 3
opciones, por Alumno, pensada para que el pago por periodos más largos calce con los
**periodos de examinación reales del Mineduc** (abril-junio y octubre, ver
`07-experto-examenes-libres.md`) — un apoderado que sabe cuándo rinde su hijo puede pagar
justo por ese tramo:

| Plan | Precio | Equivale a | Pensado para |
|---|---|---|---|
| **Prueba gratuita** | $0, 7 días | — | Probar la plataforma completa antes de pagar, sin tarjeta de crédito de entrada (reduce fricción de conversión) |
| **Mensual** | $19.990 CLP/mes | — | Familias que quieren empezar ya y decidir mes a mes |
| **Por periodo de examinación** | $89.900 CLP (pago único, ~5 meses de cobertura) | ~$17.980/mes (10% descuento vs. mensual) | La opción recomendada: cubre un periodo de examinación completo (ej. de mayo a septiembre, para el Periodo 3 de octubre) |
| **Anual** | $159.900 CLP (pago único) | ~$13.325/mes (33% descuento vs. mensual) | Familias que ya saben que su hijo rendirá en más de un periodo en el año, o quieren asegurar precio |

Incluido en todos los planes pagos (no hay versión "premium" con más contenido — el
contenido curricular siempre es el mismo completo, lo único que cambia es el compromiso de
tiempo/precio): guía, autoevaluación, pruebas de unidad, exámenes simulacro y plan de
estudio con horario de la(s) asignatura(s) de su curso.

**No incluido en el MVP** (reservado para el "Plan con acompañamiento" de fase posterior,
ver arriba): tutorías humanas, corrección personalizada, apoyo psicopedagógico — ahí sí
tendría sentido un precio mayor al tope de $19.990, cuando se decida activarlo.

**Pasarela de pago:** se define más adelante (el usuario lo confirmó explícitamente como
pendiente) — no bloquea el desarrollo del resto del MVP; la integración de pagos es un
módulo que se conecta al final sin afectar el resto del modelo de datos (`Suscripcion` ya
está diseñada de forma agnóstica al proveedor de pago).

## Tipo de entidad: empresa (decidido 2026-08-12)

El usuario confirmó que Logos se constituirá como **empresa**, no fundación — es coherente
con tener planes de pago desde el inicio. Esto simplifica la vía de financiamiento adicional:
**Start-Up Chile** aplica directamente (requiere empresa constituida), es la vía de
capital/mentoría más establecida para edtech en el país. Los fondos concursables orientados a
fundaciones/ONG (filantropía educacional) dejan de ser la vía principal, aunque fondos de
innovación abiertos a empresas (fondos.gob.cl, CORFO) siguen siendo una opción a monitorear
como financiamiento complementario a los ingresos por planes.

## Se mantiene descartado

- **Publicidad dirigida o con tracking de datos de menores** — no cambia con este ajuste;
  sigue siendo una mala práctica y un riesgo legal bajo la Ley 21.719, independiente de si
  hay planes pagos o no.
- **Financiamiento público per-alumno tipo Stride/Connections Academy** — no existe ese
  mecanismo en Chile para este tipo de examen.

## Fuentes

Wited: wited.com/cl, wited.com/cl/colegio-online/, ayuda.wited.com (artículos de registro y
términos y condiciones) — investigación 2026-08-12. Resto de fuentes (Entreser, Preparación
Ética, Filadd, financiamiento) de la investigación previa del mismo día — ver historial de
la conversación para el detalle completo por afirmación.
