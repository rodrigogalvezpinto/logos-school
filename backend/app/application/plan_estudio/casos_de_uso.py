from datetime import date, timedelta

from app.domain.auth.ports import RepositorioPerfilesAlumno
from app.domain.contenido.ports import RepositorioContenido
from app.domain.plan_estudio.entities import PlanDeEstudio, SesionEstudio, siguiente_fecha_disponible
from app.domain.plan_estudio.exceptions import (
    AsignaturaNoEncontrada,
    NivelNoEsAnterior,
    PerfilAlumnoNoEncontrado,
    PlanDeEstudioNoEncontrado,
)
from app.domain.plan_estudio.ports import RepositorioPlanEstudio
from app.domain.progreso.ports import RepositorioProgreso
from app.domain.shared.reloj import Reloj


class CrearPlanDeEstudio:
    def __init__(
        self,
        repositorio_plan_estudio: RepositorioPlanEstudio,
        repositorio_perfiles: RepositorioPerfilesAlumno,
        repositorio_contenido: RepositorioContenido,
        repositorio_progreso: RepositorioProgreso,
        reloj: Reloj,
    ):
        self._repositorio_plan_estudio = repositorio_plan_estudio
        self._repositorio_perfiles = repositorio_perfiles
        self._repositorio_contenido = repositorio_contenido
        self._repositorio_progreso = repositorio_progreso
        self._reloj = reloj

    def ejecutar(
        self, perfil_alumno_id: int, dias_por_semana: int, dias_elegidos: list[str], fecha_objetivo: date | None
    ) -> PlanDeEstudio:
        perfil = self._repositorio_perfiles.buscar_por_id(perfil_alumno_id)
        if not perfil:
            raise PerfilAlumnoNoEncontrado()

        revisadas = {g.oa_id for g in self._repositorio_progreso.listar_guias_revisadas(perfil_alumno_id)}
        pendientes_por_asignatura: dict[int, list[int]] = {}
        for asignatura in self._repositorio_contenido.listar_asignaturas(perfil.nivel_id):
            pendientes = [
                oa.id for oa in self._repositorio_contenido.listar_objetivos(asignatura.id) if oa.id not in revisadas
            ]
            if pendientes:
                pendientes_por_asignatura[asignatura.id] = pendientes

        plan = PlanDeEstudio.crear(
            perfil_alumno_id=perfil_alumno_id,
            dias_por_semana=dias_por_semana,
            dias_elegidos=dias_elegidos,
            fecha_inicio=self._reloj.ahora().date(),
            fecha_objetivo=fecha_objetivo,
            pendientes_por_asignatura=pendientes_por_asignatura,
        )
        return self._repositorio_plan_estudio.reemplazar_plan(plan)


class ObtenerPlanActivo:
    def __init__(self, repositorio_plan_estudio: RepositorioPlanEstudio, repositorio_progreso: RepositorioProgreso):
        self._repositorio_plan_estudio = repositorio_plan_estudio
        self._repositorio_progreso = repositorio_progreso

    def ejecutar(self, perfil_alumno_id: int) -> tuple[PlanDeEstudio, dict[int, bool]]:
        plan = self._repositorio_plan_estudio.buscar_activo_por_perfil(perfil_alumno_id)
        if not plan:
            raise PlanDeEstudioNoEncontrado()
        revisadas = {g.oa_id for g in self._repositorio_progreso.listar_guias_revisadas(perfil_alumno_id)}
        cumplidas = {sesion.id: sesion.esta_cumplida(revisadas) for sesion in plan.sesiones}
        return plan, cumplidas


class AgregarSesionDeRepaso:
    """Agrega al plan ya existente una sesión de repaso de contenido de un nivel YA
    CURSADO (no del nivel actual) — hallazgo comparando en vivo contra Brincus, ver
    planificacion/25-analisis-competencia-brincus.md: "permite agregar contenido de años
    anteriores para repasar". Se agenda al final del plan existente, en el próximo día que
    calce con el horario que el alumno ya eligió — no reemplaza nada del plan actual."""

    def __init__(
        self,
        repositorio_plan_estudio: RepositorioPlanEstudio,
        repositorio_perfiles: RepositorioPerfilesAlumno,
        repositorio_contenido: RepositorioContenido,
    ):
        self._repositorio_plan_estudio = repositorio_plan_estudio
        self._repositorio_perfiles = repositorio_perfiles
        self._repositorio_contenido = repositorio_contenido

    def ejecutar(self, perfil_alumno_id: int, asignatura_id: int, oa_ids: list[int]) -> SesionEstudio:
        perfil = self._repositorio_perfiles.buscar_por_id(perfil_alumno_id)
        if not perfil:
            raise PerfilAlumnoNoEncontrado()

        plan = self._repositorio_plan_estudio.buscar_activo_por_perfil(perfil_alumno_id)
        if not plan:
            raise PlanDeEstudioNoEncontrado()

        asignatura = self._repositorio_contenido.obtener_asignatura(asignatura_id)
        if not asignatura:
            raise AsignaturaNoEncontrada()
        # El repaso es de contenido YA CURSADO — comparar por `Nivel.orden` (curricular
        # real, 1=1° básico...12=4° medio), NUNCA por `Nivel.id` (bug real encontrado: en
        # la base de Desarrollo, 4° básico —el piloto— se importó primero y quedó con
        # id=1, antes que 1°-3° básico, así que comparar por id dejaba al piloto sin
        # ningún nivel "anterior" disponible para repasar).
        nivel_actual = self._repositorio_contenido.obtener_nivel(perfil.nivel_id)
        nivel_asignatura = self._repositorio_contenido.obtener_nivel(asignatura.nivel_id)
        if not nivel_actual or not nivel_asignatura:
            raise NivelNoEsAnterior()
        if nivel_asignatura.orden is None or nivel_actual.orden is None:
            raise NivelNoEsAnterior()
        if nivel_asignatura.orden >= nivel_actual.orden:
            raise NivelNoEsAnterior()

        ultima_fecha = max((s.fecha_programada for s in plan.sesiones), default=plan.fecha_inicio)
        fecha = siguiente_fecha_disponible(plan.dias_elegidos, ultima_fecha + timedelta(days=1))

        sesion = SesionEstudio(
            id=None, plan_estudio_id=plan.id, fecha_programada=fecha,
            asignatura_id=asignatura_id, oa_ids=oa_ids, incluye_prueba_unidad=False, es_repaso=True,
        )
        return self._repositorio_plan_estudio.agregar_sesion(plan.id, sesion)
