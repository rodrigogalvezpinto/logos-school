"""Útiles Escolares por nivel (hallazgo comparando en vivo contra Brincus — ver
planificacion/25-analisis-competencia-brincus.md, Paso 12, sección "Informaciones")."""

from app.infrastructure.persistence.orm_models import Nivel, UtilEscolar


def test_listar_utiles_escolares_de_un_nivel(client, session):
    nivel = Nivel(
        nombre="4° básico", regimen="A", decreto="439/2012", formato_examen="integrado",
        num_preguntas_examen=20, duracion_examen_min=90,
    )
    session.add(nivel)
    session.commit()
    session.refresh(nivel)

    session.add(UtilEscolar(nivel_id=nivel.id, orden=2, nombre="Regla", cantidad="1", asignatura="Matemática"))
    session.add(UtilEscolar(nivel_id=nivel.id, orden=1, nombre="Estuche", cantidad="1", asignatura=None))
    session.commit()

    r = client.get(f"/utiles-escolares/nivel/{nivel.id}")
    assert r.status_code == 200
    nombres = [u["nombre"] for u in r.json()]
    assert nombres == ["Estuche", "Regla"]  # respeta el orden, no el orden de inserción
    assert r.json()[0]["asignatura"] is None


def test_listar_utiles_escolares_de_nivel_sin_utiles_devuelve_lista_vacia(client, session):
    r = client.get("/utiles-escolares/nivel/999999")
    assert r.status_code == 200
    assert r.json() == []


def test_utiles_escolares_no_exige_sesion(client, session):
    """Contenido de exploración libre, igual que /plan-lector y /contenido/niveles — sin
    datos personales."""
    r = client.get("/utiles-escolares/nivel/1")
    assert r.status_code == 200
