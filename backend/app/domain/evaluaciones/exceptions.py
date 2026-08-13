class ErrorDominioEvaluaciones(Exception):
    """Base de las excepciones de negocio del contexto Evaluaciones."""


class IntentoYaEntregado(ErrorDominioEvaluaciones):
    pass


class IntentoNoEncontrado(ErrorDominioEvaluaciones):
    pass


class ConjuntoNoEncontrado(ErrorDominioEvaluaciones):
    pass


class PerfilAlumnoNoEncontrado(ErrorDominioEvaluaciones):
    pass


class ObjetivoAprendizajeNoEncontrado(ErrorDominioEvaluaciones):
    pass
