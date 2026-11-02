import re
import sys
from fractions import Fraction

import pytest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))

from parser_prueba_examen import parsear_prueba_o_examen


def test_matematica_5b_p9_tiene_una_sola_alternativa_decimal_equivalente():
    ruta = Path(__file__).resolve().parents[2] / "contenido/05-basico/pruebas/matematica-unidad-numeros-y-operaciones.md"
    pregunta, pauta = next(
        (p, r) for p, r in parsear_prueba_o_examen(ruta.read_text(encoding="utf-8"))
        if p.numero == 9
    )
    assert "3/10" in pregunta.enunciado
    assert pregunta.tipo == "alternativas"
    correctas = [chr(97 + i) for i, opcion in enumerate(pregunta.opciones)
                 if Fraction(opcion.replace(",", ".")) == Fraction(3, 10)]
    assert correctas == ["a"]
    assert pauta.respuesta_correcta == pregunta.opciones[0]
    assert Fraction("0.30") == Fraction(3, 10)
    assert Fraction(pregunta.opciones[3].replace(",", ".")) != Fraction(3, 10)


@pytest.mark.parametrize("etiqueta", ["Verdadero o falso", "V/F"])
def test_vf_sin_justificacion_ofrece_opciones_autocorregibles(etiqueta):
    texto = f"**1. ({etiqueta})** Dos más dos son cuatro.\n## Pauta de respuestas\n1. Verdadero. La suma es cuatro."
    pregunta, pauta = parsear_prueba_o_examen(texto)[0]
    assert pregunta.tipo == "verdadero_falso"
    assert pregunta.opciones == ["Verdadero", "Falso"]
    assert pauta.respuesta_correcta == "Verdadero"
    assert "La suma es cuatro" in pauta.retroalimentacion


@pytest.mark.parametrize("opciones", ["", "\na) Verdadero\nb) Falso"])
@pytest.mark.parametrize("instruccion", ["Justifica tu respuesta.", "Explica por qué.", "Corrige la afirmación si es falsa.", "Explain your answer.", "Justify your choice.", "Correct the statement if false."])
def test_vf_con_respuesta_escrita_permanece_manual(instruccion, opciones):
    texto = f"**1. (Verdadero o falso)** Dos más dos son cuatro. {instruccion}{opciones}\n## Pauta de respuestas\n1. Verdadero. Explica la suma."
    pregunta, pauta = parsear_prueba_o_examen(texto)[0]
    assert pregunta.tipo == "desarrollo_breve"
    assert pregunta.opciones is None
    assert "Explica la suma" in pauta.retroalimentacion


def test_vf_real_matematica_tercero_medio_se_clasifica_como_cerrado():
    ruta = Path(__file__).resolve().parents[2] / "contenido/03-medio/pruebas/matematica-unidad-geometria.md"
    preguntas = parsear_prueba_o_examen(ruta.read_text(encoding="utf-8"))
    assert all(preguntas[i][0].tipo == "verdadero_falso" for i in (1, 10))


@pytest.mark.parametrize("clave,esperada", [("True (Verdadero). Explicación.", "Verdadero"), ("False (Falso). Explicación.", "Falso"), ("V (Verdadero). Explicación.", "Verdadero"), ("F (Falso). Explicación.", "Falso")])
def test_vf_bilingue_normaliza_solo_clave_y_conserva_explicacion(clave, esperada):
    texto = f"**1. (V/F)** Read the statement.\n## Pauta de respuestas\n1. {clave}"
    pregunta, pauta = parsear_prueba_o_examen(texto)[0]
    assert pauta.respuesta_correcta == esperada
    assert pauta.respuesta_correcta in pregunta.opciones
    assert "Explicación" in pauta.retroalimentacion


def test_oa_principal_explicito_en_pauta_no_contamina_rubrica():
    texto = "**1. (Desarrollo)** Explica.\n## Pauta de respuestas\n1. Una explicación completa.\n**OA principal:** OA 2 (Módulo 3)\n"
    _, pauta = parsear_prueba_o_examen(texto)[0]
    assert (pauta.codigo_oa, pauta.modulo, pauta.codigos_oa) == ("OA 2", "3", ("OA 2",))
    assert pauta.respuesta_correcta == "Una explicación completa."
    assert pauta.retroalimentacion == "Una explicación completa."


@pytest.mark.parametrize("marcas", ["**OA principal:** OA 1 y OA 2", "**OA principal:** sin definir", "**OA principal:** OA 1\n**OA principal:** OA 2"])
def test_oa_principal_invalido_o_duplicado_se_rechaza(marcas):
    texto = f"**1. (Desarrollo)** Explica.\n## Pauta de respuestas\n1. Respuesta.\n{marcas}\n"
    with pytest.raises(ValueError, match="OA principal"):
        parsear_prueba_o_examen(texto)


def test_mencion_de_oa_en_prosa_no_inventa_principal():
    texto = "**1. (Desarrollo)** Explica.\n## Pauta de respuestas\n1. Compara los enfoques de OA 1 y OA 2."
    assert parsear_prueba_o_examen(texto)[0][1].codigo_oa is None


def test_lecturas_compartidas_reales_se_conservan_sin_contaminar_opciones():
    ruta = Path(__file__).resolve().parents[2] / "contenido/01-basico/pruebas/lenguaje-y-comunicacion-unidad-2.md"
    preguntas = {p.numero: p for p, _ in parsear_prueba_o_examen(ruta.read_text(encoding="utf-8"))}
    assert all("Fui a jugar a la plaza con Tomás" in preguntas[n].enunciado for n in (1, 2))
    assert preguntas[2].opciones == ["A las 5", "A las 6", "A las 7"]
    assert "Ponte jabón" in preguntas[3].enunciado
    assert "Camila" not in preguntas[3].enunciado
    assert "Ponte jabón" not in preguntas[4].enunciado
    assert "\n>" in preguntas[1].enunciado


@pytest.mark.parametrize("unidad,ultimo", [(1, 12), (2, 14)])
def test_lengua_cuarto_medio_conserva_estimulos_en_todo_el_grupo(unidad, ultimo):
    ruta = Path(__file__).resolve().parents[2] / f"contenido/04-medio/pruebas/lengua-y-literatura-unidad-{unidad}.md"
    preguntas = dict((p.numero, p) for p, _ in parsear_prueba_o_examen(ruta.read_text(encoding="utf-8")))
    assert "Lee los" in preguntas[1].enunciado
    assert "Lee los" in preguntas[ultimo].enunciado
    assert all("\n" in preguntas[n].enunciado for n in range(1, ultimo + 1))


def test_graficos_compartidos_no_se_pegan_a_alternativas_previas():
    ruta = Path(__file__).resolve().parents[2] / "contenido/04-basico/pruebas/matematica-unidad-medicion-datos-probabilidades.md"
    preguntas = {p.numero: p for p, _ in parsear_prueba_o_examen(ruta.read_text(encoding="utf-8"))}
    assert preguntas[7].opciones == ["3", "6", "2", "9"]
    assert "Mascota" not in preguntas[6].enunciado
    assert "| Mascota |" in preguntas[7].enunciado
    assert all("ventas de helados" in preguntas[n].enunciado for n in (8, 9))


def test_lecturas_cuarto_basico_llegan_a_las_preguntas_correctas():
    carpeta = Path(__file__).resolve().parents[2] / "contenido/04-basico/pruebas"
    primera = {p.numero: p for p, _ in parsear_prueba_o_examen((carpeta / "lenguaje-y-comunicacion-unidad-1.md").read_text(encoding="utf-8"))}
    segunda = {p.numero: p for p, _ in parsear_prueba_o_examen((carpeta / "lenguaje-y-comunicacion-unidad-2.md").read_text(encoding="utf-8"))}
    assert "Valentina vivía" in primera[1].enunciado
    assert "El volcán se puso su manto blanco" in primera[6].enunciado
    assert "Valentina vivía" not in primera[6].enunciado
    assert "Puma concolor" in segunda[1].enunciado
    assert "Puma concolor" not in segunda[6].enunciado


@pytest.mark.parametrize("unidad", [1, 2])
def test_textos_primero_medio_no_contaminan_grupos_anteriores(unidad):
    ruta = Path(__file__).resolve().parents[2] / f"contenido/01-medio/pruebas/lengua-y-literatura-unidad-{unidad}.md"
    preguntas = {p.numero: p for p, _ in parsear_prueba_o_examen(ruta.read_text(encoding="utf-8"))}
    assert "## Texto 1" in preguntas[1].enunciado
    assert "## Texto 2" not in preguntas[5].enunciado
    assert "## Texto 2" in preguntas[6].enunciado
    assert "## Texto 3" not in preguntas[10].enunciado
    assert "## Texto 3" in preguntas[11].enunciado


def test_pubertad_sexto_basico_no_presenta_vello_facial_como_exclusivo():
    ruta = Path(__file__).resolve().parents[2] / "contenido/06-basico/pruebas/ciencias-naturales-unidad-ciencias-de-la-vida.md"
    pregunta, pauta = next((p, r) for p, r in parsear_prueba_o_examen(ruta.read_text(encoding="utf-8")) if p.numero == 9)
    assert "exclusivos" not in pregunta.enunciado
    assert "no es exclusivo" in pauta.retroalimentacion


def test_ingles_primero_medio_comprension_no_depende_de_porcentaje_de_oxigeno():
    raiz = Path(__file__).resolve().parents[2] / "contenido/01-medio"
    texto = (raiz / "pruebas/ingles-unidad-1.md").read_text(encoding="utf-8")
    pregunta, pauta = next((p, r) for p, r in parsear_prueba_o_examen(texto) if p.numero == 3)
    assert "helps regulate the climate" in pregunta.enunciado
    assert "has no role in regulating the climate" in pregunta.enunciado
    assert pauta.respuesta_correcta == "Falso"
    assert "oxígeno" not in pauta.retroalimentacion
    guia = (raiz / "ingles.md").read_text(encoding="utf-8")
    assert "helps regulate the climate" in guia
    assert "La contribución bruta real es ~6-9%" not in guia


def test_contexto_con_rango_inexistente_se_rechaza():
    texto = "Lee este texto y responde las preguntas 1 a 999999:\n> Texto.\n**1. (Desarrollo)** Explica."
    with pytest.raises(ValueError, match="estímulo"):
        parsear_prueba_o_examen(texto)


def test_mapa_oa_por_pregunta_es_explicito_y_no_modifica_clave():
    texto = '---\noa_por_pregunta: {"1": "OA 2 (Módulo 3)"}\n---\n**1. (Desarrollo)** Explica.\n## Pauta de respuestas\n1. Respuesta completa.'
    pregunta, pauta = parsear_prueba_o_examen(texto)[0]
    assert (pauta.codigo_oa, pauta.modulo) == ("OA 2", "3")
    assert pauta.respuesta_correcta == "Respuesta completa."
    assert pregunta.enunciado == "Explica."


@pytest.mark.parametrize("mapa", ['{"1":"OA 1","1":"OA 2"}', '{"2":"OA 1"}', '{"1":"OA 1 y OA 2"}', '{"1":null}', '["OA 1"]'])
def test_mapa_oa_invalido_se_rechaza(mapa):
    texto = f'---\noa_por_pregunta: {mapa}\n---\n**1. (Desarrollo)** Explica.\n## Pauta de respuestas\n1. Respuesta.'
    with pytest.raises(ValueError, match="Mapa OA"):
        parsear_prueba_o_examen(texto)


def test_barra_condicional_escapada_no_desplaza_columnas_de_la_pauta():
    texto = r"""
**1. (Desarrollo breve)** Calcula una probabilidad condicional.
## Pauta de respuestas
| N° | Clave / Respuesta esperada | OA |
|---|---|---|
| 1 | P(A\|B) = 0,5; P(B\|A) = 0,25. | OA 2 |
"""
    _, pauta = parsear_prueba_o_examen(texto)[0]
    assert pauta.codigo_oa == "OA 2"
    assert pauta.respuesta_correcta == r"P(A\|B) = 0,5; P(B\|A) = 0,25."


@pytest.mark.parametrize("curso,numero,resultado", [
    ("03-medio", 23, "5/14"),
    ("03-medio", 25, "0,124 (12,4%)"),
    ("04-medio", 25, "0,078 (7,8%)"),
])
def test_pautas_reales_de_probabilidad_conservan_desarrollo_y_oa(curso, numero, resultado):
    ruta = Path(__file__).resolve().parents[2] / "contenido" / curso / "examenes/matematica-examen-forma-b.md"
    preguntas = parsear_prueba_o_examen(ruta.read_text(encoding="utf-8"))
    pauta = next(pauta for pregunta, pauta in preguntas if pregunta.numero == numero)
    assert pauta.codigo_oa == "OA 2"
    assert resultado in pauta.respuesta_correcta
    assert resultado in pauta.retroalimentacion
    assert r"\|" in pauta.respuesta_correcta


@pytest.mark.parametrize("curso,esperados", [
    ("03-medio", ["OA 1"] * 6 + ["OA 3"] * 6 + ["OA 4"] * 6 + ["OA 6"] * 7),
    ("04-medio", ["OA 1"] * 6 + ["OA 2"] * 7 + ["OA 4"] * 6 + ["OA 5"] * 6),
])
def test_filosofia_conserva_oa_del_bloque_en_pautas_narrativas(curso, esperados):
    ruta = Path(__file__).resolve().parents[2] / "contenido" / curso / "examenes/filosofia-examen-forma-b.md"
    preguntas = parsear_prueba_o_examen(ruta.read_text(encoding="utf-8"))
    assert [pauta.codigo_oa for _, pauta in preguntas] == esperados


def test_objetivo_de_un_encabezado_no_se_propaga_a_su_siguiente_seccion():
    texto = """
## OA 1 — Primera sección
### Desarrollo
**1. (Desarrollo breve)** Explica una idea.
## Otra sección sin OA declarado
**2. (Desarrollo breve)** Explica otra idea.
## Pauta de respuestas
1. Primera explicación.
2. Segunda explicación.
"""
    preguntas = parsear_prueba_o_examen(texto)
    assert preguntas[0][1].codigo_oa == "OA 1"
    assert preguntas[1][1].codigo_oa is None


def test_encabezado_con_varios_objetivos_no_elige_el_primero():
    texto = """
## Lectura — OA 9 y 10
**1. (Desarrollo breve)** Explica el texto.
## Pauta de respuestas
1. Explicación.
"""
    pauta = parsear_prueba_o_examen(texto)[0][1]
    assert pauta.codigo_oa is None
    assert pauta.codigos_oa == ("OA 9", "OA 10")


def test_tabla_con_varios_objetivos_no_inventa_un_objetivo_principal():
    texto = """
**1. (Desarrollo breve)** Explica el texto.
## Pauta de respuestas
| N° | Respuesta esperada | OA |
|---|---|---|
| 1 | Explicación. | OA 9, OA 10 |
"""
    pauta = parsear_prueba_o_examen(texto)[0][1]
    assert pauta.codigo_oa is None
    assert pauta.codigos_oa == ("OA 9", "OA 10")


@pytest.mark.parametrize("unidad,codigo", [
    ("algebra-y-funciones", "OA 3"),
    ("geometria", "OA 4"),
    ("probabilidad-y-estadistica", "OA 2"),
])
def test_objetivo_declarado_en_eje_de_metadatos_se_conserva(unidad, codigo):
    ruta = Path(__file__).resolve().parents[2] / "contenido/03-medio/pruebas" / f"matematica-unidad-{unidad}.md"
    preguntas = parsear_prueba_o_examen(ruta.read_text(encoding="utf-8"))
    assert len(preguntas) == 14
    assert all(pauta.codigo_oa == codigo for _, pauta in preguntas)


def test_modelos_y_probabilidad_explicitan_condiciones_de_validez():
    carpeta = Path(__file__).resolve().parents[2] / "contenido/03-medio"
    guia = (carpeta / "matematica.md").read_text(encoding="utf-8")
    algebra = parsear_prueba_o_examen((carpeta / "pruebas/matematica-unidad-algebra-y-funciones.md").read_text(encoding="utf-8"))
    probabilidad = parsear_prueba_o_examen((carpeta / "pruebas/matematica-unidad-probabilidad-y-estadistica.md").read_text(encoding="utf-8"))
    assert "a>0" in algebra[1][0].enunciado
    assert "tasa de crecimiento" in algebra[1][0].enunciado
    assert "P(B)>0" in probabilidad[9][0].enunciado
    assert "a>0 y b>1" in guia
    assert "P(B)>0" in guia


def test_encabezado_del_siguiente_oa_no_se_agrega_a_la_ultima_opcion():
    texto = """
**1. (Alternativas)** Choose a greeting.
a) Good morning.
b) Good night.
c) Goodbye.
d) Have a wonderful
   afternoon.

---

## OA 14 — Writing following a model

**2. (Desarrollo)** Write a greeting.

## PAUTA DE CORRECCIÓN
| N° | Respuesta esperada | OA |
|---|---|---|
| 1 | d) Have a wonderful afternoon. | OA6 |
| 2 | Good morning. | OA14 |
"""
    resultado = parsear_prueba_o_examen(texto)
    assert len(resultado) == 2
    pregunta, pauta = resultado[0]
    assert pregunta.opciones == [
        "Good morning.", "Good night.", "Goodbye.", "Have a wonderful afternoon."
    ]
    assert pauta.respuesta_correcta == "Have a wonderful afternoon."
    assert resultado[1][0].enunciado == "Write a greeting."


TEXTO_CON_INSTRUCCIONES = """
## Instrucciones para el estudiante

1. Este examen contiene **2 preguntas** y tiene una duración de 90 minutos.
2. Se permite el uso de calculadora.

## PREGUNTAS

**1. (Matemática)** ¿Cuánto es 2 + 2?

a) 3
b) 4
c) 5
d) 6

**2. (Historia)** ¿Verdadero o falso: Chile está en Sudamérica?

## Pauta de respuestas

**1.** b) 4 — Suma básica.
**2.** Verdadero — Chile está en el continente sudamericano.
"""


def test_las_instrucciones_numeradas_no_se_cuelan_como_preguntas():
    """Bug real encontrado simulando un examen completo (2026-08-13): las instrucciones
    numeradas al inicio del examen ("1. Este examen contiene...", "2. Se permite...") se
    parseaban como preguntas falsas, desalineando toda la pauta de respuestas con las
    preguntas reales. Las preguntas reales siempre empiezan la línea con "**" (negrita);
    las instrucciones no."""
    resultado = parsear_prueba_o_examen(TEXTO_CON_INSTRUCCIONES)

    assert len(resultado) == 2
    enunciados = [p.enunciado for p, _ in resultado]
    assert not any("contiene" in e.lower() or "duración" in e.lower() for e in enunciados)
    assert "2 + 2" in enunciados[0]

    pregunta_1, pauta_1 = resultado[0]
    assert pauta_1 is not None
    # La pauta trae la letra ("b") pero IntentoEvaluacion.entregar() compara contra el
    # TEXTO de la opción que el alumno clickeó — la letra sola nunca podría calzar
    # (bug real encontrado simulando un examen con las respuestas correctas reales:
    # 0/12 correctas pese a responder exactamente lo que decía la pauta).
    assert pauta_1.respuesta_correcta == "4"

    pregunta_2, pauta_2 = resultado[1]
    assert pauta_2 is not None
    assert pauta_2.respuesta_correcta.lower().startswith("verdadero")


TEXTO_OPCION_CON_WORD_WRAP = """
**Pregunta 1 (alternativas).** ¿Cuál de las siguientes NO corresponde?

a) Superar la ignorancia.
b) Predecir con exactitud eventos futuros mediante experimentos
   controlados.
c) Enfrentar problemas complejos.
d) Liberarnos de prejuicios y costumbres.

## Pauta de respuestas

**1.** b) Predecir con exactitud eventos futuros mediante experimentos controlados.
"""


def test_opcion_con_word_wrap_no_contamina_el_enunciado():
    """Mismo bug que en parser_contenido.py, encontrado en pruebas/exámenes también."""
    resultado = parsear_prueba_o_examen(TEXTO_OPCION_CON_WORD_WRAP)
    pregunta, pauta = resultado[0]
    assert pregunta.enunciado == "¿Cuál de las siguientes NO corresponde?"
    assert pregunta.opciones[1] == "Predecir con exactitud eventos futuros mediante experimentos controlados."


TEXTO_PREGUNTA_DE_EMPAREJAMIENTO = """
**3. (Relacionar / emparejar)** Une cada situación con la norma que corresponde:

1) Cruzar una calle con autos — 2) Hablar en clases mientras el profesor explica — 3) Visitar
un monumento histórico

a) No rayarlo ni dañarlo — b) Levantar la mano y esperar mi turno — c) Mirar hacia ambos lados

## Pauta de respuestas

**3.** 1-c, 2-b, 3-a. Cada situación tiene una norma distinta según el contexto.
"""


def test_pregunta_de_emparejamiento_no_se_reclasifica_como_alternativas_rota():
    """Bug real de contenido (73 preguntas en pruebas/exámenes, mismo bug que en
    parser_contenido.py): RE_OPCION confunde la línea en línea de definiciones
    ("a) A — b) B — c) C") con una alternativa real, dejando una sola opción ilegible y
    una pauta ("1-c, 2-b, 3-a") que nunca calza con ninguna opción clickeable — deben
    quedar como desarrollo_breve con el enunciado completo."""
    resultado = parsear_prueba_o_examen(TEXTO_PREGUNTA_DE_EMPAREJAMIENTO)
    pregunta, pauta = resultado[0]
    assert pregunta.tipo == "desarrollo_breve"
    assert pregunta.opciones is None
    assert "No rayarlo ni dañarlo" in pregunta.enunciado
    assert pauta is not None
    assert pauta.respuesta_correcta.startswith("1-c, 2-b, 3-a")


TEXTO_PAUTA_LETRA_CON_EM_DASH = """
**1. (Alternativas)** ¿Qué figura literaria usa "las manos del reloj corrían"?

a) Personificación
b) Metáfora
c) Hipérbole
d) Pregunta retórica

## Pauta de respuestas

**1.** b — se identifican directamente dos términos (las manos = manecillas), sin usar
"como" ni verbos de acción atribuidos a un objeto inanimado.
"""


def test_pauta_con_letra_y_em_dash_se_resuelve_al_texto_de_la_opcion():
    """Bug real (7 preguntas de 3°-4° medio): la pauta a veces escribe la letra seguida de
    un em-dash y la explicación ("b — se identifican...") en vez de "b." o "b)" — sin
    tolerar esa forma, RE_LETRA_INICIAL no reconocía la letra y el texto completo
    (truncado a 60 caracteres) quedaba como respuesta_correcta, sin calzar nunca con
    ninguna opción real."""
    resultado = parsear_prueba_o_examen(TEXTO_PAUTA_LETRA_CON_EM_DASH)
    pregunta, pauta = resultado[0]
    assert pauta is not None
    assert pauta.respuesta_correcta == "Metáfora"


TEXTO_EMPAREJAMIENTO_SIN_ETIQUETA = """
**4.** Une cada derecho del niño con un ejemplo de cómo se garantiza en Chile:

1) Derecho a la educación — 2) Derecho a la alimentación — 3) Derecho a la protección frente al trabajo infantil

a) Prohibición legal de que los niños trabajen antes de cierta edad — b) Educación gratuita y obligatoria — c) Programas de alimentación escolar, como los de JUNAEB

1) ___  2) ___  3) ___

## Pauta de respuestas

| N° | Respuesta correcta |
|----|---------------------|
| 4  | 1-b (educación — educación gratuita y obligatoria), 2-c (alimentación — programas como JUNAEB), 3-a (protección frente al trabajo infantil — prohibición legal) |
"""


def test_pregunta_de_emparejamiento_sin_etiqueta_se_detecta_por_estructura():
    """Bug real (30 preguntas restantes tras el fix por etiqueta): las pruebas de unidad a
    veces no traen ninguna etiqueta entre paréntesis (solo "**4.**"), así que detectar por
    la palabra "relacionar/emparejar" en la etiqueta no basta — hay que reconocer también
    la forma "a) ... — b) ..." (una línea con más de un marcador de letra pegado), que
    estructuralmente nunca ocurre en una alternativa real."""
    resultado = parsear_prueba_o_examen(TEXTO_EMPAREJAMIENTO_SIN_ETIQUETA)
    pregunta, pauta = resultado[0]
    assert pregunta.tipo == "desarrollo_breve"
    assert pregunta.opciones is None
    assert "Prohibición legal" in pregunta.enunciado


CONTENIDO = Path(__file__).resolve().parents[2] / "contenido"


def test_continuacion_numerica_no_sobrescribe_clave_de_biologia():
    texto = (CONTENIDO / "01-medio/pruebas/ciencias-naturales-unidad-biologia.md").read_text()
    resultado = {p.numero: (p, pauta) for p, pauta in parsear_prueba_o_examen(texto)}
    pregunta, pauta = resultado[5]
    assert pauta.respuesta_correcta == pregunta.opciones[1] == "Una población"
    assert "5.000 × 0,10 = 500 kcal disponibles." in resultado[10][1].retroalimentacion


def test_letra_sola_y_pautas_abiertas_con_vinetas_no_absorben_encabezados():
    texto = (CONTENIDO / "02-medio/pruebas/lengua-y-literatura-unidad-2.md").read_text()
    resultado = {p.numero: (p, pauta) for p, pauta in parsear_prueba_o_examen(texto)}
    pregunta, pauta = resultado[15]
    assert pauta.respuesta_correcta == pregunta.opciones[1]
    assert pauta.retroalimentacion == "b"
    for numero in (3, 4, 8, 9, 13, 14):
        esperado = re.search(rf"^- \*\*{numero}\.\*\* (.+)$", texto, re.MULTILINE).group(1)
        assert resultado[numero][1].respuesta_correcta == esperado
        assert resultado[numero][1].retroalimentacion == esperado


@pytest.mark.parametrize("curso,numero", [
    ("03-medio", n) for n in (4, 6, 10, 12, 16, 18, 24, 25)
] + [
    ("04-medio", n) for n in (4, 6, 12, 13, 18, 19, 23, 24, 25)
])
def test_rubricas_narrativas_integras_junto_a_tabla_de_claves(curso, numero):
    texto = (CONTENIDO / curso / "examenes/filosofia-examen-forma-b.md").read_text()
    resultado = {p.numero: (p, pauta) for p, pauta in parsear_prueba_o_examen(texto)}
    esperado = re.search(
        rf"^\*\*Pregunta {numero} \([^\n]+?\)\.\*\* (.+)$", texto, re.MULTILINE
    ).group(1).replace("*", "")
    pauta = resultado[numero][1]
    assert pauta is not None
    assert pauta.respuesta_correcta == esperado
    assert pauta.retroalimentacion == esperado
    for pregunta, clave in resultado.values():
        if pregunta.opciones:
            assert clave.respuesta_correcta in pregunta.opciones


TEXTO_RESPUESTA_EN_NEGRITA = """
**1. (Completar)** Complete the sentence with "about" or "how".

**2. (Verdadero o falso)** The sky is green.

## Pauta de respuestas

1. **about / how.**
   *About* introduce el tema; *how* introduce el modo.

2. **Falso.** El enunciado contradice el texto.

**Subtotal selección múltiple: 2 puntos.**
"""


def test_respuesta_en_linea_completamente_negrita_no_se_corta_como_encabezado():
    """Bug real (98 pautas vacías en ~20 archivos, ej. 01-medio/pruebas/ingles-unidad-1.md
    P2 "2. **about / how.**"): RE_PAUTA_LIMITE trataba CUALQUIER línea completamente en
    negrita como encabezado/subtotal y cortaba la entrada justo ahí — pero cuando la
    respuesta misma viene toda en negrita en la misma línea del número, el límite cae en
    la posición 0 y la pauta queda vacía. Solo deben cortar los encabezados reales de
    sección/subtotal."""
    resultado = parsear_prueba_o_examen(TEXTO_RESPUESTA_EN_NEGRITA)
    assert resultado[0][1].respuesta_correcta.startswith("about / how.")
    assert resultado[0][1].respuesta_correcta != ""
    assert resultado[1][1].respuesta_correcta.startswith("Falso")


def test_subtotal_en_negrita_sigue_cortando_la_entrada_anterior():
    """El límite no puede eliminarse del todo: los subtotales/totales de puntaje son
    líneas completamente en negrita que sí deben cortar la entrada anterior para no
    quedar pegados a su retroalimentación."""
    resultado = parsear_prueba_o_examen(TEXTO_RESPUESTA_EN_NEGRITA)
    assert "Subtotal" not in resultado[1][1].retroalimentacion


def test_prueba_real_ingles_1medio_unidad_1_no_deja_pautas_vacias():
    """Caso real: 10 de las 14 pautas de este archivo quedaban vacías porque la
    respuesta venía como línea completamente en negrita."""
    texto = (CONTENIDO / "01-medio/pruebas/ingles-unidad-1.md").read_text()
    resultado = {p.numero: (p, pauta) for p, pauta in parsear_prueba_o_examen(texto)}
    assert all(pauta.respuesta_correcta.strip() for _, pauta in resultado.values())
    assert resultado[2][1].respuesta_correcta.startswith("about / how.")
    assert resultado[3][0].tipo == "verdadero_falso"
    assert resultado[3][1].respuesta_correcta == "Falso"
    assert resultado[3][1].retroalimentacion.startswith("False (Falso)")
    assert resultado[8][1].respuesta_correcta == "To persuade/instruct"


TEXTO_RUBRICA_ANTES_DE_CLAVES = """
**1. (Alternativas)** ¿Cuál es la clave?

a) Opción A
b) Opción B
c) Opción C
d) Opción D

**5. (Desarrollo breve)** Compara los textos.

# PAUTA DE CORRECCIÓN

| Pregunta manual | Completo: 1 punto | Parcial: 0,5 puntos | Insuficiente: 0 puntos |
|---|---|---|---|
| 5 | Compara ambos textos con citas pertinentes. | Compara sin citas. | No compara. |

| N° | Clave / criterio de respuesta correcta | Objetivo de Aprendizaje evaluado |
|----|--------------------------------------|----------------------------------|
| 1 | **a)** La opción A es la correcta por X. | OA N°1 |
| 5 | Respuesta modelo completa del desarrollo. | OA N°1 |
"""


def test_tabla_de_claves_se_encuentra_aunque_haya_otra_tabla_antes():
    """Bug real (04-medio/examenes/lengua-y-literatura-examen-forma-b.md, 25 pautas
    perdidas): _extraer_pauta_tabla solo miraba la PRIMERA tabla del texto de pauta;
    si el examen abre con una rúbrica manual (o una grilla de respuestas vacía) y la
    tabla de claves viene después, devolvía {} y todas las pautas quedaban en None."""
    resultado = {p.numero: (p, pauta) for p, pauta in parsear_prueba_o_examen(TEXTO_RUBRICA_ANTES_DE_CLAVES)}
    assert resultado[1][1] is not None
    assert resultado[1][1].respuesta_correcta == "Opción A"
    assert resultado[5][1] is not None
    assert resultado[5][1].respuesta_correcta.startswith("Respuesta modelo completa")


def test_rubrica_manual_por_numero_se_conserva_sin_mezclar_vecinos():
    """La rúbrica manual (Completo/Parcial/Insuficiente) aporta criterios de corrección
    propios por pregunta — debe conservarse en la pauta de ESA pregunta, sin traspasar
    criterios a las entradas vecinas."""
    resultado = {p.numero: (p, pauta) for p, pauta in parsear_prueba_o_examen(TEXTO_RUBRICA_ANTES_DE_CLAVES)}
    assert "Insuficiente" in resultado[5][1].retroalimentacion
    assert "No compara" in resultado[5][1].retroalimentacion
    assert "No compara" not in resultado[1][1].retroalimentacion


def test_examen_real_4medio_lengua_forma_b_recupera_las_25_pautas():
    """Caso real: la pauta trae primero una grilla de respuestas vacía, luego la tabla
    de rúbrica manual y recién después la tabla de claves — se perdían las 25 pautas."""
    texto = (CONTENIDO / "04-medio/examenes/lengua-y-literatura-examen-forma-b.md").read_text()
    resultado = {p.numero: (p, pauta) for p, pauta in parsear_prueba_o_examen(texto)}
    assert len(resultado) == 25
    assert all(pauta is not None and pauta.respuesta_correcta.strip() for _, pauta in resultado.values())
    assert resultado[4][1].respuesta_correcta == "Falso"
    assert resultado[9][1].respuesta_correcta == resultado[9][0].opciones[3]
    # Rúbrica manual específica por número, sin mezclar criterios de vecinas
    assert "salitrero" in resultado[5][1].retroalimentacion
    assert "salitrero" not in resultado[4][1].retroalimentacion


@pytest.mark.parametrize("formato", ["lista", "tabla"])
def test_respuesta_abierta_larga_no_se_trunca(formato):
    esperado = "Una respuesta manual extensa que conserva íntegros todos sus criterios. " * 4
    esperado = esperado.strip()
    pauta = f"1. {esperado}" if formato == "lista" else (
        f"| N° | Respuesta esperada |\n|---|---|\n| 1 | {esperado} |"
    )
    texto = f"**1. (Desarrollo)** Explica.\n\n## Pauta de respuestas\n\n{pauta}"
    respuesta = parsear_prueba_o_examen(texto)[0][1]
    assert respuesta.respuesta_correcta == esperado
    assert respuesta.retroalimentacion == esperado
