import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))

from parser_contenido import parsear_guia

TEXTO_BASE = """
# Asignatura de prueba

## OA N°1: Objetivo de ejemplo

Contenido de la guía.

### Banco de preguntas de autoevaluación — OA N°1

**1. (Alternativas)** ¿Cuánto es 2 + 2?

a) 3
b) 4
c) 5
d) 6

*Respuesta correcta: b.* Retroalimentación: suma básica.

**2. (Alternativas)** ¿Cuál es la capital de Francia?

a) Madrid
b) Roma
c) París
d) Berlín

**Respuesta correcta: c) París.**
**Retroalimentación:** es la capital de Francia.

**3. (Verdadero o Falso)** El cielo es azul.

✅ Respuesta correcta: **Verdadero**
💬 *Retroalimentación:* en un día despejado, el cielo se ve azul.
"""


def test_respuesta_solo_letra_se_resuelve_al_texto_de_la_opcion():
    """Bug real (2026-08-13): la pauta a veces solo trae la letra ("b."), sin repetir el
    texto de la opción — pero el alumno siempre responde con el texto completo, nunca
    con la letra. Sin resolver la letra acá, ninguna alternativa se podría corregir bien."""
    objetivos = parsear_guia(TEXTO_BASE)
    preguntas = objetivos[0].preguntas
    assert preguntas[0].respuesta_correcta == "4"
    assert preguntas[0].respuesta_correcta in preguntas[0].opciones


def test_respuesta_letra_mas_texto_repetido_tambien_se_resuelve():
    """Otras preguntas repiten el texto tras la letra ("c) París") — también hay que
    resolver por la letra, no confiar en el texto repetido (puede traer el prefijo
    "c) " que no calza exactamente con la opción tal como está en `opciones`)."""
    objetivos = parsear_guia(TEXTO_BASE)
    preguntas = objetivos[0].preguntas
    assert preguntas[1].respuesta_correcta == "París"


def test_emoji_de_vineta_no_contamina_la_respuesta():
    """Bug real: "💬 Retroalimentación:" en su propia línea dejaba el emoji pegado al
    final de respuesta_correcta ("Verdadero 💬"), rompiendo la comparación exacta."""
    objetivos = parsear_guia(TEXTO_BASE)
    preguntas = objetivos[0].preguntas
    assert preguntas[2].respuesta_correcta == "Verdadero"


TEXTO_INGLES = """
# Inglés de prueba

## OA N°1: Objetivo de ejemplo

Contenido.

### Banco de preguntas de autoevaluación — OA N°1

**1. (Verdadero o Falso)** Chile is in South America.

**Respuesta correcta:** True (Verdadero).
**Retroalimentación:** correcto.

**2. (Verdadero o Falso)** The sky is green.

**Respuesta correcta:** False (Falso).
**Retroalimentación:** el cielo es azul, no verde.
"""


def test_verdadero_falso_bilingue_se_normaliza_al_espanol():
    """El contenido de Inglés a veces escribe la respuesta en inglés/bilingüe
    ("True (Verdadero)") — las opciones reales que el alumno clickea son siempre
    "Verdadero"/"Falso" en español, hay que normalizar."""
    objetivos = parsear_guia(TEXTO_INGLES)
    preguntas = objetivos[0].preguntas
    assert preguntas[0].respuesta_correcta == "Verdadero"
    assert preguntas[1].respuesta_correcta == "Falso"


TEXTO_OPCION_CON_WORD_WRAP = """
# Asignatura de prueba

## OA N°1: Objetivo de ejemplo

Contenido.

### Banco de preguntas de autoevaluación — OA N°1

**1. (Alternativas)** ¿Cuál de las siguientes NO corresponde a una de ellas?

a) Superar la ignorancia.
b) Predecir con exactitud eventos futuros mediante experimentos
   controlados.
c) Enfrentar problemas complejos.
d) Liberarnos de prejuicios y costumbres.

**Respuesta correcta:** b.
**Retroalimentación:** predecir es propio del método científico.
"""


def test_opcion_que_se_ajusta_a_dos_lineas_no_contamina_el_enunciado():
    """Bug real (2026-08-13, simulando 4° medio): una opción larga que se ajusta
    ("word-wrap") a la línea siguiente sin repetir "b)" hacía que esa segunda línea se
    pegara al ENUNCIADO en vez de a la opción — el alumno veía "¿cuál de las siguientes NO
    corresponde a una de ellas? controlados." como pregunta, con una opción "b" truncada."""
    objetivos = parsear_guia(TEXTO_OPCION_CON_WORD_WRAP)
    pregunta = objetivos[0].preguntas[0]
    assert pregunta.enunciado == "¿Cuál de las siguientes NO corresponde a una de ellas?"
    assert pregunta.opciones[1] == "Predecir con exactitud eventos futuros mediante experimentos controlados."
    assert pregunta.respuesta_correcta == pregunta.opciones[1]


TEXTO_EMOJI_ANTES_DE_RESPUESTA = """
# Asignatura de prueba

## OA N°1: Objetivo de ejemplo

Contenido.

### Banco de preguntas de autoevaluación — OA N°1

**1. (Alternativas)** ¿En qué cordillera se desarrolló el imperio inca?

a) Alpes
b) Andes
c) Himalaya
d) Montes Urales

✅ Respuesta correcta: **b) Andes**
💬 *Retroalimentación:* los incas se desarrollaron en la cordillera de los Andes.
"""


def test_emoji_antes_de_respuesta_correcta_no_contamina_la_ultima_opcion():
    """Bug real de seguridad de contenido (encontrado con QA de coherencia, 2026-08-14,
    curso 4° básico completo): a diferencia de RE_RETRO_MARCA y RE_PAUTA_MARCA,
    RE_RESPUESTA_MARCA no toleraba un emoji de viñeta ("✅ Respuesta correcta:") antes del
    marcador — el "✅ " quedaba pegado a la ÚLTIMA opción vista ("Montes Urales ✅"),
    mostrando una alternativa incorrecta marcada con un check visualmente confuso.
    Afectaba de forma sistemática TODA la asignatura de Historia de 4° básico."""
    objetivos = parsear_guia(TEXTO_EMOJI_ANTES_DE_RESPUESTA)
    pregunta = objetivos[0].preguntas[0]
    assert pregunta.opciones == ["Alpes", "Andes", "Himalaya", "Montes Urales"]
    assert "✅" not in pregunta.opciones[-1]
    assert pregunta.respuesta_correcta == "Andes"


TEXTO_CON_GLOSARIO = """
# Asignatura de prueba

## OA N°1: Objetivo de ejemplo

Contenido.

### Banco de preguntas de autoevaluación — OA N°1

**1. (Verdadero o Falso)** El agua moja.

**Respuesta correcta:** Verdadero.
**Retroalimentación:** el agua es un líquido.

## Glosario

- Líquido: estado de la materia que fluye y toma la forma de su recipiente.
- Sólido: estado de la materia que mantiene su forma.
"""


def test_glosario_al_final_del_archivo_no_contamina_la_ultima_pregunta():
    """Bug real (encontrado con QA de coherencia, 2026-08-14): el glosario al final del
    archivo no tiene un heading de Eje/OA después que cierre el bloque de preguntas
    anterior, así que todo su texto quedaba pegado a la retroalimentación de la ÚLTIMA
    pregunta de cada asignatura — un alumno viendo el resultado de esa pregunta se
    encontraba con un diccionario completo de 15-20 términos pegado a la explicación."""
    objetivos = parsear_guia(TEXTO_CON_GLOSARIO)
    pregunta = objetivos[0].preguntas[0]
    assert pregunta.retroalimentacion == "el agua es un líquido."
    assert "Glosario" not in pregunta.retroalimentacion
    assert "Líquido:" not in pregunta.retroalimentacion


TEXTO_ETIQUETA_NO_ALTERNATIVAS_CON_OPCIONES_REALES = """
# Asignatura de prueba

## OA N°1: Objetivo de ejemplo

Contenido.

### Banco de preguntas de autoevaluación — OA N°1

**1. (reconocer la operación).** Pedro tenía $850 y gastó $320. ¿Qué operación permite
saber cuánto dinero le queda?

a) Adición
b) Sustracción
c) Multiplicación
d) División

**Respuesta correcta: b) Sustracción.**
**Retroalimentación:** "le queda" indica una resta.
"""


def test_etiqueta_no_alternativas_con_opciones_reales_se_reclasifica_como_alternativas():
    """Bug real de contenido (encontrado con QA de coherencia, 2026-08-14, asignatura
    Matemática de 4° básico): varias preguntas rotuladas con una etiqueta distinta a
    "(Alternativas)" (ej. "(reconocer la operación)") SÍ tenían opciones a)/b)/c)/d)
    reales en el cuerpo, pero `_clasificar_tipo` solo mira el texto del rótulo y las
    dejaba como "desarrollo_breve" — el alumno nunca veía las alternativas, solo un
    campo de texto libre, con la "respuesta esperada" mostrando el fragmento sin sentido
    "b) Sustracción" en vez de una explicación completa."""
    objetivos = parsear_guia(TEXTO_ETIQUETA_NO_ALTERNATIVAS_CON_OPCIONES_REALES)
    pregunta = objetivos[0].preguntas[0]
    assert pregunta.tipo == "alternativas"
    assert pregunta.opciones == ["Adición", "Sustracción", "Multiplicación", "División"]
    assert pregunta.respuesta_correcta == "Sustracción"
