---
título: Seguridad y casos borde
estado: especificación (2026-08-12) — no negociable, aplica desde el primer commit
última actualización: 2026-08-12
---

## Postura honesta sobre seguridad

Ningún sistema es "imposible de hackear" — quien lo prometa está mintiendo. Lo que sí se
puede y se debe hacer es seguir buenas prácticas estándar de la industria que hacen que un
ataque sea difícil, caro y detectable rápido, y tener monitoreo (Sentry/UptimeRobot, ver
`17-infraestructura-y-entornos.md`) para reaccionar rápido si algo pasa. Eso es lo que se
implementa desde el primer commit, no como algo a agregar "después".

## Medidas de seguridad (aplican desde el Paso 1 del desarrollo)

| Riesgo | Medida |
|---|---|
| Contraseñas robadas si hay una filtración | Nunca se guardan en texto plano — se guarda solo un hash (bcrypt/argon2). Ni el equipo del proyecto puede ver la contraseña real de nadie. |
| Inyección SQL | Se usa un ORM (SQLModel/SQLAlchemy) con consultas parametrizadas siempre — nunca se arma una consulta SQL pegando texto del usuario directamente. |
| XSS (código malicioso inyectado en un campo de texto) | Angular escapa el HTML por defecto en todo lo que se muestra en pantalla — no se usa `innerHTML` directo con datos de usuario sin sanitizar. |
| CSRF | Tokens de autenticación (JWT) enviados por header, no por cookie automática — reduce la superficie de este ataque de forma estructural. |
| Fuerza bruta contra el login | Límite de intentos de login por IP/cuenta en un periodo corto (rate limiting en el backend), con backoff progresivo. |
| Registro masivo automatizado (bots) / abuso que genere costos inesperados | **Cloudflare Turnstile** (gratis, ya que el frontend corre en Cloudflare Pages) en el formulario de registro y login — verifica que quien se registra es una persona, sin el mal UX de un captcha tradicional con imágenes. |
| Costos inesperados por tráfico anómalo | Alertas de presupuesto activadas en Render y Neon (ambos lo permiten en su plan gratuito/inicial) — aviso automático si el uso se dispara, antes de que se convierta en una sorpresa en la factura. |
| Tráfico malicioso masivo (DDoS) | Cloudflare está delante del frontend por diseño (ver infraestructura) y tiene protección básica anti-DDoS incluida gratis; se evalúa poner también el backend detrás de Cloudflare (proxy) cuando se defina el dominio final. |
| Secretos (contraseñas de base de datos, llaves de API) expuestos | Nunca se suben al repositorio — viven solo en variables de entorno de cada ambiente (Render/Neon), y `.env*` queda en `.gitignore` desde el primer commit. |
| Dependencias con vulnerabilidades conocidas | Se revisan periódicamente con herramientas gratuitas (`pip-audit` para Python, `npm audit` para Angular) — parte de la rutina de mantención, no un evento único. |
| Todo el tráfico | HTTPS obligatorio en ambos ambientes (Render y Cloudflare Pages lo dan por defecto, sin configuración extra). |

## Casos borde de la experiencia de rendir una evaluación

Detallado también en `12-motor-de-evaluacion.md` (actualizado 2026-08-12) — se consolida
aquí la lista completa de casos contemplados, tal como pidió el usuario:

1. **El alumno deja preguntas sin responder y presiona "Entregar"**: el sistema bloquea el
   envío real y muestra un aviso explícito de qué preguntas faltan, con la opción de volver
   a revisarlas o confirmar el envío igual — el botón final de envío solo se habilita después
   de esa confirmación (ver detalle en `12-motor-de-evaluacion.md`).
2. **El alumno sale de una evaluación a medio camino y vuelve a entrar** (cierra la pestaña,
   se corta la conexión, se le apaga el dispositivo): no se pierde el progreso. Cada
   respuesta se guarda automáticamente al momento de responderla (no solo al final) — al
   volver a entrar a esa misma evaluación, continúa exactamente donde quedó.
3. **El examen simulacro se agota en tiempo**: se envía automáticamente lo que esté
   respondido hasta ese momento, sin excepción — así se comporta el examen real, y así debe
   sentirse la simulación.
4. **El cronómetro no se puede "hacer trampa" cambiando la hora del dispositivo**: el tiempo
   restante se valida contra la hora del servidor (cuándo se inició realmente el intento),
   no solo contra un contador corriendo en el navegador del alumno.
5. **El alumno abre la misma evaluación en dos pestañas o dispositivos a la vez**: se
   considera un único intento activo por evaluación — la segunda pestaña debe advertir que
   ya hay un intento en curso y ofrecer continuar ese mismo (no crear uno duplicado que
   compita por guardar respuestas).
6. **Doble clic accidental en "Enviar"**: el botón se deshabilita apenas se presiona una vez,
   para que un niño que hace doble clic por costumbre no genere un envío duplicado ni un
   error.
7. **El alumno está leyendo una guía (no una evaluación) y se interrumpe** (se corta la
   conexión, cierra sin querer): no hay pérdida de datos que importe — la guía es contenido
   de solo lectura, simplemente vuelve a abrir la asignatura y sigue leyendo donde quiera;
   no es un caso crítico como sí lo es una evaluación con nota.
8. **La sesión de login expira mientras el alumno está en medio de un examen largo (90
   min)**: la sesión de una evaluación en curso debe sobrevivir más tiempo que una sesión de
   navegación normal, o renovarse en silencio (refresh automático de token) — nunca debe
   expulsar a un alumno de un examen a medio rendir por expiración de sesión.

## Principio general para el desarrollo

Estos casos no son una lista para "revisar después" — deben construirse junto con el motor
de evaluación desde el principio (Paso 5-8 del plan de desarrollo), porque agregarlos
después sobre una base que no los contempló es mucho más caro que diseñarlos desde el
inicio. El servicio de estado del motor de evaluación (`EvaluacionStateService`, ver el plan
de desarrollo) es el lugar natural donde vive toda esta lógica de guardado/recuperación.
