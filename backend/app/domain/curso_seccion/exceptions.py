class ErrorDominioCursoSeccion(Exception):
    """Base de las excepciones de negocio del contexto Curso/Sección."""


class CursoSeccionNoEncontrado(ErrorDominioCursoSeccion):
    pass


class AlumnoNoEncontrado(ErrorDominioCursoSeccion):
    pass


class CursoAjeno(ErrorDominioCursoSeccion):
    """El profesor autenticado no es dueño de este curso."""
