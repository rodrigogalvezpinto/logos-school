# Lo que necesito de ti — Logos School

Este documento reúne lo que no puedo hacer solo: crear cuentas, entregar claves, pagar y tomar
algunas decisiones de negocio. Todo lo demás avanza de forma autónoma, según la cola de
`docs/auditorias/COLA-TRABAJO-AUTONOMO.md`.

**Cómo entregarme una clave:** nunca la pegues en el chat. Escríbela en `backend/.env`, que no
se sube al repositorio, o en el panel del servicio (Render o Cloudflare) cuando lleguemos al
despliegue. Avísame solo con «ya está la clave X en el .env».

Los precios son aproximados, con fecha 2026-11. Verifícalos al crear cada cuenta.

## 1. Cuentas para publicar la app (todas con plan gratuito para partir)

| # | Servicio | Para qué | Costo al partir | Qué tienes que hacer | Dónde se configura |
|---|---|---|---|---|---|
| 1 | **Neon** (neon.tech) | Base de datos PostgreSQL, con una base para Desarrollo y otra para Producción | Gratis | Crear el proyecto `logos-school` y 2 *branches*: `desarrollo` y `produccion`. Me entregas las 2 cadenas de conexión | `DATABASE_URL` en el `.env` de cada ambiente |
| 2 | **Render** (render.com) | Servidor del backend (FastAPI) | Gratis; el plan gratuito «duerme» tras 15 min sin uso. Unos USD 7 al mes para que no duerma | Crear la cuenta y conectarla con GitHub (repositorio `Logos`) | Variables de entorno en el panel de Render |
| 3 | **Cloudflare Pages** | Frontend (Angular) | Gratis | Crear la cuenta y conectarla con GitHub | Panel de Cloudflare |
| 4 | **Cloudflare R2** | Guardar los audios de lectura en voz alta (≈57 MB hoy y más con otros cursos) | Gratis hasta 10 GB | Activar R2 en la misma cuenta y crear el *bucket* `logos-audio` | Lo dejo preparado; ver la tarea 12 de la cola |
| 5 | **Dominio** (por ejemplo, `logosschool.cl` en NIC Chile) | Dirección web propia | Unos $10.000 CLP al año | Elegir el nombre y comprarlo. Hoy el código usa `api.logos.cl` como ejemplo | DNS en Cloudflare |
| 6 | **Resend** (resend.com) | Correos: bienvenida, recuperar contraseña, avisos al apoderado | Gratis hasta 3.000 correos al mes | Crear una cuenta nueva para este proyecto y verificar el dominio | `RESEND_API_KEY` y `RESEND_REMITENTE` |
| 7 | **Google Cloud** (OAuth) | Botón «Entrar con Google» | Gratis | Crear el proyecto, configurar la pantalla de consentimiento y crear un *Client ID* web con el dominio | `GOOGLE_CLIENT_ID` (backend) y `googleClientId` (`environment.prod.ts`) |
| 8 | **Cloudflare Turnstile** | Anti-bots en el registro (reemplazo gratuito de reCAPTCHA) | Gratis | Crear un *site key* para el dominio | Pendiente de integrar: lo preparo cuando exista el dominio |
| 9 | **Sentry** (sentry.io) | Aviso de errores en producción | Gratis (plan Developer) | Crear 2 proyectos: `logos-backend` (Python) y `logos-frontend` (Angular). Me entregas los 2 DSN | Pendiente de integrar (código detrás de variable; si está vacía, no se activa) |
| 10 | **UptimeRobot** | Aviso si la app se cae | Gratis | Crear un monitor HTTP del backend cuando esté publicado | Solo en su panel |

## 2. Cobro de planes (pasarela de pago)

Hay que decidir el proveedor. Mi recomendación para partir es **Flow** (flow.cl): acepta Webpay,
tarjetas y transferencias, se activa sin contrato con Transbank y cobra solo una comisión por
venta (alrededor de 3 % + IVA). La alternativa es **Mercado Pago**, con condiciones parecidas.
**Webpay Plus directo** con Transbank tiene una comisión más baja, pero exige más trámites.

Lo que necesito de ti:
1. Elegir el proveedor (Flow, Mercado Pago o Webpay).
2. Crear la cuenta de empresa. Requiere el RUT de la empresa y una cuenta bancaria.
3. Entregarme las claves de **integración (sandbox)** en el `.env`.

Mientras tanto construyo el adaptador en la rama `feature/pasarela-pago`, con un modo de
prueba que no cobra nada.

## 3. Profesor con inteligencia artificial (opcional)

Es un tutor que explica y da pistas, nunca la respuesta directa, con salvaguardas para menores.
Lo construyo en la rama `feature/profesor-ia`, desactivado mientras no haya clave.

- **Costo:** se paga por uso. Con un modelo económico y límites por alumno, se puede mantener
  en unos pocos dólares al mes por cada cien alumnos activos. Te mostraré la estimación real
  antes de activarlo.
- **Lo que necesito:** una cuenta en console.anthropic.com, una clave API con un límite de gasto
  mensual configurado y tu decisión de si va incluido en los planes o solo en el plan Full.

## 4. Decisiones de negocio y legales

1. **Revisión legal** de los términos de uso y de la política de privacidad. El público son
   menores de edad y en Chile rigen la Ley 19.628 y la nueva ley de datos personales (21.719).
   Recomiendo una revisión por un abogado antes de lanzar.
2. **Precios finales** de los planes. Hoy están en el panel de administrador, con tope de
   $19.990 al mes, como dice `planificacion/09-modelo-de-negocio.md`.
3. **Segunda validación del contenido.** Hice una revisión ítem por ítem de los 12 cursos, pero
   un segundo par de ojos (idealmente un profesor) da más garantía. Basta con una muestra por
   curso.
4. **Nombre de dominio** (punto 1.5).

## 5. Ramas para revisar cuando vuelvas

Las funcionalidades nuevas quedan en ramas aparte, sin mezclar con `main`, para que las revises:

| Rama | Contenido | Estado |
|---|---|---|
| `feature/juegos-practica` | Juegos de práctica con el banco de preguntas | Por construir (tarea 13) |
| `feature/profesor-ia` | Tutor con IA, desactivado sin clave | Por construir (tarea 14) |
| `feature/pasarela-pago` | Adaptador de pagos con modo de prueba | Por construir (tarea 15) |

Este documento se actualiza a medida que avanza la cola.
