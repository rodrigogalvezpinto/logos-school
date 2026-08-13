from datetime import date, timedelta

import pytest

from app.domain.plan_estudio.entities import PlanDeEstudio, generar_sesiones
from app.domain.plan_estudio.exceptions import DiasInvalidos


def test_generar_sesiones_sin_pendientes_da_lista_vacia():
    assert generar_sesiones({}, ["lunes", "miercoles", "viernes"], date(2026, 1, 5), None) == []


def test_generar_sesiones_sin_dias_elegidos_da_lista_vacia():
    assert generar_sesiones({1: [10, 11]}, [], date(2026, 1, 5), None) == []


def test_generar_sesiones_con_fecha_objetivo_anterior_a_inicio_da_lista_vacia():
    assert generar_sesiones({1: [10]}, ["lunes"], date(2026, 3, 1), date(2026, 1, 1)) == []


def test_generar_sesiones_cubre_todas_las_oa_pendientes():
    pendientes = {1: [10, 11, 12], 2: [20, 21]}
    sesiones = generar_sesiones(pendientes, ["lunes", "miercoles", "viernes"], date(2026, 1, 5), date(2026, 3, 1))
    oa_cubiertas = {oa for s in sesiones for oa in s.oa_ids}
    assert oa_cubiertas == {10, 11, 12, 20, 21}


def test_generar_sesiones_alterna_asignaturas():
    # 2026-01-05 es lunes. Con 3 días/semana y suficientes fechas, la primera sesión de
    # cada asignatura debería repartirse en fechas tempranas distintas (round-robin).
    pendientes = {1: [10, 11, 12, 13], 2: [20, 21, 22, 23]}
    sesiones = generar_sesiones(pendientes, ["lunes", "miercoles", "viernes"], date(2026, 1, 5), date(2026, 3, 1))
    asignaturas_en_orden = [s.asignatura_id for s in sesiones[:4]]
    assert len(set(asignaturas_en_orden)) > 1  # no todo seguido de la misma asignatura


def test_generar_sesiones_marca_incluye_prueba_unidad_en_la_ultima_de_cada_asignatura():
    pendientes = {1: [10, 11]}
    sesiones = generar_sesiones(pendientes, ["lunes", "miercoles", "viernes"], date(2026, 1, 5), date(2026, 3, 1))
    sesiones_asignatura_1 = [s for s in sesiones if s.asignatura_id == 1]
    assert sesiones_asignatura_1[-1].incluye_prueba_unidad is True
    assert all(not s.incluye_prueba_unidad for s in sesiones_asignatura_1[:-1])


def test_generar_sesiones_no_excede_las_fechas_disponibles():
    pendientes = {1: [10, 11, 12, 13, 14, 15, 16, 17, 18, 19]}
    fecha_inicio = date(2026, 1, 5)
    fecha_objetivo = fecha_inicio + timedelta(weeks=1)  # pocas fechas disponibles
    sesiones = generar_sesiones(pendientes, ["lunes", "miercoles", "viernes"], fecha_inicio, fecha_objetivo)
    assert len(sesiones) <= 3  # solo 3 fechas caben en esa semana


def test_esta_cumplida_requiere_todas_las_oa_revisadas():
    # Solo un lunes disponible en la ventana (2026-01-05 al 2026-01-10) — fuerza a que
    # ambas OA pendientes caigan en la misma sesión.
    sesiones = generar_sesiones({1: [10, 11]}, ["lunes"], date(2026, 1, 5), date(2026, 1, 10))
    sesion = sesiones[0]
    assert sesion.oa_ids == [10, 11]
    assert not sesion.esta_cumplida(set())
    assert not sesion.esta_cumplida({sesion.oa_ids[0]})
    assert sesion.esta_cumplida(set(sesion.oa_ids))


def test_minutos_estimados_es_proporcional_a_la_cantidad_de_oa():
    sesiones = generar_sesiones({1: [10, 11]}, ["lunes"], date(2026, 1, 5), date(2026, 3, 1))
    sesion = sesiones[0]
    assert sesion.minutos_estimados() == len(sesion.oa_ids) * 25


def test_plan_de_estudio_crear_valida_dias_por_semana():
    with pytest.raises(DiasInvalidos):
        PlanDeEstudio.crear(1, 2, ["lunes", "martes"], date(2026, 1, 5), None, {})


def test_plan_de_estudio_crear_valida_cantidad_de_dias_elegidos():
    with pytest.raises(DiasInvalidos):
        PlanDeEstudio.crear(1, 3, ["lunes", "martes"], date(2026, 1, 5), None, {})


def test_plan_de_estudio_crear_valida_nombres_de_dias():
    with pytest.raises(DiasInvalidos):
        PlanDeEstudio.crear(1, 3, ["lunes", "martes", "funday"], date(2026, 1, 5), None, {})


def test_plan_de_estudio_crear_exitoso_genera_sesiones():
    plan = PlanDeEstudio.crear(
        1, 3, ["lunes", "miercoles", "viernes"], date(2026, 1, 5), date(2026, 3, 1), {1: [10, 11]}
    )
    assert plan.perfil_alumno_id == 1
    assert len(plan.sesiones) > 0
