from app.core.config import settings


def _registrar(client, email="familia@test.cl", password="ClaveSegura123"):
    return client.post(
        "/auth/registro",
        json={"email": email, "password": password, "nombre": "Apoderado Test"},
    )


def test_registro_exitoso_devuelve_token(client):
    r = _registrar(client)
    assert r.status_code == 201
    assert "access_token" in r.json()


def test_registro_no_falla_aunque_el_envio_de_correo_falle(client, monkeypatch):
    """Bug real evitado a propósito: al conectar Resend, se encontró que
    `resend.Emails.send(...)` no tenía manejo de errores — con el dominio remitente sin
    verificar en Resend (`logos.cl`, confirmado a mano contra la API real), CADA registro
    real habría reventado con un 500 en cuanto se configurara la API key. Este test simula
    esa falla explícitamente y confirma que el registro sigue devolviendo 201 (el correo es
    una notificación secundaria, nunca una condición para que la cuenta se cree)."""
    import resend

    from app.core.config import settings as settings_reales

    monkeypatch.setattr(settings_reales, "resend_api_key", "re_clave_de_prueba")

    def _falla(*args, **kwargs):
        raise Exception("The logos.cl domain is not verified.")

    monkeypatch.setattr(resend.Emails, "send", _falla)

    r = _registrar(client, "correo.falla@test.cl")
    assert r.status_code == 201
    assert "access_token" in r.json()


def test_logout_invalida_el_token_de_inmediato(client):
    # Bug real encontrado en el análisis de seguridad: "cerrar sesión" solo borraba el
    # token del navegador, pero el mismo JWT seguía siendo una credencial válida en el
    # servidor hasta expirar (hasta 12 horas) — si alguien lo copiaba antes del logout,
    # cerrar sesión no lo detenía. Ahora un logout invalida el token de inmediato.
    r = client.post("/auth/registro", json={"email": "logout@test.cl", "password": "ClaveSegura123", "nombre": "QA"})
    token = r.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    assert client.get("/auth/yo", headers=headers).status_code == 200

    r = client.post("/auth/logout", headers=headers)
    assert r.status_code == 204

    r = client.get("/auth/yo", headers=headers)
    assert r.status_code == 401


def test_logout_no_afecta_a_otras_cuentas(client):
    token_a = client.post("/auth/registro", json={"email": "a-logout@test.cl", "password": "ClaveSegura123", "nombre": "A"}).json()["access_token"]
    token_b = client.post("/auth/registro", json={"email": "b-logout@test.cl", "password": "ClaveSegura123", "nombre": "B"}).json()["access_token"]

    client.post("/auth/logout", headers={"Authorization": f"Bearer {token_a}"})

    r = client.get("/auth/yo", headers={"Authorization": f"Bearer {token_b}"})
    assert r.status_code == 200


def test_login_de_nuevo_tras_logout_da_un_token_valido(client):
    datos = {"email": "reloggin@test.cl", "password": "ClaveSegura123"}
    client.post("/auth/registro", json={**datos, "nombre": "QA"})

    token_1 = client.post("/auth/login", json=datos).json()["access_token"]
    client.post("/auth/logout", headers={"Authorization": f"Bearer {token_1}"})

    token_2 = client.post("/auth/login", json=datos).json()["access_token"]
    r = client.get("/auth/yo", headers={"Authorization": f"Bearer {token_2}"})
    assert r.status_code == 200


def test_registro_es_insensible_a_mayusculas_en_el_correo(client):
    # Bug real encontrado probando la app: "a@x.cl" y "A@X.CL" se registraban como dos
    # cuentas distintas para lo que el usuario considera el mismo correo.
    r1 = client.post("/auth/registro", json={"email": "mayusculas@test.cl", "password": "ClaveSegura123", "nombre": "QA"})
    assert r1.status_code == 201
    r2 = client.post("/auth/registro", json={"email": "MAYUSCULAS@TEST.CL", "password": "OtraClave123", "nombre": "QA2"})
    assert r2.status_code == 400


def test_login_es_insensible_a_mayusculas_en_el_correo(client):
    client.post("/auth/registro", json={"email": "loginmayus@test.cl", "password": "ClaveSegura123", "nombre": "QA"})
    r = client.post("/auth/login", json={"email": "LoginMayus@Test.CL", "password": "ClaveSegura123"})
    assert r.status_code == 200


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
    from app.infrastructure.persistence.orm_models import Nivel

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
            "rut": "21.345.678-4",
            "nivel_id": 1,
        },
    )
    assert r.status_code == 201
    assert r.json()["nombre"] == "Sofía"
    assert r.json()["nombre_nivel"] == "4° básico"


def test_agregar_alumno_con_fecha_de_nacimiento_futura_es_rechazado(client, session):
    from app.infrastructure.persistence.orm_models import Nivel

    session.add(
        Nivel(
            nombre="4° básico", regimen="A", decreto="439/2012", formato_examen="integrado",
            num_preguntas_examen=20, duracion_examen_min=90,
        )
    )
    session.commit()

    token = _registrar(client, "fechafutura@test.cl").json()["access_token"]
    r = client.post(
        "/auth/alumnos",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "nombre": "Futuro", "apellidos": "Niño",
            "fecha_nacimiento": "2099-01-01", "rut": "55.555.555-5", "nivel_id": 1,
        },
    )
    assert r.status_code == 422


def test_agregar_alumno_con_nivel_inexistente_da_404_no_500(client, session):
    # Bug real encontrado probando la app: nivel_id tiene FK en la BD pero nada lo
    # validaba antes — un nivel_id inexistente reventaba con un 500 crudo (IntegrityError).
    token = _registrar(client, "nivelinexistente@test.cl").json()["access_token"]
    r = client.post(
        "/auth/alumnos",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "nombre": "Sofía", "apellidos": "Pérez",
            "fecha_nacimiento": "2016-03-12", "rut": "21.345.678-4", "nivel_id": 999999,
        },
    )
    assert r.status_code == 404


def test_dos_apoderados_distintos_no_pueden_registrar_el_mismo_rut(client, session):
    # Bug real encontrado probando la app: dos cuentas de Apoderado distintas podían
    # registrar un PerfilAlumno con el mismo RUT sin ningún aviso — datos de un menor
    # duplicados (o "robados" por otra cuenta) sin que nadie se enterara.
    from app.infrastructure.persistence.orm_models import Nivel

    session.add(
        Nivel(
            nombre="4° básico", regimen="A", decreto="439/2012", formato_examen="integrado",
            num_preguntas_examen=20, duracion_examen_min=90,
        )
    )
    session.commit()

    token_a = _registrar(client, "apoderadoA@test.cl").json()["access_token"]
    token_b = _registrar(client, "apoderadoB@test.cl").json()["access_token"]

    datos = {
        "nombre": "Niño", "apellidos": "Uno",
        "fecha_nacimiento": "2016-01-01", "rut": "11.111.111-1", "nivel_id": 1,
    }
    r1 = client.post("/auth/alumnos", headers={"Authorization": f"Bearer {token_a}"}, json=datos)
    assert r1.status_code == 201

    datos_b = {**datos, "nombre": "Niño Robado", "rut": "11111111-1"}  # mismo RUT, sin puntos
    r2 = client.post("/auth/alumnos", headers={"Authorization": f"Bearer {token_b}"}, json=datos_b)
    assert r2.status_code == 400


def test_agregar_alumno_con_rut_invalido_es_rechazado(client, session):
    from app.infrastructure.persistence.orm_models import Nivel

    session.add(
        Nivel(
            nombre="4° básico", regimen="A", decreto="439/2012", formato_examen="integrado",
            num_preguntas_examen=20, duracion_examen_min=90,
        )
    )
    session.commit()

    token = _registrar(client, "rutmalo@test.cl").json()["access_token"]
    r = client.post(
        "/auth/alumnos",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "nombre": "Sofía", "apellidos": "Pérez",
            "fecha_nacimiento": "2016-03-12", "rut": "21.345.678-9",  # dígito verificador incorrecto (correcto es -4)
            "nivel_id": 1,
        },
    )
    assert r.status_code == 422


def test_listar_alumnos_solo_devuelve_los_propios(client, session):
    from app.infrastructure.persistence.orm_models import Nivel

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
    assert r_a.json()[0]["nombre_nivel"] == "4° básico"


def _crear_alumno(client, token, nivel_id=1, rut="1-9"):
    return client.post(
        "/auth/alumnos",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "nombre": "Alumno Prueba",
            "apellidos": "Test",
            "fecha_nacimiento": "2016-01-01",
            "rut": rut,
            "nivel_id": nivel_id,
        },
    ).json()


def _crear_nivel_y_plan(session):
    from app.infrastructure.persistence.orm_models import Nivel, Plan

    session.add(
        Nivel(
            nombre="4° básico", regimen="A", decreto="439/2012", formato_examen="integrado",
            num_preguntas_examen=20, duracion_examen_min=90,
        )
    )
    plan = Plan(nombre="Mensual", nivel_de_acceso="completo", precio_clp=19990)
    session.add(plan)
    session.commit()
    session.refresh(plan)
    return plan


def test_listar_planes_solo_devuelve_los_activos(client, session):
    from app.infrastructure.persistence.orm_models import Plan

    plan_activo = _crear_nivel_y_plan(session)
    session.add(Plan(nombre="Descontinuado", nivel_de_acceso="completo", precio_clp=9990, activo=False))
    session.commit()

    token = _registrar(client, "planes@test.cl").json()["access_token"]
    r = client.get("/auth/planes", headers={"Authorization": f"Bearer {token}"})
    assert r.status_code == 200
    nombres = [p["nombre"] for p in r.json()]
    assert plan_activo.nombre in nombres
    assert "Descontinuado" not in nombres


def test_iniciar_prueba_gratis_activa_suscripcion_de_5_dias(client, session):
    from datetime import datetime

    from sqlmodel import select

    from app.infrastructure.persistence.orm_models import Suscripcion

    plan = _crear_nivel_y_plan(session)
    token = _registrar(client, "prueba@test.cl").json()["access_token"]
    alumno = _crear_alumno(client, token)

    r = client.post(
        f"/auth/alumnos/{alumno['id']}/prueba-gratis",
        headers={"Authorization": f"Bearer {token}"},
        json={"plan_id": plan.id},
    )
    assert r.status_code == 200
    fecha_termino = datetime.fromisoformat(r.json()["fecha_termino"])
    assert (fecha_termino - datetime.now(fecha_termino.tzinfo)).days in (4, 5)

    suscripcion = session.exec(select(Suscripcion).where(Suscripcion.perfil_alumno_id == alumno["id"])).first()
    assert suscripcion.origen == "prueba_gratis"
    assert suscripcion.estado == "activa"
    assert suscripcion.plan_id == plan.id


def test_iniciar_prueba_gratis_no_permite_activar_alumno_ajeno(client, session):
    plan = _crear_nivel_y_plan(session)
    token_a = _registrar(client, "duenoA@test.cl").json()["access_token"]
    token_b = _registrar(client, "duenoB@test.cl").json()["access_token"]
    alumno_de_a = _crear_alumno(client, token_a)

    r = client.post(
        f"/auth/alumnos/{alumno_de_a['id']}/prueba-gratis",
        headers={"Authorization": f"Bearer {token_b}"},
        json={"plan_id": plan.id},
    )
    assert r.status_code == 403


def test_registro_da_429_al_pasar_el_limite_configurado(client):
    """/auth/registro está limitado por IP (slowapi) — protección real contra fuerza
    bruta/creación masiva de cuentas, nunca verificada hasta ahora (P0 del plan de pruebas
    exhaustivo, planificacion/28-plan-de-pruebas-exhaustivo.md). El límite se lee de
    `settings.limite_registro_por_minuto` en vez de un número fijo: en Desarrollo se
    configura más alto (ver `.env` local) para que la suite Playwright completa —que
    registra muchas cuentas de prueba en corridas rápidas— no choque con un valor pensado
    para tráfico real; acá se verifica el mecanismo en sí, no un número mágico."""
    limite = settings.limite_registro_por_minuto
    for i in range(limite):
        r = _registrar(client, f"rate.registro.{i}@test.cl")
        assert r.status_code == 201

    r = _registrar(client, "rate.registro.excedido@test.cl")
    assert r.status_code == 429


def test_login_da_429_al_pasar_el_limite_configurado(client):
    """/auth/login está limitado por IP — mismo motivo que el registro, pero con un umbral
    más alto por defecto porque un usuario legítimo puede equivocarse la contraseña varias
    veces seguidas."""
    _registrar(client, "rate.login@test.cl")

    limite = settings.limite_login_por_minuto
    for _ in range(limite):
        r = client.post("/auth/login", json={"email": "rate.login@test.cl", "password": "clave-mala"})
        assert r.status_code == 401

    r = client.post("/auth/login", json={"email": "rate.login@test.cl", "password": "clave-mala"})
    assert r.status_code == 429


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


def test_agregar_alumno_da_429_al_pasar_el_limite_configurado(client, session):
    """Auditoría de seguridad (2026-08-17): sin límite, una cuenta autenticada podía
    inundar la base de datos con miles de filas de `PerfilAlumno` en minutos — el rate
    limit no reemplaza la lógica de negocio (un apoderado real agrega pocos hijos), es una
    protección contra abuso directo del endpoint."""
    _crear_nivel_y_plan(session)
    token = _registrar(client, "rate.alumnos@test.cl").json()["access_token"]

    limite = settings.limite_agregar_alumno_por_minuto
    for i in range(limite):
        r = client.post(
            "/auth/alumnos", headers={"Authorization": f"Bearer {token}"},
            json={
                "nombre": "Alumno Prueba", "apellidos": "Test", "fecha_nacimiento": "2016-01-01",
                "rut": _rut_valido(30_000_000 + i), "nivel_id": 1,
            },
        )
        assert r.status_code == 201

    r = client.post(
        "/auth/alumnos", headers={"Authorization": f"Bearer {token}"},
        json={
            "nombre": "Alumno Excedido", "apellidos": "Test", "fecha_nacimiento": "2016-01-01",
            "rut": _rut_valido(30_000_000 + limite), "nivel_id": 1,
        },
    )
    assert r.status_code == 429
