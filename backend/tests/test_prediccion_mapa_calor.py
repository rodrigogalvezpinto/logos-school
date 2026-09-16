"""Mapa de calor por eje temático — idea propia (no un hallazgo de Brincus, ver
`app/application/prediccion/consultas.py`). Reutiliza el mismo patrón de fixtures que
`test_prediccion.py`."""

from app.infrastructure.persistence.orm_models import (
    Asignatura,
    ConjuntoEvaluacion,
    Nivel,
    ObjetivoAprendizaje,
    Pregunta,
)

_CONTADOR_EMAILS = iter(range(1, 100_000))


def _rut_valido(cuerpo: int) -> str:
    cuerpo_str = str(cuerpo)
    suma = 0
    multiplicador = 2
    for c in reversed(cuerpo_str):
        suma += int(c) * multiplicador
        multiplicador = multiplicador + 1 if multiplicador < 7 else 2
    resto = 11 - (suma % 11)
    dv = "0" if resto == 11 else "K" if resto == 10 else str(resto)
    return f"{cuerpo_str}-{dv}"


def _crear_contenido(session):
    """Dos OA de la misma asignatura, en dos ejes temáticos distintos, para poder
    verificar que el mapa de calor los separa en vez de mezclarlos."""
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

    oa_numeros = ObjetivoAprendizaje(
        asignatura_id=asignatura.id, codigo_oficial="OA 1", descripcion="Sumar", eje_tematico="Números",
    )
    oa_geometria = ObjetivoAprendizaje(
        asignatura_id=asignatura.id, codigo_oficial="OA 5", descripcion="Figuras", eje_tematico="Geometría",
    )
    session.add(oa_numeros); session.add(oa_geometria)
    session.commit()
    session.refresh(oa_numeros); session.refresh(oa_geometria)

    p_numeros_1 = Pregunta(
        asignatura_id=asignatura.id, oa_id=oa_numeros.id, tipo="alternativas",
        enunciado="2+2?", opciones=["3", "4"], respuesta_correcta="4",
    )
    p_numeros_2 = Pregunta(
        asignatura_id=asignatura.id, oa_id=oa_numeros.id, tipo="alternativas",
        enunciado="3+3?", opciones=["5", "6"], respuesta_correcta="6",
    )
    p_geometria = Pregunta(
        asignatura_id=asignatura.id, oa_id=oa_geometria.id, tipo="alternativas",
        enunciado="¿Cuántos lados tiene un triángulo?", opciones=["3", "4"], respuesta_correcta="3",
    )
    session.add(p_numeros_1); session.add(p_numeros_2); session.add(p_geometria)
    session.commit()
    session.refresh(p_numeros_1); session.refresh(p_numeros_2); session.refresh(p_geometria)

    prueba = ConjuntoEvaluacion(
        tipo="prueba_unidad", asignatura_id=asignatura.id, nombre="Prueba de unidad 1",
        pregunta_ids=[p_numeros_1.id, p_numeros_2.id, p_geometria.id],
    )
    session.add(prueba)
    session.commit()
    session.refresh(prueba)

    return nivel, asignatura, prueba, (p_numeros_1, p_numeros_2, p_geometria)


def _crear_apoderado_con_alumno(client, nivel):
    n = next(_CONTADOR_EMAILS)
    email = f"apoderado.mapacalor.{n}@test.cl"
    token = client.post(
        "/auth/registro", json={"email": email, "password": "ClaveSegura123", "nombre": "Apoderado Test"},
    ).json()["access_token"]
    r = client.post(
        "/auth/alumnos", headers={"Authorization": f"Bearer {token}"},
        json={"nombre": "Test", "apellidos": "Test", "fecha_nacimiento": "2016-01-01", "rut": _rut_valido(10_000_000 + n), "nivel_id": nivel.id},
    )
    return token, r.json()["id"]


def _rendir(client, token, perfil_id, conjunto_id, respuestas: dict[int, str]):
    headers = {"Authorization": f"Bearer {token}"}
    intento_id = client.post(
        "/evaluaciones/intentos", headers=headers,
        json={"perfil_alumno_id": perfil_id, "conjunto_evaluacion_id": conjunto_id},
    ).json()["id"]
    for pregunta_id, respuesta in respuestas.items():
        client.patch(
            f"/evaluaciones/intentos/{intento_id}/responder", headers=headers,
            json={"pregunta_id": pregunta_id, "respuesta": respuesta},
        )
    client.post(f"/evaluaciones/intentos/{intento_id}/entregar", headers=headers)


def test_sin_evaluaciones_entregadas_da_lista_vacia(client, session):
    nivel, asignatura, prueba, preguntas = _crear_contenido(session)
    token, perfil_id = _crear_apoderado_con_alumno(client, nivel)

    r = client.get(f"/prediccion/{perfil_id}/mapa-calor", headers={"Authorization": f"Bearer {token}"})
    assert r.status_code == 200
    assert r.json() == []


def test_separa_correctamente_por_eje_tematico(client, session):
    nivel, asignatura, prueba, (p_numeros_1, p_numeros_2, p_geometria) = _crear_contenido(session)
    token, perfil_id = _crear_apoderado_con_alumno(client, nivel)

    # Números: 2/2 correctas (100%). Geometría: 0/1 correctas (0%).
    _rendir(client, token, perfil_id, prueba.id, {
        p_numeros_1.id: "4", p_numeros_2.id: "6", p_geometria.id: "4",
    })

    r = client.get(f"/prediccion/{perfil_id}/mapa-calor", headers={"Authorization": f"Bearer {token}"})
    assert r.status_code == 200
    celdas = {c["eje_tematico"]: c for c in r.json()}

    assert celdas["Números"]["pct_correctas"] == 100.0
    assert celdas["Números"]["total_preguntas"] == 2
    assert celdas["Números"]["asignatura_nombre"] == "Matemática"

    assert celdas["Geometría"]["pct_correctas"] == 0.0
    assert celdas["Geometría"]["total_preguntas"] == 1


def test_dos_intentos_del_mismo_eje_se_acumulan(client, session):
    nivel, asignatura, prueba, (p_numeros_1, p_numeros_2, p_geometria) = _crear_contenido(session)
    token, perfil_id = _crear_apoderado_con_alumno(client, nivel)

    _rendir(client, token, perfil_id, prueba.id, {p_numeros_1.id: "4", p_numeros_2.id: "6", p_geometria.id: "4"})  # 2/2 + 0/1
    _rendir(client, token, perfil_id, prueba.id, {p_numeros_1.id: "3", p_numeros_2.id: "5", p_geometria.id: "3"})  # 0/2 + 1/1

    r = client.get(f"/prediccion/{perfil_id}/mapa-calor", headers={"Authorization": f"Bearer {token}"})
    celdas = {c["eje_tematico"]: c for c in r.json()}

    assert celdas["Números"]["total_preguntas"] == 4  # 2 preguntas x 2 intentos
    assert celdas["Números"]["pct_correctas"] == 50.0  # 2/4 correctas en total
    assert celdas["Geometría"]["total_preguntas"] == 2
    assert celdas["Geometría"]["pct_correctas"] == 50.0  # 1/2 correctas en total


def test_mapa_calor_de_alumno_ajeno_da_403(client, session):
    nivel, asignatura, prueba, preguntas = _crear_contenido(session)
    _, perfil_id = _crear_apoderado_con_alumno(client, nivel)
    token_b, _ = _crear_apoderado_con_alumno(client, nivel)

    r = client.get(f"/prediccion/{perfil_id}/mapa-calor", headers={"Authorization": f"Bearer {token_b}"})
    assert r.status_code == 403


def test_mapa_calor_sin_sesion_da_401(client, session):
    nivel, asignatura, prueba, preguntas = _crear_contenido(session)
    _, perfil_id = _crear_apoderado_con_alumno(client, nivel)

    r = client.get(f"/prediccion/{perfil_id}/mapa-calor")
    assert r.status_code == 401
