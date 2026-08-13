class ErrorDominioComercial(Exception):
    """Base de las excepciones de negocio del contexto Comercial."""


class PlanNoEncontrado(ErrorDominioComercial):
    pass


class CodigoDescuentoNoEncontrado(ErrorDominioComercial):
    pass


class CodigoDescuentoDuplicado(ErrorDominioComercial):
    pass


class AlumnoNoEncontrado(ErrorDominioComercial):
    pass
