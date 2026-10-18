"""Nota estimada del Examen Libre — idea propia (no un hallazgo de Brincus, ver
`app/application/prediccion/consultas.py`). Reutiliza el mismo patrón de fixtures que
`test_progreso.py`."""

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
    session.add(oa)
    session.commit()
    session.refresh(oa)

    p1 = Pregunta(asignatura_id=asignatura.id, oa_id=oa.id, tipo="alternativas", enunciado="2+2?", opciones=["3", "4"], respuesta_correcta="4")
    p2 = Pregunta(asignatura_id=asignatura.id, oa_id=oa.id, tipo="alternativas", enunciado="3+3?", opciones=["5", "6"], respuesta_correcta="6")
    session.add(p1); session.add(p2)
    session.commit()
    session.refresh(p1); session.refresh(p2)

    prueba = ConjuntoEvaluacion(
        tipo="prueba_unidad", asignatura_id=asignatura.id, nombre="Prueba de unidad 1",
        pregunta_ids=[p1.id, p2.id],
    )
    examen = ConjuntoEvaluacion(
        tipo="examen_simulacro", asignatura_id=asignatura.id, nombre="Examen simulacro Forma A",
        pregunta_ids=[p1.id, p2.id], tiempo_sugerido_min=60,
    )
    session.add(prueba); session.add(examen)
    session.commit()
    session.refresh(prueba); session.refresh(examen)

    return nivel, asignatura, oa, prueba, examen, (p1, p2)


def _crear_apoderado_con_alumno(client, nivel):
    n = next(_CONTADOR_EMAILS)
    email = f"apoderado.prediccion.{n}@test.cl"
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


def test_sin_ninguna_evaluacion_da_sin_datos(client, session):
    nivel, asignatura, oa, prueba, examen, (p1, p2) = _crear_contenido(session)
    token, perfil_id = _crear_apoderado_con_alumno(client, nivel)

    r = client.get(
        f"/prediccion/{perfil_id}/nota-estimada", params={"nivel_id": nivel.id},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert r.status_code == 200
    datos = r.json()
    assert datos["nota_general_estimada"] is None
    assert datos["confianza_general"] == "sin_datos"
    assert datos["por_asignatura"][0]["confianza"] == "sin_datos"
    assert datos["por_asignatura"][0]["cobertura_pct"] == 0.0


def test_solo_nota_de_practica_da_confianza_baja(client, session):
    nivel, asignatura, oa, prueba, examen, (p1, p2) = _crear_contenido(session)
    token, perfil_id = _crear_apoderado_con_alumno(client, nivel)

    _rendir(client, token, perfil_id, prueba.id, {p1.id: "4", p2.id: "6"})  # 2/2 -> nota 7.0

    r = client.get(
        f"/prediccion/{perfil_id}/nota-estimada", params={"nivel_id": nivel.id},
        headers={"Authorization": f"Bearer {token}"},
    )
    datos = r.json()
    asignatura_resp = datos["por_asignatura"][0]
    assert asignatura_resp["nota_estimada"] == 7.0
    assert asignatura_resp["confianza"] == "baja"
    assert datos["nota_general_estimada"] == 7.0
    assert datos["confianza_general"] == "baja"


def test_practica_y_simulacro_con_cobertura_alta_da_confianza_alta(client, session):
    nivel, asignatura, oa, prueba, examen, (p1, p2) = _crear_contenido(session)
    token, perfil_id = _crear_apoderado_con_alumno(client, nivel)
    headers = {"Authorization": f"Bearer {token}"}

    client.post(f"/progreso/{perfil_id}/guias/{oa.id}/revisada", headers=headers)  # 100% cobertura (1/1 OA)
    _rendir(client, token, perfil_id, prueba.id, {p1.id: "4", p2.id: "6"})  # práctica 7.0
    _rendir(client, token, perfil_id, examen.id, {p1.id: "4", p2.id: "6"})  # simulacro 7.0

    r = client.get(
        f"/prediccion/{perfil_id}/nota-estimada", params={"nivel_id": nivel.id}, headers=headers,
    )
    datos = r.json()
    asignatura_resp = datos["por_asignatura"][0]
    assert asignatura_resp["nota_estimada"] == 7.0  # 0.65*7 + 0.35*7
    assert asignatura_resp["confianza"] == "alta"
    assert asignatura_resp["cobertura_pct"] == 100.0
    assert datos["nota_general_estimada"] == 7.0
    assert datos["confianza_general"] == "alta"


def test_solo_simulacro_con_cobertura_baja_da_confianza_baja(client, session):
    nivel, asignatura, oa, prueba, examen, (p1, p2) = _crear_contenido(session)
    token, perfil_id = _crear_apoderado_con_alumno(client, nivel)
    headers = {"Authorization": f"Bearer {token}"}

    # No se revisa ninguna guía -> cobertura 0% (< 50, el umbral medio).
    _rendir(client, token, perfil_id, examen.id, {p1.id: "4", p2.id: "6"})

    r = client.get(f"/prediccion/{perfil_id}/nota-estimada", params={"nivel_id": nivel.id}, headers=headers)
    datos = r.json()
    asignatura_resp = datos["por_asignatura"][0]
    assert asignatura_resp["nota_estimada"] == 7.0
    assert asignatura_resp["confianza"] == "baja"


def test_prediccion_de_alumno_ajeno_da_403(client, session):
    nivel, asignatura, oa, prueba, examen, (p1, p2) = _crear_contenido(session)
    _, perfil_id = _crear_apoderado_con_alumno(client, nivel)
    token_b, _ = _crear_apoderado_con_alumno(client, nivel)

    r = client.get(
        f"/prediccion/{perfil_id}/nota-estimada", params={"nivel_id": nivel.id},
        headers={"Authorization": f"Bearer {token_b}"},
    )
    assert r.status_code == 403


def test_prediccion_sin_sesion_da_401(client, session):
    nivel, asignatura, oa, prueba, examen, (p1, p2) = _crear_contenido(session)
    _, perfil_id = _crear_apoderado_con_alumno(client, nivel)

    r = client.get(f"/prediccion/{perfil_id}/nota-estimada", params={"nivel_id": nivel.id})
    assert r.status_code == 401
