"""Validación de RUT chileno (módulo 11) — ver planificacion/22-analisis-de-brechas.md,
punto 9: antes no se validaba en absoluto."""

import re


def limpiar_rut(rut: str) -> str:
    return re.sub(r"[.\-\s]", "", rut).upper()


def calcular_digito_verificador(cuerpo: str) -> str:
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


def validar_rut(rut: str) -> bool:
    limpio = limpiar_rut(rut)
    if len(limpio) < 2 or not limpio[:-1].isdigit():
        return False
    cuerpo, dv = limpio[:-1], limpio[-1]
    return calcular_digito_verificador(cuerpo) == dv
