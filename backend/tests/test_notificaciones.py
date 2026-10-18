"""Centro de notificaciones (Fase 1, ver planificacion/27-plan-incorporacion-hallazgos-brincus.md
— hallazgo comparando en vivo contra Brincus, Paso 12)."""

from datetime import date, timedelta

from app.infrastructure.persistence.orm_models import (
    Asignatura,
    Comunicado,
    CuentaProfesor,
    CursoSeccion,
    Nivel,
    ObjetivoAprendizaje,
    PerfilAlumno,
    ReporteError,
    SesionEstudio,
)

_CONTADOR_EMAILS = iter(range(1, 100_000))


def _preparar(client, session):
    nivel = Nivel(
        nombre="4° básico", regimen="A", decreto="439/2012", formato_examen="integrado",
        num_preguntas_examen=20, duracion_examen_min=90,
    )
    session.add(nivel)
    session.commit()
    session.refresh(nivel)

    email = f"apoderado.notif.{next(_CONTADOR_EMAILS)}@test.cl"
    token = client.post(
        "/auth/registro", json={"email": email, "password": "ClaveSegura123", "nombre": "Apoderado Test"}
    ).json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    perfil_id = client.post(
        "/auth/alumnos", headers=headers,
        json={"nombre": "Test", "apellidos": "Test", "fecha_nacimiento": "2016-01-01", "rut": "1-9", "nivel_id": nivel.id},
    ).json()["id"]

    return nivel, perfil_id, headers


def test_notificaciones_vacias_sin_curso_plan_ni_reportes(client, session):
    _, perfil_id, headers = _preparar(client, session)
    r = client.get(f"/notificaciones/{perfil_id}", headers=headers)
    assert r.status_code == 200
    assert r.json() == []


def test_comunicado_del_curso_aparece_como_notificacion(client, session):
    nivel, perfil_id, headers = _preparar(client, session)

    profesor = CuentaProfesor(email="prof.notif@test.cl", password_hash="x", nombre="Profesora", estado="aprobado")
    session.add(profesor)
    session.commit()
    session.refresh(profesor)

    curso = CursoSeccion(profesor_id=profesor.id, nivel_id=nivel.id, nombre="4° básico A")
    session.add(curso)
    session.commit()
    session.refresh(curso)

    alumno = session.get(PerfilAlumno, perfil_id)
    alumno.curso_seccion_id = curso.id
    session.add(alumno)
    session.commit()

    session.add(Comunicado(curso_seccion_id=curso.id, titulo="Bienvenida", cuerpo="Recuerden traer materiales."))
    session.commit()

    r = client.get(f"/notificaciones/{perfil_id}", headers=headers)
    assert r.status_code == 200
    notifs = r.json()
    assert len(notifs) == 1
    assert notifs[0]["tipo"] == "comunicado"
    assert notifs[0]["titulo"] == "Bienvenida"


def test_sesion_de_plan_atrasada_aparece_como_notificacion(client, session):
    nivel, perfil_id, headers = _preparar(client, session)
    asignatura = Asignatura(nivel_id=nivel.id, nombre="Matemática")
    session.add(asignatura)
    session.commit()
    session.refresh(asignatura)
    session.add(ObjetivoAprendizaje(asignatura_id=asignatura.id, codigo_oficial="OA 1", descripcion="Objetivo 1"))
    session.commit()

    client.post(
        f"/plan-estudio/{perfil_id}",
        json={"dias_por_semana": 3, "dias_elegidos": ["lunes", "miercoles", "viernes"]},
        headers=headers,
    )
    plan = client.get(f"/plan-estudio/{perfil_id}", headers=headers).json()
    primera_sesion_id = plan["sesiones"][0]["id"]

    sesion_orm = session.get(SesionEstudio, primera_sesion_id)
    sesion_orm.fecha_programada = date.today() - timedelta(days=1)
    session.add(sesion_orm)
    session.commit()

    r = client.get(f"/notificaciones/{perfil_id}", headers=headers)
    assert r.status_code == 200
    notifs = r.json()
    assert any(n["tipo"] == "sesion_atrasada" for n in notifs)


def test_reporte_de_error_resuelto_aparece_como_notificacion_pero_no_el_pendiente(client, session):
    _, perfil_id, headers = _preparar(client, session)

    session.add(ReporteError(
        tipo_contenido="pregunta", contenido_id=1, perfil_alumno_id=perfil_id,
        comentario="Esta pregunta está mal.", resuelto=True,
    ))
    session.add(ReporteError(
        tipo_contenido="pregunta", contenido_id=2, perfil_alumno_id=perfil_id,
        comentario="Esta otra también.", resuelto=False,
    ))
    session.commit()

    r = client.get(f"/notificaciones/{perfil_id}", headers=headers)
    assert r.status_code == 200
    notifs = r.json()
    assert len(notifs) == 1
    assert notifs[0]["tipo"] == "reporte_resuelto"


def test_notificaciones_de_alumno_ajeno_da_403(client, session):
    _, perfil_id, _ = _preparar(client, session)
    email_b = f"apoderado.notif.ajeno.{next(_CONTADOR_EMAILS)}@test.cl"
    token_b = client.post(
        "/auth/registro", json={"email": email_b, "password": "ClaveSegura123", "nombre": "Otro"}
    ).json()["access_token"]
    headers_b = {"Authorization": f"Bearer {token_b}"}
    r = client.get(f"/notificaciones/{perfil_id}", headers=headers_b)
    assert r.status_code == 403


def test_notificaciones_sin_sesion_da_401(client, session):
    _, perfil_id, _ = _preparar(client, session)
    r = client.get(f"/notificaciones/{perfil_id}")
    assert r.status_code == 401
