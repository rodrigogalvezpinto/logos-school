from datetime import date, timedelta

from app.infrastructure.persistence.orm_models import Asignatura, Nivel, ObjetivoAprendizaje, SesionEstudio


def _preparar_contenido(session):
    nivel = Nivel(
        nombre="4° básico", regimen="A", decreto="439/2012", formato_examen="integrado",
        num_preguntas_examen=20, duracion_examen_min=90, orden=4,
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


def _crear_apoderado_con_alumno(client, nivel_id, email="familia.plan@test.cl", rut="21.345.678-4"):
    token = client.post(
        "/auth/registro", json={"email": email, "password": "ClaveSegura123", "nombre": "Apoderado Test"}
    ).json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    r = client.post(
        "/auth/alumnos", headers=headers,
        json={"nombre": "Sofía", "apellidos": "Pérez", "fecha_nacimiento": "2016-03-12", "rut": rut, "nivel_id": nivel_id},
    )
    return headers, r.json()["id"]


def test_crear_plan_de_estudio_genera_sesiones(client, session):
    nivel, asignatura = _preparar_contenido(session)
    headers, perfil_id = _crear_apoderado_con_alumno(client, nivel.id)

    r = client.post(
        f"/plan-estudio/{perfil_id}",
        json={"dias_por_semana": 3, "dias_elegidos": ["lunes", "miercoles", "viernes"]},
        headers=headers,
    )
    assert r.status_code == 201
    datos = r.json()
    assert datos["dias_por_semana"] == 3
    assert len(datos["sesiones"]) > 0
    assert all(not s["cumplida"] for s in datos["sesiones"])


def test_dias_invalidos_da_422(client, session):
    nivel, asignatura = _preparar_contenido(session)
    headers, perfil_id = _crear_apoderado_con_alumno(client, nivel.id)

    r = client.post(
        f"/plan-estudio/{perfil_id}",
        json={"dias_por_semana": 3, "dias_elegidos": ["lunes", "martes"]},  # no calza con dias_por_semana
        headers=headers,
    )
    assert r.status_code == 422


def test_obtener_plan_sin_plan_creado_da_404(client, session):
    nivel, asignatura = _preparar_contenido(session)
    headers, perfil_id = _crear_apoderado_con_alumno(client, nivel.id)

    r = client.get(f"/plan-estudio/{perfil_id}", headers=headers)
    assert r.status_code == 404


def test_obtener_plan_activo_marca_sesiones_cumplidas_segun_guias_revisadas(client, session):
    nivel, asignatura = _preparar_contenido(session)
    headers, perfil_id = _crear_apoderado_con_alumno(client, nivel.id)

    client.post(
        f"/plan-estudio/{perfil_id}",
        json={"dias_por_semana": 3, "dias_elegidos": ["lunes", "miercoles", "viernes"]},
        headers=headers,
    )
    plan = client.get(f"/plan-estudio/{perfil_id}", headers=headers).json()
    primera_sesion = plan["sesiones"][0]

    for oa_id in primera_sesion["oa_ids"]:
        client.post(f"/progreso/{perfil_id}/guias/{oa_id}/revisada", headers=headers)

    plan_actualizado = client.get(f"/plan-estudio/{perfil_id}", headers=headers).json()
    sesion_actualizada = next(s for s in plan_actualizado["sesiones"] if s["id"] == primera_sesion["id"])
    assert sesion_actualizada["cumplida"] is True


def test_crear_plan_reemplaza_el_anterior(client, session):
    nivel, asignatura = _preparar_contenido(session)
    headers, perfil_id = _crear_apoderado_con_alumno(client, nivel.id)

    client.post(
        f"/plan-estudio/{perfil_id}",
        json={"dias_por_semana": 3, "dias_elegidos": ["lunes", "miercoles", "viernes"]},
        headers=headers,
    )
    r = client.post(
        f"/plan-estudio/{perfil_id}",
        json={"dias_por_semana": 4, "dias_elegidos": ["lunes", "martes", "jueves", "viernes"]},
        headers=headers,
    )
    assert r.status_code == 201
    assert r.json()["dias_por_semana"] == 4

    plan = client.get(f"/plan-estudio/{perfil_id}", headers=headers).json()
    assert plan["dias_por_semana"] == 4


def test_un_apoderado_no_puede_crear_plan_para_un_perfil_ajeno(client, session):
    nivel, asignatura = _preparar_contenido(session)
    _, perfil_id_de_a = _crear_apoderado_con_alumno(client, nivel.id, email="a@test.cl")
    headers_b, _ = _crear_apoderado_con_alumno(client, nivel.id, email="b@test.cl", rut="22.222.222-2")

    r = client.post(
        f"/plan-estudio/{perfil_id_de_a}",
        json={"dias_por_semana": 3, "dias_elegidos": ["lunes", "miercoles", "viernes"]},
        headers=headers_b,
    )
    assert r.status_code == 403


def _preparar_nivel_anterior_y_actual(session):
    """3° básico se crea primero (id menor) y 4° básico después (id mayor) — mismo
    supuesto de orden creciente que usa el caso de uso (ver CURSOS en
    importar_contenido.py: los niveles se importan de 1° básico a 4° medio, en orden)."""
    nivel_anterior = Nivel(
        nombre="3° básico", regimen="A", decreto="439/2012", formato_examen="integrado",
        num_preguntas_examen=20, duracion_examen_min=90, orden=3,
    )
    session.add(nivel_anterior)
    session.commit()
    session.refresh(nivel_anterior)
    asignatura_anterior = Asignatura(nivel_id=nivel_anterior.id, nombre="Matemática")
    session.add(asignatura_anterior)
    session.commit()
    session.refresh(asignatura_anterior)
    oa_anterior = ObjetivoAprendizaje(asignatura_id=asignatura_anterior.id, codigo_oficial="OA 1", descripcion="Repaso")
    session.add(oa_anterior)
    session.commit()
    session.refresh(oa_anterior)

    nivel_actual, _ = _preparar_contenido(session)
    return nivel_anterior, asignatura_anterior, oa_anterior, nivel_actual


def test_agregar_repaso_de_nivel_anterior_se_agenda_al_final_del_plan(client, session):
    nivel_anterior, asignatura_anterior, oa_anterior, nivel_actual = _preparar_nivel_anterior_y_actual(session)
    headers, perfil_id = _crear_apoderado_con_alumno(client, nivel_actual.id)
    client.post(
        f"/plan-estudio/{perfil_id}",
        json={"dias_por_semana": 3, "dias_elegidos": ["lunes", "miercoles", "viernes"]},
        headers=headers,
    )
    plan_antes = client.get(f"/plan-estudio/{perfil_id}", headers=headers).json()
    ultima_fecha_antes = max(s["fecha_programada"] for s in plan_antes["sesiones"])

    r = client.post(
        f"/plan-estudio/{perfil_id}/repaso",
        json={"asignatura_id": asignatura_anterior.id, "oa_ids": [oa_anterior.id]},
        headers=headers,
    )
    assert r.status_code == 201
    sesion = r.json()
    assert sesion["es_repaso"] is True
    assert sesion["asignatura_id"] == asignatura_anterior.id
    assert sesion["fecha_programada"] > ultima_fecha_antes

    plan_despues = client.get(f"/plan-estudio/{perfil_id}", headers=headers).json()
    # Se agrega al plan existente, no lo reemplaza — todas las sesiones originales siguen.
    assert len(plan_despues["sesiones"]) == len(plan_antes["sesiones"]) + 1
    assert any(s["es_repaso"] for s in plan_despues["sesiones"])


def test_agregar_repaso_del_propio_nivel_da_422(client, session):
    nivel, asignatura = _preparar_contenido(session)
    headers, perfil_id = _crear_apoderado_con_alumno(client, nivel.id)
    client.post(
        f"/plan-estudio/{perfil_id}",
        json={"dias_por_semana": 3, "dias_elegidos": ["lunes", "miercoles", "viernes"]},
        headers=headers,
    )
    oa_id = client.get(f"/plan-estudio/{perfil_id}", headers=headers).json()["sesiones"][0]["oa_ids"][0]

    r = client.post(
        f"/plan-estudio/{perfil_id}/repaso",
        json={"asignatura_id": asignatura.id, "oa_ids": [oa_id]},
        headers=headers,
    )
    assert r.status_code == 422


def test_agregar_repaso_sin_plan_creado_da_404(client, session):
    nivel_anterior, asignatura_anterior, oa_anterior, nivel_actual = _preparar_nivel_anterior_y_actual(session)
    headers, perfil_id = _crear_apoderado_con_alumno(client, nivel_actual.id)

    r = client.post(
        f"/plan-estudio/{perfil_id}/repaso",
        json={"asignatura_id": asignatura_anterior.id, "oa_ids": [oa_anterior.id]},
        headers=headers,
    )
    assert r.status_code == 404


def test_agregar_repaso_sin_sesion_da_401(client, session):
    nivel_anterior, asignatura_anterior, oa_anterior, nivel_actual = _preparar_nivel_anterior_y_actual(session)
    r = client.post(
        "/plan-estudio/1/repaso", json={"asignatura_id": asignatura_anterior.id, "oa_ids": [oa_anterior.id]},
    )
    assert r.status_code == 401


def test_sesion_con_fecha_pasada_y_no_cumplida_queda_marcada_atrasada(client, session):
    """Fase 1, hallazgo comparando en vivo contra Brincus (Paso 12: "Finalizadas /
    Pendientes / No finalizadas") — ver planificacion/27-plan-incorporacion-hallazgos-brincus.md."""
    nivel, asignatura = _preparar_contenido(session)
    headers, perfil_id = _crear_apoderado_con_alumno(client, nivel.id)
    client.post(
        f"/plan-estudio/{perfil_id}",
        json={"dias_por_semana": 3, "dias_elegidos": ["lunes", "miercoles", "viernes"]},
        headers=headers,
    )
    plan = client.get(f"/plan-estudio/{perfil_id}", headers=headers).json()
    primera_sesion_id = plan["sesiones"][0]["id"]

    sesion_orm = session.get(SesionEstudio, primera_sesion_id)
    sesion_orm.fecha_programada = date.today() - timedelta(days=1)
    session.add(sesion_orm)
    session.commit()

    plan_actualizado = client.get(f"/plan-estudio/{perfil_id}", headers=headers).json()
    sesion_atrasada = next(s for s in plan_actualizado["sesiones"] if s["id"] == primera_sesion_id)
    assert sesion_atrasada["atrasada"] is True
    assert sesion_atrasada["cumplida"] is False

    otra_sesion = next(s for s in plan_actualizado["sesiones"] if s["id"] != primera_sesion_id)
    assert otra_sesion["atrasada"] is False
