"""Fase 1, ítem 2.2 del plan de incorporación de hallazgos de Brincus — gamificación
(XP, nivel, avatar). Ver planificacion/27-plan-incorporacion-hallazgos-brincus.md."""

from datetime import datetime, timedelta, timezone

from app.infrastructure.persistence.orm_models import (
    Asignatura,
    ConjuntoEvaluacion,
    IntentoEvaluacion,
    Nivel,
    ObjetivoAprendizaje,
    Pregunta,
)

_CONTADOR_EMAILS = iter(range(1, 100_000))


def _preparar(client, session):
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

    oa = ObjetivoAprendizaje(asignatura_id=asignatura.id, codigo_oficial="MA04OA01", descripcion="Contar")
    session.add(oa)
    session.commit()
    session.refresh(oa)

    p1 = Pregunta(asignatura_id=asignatura.id, oa_id=oa.id, tipo="alternativas", enunciado="2+2?", opciones=["3", "4"], respuesta_correcta="4")
    session.add(p1)
    session.commit()
    session.refresh(p1)

    conjunto = ConjuntoEvaluacion(tipo="prueba_unidad", asignatura_id=asignatura.id, nombre="Prueba", pregunta_ids=[p1.id])
    session.add(conjunto)
    session.commit()
    session.refresh(conjunto)

    email = f"apoderado.gamif.{next(_CONTADOR_EMAILS)}@test.cl"
    token = client.post(
        "/auth/registro", json={"email": email, "password": "ClaveSegura123", "nombre": "Apoderado Test"}
    ).json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    perfil_id = client.post(
        "/auth/alumnos", headers=headers,
        json={"nombre": "Test", "apellidos": "Test", "fecha_nacimiento": "2016-01-01", "rut": "1-9", "nivel_id": nivel.id},
    ).json()["id"]

    return oa, conjunto, perfil_id, headers


def test_perfil_gamificacion_nace_en_0_xp_nivel_1(client, session):
    _, _, perfil_id, headers = _preparar(client, session)
    r = client.get(f"/gamificacion/{perfil_id}", headers=headers)
    assert r.status_code == 200
    body = r.json()
    assert body["xp"] == 0
    assert body["nivel"] == 1
    assert body["avatar_id"] == "monstruo_azul"
    assert len(body["avatares_disponibles"]) >= 5


def test_entregar_un_intento_da_xp(client, session):
    oa, conjunto, perfil_id, headers = _preparar(client, session)
    intento_id = client.post(
        "/evaluaciones/intentos", headers=headers,
        json={"perfil_alumno_id": perfil_id, "conjunto_evaluacion_id": conjunto.id},
    ).json()["id"]
    client.post(f"/evaluaciones/intentos/{intento_id}/entregar", headers=headers)

    r = client.get(f"/gamificacion/{perfil_id}", headers=headers)
    assert r.json()["xp"] == 5


def test_entregar_dos_veces_el_mismo_intento_no_duplica_el_xp(client, session):
    """`EntregarIntento` ya es idempotente — la gamificación no debe premiar dos veces."""
    oa, conjunto, perfil_id, headers = _preparar(client, session)
    intento_id = client.post(
        "/evaluaciones/intentos", headers=headers,
        json={"perfil_alumno_id": perfil_id, "conjunto_evaluacion_id": conjunto.id},
    ).json()["id"]
    client.post(f"/evaluaciones/intentos/{intento_id}/entregar", headers=headers)
    client.post(f"/evaluaciones/intentos/{intento_id}/entregar", headers=headers)  # de nuevo

    r = client.get(f"/gamificacion/{perfil_id}", headers=headers)
    assert r.json()["xp"] == 5


def test_revisar_una_guia_da_xp_solo_la_primera_vez(client, session):
    oa, _, perfil_id, headers = _preparar(client, session)
    client.post(f"/progreso/{perfil_id}/guias/{oa.id}/revisada", headers=headers)
    client.post(f"/progreso/{perfil_id}/guias/{oa.id}/revisada", headers=headers)  # de nuevo, misma guía

    r = client.get(f"/gamificacion/{perfil_id}", headers=headers)
    assert r.json()["xp"] == 2


def test_50_xp_sube_a_nivel_2(client, session):
    oa, _, perfil_id, headers = _preparar(client, session)
    asignatura_id = oa.asignatura_id

    # 10 entregas x 5 XP = 50 XP — cada una en su propio conjunto (una pregunta cada
    # uno) para que sean 10 intentos distintos, no el mismo reanudado.
    for _ in range(10):
        pregunta = Pregunta(
            asignatura_id=asignatura_id, oa_id=oa.id, tipo="alternativas",
            enunciado="1+1?", opciones=["1", "2"], respuesta_correcta="2",
        )
        session.add(pregunta)
        session.commit()
        session.refresh(pregunta)

        conjunto = ConjuntoEvaluacion(
            tipo="prueba_unidad", asignatura_id=asignatura_id, nombre="Prueba",
            pregunta_ids=[pregunta.id],
        )
        session.add(conjunto)
        session.commit()
        session.refresh(conjunto)

        intento_id = client.post(
            "/evaluaciones/intentos", headers=headers,
            json={"perfil_alumno_id": perfil_id, "conjunto_evaluacion_id": conjunto.id},
        ).json()["id"]
        client.post(f"/evaluaciones/intentos/{intento_id}/entregar", headers=headers)

    r = client.get(f"/gamificacion/{perfil_id}", headers=headers)
    assert r.json()["xp"] == 50
    assert r.json()["nivel"] == 2


def test_cambiar_avatar(client, session):
    _, _, perfil_id, headers = _preparar(client, session)
    r = client.patch(f"/gamificacion/{perfil_id}/avatar", headers=headers, json={"avatar_id": "cohete"})
    assert r.status_code == 200
    assert r.json()["avatar_id"] == "cohete"


def test_cambiar_a_avatar_invalido_da_400(client, session):
    _, _, perfil_id, headers = _preparar(client, session)
    r = client.patch(f"/gamificacion/{perfil_id}/avatar", headers=headers, json={"avatar_id": "no-existe"})
    assert r.status_code == 400


def test_gamificacion_de_alumno_ajeno_da_403(client, session):
    _, _, perfil_id, _ = _preparar(client, session)
    email_b = f"apoderado.gamif.ajeno.{next(_CONTADOR_EMAILS)}@test.cl"
    token_b = client.post(
        "/auth/registro", json={"email": email_b, "password": "ClaveSegura123", "nombre": "Otro"}
    ).json()["access_token"]
    headers_b = {"Authorization": f"Bearer {token_b}"}
    r = client.get(f"/gamificacion/{perfil_id}", headers=headers_b)
    assert r.status_code == 403


def test_gamificacion_sin_sesion_da_401(client, session):
    _, _, perfil_id, _ = _preparar(client, session)
    r = client.get(f"/gamificacion/{perfil_id}")
    assert r.status_code == 401


def test_perfil_expone_racha_y_catalogo_completo_de_logros(client, session):
    """Profundización de gamificación (2026-08-15, comparando en vivo contra Brincus —
    ver planificacion/25-analisis-competencia-brincus.md): el catálogo completo viaja
    siempre, con `desbloqueado` por ítem, para que el frontend pueda mostrar los logros
    bloqueados en gris (igual que hace Brincus), no solo los ya conseguidos."""
    oa, _, perfil_id, headers = _preparar(client, session)
    r = client.get(f"/gamificacion/{perfil_id}", headers=headers)
    body = r.json()
    assert body["racha_dias_actual"] == 0
    assert body["racha_dias_maxima"] == 0
    assert len(body["logros"]) == 15
    assert all(logro["desbloqueado"] is False for logro in body["logros"])

    client.post(f"/progreso/{perfil_id}/guias/{oa.id}/revisada", headers=headers)

    r = client.get(f"/gamificacion/{perfil_id}", headers=headers)
    body = r.json()
    assert body["racha_dias_actual"] == 1
    logro_guias_5 = next(l for l in body["logros"] if l["id"] == "guias_5")
    assert logro_guias_5["desbloqueado"] is False  # revisó 1, hacen falta 5


def test_entregar_un_intento_largo_desbloquea_logro_de_tiempo(client, session):
    """Fase 1, hallazgo comparando en vivo contra Brincus (Paso 12: logros por "tiempo
    total acumulado") — ver planificacion/27-plan-incorporacion-hallazgos-brincus.md. Se
    fuerza `fecha_inicio` al pasado para simular un intento real de 31 minutos, ya que
    `tiempo_usado_seg` se calcula a partir de fecha_inicio/fecha_termino reales."""
    oa, conjunto, perfil_id, headers = _preparar(client, session)
    intento_id = client.post(
        "/evaluaciones/intentos", headers=headers,
        json={"perfil_alumno_id": perfil_id, "conjunto_evaluacion_id": conjunto.id},
    ).json()["id"]

    intento_orm = session.get(IntentoEvaluacion, intento_id)
    intento_orm.fecha_inicio = datetime.now(timezone.utc).replace(tzinfo=None) - timedelta(minutes=31)
    session.add(intento_orm)
    session.commit()

    client.post(f"/evaluaciones/intentos/{intento_id}/entregar", headers=headers)

    r = client.get(f"/gamificacion/{perfil_id}", headers=headers)
    body = r.json()
    logro_tiempo = next(l for l in body["logros"] if l["id"] == "tiempo_30min")
    assert logro_tiempo["desbloqueado"] is True
    logro_tiempo_2h = next(l for l in body["logros"] if l["id"] == "tiempo_2h")
    assert logro_tiempo_2h["desbloqueado"] is False
