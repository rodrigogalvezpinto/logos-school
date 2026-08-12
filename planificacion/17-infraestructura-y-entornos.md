---
título: Infraestructura, entornos (desarrollo/producción) y monitoreo
estado: decisión tomada (2026-08-12), regla no negociable de ambientes separados
última actualización: 2026-08-12
---

## Regla no negociable: SIEMPRE dos ambientes separados, desde el primer día

El usuario fue explícito: **debe existir un ambiente de Desarrollo y un ambiente de
Producción desde el inicio**, cada uno con su propia base de datos, y esto no se debe
olvidar ni mezclar nunca a medida que el proyecto avanza. Se registra aquí como regla dura
para que ningún documento futuro ni ningún agente de programación lo pierda de vista.

**Se trabaja siempre primero en Desarrollo.** Producción solo recibe cambios ya probados en
Desarrollo — nunca se programa o se prueba directo contra producción.

## Elección de infraestructura: gratis para empezar, con camino claro para escalar/pagar

Criterio del usuario: tecnología gratuita en esta etapa inicial, de calidad, que permita
migrar a un plan pagado más adelante sin tener que cambiar de proveedor ni rehacer nada.

| Pieza | Proveedor elegido | Por qué | Plan gratuito | Camino de escalamiento |
|---|---|---|---|---|
| **Base de datos (PostgreSQL)** | **Neon** (neon.tech) | Postgres "serverless" con **branches** — literalmente la función pensada para tener un ambiente Desarrollo y uno Producción con un clic, sin pagar por dos servidores separados. | Sí, sin tarjeta de crédito para empezar | Neon tiene planes pagados que solo escalan cómputo/almacenamiento, mismo proveedor, sin migración |
| **Backend (API FastAPI)** | **Render** (render.com) | Soporta Python nativo, despliegue directo desde GitHub, dos servicios separados (uno por ambiente) | Sí (con la limitación de que el servicio "duerme" tras inactividad — aceptable en desarrollo/etapa inicial) | Se sube a un plan pagado (sin cold start) cuando haya usuarios reales pagando, mismo proveedor |
| **Frontend (Angular)** | **Cloudflare Pages** | Gratis de forma indefinida para sitios estáticos (no es un trial), despliega automáticamente una URL de **preview por cada rama** que no sea `main` y la versión de producción en `main` — encaja perfecto con la separación Desarrollo/Producción. Ya existe experiencia con este proveedor en otros proyectos del usuario. | Sí, ilimitado en la práctica para este tamaño de proyecto | No suele hacer falta escalar a pago para solo frontend |
| **Correo transaccional** (confirmación de registro, recuperar contraseña) | **Resend** | Ya usado en otros proyectos del usuario, plan gratuito para volumen bajo | Sí | Plan pagado por volumen, mismo proveedor |
| **Monitoreo de errores** | **Sentry** | Plan gratuito capta errores de backend (FastAPI) y frontend (Angular) en un solo lugar, alertas automáticas | Sí (con límite mensual de eventos, suficiente en etapa inicial) | Plan pagado por volumen de eventos |
| **Monitoreo de disponibilidad** ("¿está caída la página?") | **UptimeRobot** | Chequeo automático cada cierto tiempo, avisa por correo si la app deja de responder | Sí | Plan pagado con chequeos más frecuentes |

**Nota de vigencia:** los planes gratuitos de estos proveedores cambian con el tiempo —
antes de implementar, confirmar en el sitio de cada proveedor que las condiciones descritas
siguen vigentes. La elección del proveedor no cambia aunque cambien los límites exactos del
plan gratuito.

## Cómo se ven los dos ambientes en la práctica

```
Rama de código "develop"  ──▶  Cloudflare Pages (preview)  ──▶  llama a
                                                                  Render "logos-api-dev"
                                                                  ──▶ Neon branch "dev"

Rama de código "main"     ──▶  Cloudflare Pages (producción) ──▶ llama a
                                                                  Render "logos-api-prod"
                                                                  ──▶ Neon branch "main" (producción)
```

- Se trabaja y se prueba todo en la rama `develop` (ambiente Desarrollo) primero.
- Cuando algo está probado y listo, se integra a `main` (ambiente Producción).
- Cada ambiente tiene sus propias variables de entorno (`.env.development` /
  `.env.production`, nunca subidas al repositorio) con la conexión a su propia base de
  datos — nunca comparten datos entre sí.

## Registro con Google (login social)

El usuario pidió que los Apoderados puedan **registrarse/iniciar sesión con su cuenta de
Google**, además del registro simple con email y contraseña ya definido en
`10-privacidad-y-datos-de-menores.md`. Es gratuito de implementar (Google no cobra por usar
"Iniciar sesión con Google"), y reduce fricción de registro — coherente con el criterio de
"lo más simple posible" ya establecido para el registro.

**Cómo se integra sin romper el modelo de datos ya definido** (actualiza la entidad
`Cuenta` de `11-especificacion-mvp-para-desarrollo.md`):

```
Cuenta (Apoderado)
  id
  email                 (único)
  password_hash          (nullable — vacío si se registró solo con Google)
  google_id              (nullable — presente si se registró/vinculó con Google)
  nombre
  comuna_o_region        (opcional)
  pais                   (opcional)
  fecha_creacion
```

El Apoderado puede registrarse con email+contraseña, con Google, o vincular ambos métodos a
la misma cuenta más adelante. La verificación del token de Google la hace el backend
(FastAPI) contra los servidores de Google — no hay costo ni requiere que la app misma
guarde contraseñas si el usuario entra solo por Google.

## Versiones concretas del stack

Para evitar problemas de compatibilidad entre herramientas más adelante, se fijan versiones
estables al momento de iniciar el desarrollo (a confirmar la última versión estable
disponible en cada sitio oficial en el momento exacto de instalar, ya que esto avanza con
el tiempo — la regla es siempre "última versión estable", no una versión específica que
pueda quedar obsoleta antes de lanzar):

- **Python**: última versión estable 3.12.x o 3.13.x (evitar la versión más nueva recién
  salida sin soporte completo de librerías todavía).
- **FastAPI**: última versión estable publicada en PyPI al momento de iniciar.
- **PostgreSQL**: la versión que Neon tenga como default estable (Neon la gestiona,
  usualmente la más reciente con soporte largo).
- **Angular**: última versión LTS (soporte a largo plazo) estable publicada en angular.dev
  al momento de iniciar — no una versión release candidate.
- **Node.js**: la versión LTS activa recomendada por Angular para esa versión específica
  (Angular publica esta compatibilidad en su documentación).

Se confirma la versión exacta de cada una recién al momento de ejecutar el Paso 1 del plan
de desarrollo (creación del repositorio), no antes, para no fijar un número que quede
desactualizado mientras el proyecto sigue en planificación.

## Continuidad entre conversaciones (para que nada se pierda si se abre un chat nuevo)

Todo lo decidido en `planificacion/` + `CLAUDE.md` persiste como archivos reales en el
proyecto — cualquier conversación nueva de Claude Code en esta carpeta lee `CLAUDE.md`
automáticamente al iniciar, y ese archivo indexa todos los documentos de `planificacion/`.
No hace falta repetir contexto: un chat nuevo puede leer `CLAUDE.md` → seguir sus
referencias → tener el 100% de lo avanzado (contenido, roles, modelo de negocio, modelo de
datos, motor de evaluación, plan de estudio, diseño visual, navegación, y esta
infraestructura) sin rehacer ninguna decisión ya tomada.
