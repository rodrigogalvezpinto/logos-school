---
título: Reforzamiento pagado con profesores (investigación y planificación — sin construir)
estado: investigación (2026-08-13) — decisión de negocio pendiente, no autorizado a construir todavía
última actualización: 2026-08-13
---

> El usuario pidió explícitamente: **"no lo implementemos de una, primero estudiémoslo,
> planifiquémoslo"**. Este documento es solo investigación + propuesta — no se toca código a
> partir de esto hasta que el usuario decida seguir.

## El disparador

El usuario vio [wited.com/cl/reforzamiento](https://www.wited.com/cl/reforzamiento/) y
preguntó si Logos podría ofrecer algo similar: profesores dando clases de reforzamiento
pagadas a través de la plataforma, y que esos profesores puedan "impartir sus servicios" por
medio de Logos.

## Qué hace Wited hoy (investigado 2026-08-13)

Combina profesor humano + plataforma digital + IA ("Max IA"). Modelo de **suscripción
mensual con paquetes de clases**, no marketplace visible de profesores:

| Plan | Precio/mes | Incluye |
|---|---|---|
| Pro 1+ | $19.900 | 1 clase + plataforma |
| Pro 4+ | $59.900 | 4 clases + plataforma (recomendado) |
| Pro 8+ | $105.900 | 8 clases + plataforma |

Puntos importantes para la comparación con Logos:
- **No expone perfiles de profesores** al público (sin foto, especialidad, calificación,
  precio individual visible) — el apoderado no "elige" profesor desde la web, Wited debe
  asignarlo internamente.
- **No publica nada sobre el lado del profesor**: cómo se registra, cómo le pagan, qué
  comisión se queda la plataforma. Probablemente porque Wited emplea/contrata directamente a
  sus profesores (relación laboral o de honorarios gestionada internamente), no un modelo
  abierto tipo "cualquier profesor se inscribe y publica sus horarios" (que sí es el patrón de
  otras plataformas como Superprof o Preply).

**Conclusión de la investigación**: lo que Wited muestra públicamente es la cara comercial de
un **servicio con profesores propios**, no necesariamente un marketplace abierto. Si Logos
quiere que "los profesores se agreguen para ofrecer sus servicios" (como preguntó el
usuario), eso es más parecido a Superprof/Preply que a lo que Wited expone — son dos modelos
de negocio distintos y vale la pena decidir cuál, no asumir que es el mismo por default.

## Por qué esto es más grande de lo que parece (Fase 0 — descubrimiento del problema)

Siguiendo la metodología acordada (`~/Documents/Rules IA/00-metodologia-creacion-proyectos-ia.md`),
antes de plantear cómo construirlo hay que responder qué problema resuelve y a quién,
porque **esto no es una funcionalidad más — es un cambio de modelo de negocio**:

- Logos hoy es una **plataforma de contenido de autoestudio** (el profesor de Etapa 2
  gestiona un Curso/Sección ya existente, sin pago involucrado, sin marketplace).
- Un "reforzamiento pagado" convierte a Logos en un **marketplace de dos lados** (oferta:
  profesores buscando alumnos; demanda: familias buscando ayuda) — con todo lo que eso
  implica: verificación de identidad mucho más seria (ahora hay dinero y un adulto en
  contacto 1-a-1 con un menor, no solo acceso a un roster de curso), pagos y split de
  comisión, calendario/agenda, videollamada o integración con Zoom/Meet, reseñas/calificación,
  y probablemente boleta de honorarios (SII) para cada profesor.

**A quién resuelve**: familias que ya usan Logos para autoestudio y quieren apoyo humano
puntual en una materia específica; profesores que quieren un canal adicional de ingresos
dando clases particulares.

**A quién NO resuelve / qué no es**: no reemplaza el rol Profesor de Etapa 2 (gestión de
Curso/Sección, gratuito, sin dinero de por medio) — son dos cosas distintas que conviven.
Tampoco es un colegio online con clases en vivo grupales (eso es más parecido a
colegionline.cl, ya descartado en la conversación de la landing).

## Preguntas que hay que responder antes de diseñar el modelo de datos

1. **¿Marketplace abierto o profesores curados por Logos?**
   - Abierto (tipo Superprof): cualquier Profesor aprobado puede publicar que ofrece
     reforzamiento, fija su propio precio y horario. Más escalable, pero exige verificación
     de identidad mucho más fuerte que la aprobación simple actual (revisión manual con un
     clic) — estamos hablando de adultos cobrando por estar 1-a-1 con menores.
   - Curado (tipo Wited): Logos selecciona/entrevista profesores, fija precios de catálogo,
     asigna internamente. Más control y seguridad, pero no escala solo con "que se
     registren" — requiere operación humana de Logos detrás.
2. **¿Cómo se le paga al profesor?** — Chile: normalmente boleta de honorarios (profesor
   independiente) con retención de impuesto. Logos tendría que: (a) generar/recibir boletas,
   (b) hacer split de la comisión de la plataforma, (c) definir esa comisión (Superprof cobra
   ~X%, Preply ~33% la primera clase y menos después — hay que investigar tarifas de mercado
   antes de fijar la propia).
3. **¿Individual (1 a 1) o grupal?** — 1 a 1 es más simple de construir (agenda, precio,
   videollamada) pero más caro para la familia; grupal (tipo mini-curso) es más parecido al
   Curso/Sección ya construido, podría reutilizar más código, pero cambia la propuesta de
   valor ("tu profesor particular" vs. "un grupo con tu profesor").
4. **¿Videollamada propia o integración externa?** — construir videollamada propia es un
   proyecto en sí mismo (WebRTC, grabación por seguridad, moderación); lo razonable para un
   MVP de esto sería generar un link de Zoom/Google Meet por sesión agendada, no construir
   video propio.
5. **¿Seguridad del menor durante la sesión?** — punto no negociable dado el público objetivo
   de Logos: ¿la sesión queda grabada por política (con consentimiento del apoderado)? ¿el
   apoderado puede unirse o ver el historial de sesiones? ¿hay un canal de reporte si algo
   sale mal? Esto necesita su propio documento de política antes de construir, con el mismo
   cuidado que ya se aplicó en `10-privacidad-y-datos-de-menores.md`.
6. **¿Cómo calza con el tope de precio de $19.990 ya decidido?** — ese tope es explícitamente
   para el **contenido de autoestudio** (`09-modelo-de-negocio.md`); reforzamiento con
   profesor humano es otro producto con otra estructura de costos (hay que pagarle al
   profesor), así que necesita su propio rango de precios, no forzarlo bajo el mismo tope.

## Qué SÍ ya tenemos construido y reutilizable (si se decide avanzar)

- `CuentaProfesor` con aprobación manual del Administrador (Etapa 2) — sirve como base de
  "profesor verificado", aunque probablemente necesite un nivel de verificación adicional
  específico para reforzamiento pagado (ver pregunta 1 arriba).
- El panel Admin (`comercial`) ya tiene el patrón de `Plan`/`Suscripcion` — se podría extender
  en vez de inventar un sistema de cobro paralelo.
- El patrón de bounded context hexagonal (domain/application/infrastructure) ya está
  probado 6 veces en este proyecto (auth, progreso, plan_estudio, admin, comercial, profesor)
  — un nuevo contexto `reforzamiento` seguiría exactamente el mismo molde cuando se decida
  construir.

## Recomendación (no implementar todavía)

1. Primero decidir las 6 preguntas de arriba con el usuario — especialmente 1 (marketplace
   abierto vs. curado) y 5 (seguridad del menor), que cambian el diseño completo.
2. Si se decide avanzar, tratarlo como una **iniciativa nueva del roadmap** (como Etapa 2 lo
   fue para Rol Profesor), con su propio Fase 0 → especificación → arquitectura → roadmap por
   etapas, no como un ítem chico dentro de lo que ya existe.
3. Un MVP mínimo razonable, si se decide seguir el modelo curado (más simple y más seguro
   para partir): Logos cataloga un puñado de profesores ya verificados manualmente, precio
   fijo por sesión, agenda simple (el profesor publica huecos disponibles, el apoderado
   reserva), link de Meet/Zoom generado por sesión, sin manejo de pago automatizado al
   principio (activación manual como ya se hace con Cortesías) — recién ahí evaluar
   marketplace abierto y pagos automatizados si el modelo curado valida demanda.

## Fuentes

- [wited.com/cl/reforzamiento](https://www.wited.com/cl/reforzamiento/) (investigado 2026-08-13).
