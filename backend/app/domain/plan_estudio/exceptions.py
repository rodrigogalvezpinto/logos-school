class ErrorDominioPlanEstudio(Exception):
    """Base de las excepciones de negocio del contexto Plan de Estudio."""


class DiasInvalidos(ErrorDominioPlanEstudio):
    pass


class PlanDeEstudioNoEncontrado(ErrorDominioPlanEstudio):
    pass


class PerfilAlumnoNoEncontrado(ErrorDominioPlanEstudio):
    pass


class AsignaturaNoEncontrada(ErrorDominioPlanEstudio):
    pass


class NivelNoEsAnterior(ErrorDominioPlanEstudio):
    """El repaso solo tiene sentido para contenido de un nivel YA CURSADO — evita que el
    alumno agregue "repaso" de su propio nivel actual o de uno futuro, que no es repaso,
    es simplemente el plan normal."""
