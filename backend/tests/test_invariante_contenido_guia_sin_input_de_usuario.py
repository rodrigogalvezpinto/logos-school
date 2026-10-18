"""P3 del plan de pruebas exhaustivo (planificacion/28-plan-de-pruebas-exhaustivo.md):
`contenido_guia` es el único campo del proyecto que el frontend inyecta como HTML crudo
(`[innerHTML]` + `bypassSecurityTrustHtml` en `estudiar-oa.ts`, vía `markdown.pipe.ts`) —
seguro solo porque hoy nunca recibe texto de usuario, se genera una sola vez por scripts de
contenido y se sirve de solo lectura. Este test congela esa invariante a nivel estructural:
introspecciona el árbol real de rutas de FastAPI (mismo mecanismo que
`test_matriz_permisos.py`) y falla si algún día alguien agrega un endpoint de escritura
(POST/PUT/PATCH) cuyo cuerpo acepte un campo `contenido_guia` — que sería el momento exacto
en que `bypassSecurityTrustHtml` dejaría de ser seguro y habría que sanitizar de verdad."""

from fastapi.routing import APIRoute

from app.main import app


def _todas_las_rutas() -> list[APIRoute]:
    rutas: list[APIRoute] = []
    for route in app.routes:
        sub_router = getattr(route, "original_router", None)
        rutas.extend(sub_router.routes if sub_router else [route])
    return [r for r in rutas if isinstance(r, APIRoute)]


def test_ningun_endpoint_de_escritura_acepta_contenido_guia_como_input():
    metodos_de_escritura = {"POST", "PUT", "PATCH"}
    ofensores = []

    for route in _todas_las_rutas():
        if not (route.methods & metodos_de_escritura):
            continue
        body_field = getattr(route, "body_field", None)
        if not body_field:
            continue
        modelo = body_field.field_info.annotation
        campos = getattr(modelo, "model_fields", {})
        if "contenido_guia" in campos:
            ofensores.append((route.path, sorted(route.methods)))

    assert ofensores == [], (
        f"Se encontró un endpoint de escritura que acepta 'contenido_guia' como input: {ofensores}. "
        "Esto rompe la invariante que hace seguro el bypassSecurityTrustHtml en estudiar-oa.ts — "
        "si esto es intencional, hay que sanitizar el HTML antes de inyectarlo en el frontend."
    )


def test_objetivo_de_aprendizaje_solo_se_expone_en_endpoints_de_lectura():
    """Complementa el test anterior desde el otro ángulo: confirma que 'contenido_guia'
    solo aparece en respuestas GET (el read-model actual), nunca en el cuerpo de un
    request — si mañana se agrega edición de contenido vía API, este test también debe
    tocarse a propósito, no romperse en silencio."""
    apariciones_en_get = []

    for route in _todas_las_rutas():
        body_field = getattr(route, "body_field", None)
        if body_field:
            continue  # ya cubierto arriba
        if "GET" not in route.methods:
            continue
        modelo_respuesta = route.response_model
        campos = getattr(modelo_respuesta, "model_fields", {}) if modelo_respuesta else {}
        if "contenido_guia" in campos:
            apariciones_en_get.append(route.path)

    assert apariciones_en_get == ["/contenido/objetivos/{oa_id}"]
