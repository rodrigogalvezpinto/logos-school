"""Parser tolerante del contenido Markdown ya escrito en contenido/{curso}/*.md.

Ver planificacion/11-especificacion-mvp-para-desarrollo.md (Paso 3 del plan de
desarrollo aprobado) — decisión: parser regex tolerante en vez de reescribir el
contenido a mano, con validación de conteo obligatoria contra
contenido/00-estado-contenido.md.

Nota real (descubierta al implementar, no asumida de antemano): el contenido de los
distintos archivos NO sigue un único formato exacto para preguntas — hay al menos 3
variantes de cómo se marcan "Pregunta N (tipo)" y "Respuesta/Retroalimentación"
(negrita vs. cursiva, en la misma línea vs. líneas separadas, con o sin la palabra
"Pregunta"). Por eso el parser busca marcadores de texto (case-insensitive, tolerante
a **/*), no líneas exactas — así cubre las variantes ya encontradas y es más robusto
a nuevas variantes menores en el resto de los 12 cursos.
"""

import re
from dataclasses import dataclass, field

RE_EJE = re.compile(r"^##\s+Eje\s+\d+\s*[:\-]?\s*(.+)$")
# El glosario, al final del archivo, no tiene un heading de Eje/OA después que cierre el
# bloque de preguntas anterior — sin este marcador, todo su texto quedaba pegado a la
# retroalimentación de la última pregunta del archivo (bug real encontrado con QA de
# coherencia: la última pregunta de cada asignatura mostraba el glosario completo).
RE_GLOSARIO_HEADING = re.compile(r"^##\s+Glosario\b", re.IGNORECASE)
RE_OA_HEADING = re.compile(
    # Acepta "## OA 6: ...", "## OA N°6: ..." y, para el único caso del corpus sin
    # número oficial (4° medio Educación Ciudadana, temario cortado en el PDF),
    # "## OA (Democracia y sus desafíos): ...". Sin la rama del paréntesis, ese OA
    # se descartaba silenciosamente y la BD quedaba con 407 de los 408 OA.
    r"^(##|###)\s+OA\s*(?:N?°?\s*(\d+)|\(([^)]+)\))\s*[:\-—]*\s*(.*)$",
    re.IGNORECASE,
)
RE_AUTOEVAL_HEADING = re.compile(r"^(##|###|####)\s+.*autoevaluaci[oó]n.*$", re.IGNORECASE)
RE_AUTOEVAL_BOLD_PARRAFO = re.compile(r"^\*\*.*autoevaluaci[oó]n.*\*\*$", re.IGNORECASE)

# Inicio de pregunta: tolera "**Pregunta 1 (alternativas).**", "**1. (Alternativas)**"
# y "1. *(Alternativas)*" — con 0 a 2 asteriscos antes/después del número y del tipo.
RE_Q_START = re.compile(
    r"(?m)^\s*\*{0,2}(?:Pregunta\s+)?(\d+)\.?\s*\*{0,2}\(([^)]+)\)\*{0,2}\.?\s*"
)
RE_OPCION = re.compile(r"^\s*[a-d]\)\s+(.*)$")
RE_RESPUESTA_MARCA = re.compile(
    r"(?i)[^\w\s]{0,2}\s*Respuesta\s+(?:correcta|esperada)\**:?\**\s*"
)
## Algunos archivos anteponen un emoji de viñeta ("💬 Retroalimentación:") en su propia
# línea, justo después de la respuesta — sin el `[^\w\s]{0,2}\s*` inicial, ese emoji queda
# pegado dentro de `respuesta_correcta` (ej. "Falso 💬") y ya no calza con ninguna opción.
# El emoji y el "*" de negrita a veces van separados por un espacio ("💬 *Retroalimentación:*")
# — con un solo grupo `[^\w\s]{0,2}` eso no calzaba (el espacio corta la racha de símbolos)
# y el emoji quedaba pegado al final de `respuesta_correcta` (ej. "1-b, 2-c, 3-a 💬"). Se
# repite el grupo símbolo+espacio hasta 2 veces para tolerar ambos símbolos por separado.
RE_RETRO_MARCA = re.compile(r"(?i)(?:[^\w\s]\s*){0,2}Retroalimentaci[oó]n:?\s*")
# Preguntas de "relacionar / emparejar" (unir concepto con definición): el autor escribe dos
# listas en línea separadas por em-dash, ej. "a) Adaptación... — b) Establecerse... — c)
# Cantidad...". RE_OPCION las confunde con alternativas reales (matchea el primer "a)" y se
# traga el resto de la línea como una sola opción pegada) — sin este detector, el fallback de
# abajo las reclasificaba como "alternativas" con una única opción ilegible y una respuesta
# tipo "1-b, 2-c, 3-a" que nunca calza con ninguna opción clickeable (bug real: 153 preguntas
# quedaban permanentemente sin poder responderse bien).
RE_EMPAREJAR = re.compile(r"relacion|emparej|parea", re.IGNORECASE)
# Algunos archivos de PRUEBAS (no de guías) escriben la misma pregunta de emparejamiento sin
# ninguna etiqueta entre paréntesis (ej. "**4.** Une cada derecho..."), así que RE_EMPAREJAR
# sobre la etiqueta no basta — se detecta también por la forma: una línea "a) ... — b) ..."
# con un segundo marcador de letra pegado en la misma línea es, estructuralmente, siempre la
# fusión de dos listas en línea, nunca una alternativa real (esas nunca traen "— b)" dentro
# de la opción "a)").
RE_OPCION_FUSIONADA = re.compile(r"^\s*a\)\s.*—\s*[b-d]\)\s", re.IGNORECASE)
# Variante encontrada en preguntas de desarrollo sin "Respuesta correcta/esperada"
# explícita — una única pauta combinada que sirve de respuesta y de retroalimentación.
RE_PAUTA_MARCA = re.compile(r"(?i)[^\w\s]{0,2}\s*Pauta\s+de\s+retroalimentaci[oó]n:?\s*")
# El texto fuente es inconsistente: a veces "Respuesta correcta: b." (solo la letra), a
# veces "Respuesta correcta: d) Unidad de mil." (letra + texto repetido). En ambos casos
# hay que resolver por la letra al texto real de la opción — nunca confiar en lo que la
# sigue — porque IntentoEvaluacion.entregar()/esCorrectaEnAutoevaluacion() comparan la
# respuesta del alumno (el texto de la opción que clickeó) contra este campo tal cual.
RE_LETRA_RESPUESTA = re.compile(r"^\(?([a-dA-D])(?:\)|\.|\s|$)")


@dataclass
class PreguntaParseada:
    tipo: str
    enunciado: str
    opciones: list[str] | None
    respuesta_correcta: str
    retroalimentacion: str


@dataclass
class ObjetivoParseado:
    codigo_oficial: str
    descripcion: str
    eje_tematico: str | None
    contenido_guia: str = ""
    preguntas: list[PreguntaParseada] = field(default_factory=list)


def _clasificar_tipo(etiqueta: str) -> str:
    et = etiqueta.lower()
    if "verdadero" in et:
        return "verdadero_falso"
    if "alternativas" in et:
        return "alternativas"
    return "desarrollo_breve"


def _limpiar(texto: str) -> str:
    texto = texto.replace("**", "").replace("*", "")
    texto = re.sub(r"\s+", " ", texto).strip()
    texto = re.sub(r"\s*-{3,}\s*$", "", texto)  # separador markdown "---" al final
    return texto.strip()


def _parsear_bloque_preguntas(texto_bloque: str) -> list[PreguntaParseada]:
    matches = list(RE_Q_START.finditer(texto_bloque))
    preguntas: list[PreguntaParseada] = []

    for idx, m in enumerate(matches):
        inicio = m.end()
        fin = matches[idx + 1].start() if idx + 1 < len(matches) else len(texto_bloque)
        etiqueta = m.group(2)
        tipo = _clasificar_tipo(etiqueta)
        cuerpo = texto_bloque[inicio:fin]

        resp_m = RE_RESPUESTA_MARCA.search(cuerpo)
        if not resp_m:
            resp_m = RE_PAUTA_MARCA.search(cuerpo)
        antes = cuerpo[: resp_m.start()] if resp_m else cuerpo
        despues = cuerpo[resp_m.end() :] if resp_m else ""

        es_emparejamiento = bool(RE_EMPAREJAR.search(etiqueta)) or any(
            RE_OPCION_FUSIONADA.match(linea) for linea in antes.splitlines()
        )

        # enunciado + opciones (antes de la respuesta)
        opciones: list[str] = []
        enunciado_partes: list[str] = []
        for linea in antes.splitlines():
            # En preguntas de relacionar/emparejar, las líneas "a) ... — b) ... — c) ..."
            # no son alternativas clickeables — se dejan como parte del enunciado completo.
            op = None if es_emparejamiento else RE_OPCION.match(linea)
            if op:
                opciones.append(_limpiar(op.group(1)))
            elif linea.strip():
                # Una opción larga a veces se ajusta ("word-wrap") a la línea siguiente sin
                # repetir "b)" — si ya vimos al menos una opción, cualquier línea siguiente
                # que no sea una opción nueva es continuación de la ÚLTIMA opción, no del
                # enunciado (que siempre va completo antes de la primera opción).
                if opciones:
                    opciones[-1] = _limpiar(opciones[-1] + " " + linea.strip())
                else:
                    enunciado_partes.append(linea.strip())
        enunciado = _limpiar(" ".join(enunciado_partes))

        # respuesta + retroalimentación (después de la marca "Respuesta ...:")
        retro_m = RE_RETRO_MARCA.search(despues)
        if retro_m:
            respuesta_correcta = _limpiar(despues[: retro_m.start()]).rstrip(".")
            retroalimentacion = _limpiar(despues[retro_m.end() :])
        else:
            respuesta_correcta = _limpiar(despues).rstrip(".")
            # Sin marca de "Retroalimentación" propia (ej. "Pauta de retroalimentación"
            # combinada) — se usa el mismo texto para ambos campos.
            retroalimentacion = respuesta_correcta

        if tipo == "verdadero_falso":
            opciones_finales = ["Verdadero", "Falso"]
            # El contenido de Inglés a veces escribe la respuesta en inglés o bilingüe
            # ("True (Verdadero)", "False (Falso)") — se normaliza a las opciones reales
            # en español, que es lo único que el alumno puede clickear.
            respuesta_baja = respuesta_correcta.lower()
            if "verdadero" in respuesta_baja or respuesta_baja.startswith("true"):
                respuesta_correcta = "Verdadero"
            elif "falso" in respuesta_baja or respuesta_baja.startswith("false"):
                respuesta_correcta = "Falso"
        elif opciones:
            # El rótulo del autor a veces no dice "(Alternativas)" — usa etiquetas como
            # "(reconocer la operación)" — pero el cuerpo sí tiene opciones a)/b)/c)/d)
            # reales. Se clasifica por lo que la pregunta realmente tiene, no por el
            # rótulo (bug real: quedaba como "desarrollo_breve" sin mostrar nunca las
            # alternativas al alumno, con la respuesta pegada tal cual "b) Sustracción").
            tipo = "alternativas"
            opciones_finales = opciones
        else:
            opciones_finales = None

        if opciones_finales:
            letra_m = RE_LETRA_RESPUESTA.match(respuesta_correcta)
            if letra_m:
                idx = ord(letra_m.group(1).lower()) - ord("a")
                if 0 <= idx < len(opciones_finales):
                    respuesta_correcta = opciones_finales[idx]

        preguntas.append(
            PreguntaParseada(
                tipo=tipo,
                enunciado=enunciado,
                opciones=opciones_finales,
                respuesta_correcta=respuesta_correcta,
                retroalimentacion=retroalimentacion,
            )
        )
    return preguntas


def parsear_guia(texto: str) -> list[ObjetivoParseado]:
    """Parsea un archivo de guía completo (contenido/{curso}/{asignatura}.md) y
    devuelve la lista de Objetivos de Aprendizaje con su guía y su banco de preguntas.
    """
    lineas = texto.splitlines()
    objetivos: list[ObjetivoParseado] = []
    eje_actual: str | None = None
    oa_actual: ObjetivoParseado | None = None
    guia_buffer: list[str] = []
    preguntas_buffer: list[str] = []
    en_bloque_preguntas = False

    def cerrar_oa():
        if oa_actual is None:
            return
        oa_actual.contenido_guia = "\n".join(guia_buffer).strip()
        oa_actual.preguntas = _parsear_bloque_preguntas("\n".join(preguntas_buffer))
        objetivos.append(oa_actual)

    for linea in lineas:
        if RE_GLOSARIO_HEADING.match(linea):
            cerrar_oa()
            oa_actual = None
            guia_buffer, preguntas_buffer = [], []
            en_bloque_preguntas = False
            continue

        eje_m = RE_EJE.match(linea)
        if eje_m:
            cerrar_oa()
            oa_actual = None
            guia_buffer, preguntas_buffer = [], []
            en_bloque_preguntas = False
            eje_actual = eje_m.group(1).strip()
            continue

        oa_m = RE_OA_HEADING.match(linea)
        if oa_m:
            cerrar_oa()
            numero = oa_m.group(2)
            descriptor = oa_m.group(3)
            titulo = oa_m.group(4).strip()
            codigo_oficial = (
                f"OA {numero}" if numero else f"OA ({descriptor.strip()})"
            )
            oa_actual = ObjetivoParseado(
                codigo_oficial=codigo_oficial,
                descripcion=titulo,
                eje_tematico=eje_actual,
            )
            guia_buffer, preguntas_buffer = [], []
            en_bloque_preguntas = False
            continue

        if oa_actual is None:
            continue  # contenido antes del primer OA (bienvenida, índice) — se descarta

        if RE_AUTOEVAL_HEADING.match(linea) or RE_AUTOEVAL_BOLD_PARRAFO.match(linea):
            en_bloque_preguntas = True
            continue

        if en_bloque_preguntas:
            preguntas_buffer.append(linea)
        else:
            guia_buffer.append(linea)

    cerrar_oa()
    return objetivos
