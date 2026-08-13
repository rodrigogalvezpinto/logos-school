class ErrorDominioPlanEstudio(Exception):
    """Base de las excepciones de negocio del contexto Plan de Estudio."""


class DiasInvalidos(ErrorDominioPlanEstudio):
    pass


class PlanDeEstudioNoEncontrado(ErrorDominioPlanEstudio):
    pass


class PerfilAlumnoNoEncontrado(ErrorDominioPlanEstudio):
    pass
