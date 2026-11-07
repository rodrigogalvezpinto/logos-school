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


class AsignaturaNoEncontrada(ErrorDominioEvaluaciones):
    pass


class CoberturaInsuficiente(ErrorDominioEvaluaciones):
    """El alumno todavía no cubre el % de temario necesario para el simulacro parcial."""


class SinPreguntasDisponibles(ErrorDominioEvaluaciones):
    """Hay cobertura suficiente pero ninguna pregunta autocorregible de esas OA."""


class IntentoNoEntregado(ErrorDominioEvaluaciones):
    """El detalle por pregunta solo existe una vez entregado — antes de eso mostrar la
    respuesta correcta filtraría la solución de un intento en curso."""


class PreguntaNoEncontrada(ErrorDominioEvaluaciones):
    pass
