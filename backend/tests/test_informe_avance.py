"""Fase 1 del plan de incorporación de hallazgos de Brincus — informe de avance
descargable en PDF para el Apoderado. Ver planificacion/27-plan-incorporacion-hallazgos-brincus.md."""

import io

from pypdf import PdfReader

from app.infrastructure.persistence.orm_models import Asignatura, ConjuntoEvaluacion, Nivel, Pregunta

_CONTADOR_EMAILS = iter(range(1, 100_000))


def _preparar(client, session):
    nivel = Nivel(
        nombre="4° básico", regimen="A", decreto="439/2012", formato_examen="integrado",
        num_preguntas_examen=20, duracion_examen_min=90,
    )
    session.add(nivel)
    session.commit()
    session.refresh(nivel)

    email = f"apoderado.informe.{next(_CONTADOR_EMAILS)}@test.cl"
    token = client.post(
        "/auth/registro", json={"email": email, "password": "ClaveSegura123", "nombre": "Apoderado Test"}
    ).json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    perfil_id = client.post(
        "/auth/alumnos", headers=headers,
        json={"nombre": "María José", "apellidos": "Pérez Soto", "fecha_nacimiento": "2016-01-01", "rut": "1-9", "nivel_id": nivel.id},
    ).json()["id"]

    return nivel, perfil_id, headers


def test_descargar_informe_de_avance_devuelve_un_pdf_real_sin_evaluaciones(client, session):
    _, perfil_id, headers = _preparar(client, session)
    r = client.get(f"/auth/alumnos/{perfil_id}/informe-avance.pdf", headers=headers)
    assert r.status_code == 200
    assert r.headers["content-type"] == "application/pdf"
    assert r.content[:5] == b"%PDF-"


def test_descargar_informe_de_avance_con_evaluaciones_entregadas(client, session):
    nivel, perfil_id, headers = _preparar(client, session)
    asignatura = Asignatura(nivel_id=nivel.id, nombre="Matemática")
    session.add(asignatura)
    session.commit()
    session.refresh(asignatura)

    p1 = Pregunta(asignatura_id=asignatura.id, tipo="alternativas", enunciado="2+2?", opciones=["3", "4"], respuesta_correcta="4")
    p2 = Pregunta(asignatura_id=asignatura.id, tipo="alternativas", enunciado="3+3?", opciones=["5", "6"], respuesta_correcta="6")
    session.add(p1); session.add(p2)
    session.commit()
    session.refresh(p1); session.refresh(p2)

    prueba = ConjuntoEvaluacion(
        tipo="prueba_unidad", asignatura_id=asignatura.id, nombre="Prueba de unidad 1",
        pregunta_ids=[p1.id, p2.id],
    )
    session.add(prueba)
    session.commit()
    session.refresh(prueba)

    # Solo se rinde la prueba de unidad — a propósito, para ejercitar el caso donde
    # nota_simulacro queda None y el PDF debe imprimir el marcador "-" sin reventar por
    # un carácter fuera de latin-1 (bug real encontrado: un em dash "—" sin sanitizar
    # tumbaba la generación completa del PDF con FPDFUnicodeEncodingException).
    r = client.post(
        "/evaluaciones/intentos", headers=headers,
        json={"perfil_alumno_id": perfil_id, "conjunto_evaluacion_id": prueba.id},
    )
    intento_id = r.json()["id"]
    client.patch(
        f"/evaluaciones/intentos/{intento_id}/responder", headers=headers,
        json={"pregunta_id": p1.id, "respuesta": "4"},
    )
    client.post(f"/evaluaciones/intentos/{intento_id}/entregar", headers=headers)

    r = client.get(f"/auth/alumnos/{perfil_id}/informe-avance.pdf", headers=headers)
    assert r.status_code == 200
    assert r.headers["content-type"] == "application/pdf"
    assert r.content[:5] == b"%PDF-"

    # P1 del plan de pruebas exhaustivo (planificacion/28-plan-de-pruebas-exhaustivo.md):
    # hasta ahora solo se verificaba el header `%PDF-`, nunca el contenido — leer el texto
    # real confirma que el nombre y la asignatura sí llegan al PDF, y no solo que no
    # revienta (que es lo que ya cubría el caso del em dash arriba).
    texto = "".join(pagina.extract_text() for pagina in PdfReader(io.BytesIO(r.content)).pages)
    assert "María José" in texto
    assert "Matemática" in texto


def test_informe_de_avance_de_alumno_ajeno_da_403(client, session):
    _, perfil_id, _ = _preparar(client, session)
    email_b = f"apoderado.informe.ajeno.{next(_CONTADOR_EMAILS)}@test.cl"
    token_b = client.post(
        "/auth/registro", json={"email": email_b, "password": "ClaveSegura123", "nombre": "Otro"}
    ).json()["access_token"]
    headers_b = {"Authorization": f"Bearer {token_b}"}
    r = client.get(f"/auth/alumnos/{perfil_id}/informe-avance.pdf", headers=headers_b)
    assert r.status_code == 403


def test_informe_de_avance_sin_sesion_da_401(client, session):
    _, perfil_id, _ = _preparar(client, session)
    r = client.get(f"/auth/alumnos/{perfil_id}/informe-avance.pdf")
    assert r.status_code == 401


def test_informe_de_avance_de_perfil_inexistente_da_404(client, session):
    email = f"apoderado.informe.404.{next(_CONTADOR_EMAILS)}@test.cl"
    token = client.post(
        "/auth/registro", json={"email": email, "password": "ClaveSegura123", "nombre": "Apoderado Test"}
    ).json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    r = client.get("/auth/alumnos/999999/informe-avance.pdf", headers=headers)
    assert r.status_code == 404
