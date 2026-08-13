from datetime import date

from app.infrastructure.persistence.orm_models import Asignatura, ConjuntoEvaluacion, Nivel, Pregunta


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

    p1 = Pregunta(asignatura_id=asignatura.id, tipo="alternativas", enunciado="2+2?", opciones=["3", "4"], respuesta_correcta="4")
    p2 = Pregunta(asignatura_id=asignatura.id, tipo="alternativas", enunciado="3+3?", opciones=["5", "6"], respuesta_correcta="6")
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

    return nivel, asignatura, prueba, examen, (p1, p2)


def _crear_apoderado_con_alumno(client, session, nivel, email="familia.progreso@test.cl"):
    token = client.post(
        "/auth/registro",
        json={"email": email, "password": "ClaveSegura123", "nombre": "Apoderado Test"},
    ).json()["access_token"]

    r = client.post(
        "/auth/alumnos",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "nombre": "Sofía", "apellidos": "Pérez",
            "fecha_nacimiento": "2016-03-12", "rut": "21.345.678-4", "nivel_id": nivel.id,
        },
    )
    perfil_id = r.json()["id"]
    return token, perfil_id


def _rendir(client, token, perfil_id, conjunto_id, respuestas: dict[int, str]):
    headers = {"Authorization": f"Bearer {token}"}
    r = client.post(
        "/evaluaciones/intentos",
        json={"perfil_alumno_id": perfil_id, "conjunto_evaluacion_id": conjunto_id},
    )
    intento_id = r.json()["id"]
    for pregunta_id, respuesta in respuestas.items():
        client.patch(
            f"/evaluaciones/intentos/{intento_id}/responder",
            json={"pregunta_id": pregunta_id, "respuesta": respuesta},
        )
    return client.post(f"/evaluaciones/intentos/{intento_id}/entregar").json()


def test_historial_incluye_pruebas_examenes_y_separa_notas_por_tipo(client, session):
    nivel, asignatura, prueba, examen, (p1, p2) = _crear_contenido(session)
    token, perfil_id = _crear_apoderado_con_alumno(client, session, nivel)
    headers = {"Authorization": f"Bearer {token}"}

    _rendir(client, token, perfil_id, prueba.id, {p1.id: "4", p2.id: "5"})  # 1/2 correcta
    _rendir(client, token, perfil_id, examen.id, {p1.id: "4", p2.id: "6"})  # 2/2 correcta

    r = client.get(f"/progreso/{perfil_id}", headers=headers)
    assert r.status_code == 200
    datos = r.json()

    assert len(datos["historial"]) == 2
    tipos = {item["tipo"] for item in datos["historial"]}
    assert tipos == {"prueba_unidad", "examen_simulacro"}

    assert len(datos["notas_por_asignatura"]) == 1
    nota_asignatura = datos["notas_por_asignatura"][0]
    assert nota_asignatura["asignatura_id"] == asignatura.id
    assert nota_asignatura["nota_practica"] == 3.5  # calcular_nota(1, 2)
    assert nota_asignatura["nota_simulacro"] == 7.0  # calcular_nota(2, 2)


def test_marcar_guia_revisada_aparece_en_el_historial(client, session):
    nivel, asignatura, prueba, examen, (p1, p2) = _crear_contenido(session)
    from app.infrastructure.persistence.orm_models import ObjetivoAprendizaje

    oa = ObjetivoAprendizaje(asignatura_id=asignatura.id, codigo_oficial="OA 1", descripcion="Suma")
    session.add(oa)
    session.commit()
    session.refresh(oa)

    token, perfil_id = _crear_apoderado_con_alumno(client, session, nivel)
    headers = {"Authorization": f"Bearer {token}"}

    r = client.post(f"/progreso/{perfil_id}/guias/{oa.id}/revisada", headers=headers)
    assert r.status_code == 204

    r = client.get(f"/progreso/{perfil_id}", headers=headers)
    assert len(r.json()["guias_revisadas"]) == 1
    assert r.json()["guias_revisadas"][0]["oa_id"] == oa.id


def test_marcar_guia_revisada_dos_veces_no_duplica(client, session):
    nivel, asignatura, *_ = _crear_contenido(session)
    from app.infrastructure.persistence.orm_models import ObjetivoAprendizaje

    oa = ObjetivoAprendizaje(asignatura_id=asignatura.id, codigo_oficial="OA 1", descripcion="Suma")
    session.add(oa)
    session.commit()
    session.refresh(oa)

    token, perfil_id = _crear_apoderado_con_alumno(client, session, nivel)
    headers = {"Authorization": f"Bearer {token}"}

    client.post(f"/progreso/{perfil_id}/guias/{oa.id}/revisada", headers=headers)
    client.post(f"/progreso/{perfil_id}/guias/{oa.id}/revisada", headers=headers)

    r = client.get(f"/progreso/{perfil_id}", headers=headers)
    assert len(r.json()["guias_revisadas"]) == 1


def test_un_apoderado_no_puede_ver_el_progreso_de_un_perfil_ajeno(client, session):
    nivel, *_ = _crear_contenido(session)
    _, perfil_id_de_a = _crear_apoderado_con_alumno(client, session, nivel, email="a@test.cl")
    token_b, _ = _crear_apoderado_con_alumno(client, session, nivel, email="b@test.cl")

    r = client.get(f"/progreso/{perfil_id_de_a}", headers={"Authorization": f"Bearer {token_b}"})
    assert r.status_code == 403


def test_progreso_sin_evaluaciones_ni_guias_devuelve_listas_vacias(client, session):
    nivel, *_ = _crear_contenido(session)
    token, perfil_id = _crear_apoderado_con_alumno(client, session, nivel)

    r = client.get(f"/progreso/{perfil_id}", headers={"Authorization": f"Bearer {token}"})
    assert r.status_code == 200
    assert r.json() == {"historial": [], "guias_revisadas": [], "notas_por_asignatura": []}


def test_faltantes_sin_guias_revisadas_prueba_esta_habilitada_y_examen_no(client, session):
    from app.infrastructure.persistence.orm_models import ObjetivoAprendizaje

    nivel, asignatura, prueba, examen, (p1, p2) = _crear_contenido(session)
    # p1/p2 no tienen oa_id en _crear_contenido — sin OA que cubrir, la prueba de unidad
    # queda habilitada por defecto (no hay nada que bloquee su desbloqueo).
    session.add(ObjetivoAprendizaje(asignatura_id=asignatura.id, codigo_oficial="OA 1", descripcion="Suma"))
    session.commit()

    token, perfil_id = _crear_apoderado_con_alumno(client, session, nivel)
    headers = {"Authorization": f"Bearer {token}"}

    r = client.get(f"/progreso/{perfil_id}/faltantes", params={"nivel_id": nivel.id}, headers=headers)
    assert r.status_code == 200
    datos = r.json()

    tipos_habilitados = {f["tipo"]: f["habilitado"] for f in datos["faltantes"]}
    assert tipos_habilitados["prueba_unidad"] is True  # sin OA vinculadas, no bloquea
    assert tipos_habilitados["examen_simulacro"] is False  # 0% de cobertura

    cobertura = datos["coberturas"][0]
    assert cobertura["cobertura_pct"] == 0.0
    assert cobertura["simulacro_parcial_disponible"] is False


def test_faltantes_examen_se_habilita_al_100_por_ciento_de_cobertura(client, session):
    from app.infrastructure.persistence.orm_models import ObjetivoAprendizaje

    nivel, asignatura, prueba, examen, (p1, p2) = _crear_contenido(session)
    oa = ObjetivoAprendizaje(asignatura_id=asignatura.id, codigo_oficial="OA 1", descripcion="Suma")
    session.add(oa)
    session.commit()
    session.refresh(oa)

    token, perfil_id = _crear_apoderado_con_alumno(client, session, nivel)
    headers = {"Authorization": f"Bearer {token}"}

    client.post(f"/progreso/{perfil_id}/guias/{oa.id}/revisada", headers=headers)

    r = client.get(f"/progreso/{perfil_id}/faltantes", params={"nivel_id": nivel.id}, headers=headers)
    datos = r.json()
    tipos_habilitados = {f["tipo"]: f["habilitado"] for f in datos["faltantes"]}
    assert tipos_habilitados["examen_simulacro"] is True  # 100% de cobertura (1/1 OA)
    assert datos["coberturas"][0]["simulacro_parcial_disponible"] is True


def test_faltantes_no_incluye_conjuntos_ya_entregados(client, session):
    nivel, asignatura, prueba, examen, (p1, p2) = _crear_contenido(session)
    token, perfil_id = _crear_apoderado_con_alumno(client, session, nivel)
    headers = {"Authorization": f"Bearer {token}"}

    _rendir(client, token, perfil_id, prueba.id, {p1.id: "4"})

    r = client.get(f"/progreso/{perfil_id}/faltantes", params={"nivel_id": nivel.id}, headers=headers)
    conjuntos_faltantes = {f["conjunto_id"] for f in r.json()["faltantes"]}
    assert prueba.id not in conjuntos_faltantes
    assert examen.id in conjuntos_faltantes
