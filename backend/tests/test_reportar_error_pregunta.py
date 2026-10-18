"""Fase 1, ítems 2.1 y 2.6 del plan de incorporación de hallazgos de Brincus — reportar
error de contenido a nivel de pregunta individual. Ver
planificacion/27-plan-incorporacion-hallazgos-brincus.md."""

from app.core.config import settings
from app.infrastructure.persistence.orm_models import Asignatura, Nivel, Pregunta, ReporteError

_CONTADOR_EMAILS = iter(range(1, 100_000))


def _preparar(client, session):
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

    pregunta = Pregunta(
        asignatura_id=asignatura.id, tipo="alternativas", enunciado="2+2?",
        opciones=["3", "4"], respuesta_correcta="5",  # a propósito mal calibrada, como en Brincus
    )
    session.add(pregunta)
    session.commit()
    session.refresh(pregunta)

    email = f"apoderado.reporte.{next(_CONTADOR_EMAILS)}@test.cl"
    token = client.post(
        "/auth/registro", json={"email": email, "password": "ClaveSegura123", "nombre": "Apoderado Test"}
    ).json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    perfil_id = client.post(
        "/auth/alumnos", headers=headers,
        json={"nombre": "Test", "apellidos": "Test", "fecha_nacimiento": "2016-01-01", "rut": "1-9", "nivel_id": nivel.id},
    ).json()["id"]

    return pregunta, perfil_id, headers


def test_reportar_error_de_pregunta(client, session):
    pregunta, perfil_id, headers = _preparar(client, session)

    r = client.post(
        f"/evaluaciones/preguntas/{pregunta.id}/reportar-error", headers=headers,
        json={"perfil_alumno_id": perfil_id, "comentario": "La respuesta correcta debería ser 4, no 5."},
    )
    assert r.status_code == 201
    body = r.json()
    assert body["tipo_contenido"] == "pregunta"
    assert body["contenido_id"] == pregunta.id


def test_reportar_error_sin_comentario_tambien_funciona(client, session):
    """Brincus permite un reporte de un click, sin obligar a escribir nada."""
    pregunta, perfil_id, headers = _preparar(client, session)

    r = client.post(
        f"/evaluaciones/preguntas/{pregunta.id}/reportar-error", headers=headers,
        json={"perfil_alumno_id": perfil_id},
    )
    assert r.status_code == 201


def test_reportar_error_de_pregunta_inexistente_da_404(client, session):
    _, perfil_id, headers = _preparar(client, session)
    r = client.post(
        "/evaluaciones/preguntas/999999/reportar-error", headers=headers,
        json={"perfil_alumno_id": perfil_id, "comentario": "x"},
    )
    assert r.status_code == 404


def test_reportar_error_de_alumno_ajeno_da_403(client, session):
    pregunta, _, headers = _preparar(client, session)
    email_b = f"apoderado.reporte.ajeno.{next(_CONTADOR_EMAILS)}@test.cl"
    token_b = client.post(
        "/auth/registro", json={"email": email_b, "password": "ClaveSegura123", "nombre": "Otro"}
    ).json()["access_token"]
    headers_b = {"Authorization": f"Bearer {token_b}"}
    perfil_b_id = client.post(
        "/auth/alumnos", headers=headers_b,
        json={"nombre": "Otro Alumno", "apellidos": "T", "fecha_nacimiento": "2016-01-01", "rut": "2-7", "nivel_id": 1},
    ).json()["id"]

    # headers (dueño A) reporta usando el perfil de B → debe rechazarse.
    r = client.post(
        f"/evaluaciones/preguntas/{pregunta.id}/reportar-error", headers=headers,
        json={"perfil_alumno_id": perfil_b_id, "comentario": "x"},
    )
    assert r.status_code == 403


def test_reportar_error_con_comentario_demasiado_largo_da_422(client, session):
    """Auditoría de seguridad (Fase 1, ver
    planificacion/27-plan-incorporacion-hallazgos-brincus.md): sin límite, un request
    directo a la API podía guardar un blob de texto arbitrariamente grande."""
    pregunta, perfil_id, headers = _preparar(client, session)
    r = client.post(
        f"/evaluaciones/preguntas/{pregunta.id}/reportar-error", headers=headers,
        json={"perfil_alumno_id": perfil_id, "comentario": "x" * 1001},
    )
    assert r.status_code == 422


def test_reportar_error_sin_sesion_da_401(client, session):
    pregunta, perfil_id, _ = _preparar(client, session)
    r = client.post(
        f"/evaluaciones/preguntas/{pregunta.id}/reportar-error",
        json={"perfil_alumno_id": perfil_id, "comentario": "x"},
    )
    assert r.status_code == 401


def test_reportar_error_con_payload_adversarial_se_guarda_como_texto_literal(client, session):
    """P0 del plan de pruebas exhaustivo — mismo criterio que sugerencias: sin bandeja de
    Admin todavía para leer reportes por API, se verifica directo en la fila ORM que el
    payload quedó guardado literal, sin ejecutarse ni romper el insert."""
    pregunta, perfil_id, headers = _preparar(client, session)
    payload = "<img src=x onerror=alert(1)>'; DROP TABLE reporte_error;--"
    r = client.post(
        f"/evaluaciones/preguntas/{pregunta.id}/reportar-error", headers=headers,
        json={"perfil_alumno_id": perfil_id, "comentario": payload},
    )
    assert r.status_code == 201
    reporte_id = r.json()["id"]

    reporte = session.get(ReporteError, reporte_id)
    assert reporte.comentario == payload


def test_reportar_error_da_429_al_pasar_el_limite_configurado(client, session):
    """Auditoría de seguridad (2026-08-17): sin límite, un alumno (o cuenta comprometida)
    podía inundar la bandeja de reportes de contenido en segundos."""
    pregunta, perfil_id, headers = _preparar(client, session)

    limite = settings.limite_reportar_error_por_minuto
    for _ in range(limite):
        r = client.post(
            f"/evaluaciones/preguntas/{pregunta.id}/reportar-error", headers=headers,
            json={"perfil_alumno_id": perfil_id, "comentario": "x"},
        )
        assert r.status_code == 201

    r = client.post(
        f"/evaluaciones/preguntas/{pregunta.id}/reportar-error", headers=headers,
        json={"perfil_alumno_id": perfil_id, "comentario": "excedido"},
    )
    assert r.status_code == 429
