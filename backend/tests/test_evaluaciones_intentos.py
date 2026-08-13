from datetime import date

from app.infrastructure.persistence.orm_models import Asignatura, ConjuntoEvaluacion, Cuenta, Nivel, PerfilAlumno, Pregunta


def _preparar(session):
    cuenta = Cuenta(email="apoderado@test.cl", password_hash="x", nombre="Apoderado Test")
    session.add(cuenta)
    session.commit()
    session.refresh(cuenta)

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

    p1 = Pregunta(asignatura_id=asignatura.id, tipo="alternativas", enunciado="2+2?", opciones=["3", "4"], respuesta_correcta="4")
    p2 = Pregunta(asignatura_id=asignatura.id, tipo="alternativas", enunciado="3+3?", opciones=["5", "6"], respuesta_correcta="6")
    p3 = Pregunta(asignatura_id=asignatura.id, tipo="desarrollo_breve", enunciado="Explica.", respuesta_correcta="algo")
    session.add(p1); session.add(p2); session.add(p3)
    session.commit()
    session.refresh(p1); session.refresh(p2); session.refresh(p3)

    conjunto = ConjuntoEvaluacion(
        tipo="prueba_unidad", asignatura_id=asignatura.id, nombre="Prueba de prueba",
        pregunta_ids=[p1.id, p2.id, p3.id],
    )
    session.add(conjunto)
    session.commit()
    session.refresh(conjunto)

    perfil = PerfilAlumno(
        cuenta_apoderado_id=cuenta.id, nombre="Test", apellidos="Test",
        fecha_nacimiento=date(2016, 1, 1), rut="1-9", nivel_id=nivel.id,
    )
    session.add(perfil)
    session.commit()
    session.refresh(perfil)

    return conjunto, perfil, (p1, p2, p3)


def test_ciclo_completo_iniciar_responder_entregar(client, session):
    conjunto, perfil, (p1, p2, p3) = _preparar(session)

    r = client.post("/evaluaciones/intentos", json={"perfil_alumno_id": perfil.id, "conjunto_evaluacion_id": conjunto.id})
    assert r.status_code == 201
    intento_id = r.json()["id"]
    assert r.json()["nota"] is None

    r = client.patch(f"/evaluaciones/intentos/{intento_id}/responder", json={"pregunta_id": p1.id, "respuesta": "4"})
    assert r.status_code == 200
    assert r.json()["respuestas"] == {str(p1.id): "4"}

    client.patch(f"/evaluaciones/intentos/{intento_id}/responder", json={"pregunta_id": p2.id, "respuesta": "5"})  # incorrecta

    r = client.post(f"/evaluaciones/intentos/{intento_id}/entregar")
    assert r.status_code == 200
    datos = r.json()
    # 1 de 2 preguntas autocorregibles correcta (la de desarrollo no cuenta)
    assert datos["puntaje"] == 1.0
    assert datos["nota"] == 3.5  # calcular_nota(1, 2): aprobación=1.2, nota=1+3*(1/1.2)=3.5
    assert datos["fecha_termino"] is not None


def test_entregar_es_idempotente(client, session):
    conjunto, perfil, (p1, p2, p3) = _preparar(session)
    r = client.post("/evaluaciones/intentos", json={"perfil_alumno_id": perfil.id, "conjunto_evaluacion_id": conjunto.id})
    intento_id = r.json()["id"]
    client.patch(f"/evaluaciones/intentos/{intento_id}/responder", json={"pregunta_id": p1.id, "respuesta": "4"})

    primera = client.post(f"/evaluaciones/intentos/{intento_id}/entregar").json()
    segunda = client.post(f"/evaluaciones/intentos/{intento_id}/entregar").json()
    assert primera == segunda


def test_iniciar_dos_veces_reanuda_el_mismo_intento(client, session):
    conjunto, perfil, _ = _preparar(session)
    r1 = client.post("/evaluaciones/intentos", json={"perfil_alumno_id": perfil.id, "conjunto_evaluacion_id": conjunto.id})
    r2 = client.post("/evaluaciones/intentos", json={"perfil_alumno_id": perfil.id, "conjunto_evaluacion_id": conjunto.id})
    assert r1.json()["id"] == r2.json()["id"]


def test_no_se_puede_responder_un_intento_ya_entregado(client, session):
    conjunto, perfil, (p1, _, _) = _preparar(session)
    r = client.post("/evaluaciones/intentos", json={"perfil_alumno_id": perfil.id, "conjunto_evaluacion_id": conjunto.id})
    intento_id = r.json()["id"]
    client.post(f"/evaluaciones/intentos/{intento_id}/entregar")

    r = client.patch(f"/evaluaciones/intentos/{intento_id}/responder", json={"pregunta_id": p1.id, "respuesta": "4"})
    assert r.status_code == 400


def test_conjunto_no_expone_respuesta_correcta(client, session):
    conjunto, _, _ = _preparar(session)
    r = client.get(f"/evaluaciones/conjuntos/{conjunto.id}")
    assert r.status_code == 200
    for p in r.json()["preguntas"]:
        assert "respuesta_correcta" not in p
