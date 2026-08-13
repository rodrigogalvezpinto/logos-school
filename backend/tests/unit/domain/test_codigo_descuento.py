from datetime import date

from app.domain.comercial.entities import CodigoDescuento


def test_sin_vencimiento_ni_limite_de_usos_siempre_vigente():
    d = CodigoDescuento.crear("SIEMPRE", "porcentaje", 10)
    assert d.vigente(date(2030, 1, 1))


def test_vencido_no_esta_vigente():
    d = CodigoDescuento.crear("VENCE", "porcentaje", 10, fecha_vencimiento=date(2026, 1, 1))
    assert not d.vigente(date(2026, 1, 1))  # el día del vencimiento ya no es válido
    assert d.vigente(date(2025, 12, 31))


def test_usos_agotados_no_esta_vigente():
    d = CodigoDescuento.crear("LIMITADO", "monto_fijo", 5000, usos_maximos=2)
    d.usos_actuales = 2
    assert not d.vigente(date(2026, 1, 1))


def test_usos_bajo_el_limite_esta_vigente():
    d = CodigoDescuento.crear("LIMITADO", "monto_fijo", 5000, usos_maximos=2)
    d.usos_actuales = 1
    assert d.vigente(date(2026, 1, 1))


def test_desactivar_lo_deja_no_vigente_de_inmediato():
    d = CodigoDescuento.crear("ACTIVO", "porcentaje", 10)
    hoy = date(2026, 8, 13)
    assert d.vigente(hoy)
    d.desactivar(hoy)
    assert not d.vigente(hoy)
