"""Logros (racha de días, contadores de hábito) — profundización de la gamificación
2026-08-15 comparando en vivo contra la cuenta real de Brincus (ver
planificacion/25-analisis-competencia-brincus.md). Tests de dominio puro, sin backend/DB:
más rápidos y más fáciles de razonar para la lógica de fechas de la racha."""

from datetime import date

from app.domain.gamificacion.entities import CATALOGO_LOGROS, PerfilGamificacion


def _perfil() -> PerfilGamificacion:
    return PerfilGamificacion.crear(perfil_alumno_id=1)


def test_primera_actividad_deja_la_racha_en_1():
    perfil = _perfil()
    perfil.registrar_actividad(date(2026, 8, 10))
    assert perfil.racha_dias_actual == 1
    assert perfil.racha_dias_maxima == 1


def test_actividad_el_dia_siguiente_suma_la_racha():
    perfil = _perfil()
    perfil.registrar_actividad(date(2026, 8, 10))
    perfil.registrar_actividad(date(2026, 8, 11))
    perfil.registrar_actividad(date(2026, 8, 12))
    assert perfil.racha_dias_actual == 3
    assert perfil.racha_dias_maxima == 3


def test_dos_actividades_el_mismo_dia_no_inflan_la_racha():
    """Bug real que se evita a propósito: sin esto, entregar 3 pruebas el mismo día
    contaría como 3 días de racha."""
    perfil = _perfil()
    perfil.registrar_actividad(date(2026, 8, 10))
    perfil.registrar_actividad(date(2026, 8, 10))
    perfil.registrar_actividad(date(2026, 8, 10))
    assert perfil.racha_dias_actual == 1


def test_saltarse_un_dia_corta_la_racha_pero_conserva_la_maxima():
    perfil = _perfil()
    perfil.registrar_actividad(date(2026, 8, 10))
    perfil.registrar_actividad(date(2026, 8, 11))
    perfil.registrar_actividad(date(2026, 8, 12))  # racha de 3
    perfil.registrar_actividad(date(2026, 8, 20))  # salto — se corta
    assert perfil.racha_dias_actual == 1
    assert perfil.racha_dias_maxima == 3


def test_logro_de_racha_se_desbloquea_con_la_maxima_no_la_actual():
    perfil = _perfil()
    for dia in range(10, 15):  # 5 días seguidos
        perfil.registrar_actividad(date(2026, 8, dia))
    perfil.registrar_actividad(date(2026, 8, 25))  # se corta la racha actual

    desbloqueados = perfil.logros_desbloqueados()
    assert "racha_2" in desbloqueados
    assert "racha_5" in desbloqueados
    assert "racha_10" not in desbloqueados


def test_logros_de_contenido_y_evaluaciones_por_contador():
    perfil = _perfil()
    for _ in range(5):
        perfil.incrementar_guias_revisadas()
    perfil.incrementar_evaluaciones_entregadas()

    desbloqueados = perfil.logros_desbloqueados()
    assert "guias_5" in desbloqueados
    assert "guias_15" not in desbloqueados
    assert "evals_1" in desbloqueados
    assert "evals_5" not in desbloqueados


def test_logro_de_nivel_usa_el_nivel_derivado_del_xp():
    perfil = _perfil()
    perfil.sumar_xp(500)  # nivel 5 (umbral acumulado 25*4*5=500, curva no lineal)
    desbloqueados = perfil.logros_desbloqueados()
    assert "nivel_5" in desbloqueados
    assert "nivel_10" not in desbloqueados


def test_curva_de_niveles_no_lineal():
    """Nivel 2 = 50 XP, nivel 3 = 150 XP, nivel 5 = 500 XP — creciente, no un múltiplo fijo
    (hallazgo comparando en vivo contra Brincus, Paso 12 — ver
    planificacion/27-plan-incorporacion-hallazgos-brincus.md)."""
    assert _perfil().nivel == 1
    p = _perfil()
    p.sumar_xp(49)
    assert p.nivel == 1
    p2 = _perfil()
    p2.sumar_xp(50)
    assert p2.nivel == 2
    p3 = _perfil()
    p3.sumar_xp(150)
    assert p3.nivel == 3
    p3.sumar_xp(1)
    assert p3.nivel == 3  # todavía no alcanza el umbral del nivel 4 (300)


def test_catalogo_de_logros_no_tiene_ids_duplicados():
    ids = [logro.id for logro in CATALOGO_LOGROS]
    assert len(ids) == len(set(ids))


def test_logro_de_tiempo_evaluando_se_desbloquea_por_umbral_acumulado():
    """Hallazgo comparando en vivo contra Brincus, Paso 12 (logros por "sesión más larga" /
    "tiempo total acumulado"). Se mide con tiempo real de evaluaciones entregadas, sumado
    a través de múltiples intentos — no de una sola vez."""
    perfil = _perfil()
    perfil.sumar_tiempo_evaluando(20 * 60)
    perfil.sumar_tiempo_evaluando(15 * 60)  # total: 35 min

    desbloqueados = perfil.logros_desbloqueados()
    assert "tiempo_30min" in desbloqueados
    assert "tiempo_2h" not in desbloqueados


def test_sumar_tiempo_evaluando_ignora_valores_no_positivos():
    perfil = _perfil()
    perfil.sumar_tiempo_evaluando(0)
    perfil.sumar_tiempo_evaluando(-100)
    assert perfil.tiempo_evaluando_total_seg == 0
