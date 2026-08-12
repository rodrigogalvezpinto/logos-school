import pytest

from app.services.calificacion import calcular_nota


def test_cero_correctas_da_nota_minima():
    assert calcular_nota(0, 20) == 1.0


def test_exactamente_exigencia_da_nota_cuatro():
    assert calcular_nota(12, 20) == 4.0  # 60% de 20 = 12


def test_todas_correctas_da_nota_maxima():
    assert calcular_nota(20, 20) == 7.0


def test_bajo_exigencia_nota_intermedia():
    # 6 de 20 = 30% de logro, la mitad del camino a la exigencia (12) → nota 2.5
    assert calcular_nota(6, 20) == 2.5


def test_sobre_exigencia_nota_intermedia():
    # 16 de 20 = mitad del camino entre 12 (exigencia, nota 4) y 20 (nota 7) → nota 5.5
    assert calcular_nota(16, 20) == 5.5


def test_puntaje_total_cero_lanza_error():
    with pytest.raises(ValueError):
        calcular_nota(5, 0)


def test_examen_regimen_a_20_preguntas():
    # Caso real: examen integrado de 1°-4° básico, 20 preguntas.
    # 18/20 correctas: aprobación=12, nota = 4 + 3*((18-12)/(20-12)) = 6.25 → 6.2/6.3 según redondeo
    assert calcular_nota(18, 20) in (6.2, 6.3)


def test_prueba_25_preguntas_regimen_b():
    # Caso real: prueba separada 5° básico en adelante, 25 preguntas
    assert calcular_nota(15, 25) == 4.0  # 60% exacto de 25 = 15
