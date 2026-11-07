class ErrorDominioCursoSeccion(Exception):
    """Base de las excepciones de negocio del contexto Curso/Sección."""


class CursoSeccionNoEncontrado(ErrorDominioCursoSeccion):
    pass


class AlumnoNoEncontrado(ErrorDominioCursoSeccion):
    pass


class CursoAjeno(ErrorDominioCursoSeccion):
    """El profesor autenticado no es dueño de este curso."""


class NivelIncompatible(ErrorDominioCursoSeccion):
    """El alumno cursa un nivel distinto al del Curso/Sección — no se puede agregar."""
