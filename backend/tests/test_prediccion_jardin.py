""""Racha de la casa" / jardín semanal — idea 3 del boceto de innovación (2026-08-17),
variante "jardín" recomendada tras evaluar los límites de la idea original (una planta que
se marchita, descartada por contradecir el lenguaje "todavía no"). Ver
`app/application/prediccion/consultas.py`."""

from datetime import date, timedelta

from app.infrastructure.persistence.orm_models import Nivel, ProgresoOA

_CONTADOR_EMAILS = iter(range(1, 100_000))


def _preparar(client, session):
    nivel = Nivel(
        nombre="4° básico", regimen="A", decreto="439/2012", formato_examen="integrado",
        num_preguntas_examen=20, duracion_examen_min=90,
    )
    session.add(nivel)
    session.commit()
    session.refresh(nivel)

    email = f"apoderado.jardin.{next(_CONTADOR_EMAILS)}@test.cl"
    token = client.post(
        "/auth/registro", json={"email": email, "password": "ClaveSegura123", "nombre": "Apoderado Test"}
    ).json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    perfil_id = client.post(
        "/auth/alumnos", headers=headers,
        json={"nombre": "Test", "apellidos": "Test", "fecha_nacimiento": "2016-01-01", "rut": "1-9", "nivel_id": nivel.id},
    ).json()["id"]

    return perfil_id, headers


def test_sin_actividad_las_8_semanas_son_semilla(client, session):
    perfil_id, headers = _preparar(client, session)
    r = client.get(f"/prediccion/{perfil_id}/jardin-semanal", headers=headers)
    assert r.status_code == 200
    semanas = r.json()
    assert len(semanas) == 8
    assert all(s["etapa"] == "semilla" and s["dias_activos"] == 0 for s in semanas)


def test_una_semana_con_mucha_actividad_da_flor_completa(client, session):
    """No hay forma de forzar `ultimo_intento_fecha` por API (siempre usa
    `reloj.ahora()`), así que se marca directo en el ORM — 7 OA distintos revisados en
    días distintos de la SEMANA ANTERIOR (ya completa, a diferencia de la semana actual que
    todavía podría estar a mitad de camino según qué día es hoy)."""
    from app.infrastructure.persistence.orm_models import Asignatura, ObjetivoAprendizaje

    perfil_id, headers = _preparar(client, session)

    nivel_id = client.get("/contenido/niveles", headers=headers).json()[0]["id"]
    asignatura = Asignatura(nivel_id=nivel_id, nombre="Matemática")
    session.add(asignatura)
    session.commit()
    session.refresh(asignatura)

    hoy = date.today()
    inicio_semana_actual = hoy - timedelta(days=hoy.weekday())
    inicio_semana_anterior = inicio_semana_actual - timedelta(days=7)
    for i in range(7):
        oa = ObjetivoAprendizaje(asignatura_id=asignatura.id, codigo_oficial=f"OA {i}", descripcion=f"Objetivo {i}")
        session.add(oa)
        session.commit()
        session.refresh(oa)
        fila = ProgresoOA(
            perfil_alumno_id=perfil_id, oa_id=oa.id, estado="en_progreso",
            ultimo_intento_fecha=inicio_semana_anterior + timedelta(days=i),
        )
        session.add(fila)
    session.commit()

    r = client.get(f"/prediccion/{perfil_id}/jardin-semanal", headers=headers)
    semanas = r.json()
    semana_anterior = semanas[-2]  # penúltima = semana anterior, ya completa
    assert semana_anterior["dias_activos"] == 7
    assert semana_anterior["etapa"] == "flor_completa"


def test_jardin_de_alumno_ajeno_da_403(client, session):
    perfil_id, _ = _preparar(client, session)
    token_b = client.post(
        "/auth/registro", json={"email": f"ajeno.jardin.{next(_CONTADOR_EMAILS)}@test.cl", "password": "ClaveSegura123", "nombre": "Otro"}
    ).json()["access_token"]
    r = client.get(f"/prediccion/{perfil_id}/jardin-semanal", headers={"Authorization": f"Bearer {token_b}"})
    assert r.status_code == 403


def test_jardin_sin_sesion_da_401(client, session):
    perfil_id, _ = _preparar(client, session)
    r = client.get(f"/prediccion/{perfil_id}/jardin-semanal")
    assert r.status_code == 401
