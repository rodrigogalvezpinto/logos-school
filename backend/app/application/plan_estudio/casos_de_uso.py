from datetime import date

from app.domain.auth.ports import RepositorioPerfilesAlumno
from app.domain.contenido.ports import RepositorioContenido
from app.domain.plan_estudio.entities import PlanDeEstudio
from app.domain.plan_estudio.exceptions import PerfilAlumnoNoEncontrado, PlanDeEstudioNoEncontrado
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
