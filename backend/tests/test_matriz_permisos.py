"""Matriz de permisos automática — a diferencia de los tests de un endpoint puntual (ej.
"un token de Profesor no sirve en /admin/*"), este archivo NO enumera rutas a mano: lee
`app.routes` en tiempo real y genera un caso por cada endpoint protegido. Si mañana se
agrega un endpoint nuevo y alguien olvida protegerlo, este test lo detecta solo, sin que
nadie tenga que acordarse de agregar un caso a mano.

Nació de un hallazgo real (2026-08-14): todo el router `/evaluaciones/*` (iniciar/
responder/entregar una prueba) no tenía NINGUNA autenticación — cualquiera, sin sesión,
podía responder o entregar la evaluación de cualquier alumno adivinando su id. Una prueba
manual nunca lo iba a encontrar porque el frontend siempre manda un token válido; hizo
falta mirar el grafo de dependencias de cada ruta, no el flujo de un usuario real.

Qué prueba, por cada endpoint protegido:
1. Sin ningún token → 401/403.
2. Con un token de un tipo de cuenta distinto al que exige el endpoint (ej. token de
   Profesor en un endpoint de Admin) → 401/403 — nunca 200 y nunca un 404/422 que delate
   que el request llegó a ejecutar lógica de negocio antes de validar quién es.

Qué NO prueba (fuera de alcance a propósito): reglas de propiedad más finas ya cubiertas
por tests específicos (ej. "un apoderado no puede ver el perfil de otro apoderado" vive en
test_progreso.py/test_evaluaciones_intentos.py, porque necesita datos de dominio reales
que esta matriz genérica no construye).
"""

import re

import pytest

from app.main import app

# Nombres de función de las dependencias-guardia que reconoce este archivo, y a qué tipo
# de cuenta corresponden. Si se agrega un tipo de cuenta nuevo (ej. otro rol futuro), basta
# con sumar su/sus nombres de dependencia acá.
GUARDIAS_POR_TIPO = {
    "apoderado": {"get_cuenta_actual", "verificar_perfil_propio"},
    "admin": {"get_cuenta_admin_actual"},
    "profesor": {"get_profesor_aprobado_actual", "get_cuenta_profesor_actual"},
}
TODOS_LOS_GUARDIAS = {g for guardias in GUARDIAS_POR_TIPO.values() for g in guardias}


def _descubrir_rutas_protegidas() -> list[tuple[str, str, str]]:
    """Devuelve (metodo, path, tipo_de_cuenta_exigido) para cada ruta que declara alguna
    de las dependencias-guardia conocidas — en cualquier punto de su árbol de
    dependencias, no solo como parámetro directo (cubre tanto `dependencies=[Depends(...)]`
    a nivel de router como `Depends(...)` como parámetro de la función)."""
    encontradas = []
    for route in app.routes:
        sub_router = getattr(route, "original_router", None)
        rutas = sub_router.routes if sub_router else [route]
        for r in rutas:
            if not hasattr(r, "dependant"):
                continue
            nombres_deps = {d.call.__name__ for d in r.dependant.dependencies}
            guardias_presentes = nombres_deps & TODOS_LOS_GUARDIAS
            if not guardias_presentes:
                continue
            for tipo, nombres in GUARDIAS_POR_TIPO.items():
                if guardias_presentes & nombres:
                    for metodo in sorted(r.methods - {"HEAD", "OPTIONS"}):
                        encontradas.append((metodo, r.path, tipo))
                    break
    return encontradas


RUTAS_PROTEGIDAS = _descubrir_rutas_protegidas()

# Rutas sin ningún guardia de sesión — deben estar acá a propósito y con una razón, o el
# test de abajo falla. Así, si alguien agrega un endpoint nuevo con datos sensibles y se le
# olvida el `Depends(get_cuenta_actual)` (exactamente el bug real que motivó este archivo),
# el test lo detecta sin que nadie tenga que acordarse de nada.
RUTAS_PUBLICAS_A_PROPOSITO = {
    ("GET", "/salud"): "healthcheck de infraestructura",
    ("POST", "/auth/registro"): "trámite de registro — todavía no hay sesión",
    ("POST", "/auth/login"): "login — todavía no hay sesión",
    ("POST", "/auth/login-google"): "login — todavía no hay sesión",
    ("POST", "/profesor/auth/registro"): "trámite de registro — todavía no hay sesión",
    ("POST", "/profesor/auth/login"): "login — todavía no hay sesión",
    ("POST", "/admin/auth/login"): "login — todavía no hay sesión",
    ("GET", "/contenido/niveles"): "temario oficial — contenido de marketing/exploración libre",
    ("GET", "/contenido/niveles/{nivel_id}/asignaturas"): "temario oficial — contenido de exploración libre",
    ("GET", "/contenido/asignaturas/{asignatura_id}/objetivos"): "temario oficial — contenido de exploración libre",
    ("GET", "/contenido/objetivos/{oa_id}"): "temario oficial — contenido de exploración libre",
    ("GET", "/evaluaciones/autoevaluacion/{oa_id}"): "banco de práctica — sin datos personales de un alumno",
    ("GET", "/evaluaciones/conjuntos/asignatura/{asignatura_id}"): "lista de pruebas/exámenes disponibles, sin respuestas",
    ("GET", "/evaluaciones/conjuntos/nivel/{nivel_id}"): "lista de pruebas/exámenes disponibles, sin respuestas",
    ("GET", "/evaluaciones/conjuntos/{conjunto_id}"): "preguntas sin respuesta_correcta — sin datos personales",
}


def _descubrir_todas_las_rutas_de_negocio() -> list[tuple[str, str]]:
    """Como `_descubrir_rutas_protegidas`, pero devuelve TODAS las rutas (con o sin
    guardia) — se usa para detectar las que no tienen guardia y tampoco están en la lista
    blanca de arriba."""
    todas = []
    for route in app.routes:
        sub_router = getattr(route, "original_router", None)
        rutas = sub_router.routes if sub_router else [route]
        for r in rutas:
            if not hasattr(r, "dependant") or not hasattr(r, "path"):
                continue
            for metodo in sorted(r.methods - {"HEAD", "OPTIONS"}):
                todas.append((metodo, r.path))
    return todas


def test_toda_ruta_sin_guardia_esta_en_la_lista_blanca_de_publicas():
    protegidas = {(m, p) for m, p, _ in RUTAS_PROTEGIDAS}
    sin_clasificar = [
        (m, p) for m, p in _descubrir_todas_las_rutas_de_negocio()
        if (m, p) not in protegidas and (m, p) not in RUTAS_PUBLICAS_A_PROPOSITO and p != "/openapi.json"
        and not p.startswith("/docs") and p != "/redoc"
    ]
    assert not sin_clasificar, (
        f"Estas rutas no tienen ningún guardia de sesión Y no están en RUTAS_PUBLICAS_A_PROPOSITO — "
        f"si es intencional, agrégalas a la lista con el motivo; si no, les falta protección: {sin_clasificar}"
    )


def _path_con_dummies(path: str) -> str:
    return re.sub(r"\{[^}]+\}", "1", path)


def _token_apoderado(client) -> str:
    import time

    email = f"matriz.apoderado.{time.time_ns()}@test.cl"
    r = client.post("/auth/registro", json={"email": email, "password": "ClaveSegura123", "nombre": "QA"})
    return r.json()["access_token"]


def _token_profesor(client) -> str:
    import time

    email = f"matriz.profesor.{time.time_ns()}@test.cl"
    r = client.post("/profesor/auth/registro", json={"email": email, "password": "ClaveSegura123", "nombre": "QA"})
    return r.json()["access_token"]


def _token_admin(client, session) -> str:
    from app.infrastructure.persistence.orm_models import CuentaAdmin
    from app.infrastructure.seguridad.bcrypt_hasheador import HasheadorPasswordBcrypt

    cuenta = CuentaAdmin(
        email="matriz.admin@logos.cl", nombre="Admin QA",
        password_hash=HasheadorPasswordBcrypt().hashear("ClaveAdmin123"),
    )
    session.add(cuenta)
    session.commit()
    r = client.post("/admin/auth/login", json={"email": "matriz.admin@logos.cl", "password": "ClaveAdmin123"})
    return r.json()["access_token"]


@pytest.mark.parametrize("metodo,path,tipo_exigido", RUTAS_PROTEGIDAS, ids=[f"{m} {p}" for m, p, _ in RUTAS_PROTEGIDAS])
def test_ruta_protegida_rechaza_sin_token(client, session, metodo, path, tipo_exigido):
    assert RUTAS_PROTEGIDAS, "no se descubrió ninguna ruta protegida — revisar _descubrir_rutas_protegidas"
    r = client.request(metodo, _path_con_dummies(path), json={} if metodo in ("POST", "PATCH", "PUT") else None)
    assert r.status_code in (401, 403), f"{metodo} {path} debería exigir sesión y devolvió {r.status_code}"


@pytest.mark.parametrize("metodo,path,tipo_exigido", RUTAS_PROTEGIDAS, ids=[f"{m} {p}" for m, p, _ in RUTAS_PROTEGIDAS])
def test_ruta_protegida_rechaza_token_de_otro_tipo_de_cuenta(client, session, metodo, path, tipo_exigido):
    tokens_de_otros_tipos = {
        "apoderado": lambda: _token_apoderado(client),
        "profesor": lambda: _token_profesor(client),
        "admin": lambda: _token_admin(client, session),
    }
    del tokens_de_otros_tipos[tipo_exigido]

    for construir_token in tokens_de_otros_tipos.values():
        headers = {"Authorization": f"Bearer {construir_token()}"}
        r = client.request(
            metodo, _path_con_dummies(path), headers=headers,
            json={} if metodo in ("POST", "PATCH", "PUT") else None,
        )
        assert r.status_code in (401, 403), (
            f"{metodo} {path} exige cuenta de tipo '{tipo_exigido}' pero aceptó un token de otro tipo "
            f"(devolvió {r.status_code} en vez de 401/403)"
        )
