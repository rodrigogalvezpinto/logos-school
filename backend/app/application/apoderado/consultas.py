"""Vistas agregadas para el Apoderado, sobre todos sus alumnos a la vez — idea propia (no
un hallazgo de Brincus). Cruce legítimo entre contextos ya existentes (auth, progreso,
gamificación, plan_estudio), mismo criterio que ya usan `ObtenerProgresoDeCurso` o
`AgregarSesionDeRepaso`: no se duplica ninguna lógica de cálculo, solo se reutilizan los
casos de uso ya construidos, una vez por alumno."""

from dataclasses import dataclass
from datetime import date, timedelta

from app.application.prediccion.consultas import EvaluarRitmoDeEstudio, ObtenerMapaDeCalorPorEje
from app.application.progreso.consultas import ObtenerFaltantes
from app.domain.agenda_familiar.ports import RepositorioAgendaFamiliar
from app.domain.auth.ports import RepositorioPerfilesAlumno
from app.domain.evaluaciones.ports import RepositorioIntentos
from app.domain.gamificacion.ports import RepositorioGamificacion
from app.domain.progreso.ports import RepositorioProgreso


@dataclass(frozen=True)
class EstadisticaAlumno:
    perfil_alumno_id: int
    nombre: str
    cobertura_pct: float
    racha_dias_actual: int
    tiene_alerta_de_ritmo: bool


class ObtenerEstadisticasFamiliares:
    """Idea 1 del boceto de innovación (2026-08-17): "Estadísticas" como vista propia del
    Apoderado, distinta de entrar al detalle de "Mis Notas" de cada hijo por separado."""

    def __init__(
        self,
        repositorio_perfiles: RepositorioPerfilesAlumno,
        repositorio_gamificacion: RepositorioGamificacion,
        obtener_faltantes: ObtenerFaltantes,
        evaluar_ritmo: EvaluarRitmoDeEstudio,
    ):
        self._repositorio_perfiles = repositorio_perfiles
        self._repositorio_gamificacion = repositorio_gamificacion
        self._obtener_faltantes = obtener_faltantes
        self._evaluar_ritmo = evaluar_ritmo

    def ejecutar(self, cuenta_apoderado_id: int, hoy: date) -> list[EstadisticaAlumno]:
        alumnos = self._repositorio_perfiles.listar_por_cuenta(cuenta_apoderado_id)
        resultado: list[EstadisticaAlumno] = []

        for alumno in alumnos:
            faltantes = self._obtener_faltantes.ejecutar(alumno.id, alumno.nivel_id)
            cobertura_pct = (
                round(sum(c.cobertura_pct for c in faltantes.coberturas) / len(faltantes.coberturas), 1)
                if faltantes.coberturas else 0.0
            )
            gamificacion = self._repositorio_gamificacion.obtener_o_crear(alumno.id)
            alerta = self._evaluar_ritmo.ejecutar(alumno.id, hoy)

            resultado.append(
                EstadisticaAlumno(
                    perfil_alumno_id=alumno.id,
                    nombre=alumno.nombre,
                    cobertura_pct=cobertura_pct,
                    racha_dias_actual=gamificacion.racha_dias_actual,
                    tiene_alerta_de_ritmo=bool(alerta and alerta.tiene_alerta),
                )
            )

        return resultado


# Metas familiares compartidas — idea 9 del boceto de innovación (2026-08-17): con 2+
# alumnos, una meta conjunta ("la familia estudió N días combinados esta semana") en vez de
# un ranking que compare a un hermano con otro — mismo cuidado de evitar comparación directa
# que ya se aplica entre alumnos de toda la plataforma, puertas adentro de una misma familia
# también. "Día combinado" = un día activo de un alumno; si 2 hijos estudian el mismo día,
# cuenta 2 (no es "días distintos del calendario familiar", es esfuerzo total sumado).


@dataclass(frozen=True)
class MetaFamiliar:
    dias_esta_semana: int
    dias_semana_anterior: int
    es_nueva_marca: bool


class ObtenerMetaFamiliar:
    def __init__(
        self,
        repositorio_perfiles: RepositorioPerfilesAlumno,
        repositorio_intentos: RepositorioIntentos,
        repositorio_progreso: RepositorioProgreso,
    ):
        self._repositorio_perfiles = repositorio_perfiles
        self._repositorio_intentos = repositorio_intentos
        self._repositorio_progreso = repositorio_progreso

    def ejecutar(self, cuenta_apoderado_id: int, hoy: date) -> MetaFamiliar | None:
        alumnos = self._repositorio_perfiles.listar_por_cuenta(cuenta_apoderado_id)
        if len(alumnos) < 2:
            return None  # con un solo alumno no hay "familia" que sumar

        inicio_semana_actual = hoy - timedelta(days=hoy.weekday())  # lunes de esta semana
        inicio_semana_anterior = inicio_semana_actual - timedelta(days=7)

        dias_esta_semana = 0
        dias_semana_anterior = 0
        for alumno in alumnos:
            fechas = {i.fecha_termino.date() for i in self._repositorio_intentos.listar_entregados_por_perfil(alumno.id) if i.fecha_termino}
            fechas |= {g.fecha.date() for g in self._repositorio_progreso.listar_guias_revisadas(alumno.id)}

            dias_esta_semana += sum(1 for f in fechas if inicio_semana_actual <= f <= hoy)
            dias_semana_anterior += sum(1 for f in fechas if inicio_semana_anterior <= f < inicio_semana_actual)

        return MetaFamiliar(
            dias_esta_semana=dias_esta_semana,
            dias_semana_anterior=dias_semana_anterior,
            es_nueva_marca=dias_esta_semana > dias_semana_anterior,
        )


# Agenda familiar del domingo — idea 7 del boceto de innovación (2026-08-17): 3 preguntas
# armadas a partir de datos reales del alumno (no genéricas), para que la mamá no tenga que
# inventar de qué hablar. Se puede marcar "ya conversamos" y no vuelve a insistir esa misma
# semana — sí vuelve la semana siguiente.


@dataclass(frozen=True)
class AgendaFamiliar:
    preguntas: list[str]
    ya_conversada: bool


def _inicio_de_semana(hoy: date) -> date:
    return hoy - timedelta(days=hoy.weekday())


class ObtenerAgendaFamiliar:
    def __init__(
        self,
        obtener_mapa_calor: ObtenerMapaDeCalorPorEje,
        repositorio_gamificacion: RepositorioGamificacion,
        evaluar_ritmo: EvaluarRitmoDeEstudio,
        repositorio_agenda: RepositorioAgendaFamiliar,
    ):
        self._obtener_mapa_calor = obtener_mapa_calor
        self._repositorio_gamificacion = repositorio_gamificacion
        self._evaluar_ritmo = evaluar_ritmo
        self._repositorio_agenda = repositorio_agenda

    def ejecutar(self, perfil_alumno_id: int, hoy: date) -> AgendaFamiliar:
        preguntas: list[str] = []

        celdas = self._obtener_mapa_calor.ejecutar(perfil_alumno_id)
        if celdas:
            peor = min(celdas, key=lambda c: c.pct_correctas)
            preguntas.append(f"Esta semana le costó más {peor.eje_tematico} — pregúntale qué fue lo más difícil.")

        gamificacion = self._repositorio_gamificacion.obtener_o_crear(perfil_alumno_id)
        if gamificacion.racha_dias_actual >= 2:
            preguntas.append(
                f"Estudió {gamificacion.racha_dias_actual} días seguidos — vale la pena celebrarlo, aunque sea chico."
            )

        alerta = self._evaluar_ritmo.ejecutar(perfil_alumno_id, hoy)
        if alerta:
            if alerta.tiene_alerta:
                preguntas.append("Va atrasado con su plan de estudio — pregúntale si necesita ayuda para ponerse al día.")
            else:
                preguntas.append("Va a buen ritmo con su plan de estudio — vale la pena reconocérselo.")

        if not preguntas:
            preguntas.append("¿Cómo se ha sentido esta semana estudiando? Vale la pena preguntarle, sin más.")

        return AgendaFamiliar(
            preguntas=preguntas[:3],
            ya_conversada=self._repositorio_agenda.ya_conversada(perfil_alumno_id, _inicio_de_semana(hoy)),
        )
