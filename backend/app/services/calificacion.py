"""Cálculo de nota — fórmula chilena estándar, exigencia 60%.

Ver planificacion/12-motor-de-evaluacion.md para la especificación completa.
"""


def calcular_nota(puntaje_obtenido: float, puntaje_total: float, exigencia: float = 0.6) -> float:
    """Devuelve la nota en escala 1.0-7.0 según la fórmula chilena de exigencia.

    - 0% de logro → nota 1.0
    - `exigencia` de logro (60% por defecto) → nota 4.0 (aprobación)
    - 100% de logro → nota 7.0
    """
    if puntaje_total <= 0:
        raise ValueError("puntaje_total debe ser mayor que 0")
    if not (0 < exigencia < 1):
        raise ValueError("exigencia debe estar entre 0 y 1 (excluyentes)")

    puntaje_aprobacion = puntaje_total * exigencia

    if puntaje_obtenido <= puntaje_aprobacion:
        nota = 1.0 + 3.0 * (puntaje_obtenido / puntaje_aprobacion)
    else:
        nota = 4.0 + 3.0 * (
            (puntaje_obtenido - puntaje_aprobacion) / (puntaje_total - puntaje_aprobacion)
        )

    nota = max(1.0, min(7.0, nota))
    return round(nota, 1)
