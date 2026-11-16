from datetime import date, datetime, timezone

from app.domain.shared.fechas import fecha_local


def test_domingo_en_la_noche_en_chile_sigue_siendo_domingo():
    # 2026-11-16 02:00 UTC es domingo 15 a las 23:00 en Chile (horario de verano, UTC−3).
    assert fecha_local(datetime(2026, 11, 16, 2, 0, tzinfo=timezone.utc)) == date(2026, 11, 15)


def test_hora_sin_zona_se_interpreta_como_utc():
    assert fecha_local(datetime(2026, 7, 1, 3, 30)) == date(2026, 6, 30)  # invierno, UTC−4


def test_mediodia_no_cambia_la_fecha():
    assert fecha_local(datetime(2026, 11, 15, 15, 0, tzinfo=timezone.utc)) == date(2026, 11, 15)
