---
título: Análisis de competencia — Brincus (colegio online, competidor directo)
estado: exploración completa + segunda pasada de verificación con capturas reales del usuario,
  correcciones aplicadas (2026-08-14) + tercera pasada en vivo con la cuenta de prueba real
  del usuario, comparando directamente contra Logos (2026-08-15)
---

## Nota de la tercera pasada (2026-08-15) — re-verificado en vivo, no solo releído

Se volvió a entrar con la cuenta de prueba real del usuario (día 1, sigue activa) para
comparar paso a paso contra un recorrido equivalente recién hecho en Logos (4° básico,
asignatura Matemática/Lenguaje). Confirma en vivo, sin cambios, todo lo ya documentado abajo
(onboarding de 7 pasos, check-in emocional, tarjetas de "profesor" con foto por asignatura,
estructura video→cuestionario→guía por sub-tema, cuestionario de 10 preguntas con 5
alternativas A-E y navegación libre, URL pública del PDF de guía sin autenticación).

**Hallazgo confirmado de primera mano, el más relevante para la pregunta de "mucho texto"**:
se descargó y leyó completa la Guía 1.1 de Matemática 4° básico
(`U1_Guía1-1_LecturaYRepresentaciónNúmerosHasta10000_M-4B.pdf`, 3 páginas). **No tiene ni una
sola línea de teoría o ejemplo resuelto** — va directo a 4 ejercicios de completar (a, b, c,
d) y termina en una página de "Resultados" con las respuestas. Es un cuestionario de reforzar,
no material de enseñanza. Comparado con la guía equivalente de Logos: sí es materialmente más
corta, pero solo porque **Brincus mueve toda la enseñanza del concepto al video** (Edith
Giavio explicando en cámara), algo que Logos no tiene ni puede construir sin filmar clases
reales. La comparación justa no es "guía de Logos vs. guía de Brincus", es "guía de Logos
(explicación + ejemplos + práctica en un solo documento) vs. video de Brincus + guía de
Brincus (dos piezas separadas)". Logos ya tiene, dentro de su propia guía, las dos secciones
equivalentes (explicación+ejemplos, y banco de preguntas de autoevaluación) — la mejora
concreta y realista no es "borrar la teoría" sino **presentarlas como dos pasos separados en
vez de un solo scroll largo**, ver recomendación en la conversación de esa fecha.

Brincus (`brincus.com`) es un colegio online chileno que prepara para Exámenes Libres —
competidor directo de Logos School, con más escala y funcionalidad ya construida (30.000+
alumnos rindieron examen libre gratis en 2024 según su propio marketing).

Exploración hecha creando una cuenta de prueba gratuita real (5 días), con un script de
Playwright (headless, controlado por código) que navegó el registro, activación por correo,
login, y las 16 secciones del panel del Alumno más el panel del Apoderado. Capturas de
pantalla y volcados de texto de cada pantalla quedaron en el scratchpad de la sesión que
generó este documento (no versionados en el repo).

**Segunda pasada de verificación**: el usuario complementó esta exploración imprimiendo a PDF
(con "Guardar como PDF" del navegador) 24 pantallas reales de su propia sesión en Brincus,
guardadas en `planificacion/25-brincus-capturas-originales/`. Esto permitió confirmar con contenido
real (no descripciones parafraseadas) el sistema de Logros/avatares completo, la lista real de
Juegos, el Plan Lector, los Tutoriales, y corregir errores de interpretación de la primera
pasada (ver Paso 11 y Paso 11.5 más abajo).

## Paso 1 — Landing / entrada al registro

- URL: `home2.brincus.com/index/reservabrincus` → landing de campaña (probablemente de un
  anuncio de Google Ads, dado el `gclid` en la URL original que compartió el usuario).
- Botón de esa landing lleva a `home2.brincus.com/colegio/crear_gratuito` — el formulario de
  registro real.

## Paso 2 — Formulario de registro (`colegio/crear_gratuito`)

Campos: Email, Nombre Apoderado, Crea tu clave, Repetir Clave, Teléfono (+569 fijo, solo pide
el número), **"¿Cuántos alumnos desea inscribir?"** (select 1-4) → al elegir una cantidad,
revela dinámicamente un bloque por cada alumno: Nombre Estudiante, Plan (select — en la
prueba gratuita viene fijo "Prueba Gratis por 5 días"), Curso (select con Pre Kinder a IV
Medio).

**Idea a rescatar para Logos**: registrar **todos los alumnos de la familia en el mismo
formulario inicial** (hasta 4), no uno a la vez después de crear la cuenta como hace Logos
hoy. Reduce fricción para familias con más de un hijo.

## Paso 3 — Activación por correo (obligatoria)

Al enviar el formulario, Brincus **no da acceso inmediato** — redirige a una pantalla
"Activa tu cuenta" que exige hacer clic en un link de activación enviado al correo, antes de
poder entrar. Sin eso, no hay acceso a nada, ni siquiera a un dashboard vacío.

**Comparación con Logos**: Logos hoy da acceso inmediato sin verificar correo (decisión
consciente, ver `planificacion/10-privacidad-y-datos-de-menores.md`, "sin fricción de
trámite"). Brincus prioriza verificar que el correo es real (probablemente para proteger la
prueba gratuita de abuso/cuentas falsas) por sobre la fricción cero. **A evaluar**: si Logos
en algún momento ve abuso de la prueba gratuita de 7 días, este es el mecanismo que usa un
competidor real para evitarlo.

## Paso 4 — Post-activación: selector de perfil

Tras activar y volver a "Ir a mi cuenta", la URL es `micuenta/seleccionarPerfil` — una
pantalla "¿Quién utilizará la plataforma?" con una tarjeta circular por alumno (avatar +
nombre + curso). Mismo patrón que ya usa Logos (`/selector-perfil`) — confirma que es un
patrón estándar de la categoría, no una idea nueva que rescatar.

## Paso 5 — Login (para sesiones futuras, no la primera vez)

- URL: `home2.brincus.com/index/iniciar_sesion`.
- El formulario pide **RUT o correo indistintamente en el mismo campo** (`onchange=
  "loginRutEmail(...)"`), más contraseña, más checkbox "Recuérdame". Un solo campo que
  acepta dos formatos de identificador, en vez de forzar uno — reduce fricción de "¿con qué
  me registré?".

*(bitácora continúa a medida que avanzo)*

## Paso 6 — Límite de dispositivos simultáneos (hallazgo real, no buscado)

Al intentar loguear con Playwright mientras el usuario todavía tenía sesión abierta en su
propio navegador, Brincus mostró: **"No puedes iniciar sesión debido a que llegaste al
límite de dispositivos simultáneos por cuenta"**, con dos opciones: "Ingresar en este
Dispositivo" (cierra la sesión más antigua) o "Seguir usando en el otro Dispositivo".

**Idea a rescatar para Logos**: un límite de dispositivos simultáneos por cuenta es una
protección real contra que una familia comparta su cuenta de pago con otras — hoy Logos no
tiene ningún control de este tipo. Vale la pena evaluarlo para cuando haya pagos reales
(motivo de negocio, no solo UX).

## Paso 7 — Onboarding con checklist de inducción (¡hallazgo muy fuerte!)

Tras elegir el perfil del alumno por primera vez, Brincus no tira al alumno directo al
dashboard — muestra `/micuenta/onboarding`: "¡Hola, Melody Galvez! Bienvenido/a a Brincus"
con una **checklist de inducción de 7 pasos concretos** a modo de gamificación de la primera
sesión:
1. Ver un video dentro de Mis Asignaturas
2. Realizar un cuestionario
3. Revisar una guía
4. Entrar a Clases en Vivo
5. Entrar a la Biblioteca
6. Hablar con el Profesor Virtual (Brincus AI)
7. Probar un juego educativo

**Idea a rescatar para Logos, alta prioridad**: un onboarding tipo checklist en la primera
sesión de un alumno nuevo es una forma de UX probada para que un niño (no un adulto)
entienda qué puede hacer en la plataforma sin que un apoderado tenga que explicarle. Logos
hoy no tiene nada así — el alumno llega directo a `/alumno/inicio`. Esto también revela de
paso el mapa completo de funcionalidades de Brincus, que sigo explorando a continuación.

**Nota importante de producto de Brincus**: tienen "Brincus AI" (profesor virtual con IA) y
"Clases en Vivo" — dos cosas que Logos no tiene y que son diferenciadores reales de Brincus
frente a Logos (que es autoestudio puro, sin profesor humano en vivo por ahora, ver
`planificacion/00-vision-alcance.md`).

## Paso 8 — Panel del Apoderado (`/cuenta`) — separado del panel del Alumno (`/micuenta`)

Confirma el mismo patrón arquitectónico que ya usa Logos (Apoderado y Alumno como
experiencias/rutas separadas). Sidebar del Apoderado: **Gestión de pagos, Gestión de la
cuenta, Inscripciones, Cursos online, Cambiar datos**.

Pantalla principal "Detalle de tus perfiles": una tarjeta por alumno con:
- Foto/avatar + badge de plan ("Colegio Online Premium")
- Nombre + "Curso 2026: 4° Básico"
- Botones de **upsell de matrícula** directamente en la tarjeta ("Matrícula 2026",
  "Asegura tu matrícula 2027") — venta cruzada visible en el lugar donde el apoderado ya
  está mirando a su hijo, no en una página de planes aparte.
- Fecha de renovación / Tipo de pago (hoy vacíos, cuenta de prueba).
- Nota de aviso: "Recomendamos gestionar su pago antes de la fecha para no perder el acceso
  a tu plan."
- Junto a la tarjeta del alumno: **"+ Nuevo perfil"** — agregar otro hijo sin salir de esta
  pantalla (nombre + curso + botón Crear), no un flujo separado.
- Debajo: "Historial de cobros" (tabla: Fecha, Detalle, Perfil(es) pagado(s), Monto,
  Comprobante) — transparencia total de pagos pasados con comprobante descargable.
- Barra superior fija de campaña: "Matrícula 2027 - Reserva Ahora - Cupos Limitados -
  ¡Matricúlate acá!" — recordatorio de venta permanente, no solo en la landing.

**Ideas a rescatar para Logos** (esto es panel de Admin/Apoderado, área de negocio real):
1. Agregar un alumno nuevo **inline en el mismo panel de "mis perfiles"**, no en una ruta
   aparte (`/agregar-alumno` hoy en Logos) — menos fricción para una segunda inscripción.
2. Mostrar el **historial de cobros con comprobante** directamente al apoderado — hoy Logos
   no tiene ninguna vista de esto para el apoderado (solo existe en el panel de Admin).
   Transparencia de pagos es algo que un apoderado buscaría activamente.
3. CTA de renovación/upsell **en la propia tarjeta del alumno**, con aviso explícito de "se
   pierde el acceso si no pagas a tiempo" — comunica la urgencia sin ser agresivo.

## Paso 9 — "Mis Asignaturas": el mapa completo del panel del Alumno

Sidebar completo del Alumno (16 secciones): Clases en vivo, **Mis asignaturas**, Mi
progreso, **Mis evaluaciones**, Mis Tareas, Comunicación, **Profesor virtual**, Plan de
estudio, **Biblioteca**, **Ensayos**, Logros, Juegos, Tutoriales, Informaciones, Mi perfil,
Inducción Brincus.

**Hallazgos fuertes de esta pantalla:**

1. **Check-in emocional diario** ("¿CÓMO TE SIENTES HOY?"): modal que aparece al entrar,
   pide elegir un emoji entre Feliz / Tranquilo / Normal / Cansado / Preocupado / Triste /
   Frustrado, con el texto "Esto nos ayuda a acompañarte mejor en tu camino". **Idea a
   rescatar, alta prioridad**: Logos no tiene nada de seguimiento socio-emocional. Para
   niños que a veces rinden examen libre por bullying o baja en rendimiento (motivo
   explícito de Brincus en su propio marketing), un check-in de ánimo es coherente con el
   público objetivo y barato de construir (un modal + guardar el dato).

2. **Aviso de días restantes de prueba gratis** ("Tu Prueba Gratis expira en 5 días"),
   visible permanentemente bajo el avatar del alumno en el sidebar, no solo en un correo o
   en el panel de pagos del apoderado. Genera urgencia de conversión sin ser invasivo.

3. **Cada asignatura tiene una "profesora" con foto y nombre** (Historia: Romina Bruna,
   Lenguaje: Valentina Ponce, Matemáticas: Edith Giavio, Ciencias: Isidora Valdés) —
   personifica el contenido grabado/AI como si fuera un profesor real y cercano, con botón
   "¡Conoce a tus profesores!". Refuerza la sensación de "colegio", no de app fría.

4. **"Cursos complementarios"**: Inglés Básico/Intermedio/Avanzado como contenido extra
   fuera de las 4 asignaturas curriculares — mismo patrón "profesor con cara" (foto de un
   mismo profesor de inglés en los 3 niveles). Bonus percibido, sube el valor del plan sin
   ser parte del currículum obligatorio.

5. Botones sueltos en la cabecera: "Mis favoritos" (♥, marcar contenido para volver
   rápido) y "Regalo de contenidos" (🎁, probablemente contenido promocional/bonus).

Sigo ahora a Mis evaluaciones, Biblioteca, Ensayos y Profesor virtual — el corazón de lo que
pediste analizar (tomar pruebas, exámenes, materiales de estudio).

## Paso 10 — "Mis evaluaciones" (el corazón de lo pedido: pruebas y exámenes)

Página con explicación clara al alumno de **4 tipos de evaluación distintos**, cada uno con
su propia tarjeta de color y descripción en lenguaje simple:

1. **Evaluaciones de cierre de unidad** (morado) — "se realizan en clases para identificar
   los nudos de aprendizaje antes de cerrar la unidad".
2. **Simulacros en vivo** (naranjo) — "se rinden en fechas específicas, simulando
   condiciones reales para practicar cómo rendir un examen". **Esto es un simulacro
   PROGRAMADO en el tiempo** (como un evento agendado), no siempre disponible — genera un
   compromiso de fecha, parecido a un examen real de verdad.
3. **Simulacros asincrónicos** (verde) — "ensayos nacionales que reflejan los contenidos
   vistos hasta la fecha, para que practiques bajo condiciones similares a un examen real" —
   disponibles hasta una fecha límite, pero sin horario fijo (asíncronos).
4. **Ensayos** (azul oscuro) — "evaluaciones que puedes rendir en distintos momentos para
   reforzar contenidos de los exámenes libres a tu propio ritmo" — sin ninguna restricción
   de fecha, práctica libre.

También hay un botón "¿Cómo funciona?" junto al título (probablemente un tutorial/modal
explicativo) y un link directo a "Mi progreso / Calificaciones" desde la misma página.

**Ideas a rescatar para Logos — alta prioridad, esto es exactamente lo que se pidió
analizar:**

1. **Separar "simulacro en vivo" (con fecha/hora programada) de "simulacro asincrónico"**
   (disponible hasta una fecha límite, sin horario fijo) — hoy Logos solo tiene un tipo de
   examen simulacro sin fecha, disponible siempre que se cumplan los requisitos de
   cobertura. Un simulacro con fecha fija generaría más fidelidad con el examen real (que
   sí tiene fecha) y crearía un evento que genera compromiso — algo que la app de Logos no
   replica hoy.
2. **Explicar la diferencia entre tipos de evaluación en lenguaje simple, en la propia
   pantalla**, antes de que el alumno elija qué rendir — hoy Logos asume que el alumno ya
   entiende la diferencia entre "prueba de unidad" y "examen simulacro" sin explicarla ahí
   mismo.
3. Un botón "¿Cómo funciona?" contextual en cada sección compleja — patrón de ayuda
   in-context que Logos no usa hoy en ningún lado del panel del Alumno.

Sigo entrando a cada una de las 4 tarjetas.

## Paso 11 — Reproductor de clase (`/micuenta/reproducir/260`) — HALLAZGO MAYOR

Al pinchar la asignatura Matemáticas entra directo a un video de clase: "Lectura y
representación de números hasta el 10.000", 4° Básico - Edith Giavio.

**Estructura de la pantalla:**

- **Video grande a la izquierda** (thumbnail con "Dale clic y comienza tu clase"),
  con acciones: Volver a mis cursos, ♥ Agregar a mis favoritos, 🔴 **"¿Tienes alguna duda?"**
  (botón de ayuda directo desde la clase — probablemente contacta al profesor/tutor), y
  ✅ **"Siguiente"** (avanza a la próxima lección de la ruta sin tener que volver al temario).
- **4 pestañas debajo del video**: Resumen / Preguntas / Evaluar / Errores.
  - Resumen: 1 frase explicando qué se aprende en el video.
  - **Preguntas** (corregido tras revisar el HTML real — mi primera lectura estaba
    equivocada): NO es una pestaña con contenido propio, es un link que saca al alumno de la
    página hacia `/micuenta/chat` — el mismo chat/soporte general de la plataforma, no algo
    específico del video que se está viendo.
  - **Evaluar** (corregido): widget simple de **calificar el video con 1 a 5 estrellas**, sin
    relación con cuestionarios ni con contenido — feedback de calidad del video en sí.
  - **Errores** (corregido, esto era mi error más importante en la primera pasada): es
    **"Reportar Error"** — un botón para reportar un problema de CONTENIDO (video mal
    cargado, guía con un dato incorrecto, etc.), no un repaso personalizado de respuestas
    equivocadas de ningún cuestionario. Confirmado además que **está deshabilitado durante la
    prueba gratuita**: el propio botón muestra "esta opción solo está disponible para
    usuarios con perfil activo. No aplica para la prueba gratis" — Brincus limita
    deliberadamente esta función a cuentas pagadas.
- **"Temario" a la derecha**, con 3 sub-pestañas: **Unidades / OA / Exámenes Libres** — y
  dentro de Unidades, un **buscador de contenido por palabra** más una unidad expandible
  ("1. Números hasta 1000 y operatoria") que lista, en orden, la secuencia pedagógica
  completa de esa unidad:
  - `1.1 [Video] Lectura y representación... (Materia) — 9 min` (el video actual, resaltado)
  - `Cuestionario - Lectura y representación... — "Ver intentos"` (quiz específico de ESE
    video, con historial de intentos anteriores)
  - `Guía 1: Lectura y representación...` (documento de guía, aparte del video)
  - `1.2 [Video] Ejercicios: Lectura y representación... (Ejercicios) — 14 min` (un SEGUNDO
    tipo de video, de ejercicios prácticos, distinto al video de materia)
  - `1.3 [Video] Conteo de números... (Materia) — 9 min`
  - `Cuestionario - Conteo...`, `Guía 1: Conteo...`, `1.4 [Video] Ejercicios: Conteo...`
  - `1.5 [Video] Valor posicional... (Materia) — 13 min`
  - ...continúa

**Esto revela la secuencia pedagógica real de Brincus por sub-tema**: video de materia (con
duración visible) → cuestionario de ese video específico (con historial de intentos) → guía
escrita → video de ejercicios → repite para el siguiente sub-tema. Mucho más granular que
Logos, que hoy tiene un solo bloque de "guía" + "banco de autoevaluación" por OA completo,
sin dividir en sub-temas con video propio.

**Ideas a rescatar para Logos — muy alta prioridad:**

1. **Mostrar la duración de cada video/actividad** (ej. "9 minutos") en la lista de
   contenido — ayuda al alumno (y al apoderado planificando el horario de estudio) a saber
   cuánto tiempo le va a tomar antes de empezar.
2. **Historial de intentos por cuestionario** ("Ver intentos") visible directamente junto al
   cuestionario en el temario, no solo en una sección de "Mis Notas" aparte.
3. **Botón de ayuda contextual dentro de la clase** ("¿Tienes alguna duda?") — Logos no
   tiene ningún mecanismo de ayuda mientras el alumno está estudiando una guía.
4. **Botón "Siguiente" para avanzar linealmente** por la ruta de aprendizaje sin volver al
   listado — hoy en Logos, terminar de estudiar un OA no ofrece un camino directo al
   siguiente.
5. **Botón "Reportar Error" de contenido, limitado a cuentas pagadas** — un canal simple para
   que un alumno/apoderado avise de un error real en un video o guía, sin necesidad de correo
   ni ticket externo. Barato de construir, y Brincus lo usa además como palanca de
   conversión (deshabilitado en la prueba gratis).
6. **Buscador de contenido por palabra** dentro del temario de una asignatura — Logos no
   tiene búsqueda dentro del contenido de estudio hoy.

## Paso 11.5 — Cuestionario real, rendido de principio a fin (verificado, no inferido)

Corrección directa al feedback del usuario ("no notaste prácticamente nada"): esto es lo que
realmente pasa al tomar un cuestionario, verificado haciendo clic en cada paso con Playwright,
no leyendo copy de marketing.

- El botón "Cuestionario" de una lección dispara una función JS (`intentoDiario(id_video)`)
  que hace un POST a `/micuenta/intento_diario` y decide server-side: si no hay intento
  previo, abre `/cuestionario/iniciar/{id_video}` (cuestionario nuevo); si ya había uno en
  curso, muestra un modal ("Tienes un intento en progreso") con un link "Continuar
  cuestionario" hacia `/cuestionario/resumen/{intento_id}` — **el cuestionario recuerda el
  intento a medio hacer y lo retoma**, no lo reinicia.
- Pantalla de intro: "Cuestionario 1 | 10 preguntas" antes de empezar.
- Cada pregunta tiene **5 alternativas (A a E)**, no 4 — un detalle simple que cambia el
  diseño de la grilla de opciones respecto a lo que suele usarse.
- **Barra de navegación por número de pregunta** (1 a 10, se puede saltar a cualquiera en
  cualquier momento, no es estrictamente lineal).
- **"Finalizar intento" disponible en todo momento**, no solo al llegar a la última
  pregunta — el alumno puede cortar el cuestionario cuando quiera y ya queda con lo que
  alcanzó a responder.
- Cada pregunta tiene su propio botón **"Notificar error"** (mismo patrón de reporte de
  contenido que en el video, pero a nivel de pregunta individual).
- Al finalizar, modal de confirmación: "¿Estás seguro que deseas terminar el intento?".
- **Pantalla de resultado**: "DETALLES DEL INTENTO ACTUAL" con "Puntaje obtenido: X de 10
  correctas", seguido de "RESUMEN DEL INTENTO ACTUAL" — una tabla con una fila por pregunta,
  columnas Resultado (correcta/incorrecta) y Revisión (link para revisar esa pregunta
  puntual).

**Ideas a rescatar, alta prioridad — esto es exactamente el corazón de "tomar pruebas" que se
pidió analizar:**

1. **Retomar un intento a medio hacer en vez de reiniciarlo** — si un alumno cierra la
   pestaña a mitad de un cuestionario, Brincus lo trae de vuelta exactamente donde quedó.
   Logos hoy no tiene esta persistencia de intento en curso.
2. **Navegación libre entre preguntas + "Finalizar" disponible siempre** — más flexible que
   forzar orden estrictamente lineal, se siente menos como un examen rígido y más como
   práctica.
3. **Resumen final con una fila por pregunta (correcta/incorrecta + link de revisión)** —
   feedback granular inmediato, no solo una nota global.
4. **"Notificar error" a nivel de pregunta individual**, no solo a nivel de video — permite
   detectar preguntas mal calibradas del banco con mucha más precisión.

## Nota honesta sobre la Guía (no verificado del todo)

Se ubicaron URLs reales de guías (`/biblioteca/material_curso/{id}/{id}`) desde el HTML del
temario, pero al navegar a una con la cuenta de prueba, la página cargó solo el layout base
(sidebar + cabecera de "Progreso de tu inducción") sin mostrar el documento de la guía en sí
en el volcado de texto capturado. **Esto ya se verificó — era JS pesado, no un límite del
trial**: la página embebe el PDF con el **Adobe Document Cloud View SDK** (un iframe de
`documentservices.adobe.com`), y el volcado de texto plano no capturaba lo que corre dentro de
ese iframe. Interceptando las peticiones de red se encontró la URL real del PDF servido:

```
https://home2.brincus.com/public/guias2025/U1_Guía1-1_LecturaYRepresentaciónNúmerosHasta10000_M-4B.pdf
```

**Hallazgo de seguridad/arquitectura, no menor**: esta URL está en `/public/` y **se pudo
descargar directamente con `curl`, sin sesión ni cookies de login** — el control de acceso de
Brincus a las guías vive solo en la capa de UI (mostrar/ocultar el link dentro de la cuenta),
no en el archivo mismo. Cualquiera con la URL exacta puede bajar la guía completa sin pagar ni
tener cuenta. **Para Logos**: si se sirven guías como PDF descargable, hay que decidir
conscientemente si van en un bucket público (como Brincus, más simple, más rápido, pero
regalable) o detrás de una URL firmada/temporal (más trabajo, pero controla mejor el acceso a
contenido pago) — no asumir el patrón de Brincus como "la forma correcta" sin decidirlo.

**Formato real de una Guía de Brincus** (2 PDFs reales descargados y leídos completos, no
solo el nombre del archivo):
- Encabezado en cada página: franja de color con "UNIDAD N" + nombre de la unidad + número de
  guía (ej. "Guía 1.1"), más una insignia circular con el curso ("4° BÁSICO") arriba a la
  derecha.
- Título de la guía en un recuadro con borde punteado, con tipografía tipo manuscrita/informal
  (no la misma fuente del resto del documento) — refuerza sensación "hecho a mano para
  niños", no un documento corporativo.
- **Es una guía de EJERCICIOS (formato "hoja de trabajo para imprimir"), no un texto
  explicativo** — no hay párrafos de teoría ni ejemplos resueltos antes de las preguntas, va
  directo a una lista numerada de ejercicios con sub-ítems a), b), c)... y espacios en blanco
  o tablas para completar a mano.
- Footer con logo de Brincus + número de página, en todas las páginas.
- **Última página siempre es "Resultados"**: un recuadro con borde punteado que contiene las
  respuestas correctas de cada ejercicio de la guía — el PDF se autocontiene, no hay que
  volver a la plataforma para saber si algo estaba bien.
- Botón "Imprimir" visible junto al visor (aunque no se confirmó si dispara `window.print()`
  del navegador o una descarga — el href capturado estaba vacío, sugiere que es JS inline).

**Hallazgo de calidad de contenido de Brincus, no de Logos** (vale la pena registrarlo como
lección, no para copiar): la segunda guía descargada, "Guía 1.5 — Valor posicional:
descomposición estándar y expandida", nominalmente de la Unidad 1 de 4° Básico ("Números hasta
10 000 y operatoria" — así dice el propio encabezado), contiene ejercicios con números como
"607 mil millones 43 mil 17" (607.000.043.017) — **muy por encima del alcance declarado de la
propia unidad** (números hasta 10.000). Parece un error real de contenido (probablemente una
guía de un nivel superior mal etiquetada o copiada). **Lección para Logos**: con 2.917
preguntas y contenido para 12 cursos, un control de calidad que verifique que el rango
numérico/dificultad de cada ítem calza con el nivel declarado es barato de automatizar
(validación simple de rango) y evita este tipo de error, que en Brincus llegó a producción.

## Paso 11.6 — Las 3 rutas del Temario (Unidades / OA / Exámenes Libres) — verificado, corrige un pendiente

Las 3 sub-pestañas del Temario (mencionadas en el Paso 11 pero nunca abiertas hasta ahora) son
**3 formas distintas de recorrer exactamente el mismo contenido**, no 3 contenidos distintos:

- **Unidades**: el orden pedagógico normal (Unidad 1, 2, 3... como se enseñaría en clase).
- **OA**: el mismo contenido, reordenado por Objetivo de Aprendizaje individual en vez de por
  unidad — Brincus lo explica así en la propia pantalla: "Es el mismo contenido de Unidades,
  pero organizado por Objetivos de Aprendizaje (...) La materia es exactamente la misma; solo
  cambia la forma de ordenarla. Elige la ruta que te acomode más y avanza solo en una ruta por
  asignatura" (esto último es clave: **avisa explícitamente que no hay que avanzar por las dos
  rutas a la vez**, para no confundir al alumno pensando que es contenido duplicado).
- **Exámenes Libres**: una **versión resumida**, alineada al temario oficial del Mineduc para
  el examen — salta directamente entre los números de OA que sí se examinan (en la cuenta de
  4° básico salta del OA 1 al 3, 5, 6, 7, 8, 9, 13, 14... sin los OA intermedios). Copy
  explícito en pantalla: "Si necesitas avanzar rápido, puedes usar esta ruta; de lo contrario,
  recomendamos estudiar todo el contenido desde la sección Unidades" — la presentan como el
  atajo para quien tiene poco tiempo, no como la ruta recomendada por defecto.

**Idea a rescatar, alta prioridad**: Logos ya tiene el concepto de "temario oficial vs.
contenido completo" en el propio dato (los 408 OA con indicadores de evaluación, ver
`Temarios/analisis/`), pero no una forma de que el alumno elija explícitamente entre "quiero
todo el contenido en orden pedagógico" vs. "solo quiero lo que se examina, lo más rápido
posible". Ofrecer esta elección explícita (con la misma advertencia de "elige una ruta, no
mezcles las dos") es una idea de UX barata porque **no requiere contenido nuevo**, solo una
forma distinta de navegar el contenido que ya existe.

## Paso 11.7 — Facsímil real, rendido hasta la primera pregunta (verificado, no inferido)

Se abrió `/micuenta/examenes_libres` (la URL real detrás del ítem "Ensayos" del sidebar —
distinto del nombre que muestra el menú) y se expandió el acordeón "MOSTRAR ENSAYOS" de
Matemáticas, algo que en la primera pasada de exploración nunca se logró (0 resultados en el
locator). Esta vez sí:

- **Cada asignatura (Lenguaje, Matemáticas, Ciencias, Historia, Inglés) tiene 5 Facsímiles**,
  cada uno de **40 preguntas** (el doble que un cuestionario de video normal, que es de 10) —
  y cada facsímil tiene su propio "Ver intentos", igual que los cuestionarios de video.
- Se entró a un Facsímil N°1 real (`/exameneslibres/introduccion/97` →
  `/exameneslibres/pregunta/32813/575`): misma mecánica ya documentada del cuestionario normal
  (navegación 1 a 40, 5 alternativas A-E, "Finalizar intento" disponible siempre, "Reportar"
  error por pregunta), **más un elemento nuevo que el cuestionario de video no tiene: "Ver
  video asociado" junto a cada pregunta** — un link directo de vuelta a la lección específica
  que cubre el contenido de esa pregunta puntual.

**Idea a rescatar, alta prioridad**: enlazar cada pregunta de un examen simulacro/facsímil
directamente al video/guía del OA correspondiente, para que el alumno pueda ir a repasar sin
tener que buscar manualmente el contenido — hoy en Logos el flujo de revisión de un intento no
tiene este atajo directo.

## Paso 11.8 — Profesor Virtual: probado con una pregunta real, no solo descrito

Se entró al chat de Matemáticas (Prof. Euler) y se verificaron elementos que la primera pasada
no había capturado:

- **3 modos activables/desactivables** (toggle, todos "apagados" por defecto): **Práctica
  guiada** ("aprender algo paso a paso con ejercicios cortos"), **Prueba de práctica**
  ("simular una prueba con preguntas de alternativas"), **Aprender más** ("explorar temas que
  te dan curiosidad") — el profesor virtual no es solo un chat libre, tiene modos de
  interacción con propósito pedagógico distinto cada uno.
- **"Mis metas con el Profesor Virtual"**: un campo donde el alumno escribe explícitamente qué
  quiere aprender o mejorar, y el copy dice que "el profesor usará estas metas para explicarte
  y practicar contigo" — personalización declarada por el propio alumno, no inferida solo del
  progreso.
- **Se envió una pregunta real ("¿Cuánto es 7 + 5?") y se recibió una respuesta real de IA**,
  confirmando que es un modelo funcionando de verdad, no una maqueta: *"¡Muy bien! 7 + 5 = 12.
  Una forma fácil de verlo: suma 3 a 7 para llegar a 10, y luego suma los 2 que quedan: 10 + 2
  = 12. También puedes contarlos con los dedos o dibujar 7 y 5 puntitos y unirlos. ¿Quieres
  practicar otro sumando parecido?"* — tono cercano, pedagógico (dos estrategias de cálculo
  mental, no solo el resultado), y termina invitando a seguir practicando.

**Idea a rescatar, alta prioridad para cuando Logos construya su Profesor IA (Fase 2, ver
`planificacion/27-plan-incorporacion-hallazgos-brincus.md`)**: los 3 modos con propósito
distinto y el campo de "metas propias" son más ricos que un chat genérico de dudas — vale la
pena diseñar el Profesor IA de Logos con esta misma estructura desde el principio, no como un
chat plano.

## Paso 12 — Recorrido sistemático de TODO el sidebar del Alumno (16 secciones)

### Notificaciones (campana 🔔 → "Ver todo")
3 pestañas: **Notificaciones / Preguntas y Respuestas / Errores reportados** (las 3 vacías
en esta cuenta nueva). "Preguntas y Respuestas" sugiere un historial centralizado de dudas
que el alumno hizo (probablemente al Profesor Virtual o a un profesor humano), separado de
"Errores reportados" (reportar un bug/problema de contenido, no errores de un cuestionario).

### Clases en vivo
Calendario real (vista Hoy/Semana/Mes) de clases en vivo por asignatura, con "Descargar
Horario". Para la cuenta de prueba, aparece un banner específico: **"PRUEBA 3 CLASES
GRATIS"** — durante el trial, el alumno puede elegir libremente 3 clases en vivo reales para
asistir como invitado, con un código de conducta explícito (llegar a tiempo, cámara
encendida si es posible, no interrumpir). Clases grabadas quedan disponibles después en
Biblioteca.

**Idea a rescatar**: ofrecer una "muestra" muy concreta y acotada (3 clases) durante el
trial, en vez de solo dar acceso genérico a "todo por 5 días" — hace tangible el valor antes
de pagar.

### Mi progreso
2 vistas: **"Progreso" (Ruta de aprendizaje** — avance en contenido asincrónico y
cuestionarios) y **"Calificaciones" (Notas por asignatura** — detalle por tipo de
evaluación). Separación clara entre "cuánto contenido llevo visto" y "qué notas tengo".

### Mis Tareas
Tareas asignadas por un profesor humano (ligadas a Clases en Vivo), con entrega dentro de un
plazo para recibir retroalimentación — funcionalidad de colegio real, no aplica a Logos
(autoestudio puro, sin profesor).

### Comunicación
Mensajería directa con profesores: **Mensajes sin leer / leídos / enviados**, botón
"+ Nuevo mensaje". Un canal de comunicación 1 a 1 alumno↔profesor real, dentro de la
plataforma (no por WhatsApp/correo externo).

### Profesor virtual — IA por asignatura, con personaje propio
"Conoce a tus profesores virtuales de Brincus 🤖💙 — Entrenados con Inteligencia Artificial y
contenido oficial del MINEDUC, disponibles 24/7". **Un "profesor" de IA con nombre y
personalidad distinta por asignatura**: Sra. Gramática (Lenguaje), Prof. Euler (Matemáticas),
Sr. Williams Cronos (Historia), Prof. Darwin (Biología), Dra. Naturaleza (Ciencias), Dr.
Albert (Física), Dra. Molécula (Química). **Límite visible en la prueba gratuita: "5
preguntas disponibles este mes"** — el uso de IA está limitado/medido incluso en la versión
paga más básica, evidencia de que gestionan el costo de inferencia de IA como un recurso
limitado por plan.

**Ideas a rescatar, alta prioridad**: 1) un tutor IA con personaje/nombre por asignatura es
mucho más cercano para un niño que un chat genérico; 2) limitar las preguntas de IA por mes
es el mecanismo real que un competidor usa para controlar costo de LLM — relevante si Logos
construye algo así.

### Biblioteca
4 categorías de recursos: **Grabación de clases en vivo, PPT de clases, Guías de apoyo,
Libros ministeriales** (los textos oficiales del MINEDUC en PDF/digital). Va más allá del
contenido propio de Brincus — agrega también el material oficial del Estado como recurso
descargable en un solo lugar.

### Ensayos (Facsímiles) — distinto de "Mis evaluaciones"
Los **"Facsímiles"** son un tercer concepto de evaluación, aparte de los 4 de "Mis
evaluaciones": cubren **el temario ANUAL COMPLETO** (no solo lo visto hasta la fecha), estilo
"preuniversitario", pensados para medir avance de nota a lo largo de todo el año.
Explícitamente aclaran en la propia página que esto es distinto de los simulacros de Clases
en Vivo. Organizados por asignatura (Lenguaje, Matemáticas, Ciencias, Historia, Inglés), cada
una con su acordeón "MOSTRAR ENSAYOS".

**Idea a rescatar**: Brincus separa muy claramente evaluación de "lo que ya viste" (formativo,
progresivo) de evaluación de "todo el año" (sumativo/preparación real de examen) — y lo
explica con texto simple al alumno, en vez de asumir que entiende la diferencia. Logos podría
adoptar exactamente este lenguaje ("evalúa lo que ya estudiaste" vs. "practica el examen
completo, aunque no hayas visto todo").

### Logros — gamificación completa (confirmado con la lista real de logros, no solo la intro)
Sistema de **niveles + XP + avatares desbloqueables**: Bronce (5 XP, fácil), Plata (15 XP,
moderado), Oro (50 XP, difícil), Platino (200 XP, muy difícil). Cada 50 XP sube un nivel, lo
que desbloquea nuevos avatares premium. Todo alumno arranca en "Nivel 1, 0 XP".

El listado real de logros (~40 ítems, con % de alumnos que ya lo tienen, visible como
motivador social tipo "X% de los jugadores ya lo desbloqueó") cubre varias familias de
comportamiento, no solo "avanzar contenido":
- **Constancia de sesión**: iniciar sesión 2/5/10 días consecutivos, o 5/10/50/364 veces en
  total (el de 364 veces da Platino/200 XP — literalmente "todos los días del año").
- **Tiempo de uso**: sesión más larga de 30min/2h/4h; tiempo total acumulado de 2h/12h/36h/100h.
- **Consumo de contenido**: reproducir 3/9/20 cápsulas en un mismo día, o 5/25/100/1000 en
  total; ver 1/15/50 materiales de apoyo.
- **Avance curricular**: 15%/50%/100% de avance en una asignatura, y el mismo umbral pero "en
  TODAS las asignaturas del año actual" (logro más difícil, empuja a no abandonar una sola
  materia a medio camino).
- **Cuestionarios**: 1/3/10 mini-tests nuevos en un mismo día, o 5/15/50 en total.
- **Clases en vivo**: asistir 1/5/15 en total, o 2 en un mismo día.

**Idea a rescatar, prioridad media-alta**: Logos hoy no tiene NINGÚN sistema de gamificación
— ni puntos, ni niveles, ni avatares, ni logros. Lo valioso de copiar no es solo "poner XP",
es que los logros de Brincus premian explícitamente **hábitos** (racha de días, tiempo de
sesión) además de logros de contenido — refuerza constancia, que es justamente lo que un
alumno de examen libre autodidacta necesita más.

### Juegos (11 confirmados, lista real)
2048, Ajedrez, Crucigrama, Damas, Pasapalabra, Dominó, Mahjong, Blockbuster Puzzle, Tic Tac
Toe, Falling Cubes, Mill Game. Función de retención/descanso, no de contenido curricular —
presentados como parte de "aprender jugando" aunque en la práctica sean juegos de mesa
clásicos con skin educativo (imágenes de stock genéricas, no arte propio de Brincus).

### Informaciones (confirmado con contenido real de 2 de las 4 sub-secciones)
Centraliza 4 recursos prácticos para la familia en un solo lugar: **Temarios oficiales 2026,
Útiles Escolares** (lista de materiales que hay que comprar), **Plan Lector**, **Planificador
de estudio**. Es información que hoy un apoderado de Logos tendría que buscar aparte (o no
existe, como la lista de útiles escolares).

El **Plan Lector de 4° Básico real** son 4 libros, en una tabla con columnas Título / Autor /
Editorial / botón "Ver libro": *Trece casos misteriosos* (Jacqueline Balcells, SM), *Las
Brujas* (Roald Dahl, SM), *Papelucho en la clínica* (Marcela Paz, Alfaguara), *El príncipe y
el mendigo* (Mark Twain, Nueva Biblioteca Billiken). **Idea a rescatar**: un plan lector
curado por nivel, con editorial y link, es contenido de valor percibido alto y costo de
mantención bajo — Logos no tiene nada de plan lector hoy pese a tener Lenguaje como
asignatura central.

### Mi perfil
Edición simple: nombre, año académico (curso), foto de avatar. La colección de avatares
confirma el sistema de "Logros": 5 familias de avatar (monstruo clásico, huevo evolutivo,
etc.) × 4 niveles cada una, todos bloqueados salvo Nivel 1 al partir — más una fila aparte de
"Avatares Clásicos" (5 monstruos simples) disponibles desde el día uno sin requisito. Combina
bien recompensa progresiva (avatares evolutivos) con personalización inmediata (clásicos
gratis) para que la cuenta nueva no se sienta vacía.

### Plan de estudio (`/plan_estudios`, fuera del namespace `/micuenta`)
Planificador personal con **vista Semanal / Mensual / Anual / Personalizado** y un resumen de
tareas por estado: **Finalizadas / Pendientes / No finalizadas**. Permite agregar contenido
de años anteriores para repasar, no solo del año actual — algo que Logos no contempla hoy
(el plan de estudio de Logos está acotado al nivel actual del alumno).

## Paso 13 — Índice de Tutoriales (aportado por el usuario, navegación manual)

El usuario navegó manualmente la sección "Tutoriales" (que mi script no pudo abrir) y pasó el
listado completo de títulos. Revela varias funcionalidades que no había encontrado
explorando por mi cuenta:

**Tutoriales del uso de la plataforma** (lista completa): ¿Cómo iniciar sesión? / ¿Cómo
renovar tu suscripción? / ¿Cómo pagar tu cuota? / ¿Cómo imprimir una guía? / **¿Cómo
inscribir los clubes de interés?** / ¿Cómo ver las clases en vivo grabadas? / **¿Cómo revisar
los informes de avance?** / **¿Cómo descargar el certificado?** / ¿Dónde encuentro los libros
ministeriales? / ¿Qué encuentro en informaciones? / ¿Cómo le escribo a mis profesores de
clases en vivo? / ¿Cómo reviso las estadísticas de mi hijo/a? / **¿Cómo cambiar tu año
escolar? Plan Básico y Full** / Plan Básico y Full (Cápsulas, Videos y Cuestionarios) / ¿Cómo
ingresar a las clases en vivo? / **¿Cómo doy ideas para mejorar la plataforma?** / **¿Cómo me
inscribo a las comunidades de WhatsApp?** / ¿Cómo funciona el Profesor Virtual? / ¿Cómo
funciona el Buzón de Tareas? / ¿Cómo funciona el Plan de Estudios?

**Tutoriales de cada funcionalidad** (lista de módulos, confirma nombres oficiales): Mis
Asignaturas, Clases en vivo, Buzón de Tareas, Comunicación, Profesor Virtual, Plan de
estudio, Logros, Biblioteca, **Estadísticas**, Informaciones, Ensayos.

**Hallazgos nuevos que esto revela (no visibles navegando la cuenta vacía):**

1. **Clubes de interés**: una función de inscripción a clubes/actividades extracurriculares
   por interés — no alcancé a verla en el sidebar de una cuenta recién creada (probablemente
   aparece solo con un plan pagado o más avanzado, o está bajo otra sección que no mapeé).
2. **Certificado descargable — confirmado el nombre exacto** en el PDF que aportó el usuario:
   el tutorial se titula literalmente "¿Cómo descargar el Certificado de **Alumno
   Regular**?". Esto es clave: **no** es un certificado que reemplace ni certifique el
   Examen Libre en sí (ese lo emite Mineduc/la entidad examinadora, no Brincus) — es un
   "certificado de alumno regular" tipo el que emite cualquier colegio para trámites
   (subsidios, seguros, etc.), aprovechando que Brincus se posiciona como "colegio online".
   **Idea a rescatar, bajo costo**: Logos podría emitir un documento equivalente
   ("certificado de alumno inscrito en Logos School") sin que eso implique ningún cambio de
   alcance legal — es solo un PDF generado con nombre/curso/fecha.
3. **Informes de avance descargables** para el apoderado — un documento (PDF probablemente)
   con el progreso del hijo, más formal que solo mirar una pantalla de estadísticas.
4. **Comunidades de WhatsApp**: Brincus arma comunidades por curso/nivel en WhatsApp, fuera
   de la propia plataforma — una capa de comunidad/soporte entre apoderados que compite
   directamente con el canal de comunicación oficial dentro de la app.
5. **Buzón de sugerencias** ("¿Cómo doy ideas para mejorar la plataforma?") — canal explícito
   y visible para que un usuario proponga mejoras, no escondido en un correo de soporte.
6. **Dos planes con distinto contenido**: "Plan Básico" y "Plan Full" — el Full parece incluir
   más (posiblemente Clases en Vivo + Profesor Virtual con más cupo), el Básico solo
   "Cápsulas, Videos y Cuestionarios" (contenido grabado, sin clases en vivo). Confirma que
   la segmentación de planes de Brincus no es solo por cantidad de alumnos (como hoy Logos
   planea) sino por **profundidad de funcionalidad**.
7. **"Estadísticas"** aparece como categoría propia en el índice de tutoriales, separada de
   "Mi progreso" que sí alcancé a explorar — probablemente es la vista específica que usa el
   Apoderado para ver el avance de su hijo (distinta del "Mi progreso" que ve el Alumno).

**Ideas a rescatar de este paso**: el buzón de sugerencias explícito (bajo costo, alto valor
de percepción de cercanía) y el informe de avance descargable en PDF para el apoderado son
las dos más baratas de evaluar para Logos. Las comunidades de WhatsApp son una estrategia de
retención/comunidad que no depende de desarrollo de producto — vale la pena como idea de
negocio, no de ingeniería.

## Resumen — lo más importante a rescatar (orden de prioridad sugerido)

1. **Cuestionario que retoma el intento en curso + navegación libre entre preguntas +
   resumen final con detalle pregunta por pregunta** (Paso 11.5) — es el flujo verificado de
   principio a fin, y es directamente el "tomar pruebas" que motivó todo este análisis.
2. **Gamificación (Logros: XP, niveles, avatares, premiando hábito y no solo contenido)** —
   ausente por completo en Logos, estándar en la categoría, alto impacto en retención de
   niños.
3. **Onboarding con checklist de primera sesión** — guía al alumno nuevo sin depender de que
   el apoderado le explique la plataforma.
4. **Separación clara entre evaluación formativa (lo ya visto) y evaluación sumativa (todo el
   año, tipo facsímil)**, explicada en lenguaje simple en la propia pantalla.
5. **Simulacro con fecha programada ("en vivo")** además del simulacro siempre-disponible que
   ya tiene Logos — genera compromiso real de fecha, como el examen de verdad.
6. **Check-in emocional diario** — coherente con el público objetivo (niños que a veces
   rinden examen libre por bullying/baja autoestima académica).
7. **Duración visible de cada video/actividad** en el listado de contenido de una unidad.
8. **Historial de intentos visible junto a cada cuestionario**, no solo en una sección
   separada de notas.
9. **Botón de ayuda contextual ("¿Tienes alguna duda?")** disponible mientras se estudia, y
   "Notificar error" a nivel de pregunta individual dentro de un cuestionario.
10. **Plan Lector curado por nivel** (título/autor/editorial/link) — contenido de alto valor
    percibido y bajo costo de mantención, hoy inexistente en Logos pese a tener Lenguaje
    como asignatura central.
11. **Certificado de "alumno regular" descargable** (PDF simple con nombre/curso/fecha) — no
    reemplaza el trámite oficial de Mineduc, es solo un documento de conveniencia para la
    familia.
12. **Agregar un alumno nuevo inline** en el panel del apoderado, sin salir a otra ruta.
13. **Historial de pagos con comprobante**, visible para el apoderado (hoy solo existe para
    Admin en Logos).
14. **Biblioteca de recursos descargables** (incluyendo libros oficiales del MINEDUC en
    PDF) como sección aparte del contenido propio.
15. **Límite mensual de preguntas a un tutor IA** — relevante solo si Logos construye un
    tutor con IA en el futuro, como forma de controlar costo.

## Lo que Brincus tiene y que Logos deliberadamente NO tiene hoy (no es una omisión, es una
decisión de alcance ya tomada)

- Profesores humanos en vivo + tareas + mensajería 1 a 1 (Logos es autoestudio puro por
  decisión, ver `planificacion/00-vision-alcance.md`).
- Tutor de IA por asignatura (Logos no tiene IA integrada todavía).
- Tienda/colegio con matrícula anual formal, con foco en ser percibido como "colegio online"
  (Logos se posiciona como plataforma de apoyo de estudio, no como colegio).

Estas diferencias no son necesariamente "brechas a cerrar" — son decisiones de producto que
ya se tomaron con fundamento (ver CLAUDE.md, "Autoestudio primero"). Se documentan acá solo
para que quede explícito qué SÍ es una elección consciente, no un olvido.
