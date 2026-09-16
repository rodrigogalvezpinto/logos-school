"""Idea 9 del boceto de innovación (2026-08-17): metas familiares compartidas, no ranking
entre hermanos. Ver `app/application/apoderado/consultas.py`."""

from datetime import date, timedelta

from app.infrastructure.persistence.orm_models import Asignatura, Nivel, ObjetivoAprendizaje, ProgresoOA

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
    email = f"apoderado.meta.{next(_CONTADOR_EMAILS)}@test.cl"
    token = client.post(
        "/auth/registro", json={"email": email, "password": "ClaveSegura123", "nombre": "Apoderado Test"}
    ).json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


def _agregar_alumno(client, headers, nivel_id, nombre, rut):
    return client.post(
        "/auth/alumnos", headers=headers,
        json={"nombre": nombre, "apellidos": "Test", "fecha_nacimiento": "2016-01-01", "rut": rut, "nivel_id": nivel_id},
    ).json()["id"]


def test_con_un_solo_alumno_da_null(client, session):
    nivel, _ = _preparar_nivel(session)
    headers = _registrar_apoderado(client)
    _agregar_alumno(client, headers, nivel.id, "Único Hijo", "1-9")

    r = client.get("/apoderado/meta-familiar", headers=headers)
    assert r.status_code == 200
    assert r.json() is None


def test_suma_dias_activos_de_ambos_hijos_esta_semana(client, session):
    nivel, oa = _preparar_nivel(session)
    headers = _registrar_apoderado(client)
    perfil_a = _agregar_alumno(client, headers, nivel.id, "Alumno A", "1-9")
    perfil_b = _agregar_alumno(client, headers, nivel.id, "Alumno B", "2-7")

    # Ambos revisan la misma guía hoy → cuenta como 2 "días combinados" (uno por alumno),
    # no como 1 día del calendario familiar.
    client.post(f"/progreso/{perfil_a}/guias/{oa.id}/revisada", headers=headers)
    client.post(f"/progreso/{perfil_b}/guias/{oa.id}/revisada", headers=headers)

    r = client.get("/apoderado/meta-familiar", headers=headers)
    datos = r.json()
    assert datos["dias_esta_semana"] == 2
    assert datos["dias_semana_anterior"] == 0
    assert datos["es_nueva_marca"] is True


def test_meta_familiar_semana_anterior_con_fecha_directa_en_bd(client, session):
    nivel, oa = _preparar_nivel(session)
    headers = _registrar_apoderado(client)
    perfil_a = _agregar_alumno(client, headers, nivel.id, "Alumno A", "1-9")
    perfil_b = _agregar_alumno(client, headers, nivel.id, "Alumno B", "2-7")

    hoy = date.today()
    inicio_semana_actual = hoy - timedelta(days=hoy.weekday())
    hace_9_dias = inicio_semana_actual - timedelta(days=2)  # cae en la semana anterior

    for perfil_id in (perfil_a, perfil_b):
        fila = ProgresoOA(perfil_alumno_id=perfil_id, oa_id=oa.id, estado="en_progreso", ultimo_intento_fecha=hace_9_dias)
        session.add(fila)
    session.commit()

    r = client.get("/apoderado/meta-familiar", headers=headers)
    datos = r.json()
    assert datos["dias_esta_semana"] == 0
    assert datos["dias_semana_anterior"] == 2
    assert datos["es_nueva_marca"] is False


def test_meta_familiar_sin_sesion_da_401(client, session):
    r = client.get("/apoderado/meta-familiar")
    assert r.status_code == 401
