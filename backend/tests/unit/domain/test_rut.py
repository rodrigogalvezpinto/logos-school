import pytest

from app.domain.auth.value_objects import Rut


def test_rut_valido_no_lanza():
    Rut("21.345.678-4")


def test_rut_valido_sin_puntos_ni_guion():
    Rut("213456784")


def test_rut_con_digito_verificador_incorrecto_lanza():
    with pytest.raises(ValueError):
        Rut("21.345.678-9")


def test_rut_demasiado_corto_lanza():
    with pytest.raises(ValueError):
        Rut("1")


def test_str_devuelve_el_valor_original():
    assert str(Rut("21.345.678-4")) == "21.345.678-4"
