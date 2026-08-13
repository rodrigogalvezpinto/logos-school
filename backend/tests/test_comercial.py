from datetime import date, timedelta

from app.infrastructure.persistence.orm_models import Cuenta, CuentaAdmin, Nivel, PerfilAlumno, Plan
from app.infrastructure.seguridad.bcrypt_hasheador import HasheadorPasswordBcrypt


def _token_admin(client, session, email="admin@logos.cl"):
    cuenta = CuentaAdmin(email=email, nombre="Admin Test", password_hash=HasheadorPasswordBcrypt().hashear("ClaveAdmin123"))
    session.add(cuenta)
    session.commit()
    r = client.post("/admin/auth/login", json={"email": email, "password": "ClaveAdmin123"})
    return r.json()["access_token"]


def _headers_admin(client, session):
    return {"Authorization": f"Bearer {_token_admin(client, session)}"}


def test_listar_planes_requiere_sesion_admin(client):
    r = client.get("/admin/planes")
    assert r.status_code in (401, 403)


def test_crear_editar_y_desactivar_plan(client, session):
    headers = _headers_admin(client, session)

    r = client.post("/admin/planes", headers=headers, json={"nombre": "Mensual", "nivel_de_acceso": "completo", "precio_clp": 19990})
    assert r.status_code == 201
    plan_id = r.json()["id"]
    assert r.json()["activo"] is True

    r = client.patch(f"/admin/planes/{plan_id}", headers=headers, json={"nombre": "Mensual Plus", "nivel_de_acceso": "completo", "precio_clp": 24990})
    assert r.status_code == 200
    assert r.json()["nombre"] == "Mensual Plus"
    assert r.json()["precio_clp"] == 24990

    r = client.post(f"/admin/planes/{plan_id}/desactivar", headers=headers)
    assert r.status_code == 200
    assert r.json()["activo"] is False

    r = client.post(f"/admin/planes/{plan_id}/activar", headers=headers)
    assert r.status_code == 200
    assert r.json()["activo"] is True

    r = client.get("/admin/planes", headers=headers)
    assert len(r.json()) == 1


def test_crear_plan_con_precio_negativo_falla(client, session):
    headers = _headers_admin(client, session)
    r = client.post("/admin/planes", headers=headers, json={"nombre": "Malo", "nivel_de_acceso": "completo", "precio_clp": -100})
    assert r.status_code == 422


def test_crear_y_desactivar_codigo_descuento(client, session):
    headers = _headers_admin(client, session)

    r = client.post(
        "/admin/descuentos", headers=headers,
        json={"codigo": "BIENVENIDA20", "tipo": "porcentaje", "valor": 20, "usos_maximos": 100},
    )
    assert r.status_code == 201
    descuento_id = r.json()["id"]
    assert r.json()["vigente"] is True

    r = client.post(f"/admin/descuentos/{descuento_id}/desactivar", headers=headers)
    assert r.status_code == 200
    assert r.json()["vigente"] is False

    r = client.get("/admin/descuentos", headers=headers)
    assert len(r.json()) == 1
    assert r.json()[0]["vigente"] is False


def test_codigo_descuento_vencido_no_esta_vigente(client, session):
    headers = _headers_admin(client, session)
    ayer = (date.today() - timedelta(days=1)).isoformat()
    r = client.post(
        "/admin/descuentos", headers=headers,
        json={"codigo": "VENCIDO", "tipo": "monto_fijo", "valor": 5000, "fecha_vencimiento": ayer},
    )
    assert r.status_code == 201
    assert r.json()["vigente"] is False


def _crear_alumno(session):
    cuenta = Cuenta(email="familia.comercial@test.cl", password_hash="x", nombre="Apoderado Test")
    session.add(cuenta)
    session.commit()
    session.refresh(cuenta)

    nivel = Nivel(
        nombre="4° básico", regimen="A", decreto="439/2012", formato_examen="integrado",
        num_preguntas_examen=20, duracion_examen_min=90,
    )
    session.add(nivel)
    session.commit()
    session.refresh(nivel)

    perfil = PerfilAlumno(
        cuenta_apoderado_id=cuenta.id, nombre="Sofía", apellidos="Pérez",
        fecha_nacimiento=date(2016, 1, 1), rut="21.345.678-4", nivel_id=nivel.id,
    )
    session.add(perfil)
    session.commit()
    session.refresh(perfil)
    return cuenta, perfil


def test_buscar_alumno_por_nombre_y_asignar_cortesia(client, session):
    headers = _headers_admin(client, session)
    cuenta, perfil = _crear_alumno(session)

    plan = Plan(nombre="Mensual", nivel_de_acceso="completo", precio_clp=19990)
    session.add(plan)
    session.commit()
    session.refresh(plan)

    r = client.get("/admin/alumnos/buscar?q=Sofía", headers=headers)
    assert r.status_code == 200
    assert len(r.json()) == 1
    assert r.json()[0]["email_apoderado"] == "familia.comercial@test.cl"

    r = client.post(f"/admin/alumnos/{perfil.id}/cortesia", headers=headers, json={"plan_id": plan.id})
    assert r.status_code == 204

    r = client.get("/admin/metricas", headers=headers)
    assert r.status_code == 200
    datos = r.json()
    assert datos["alumnos_registrados"] == 1
    assert datos["apoderados_registrados"] == 1
    assert datos["suscripciones_por_plan"] == [{"plan_id": plan.id, "plan_nombre": "Mensual", "activas": 1}]


def test_asignar_cortesia_a_alumno_inexistente_da_404(client, session):
    headers = _headers_admin(client, session)
    plan = Plan(nombre="Mensual", nivel_de_acceso="completo", precio_clp=19990)
    session.add(plan)
    session.commit()
    session.refresh(plan)

    r = client.post("/admin/alumnos/9999/cortesia", headers=headers, json={"plan_id": plan.id})
    assert r.status_code == 404


def test_metricas_sin_datos_devuelve_ceros(client, session):
    headers = _headers_admin(client, session)
    r = client.get("/admin/metricas", headers=headers)
    assert r.status_code == 200
    datos = r.json()
    assert datos["apoderados_registrados"] == 0
    assert datos["alumnos_registrados"] == 0
    assert datos["suscripciones_por_plan"] == []
    assert datos["ingresos_mes_aprox_clp"] == 0
