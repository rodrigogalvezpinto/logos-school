"""Casos de uso del contexto Evaluaciones — orquestan el agregado IntentoEvaluacion +
puertos. IniciarIntento depende también del puerto RepositorioPerfilesAlumno del
contexto Auth: un intento pertenece a un perfil de alumno real, así que verificar su
existencia es una dependencia legítima entre contextos, no una fuga de capas."""

from app.domain.auth.ports import RepositorioPerfilesAlumno
from app.domain.contenido.ports import RepositorioContenido
from app.domain.evaluaciones.entities import IntentoEvaluacion
from app.domain.evaluaciones.exceptions import (
    AsignaturaNoEncontrada,
    ConjuntoNoEncontrado,
    CoberturaInsuficiente,
    IntentoNoEncontrado,
    IntentoNoEntregado,
    PerfilAlumnoNoEncontrado,
    SinPreguntasDisponibles,
)
from app.domain.evaluaciones.ports import (
    ConjuntoLectura,
    DetallePregunta,
    RepositorioConjuntos,
    RepositorioIntentos,
    RepositorioPreguntas,
)
from app.domain.evaluaciones.value_objects import (
    MAX_PREGUNTAS_SIMULACRO_PARCIAL,
    TIPOS_AUTOCORREGIBLES,
    UMBRAL_SIMULACRO_PARCIAL,
)
from app.domain.progreso.ports import RepositorioProgreso
from app.domain.shared.reloj import Reloj


class IniciarIntento:
    def __init__(
        self,
        repositorio_intentos: RepositorioIntentos,
        repositorio_conjuntos: RepositorioConjuntos,
        repositorio_perfiles: RepositorioPerfilesAlumno,
        reloj: Reloj,
    ):
        self._repositorio_intentos = repositorio_intentos
        self._repositorio_conjuntos = repositorio_conjuntos
        self._repositorio_perfiles = repositorio_perfiles
        self._reloj = reloj

    def ejecutar(self, perfil_alumno_id: int, conjunto_evaluacion_id: int) -> IntentoEvaluacion:
        if not self._repositorio_perfiles.buscar_por_id(perfil_alumno_id):
            raise PerfilAlumnoNoEncontrado()
        if not self._repositorio_conjuntos.buscar_por_id(conjunto_evaluacion_id):
            raise ConjuntoNoEncontrado()

        # Caso borde: si ya hay un intento sin terminar para este alumno+conjunto, se
        # reanuda en vez de crear uno nuevo (ver planificacion/20-seguridad-y-casos-borde.md,
        # "abandono y reingreso" y "misma evaluación en dos pestañas").
        existente = self._repositorio_intentos.buscar_activo(perfil_alumno_id, conjunto_evaluacion_id)
        if existente:
            return existente

        intento = IntentoEvaluacion.iniciar(perfil_alumno_id, conjunto_evaluacion_id, self._reloj)
        return self._repositorio_intentos.guardar(intento)


class ObtenerIntento:
    def __init__(self, repositorio_intentos: RepositorioIntentos):
        self._repositorio_intentos = repositorio_intentos

    def ejecutar(self, intento_id: int) -> IntentoEvaluacion:
        intento = self._repositorio_intentos.buscar_por_id(intento_id)
        if not intento:
            raise IntentoNoEncontrado()
        return intento


class ResponderPregunta:
    def __init__(self, repositorio_intentos: RepositorioIntentos):
        self._repositorio_intentos = repositorio_intentos

    def ejecutar(self, intento_id: int, pregunta_id: int, respuesta: str) -> IntentoEvaluacion:
        intento = self._repositorio_intentos.buscar_por_id(intento_id)
        if not intento:
            raise IntentoNoEncontrado()
        intento.responder(pregunta_id, respuesta)  # lanza IntentoYaEntregado si corresponde
        return self._repositorio_intentos.guardar(intento)


class EntregarIntento:
    def __init__(
        self,
        repositorio_intentos: RepositorioIntentos,
        repositorio_conjuntos: RepositorioConjuntos,
        repositorio_preguntas: RepositorioPreguntas,
        reloj: Reloj,
    ):
        self._repositorio_intentos = repositorio_intentos
        self._repositorio_conjuntos = repositorio_conjuntos
        self._repositorio_preguntas = repositorio_preguntas
        self._reloj = reloj

    def ejecutar(self, intento_id: int) -> IntentoEvaluacion:
        intento = self._repositorio_intentos.buscar_por_id(intento_id)
        if not intento:
            raise IntentoNoEncontrado()
        if intento.esta_entregado:
            return intento  # idempotente — no vuelve a consultar preguntas ni recalcula

        conjunto = self._repositorio_conjuntos.buscar_por_id(intento.conjunto_evaluacion_id)
        preguntas = self._repositorio_preguntas.listar_para_correccion(conjunto.pregunta_ids)
        intento.entregar(preguntas, self._reloj)
        return self._repositorio_intentos.guardar(intento)


class ObtenerDetalleIntento:
    """Arma el desglose pregunta-por-pregunta de un intento ya entregado (Fase 1, ítem
    2.1 del plan de incorporación de hallazgos de Brincus — resumen final con detalle por
    pregunta, en vez de solo la nota agregada que ya calculaba `entregar()`). No toca el
    agregado `IntentoEvaluacion`: es una consulta de solo lectura que compara
    `intento.respuestas` contra el enunciado/respuesta_correcta real de cada pregunta."""

    def __init__(
        self,
        repositorio_intentos: RepositorioIntentos,
        repositorio_conjuntos: RepositorioConjuntos,
        repositorio_preguntas: RepositorioPreguntas,
    ):
        self._repositorio_intentos = repositorio_intentos
        self._repositorio_conjuntos = repositorio_conjuntos
        self._repositorio_preguntas = repositorio_preguntas

    def ejecutar(self, intento_id: int) -> list[DetallePregunta]:
        intento = self._repositorio_intentos.buscar_por_id(intento_id)
        if not intento:
            raise IntentoNoEncontrado()
        if not intento.esta_entregado:
            raise IntentoNoEntregado()

        conjunto = self._repositorio_conjuntos.buscar_por_id(intento.conjunto_evaluacion_id)
        preguntas = self._repositorio_preguntas.listar_por_ids(conjunto.pregunta_ids)

        detalle: list[DetallePregunta] = []
        for p in preguntas:
            respuesta_alumno = intento.respuestas.get(str(p.id))
            es_autocorregible = p.tipo in TIPOS_AUTOCORREGIBLES
            es_correcta = None
            if es_autocorregible:
                es_correcta = bool(
                    respuesta_alumno and respuesta_alumno.strip().lower() == p.respuesta_correcta.strip().lower()
                )
            detalle.append(
                DetallePregunta(
                    pregunta_id=p.id,
                    enunciado=p.enunciado,
                    tipo=p.tipo,
                    opciones=p.opciones,
                    respuesta_alumno=respuesta_alumno,
                    respuesta_correcta=p.respuesta_correcta if es_autocorregible else None,
                    es_correcta=es_correcta,
                )
            )
        return detalle


class ProgramarFechaSimulacro:
    """Uso exclusivo del Admin (Fase 1, ítem 2.1 — simulacro con fecha programada, ver
    planificacion/27-plan-incorporacion-hallazgos-brincus.md). No pertenece a un rol
    Profesor todavía (ese plan sigue aparte) — el Admin programa la fecha desde su panel
    ya existente, igual que ya administra Planes/Descuentos/Cortesías."""

    def __init__(self, repositorio_conjuntos: RepositorioConjuntos):
        self._repositorio_conjuntos = repositorio_conjuntos

    def ejecutar(self, conjunto_id: int, fecha_programada) -> ConjuntoLectura:
        if not self._repositorio_conjuntos.buscar_por_id(conjunto_id):
            raise ConjuntoNoEncontrado()
        return self._repositorio_conjuntos.programar_fecha(conjunto_id, fecha_programada)


class GenerarSimulacroParcial:
    """Genera on-demand un `ConjuntoEvaluacion` real (tipo `examen_simulacro_parcial`)
    acotado a las OA que el alumno ya cubrió — ver planificacion/13-plan-de-estudio.md,
    sección "Requisitos adicionales". A partir de ahí sigue el ciclo normal de
    IniciarIntento/EntregarIntento sin ningún cambio, es la misma IntentoEvaluacion de
    siempre."""

    def __init__(
        self,
        repositorio_conjuntos: RepositorioConjuntos,
        repositorio_preguntas: RepositorioPreguntas,
        repositorio_contenido: RepositorioContenido,
        repositorio_progreso: RepositorioProgreso,
    ):
        self._repositorio_conjuntos = repositorio_conjuntos
        self._repositorio_preguntas = repositorio_preguntas
        self._repositorio_contenido = repositorio_contenido
        self._repositorio_progreso = repositorio_progreso

    def ejecutar(self, asignatura_id: int, perfil_alumno_id: int) -> ConjuntoLectura:
        asignatura = self._repositorio_contenido.obtener_asignatura(asignatura_id)
        if not asignatura:
            raise AsignaturaNoEncontrada()

        objetivos = self._repositorio_contenido.listar_objetivos(asignatura_id)
        if not objetivos:
            raise SinPreguntasDisponibles()

        oa_ids_asignatura = {oa.id for oa in objetivos}
        revisadas = {g.oa_id for g in self._repositorio_progreso.listar_guias_revisadas(perfil_alumno_id)}
        cubiertas = oa_ids_asignatura & revisadas
        cobertura = len(cubiertas) / len(oa_ids_asignatura)
        if cobertura < UMBRAL_SIMULACRO_PARCIAL:
            raise CoberturaInsuficiente()

        pregunta_ids: list[int] = []
        for oa_id in cubiertas:
            for p in self._repositorio_preguntas.buscar_por_oa(oa_id):
                if p.tipo in TIPOS_AUTOCORREGIBLES:
                    pregunta_ids.append(p.id)
        pregunta_ids = pregunta_ids[:MAX_PREGUNTAS_SIMULACRO_PARCIAL]
        if not pregunta_ids:
            raise SinPreguntasDisponibles()

        nombre = f"Simulacro parcial — {asignatura.nombre} ({round(cobertura * 100)}% del temario)"
        return self._repositorio_conjuntos.crear(
            tipo="examen_simulacro_parcial",
            nombre=nombre,
            forma=None,
            asignatura_id=asignatura_id,
            nivel_id=None,
            pregunta_ids=pregunta_ids,
            tiempo_sugerido_min=len(pregunta_ids) * 2,
        )
