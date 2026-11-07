class ErrorDominioAuth(Exception):
    """Base de las excepciones de negocio del contexto Auth — los routers las traducen
    a HTTPException, nunca al revés (el dominio no conoce HTTP)."""


class CorreoYaRegistrado(ErrorDominioAuth):
    pass


class CredencialesInvalidas(ErrorDominioAuth):
    pass


class GoogleLoginNoConfigurado(ErrorDominioAuth):
    pass


class TokenGoogleInvalido(ErrorDominioAuth):
    pass


class RutYaRegistrado(ErrorDominioAuth):
    """Ya existe un PerfilAlumno con ese RUT — evita que dos Apoderados distintos (o el
    mismo, por error) registren dos veces al mismo niño/a."""


class NivelNoEncontrado(ErrorDominioAuth):
    pass
