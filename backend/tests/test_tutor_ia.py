"""Profesor IA (tarea 14, 2026-11-18): se prueba con un tutor falso; nunca se llama a la API real."""
import pytest

from app.core.config import settings
from app.domain.tutor_ia.ports import RespuestaTutor, TutorNoDisponible
from app.domain.tutor_ia.salvaguardas import anonimizar, senal_de_crisis
from app.infrastructure.persistence.orm_models import Asignatura, Nivel, ObjetivoAprendizaje
from app.main import app
from app.routers import tutor_ia

_N = iter(range(1, 100_000))


class TutorFalso:
    def __init__(self, falla=False):
        self.llamadas = []
        self.falla = falla

    def responder(self, *, nivel, objetivo, guia, mensajes):
        self.llamadas.append({"nivel": nivel, "objetivo": objetivo, "guia": guia, "mensajes": mensajes})
        if self.falla:
            raise TutorNoDisponible()
        return RespuestaTutor(texto="Pista: piensa en las decenas.")


@pytest.fixture
def habilitado(monkeypatch):
    monkeypatch.setattr(settings, "logos_ia_habilitada", True)
    monkeypatch.setattr(settings, "anthropic_api_key", "clave-de-prueba")
    monkeypatch.setattr(tutor_ia, "uso_diario", tutor_ia._UsoDiario())
    falso = TutorFalso()
    app.dependency_overrides[tutor_ia.get_tutor_ia] = lambda: falso
    yield falso
    app.dependency_overrides.pop(tutor_ia.get_tutor_ia, None)


def _preparar(client, session, nombre_nivel="4° básico", rut="21.345.678-4"):
    nivel = Nivel(nombre=nombre_nivel, regimen="A", decreto="439/2012", formato_examen="integrado",
                  num_preguntas_examen=20, duracion_examen_min=90)
    session.add(nivel); session.commit(); session.refresh(nivel)
    asig = Asignatura(nivel_id=nivel.id, nombre="Matemática")
    session.add(asig); session.commit(); session.refresh(asig)
    oa = ObjetivoAprendizaje(asignatura_id=asig.id, codigo_oficial="OA 1", descripcion="Números hasta el 10.000",
                             contenido_guia="Guía: valor posicional.")
    session.add(oa); session.commit(); session.refresh(oa)
    token = client.post("/auth/registro", json={"email": f"tutor.{next(_N)}@test.cl", "password": "ClaveSegura123",
                                                "nombre": "Apoderado Test"}).json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    perfil = client.post("/auth/alumnos", headers=headers, json={"nombre": "Sofía", "apellidos": "Pérez",
                         "fecha_nacimiento": "2016-01-01", "rut": rut, "nivel_id": nivel.id}).json()["id"]
    return perfil, oa.id, headers


def _preguntar(client, perfil, oa, headers, texto):
    return client.post(f"/tutor-ia/{perfil}/oa/{oa}", headers=headers, json={"mensajes": [{"rol": "alumno", "texto": texto}]})


def test_estado_desactivado_por_defecto(client):
    assert client.get("/tutor-ia/estado").json() == {"habilitado": False}


def test_sin_habilitar_responde_503(client, session):
    perfil, oa, h = _preparar(client, session)
    assert _preguntar(client, perfil, oa, h, "¿Qué es una decena?").status_code == 503


def test_responde_y_envia_solo_guia_curso_y_mensajes_anonimizados(client, session, habilitado):
    perfil, oa, h = _preparar(client, session)
    r = _preguntar(client, perfil, oa, h, "Soy Sofía, mi RUT es 21.345.678-4 y mi correo sofia@mail.cl, ¿qué es una decena?")
    assert r.status_code == 200 and r.json()["texto"].startswith("Pista")
    llamada = habilitado.llamadas[0]
    assert llamada["nivel"] == "4° básico" and llamada["guia"] == "Guía: valor posicional."
    enviado = llamada["mensajes"][0].texto
    assert "21.345.678-4" not in enviado and "sofia@mail.cl" not in enviado


def test_senal_de_crisis_no_llama_al_proveedor_y_deriva(client, session, habilitado):
    perfil, oa, h = _preparar(client, session)
    r = _preguntar(client, perfil, oa, h, "a veces me quiero morir")
    assert r.status_code == 200 and r.json()["derivacion"] is True
    assert "*4141" in r.json()["texto"]
    assert habilitado.llamadas == []


def test_no_permite_usar_el_perfil_de_otra_cuenta(client, session, habilitado):
    perfil, oa, _ = _preparar(client, session)
    _, _, otros = _preparar(client, session, "5° básico", "1-9")
    assert _preguntar(client, perfil, oa, otros, "hola").status_code == 403


def test_limite_diario(client, session, habilitado, monkeypatch):
    monkeypatch.setattr(settings, "logos_ia_limite_diario", 2)
    perfil, oa, h = _preparar(client, session)
    assert [_preguntar(client, perfil, oa, h, "¿y esto?").status_code for _ in range(3)] == [200, 200, 429]


def test_falla_del_proveedor_da_503(client, session, habilitado):
    perfil, oa, h = _preparar(client, session)
    habilitado.falla = True
    assert _preguntar(client, perfil, oa, h, "¿qué es una centena?").status_code == 503


def test_anonimizar_y_crisis():
    assert "[dato borrado]" in anonimizar("mi rut es 12.345.678-9")
    assert "[dato borrado]" in anonimizar("llámame al +56 9 1234 5678")
    assert anonimizar("¿cuánto es 3.000 + 400?") == "¿cuánto es 3.000 + 400?"
    assert senal_de_crisis("quiero hacerme daño") and not senal_de_crisis("me cuesta la división")


def test_adaptador_claude_envia_parametros_esperados_y_maneja_rechazo():
    from types import SimpleNamespace as NS

    from app.domain.tutor_ia.ports import MensajeTutor
    from app.infrastructure.ia.tutor_claude import RESPUESTA_DECLINADA, TutorIAClaude

    capturado = {}

    def crear(**kw):
        capturado.update(kw)
        return NS(stop_reason="end_turn", content=[NS(type="thinking"), NS(type="text", text="Una decena son 10 unidades.")])

    t = TutorIAClaude(api_key="x", modelo="claude-opus-5-5")
    t._cliente = NS(beta=NS(messages=NS(create=crear)))
    r = t.responder(nivel="4° básico", objetivo="OA 1", guia="Guía", mensajes=[MensajeTutor("alumno", "¿Qué es una decena?")])
    assert r.texto == "Una decena son 10 unidades."
    assert capturado["model"] == "claude-opus-5-5" and capturado["fallbacks"] == "default"
    assert capturado["output_config"] == {"effort": "low"} and "thinking" not in capturado
    assert capturado["messages"] == [{"role": "user", "content": "¿Qué es una decena?"}]
    assert "Guía" in capturado["system"] and "4° básico" in capturado["system"]

    t._cliente = NS(beta=NS(messages=NS(create=lambda **kw: NS(stop_reason="refusal", content=[]))))
    r = t.responder(nivel="4° básico", objetivo="OA 1", guia="Guía", mensajes=[MensajeTutor("alumno", "x")])
    assert r.declinada and r.texto == RESPUESTA_DECLINADA
