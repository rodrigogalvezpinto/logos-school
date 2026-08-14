from app.infrastructure.persistence.orm_models import CuentaAdmin, Nivel
from app.infrastructure.seguridad.bcrypt_hasheador import HasheadorPasswordBcrypt


def _crear_nivel(session):
    nivel = Nivel(
        nombre="4° básico", regimen="A", decreto="439/2012", formato_examen="integrado",
        num_preguntas_examen=20, duracion_examen_min=90,
    )
    session.add(nivel)
    session.commit()
    session.refresh(nivel)
    return nivel


def _headers_admin_curso(client, session):
    from sqlmodel import select

    existente = session.exec(select(CuentaAdmin).where(CuentaAdmin.email == "admin.curso@logos.cl")).first()
    if not existente:
        admin = CuentaAdmin(email="admin.curso@logos.cl", nombre="Admin", password_hash=HasheadorPasswordBcrypt().hashear("ClaveAdmin123"))
        session.add(admin)
        session.commit()
    token_admin = client.post("/admin/auth/login", json={"email": "admin.curso@logos.cl", "password": "ClaveAdmin123"}).json()["access_token"]
    return {"Authorization": f"Bearer {token_admin}"}


def _profesor_aprobado(client, session, email="profe.curso@test.cl"):
    headers_admin = _headers_admin_curso(client, session)

    token_profesor = client.post(
        "/profesor/auth/registro", json={"email": email, "password": "ClaveProfe123", "nombre": "Profe Test"}
    ).json()["access_token"]
    headers_profesor = {"Authorization": f"Bearer {token_profesor}"}

    pendientes = client.get("/admin/profesores/pendientes", headers=headers_admin).json()
    profesor_id = next(p["id"] for p in pendientes if p["email"] == email)
    client.post(f"/admin/profesores/{profesor_id}/aprobar", headers=headers_admin)

    return headers_profesor


def _alumno_de_apoderado(client, nivel_id, email="familia.curso@test.cl"):
    token = client.post(
        "/auth/registro", json={"email": email, "password": "ClaveSegura123", "nombre": "Apoderado Test"}
    ).json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    r = client.post(
        "/auth/alumnos", headers=headers,
        json={"nombre": "Sofía", "apellidos": "Pérez", "fecha_nacimiento": "2016-03-12", "rut": "21.345.678-4", "nivel_id": nivel_id},
    )
    return headers, r.json()["id"]


def test_crear_curso_y_agregar_alumno(client, session):
    nivel = _crear_nivel(session)
    headers_profesor = _profesor_aprobado(client, session)
    headers_apoderado, perfil_id = _alumno_de_apoderado(client, nivel.id)

    r = client.post("/profesor/cursos", headers=headers_profesor, json={"nivel_id": nivel.id, "nombre": "4° básico A"})
    assert r.status_code == 201
    curso_id = r.json()["id"]

    r = client.post(f"/profesor/cursos/{curso_id}/alumnos/{perfil_id}", headers=headers_profesor)
    assert r.status_code == 204

    r = client.get(f"/curso-seccion/mi-curso/{perfil_id}", headers=headers_apoderado)
    assert r.status_code == 200
    assert r.json()["nombre_curso"] == "4° básico A"


def test_quitar_alumno_del_curso(client, session):
    nivel = _crear_nivel(session)
    headers_profesor = _profesor_aprobado(client, session)
    headers_apoderado, perfil_id = _alumno_de_apoderado(client, nivel.id)

    curso_id = client.post("/profesor/cursos", headers=headers_profesor, json={"nivel_id": nivel.id, "nombre": "4° básico A"}).json()["id"]
    client.post(f"/profesor/cursos/{curso_id}/alumnos/{perfil_id}", headers=headers_profesor)

    r = client.delete(f"/profesor/cursos/{curso_id}/alumnos/{perfil_id}", headers=headers_profesor)
    assert r.status_code == 204

    r = client.get(f"/curso-seccion/mi-curso/{perfil_id}", headers=headers_apoderado)
    assert r.json() is None


def test_no_se_puede_agregar_un_alumno_de_otro_nivel(client, session):
    nivel_4basico = _crear_nivel(session)
    nivel_8basico = Nivel(
        nombre="8° básico", regimen="B", decreto="614/2013", formato_examen="separado",
        num_preguntas_examen=25, duracion_examen_min=90,
    )
    session.add(nivel_8basico)
    session.commit()
    session.refresh(nivel_8basico)

    headers_profesor = _profesor_aprobado(client, session)
    _, perfil_id = _alumno_de_apoderado(client, nivel_4basico.id)

    curso_id = client.post(
        "/profesor/cursos", headers=headers_profesor, json={"nivel_id": nivel_8basico.id, "nombre": "8° básico A"}
    ).json()["id"]

    r = client.post(f"/profesor/cursos/{curso_id}/alumnos/{perfil_id}", headers=headers_profesor)
    assert r.status_code == 400

    r = client.get(f"/profesor/cursos/{curso_id}/progreso", headers=headers_profesor)
    assert r.json()["alumnos"] == []


def test_un_profesor_no_puede_tocar_el_curso_de_otro(client, session):
    nivel = _crear_nivel(session)
    headers_profesor_1 = _profesor_aprobado(client, session, email="profe1@test.cl")
    headers_profesor_2 = _profesor_aprobado(client, session, email="profe2@test.cl")
    _, perfil_id = _alumno_de_apoderado(client, nivel.id)

    curso_id = client.post("/profesor/cursos", headers=headers_profesor_1, json={"nivel_id": nivel.id, "nombre": "Curso de 1"}).json()["id"]

    r = client.post(f"/profesor/cursos/{curso_id}/alumnos/{perfil_id}", headers=headers_profesor_2)
    assert r.status_code == 403

    r = client.get(f"/profesor/cursos/{curso_id}/progreso", headers=headers_profesor_2)
    assert r.status_code == 403

    r = client.post(
        f"/profesor/cursos/{curso_id}/comunicados", headers=headers_profesor_2,
        json={"titulo": "x", "cuerpo": "y"},
    )
    assert r.status_code == 403


def test_operaciones_sobre_curso_inexistente_dan_404(client, session):
    nivel = _crear_nivel(session)
    headers_profesor = _profesor_aprobado(client, session)
    _, perfil_id = _alumno_de_apoderado(client, nivel.id)

    assert client.post(f"/profesor/cursos/99999/alumnos/{perfil_id}", headers=headers_profesor).status_code == 404
    assert client.get("/profesor/cursos/99999/progreso", headers=headers_profesor).status_code == 404
    r = client.post(
        "/profesor/cursos/99999/comunicados", headers=headers_profesor,
        json={"titulo": "x", "cuerpo": "y"},
    )
    assert r.status_code == 404


def test_progreso_de_curso_trae_notas_reales(client, session):
    nivel = _crear_nivel(session)
    headers_profesor = _profesor_aprobado(client, session)
    headers_apoderado, perfil_id = _alumno_de_apoderado(client, nivel.id)

    curso_id = client.post("/profesor/cursos", headers=headers_profesor, json={"nivel_id": nivel.id, "nombre": "4° básico A"}).json()["id"]
    client.post(f"/profesor/cursos/{curso_id}/alumnos/{perfil_id}", headers=headers_profesor)

    r = client.get(f"/profesor/cursos/{curso_id}/progreso", headers=headers_profesor)
    assert r.status_code == 200
    datos = r.json()
    assert len(datos["alumnos"]) == 1
    assert datos["alumnos"][0]["nombre"] == "Sofía"
    assert datos["alumnos"][0]["notas_por_asignatura"] == []  # todavía no rindió nada


def test_publicar_comunicado_lo_deja_ver_al_apoderado(client, session):
    nivel = _crear_nivel(session)
    headers_profesor = _profesor_aprobado(client, session)
    headers_apoderado, perfil_id = _alumno_de_apoderado(client, nivel.id)

    curso_id = client.post("/profesor/cursos", headers=headers_profesor, json={"nivel_id": nivel.id, "nombre": "4° básico A"}).json()["id"]
    client.post(f"/profesor/cursos/{curso_id}/alumnos/{perfil_id}", headers=headers_profesor)

    r = client.post(
        f"/profesor/cursos/{curso_id}/comunicados", headers=headers_profesor,
        json={"titulo": "Bienvenida", "cuerpo": "Empezamos la próxima semana."},
    )
    assert r.status_code == 201

    r = client.get(f"/curso-seccion/mi-curso/{perfil_id}", headers=headers_apoderado)
    assert len(r.json()["comunicados"]) == 1
    assert r.json()["comunicados"][0]["titulo"] == "Bienvenida"


def test_alumno_sin_curso_mi_curso_devuelve_null(client, session):
    nivel = _crear_nivel(session)
    headers_apoderado, perfil_id = _alumno_de_apoderado(client, nivel.id)

    r = client.get(f"/curso-seccion/mi-curso/{perfil_id}", headers=headers_apoderado)
    assert r.status_code == 200
    assert r.json() is None


def test_profesor_puede_buscar_alumnos_para_agregar(client, session):
    nivel = _crear_nivel(session)
    headers_profesor = _profesor_aprobado(client, session)
    _, perfil_id = _alumno_de_apoderado(client, nivel.id)

    r = client.get("/profesor/alumnos/buscar", headers=headers_profesor, params={"q": "Sofía"})
    assert r.status_code == 200
    assert len(r.json()) == 1
    assert r.json()[0]["perfil_alumno_id"] == perfil_id


def test_listar_mis_cursos(client, session):
    nivel = _crear_nivel(session)
    headers_profesor = _profesor_aprobado(client, session)

    client.post("/profesor/cursos", headers=headers_profesor, json={"nivel_id": nivel.id, "nombre": "Curso A"})
    client.post("/profesor/cursos", headers=headers_profesor, json={"nivel_id": nivel.id, "nombre": "Curso B"})

    r = client.get("/profesor/cursos", headers=headers_profesor)
    assert r.status_code == 200
    assert len(r.json()) == 2
