"""Cambiar contraseña con sesión y eliminar la cuenta del apoderado (2026-11-22)."""

from sqlmodel import select

from app.infrastructure.persistence.orm_models import Cuenta, Nivel, PerfilAlumno, ProgresoOA, Suscripcion, Plan

EMAIL = "papa.cuenta@ejemplo.cl"
CLAVE = "ClaveVieja123"


def _h(token):
    return {"Authorization": f"Bearer {token}"}


def _registrar(client):
    r = client.post("/auth/registro", json={"email": EMAIL, "password": CLAVE, "nombre": "Papá"})
    assert r.status_code == 201
    return r.json()["access_token"]


def test_cambiar_password_mantiene_la_sesion_y_cierra_las_demas(client):
    token_a = _registrar(client)
    token_b = client.post("/auth/login", json={"email": EMAIL, "password": CLAVE}).json()["access_token"]
    r = client.post("/auth/cambiar-password", headers=_h(token_a),
                    json={"password_actual": CLAVE, "password_nuevo": "ClaveNueva456"})
    assert r.status_code == 200
    nuevo = r.json()["access_token"]
    assert client.get("/auth/yo", headers=_h(nuevo)).status_code == 200
    assert client.get("/auth/yo", headers=_h(token_b)).status_code == 401
    assert client.post("/auth/login", json={"email": EMAIL, "password": "ClaveNueva456"}).status_code == 200


def test_cambiar_password_con_actual_incorrecta_falla(client):
    token = _registrar(client)
    r = client.post("/auth/cambiar-password", headers=_h(token),
                    json={"password_actual": "otra", "password_nuevo": "ClaveNueva456"})
    assert r.status_code == 400
    assert client.post("/auth/login", json={"email": EMAIL, "password": CLAVE}).status_code == 200


def test_cambiar_password_requiere_sesion(client):
    r = client.post("/auth/cambiar-password", json={"password_actual": CLAVE, "password_nuevo": "ClaveNueva456"})
    assert r.status_code == 401


def test_eliminar_cuenta_borra_alumnos_y_su_historial(client, session):
    session.add(Nivel(nombre="4° básico", regimen="A", decreto="439/2012", formato_examen="integrado",
                      num_preguntas_examen=20, duracion_examen_min=90))
    session.add(Plan(nombre="Mensual", nivel_de_acceso="completo", precio_clp=19990))
    session.commit()
    token = _registrar(client)
    r = client.post("/auth/alumnos", headers=_h(token), json={
        "nombre": "Sofía", "apellidos": "Pérez", "fecha_nacimiento": "2016-03-12", "rut": "21.345.678-4", "nivel_id": 1})
    assert r.status_code == 201
    alumno_id = r.json()["id"]
    plan_id = session.exec(select(Plan)).first().id
    r = client.post(f"/auth/alumnos/{alumno_id}/prueba-gratis", headers=_h(token), json={"plan_id": plan_id})
    assert r.status_code in (200, 201)
    assert session.exec(select(Suscripcion)).all() != []

    # Contraseña incorrecta: no borra nada.
    assert client.post("/auth/eliminar-cuenta", headers=_h(token), json={"password": "mala"}).status_code == 400
    assert session.exec(select(Cuenta).where(Cuenta.email == EMAIL)).first() is not None

    assert client.post("/auth/eliminar-cuenta", headers=_h(token), json={"password": CLAVE}).status_code == 204
    session.expire_all()
    assert session.exec(select(Cuenta).where(Cuenta.email == EMAIL)).first() is None
    assert session.exec(select(PerfilAlumno)).all() == []
    assert session.exec(select(Suscripcion)).all() == []
    assert session.exec(select(ProgresoOA)).all() == []
    # El token queda sin cuenta: ya no sirve.
    assert client.get("/auth/yo", headers=_h(token)).status_code == 401
    # El correo queda libre para registrarse de nuevo.
    assert client.post("/auth/registro", json={"email": EMAIL, "password": CLAVE, "nombre": "Papá"}).status_code == 201


def test_cuenta_solo_google_se_elimina_escribiendo_el_correo(client, session):
    session.add(Cuenta(email="google@ejemplo.cl", nombre="G", google_id="g-123"))
    session.commit()
    from app.infrastructure.seguridad.jose_tokens import ServicioTokenJWT
    cuenta = session.exec(select(Cuenta).where(Cuenta.email == "google@ejemplo.cl")).one()
    token = ServicioTokenJWT().generar(cuenta.id, cuenta.sesion_version)
    assert client.post("/auth/eliminar-cuenta", headers=_h(token), json={"confirmacion_email": "otro@x.cl"}).status_code == 400
    assert client.post("/auth/eliminar-cuenta", headers=_h(token), json={"confirmacion_email": "Google@Ejemplo.cl"}).status_code == 204
