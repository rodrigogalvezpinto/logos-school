def _registrar(client, email="familia@test.cl", password="ClaveSegura123"):
    return client.post(
        "/auth/registro",
        json={"email": email, "password": password, "nombre": "Apoderado Test"},
    )


def test_registro_exitoso_devuelve_token(client):
    r = _registrar(client)
    assert r.status_code == 201
    assert "access_token" in r.json()


def test_registro_duplicado_falla(client):
    _registrar(client)
    r2 = _registrar(client)
    assert r2.status_code == 400


def test_login_correcto(client):
    _registrar(client, "login@test.cl", "ClaveSegura123")
    r = client.post("/auth/login", json={"email": "login@test.cl", "password": "ClaveSegura123"})
    assert r.status_code == 200
    assert "access_token" in r.json()


def test_login_password_incorrecta(client):
    _registrar(client, "login2@test.cl", "ClaveSegura123")
    r = client.post("/auth/login", json={"email": "login2@test.cl", "password": "otraClave"})
    assert r.status_code == 401
    # No debe revelar si el correo existe o no (ver planificacion/20-seguridad-y-casos-borde.md)
    assert "incorrectos" in r.json()["detail"].lower()


def test_login_correo_inexistente_mismo_mensaje_que_password_incorrecta(client):
    r = client.post("/auth/login", json={"email": "nadie@test.cl", "password": "loquesea"})
    assert r.status_code == 401
    assert "incorrectos" in r.json()["detail"].lower()


def test_yo_sin_token_rechaza(client):
    r = client.get("/auth/yo")
    assert r.status_code in (401, 403)


def test_yo_con_token_devuelve_cuenta(client):
    token = _registrar(client, "yo@test.cl").json()["access_token"]
    r = client.get("/auth/yo", headers={"Authorization": f"Bearer {token}"})
    assert r.status_code == 200
    assert r.json()["email"] == "yo@test.cl"


def test_agregar_alumno_requiere_nivel_existente(client, session):
    from app.models import Nivel

    session.add(
        Nivel(
            nombre="4° básico",
            regimen="A",
            decreto="439/2012",
            formato_examen="integrado",
            num_preguntas_examen=20,
            duracion_examen_min=90,
        )
    )
    session.commit()

    token = _registrar(client, "conAlumno@test.cl").json()["access_token"]
    r = client.post(
        "/auth/alumnos",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "nombre": "Sofía",
            "apellidos": "Pérez",
            "fecha_nacimiento": "2016-03-12",
            "rut": "21.345.678-9",
            "nivel_id": 1,
        },
    )
    assert r.status_code == 201
    assert r.json()["nombre"] == "Sofía"


def test_listar_alumnos_solo_devuelve_los_propios(client, session):
    from app.models import Nivel

    session.add(
        Nivel(
            nombre="4° básico",
            regimen="A",
            decreto="439/2012",
            formato_examen="integrado",
            num_preguntas_examen=20,
            duracion_examen_min=90,
        )
    )
    session.commit()

    token_a = _registrar(client, "a@test.cl").json()["access_token"]
    token_b = _registrar(client, "b@test.cl").json()["access_token"]

    client.post(
        "/auth/alumnos",
        headers={"Authorization": f"Bearer {token_a}"},
        json={
            "nombre": "Hijo de A",
            "apellidos": "Test",
            "fecha_nacimiento": "2016-01-01",
            "rut": "1-9",
            "nivel_id": 1,
        },
    )

    r_b = client.get("/auth/alumnos", headers={"Authorization": f"Bearer {token_b}"})
    assert r_b.status_code == 200
    assert r_b.json() == []  # B no debe ver al hijo de A

    r_a = client.get("/auth/alumnos", headers={"Authorization": f"Bearer {token_a}"})
    assert len(r_a.json()) == 1
