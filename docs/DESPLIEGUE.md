# Despliegue de Logos School: paso a paso

**Estado:** preparado, sin desplegar. Esta guía se sigue cuando existan las cuentas de
`docs/PENDIENTES-USUARIO.md`. Respeta la regla de `planificacion/17-infraestructura-y-entornos.md`:
**Desarrollo y Producción separados**, cada uno con su propia base de datos.

## Piezas ya preparadas en el repositorio

| Pieza | Archivo | Qué hace |
|---|---|---|
| Backend en Render | `render.yaml` | Define 2 servicios: `logos-api-dev`, que se publica automáticamente con cada cambio en `main`, y `logos-api-prod`, que se publica a mano. Instala las versiones exactas de `uv.lock` y aplica las migraciones al arrancar |
| CORS por ambiente | `CORS_ORIGENES` (`backend/app/core/config.py`) | En Producción la API acepta **solo** el dominio real. Antes estaba fija en `localhost` y la app publicada no habría podido llamar a la API |
| Seguridad del backend | `JWT_SECRET` | Render lo genera solo. La API no arranca en Producción con el valor de ejemplo |
| Frontend | `scripts/desplegar/frontend.sh` | Compila con la URL real de la API, ajusta el CSP de `_headers` a ese dominio y publica en Cloudflare Pages, con los audios incluidos |
| Audios de lectura | `scripts/voz/generar_audios.sh` | Genera los `.m4a` en este Mac (Kokoro «alex»). Cloudflare Pages admite archivos de hasta 25 MB y 20.000 archivos: caben sin necesidad de R2 |

## Orden de despliegue

1. **Base de datos (Neon).** Crear el proyecto con las branches `desarrollo` y `produccion`.
   Copiar las dos cadenas de conexión: van a Render, nunca al repositorio.
2. **Cargar el contenido**, una vez por base, desde este Mac:
   ```bash
   cd backend
   export DATABASE_URL='<cadena de Neon de la branch correspondiente>'
   .venv/bin/alembic upgrade head
   .venv/bin/python scripts/importar_contenido.py
   .venv/bin/python scripts/sembrar_planes.py
   .venv/bin/python scripts/seed_plan_lector.py
   .venv/bin/python scripts/seed_utiles_escolares.py
   .venv/bin/python scripts/crear_admin.py   # crea la cuenta de administrador (pide los datos)
   ```
   No ejecutar `datos_de_prueba.py` en Producción: crea cuentas ficticias.
3. **Backend (Render).**
   1. Entrar a New → Blueprint, elegir el repositorio y aceptar `render.yaml`.
   2. Completar en cada servicio `DATABASE_URL`, `CORS_ORIGENES` (por ejemplo,
      `https://logosschool.cl,https://www.logosschool.cl`), `GOOGLE_CLIENT_ID` y `RESEND_API_KEY`.
   3. Probar que `https://<servicio>.onrender.com/docs` responda.
4. **Frontend (Cloudflare Pages)**, desde este Mac:
   ```bash
   npx wrangler login                       # una sola vez
   DATABASE_URL='<Neon prod>' scripts/voz/generar_audios.sh   # audios con los textos de esa base
   LOGOS_API_URL=https://<api> scripts/desplegar/frontend.sh logos-school
   ```
5. **Dominio.** En Cloudflare, asociar el dominio al proyecto de Pages, y `api.<dominio>` al
   servicio de Render (con un CNAME). Después, actualizar `CORS_ORIGENES` y volver a ejecutar el
   paso 4 con `LOGOS_API_URL=https://api.<dominio>`.
6. **Correo y Google.** Verificar el dominio en Resend y agregar el dominio a los orígenes
   autorizados del *Client ID* de Google.
7. **Monitoreo.** Crear un monitor en UptimeRobot sobre `https://api.<dominio>/docs`. Sentry y
   Turnstile se integran cuando existan sus claves; ver `docs/PENDIENTES-USUARIO.md`.

## Verificación después de publicar

- Ejecutar la suite E2E contra el ambiente publicado:
  `LOGOS_E2E_WEB_URL=https://<dominio> LOGOS_E2E_API_URL=https://api.<dominio> npx playwright test`.
  Hacerlo solo en **Desarrollo**: la suite crea cuentas de prueba.
- Abrir la consola del navegador en el sitio publicado y confirmar que no haya bloqueos de CSP.
- En 1.° básico, comprobar que «Escuchar» reproduzca el audio pregrabado.
