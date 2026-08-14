from app.infrastructure.persistence.orm_models import Asignatura, Nivel, ObjetivoAprendizaje


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
