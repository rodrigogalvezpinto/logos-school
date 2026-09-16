"""Alerta temprana de ritmo de estudio — idea propia (no un hallazgo de Brincus, ver
`app/application/prediccion/consultas.py`)."""

from datetime import date, timedelta

from app.infrastructure.persistence.orm_models import Asignatura, Nivel, ObjetivoAprendizaje

_CONTADOR_EMAILS = iter(range(1, 100_000))


def _rut_valido(cuerpo: int) -> str:
    cuerpo_str = str(cuerpo)
    suma = 0
    multiplicador = 2
    for c in reversed(cuerpo_str):
        suma += int(c) * multiplicador
        multiplicador = multiplicador + 1 if multiplicador < 7 else 2
    resto = 11 - (suma % 11)
    dv = "0" if resto == 11 else "K" if resto == 10 else str(resto)
    return f"{cuerpo_str}-{dv}"


def _preparar_contenido(session):
    nivel = Nivel(
        nombre="4° básico", regimen="A", decreto="439/2012", formato_examen="integrado",
        num_preguntas_examen=20, duracion_examen_min=90,
    )
    session.add(nivel)
    session.commit()
    session.refresh(nivel)

    asignatura = Asignatura(nivel_id=nivel.id, nombre="Matemática")
    session.add(asignatura)
    session.commit()
    session.refresh(asignatura)

    for i in range(4):
        session.add(ObjetivoAprendizaje(asignatura_id=asignatura.id, codigo_oficial=f"OA {i+1}", descripcion=f"Objetivo {i+1}"))
    session.commit()

    return nivel, asignatura


def _crear_apoderado_con_alumno(client, nivel_id):
    n = next(_CONTADOR_EMAILS)
    email = f"apoderado.ritmo.{n}@test.cl"
    token = client.post(
        "/auth/registro", json={"email": email, "password": "ClaveSegura123", "nombre": "Apoderado Test"},
    ).json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    perfil_id = client.post(
        "/auth/alumnos", headers=headers,
        json={"nombre": "Test", "apellidos": "Test", "fecha_nacimiento": "2016-01-01", "rut": _rut_valido(20_000_000 + n), "nivel_id": nivel_id},
    ).json()["id"]
    return headers, perfil_id


def test_sin_plan_creado_devuelve_null(client, session):
    nivel, _ = _preparar_contenido(session)
    headers, perfil_id = _crear_apoderado_con_alumno(client, nivel.id)

    r = client.get(f"/prediccion/{perfil_id}/ritmo-de-estudio", headers=headers)
    assert r.status_code == 200
    assert r.json() is None


def test_plan_sin_fecha_objetivo_devuelve_null(client, session):
    nivel, _ = _preparar_contenido(session)
    headers, perfil_id = _crear_apoderado_con_alumno(client, nivel.id)
    client.post(
        f"/plan-estudio/{perfil_id}",
        json={"dias_por_semana": 3, "dias_elegidos": ["lunes", "miercoles", "viernes"]},
        headers=headers,
    )

    r = client.get(f"/prediccion/{perfil_id}/ritmo-de-estudio", headers=headers)
    assert r.status_code == 200
    assert r.json() is None


def test_sin_guias_revisadas_y_fecha_objetivo_cercana_hay_alerta(client, session):
    nivel, _ = _preparar_contenido(session)
    headers, perfil_id = _crear_apoderado_con_alumno(client, nivel.id)
    fecha_objetivo = (date.today() + timedelta(days=5)).isoformat()
    client.post(
        f"/plan-estudio/{perfil_id}",
        json={"dias_por_semana": 3, "dias_elegidos": ["lunes", "miercoles", "viernes"], "fecha_objetivo": fecha_objetivo},
        headers=headers,
    )

    r = client.get(f"/prediccion/{perfil_id}/ritmo-de-estudio", headers=headers)
    assert r.status_code == 200
    datos = r.json()
    assert datos["tiene_alerta"] is True
    assert datos["oa_pendientes"] > 0
    # 4 o 5 según si el reloj del servidor (UTC) cruza medianoche respecto al `date.today()`
    # local de este test — mismo caso borde ya documentado en
    # planificacion/28-plan-de-pruebas-exhaustivo.md ("racha cerca de medianoche").
    assert datos["dias_restantes"] in (4, 5)
    assert datos["ritmo_actual_oa_por_dia"] == 0.0


def test_revisar_todo_el_contenido_del_plan_quita_la_alerta(client, session):
    nivel, asignatura = _preparar_contenido(session)
    headers, perfil_id = _crear_apoderado_con_alumno(client, nivel.id)
    fecha_objetivo = (date.today() + timedelta(days=30)).isoformat()
    plan = client.post(
        f"/plan-estudio/{perfil_id}",
        json={"dias_por_semana": 3, "dias_elegidos": ["lunes", "miercoles", "viernes"], "fecha_objetivo": fecha_objetivo},
        headers=headers,
    ).json()

    oa_ids_del_plan = {oa_id for s in plan["sesiones"] for oa_id in s["oa_ids"]}
    for oa_id in oa_ids_del_plan:
        client.post(f"/progreso/{perfil_id}/guias/{oa_id}/revisada", headers=headers)

    r = client.get(f"/prediccion/{perfil_id}/ritmo-de-estudio", headers=headers)
    datos = r.json()
    assert datos["tiene_alerta"] is False
    assert datos["oa_pendientes"] == 0


def test_ritmo_de_alumno_ajeno_da_403(client, session):
    nivel, _ = _preparar_contenido(session)
    _, perfil_id = _crear_apoderado_con_alumno(client, nivel.id)
    headers_b, _ = _crear_apoderado_con_alumno(client, nivel.id)

    r = client.get(f"/prediccion/{perfil_id}/ritmo-de-estudio", headers=headers_b)
    assert r.status_code == 403


def test_ritmo_sin_sesion_da_401(client, session):
    nivel, _ = _preparar_contenido(session)
    _, perfil_id = _crear_apoderado_con_alumno(client, nivel.id)

    r = client.get(f"/prediccion/{perfil_id}/ritmo-de-estudio")
    assert r.status_code == 401
