"""Casos de uso del contexto Evaluaciones — orquestan el agregado IntentoEvaluacion +
puertos. IniciarIntento depende también del puerto RepositorioPerfilesAlumno del
contexto Auth: un intento pertenece a un perfil de alumno real, así que verificar su
existencia es una dependencia legítima entre contextos, no una fuga de capas."""

from app.domain.auth.ports import RepositorioPerfilesAlumno
from app.domain.evaluaciones.entities import IntentoEvaluacion
from app.domain.evaluaciones.exceptions import ConjuntoNoEncontrado, IntentoNoEncontrado, PerfilAlumnoNoEncontrado
from app.domain.evaluaciones.ports import RepositorioConjuntos, RepositorioIntentos, RepositorioPreguntas
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
