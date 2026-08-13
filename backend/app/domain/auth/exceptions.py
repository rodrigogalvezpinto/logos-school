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
