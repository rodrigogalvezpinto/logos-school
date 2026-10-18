"""Fase 1, ítem 2.5 del plan de incorporación de hallazgos de Brincus — descarga de guía
en PDF. Ver planificacion/27-plan-incorporacion-hallazgos-brincus.md."""

from app.infrastructure.persistence.orm_models import Asignatura, Nivel, ObjetivoAprendizaje


def _preparar(session):
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

    oa = ObjetivoAprendizaje(
        asignatura_id=asignatura.id, codigo_oficial="MA04OA01",
        descripcion="Contar números hasta el 10.000",
        contenido_guia="## Introducción\n\nAprenderás a **contar** de 10 en 10.\n\n- Punto uno\n- Punto dos",
    )
    session.add(oa)
    session.commit()
    session.refresh(oa)
    return oa


def test_descargar_guia_pdf_devuelve_un_pdf_real(client, session):
    oa = _preparar(session)
    r = client.get(f"/contenido/objetivos/{oa.id}/guia.pdf")
    assert r.status_code == 200
    assert r.headers["content-type"] == "application/pdf"
    assert r.content[:5] == b"%PDF-"
    assert len(r.content) > 500  # un PDF vacío/roto sería mucho más chico


def test_descargar_guia_de_oa_inexistente_da_404(client, session):
    r = client.get("/contenido/objetivos/999999/guia.pdf")
    assert r.status_code == 404


def test_contenido_con_guion_largo_y_tildes_no_rompe_el_pdf(client, session):
    """El contenido real de `contenido/` usa em dash (—) y tildes con frecuencia — sin
    sanitizar, fpdf2 lanza FPDFUnicodeEncodingException con la fuente Helvetica core."""
    nivel = Nivel(
        nombre="4° básico", regimen="A", decreto="439/2012", formato_examen="integrado",
        num_preguntas_examen=20, duracion_examen_min=90,
    )
    session.add(nivel)
    session.commit()
    session.refresh(nivel)
    asignatura = Asignatura(nivel_id=nivel.id, nombre="Lenguaje")
    session.add(asignatura)
    session.commit()
    session.refresh(asignatura)
    oa = ObjetivoAprendizaje(
        asignatura_id=asignatura.id, codigo_oficial="LE04OA02",
        descripcion="Comprensión — análisis de textos",
        contenido_guia="Recuerda — la idea principal está al final. Los signos ¿?¡! también aparecen aquí.",
    )
    session.add(oa)
    session.commit()
    session.refresh(oa)

    r = client.get(f"/contenido/objetivos/{oa.id}/guia.pdf")
    assert r.status_code == 200
    assert r.content[:5] == b"%PDF-"
