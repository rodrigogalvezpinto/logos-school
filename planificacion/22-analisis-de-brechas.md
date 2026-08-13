---
título: Análisis de brechas — qué falta para que esto sea un producto real
estado: auditoría (2026-08-12), verificado contra el código y la base de datos reales
última actualización: 2026-08-12
---

Este documento se generó revisando el estado real del repositorio y de la base de datos
(no de memoria) — cada punto está verificado con un comando concreto, no es una lista
genérica.

## 🔴 Bloqueante — sin esto, el MVP (Fase 1.1) no es usable de verdad

1. **El Front no está conectado al backend.** Verificado: cero archivos en
   `frontend/src/app/` usan `HttpClient` o llaman a `localhost:8000`. Todo lo que ves hoy
   (asignaturas, preguntas, notas) es data de ejemplo hardcodeada
   (`core/mock-data/mock-data.ts`). Es el paso más grande pendiente — sin esto, nada de lo
   demás importa.
2. **Las Pruebas de unidad y Exámenes simulacro no están importados a la base.**
   Verificado: `SELECT count(*) FROM conjunto_evaluacion` → **0 filas**. Solo se importó la
   autoevaluación por OA (`Pregunta` sí tiene datos). El contenido real existe en
   `contenido/{curso}/pruebas/` y `/examenes/` pero el parser todavía no lo procesa — hay
   que extenderlo (mismo patrón de trabajo que ya se hizo para las guías, con sus propias
   variantes de formato a descubrir).
3. **Nada persiste un intento de evaluación.** Verificado: `SELECT count(*) FROM
   intento_evaluacion` → **0 filas**. El servicio de cálculo de nota existe y tiene tests,
   pero ningún endpoint lo usa todavía — faltan: `POST /evaluaciones/intentos` (iniciar),
   `POST .../responder` (autosave por pregunta), `POST .../entregar` (corrige y calcula
   nota). Esto es lo que le da sentido real al motor de evaluación.
4. **Los Planes en la base no calzan con lo que se decidió.** Verificado: solo existe 1
   plan ("Completo", $19.990) creado por el script de prueba. Falta cargar la estructura
   real de 3 planes de `planificacion/09-modelo-de-negocio.md` (mensual / por periodo de
   examinación / anual) como datos semilla reales, no solo para la cuenta de prueba.

## 🟠 Necesario antes de mostrarle esto a una familia real (no solo a ti)

5. **Pasarela de pago real.** Sigue mockeada (activación manual sin cobrar) — decisión ya
   tomada de dejarlo para después, pero en algún momento hay que elegir proveedor
   (Webpay/Transbank es el estándar en Chile) e integrarlo.
6. **Login con Google no tiene credenciales reales.** El código está listo
   (`app/routers/auth.py`), pero `GOOGLE_CLIENT_ID` no existe — no hay archivo `.env` real
   todavía (verificado, solo existe `.env.example`). Sin esto, el botón "Continuar con
   Google" del Front fallaría en producción.
7. **Correo (Resend) sin API key real** — mismo caso: el servicio está escrito y probado en
   modo "registra en log pero no envía", pero nadie recibe un correo de bienvenida de
   verdad todavía.
8. **Nada está desplegado.** Todo corre en tu Mac (Postgres local, `uvicorn`, `ng serve`).
   Faltan las cuentas reales de Neon, Render y Cloudflare Pages que ya elegimos en
   `planificacion/17-infraestructura-y-entornos.md` — hay que crearlas (2-3 acciones que
   requieren tu información de contacto/pago, no las puedo autoservicio).
9. **Validación de RUT chileno.** Verificado: el campo `rut` se guarda como texto libre, sin
   validar dígito verificador ni formato. Un apoderado podría escribir cualquier cosa.
10. **Página de Política de Privacidad y Términos y Condiciones.** Están descritos en
    `planificacion/10-privacidad-y-datos-de-menores.md` pero no existen como páginas reales
    en el Front — y son legalmente necesarias antes de recolectar datos de menores en serio.
11. **Cloudflare Turnstile (anti-bots) no está implementado** en el registro/login, aunque
    ya está decidido en `planificacion/20-seguridad-y-casos-borde.md`.

## 🟡 Ya planificado, simplemente no construido todavía (no es una sorpresa)

12. **Fase 1.2 (historial y notas por materia)** — pantallas y endpoints no existen aún,
    según lo previsto en `03-roadmap-etapas.md`.
13. **Fase 1.3 (plan de estudio con horario)** — mismo caso, ya diseñado en
    `13-plan-de-estudio.md`, no construido.
14. **Panel de Administrador** (`planificacion/18-panel-administrador.md`) — cero código,
    ni frontend ni backend. Lo vas a necesitar pronto para gestionar precios/cortesías.
15. **Rol Profesor / Curso-Sección** — Etapa 2 del roadmap, correctamente fuera de alcance
    todavía.

## 🟢 Calidad / pulido — no bloquea lanzar, pero se nota

16. **Componentes visuales de Matemática** (recta numérica, modelo de fracciones) y
    **lectura en voz alta** (Web Speech API) de `planificacion/21-...md` — decididos, no
    implementados.
17. **Logo**: sigue siendo el concepto SVG simple que armé, no una versión pulida final.
18. **CI/CD**: no hay ningún pipeline (GitHub Actions u otro) que corra los 44 tests
    automáticamente en cada cambio — hoy dependen de que yo los corra a mano.
19. **Responsive/móvil**: no se ha probado explícitamente en pantallas chicas (la mayoría de
    apoderados van a entrar desde el celular).
20. **Auditoría de accesibilidad** (lectores de pantalla, contraste WCAG real medido, no solo
    diseñado) — no se ha hecho formalmente.

## Recomendación de orden

Dado que ya tienes contenido, diseño y motor de evaluación sólidos, el camino más corto a
"esto ya sirve para una familia real" es, en este orden: **(1) conectar el Front al
backend real → (2) importar pruebas/exámenes → (3) endpoints de IntentoEvaluacion/nota real
→ (4) desplegar a Neon+Render+Cloudflare Pages.** Con esos 4 pasos, el resto de la lista
(pago real, Google, correo, admin panel) se puede ir sumando con la app ya funcionando de
verdad, en vez de todo en local.
