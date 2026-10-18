from app.infrastructure.persistence.orm_models import Asignatura, Nivel, ObjetivoAprendizaje, Pregunta


def _preparar_contenido(session, num_oa=4):
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

    oas = []
    for i in range(num_oa):
        oa = ObjetivoAprendizaje(asignatura_id=asignatura.id, codigo_oficial=f"OA {i+1}", descripcion=f"Objetivo {i+1}")
        session.add(oa)
        session.commit()
        session.refresh(oa)
        pregunta = Pregunta(
            oa_id=oa.id, asignatura_id=asignatura.id, tipo="alternativas",
            enunciado=f"Pregunta del OA {i+1}", opciones=["a", "b"], respuesta_correcta="a",
        )
        session.add(pregunta)
        session.commit()
        session.refresh(pregunta)
        oas.append((oa, pregunta))

    return nivel, asignatura, oas


def _crear_apoderado_con_alumno(client, nivel_id, email="familia.parcial@test.cl"):
    token = client.post(
        "/auth/registro", json={"email": email, "password": "ClaveSegura123", "nombre": "Apoderado Test"}
    ).json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    r = client.post(
        "/auth/alumnos", headers=headers,
        json={"nombre": "Sofía", "apellidos": "Pérez", "fecha_nacimiento": "2016-03-12", "rut": "21.345.678-4", "nivel_id": nivel_id},
    )
    return headers, r.json()["id"]


def _marcar_revisadas(client, headers, perfil_id, oas):
    for oa, _ in oas:
        client.post(f"/progreso/{perfil_id}/guias/{oa.id}/revisada", headers=headers)


def test_cobertura_insuficiente_rechaza_con_400(client, session):
    nivel, asignatura, oas = _preparar_contenido(session)
    headers, perfil_id = _crear_apoderado_con_alumno(client, nivel.id)

    r = client.post(f"/evaluaciones/simulacro-parcial/{asignatura.id}", json={"perfil_alumno_id": perfil_id}, headers=headers)
    assert r.status_code == 400


def test_asignatura_inexistente_da_404(client, session):
    nivel, asignatura, oas = _preparar_contenido(session)
    headers, perfil_id = _crear_apoderado_con_alumno(client, nivel.id)

    r = client.post("/evaluaciones/simulacro-parcial/9999", json={"perfil_alumno_id": perfil_id}, headers=headers)
    assert r.status_code == 404


def test_cobertura_suficiente_genera_y_permite_rendir_ciclo_completo(client, session):
    nivel, asignatura, oas = _preparar_contenido(session, num_oa=4)
    headers, perfil_id = _crear_apoderado_con_alumno(client, nivel.id)
    # Revisa 2 de 4 OA (50%, cumple el umbral).
    _marcar_revisadas(client, headers, perfil_id, oas[:2])

    r = client.post(f"/evaluaciones/simulacro-parcial/{asignatura.id}", json={"perfil_alumno_id": perfil_id}, headers=headers)
    assert r.status_code == 201
    datos = r.json()
    assert datos["nota"] is None
    intento_id = datos["id"]

    pregunta_cubierta = oas[0][1]
    client.patch(
        f"/evaluaciones/intentos/{intento_id}/responder",
        json={"pregunta_id": pregunta_cubierta.id, "respuesta": "a"},
        headers=headers,
    )

    r = client.post(f"/evaluaciones/intentos/{intento_id}/entregar", headers=headers)
    assert r.status_code == 200
    assert r.json()["nota"] is not None


def test_cobertura_justo_bajo_el_umbral_sigue_rechazando(client, session):
    """P2 del plan de pruebas exhaustivo (planificacion/28-plan-de-pruebas-exhaustivo.md):
    el umbral es `cobertura >= UMBRAL_SIMULACRO_PARCIAL` (0.5) — ya había un caso en exactamente
    50% (`test_cobertura_suficiente_genera_y_permite_rendir_ciclo_completo`, 2/4), pero nunca
    se había probado el borde justo por DEBAJO del umbral, donde un `>` en vez de `>=` (o un
    error de redondeo) recién se notaría. Con 100 OA, 49/100 = 49% debe seguir rechazando."""
    nivel, asignatura, oas = _preparar_contenido(session, num_oa=100)
    headers, perfil_id = _crear_apoderado_con_alumno(client, nivel.id)
    _marcar_revisadas(client, headers, perfil_id, oas[:49])  # 49% — justo bajo el 50%

    r = client.post(f"/evaluaciones/simulacro-parcial/{asignatura.id}", json={"perfil_alumno_id": perfil_id}, headers=headers)
    assert r.status_code == 400


def test_simulacro_parcial_no_incluye_preguntas_de_oa_no_cubiertas(client, session):
    nivel, asignatura, oas = _preparar_contenido(session, num_oa=4)
    headers, perfil_id = _crear_apoderado_con_alumno(client, nivel.id)
    _marcar_revisadas(client, headers, perfil_id, oas[:2])  # solo los 2 primeros OA

    r = client.post(f"/evaluaciones/simulacro-parcial/{asignatura.id}", json={"perfil_alumno_id": perfil_id}, headers=headers)
    conjunto_id = r.json()["conjunto_evaluacion_id"]

    detalle = client.get(f"/evaluaciones/conjuntos/{conjunto_id}", headers=headers).json()
    ids_preguntas_conjunto = {p["id"] for p in detalle["preguntas"]}
    ids_preguntas_no_cubiertas = {oas[2][1].id, oas[3][1].id}
    assert ids_preguntas_conjunto.isdisjoint(ids_preguntas_no_cubiertas)
