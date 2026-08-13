---
título: Análisis de brechas — qué falta para que esto sea un producto real
estado: auditoría (2026-08-12), verificado contra el código y la base de datos reales
última actualización: 2026-08-12 (segunda pasada — Fase 1.1 + refactor hexagonal completos)
---

Este documento se generó revisando el estado real del repositorio y de la base de datos
(no de memoria) — cada punto está verificado con un comando concreto, no es una lista
genérica.

## ✅ Resuelto en esta sesión (ya no son brechas)

1. ~~El Front no está conectado al backend~~ — conectado con `HttpClient` real, JWT,
   `SesionService` persistido en `localStorage`, guards de ruta.
2. ~~Pruebas de unidad y Exámenes simulacro no importados~~ — parser nuevo
   (`scripts/parser_prueba_examen.py`) + importados: 4° básico 12 pruebas/108 preguntas +
   2 exámenes/56 preguntas, 6° básico 14 pruebas/170 preguntas + 5 exámenes/150 preguntas.
3. ~~Nada persiste un intento de evaluación~~ — ciclo completo iniciar/responder/entregar,
   idempotente, con cálculo de nota real server-side.
4. ~~Los Planes no calzan con lo decidido~~ — sembrados los 3 planes reales de
   `09-modelo-de-negocio.md` (mensual $19.990 / por periodo $89.900 / anual $159.900).
5. ~~Validación de RUT chileno~~ — módulo 11, en frontend y backend.
6. ~~Página de Privacidad y Términos~~ — existen y están enlazadas desde el registro.
7. ~~Arquitectura del backend~~ — refactor completo a hexagonal (dominio/aplicación/
   infraestructura), SOLID, patrones nombrados (Repository, Strategy, DI, Factory methods,
   Value Objects). Ver el commit "Refactor backend a arquitectura hexagonal".

Verificación end-to-end vigente: **51/51 tests de backend, 18/18 E2E de Playwright**.

## 🟠 Necesario antes de mostrarle esto a una familia real (no solo a ti)

1. **Pasarela de pago real.** Sigue mockeada (activación manual sin cobrar) — hay que
   elegir proveedor (Webpay/Transbank es el estándar en Chile) e integrarlo.
2. **Login con Google no tiene credenciales reales.** El código está listo y ahora detrás
   de un puerto (`VerificadorTokenGoogleAdapter`), pero `GOOGLE_CLIENT_ID` no existe — no
   hay `.env` real todavía, solo `.env.example`.
3. **Correo (Resend) sin API key real.** El adaptador existe (`infrastructure/
   notificaciones/`, pendiente de mover — ver Paso 5 diferido del refactor) pero no está
   cableado a ningún caso de uso ni tiene API key real.
4. **Nada está desplegado.** Todo corre en tu Mac (Postgres local, `uvicorn`, `ng serve`).
   Faltan las cuentas reales de Neon, Render y Cloudflare Pages
   (`planificacion/17-infraestructura-y-entornos.md`) — requieren tu información de
   contacto/pago, no las puedo crear yo.
5. **Cloudflare Turnstile (anti-bots)** no está implementado en registro/login, aunque ya
   está decidido en `planificacion/20-seguridad-y-casos-borde.md`.

## 🟡 Ya planificado, simplemente no construido todavía (no es una sorpresa)

6. ~~Fase 1.2 (historial y notas por materia)~~ — **completa (2026-08-12)**: nuevo bounded
   context `progreso`, endpoints `GET/POST /progreso/{perfil_alumno_id}`, páginas
   `/alumno/notas` y `/apoderado/progreso/:id`. 56/56 tests backend, 21/21 E2E.
7. ~~Fase 1.3 (plan de estudio con horario)~~ — **completa (2026-08-13)**: nuevo bounded
   context `plan_estudio` (cronograma round-robin puro y testeable, orientado a la fecha
   del examen o +8 semanas por defecto), simulacro parcial generado on-demand
   (`ConjuntoEvaluacion` dinámico acotado a las OA ya cubiertas, reutiliza el ciclo
   IniciarIntento/EntregarIntento sin cambios), habilitación progresiva de pruebas/exámenes
   y lista de "faltantes" en `/alumno/notas`, onboarding con selección de días y fecha
   objetivo. Páginas `/alumno/plan-estudio` y sección de faltantes en `/alumno/notas`.
   102/102 tests backend, 32/32 E2E.
8. ~~Panel de Administrador~~ — **completo (2026-08-13)**: nuevos bounded contexts `admin`
   (login separado del Apoderado, JWT con claim `tipo` propio para que un token nunca sirva
   de credencial del otro) y `comercial` (Planes, Códigos de descuento, cortesías,
   métricas). Páginas `/admin/login`, `/admin/dashboard`, `/admin/planes`,
   `/admin/descuentos`, `/admin/cortesias`. 76/76 tests backend, 29/29 E2E.
9. ~~Rol Profesor / Curso-Sección~~ — **completo (2026-08-13)**: nuevos bounded contexts
   `profesor` (auto-registro, `estado="pendiente"` hasta aprobación, JWT propio con claim
   `tipo="profesor"`) y `curso_seccion` (crear curso, agregar/quitar alumno, comunicados,
   progreso agregado del curso reutilizando `ObtenerHistorialYNotas` de Fase 1.2). Aprobación
   de cuentas reutiliza el panel Admin ya existente (`/admin/profesores`, protegido por
   `get_cuenta_admin_actual`), sin construir un cuarto sistema de auth. Páginas
   `/profesor/login`, `/profesor/dashboard`, `/profesor/cursos/:id`, `/admin/profesores`, y
   sección "Mi Curso" en `/alumno/inicio`. 122/122 tests backend, 35/35 E2E.

**Orden acordado con el usuario (2026-08-12): Fase 1.2 (✅) → Panel de Administrador (✅) →
Fase 1.3 (✅) → Rol Profesor (✅). Etapa 1 (MVP) + Etapa 2 completas.**

## 🟢 Calidad / pulido — no bloquea lanzar, pero se nota

10. ~~Lectura en voz alta~~ — **implementada (2026-08-13)**: `LectorVozService` +
    `BotonEscuchar`, conectado en guía de estudio y en cada pregunta (autoevaluación, prueba,
    examen). Ver `21-accesibilidad-lectura-y-contenido-visual.md`. **Componentes visuales de
    Matemática** (recta numérica, modelo de fracciones) siguen decididos, no implementados.
11. **Logo**: sigue siendo el concepto SVG simple, no una versión pulida final.
12. **CI/CD**: no hay ningún pipeline (GitHub Actions u otro) que corra los tests
    automáticamente en cada cambio — hoy dependen de correrlos a mano.
13. **Responsive/móvil**: no se ha probado explícitamente en pantallas chicas (la mayoría
    de apoderados van a entrar desde el celular).
14. **Auditoría de accesibilidad** (lectores de pantalla, contraste WCAG real medido) — no
    se ha hecho formalmente.

## Recomendación de orden

Con la Fase 1.1 funcionando de verdad end-to-end y el backend ya en arquitectura hexagonal,
el camino más corto a "esto ya sirve para una familia real" es: **(1) desplegar a
Neon+Render+Cloudflare Pages → (2) credenciales reales de Google/Resend → (3) pasarela de
pago → (4) Turnstile.** Con esos 4 pasos la app deja de vivir solo en tu Mac. El resto
(Fase 1.2/1.3, Admin panel, pulido visual) se puede ir sumando con la app ya en producción.
