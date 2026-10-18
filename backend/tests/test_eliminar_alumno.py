"""Auditoría de seguridad (2026-08-17): no existía forma de que un apoderado pidiera
borrar los datos de un hijo — brecha real de privacidad para una app que maneja datos de
menores. Ver `app/infrastructure/persistence/repositorios/perfiles_alumno.py::eliminar_en_cascada`."""

from sqlmodel import select

from app.infrastructure.persistence.orm_models import (
    Asignatura,
    CalificacionGuia,
    ConjuntoEvaluacion,
    IntentoEvaluacion,
    Nivel,
    ObjetivoAprendizaje,
    PerfilAlumno,
    PerfilGamificacion,
    PlanDeEstudio,
    Pregunta,
    ProgresoOA,
    ReporteError,
    SesionEstudio,
    Sugerencia,
)

_CONTADOR_EMAILS = iter(range(1, 100_000))


def _preparar_con_datos_en_todas_las_tablas(client, session):
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
    # Un segundo OA que se deja SIN revisar a propósito — si el único OA de la asignatura
    # ya está revisado, el plan de estudio no tiene nada pendiente que agendar y no crea
    # ninguna SesionEstudio (bug de test real encontrado así: sin este segundo OA, la
    # aserción de que existe una sesión antes de borrar fallaba).
    oa_pendiente = ObjetivoAprendizaje(asignatura_id=asignatura.id, codigo_oficial="OA 2", descripcion="Restar")
    session.add(oa)
    session.add(oa_pendiente)
    session.commit()
    session.refresh(oa)
    session.refresh(oa_pendiente)

    pregunta = Pregunta(asignatura_id=asignatura.id, oa_id=oa.id, tipo="alternativas", enunciado="2+2?", opciones=["3", "4"], respuesta_correcta="4")
    session.add(pregunta)
    session.commit()
    session.refresh(pregunta)

    prueba = ConjuntoEvaluacion(tipo="prueba_unidad", asignatura_id=asignatura.id, nombre="Prueba 1", pregunta_ids=[pregunta.id])
    session.add(prueba)
    session.commit()
    session.refresh(prueba)

    email = f"apoderado.eliminar.{next(_CONTADOR_EMAILS)}@test.cl"
    token = client.post(
        "/auth/registro", json={"email": email, "password": "ClaveSegura123", "nombre": "Apoderado Test"}
    ).json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    perfil_id = client.post(
        "/auth/alumnos", headers=headers,
        json={"nombre": "Test", "apellidos": "Test", "fecha_nacimiento": "2016-01-01", "rut": "1-9", "nivel_id": nivel.id},
    ).json()["id"]

    # Genera datos reales en la mayor cantidad de tablas asociadas posible: evaluación,
    # progreso, plan de estudio, gamificación (XP por la guía), sugerencia, calificación,
    # reporte de error.
    client.post(f"/progreso/{perfil_id}/guias/{oa.id}/revisada", headers=headers)  # ProgresoOA + PerfilGamificacion
    client.post(f"/sugerencias/{perfil_id}", headers=headers, json={"texto": "Una idea"})  # Sugerencia
    client.put(f"/calificaciones/{perfil_id}/guias/{oa.id}", headers=headers, json={"estrellas": 5})  # CalificacionGuia
    client.post(f"/evaluaciones/preguntas/{pregunta.id}/reportar-error", headers=headers, json={"perfil_alumno_id": perfil_id, "comentario": "x"})  # ReporteError
    client.post(f"/plan-estudio/{perfil_id}", headers=headers, json={"dias_por_semana": 3, "dias_elegidos": ["lunes", "miercoles", "viernes"]})  # PlanDeEstudio + SesionEstudio

    intento_id = client.post(
        "/evaluaciones/intentos", headers=headers,
        json={"perfil_alumno_id": perfil_id, "conjunto_evaluacion_id": prueba.id},
    ).json()["id"]
    client.post(f"/evaluaciones/intentos/{intento_id}/entregar", headers=headers)  # IntentoEvaluacion

    return perfil_id, headers


def test_eliminar_alumno_borra_todas_las_tablas_asociadas(client, session):
    perfil_id, headers = _preparar_con_datos_en_todas_las_tablas(client, session)

    # Confirma que de verdad hay datos ANTES de borrar — si no, el test no prueba nada.
    assert session.exec(select(ProgresoOA).where(ProgresoOA.perfil_alumno_id == perfil_id)).first() is not None
    assert session.exec(select(PerfilGamificacion).where(PerfilGamificacion.perfil_alumno_id == perfil_id)).first() is not None
    assert session.exec(select(Sugerencia).where(Sugerencia.perfil_alumno_id == perfil_id)).first() is not None
    assert session.exec(select(CalificacionGuia).where(CalificacionGuia.perfil_alumno_id == perfil_id)).first() is not None
    assert session.exec(select(ReporteError).where(ReporteError.perfil_alumno_id == perfil_id)).first() is not None
    assert session.exec(select(PlanDeEstudio).where(PlanDeEstudio.perfil_alumno_id == perfil_id)).first() is not None
    assert session.exec(select(IntentoEvaluacion).where(IntentoEvaluacion.perfil_alumno_id == perfil_id)).first() is not None
    plan_id = session.exec(select(PlanDeEstudio).where(PlanDeEstudio.perfil_alumno_id == perfil_id)).first().id
    assert session.exec(select(SesionEstudio).where(SesionEstudio.plan_estudio_id == plan_id)).first() is not None

    r = client.delete(f"/auth/alumnos/{perfil_id}", headers=headers)
    assert r.status_code == 204

    session.expire_all()
    assert session.get(PerfilAlumno, perfil_id) is None
    assert session.exec(select(ProgresoOA).where(ProgresoOA.perfil_alumno_id == perfil_id)).first() is None
    assert session.exec(select(PerfilGamificacion).where(PerfilGamificacion.perfil_alumno_id == perfil_id)).first() is None
    assert session.exec(select(Sugerencia).where(Sugerencia.perfil_alumno_id == perfil_id)).first() is None
    assert session.exec(select(CalificacionGuia).where(CalificacionGuia.perfil_alumno_id == perfil_id)).first() is None
    assert session.exec(select(ReporteError).where(ReporteError.perfil_alumno_id == perfil_id)).first() is None
    assert session.exec(select(PlanDeEstudio).where(PlanDeEstudio.perfil_alumno_id == perfil_id)).first() is None
    assert session.exec(select(SesionEstudio).where(SesionEstudio.plan_estudio_id == plan_id)).first() is None
    assert session.exec(select(IntentoEvaluacion).where(IntentoEvaluacion.perfil_alumno_id == perfil_id)).first() is None

    # El alumno ya no aparece en la lista de la cuenta.
    r = client.get("/auth/alumnos", headers=headers)
    assert r.json() == []


def test_eliminar_alumno_ajeno_da_403(client, session):
    nivel = Nivel(
        nombre="4° básico", regimen="A", decreto="439/2012", formato_examen="integrado",
        num_preguntas_examen=20, duracion_examen_min=90,
    )
    session.add(nivel)
    session.commit()
    session.refresh(nivel)

    email_a = f"apoderado.eliminar.a.{next(_CONTADOR_EMAILS)}@test.cl"
    token_a = client.post("/auth/registro", json={"email": email_a, "password": "ClaveSegura123", "nombre": "A"}).json()["access_token"]
    perfil_id = client.post(
        "/auth/alumnos", headers={"Authorization": f"Bearer {token_a}"},
        json={"nombre": "Hijo de A", "apellidos": "Test", "fecha_nacimiento": "2016-01-01", "rut": "1-9", "nivel_id": nivel.id},
    ).json()["id"]

    email_b = f"apoderado.eliminar.b.{next(_CONTADOR_EMAILS)}@test.cl"
    token_b = client.post("/auth/registro", json={"email": email_b, "password": "ClaveSegura123", "nombre": "B"}).json()["access_token"]

    r = client.delete(f"/auth/alumnos/{perfil_id}", headers={"Authorization": f"Bearer {token_b}"})
    assert r.status_code == 403

    # Sigue existiendo — el intento ajeno no debe haber borrado nada.
    session.expire_all()
    assert session.get(PerfilAlumno, perfil_id) is not None


def test_eliminar_alumno_sin_sesion_da_401(client, session):
    r = client.delete("/auth/alumnos/1")
    assert r.status_code == 401


def test_eliminar_alumno_inexistente_da_404(client, session):
    email = f"apoderado.eliminar.404.{next(_CONTADOR_EMAILS)}@test.cl"
    token = client.post("/auth/registro", json={"email": email, "password": "ClaveSegura123", "nombre": "Test"}).json()["access_token"]
    r = client.delete("/auth/alumnos/999999", headers={"Authorization": f"Bearer {token}"})
    assert r.status_code == 404
