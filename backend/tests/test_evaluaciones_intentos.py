from app.infrastructure.persistence.orm_models import Asignatura, ConjuntoEvaluacion, Nivel, Pregunta

_CONTADOR_EMAILS = iter(range(1, 100_000))


def _preparar(client, session):
    """Devuelve (conjunto, perfil, preguntas, headers) — `headers` trae el token real del
    Apoderado dueño de `perfil`, necesario desde que /evaluaciones/* exige sesión (bug de
    seguridad real: antes cualquiera sin login podía iniciar/responder/entregar la
    evaluación de cualquier alumno adivinando su id)."""
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

    email = f"apoderado.intentos.{next(_CONTADOR_EMAILS)}@test.cl"
    token = client.post(
        "/auth/registro", json={"email": email, "password": "ClaveSegura123", "nombre": "Apoderado Test"}
    ).json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    perfil_id = client.post(
        "/auth/alumnos", headers=headers,
        json={"nombre": "Test", "apellidos": "Test", "fecha_nacimiento": "2016-01-01", "rut": "1-9", "nivel_id": nivel.id},
    ).json()["id"]

    class _Perfil:
        id = perfil_id

    return conjunto, _Perfil(), (p1, p2, p3), headers


def test_ciclo_completo_iniciar_responder_entregar(client, session):
    conjunto, perfil, (p1, p2, p3), headers = _preparar(client, session)

    r = client.post(
        "/evaluaciones/intentos", headers=headers,
        json={"perfil_alumno_id": perfil.id, "conjunto_evaluacion_id": conjunto.id},
    )
    assert r.status_code == 201
    intento_id = r.json()["id"]
    assert r.json()["nota"] is None

    r = client.patch(
        f"/evaluaciones/intentos/{intento_id}/responder", headers=headers,
        json={"pregunta_id": p1.id, "respuesta": "4"},
    )
    assert r.status_code == 200
    assert r.json()["respuestas"] == {str(p1.id): "4"}

    client.patch(
        f"/evaluaciones/intentos/{intento_id}/responder", headers=headers,
        json={"pregunta_id": p2.id, "respuesta": "5"},
    )  # incorrecta

    r = client.post(f"/evaluaciones/intentos/{intento_id}/entregar", headers=headers)
    assert r.status_code == 200
    datos = r.json()
    # 1 de 2 preguntas autocorregibles correcta (la de desarrollo no cuenta)
    assert datos["puntaje"] == 1.0
    assert datos["nota"] == 3.5  # calcular_nota(1, 2): aprobación=1.2, nota=1+3*(1/1.2)=3.5
    assert datos["fecha_termino"] is not None


def test_entregar_es_idempotente(client, session):
    conjunto, perfil, (p1, p2, p3), headers = _preparar(client, session)
    r = client.post(
        "/evaluaciones/intentos", headers=headers,
        json={"perfil_alumno_id": perfil.id, "conjunto_evaluacion_id": conjunto.id},
    )
    intento_id = r.json()["id"]
    client.patch(
        f"/evaluaciones/intentos/{intento_id}/responder", headers=headers,
        json={"pregunta_id": p1.id, "respuesta": "4"},
    )

    primera = client.post(f"/evaluaciones/intentos/{intento_id}/entregar", headers=headers).json()
    segunda = client.post(f"/evaluaciones/intentos/{intento_id}/entregar", headers=headers).json()
    assert primera == segunda


def test_iniciar_dos_veces_reanuda_el_mismo_intento(client, session):
    conjunto, perfil, _, headers = _preparar(client, session)
    r1 = client.post(
        "/evaluaciones/intentos", headers=headers,
        json={"perfil_alumno_id": perfil.id, "conjunto_evaluacion_id": conjunto.id},
    )
    r2 = client.post(
        "/evaluaciones/intentos", headers=headers,
        json={"perfil_alumno_id": perfil.id, "conjunto_evaluacion_id": conjunto.id},
    )
    assert r1.json()["id"] == r2.json()["id"]


def test_no_se_puede_responder_un_intento_ya_entregado(client, session):
    conjunto, perfil, (p1, _, _), headers = _preparar(client, session)
    r = client.post(
        "/evaluaciones/intentos", headers=headers,
        json={"perfil_alumno_id": perfil.id, "conjunto_evaluacion_id": conjunto.id},
    )
    intento_id = r.json()["id"]
    client.post(f"/evaluaciones/intentos/{intento_id}/entregar", headers=headers)

    r = client.patch(
        f"/evaluaciones/intentos/{intento_id}/responder", headers=headers,
        json={"pregunta_id": p1.id, "respuesta": "4"},
    )
    assert r.status_code == 400


def test_iniciar_intento_con_conjunto_inexistente_da_404(client, session):
    _, perfil, _, headers = _preparar(client, session)
    r = client.post(
        "/evaluaciones/intentos", headers=headers,
        json={"perfil_alumno_id": perfil.id, "conjunto_evaluacion_id": 99999},
    )
    assert r.status_code == 404


def test_obtener_intento_inexistente_da_404(client, session):
    _, _, _, headers = _preparar(client, session)
    r = client.get("/evaluaciones/intentos/99999", headers=headers)
    assert r.status_code == 404


def test_obtener_conjunto_inexistente_da_404(client, session):
    r = client.get("/evaluaciones/conjuntos/99999")
    assert r.status_code == 404


def test_iniciar_intento_con_perfil_inexistente_da_404(client, session):
    conjunto, _, _, headers = _preparar(client, session)
    r = client.post(
        "/evaluaciones/intentos", headers=headers,
        json={"perfil_alumno_id": 99999, "conjunto_evaluacion_id": conjunto.id},
    )
    assert r.status_code == 404


def test_no_se_puede_iniciar_intento_de_un_alumno_ajeno(client, session):
    # Bug de seguridad real encontrado con una matriz de permisos automática (2026-08-14):
    # /evaluaciones/* no exigía sesión — cualquiera podía iniciar/responder/entregar la
    # evaluación de cualquier alumno adivinando su id. Ahora exige que el perfil pertenezca
    # a la cuenta autenticada.
    conjunto, perfil_de_otro, _, _ = _preparar(client, session)

    token_ajeno = client.post(
        "/auth/registro", json={"email": "ajeno@test.cl", "password": "ClaveSegura123", "nombre": "Ajeno"}
    ).json()["access_token"]
    headers_ajenos = {"Authorization": f"Bearer {token_ajeno}"}

    r = client.post(
        "/evaluaciones/intentos", headers=headers_ajenos,
        json={"perfil_alumno_id": perfil_de_otro.id, "conjunto_evaluacion_id": conjunto.id},
    )
    assert r.status_code == 403


def test_evaluaciones_sin_sesion_da_401(client, session):
    conjunto, perfil, _, headers = _preparar(client, session)
    r = client.post(
        "/evaluaciones/intentos",
        json={"perfil_alumno_id": perfil.id, "conjunto_evaluacion_id": conjunto.id},
    )
    assert r.status_code in (401, 403)


def test_iniciar_intento_concurrente_no_crea_duplicados(client, session):
    # Bug real encontrado con un test de concurrencia contra el servidor real: 10
    # requests simultáneos a "iniciar intento" (ej. doble clic, dos pestañas cargando a
    # la vez) creaban hasta 3 intentos activos distintos para la misma prueba, en vez de
    # reanudar el mismo. Corregido con un índice único parcial en la BD + manejo de la
    # condición de carrera en el repositorio (ver IntentoEvaluacion.__table_args__).
    #
    # La sesión de SQLAlchemy no es thread-safe, así que este test no puede reusar la
    # sesión compartida del fixture `client`/`session` (usada para aislar tests por
    # transacción) — necesita una sesión nueva por hilo, igual que en producción real.
    import threading

    from sqlmodel import Session as SQLSession, create_engine

    from app.infrastructure.persistence.db import get_session
    from app.main import app

    conjunto, perfil, _, headers = _preparar(client, session)
    # Misma URL que tests/conftest.py::TEST_DATABASE_URL — se repite acá porque "tests"
    # no es un paquete importable (sin __init__.py) en esta configuración de pytest.
    engine_hilos = create_engine("postgresql://logos_dev:logos_dev_local@localhost:5432/logos_test")

    def _sesion_fresca_por_llamada():
        with SQLSession(engine_hilos) as s:
            yield s

    app.dependency_overrides[get_session] = _sesion_fresca_por_llamada
    try:
        resultados: list[int] = []
        barrera = threading.Barrier(10)

        def iniciar():
            barrera.wait()  # todos los hilos disparan el request lo más juntos posible
            r = client.post(
                "/evaluaciones/intentos", headers=headers,
                json={"perfil_alumno_id": perfil.id, "conjunto_evaluacion_id": conjunto.id},
            )
            resultados.append(r.json()["id"])

        hilos = [threading.Thread(target=iniciar) for _ in range(10)]
        for h in hilos:
            h.start()
        for h in hilos:
            h.join()

        assert len(set(resultados)) == 1
    finally:
        app.dependency_overrides[get_session] = lambda: (yield session)


def test_conjunto_no_expone_respuesta_correcta(client, session):
    conjunto, _, _, _ = _preparar(client, session)
    r = client.get(f"/evaluaciones/conjuntos/{conjunto.id}")
    assert r.status_code == 200
    for p in r.json()["preguntas"]:
        assert "respuesta_correcta" not in p


def test_conjunto_sin_perfil_alumno_id_devuelve_orden_original(client, session):
    conjunto, _, (p1, p2, p3), _ = _preparar(client, session)
    r = client.get(f"/evaluaciones/conjuntos/{conjunto.id}")
    assert [p["id"] for p in r.json()["preguntas"]] == [p1.id, p2.id, p3.id]


def test_conjunto_con_perfil_alumno_id_es_estable_entre_llamadas(client, session):
    conjunto, perfil, _, _ = _preparar(client, session)
    r1 = client.get(f"/evaluaciones/conjuntos/{conjunto.id}", params={"perfil_alumno_id": perfil.id})
    r2 = client.get(f"/evaluaciones/conjuntos/{conjunto.id}", params={"perfil_alumno_id": perfil.id})
    orden1 = [p["id"] for p in r1.json()["preguntas"]]
    orden2 = [p["id"] for p in r2.json()["preguntas"]]
    assert orden1 == orden2  # mismo alumno, mismo conjunto → mismo orden en cada carga/recarga


def test_conjunto_con_perfil_alumno_id_conserva_todas_las_preguntas(client, session):
    conjunto, perfil, (p1, p2, p3), _ = _preparar(client, session)
    r = client.get(f"/evaluaciones/conjuntos/{conjunto.id}", params={"perfil_alumno_id": perfil.id})
    orden = [p["id"] for p in r.json()["preguntas"]]
    assert sorted(orden) == sorted([p1.id, p2.id, p3.id])


def test_responder_con_texto_demasiado_largo_da_422(client, session):
    """Auditoría de seguridad (Fase 1, ver
    planificacion/27-plan-incorporacion-hallazgos-brincus.md): sin límite, un request
    directo a la API (sin pasar por el frontend) podía guardar una respuesta de
    desarrollo de tamaño arbitrario."""
    conjunto, perfil, (p1, p2, p3), headers = _preparar(client, session)
    intento_id = client.post(
        "/evaluaciones/intentos", headers=headers,
        json={"perfil_alumno_id": perfil.id, "conjunto_evaluacion_id": conjunto.id},
    ).json()["id"]
    r = client.patch(
        f"/evaluaciones/intentos/{intento_id}/responder", headers=headers,
        json={"pregunta_id": p3.id, "respuesta": "x" * 4001},
    )
    assert r.status_code == 422


def test_listar_conjuntos_de_asignatura_sin_perfil_no_trae_historial(client, session):
    """Comparado en vivo contra Brincus (que muestra "Ver intentos" junto a cada
    cuestionario del temario, sin obligar al alumno a ir a una sección de notas aparte):
    sin `perfil_alumno_id`, la lista de pruebas/exámenes sigue funcionando igual que
    antes (retrocompatible), solo que sin datos de historial."""
    conjunto, _, _, headers = _preparar(client, session)
    r = client.get(f"/evaluaciones/conjuntos/asignatura/{conjunto.asignatura_id}", headers=headers)
    assert r.status_code == 200
    fila = next(c for c in r.json() if c["id"] == conjunto.id)
    assert fila["intentos_entregados"] == 0
    assert fila["ultima_nota"] is None


def test_listar_conjuntos_de_asignatura_con_perfil_trae_la_ultima_nota(client, session):
    conjunto, perfil, (p1, p2, p3), headers = _preparar(client, session)
    intento_id = client.post(
        "/evaluaciones/intentos", headers=headers,
        json={"perfil_alumno_id": perfil.id, "conjunto_evaluacion_id": conjunto.id},
    ).json()["id"]
    client.patch(
        f"/evaluaciones/intentos/{intento_id}/responder", headers=headers,
        json={"pregunta_id": p1.id, "respuesta": "4"},
    )
    client.post(f"/evaluaciones/intentos/{intento_id}/entregar", headers=headers)

    r = client.get(
        f"/evaluaciones/conjuntos/asignatura/{conjunto.asignatura_id}",
        params={"perfil_alumno_id": perfil.id}, headers=headers,
    )
    assert r.status_code == 200
    fila = next(c for c in r.json() if c["id"] == conjunto.id)
    assert fila["intentos_entregados"] == 1
    assert fila["ultima_nota"] is not None


def test_listar_conjuntos_de_asignatura_con_perfil_ajeno_da_403(client, session):
    """Mismo bug de seguridad que ya se corrigió en otros endpoints (ej.
    reportar-error): sin verificar dueño, cualquiera con sesión podía leer la nota de un
    alumno ajeno con solo adivinar su perfil_alumno_id."""
    conjunto, _, _, headers = _preparar(client, session)
    email_b = f"apoderado.intentos.ajeno.{next(_CONTADOR_EMAILS)}@test.cl"
    token_b = client.post(
        "/auth/registro", json={"email": email_b, "password": "ClaveSegura123", "nombre": "Otro"}
    ).json()["access_token"]
    headers_b = {"Authorization": f"Bearer {token_b}"}
    perfil_b_id = client.post(
        "/auth/alumnos", headers=headers_b,
        json={"nombre": "Otro", "apellidos": "Alumno", "fecha_nacimiento": "2016-01-01", "rut": "2-7", "nivel_id": 1},
    ).json()["id"]

    r = client.get(
        f"/evaluaciones/conjuntos/asignatura/{conjunto.asignatura_id}",
        params={"perfil_alumno_id": perfil_b_id}, headers=headers,
    )
    assert r.status_code == 403


def test_listar_conjuntos_de_asignatura_sin_sesion_da_401(client, session):
    conjunto, _, _, _ = _preparar(client, session)
    r = client.get(f"/evaluaciones/conjuntos/asignatura/{conjunto.asignatura_id}")
    assert r.status_code == 401
