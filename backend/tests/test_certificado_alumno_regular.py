"""Fase 1, ítem 2.7 del plan de incorporación de hallazgos de Brincus — certificado de
alumno regular en PDF. Ver planificacion/27-plan-incorporacion-hallazgos-brincus.md."""

import io

from pypdf import PdfReader

from app.infrastructure.persistence.orm_models import Nivel

_CONTADOR_EMAILS = iter(range(1, 100_000))


def _preparar(client, session):
    nivel = Nivel(
        nombre="4° básico", regimen="A", decreto="439/2012", formato_examen="integrado",
        num_preguntas_examen=20, duracion_examen_min=90,
    )
    session.add(nivel)
    session.commit()
    session.refresh(nivel)

    email = f"apoderado.certificado.{next(_CONTADOR_EMAILS)}@test.cl"
    token = client.post(
        "/auth/registro", json={"email": email, "password": "ClaveSegura123", "nombre": "Apoderado Test"}
    ).json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    perfil_id = client.post(
        "/auth/alumnos", headers=headers,
        json={"nombre": "María José", "apellidos": "Pérez Soto", "fecha_nacimiento": "2016-01-01", "rut": "1-9", "nivel_id": nivel.id},
    ).json()["id"]

    return perfil_id, headers


def test_descargar_certificado_devuelve_un_pdf_real(client, session):
    perfil_id, headers = _preparar(client, session)
    r = client.get(f"/auth/alumnos/{perfil_id}/certificado.pdf", headers=headers)
    assert r.status_code == 200
    assert r.headers["content-type"] == "application/pdf"
    assert r.content[:5] == b"%PDF-"


def test_certificado_de_alumno_ajeno_da_403(client, session):
    perfil_id, _ = _preparar(client, session)
    email_b = f"apoderado.certificado.ajeno.{next(_CONTADOR_EMAILS)}@test.cl"
    token_b = client.post(
        "/auth/registro", json={"email": email_b, "password": "ClaveSegura123", "nombre": "Otro"}
    ).json()["access_token"]
    headers_b = {"Authorization": f"Bearer {token_b}"}
    r = client.get(f"/auth/alumnos/{perfil_id}/certificado.pdf", headers=headers_b)
    assert r.status_code == 403


def test_certificado_sin_sesion_da_401(client, session):
    perfil_id, _ = _preparar(client, session)
    r = client.get(f"/auth/alumnos/{perfil_id}/certificado.pdf")
    assert r.status_code == 401


def test_certificado_contiene_el_nombre_real_del_alumno_y_el_nivel(client, session):
    """P1 del plan de pruebas exhaustivo (planificacion/28-plan-de-pruebas-exhaustivo.md):
    hasta ahora solo se verificaba el header `%PDF-`, nunca el contenido — un bug de
    contenido (nombre cortado, dato mal armado) pasaría sin que ningún test lo note. Ya pasó
    una vez en esta sesión con el bug del guion largo en /seleccion-plan (encontrado porque
    ESE test sí ejercitaba datos reales, no por leer un PDF)."""
    perfil_id, headers = _preparar(client, session)
    r = client.get(f"/auth/alumnos/{perfil_id}/certificado.pdf", headers=headers)
    assert r.status_code == 200

    texto = "".join(pagina.extract_text() for pagina in PdfReader(io.BytesIO(r.content)).pages)
    assert "María José" in texto
    assert "Pérez Soto" in texto
    assert "4° básico" in texto


def test_certificado_de_perfil_inexistente_da_404(client, session):
    email = f"apoderado.certificado.404.{next(_CONTADOR_EMAILS)}@test.cl"
    token = client.post(
        "/auth/registro", json={"email": email, "password": "ClaveSegura123", "nombre": "Apoderado Test"}
    ).json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    r = client.get("/auth/alumnos/999999/certificado.pdf", headers=headers)
    assert r.status_code == 404
