"""Idea 1 del boceto de innovación (2026-08-17): "Estadísticas" como vista propia del
Apoderado, agregando a todos sus alumnos de una vez. Ver
`app/application/apoderado/consultas.py`."""

from app.infrastructure.persistence.orm_models import Asignatura, Nivel, ObjetivoAprendizaje

_CONTADOR_EMAILS = iter(range(1, 100_000))


def _preparar_nivel(session):
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

    oa = ObjetivoAprendizaje(asignatura_id=asignatura.id, codigo_oficial="OA 1", descripcion="Sumar")
    session.add(oa)
    session.commit()
    session.refresh(oa)

    return nivel, oa


def _registrar_apoderado(client):
    email = f"apoderado.estadisticas.{next(_CONTADOR_EMAILS)}@test.cl"
    token = client.post(
        "/auth/registro", json={"email": email, "password": "ClaveSegura123", "nombre": "Apoderado Test"}
    ).json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


def _agregar_alumno(client, headers, nivel_id, nombre, rut):
    return client.post(
        "/auth/alumnos", headers=headers,
        json={"nombre": nombre, "apellidos": "Test", "fecha_nacimiento": "2016-01-01", "rut": rut, "nivel_id": nivel_id},
    ).json()["id"]


def test_estadisticas_de_dos_alumnos(client, session):
    nivel, oa = _preparar_nivel(session)
    headers = _registrar_apoderado(client)
    perfil_a = _agregar_alumno(client, headers, nivel.id, "Alumno A", "1-9")
    perfil_b = _agregar_alumno(client, headers, nivel.id, "Alumno B", "2-7")

    # Alumno A revisa la única guía → 100% de cobertura.
    client.post(f"/progreso/{perfil_a}/guias/{oa.id}/revisada", headers=headers)

    r = client.get("/apoderado/estadisticas", headers=headers)
    assert r.status_code == 200
    datos = {e["perfil_alumno_id"]: e for e in r.json()}

    assert datos[perfil_a]["nombre"] == "Alumno A"
    assert datos[perfil_a]["cobertura_pct"] == 100.0
    assert datos[perfil_b]["nombre"] == "Alumno B"
    assert datos[perfil_b]["cobertura_pct"] == 0.0


def test_estadisticas_sin_alumnos_da_lista_vacia(client, session):
    headers = _registrar_apoderado(client)
    r = client.get("/apoderado/estadisticas", headers=headers)
    assert r.status_code == 200
    assert r.json() == []


def test_estadisticas_solo_trae_los_alumnos_propios(client, session):
    nivel, _ = _preparar_nivel(session)
    headers_a = _registrar_apoderado(client)
    headers_b = _registrar_apoderado(client)
    _agregar_alumno(client, headers_a, nivel.id, "Alumno de A", "3-5")

    r = client.get("/apoderado/estadisticas", headers=headers_b)
    assert r.json() == []


def test_estadisticas_sin_sesion_da_401(client, session):
    r = client.get("/apoderado/estadisticas")
    assert r.status_code == 401
