---
título: Documento de continuación — Fase 1.3 en construcción (cortada a mitad de camino)
estado: ✅ obsoleto — la Fase 1.3 se completó en la misma conversación, no se cambió de
  chat. Se deja como registro histórico; ver `13-plan-de-estudio.md` y
  `22-analisis-de-brechas.md` para el estado vigente.
última actualización: 2026-08-13
---

## Por qué existe este documento

La conversación anterior se cortó a mitad de la implementación de la Fase 1.3 (plan de
estudio con horario + habilitación progresiva + simulacro parcial) para cambiar a un chat
nuevo. Esto deja constancia exacta de qué se hizo, qué falta, y cómo retomarlo sin perder
contexto ni repetir trabajo.

**Primera acción al retomar: leer el plan completo y aprobado en
`/Users/rodrigogalvez/.claude/plans/eventual-strolling-gadget.md`** — ese archivo tiene el
diseño completo (decisiones de alcance, arquitectura, archivos críticos, verificación) tal
como quedó aprobado por el usuario. Este documento es un complemento — dice **qué de ese
plan ya está hecho** y qué falta, no repite el diseño completo.

## Contexto del proyecto (por si el chat nuevo no lo tiene)

Proyecto **Logos School**: plataforma de estudio para Exámenes Libres de Chile. Backend
FastAPI+SQLModel+Postgres en arquitectura hexagonal (`domain/`/`application/`/
`infrastructure/` por bounded context, composition root en `backend/app/core/deps.py`),
frontend Angular standalone+signals. El usuario pidió explícitamente esta arquitectura
hexagonal con SOLID y patrones de diseño nombrados — no es una elección mía, es un requisito
duro que ya se aplicó consistentemente en todo el backend.

**Orden de trabajo acordado con el usuario**: Fase 1.2 (✅ completa) → Panel de
Administrador (✅ completo) → **Fase 1.3 (🔄 en construcción, este documento)** → Rol
Profesor (⏳ no iniciado). Todo el trabajo hasta ahora está commiteado en git — la Fase 1.3
es la primera que queda a medio camino sin commit.

Estado de tests antes de empezar Fase 1.3 (línea base a no romper):
**76/76 tests de backend, 29/29 E2E de Playwright.**

## Qué se alcanzó a construir de la Fase 1.3 (sin commitear todavía)

Archivos nuevos, ya escritos y verificados que no rompen nada (`uv run pytest -q` sigue
76/76 en verde):

- `backend/app/domain/plan_estudio/__init__.py` — vacío, solo paquete.
- `backend/app/domain/plan_estudio/exceptions.py` — `DiasInvalidos`, `PlanDeEstudioNoEncontrado`.
- `backend/app/domain/plan_estudio/entities.py` — **completo**:
  - `SesionEstudio` (dataclass: `id, plan_estudio_id, fecha_programada, asignatura_id, oa_ids, incluye_prueba_unidad`)
    con `esta_cumplida(oa_revisados: set[int]) -> bool` y `minutos_estimados() -> int`
    (`len(oa_ids) * MINUTOS_POR_OA`, constante `MINUTOS_POR_OA = 25`).
  - `PlanDeEstudio` (dataclass, incluye `sesiones: list[SesionEstudio]`) con factory
    `crear(perfil_alumno_id, dias_por_semana, dias_elegidos, fecha_inicio, fecha_objetivo, pendientes_por_asignatura)`
    que valida `dias_por_semana ∈ {3,4,5}`, `len(dias_elegidos) == dias_por_semana`, y que
    los días sean válidos (`DIAS_VALIDOS = {"lunes",...,"domingo"}`), y llama a
    `generar_sesiones(...)`.
  - `generar_sesiones(pendientes_por_asignatura, dias_elegidos, fecha_inicio, fecha_objetivo) -> list[SesionEstudio]`:
    **función pura, sin I/O**, ya implementada — reparto round-robin de OA pendientes entre
    las fechas disponibles (calculadas por `_fechas_disponibles`, que usa `fecha_objetivo` o
    `fecha_inicio + 8 semanas` por defecto — `SEMANAS_PLAZO_DEFECTO = 8`), alternando
    asignaturas, marcando `incluye_prueba_unidad=True` en la última sesión de cada
    asignatura (cuando su cola de OA pendientes queda vacía). Tiene una cota de seguridad
    (`intentos_maximos`) para no loopear infinito si hay asignaturas sin fechas suficientes.
    **Esta función es exactamente el tipo de lógica que el plan pide testear con
    `tests/unit/domain/test_plan_de_estudio.py` — todavía no se escribió ese test.**
  - `backend/app/domain/plan_estudio/ports.py` — `RepositorioPlanEstudio` (Protocol):
    `buscar_activo_por_perfil(perfil_alumno_id) -> PlanDeEstudio | None`,
    `reemplazar_plan(plan: PlanDeEstudio) -> PlanDeEstudio` (borra el plan+sesiones previo
    del perfil si existe, guarda el nuevo).
- `backend/app/application/plan_estudio/__init__.py` — vacío, creado, **sin casos de uso
  todavía** (`CrearPlanDeEstudio`/`ObtenerPlanActivo` del plan aún no están escritos).
- `backend/app/domain/evaluaciones/ports.py` — **modificado**: se agregó a
  `RepositorioConjuntos` el método `crear(tipo, nombre, forma, asignatura_id, nivel_id,
  pregunta_ids, tiempo_sugerido_min) -> ConjuntoLectura` (con docstring explicando que es el
  único método de escritura del puerto, para el simulacro parcial). **Ojo: este método
  todavía NO está implementado en `RepositorioConjuntosSQLModel`** — como es un
  `typing.Protocol`, Python no lo exige en tiempo de ejecución, así que no rompe nada hoy,
  pero cualquier código que intente usarlo fallará con `AttributeError` hasta que se
  implemente en `backend/app/infrastructure/persistence/repositorios/conjuntos.py`.

**Nada de esto está commiteado.** `git status` muestra:
```
 M backend/app/domain/evaluaciones/ports.py
?? backend/app/application/plan_estudio/
?? backend/app/domain/plan_estudio/
```

## Qué falta (siguiendo el plan en `eventual-strolling-gadget.md`, en orden razonable)

1. **`RepositorioConjuntosSQLModel.crear(...)`** en
   `backend/app/infrastructure/persistence/repositorios/conjuntos.py` — implementar el
   método nuevo del puerto (insertar fila `ConjuntoEvaluacion`, devolver `ConjuntoLectura`).
2. **ORM nuevo** en `backend/app/infrastructure/persistence/orm_models.py`: tablas
   `PlanDeEstudio` (`dias_elegidos` como columna JSON) y `SesionEstudio` (`oa_ids` como
   columna JSON) — **sin columna `estado`** (decisión ya tomada: el estado de una sesión se
   calcula al leer, nunca se persiste — ver el plan completo para el razonamiento).
   Después: `uv run alembic revision --autogenerate -m plan_de_estudio` +
   revisar el archivo generado a mano (mismo cuidado que las migraciones anteriores — por
   ejemplo, si alguna columna nueva NOT NULL cae sobre una tabla con filas existentes, hace
   falta `server_default`, aunque acá probablemente no aplica porque son tablas nuevas) +
   `uv run alembic upgrade head`.
3. **`backend/app/infrastructure/persistence/repositorios/plan_estudio.py`** (nuevo) —
   `RepositorioPlanEstudioSQLModel` implementando el puerto de arriba.
4. **`backend/app/application/plan_estudio/casos_de_uso.py`** (nuevo) —
   `CrearPlanDeEstudio` y `ObtenerPlanActivo`, exactamente como los describe el plan
   (`ObtenerPlanActivo` recalcula `esta_cumplida` de cada sesión contra
   `RepositorioProgreso.listar_guias_revisadas` actual, nunca lee un campo persistido).
5. **`GenerarSimulacroParcial`** nuevo en
   `backend/app/application/evaluaciones/casos_de_uso.py` — ver el plan para la lógica
   exacta (umbral 50% de cobertura, `UMBRAL_SIMULACRO_PARCIAL = 0.5`, arma preguntas
   autocorregibles de las OA cubiertas, llama a `RepositorioConjuntos.crear(...)`).
6. **`ObtenerFaltantes`** nuevo en `backend/app/application/progreso/consultas.py` — lista
   de pruebas/exámenes no rendidos por asignatura, con `habilitado: bool` calculado (ver
   reglas de habilitación exactas en el plan: prueba de unidad habilitada si todas sus OA
   —derivadas de `Pregunta.oa_id`— están revisadas; examen completo habilitado al 100% de
   cobertura de la asignatura o del nivel para Régimen A).
7. **`core/deps.py`**: factories nuevas (`get_repositorio_plan_estudio`,
   `get_crear_plan_de_estudio_uc`, `get_obtener_plan_activo_uc`,
   `get_generar_simulacro_parcial_uc`, `get_obtener_faltantes_uc`), mismo estilo que las
   ~30 factories que ya existen ahí.
8. **Routers**: `backend/app/routers/plan_estudio.py` (nuevo, `POST`/`GET
   /plan-estudio/{perfil_alumno_id}`, protegido con `verificar_perfil_propio` igual que
   `progreso.py`), extender `progreso.py` (`GET /progreso/{perfil_alumno_id}/faltantes`) y
   `evaluaciones.py` (`POST /evaluaciones/simulacro-parcial/{asignatura_id}`). Registrar el
   router nuevo en `backend/app/main.py`.
9. **Tests backend** (ver plan para la lista completa): `tests/unit/domain/test_plan_de_estudio.py`
   (la función pura `generar_sesiones` — varios escenarios de reparto, sin DB),
   `tests/test_plan_estudio.py`, `tests/test_evaluaciones_simulacro_parcial.py`, extender
   `tests/test_progreso.py` con casos de `/faltantes`. Correr `uv run pytest -q` — debe
   seguir en verde (76/76 + los nuevos).
10. **Frontend completo** — nada de esto se empezó todavía:
    - `frontend/src/app/core/plan-estudio.service.ts` (nuevo).
    - `frontend/src/app/pages/agregar-alumno/agregar-alumno.ts` — agregar selección de días
      (checkboxes, mínimo 3) + fecha objetivo opcional, llamar a crear el plan tras crear el
      perfil.
    - `frontend/src/app/pages/plan-estudio/plan-estudio.ts` (nuevo, ruta
      `/alumno/plan-estudio`) — banner "hoy te toca" + lista de próximas sesiones.
    - `frontend/src/app/pages/notas/notas.ts` — sección "Pruebas y exámenes faltantes" +
      botón "Rendir simulacro parcial" cuando corresponda.
    - `frontend/src/app/shared/sidebar/sidebar.ts` — quitar `proximamente: true` de "Plan de
      Estudio".
11. **E2E**: `frontend/e2e/plan-estudio.spec.ts` (nuevo) + extender el spec de
    faltantes/simulacro parcial. Correr `npx playwright test --workers=1` — debe seguir en
    verde (29/29 + los nuevos). El backend (`uvicorn --reload`) y frontend (`ng serve`) ya
    están corriendo en background en esta máquina (puertos 8000 y 4300) — probablemente
    sigan corriendo si la máquina no se reinició; si no, hay que levantarlos de nuevo.
12. **Commit final** de toda la Fase 1.3 junta (backend+frontend+tests), actualizar
    `planificacion/13-plan-de-estudio.md` (marcar como completa) y
    `planificacion/22-analisis-de-brechas.md` (mover Fase 1.3 a resuelto), igual que se hizo
    al cerrar la Fase 1.2 y el Panel de Administrador.

## Después de la Fase 1.3

Sigue **Rol Profesor** (Etapa 2 del roadmap) — todavía sin ningún diseño hecho. Cuando le
toque el turno, retomar desde `planificacion/01-roles-y-permisos.md` (sección Profesor,
requiere verificación manual por un Administrador antes de activarse — por eso se secuenció
después del Panel de Administrador, que es quien aprueba esas cuentas) y
`planificacion/03-roadmap-etapas.md` (Etapa 2).

## Recordatorios de proceso (para el chat nuevo)

- El usuario dio feedback explícito de **no pedir confirmaciones sí/no** — actuar con
  criterio propio, avanzar, informar después (ver memoria global
  `feedback_no_pedir_confirmaciones`).
- El usuario exigió explícitamente arquitectura hexagonal + SOLID + patrones de diseño
  nombrados en todo el backend — no es opcional, ya está aplicado en todo lo construido
  hasta ahora y hay que seguir el mismo patrón exacto (ver cualquier bounded context
  existente — `domain/progreso/`, `domain/comercial/` son los más recientes y los más
  parecidos en forma a lo que falta de `domain/plan_estudio/`).
- Verificar SIEMPRE con `uv run pytest -q` y `npx playwright test --workers=1` después de
  cada pieza — así se ha trabajado en todas las fases anteriores, no dejar código sin correr
  los tests reales.
- La base de datos de Desarrollo (`logos_dev`) es persistente entre corridas de test E2E —
  usar sufijos únicos (`Date.now()`) en nombres/códigos creados por tests E2E para evitar
  colisión con datos de corridas anteriores (ya pasó una vez con "Plan E2E" en el Panel de
  Administrador, ver `frontend/e2e/admin.spec.ts` para el patrón de solución).
