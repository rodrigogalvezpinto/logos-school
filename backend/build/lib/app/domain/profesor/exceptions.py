class ErrorDominioProfesor(Exception):
    """Base de las excepciones de negocio del contexto Profesor."""


class CorreoYaRegistrado(ErrorDominioProfesor):
    pass


class CredencialesProfesorInvalidas(ErrorDominioProfesor):
    pass


class CuentaProfesorNoEncontrada(ErrorDominioProfesor):
    pass


class ProfesorNoAprobado(ErrorDominioProfesor):
    pass
