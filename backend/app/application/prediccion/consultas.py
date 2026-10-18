"""Nota estimada del Examen Libre — idea propia (no un hallazgo de Brincus: ni Brincus ni
ningún competidor revisado en `planificacion/25-analisis-competencia-brincus.md` proyecta una
nota, solo separan "progreso" de "calificaciones"). Fórmula aritmética simple y transparente,
sin IA/modelo: combina la nota de práctica (pruebas de unidad) con la de simulacro (más
parecida al examen real) y la pondera con qué tanto del temario ya se cubrió — así una nota
alta con poca cobertura no se muestra con la misma confianza que una nota alta con el temario
casi completo. Reutiliza `ObtenerHistorialYNotas` y `ObtenerFaltantes` tal cual, sin duplicar
el cálculo de notas/cobertura que ya existen."""

from dataclasses import dataclass
from datetime import date, datetime, timedelta

from app.application.progreso.consultas import ObtenerFaltantes, ObtenerHistorialYNotas
from app.domain.contenido.ports import RepositorioContenido
from app.domain.evaluaciones.ports import RepositorioIntentos, RepositorioPreguntas
from app.domain.evaluaciones.value_objects import TIPOS_AUTOCORREGIBLES
from app.domain.plan_estudio.ports import RepositorioPlanEstudio
from app.domain.progreso.ports import RepositorioProgreso

PESO_SIMULACRO = 0.65
PESO_PRACTICA = 0.35
UMBRAL_COBERTURA_ALTA = 70.0
UMBRAL_COBERTURA_MEDIA = 50.0

ORDEN_CONFIANZA = {"sin_datos": 0, "baja": 1, "media": 2, "alta": 3}


@dataclass(frozen=True)
class EstimacionAsignatura:
    asignatura_id: int
    asignatura_nombre: str
    nota_estimada: float | None
    confianza: str  # "sin_datos" | "baja" | "media" | "alta"
    cobertura_pct: float


@dataclass(frozen=True)
class EstimacionExamen:
    nota_general_estimada: float | None
    confianza_general: str
    por_asignatura: list[EstimacionAsignatura]


def _estimar_asignatura(nota_practica: float | None, nota_simulacro: float | None, cobertura_pct: float) -> tuple[float | None, str]:
    if nota_simulacro is not None and nota_practica is not None:
        estimada = round(PESO_SIMULACRO * nota_simulacro + PESO_PRACTICA * nota_practica, 1)
        confianza = "alta" if cobertura_pct >= UMBRAL_COBERTURA_ALTA else "media"
        return estimada, confianza
    if nota_simulacro is not None:
        confianza = "media" if cobertura_pct >= UMBRAL_COBERTURA_MEDIA else "baja"
        return nota_simulacro, confianza
    if nota_practica is not None:
        return nota_practica, "baja"
    return None, "sin_datos"


class EstimarNotaExamen:
    def __init__(self, obtener_historial_y_notas: ObtenerHistorialYNotas, obtener_faltantes: ObtenerFaltantes):
        self._obtener_historial_y_notas = obtener_historial_y_notas
        self._obtener_faltantes = obtener_faltantes

    def ejecutar(self, perfil_alumno_id: int, nivel_id: int) -> EstimacionExamen:
        historial = self._obtener_historial_y_notas.ejecutar(perfil_alumno_id)
        faltantes = self._obtener_faltantes.ejecutar(perfil_alumno_id, nivel_id)

        notas_por_id = {n.asignatura_id: n for n in historial.notas_por_asignatura}

        por_asignatura: list[EstimacionAsignatura] = []
        for cobertura in faltantes.coberturas:
            nota = notas_por_id.get(cobertura.asignatura_id)
            nota_practica = nota.nota_practica if nota else None
            nota_simulacro = nota.nota_simulacro if nota else None
            estimada, confianza = _estimar_asignatura(nota_practica, nota_simulacro, cobertura.cobertura_pct)
            por_asignatura.append(
                EstimacionAsignatura(
                    asignatura_id=cobertura.asignatura_id,
                    asignatura_nombre=cobertura.asignatura_nombre,
                    nota_estimada=estimada,
                    confianza=confianza,
                    cobertura_pct=cobertura.cobertura_pct,
                )
            )

        con_datos = [a for a in por_asignatura if a.nota_estimada is not None]
        if con_datos:
            nota_general = round(sum(a.nota_estimada for a in con_datos) / len(con_datos), 1)
            confianza_general = min((a.confianza for a in con_datos), key=lambda c: ORDEN_CONFIANZA[c])
        else:
            nota_general = None
            confianza_general = "sin_datos"

        return EstimacionExamen(
            nota_general_estimada=nota_general, confianza_general=confianza_general, por_asignatura=por_asignatura,
        )


# Alerta temprana de ritmo de estudio — idea propia (no un hallazgo de Brincus): compara
# el ritmo real con el que el alumno viene revisando guías contra el ritmo que necesitaría
# para cubrir todo el contenido planeado antes de la fecha objetivo del plan de estudio
# (`PlanDeEstudio.fecha_objetivo`, ya existía, opcional). Solo aritmética simple y
# transparente sobre datos que ya existen — sin IA.


@dataclass(frozen=True)
class AlertaRitmoEstudio:
    tiene_alerta: bool
    mensaje: str
    dias_restantes: int
    oa_pendientes: int
    ritmo_actual_oa_por_dia: float
    ritmo_necesario_oa_por_dia: float


class EvaluarRitmoDeEstudio:
    def __init__(self, repositorio_plan_estudio: RepositorioPlanEstudio, repositorio_progreso: RepositorioProgreso):
        self._repositorio_plan_estudio = repositorio_plan_estudio
        self._repositorio_progreso = repositorio_progreso

    def ejecutar(self, perfil_alumno_id: int, hoy: date) -> AlertaRitmoEstudio | None:
        plan = self._repositorio_plan_estudio.buscar_activo_por_perfil(perfil_alumno_id)
        if not plan or not plan.fecha_objetivo:
            return None  # sin plan o sin fecha objetivo, no hay nada que proyectar

        dias_restantes = (plan.fecha_objetivo - hoy).days
        if dias_restantes <= 0:
            return None  # la fecha objetivo ya llegó o pasó, ya no aplica una alerta "temprana"

        oa_del_plan: set[int] = set()
        for sesion in plan.sesiones:
            oa_del_plan.update(sesion.oa_ids)

        revisadas = {g.oa_id for g in self._repositorio_progreso.listar_guias_revisadas(perfil_alumno_id)}
        oa_revisados_del_plan = oa_del_plan & revisadas
        oa_pendientes = len(oa_del_plan - revisadas)

        if oa_pendientes == 0:
            return AlertaRitmoEstudio(
                tiene_alerta=False, mensaje="Ya revisaste todo el contenido de tu plan actual — vas muy bien.",
                dias_restantes=dias_restantes, oa_pendientes=0, ritmo_actual_oa_por_dia=0.0,
                ritmo_necesario_oa_por_dia=0.0,
            )

        dias_transcurridos = max((hoy - plan.fecha_inicio).days, 1)
        ritmo_actual = round(len(oa_revisados_del_plan) / dias_transcurridos, 2)
        ritmo_necesario = round(oa_pendientes / dias_restantes, 2)

        tiene_alerta = ritmo_actual < ritmo_necesario
        if tiene_alerta:
            mensaje = (
                f"A este ritmo no vas a alcanzar a cubrir todo el contenido antes de la fecha objetivo — "
                f"te faltan {oa_pendientes} objetivos y quedan {dias_restantes} días."
            )
        else:
            mensaje = "Vas a buen ritmo para llegar a tu fecha objetivo con el contenido cubierto."

        return AlertaRitmoEstudio(
            tiene_alerta=tiene_alerta, mensaje=mensaje, dias_restantes=dias_restantes,
            oa_pendientes=oa_pendientes, ritmo_actual_oa_por_dia=ritmo_actual,
            ritmo_necesario_oa_por_dia=ritmo_necesario,
        )


# Mapa de calor por eje temático — idea propia (no un hallazgo de Brincus): cruza todas las
# respuestas de los intentos ya entregados del alumno contra el eje temático de la OA de cada
# pregunta (ej. en Matemática: "Números", "Álgebra", "Geometría") para mostrar en qué ejes
# específicos le va peor, más granular que "cuánto le falta por asignatura". Solo aritmética
# sobre datos que ya existen — sin IA. Cada respuesta ya registrada cuenta (si el alumno
# respondió la misma OA en más de un intento, cada intento aporta su propio dato al eje).


@dataclass(frozen=True)
class CeldaMapaCalor:
    asignatura_id: int
    asignatura_nombre: str
    eje_tematico: str
    pct_correctas: float
    total_preguntas: int


class ObtenerMapaDeCalorPorEje:
    def __init__(
        self,
        repositorio_intentos: RepositorioIntentos,
        repositorio_preguntas: RepositorioPreguntas,
        repositorio_contenido: RepositorioContenido,
    ):
        self._repositorio_intentos = repositorio_intentos
        self._repositorio_preguntas = repositorio_preguntas
        self._repositorio_contenido = repositorio_contenido

    def ejecutar(self, perfil_alumno_id: int) -> list[CeldaMapaCalor]:
        intentos = self._repositorio_intentos.listar_entregados_por_perfil(perfil_alumno_id)

        respuestas: list[tuple[int, str]] = []
        for intento in intentos:
            for pregunta_id_str, respuesta_alumno in intento.respuestas.items():
                respuestas.append((int(pregunta_id_str), respuesta_alumno))

        if not respuestas:
            return []

        pregunta_ids = list({pid for pid, _ in respuestas})
        preguntas_por_id = {p.id: p for p in self._repositorio_preguntas.listar_por_ids(pregunta_ids)}

        oa_ids = {p.oa_id for p in preguntas_por_id.values() if p.oa_id is not None}
        objetivos_por_id = {oa_id: self._repositorio_contenido.obtener_objetivo(oa_id) for oa_id in oa_ids}

        acumulado: dict[tuple[int, str], list[int]] = {}  # (asignatura_id, eje) -> [correctas, total]
        for pregunta_id, respuesta_alumno in respuestas:
            pregunta = preguntas_por_id.get(pregunta_id)
            if pregunta is None or pregunta.tipo not in TIPOS_AUTOCORREGIBLES or pregunta.oa_id is None:
                continue
            objetivo = objetivos_por_id.get(pregunta.oa_id)
            if objetivo is None or not objetivo.eje_tematico:
                continue

            clave = (objetivo.asignatura_id, objetivo.eje_tematico)
            correctas, total = acumulado.get(clave, [0, 0])
            es_correcta = respuesta_alumno.strip().lower() == pregunta.respuesta_correcta.strip().lower()
            acumulado[clave] = [correctas + (1 if es_correcta else 0), total + 1]

        asignaturas_por_id: dict[int, str] = {}
        celdas: list[CeldaMapaCalor] = []
        for (asignatura_id, eje), (correctas, total) in acumulado.items():
            if asignatura_id not in asignaturas_por_id:
                asignatura = self._repositorio_contenido.obtener_asignatura(asignatura_id)
                asignaturas_por_id[asignatura_id] = asignatura.nombre if asignatura else ""
            celdas.append(
                CeldaMapaCalor(
                    asignatura_id=asignatura_id,
                    asignatura_nombre=asignaturas_por_id[asignatura_id],
                    eje_tematico=eje,
                    pct_correctas=round(100 * correctas / total, 1),
                    total_preguntas=total,
                )
            )

        celdas.sort(key=lambda c: (c.asignatura_nombre, c.eje_tematico))
        return celdas


# Cruce sueño / horario de estudio — idea propia (no un hallazgo de Brincus): cruza la hora
# real de las sesiones de estudio (intentos entregados + guías revisadas, únicas dos fuentes
# de "actividad" con marca de tiempo que ya existen) para detectar un patrón de estudio
# tardío en la noche. Deliberadamente visible solo para el Apoderado, no para el alumno —
# es información para que un adulto decida, no una alerta directa al niño.

UMBRAL_HORA_TARDE = 21  # 21:00 hora de Chile en adelante (o después de medianoche)
UMBRAL_HORA_MADRUGADA = 5  # antes de las 5:00 también cuenta como "tarde en la noche"
UMBRAL_SESIONES_TARDE = 3  # de las últimas `VENTANA_SESIONES` sesiones
VENTANA_SESIONES = 7

# UTC-3 fijo — mismo criterio ya aceptado en el proyecto para no modelar timezone por
# alumno (ver "racha cerca de medianoche" en planificacion/28-plan-de-pruebas-exhaustivo.md):
# el servidor guarda todo en UTC, sin la hora local exacta de cada familia.
OFFSET_CHILE_HORAS = -3


def _hora_chile(momento: datetime) -> int:
    return (momento.hour + OFFSET_CHILE_HORAS) % 24


@dataclass(frozen=True)
class ObservacionHorario:
    tiene_observacion: bool
    mensaje: str
    sesiones_tarde: int
    sesiones_analizadas: int


class ObservarHorarioDeEstudio:
    def __init__(self, repositorio_intentos: RepositorioIntentos, repositorio_progreso: RepositorioProgreso):
        self._repositorio_intentos = repositorio_intentos
        self._repositorio_progreso = repositorio_progreso

    def ejecutar(self, perfil_alumno_id: int) -> ObservacionHorario | None:
        fechas: list[datetime] = [
            i.fecha_termino for i in self._repositorio_intentos.listar_entregados_por_perfil(perfil_alumno_id)
            if i.fecha_termino is not None
        ]
        fechas += [g.fecha for g in self._repositorio_progreso.listar_guias_revisadas(perfil_alumno_id)]

        if not fechas:
            return None

        fechas.sort(reverse=True)
        recientes = fechas[:VENTANA_SESIONES]
        tarde = sum(
            1 for f in recientes
            if _hora_chile(f) >= UMBRAL_HORA_TARDE or _hora_chile(f) < UMBRAL_HORA_MADRUGADA
        )

        if tarde < UMBRAL_SESIONES_TARDE:
            return ObservacionHorario(
                tiene_observacion=False, mensaje="", sesiones_tarde=tarde, sesiones_analizadas=len(recientes),
            )

        return ObservacionHorario(
            tiene_observacion=True,
            mensaje=(
                f"{tarde} de sus últimas {len(recientes)} sesiones fueron después de las 21:00 "
                "— podría estar afectando su descanso."
            ),
            sesiones_tarde=tarde,
            sesiones_analizadas=len(recientes),
        )


# "Racha de la casa" / jardín semanal — idea 3 del boceto de innovación (2026-08-17), variante
# recomendada tras evaluar los límites de la idea (ver el boceto publicado esa fecha): en vez
# de UNA planta que se marchita al perder la racha (contradice el lenguaje "todavía no" que
# ya usa toda la app — el rojo/castigo visual desmotiva), cada semana suma una plantita nueva
# al jardín acumulado. Si esa semana hubo poca actividad, esa plantita queda más chica — pero
# el jardín completo (la historia) nunca desaparece ni se marchita.

ETAPAS_JARDIN = ["semilla", "brote", "crecimiento", "floreciendo", "flor_completa"]


def _etapa_de(dias_activos: int) -> str:
    if dias_activos <= 0:
        return "semilla"
    if dias_activos <= 2:
        return "brote"
    if dias_activos <= 4:
        return "crecimiento"
    if dias_activos <= 6:
        return "floreciendo"
    return "flor_completa"


@dataclass(frozen=True)
class SemanaJardin:
    semana_inicio: date
    dias_activos: int
    etapa: str


class ObtenerJardinSemanal:
    def __init__(self, repositorio_intentos: RepositorioIntentos, repositorio_progreso: RepositorioProgreso):
        self._repositorio_intentos = repositorio_intentos
        self._repositorio_progreso = repositorio_progreso

    def ejecutar(self, perfil_alumno_id: int, hoy: date, semanas: int = 8) -> list[SemanaJardin]:
        fechas_actividad: set[date] = {
            i.fecha_termino.date() for i in self._repositorio_intentos.listar_entregados_por_perfil(perfil_alumno_id)
            if i.fecha_termino is not None
        }
        fechas_actividad |= {g.fecha.date() for g in self._repositorio_progreso.listar_guias_revisadas(perfil_alumno_id)}

        inicio_semana_actual = hoy - timedelta(days=hoy.weekday())
        resultado: list[SemanaJardin] = []
        for i in range(semanas):
            inicio = inicio_semana_actual - timedelta(weeks=(semanas - 1 - i))
            fin = min(inicio + timedelta(days=6), hoy)
            dias_activos = len({f for f in fechas_actividad if inicio <= f <= fin})
            resultado.append(SemanaJardin(semana_inicio=inicio, dias_activos=dias_activos, etapa=_etapa_de(dias_activos)))

        return resultado
