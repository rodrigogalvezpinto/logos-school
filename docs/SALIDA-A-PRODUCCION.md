# Primera salida a producción: estado y lista de verificación

> Actualizado el 2026-11-21. Pasos de despliegue: `docs/DESPLIEGUE.md`. Este documento dice **qué está listo,
> qué falta y quién lo hace**.

## 1. Veredicto

**Técnicamente lista para la primera salida.** Falta crear las cuentas y cargar las variables de entorno
(sección 3), y una decisión de negocio sobre el cobro (sección 4).

Ensayo general del 2026-11-21, hecho en este Mac:

- Base **nueva y vacía**, cargada solo con los pasos de `DESPLIEGUE.md` (sin `datos_de_prueba.py` ni cuenta demo).
- API con `ENTORNO=produccion` y `JWT_SECRET` aleatorio.
- Compilación de producción del frontend, servida **con el mismo CSP de `_headers`** que aplicará Cloudflare.

Resultados del ensayo:

- `/salud` respondió `{"estado":"ok"}`; `/docs` y `/openapi.json`, 404.
- Recorridos completos (registro → alumno → prueba gratis → apoderado → guías → autoevaluación → prueba de unidad
  → simulacro → plan de estudio → notas) en 1.° básico, 4.° básico, 8.° básico, 3.° medio y 4.° medio: **35/35**.
- `e2e/ensayo-produccion.spec.ts` y `e2e/recuperar-password.spec.ts`: **10/10**. Cubren:
  - sin botón demo y sin botón de Google cuando no hay Client ID;
  - guía con imágenes y fuentes propias;
  - PDF de la guía, juegos, certificado PDF;
  - «¿Olvidaste tu contraseña?».
- Backend 759 pruebas + 6 de recuperación de contraseña; frontend 151 unitarias.

Lo que el ensayo encontró y quedó corregido:

| Problema | Efecto en producción | Corrección |
|---|---|---|
| Angular cargaba el CSS con un `onload` inline | El CSP lo bloqueaba: CSS con media=print | `inlineCritical: false` en `angular.json` |
| Fuentes Poppins/Inter desde Google Fonts | El CSP las bloqueaba (letra del sistema) y cada visita avisaba a Google | Fuentes alojadas en el sitio (`@fontsource`, OFL) |
| No existía «¿Olvidaste tu contraseña?» | Un apoderado que olvida la clave pierde el acceso | Enlace por correo, 1 hora, un solo uso, cierra las sesiones |
| Login con Google y CSP | Si se configura Google, su script quedaría bloqueado | `frontend.sh` agrega `accounts.google.com/gsi` solo si hay Client ID |
| Health check en `/docs` | `/docs` está apagado en producción | `GET /salud` (consulta la base) |

## 2. Repetir el ensayo

```bash
# API en modo producción contra una base local nueva (ver la lista de comandos en DESPLIEGUE.md, paso 2)
ENTORNO=produccion JWT_SECRET=$(openssl rand -hex 32) CORS_ORIGENES=http://localhost:4410 \
  DATABASE_URL=<base nueva> .venv/bin/uvicorn app.main:app --port 8002
# Compilación de producción servida con el CSP de _headers (connect-src → http://localhost:8002), puerto 4410
LOGOS_E2E_WEB_URL=http://localhost:4410 npx playwright test -c playwright.ensayo-prod.config.ts \
  e2e/ensayo-produccion.spec.ts e2e/recuperar-password.spec.ts e2e/flujo-completo-4-basico.spec.ts
```

## 3. Cuentas y variables (las crea el dueño; nada de esto va al repositorio)

| Dónde | Variable | Obligatoria | Nota |
|---|---|---|---|
| Neon | — | Sí | Proyecto con branches `desarrollo` y `produccion` (plan gratis) |
| Render (prod) | `DATABASE_URL` | Sí | Cadena de Neon, branch `produccion` |
| Render | `JWT_SECRET` | Sí | Render lo genera solo (`generateValue`) |
| Render | `CORS_ORIGENES` | Sí | Dominio del sitio, p. ej. `https://logosschool.cl,https://www.logosschool.cl` |
| Render | `URL_FRONTEND` | Recomendada | Para los enlaces de los correos; sin ella se usa el primer origen de CORS |
| Render | `RESEND_API_KEY` | Sí, para recuperar contraseña | Cuenta Resend propia del proyecto |
| Render | `RESEND_REMITENTE` | Sí, con Resend | Con un dominio **verificado** en Resend; sin dominio verificado, Resend solo entrega al correo del dueño |
| Render | `GOOGLE_CLIENT_ID` | No | Sin ella, el botón de Google no aparece |
| Render | `LOGOS_IA_HABILITADA` + `ANTHROPIC_API_KEY` | No | Profesor IA; apagado por defecto |
| Render | `SENTRY_DSN` | Recomendada | Aviso de errores del backend (sentry.io, plan gratis); vacío = apagado |
| Mac (al compilar) | `LOGOS_API_URL` | Sí | URL pública del backend; `frontend.sh` también ajusta el CSP |
| Mac (al compilar) | `LOGOS_GOOGLE_CLIENT_ID` | No | Mismo Client ID que en Render |
| Mac (al compilar) | `LOGOS_SENTRY_DSN` | Recomendada | DSN del proyecto Sentry del frontend; `frontend.sh` agrega su origen al CSP |
| Cloudflare | — | Sí | Pages (`npx wrangler login`) y DNS del dominio |
| Dominio | — | Sí | `.cl` en NIC Chile u otro; `api.<dominio>` → Render |
| UptimeRobot | — | Recomendada | Monitor sobre `https://api.<dominio>/salud` |

Después del despliegue: crear el administrador con `scripts/crear_admin.py` (paso 2 de `DESPLIEGUE.md`).

Plan gratis de Render: el servicio «duerme» tras 15 minutos sin uso y la primera visita tarda unos 50 segundos.
Para alumnos reales conviene el plan Starter.

## 4. Decisión de negocio pendiente: el cobro

Hoy **no hay pasarela de pago y el acceso al contenido no depende del plan**. La «prueba gratis de 5 días» se
registra, pero al vencer el alumno sigue estudiando y nadie le cobra. Opciones para la primera salida:

| Opción | Qué implica | Trabajo |
|---|---|---|
| **A. Beta gratuita** (recomendada para salir ya) | Se anuncia como beta abierta; se ajusta el texto de planes y de la prueba gratis | Poco: solo textos |
| B. Prueba gratis + pago manual | Al vencer la prueba se bloquea el contenido; el dueño cobra por transferencia y activa el plan desde Admin → Cortesías | Medio: bloqueo por plan + aviso al apoderado |
| C. Esperar la pasarela | Flow (recomendada en Chile), Mercado Pago o Webpay; requiere cuenta comercial del dueño | Mayor: tarea 15 |

## 4b. Hecho después del primer ensayo (rama `desarrollo/post-lanzamiento`, 2026-11-22)

- Cambiar contraseña y **eliminar la cuenta** del apoderado (con todos sus alumnos) en Configuración.
  Reemplazan dos botones que no hacían nada.
- Sentry en backend y frontend, sin datos personales: sin cuerpos, parámetros de URL, usuario ni migas.
  El SDK del navegador solo se descarga si hay DSN.
- Menú del alumno sin marcadores «pronto»; textos de prueba gratis y pagos sin promesas que la app no cumple.
- Plan Lector (48 libros) y Útiles Escolares (132 ítems) para los 12 cursos; antes solo había para 4.° básico.
  Se cargan con los mismos `seed_plan_lector.py` y `seed_utiles_escolares.py` del paso 2 de `DESPLIEGUE.md`.
- **Cobro:** se trabaja con la opción A (beta gratuita), la recomendada (2026-11-22). Asumida, no confirmada
  expresamente por el dueño: si elige B o C, lo siguiente es el bloqueo por plan.
- **Vacío conocido para el bloqueo por plan:** hoy la prueba gratis se puede reactivar sin límite. No importa
  mientras nada se bloquee, pero hay que cerrarlo al construir el bloqueo.

## 5. Antes de abrir a familias reales (dueño)

- Revisión legal de `/terminos` y `/privacidad` (Ley 19.628 y Ley 21.719, datos de menores).
- Precios finales en Admin → Planes.
- Revisión del material por un profesor (pendiente desde la Fase 1).
