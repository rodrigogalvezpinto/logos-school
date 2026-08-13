"""Value Object: RUT chileno (módulo 11). Inmutable y se valida a sí mismo en la
construcción — un Rut nunca existe en un estado inválido, a diferencia de la validación
suelta anterior en app/core/rut.py."""

import re
from dataclasses import dataclass


def _limpiar(rut: str) -> str:
    return re.sub(r"[.\-\s]", "", rut).upper()


def _digito_verificador(cuerpo: str) -> str:
    suma = 0
    multiplicador = 2
    for digito in reversed(cuerpo):
        suma += int(digito) * multiplicador
        multiplicador = multiplicador + 1 if multiplicador < 7 else 2
    resto = 11 - (suma % 11)
    if resto == 11:
        return "0"
    if resto == 10:
        return "K"
    return str(resto)


@dataclass(frozen=True)
class Rut:
    valor: str

    def __post_init__(self) -> None:
        limpio = _limpiar(self.valor)
        if len(limpio) < 2 or not limpio[:-1].isdigit():
            raise ValueError("RUT inválido — revisa el número y el dígito verificador")
        cuerpo, digito_verificador = limpio[:-1], limpio[-1]
        if _digito_verificador(cuerpo) != digito_verificador:
            raise ValueError("RUT inválido — revisa el número y el dígito verificador")

    def __str__(self) -> str:
        return self.valor
