"""Plan Lector por nivel (hallazgo comparando en vivo contra Brincus — ver
planificacion/25-analisis-competencia-brincus.md)."""

from app.infrastructure.persistence.orm_models import LibroPlanLector, Nivel


def test_listar_plan_lector_de_un_nivel(client, session):
    nivel = Nivel(
        nombre="4° básico", regimen="A", decreto="439/2012", formato_examen="integrado",
        num_preguntas_examen=20, duracion_examen_min=90,
    )
    session.add(nivel)
    session.commit()
    session.refresh(nivel)

    session.add(LibroPlanLector(nivel_id=nivel.id, orden=2, titulo="Matilda", autor="Roald Dahl", editorial="Alfaguara"))
    session.add(LibroPlanLector(nivel_id=nivel.id, orden=1, titulo="Papelucho", autor="Marcela Paz", editorial="Planeta"))
    session.commit()

    r = client.get(f"/plan-lector/nivel/{nivel.id}")
    assert r.status_code == 200
    titulos = [libro["titulo"] for libro in r.json()]
    assert titulos == ["Papelucho", "Matilda"]  # respeta el orden, no el orden de inserción


def test_listar_plan_lector_de_nivel_sin_libros_devuelve_lista_vacia(client, session):
    r = client.get("/plan-lector/nivel/999999")
    assert r.status_code == 200
    assert r.json() == []


def test_plan_lector_no_exige_sesion(client, session):
    """Contenido de exploración libre, igual que /contenido/niveles — sin datos personales."""
    r = client.get("/plan-lector/nivel/1")
    assert r.status_code == 200
