"""Buzón de sugerencias (Fase 1 — ver planificacion/27-plan-incorporacion-hallazgos-brincus.md,
Paso 13, hallazgo comparando en vivo contra Brincus: "¿Cómo doy ideas para mejorar la
plataforma?")."""

from app.core.config import settings
from app.infrastructure.persistence.orm_models import Nivel

_CONTADOR_EMAILS = iter(range(1, 100_000))


def _preparar(client, session):
    nivel = Nivel(
        nombre="4° básico", regimen="A", decreto="439/2012", formato_examen="integrado",
        num_preguntas_examen=20, duracion_examen_min=90,
    )
    session.add(nivel)
    session.commit()
    session.refresh(nivel)

    email = f"apoderado.sugerencia.{next(_CONTADOR_EMAILS)}@test.cl"
    token = client.post(
        "/auth/registro", json={"email": email, "password": "ClaveSegura123", "nombre": "Apoderado Test"}
    ).json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    perfil_id = client.post(
        "/auth/alumnos", headers=headers,
        json={"nombre": "Test", "apellidos": "Test", "fecha_nacimiento": "2016-01-01", "rut": "1-9", "nivel_id": nivel.id},
    ).json()["id"]

    return perfil_id, headers


def test_enviar_sugerencia(client, session):
    perfil_id, headers = _preparar(client, session)
    r = client.post(
        f"/sugerencias/{perfil_id}", headers=headers, json={"texto": "Sería bueno tener un modo oscuro."},
    )
    assert r.status_code == 201
    assert r.json()["texto"] == "Sería bueno tener un modo oscuro."


def test_enviar_sugerencia_vacia_da_422(client, session):
    perfil_id, headers = _preparar(client, session)
    r = client.post(f"/sugerencias/{perfil_id}", headers=headers, json={"texto": "   "})
    assert r.status_code == 422


def test_listar_mis_sugerencias(client, session):
    perfil_id, headers = _preparar(client, session)
    client.post(f"/sugerencias/{perfil_id}", headers=headers, json={"texto": "Primera idea"})
    client.post(f"/sugerencias/{perfil_id}", headers=headers, json={"texto": "Segunda idea"})

    r = client.get(f"/sugerencias/{perfil_id}", headers=headers)
    assert r.status_code == 200
    textos = [s["texto"] for s in r.json()]
    assert textos == ["Segunda idea", "Primera idea"]  # más reciente primero


def test_sugerencia_de_alumno_ajeno_da_403(client, session):
    perfil_id, _ = _preparar(client, session)
    email_b = f"apoderado.sugerencia.ajeno.{next(_CONTADOR_EMAILS)}@test.cl"
    token_b = client.post(
        "/auth/registro", json={"email": email_b, "password": "ClaveSegura123", "nombre": "Otro"}
    ).json()["access_token"]
    headers_b = {"Authorization": f"Bearer {token_b}"}
    r = client.post(f"/sugerencias/{perfil_id}", headers=headers_b, json={"texto": "Intento ajeno"})
    assert r.status_code == 403


def test_sugerencia_sin_sesion_da_401(client, session):
    perfil_id, _ = _preparar(client, session)
    r = client.post(f"/sugerencias/{perfil_id}", json={"texto": "Sin sesión"})
    assert r.status_code == 401


def test_sugerencia_con_payload_adversarial_se_guarda_como_texto_literal(client, session):
    """P0 del plan de pruebas exhaustivo (planificacion/28-plan-de-pruebas-exhaustivo.md):
    confirmar que un payload de XSS/inyección en un campo de texto libre no rompe nada — se
    guarda y se devuelve tal cual, como texto plano (SQLModel parametriza las consultas, no
    hay SQL crudo; el frontend interpola con `{{ }}`, que Angular escapa por defecto — la
    única excepción del proyecto es `contenido_guia`, que nunca recibe texto de usuario)."""
    perfil_id, headers = _preparar(client, session)
    payload = "<script>alert(1)</script>'; DROP TABLE sugerencia;--"
    r = client.post(f"/sugerencias/{perfil_id}", headers=headers, json={"texto": payload})
    assert r.status_code == 201
    assert r.json()["texto"] == payload

    r = client.get(f"/sugerencias/{perfil_id}", headers=headers)
    assert r.status_code == 200
    assert r.json()[0]["texto"] == payload  # se guardó literal, no se ejecutó ni se truncó


def test_sugerencia_da_429_al_pasar_el_limite_configurado(client, session):
    """Auditoría de seguridad (2026-08-17): sin límite, el buzón podía inundarse de spam
    en segundos — el `max_length=2000` ya existente evita un blob enorme por request, pero
    no la cantidad de requests."""
    perfil_id, headers = _preparar(client, session)

    limite = settings.limite_sugerencia_por_minuto
    for _ in range(limite):
        r = client.post(f"/sugerencias/{perfil_id}", headers=headers, json={"texto": "Idea válida"})
        assert r.status_code == 201

    r = client.post(f"/sugerencias/{perfil_id}", headers=headers, json={"texto": "Idea excedida"})
    assert r.status_code == 429
