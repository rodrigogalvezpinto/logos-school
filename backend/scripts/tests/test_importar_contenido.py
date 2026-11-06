"""Regresiones de identidad curricular sin conexiones a bases de datos."""
import os
import sys
from pathlib import Path

import pytest

SCRIPTS = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SCRIPTS))
from parser_contenido import clave_valida, parsear_guia
from parser_prueba_examen import parsear_prueba_o_examen

CONTENIDO = SCRIPTS.parents[1] / "contenido"


class SesionCaptura:
    def __init__(self):
        self.objetos = []

    def add(self, objeto):
        self.objetos.append(objeto)
        objeto.id = len(self.objetos)

    def commit(self):
        pass

    def refresh(self, objeto):
        pass


def test_identidades_reales_ciencias_tercero_medio():
    guia = parsear_guia((CONTENIDO / "03-medio/ciencias-para-la-ciudadania.md").read_text())
    assert [(o.modulo, o.codigo_oficial) for o in guia] == [
        ("1", "OA 1"), ("1", "OA 3"), ("2", "OA 1"), ("2", "OA 3")
    ]
    from importar_contenido import _resolver_oa
    mapa = {(o.modulo, o.codigo_oficial): i for i, o in enumerate(guia, 1)}
    examen = parsear_prueba_o_examen((CONTENIDO / "03-medio/examenes/ciencias-para-la-ciudadania-examen-forma-b.md").read_text())
    assert len(examen) == 25
    assert [_resolver_oa(mapa, p.codigo_oa, p.modulo) for _, p in examen] == [1]*6 + [2]*6 + [3]*6 + [4]*7
    assert [p.modulo for _, p in examen] == ["1"]*12 + ["2"]*13
    assert all(f"(Módulo {o.modulo})" in o.descripcion for o in guia)

    from importar_contenido import _importar_conjunto
    from app.infrastructure.persistence.orm_models import Pregunta

    sesion = SesionCaptura()
    cantidad = _importar_conjunto(
        sesion,
        CONTENIDO / "03-medio/examenes/ciencias-para-la-ciudadania-examen-forma-b.md",
        "examen_simulacro", "Ciencias", "B", 9, None, 90, mapa,
    )
    assert cantidad == 25
    preguntas = [p for p in sesion.objetos if isinstance(p, Pregunta)]
    assert [p.oa_id for p in preguntas] == [1]*6 + [2]*6 + [3]*6 + [4]*7
    assert all(p.asignatura_id == 9 for p in preguntas)


@pytest.mark.parametrize("codigos,modulo,esperado", [
    ((), None, None),
    (("OA 1", "OA 2"), None, None),
    (("OA 2",), None, 102),
    (("OA 3",), None, None),
    (("OA 1",), "2", 201),
])
def test_fallback_exacto_intersecta_contexto_y_modulo_sin_adivinar(codigos, modulo, esperado):
    from importar_contenido import _huella_pregunta, _resolver_oa_pregunta
    from parser_prueba_examen import PreguntaSinRespuesta, RespuestaPauta

    pregunta = PreguntaSinRespuesta(1, "desarrollo_breve", "Explica una idea.", None)
    mapa = {(None, "OA 1"): 101, (None, "OA 2"): 102, ("2", "OA 1"): 201}
    banco = {_huella_pregunta(pregunta): set(mapa)}
    pauta = RespuestaPauta("Explicación.", "Criterio.", modulo=modulo, codigos_oa=codigos)
    assert _resolver_oa_pregunta(pregunta, pauta, mapa, banco) == esperado


def test_indice_banco_conserva_todas_las_identidades_y_espacios_equivalentes():
    from types import SimpleNamespace
    from importar_contenido import _huella_pregunta, _indexar_banco
    from parser_prueba_examen import PreguntaSinRespuesta

    original = PreguntaSinRespuesta(1, "alternativas", "  ¿Qué   número?\n", ["Uno", "Dos"])
    equivalente = PreguntaSinRespuesta(1, "alternativas", "¿Qué número?", ["Uno", "Dos"])
    objetivos = [SimpleNamespace(modulo=modulo, codigo_oficial="OA 1", preguntas=[original]) for modulo in ("1", "2")]
    indice = _indexar_banco(objetivos)
    assert indice[_huella_pregunta(equivalente)] == {("1", "OA 1"), ("2", "OA 1")}


@pytest.mark.parametrize("texto,opciones", [
    ("Calcula 22 para X.", ["4", "22"]),
    ("Calcula 2² para x.", ["4", "22"]),
    ("Calcula 2² para X.", ["22", "4"]),
])
def test_huella_no_confunde_notacion_matematica_mayusculas_ni_orden(texto, opciones):
    from importar_contenido import _huella_pregunta
    from parser_prueba_examen import PreguntaSinRespuesta

    original = PreguntaSinRespuesta(1, "alternativas", "Calcula 2² para X.", ["4", "22"])
    diferente = PreguntaSinRespuesta(1, "alternativas", texto, opciones)
    assert _huella_pregunta(original) != _huella_pregunta(diferente)


def test_importacion_completa_en_memoria_conserva_banco_y_asociaciones(capsys):
    from types import SimpleNamespace
    from importar_contenido import CURSOS, importar_curso
    from app.infrastructure.persistence.orm_models import ConjuntoEvaluacion, Nivel, ObjetivoAprendizaje, Pregunta

    class SesionCurso(SesionCaptura):
        def exec(self, consulta):
            assert consulta.column_descriptions[0]["entity"] is Nivel
            return SimpleNamespace(first=lambda: None)

    resumen = {}
    detalle_curso = os.environ.get("LOGOS_AUDIT_CURSO")
    assert detalle_curso is None or detalle_curso in {curso["carpeta"] for curso in CURSOS}
    pendientes = []
    total_banco = total_evaluaciones = total_vinculadas_unidad = 0
    for curso in CURSOS:
        sesion = SesionCurso()
        importar_curso(sesion, curso)
        preguntas = {p.id: p for p in sesion.objetos if isinstance(p, Pregunta)}
        objetivos = {oa.id: oa for oa in sesion.objetos if isinstance(oa, ObjetivoAprendizaje)}
        conjuntos = [c for c in sesion.objetos if isinstance(c, ConjuntoEvaluacion)]
        ids_evaluaciones = set()
        conteos = {"unidad": [0, 0], "examen": [0, 0]}
        for conjunto in conjuntos:
            categoria = "unidad" if conjunto.tipo == "prueba_unidad" else "examen"
            ids_evaluaciones.update(conjunto.pregunta_ids)
            for numero, pregunta_id in enumerate(conjunto.pregunta_ids, 1):
                pregunta = preguntas[pregunta_id]
                referencia = (curso["carpeta"], conjunto.nombre, pregunta_id)
                assert pregunta.asignatura_id is not None, referencia
                conteos[categoria][0] += 1
                if pregunta.oa_id is not None:
                    assert objetivos[pregunta.oa_id].asignatura_id == pregunta.asignatura_id, referencia
                    conteos[categoria][1] += 1
                elif categoria == "examen":
                    pytest.fail(f"Examen sin OA: {referencia}")
                elif detalle_curso == curso["carpeta"]:
                    pendientes.append((conjunto.nombre, numero, pregunta.tipo, pregunta.enunciado, pregunta.opciones))
        banco = [p for pid, p in preguntas.items() if pid not in ids_evaluaciones]
        assert all(p.oa_id in objetivos for p in banco), curso["carpeta"]
        total_banco += len(banco)
        total_evaluaciones += len(ids_evaluaciones)
        total_vinculadas_unidad += conteos["unidad"][1]
        resumen[curso["carpeta"]] = conteos
    salida = capsys.readouterr().out
    assert "No existe" not in salida and "No pude asociar" not in salida, salida
    if detalle_curso:
        print({"curso": detalle_curso, "resumen": resumen[detalle_curso], "pendientes": pendientes})
    else:
        print(resumen)
    assert total_banco == 3115
    assert total_evaluaciones == 3035
    assert total_vinculadas_unidad == 1825
    assert all(total == vinculadas for conteos in resumen.values() for total, vinculadas in conteos.values()), resumen


def test_fuentes_coinciden_con_postgresql_candidato():
    from collections import Counter
    from types import SimpleNamespace
    from sqlalchemy import text
    from sqlalchemy.engine import make_url
    from sqlmodel import Session, create_engine, select
    from importar_contenido import CURSOS, importar_curso
    from app.infrastructure.persistence.orm_models import Asignatura, ConjuntoEvaluacion, Nivel, ObjetivoAprendizaje, Pregunta

    configuracion = os.environ.get("LOGOS_AUDIT_DATABASE_URL")
    if not configuracion:
        pytest.skip("Integración opcional: requiere LOGOS_AUDIT_DATABASE_URL de una candidata importada")
    url = make_url(configuracion)
    assert url.host in {"localhost", "127.0.0.1", "::1"}
    assert url.database and url.database.startswith("logos_auditoria_fuentes_")

    class CapturaCurso(SesionCaptura):
        def exec(self, consulta):
            assert consulta.column_descriptions[0]["entity"] is Nivel
            return SimpleNamespace(first=lambda: None)

    def firmas(objetos):
        niveles = {o.id: o.nombre for o in objetos if isinstance(o, Nivel)}
        asignaturas = {o.id: (niveles[o.nivel_id], o.nombre) for o in objetos if isinstance(o, Asignatura)}
        objetivos = {o.id: (asignaturas[o.asignatura_id], o.codigo_oficial, o.descripcion, o.eje_tematico, o.contenido_guia) for o in objetos if isinstance(o, ObjetivoAprendizaje)}
        preguntas = {p.id: (objetivos[p.oa_id], asignaturas.get(p.asignatura_id), p.tipo, p.enunciado, None if p.opciones is None else tuple(p.opciones), p.respuesta_correcta, p.retroalimentacion, p.nivel_dificultad) for p in objetos if isinstance(p, Pregunta)}
        conjuntos = [(c.tipo, asignaturas.get(c.asignatura_id), niveles.get(c.nivel_id), c.nombre, c.forma, c.tiempo_sugerido_min, tuple(preguntas[pid] for pid in c.pregunta_ids)) for c in objetos if isinstance(c, ConjuntoEvaluacion)]
        return Counter(objetivos.values()), Counter(preguntas.values()), Counter(conjuntos)

    engine = create_engine(url, echo=False)
    try:
        with Session(engine) as sesion:
            sesion.execute(text("SET TRANSACTION READ ONLY"))
            modelos = (Nivel, Asignatura, ObjetivoAprendizaje, Pregunta, ConjuntoEvaluacion)
            observados = firmas([o for modelo in modelos for o in sesion.exec(select(modelo)).all()])
            esperados = (Counter(), Counter(), Counter())
            for curso in CURSOS:
                captura = CapturaCurso()
                importar_curso(captura, curso)
                for acumulado, actual in zip(esperados, firmas(captura.objetos)):
                    acumulado.update(actual)
            assert [sum(c.values()) for c in esperados] == [410, 6150, 206]
            for nombre, esperado, observado in zip(("OA y guías", "preguntas", "conjuntos y orden"), esperados, observados):
                assert esperado == observado, (nombre, esperado - observado, observado - esperado)
    finally:
        engine.dispose()


def test_escala_historia_segundo_medio_coincide_con_motor():
    import re
    from app.domain.evaluaciones.value_objects import calcular_nota

    ruta = CONTENIDO / "02-medio/examenes/historia-geografia-y-cs-sociales-examen-forma-b.md"
    texto = ruta.read_text(encoding="utf-8")
    bandas = re.findall(r"\|\s*(\d+)-(\d+)\s+pts\s*\|\s*(\d+,\d)\s*-\s*(\d+,\d)", texto)
    assert len(bandas) == 5
    for minimo, maximo, nota_minima, nota_maxima in bandas:
        assert calcular_nota(int(minimo), 37) == float(nota_minima.replace(",", "."))
        assert calcular_nota(int(maximo), 37) == float(nota_maxima.replace(",", "."))


def test_lookup_ambiguo_no_elige_ultimo():
    from importar_contenido import _resolver_oa
    with pytest.raises(ValueError, match="ambigu"):
        _resolver_oa({("1", "OA 1"): 1, ("2", "OA 1"): 2}, "OA 1", None)
    assert _resolver_oa({(None, "OA 1"): 7}, "OA 1", None) == 7
    with pytest.raises(ValueError):
        _resolver_oa({("1", "OA 1"): 1}, "OA 1", "2")


@pytest.mark.parametrize("unidad,modulo", [("bienestar-y-salud", "1"), ("seguridad-prevencion-autocuidado", "2")])
def test_unidades_preservan_modulo(unidad, modulo):
    ruta = CONTENIDO / f"03-medio/pruebas/ciencias-para-la-ciudadania-unidad-{unidad}.md"
    resultado = parsear_prueba_o_examen(ruta.read_text())
    assert resultado
    assert all(p.modulo == modulo for _, p in resultado)


@pytest.mark.parametrize("respuesta", [None, "", "Tres"])
def test_clave_cerrada_invalida_se_rechaza_antes_de_persistir(tmp_path, monkeypatch, respuesta):
    from types import SimpleNamespace
    import importar_contenido
    from parser_prueba_examen import PreguntaSinRespuesta, RespuestaPauta

    ruta = tmp_path / "prueba.md"
    ruta.write_text("Contenido de prueba", encoding="utf-8")
    pregunta = PreguntaSinRespuesta(1, "alternativas", "Elige una cantidad", ["Uno", "Dos"])
    pauta = None if respuesta is None else RespuestaPauta(respuesta, "Explicación")
    monkeypatch.setattr(importar_contenido, "parsear_prueba_o_examen", lambda _: [(pregunta, pauta)])
    enviados = []
    sesion = SimpleNamespace(add=enviados.append, commit=lambda: None, refresh=lambda _: None)
    with pytest.raises(ValueError, match="pregunta 1"):
        importar_contenido._importar_conjunto(
            sesion, ruta, "prueba_unidad", "Prueba", None, 1, None, None, {},
        )
    assert enviados == []


@pytest.mark.parametrize("respuesta", [None, "", " \t"])
def test_pauta_abierta_ausente_o_vacia_se_rechaza_antes_de_persistir(tmp_path, monkeypatch, respuesta):
    import importar_contenido
    from parser_prueba_examen import PreguntaSinRespuesta, RespuestaPauta

    ruta = tmp_path / "prueba.md"
    ruta.write_text("Contenido de prueba", encoding="utf-8")
    pregunta = PreguntaSinRespuesta(1, "desarrollo_breve", "Explica", None)
    pauta = None if respuesta is None else RespuestaPauta(respuesta, "")
    monkeypatch.setattr(importar_contenido, "parsear_prueba_o_examen", lambda _: [(pregunta, pauta)])
    sesion = SesionCaptura()
    with pytest.raises(ValueError, match="pregunta 1"):
        importar_contenido._importar_conjunto(
            sesion, ruta, "prueba_unidad", "Prueba", None, 1, None, None, {},
        )
    assert sesion.objetos == []


@pytest.mark.parametrize("carpeta", ["01-basico", "02-basico", "03-basico", "04-basico"])
@pytest.mark.parametrize("forma", ["a", "b"])
def test_integrados_vinculan_cada_pregunta_a_su_asignatura_y_oa(carpeta, forma):
    from importar_contenido import CURSOS, _importar_conjunto
    from app.infrastructure.persistence.orm_models import Pregunta

    curso = next(c for c in CURSOS if c["carpeta"] == carpeta)
    referencias = {}
    for asignatura_id, (slug, _) in enumerate(curso["asignaturas"], 1):
        guia = parsear_guia((CONTENIDO / carpeta / f"{slug}.md").read_text(encoding="utf-8"))
        referencias[slug] = (asignatura_id, {
            (oa.modulo, oa.codigo_oficial): asignatura_id * 1000 + i
            for i, oa in enumerate(guia, 1)
        })
    ruta = CONTENIDO / carpeta / "examenes" / f"examen-integrado-forma-{forma}.md"
    resultados = parsear_prueba_o_examen(ruta.read_text(encoding="utf-8"))
    alias = {
        "Matemática": "matematica",
        "Lenguaje": "lenguaje-y-comunicacion",
        "Lenguaje y Comunicación": "lenguaje-y-comunicacion",
        "Ciencias": "ciencias-naturales",
        "Ciencias Naturales": "ciencias-naturales",
        "Historia": "historia-geografia-y-cs-sociales",
        "Historia, Geografía y Cs. Sociales": "historia-geografia-y-cs-sociales",
        "Historia, Geografía y Ciencias Sociales": "historia-geografia-y-cs-sociales",
    }
    esperadas = []
    for _, pauta in resultados:
        assert pauta is not None and pauta.asignatura in alias
        asignatura_id, mapa = referencias[alias[pauta.asignatura]]
        esperadas.append((asignatura_id, mapa[(pauta.modulo, pauta.codigo_oa)]))
    sesion = SesionCaptura()
    assert _importar_conjunto(
        sesion, ruta, "examen_simulacro", "Integrado", forma.upper(), None, 1, 90, {},
        asignaturas_integradas=referencias,
    ) == 20
    preguntas = [p for p in sesion.objetos if isinstance(p, Pregunta)]
    assert [(p.asignatura_id, p.oa_id) for p in preguntas] == esperadas


@pytest.mark.parametrize("asignatura,codigo", [(None, "OA 1"), ("Biología", "OA 1"), ("Matemática", "OA 99")])
def test_integrado_rechaza_referencia_incompleta_antes_de_persistir(tmp_path, monkeypatch, asignatura, codigo):
    import importar_contenido
    from parser_prueba_examen import PreguntaSinRespuesta, RespuestaPauta

    ruta = tmp_path / "integrado.md"
    ruta.write_text("Contenido de prueba", encoding="utf-8")
    pregunta = PreguntaSinRespuesta(1, "alternativas", "Elige", ["Uno", "Dos"])
    pauta = RespuestaPauta("Dos", "Explicación", codigo_oa=codigo, asignatura=asignatura)
    monkeypatch.setattr(importar_contenido, "parsear_prueba_o_examen", lambda _: [(pregunta, pauta)])
    sesion = SesionCaptura()
    with pytest.raises(ValueError):
        importar_contenido._importar_conjunto(
            sesion, ruta, "examen_simulacro", "Integrado", "A", None, 1, 90, {},
            asignaturas_integradas={"matematica": (3, {(None, "OA 1"): 301})},
        )
    assert sesion.objetos == []


def test_snapshot_corpus_actual_con_pautas_y_claves_completas():
    from importar_contenido import CURSOS

    totales = {"guias": 0, "oa": 0, "banco": 0, "pruebas": 0, "preguntas_pruebas": 0,
               "examenes": 0, "preguntas_examenes": 0, "pruebas_sin_oa": 0, "examenes_sin_oa": 0}
    sin_oa_examen = {}
    for curso in CURSOS:
        carpeta = CONTENIDO / curso["carpeta"]
        for slug, _ in curso["asignaturas"]:
            ruta = carpeta / f"{slug}.md"
            objetivos = parsear_guia(ruta.read_text(encoding="utf-8"))
            assert objetivos, ruta
            totales["guias"] += 1
            totales["oa"] += len(objetivos)
            assert len({(oa.modulo, oa.codigo_oficial) for oa in objetivos}) == len(objetivos), ruta
            for oa in objetivos:
                for numero, pregunta in enumerate(oa.preguntas, 1):
                    referencia = (ruta, oa.modulo, oa.codigo_oficial, numero)
                    assert pregunta.respuesta_correcta.strip(), referencia
                    assert clave_valida(pregunta.tipo, pregunta.respuesta_correcta, pregunta.opciones), referencia
                    totales["banco"] += 1
        for directorio, categoria in (("pruebas", "pruebas"), ("examenes", "examenes")):
            for ruta in sorted((carpeta / directorio).glob("*.md")):
                preguntas = parsear_prueba_o_examen(ruta.read_text(encoding="utf-8"))
                assert preguntas, ruta
                assert [p.numero for p, _ in preguntas] == list(range(1, len(preguntas) + 1)), ruta
                totales[categoria] += 1
                totales[f"preguntas_{categoria}"] += len(preguntas)
                for pregunta, pauta in preguntas:
                    referencia = (ruta, pregunta.numero)
                    assert pauta is not None and pauta.respuesta_correcta.strip(), referencia
                    assert clave_valida(pregunta.tipo, pauta.respuesta_correcta, pregunta.opciones), referencia
                    if pauta.codigo_oa is None:
                        totales[f"{categoria}_sin_oa"] += 1
                        if categoria == "examenes":
                            sin_oa_examen.setdefault(str(ruta.relative_to(CONTENIDO)), []).append(pregunta.numero)
    print(totales)
    print({"examenes_sin_oa": sin_oa_examen})
    assert (totales["guias"], totales["oa"], totales["banco"]) == (58, 410, 3115)
    assert (totales["pruebas"], totales["preguntas_pruebas"]) == (156, 1825)
    assert (totales["examenes"], totales["preguntas_examenes"]) == (50, 1210)
