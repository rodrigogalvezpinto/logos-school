from app.domain.evaluaciones.value_objects import mezclar_orden_al_azar, mezclar_orden_estable


def test_mezclar_orden_estable_misma_semilla_da_mismo_orden():
    items = list(range(20))
    assert mezclar_orden_estable(items, semilla=42) == mezclar_orden_estable(items, semilla=42)


def test_mezclar_orden_estable_semillas_distintas_dan_ordenes_distintos():
    items = list(range(20))
    assert mezclar_orden_estable(items, semilla=1) != mezclar_orden_estable(items, semilla=2)


def test_mezclar_orden_estable_no_muta_la_lista_original():
    items = [1, 2, 3, 4, 5]
    original = list(items)
    mezclar_orden_estable(items, semilla=7)
    assert items == original


def test_mezclar_orden_estable_conserva_los_mismos_elementos():
    items = list(range(15))
    assert sorted(mezclar_orden_estable(items, semilla=99)) == items


def test_mezclar_orden_al_azar_conserva_los_mismos_elementos():
    items = list(range(15))
    assert sorted(mezclar_orden_al_azar(items)) == items


def test_mezclar_orden_al_azar_no_muta_la_lista_original():
    items = [1, 2, 3, 4, 5]
    original = list(items)
    mezclar_orden_al_azar(items)
    assert items == original
