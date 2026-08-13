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
    PerfilAlumnoNoEncontrado,
    SinPreguntasDisponibles,
)
from app.domain.evaluaciones.ports import ConjuntoLectura, RepositorioConjuntos, RepositorioIntentos, RepositorioPreguntas
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
