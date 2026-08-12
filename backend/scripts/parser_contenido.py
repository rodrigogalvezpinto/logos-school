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
RE_OA_HEADING = re.compile(r"^(##|###)\s+OA\s*N?°?\s*(\d+)\s*[:\-—]*\s*(.*)$", re.IGNORECASE)
RE_AUTOEVAL_HEADING = re.compile(r"^(##|###|####)\s+.*autoevaluaci[oó]n.*$", re.IGNORECASE)
RE_AUTOEVAL_BOLD_PARRAFO = re.compile(r"^\*\*.*autoevaluaci[oó]n.*\*\*$", re.IGNORECASE)

# Inicio de pregunta: tolera "**Pregunta 1 (alternativas).**", "**1. (Alternativas)**"
# y "1. *(Alternativas)*" — con 0 a 2 asteriscos antes/después del número y del tipo.
RE_Q_START = re.compile(
    r"(?m)^\s*\*{0,2}(?:Pregunta\s+)?(\d+)\.?\s*\*{0,2}\(([^)]+)\)\*{0,2}\.?\s*"
)
RE_OPCION = re.compile(r"^\s*[a-d]\)\s+(.*)$")
RE_RESPUESTA_MARCA = re.compile(
    r"(?i)Respuesta\s+(?:correcta|esperada)\**:?\**\s*"
)
RE_RETRO_MARCA = re.compile(r"(?i)Retroalimentaci[oó]n:?\s*")
# Variante encontrada en preguntas de desarrollo sin "Respuesta correcta/esperada"
# explícita — una única pauta combinada que sirve de respuesta y de retroalimentación.
RE_PAUTA_MARCA = re.compile(r"(?i)Pauta\s+de\s+retroalimentaci[oó]n:?\s*")


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

        # enunciado + opciones (antes de la respuesta)
        opciones: list[str] = []
        enunciado_partes: list[str] = []
        for linea in antes.splitlines():
            op = RE_OPCION.match(linea)
            if op:
                opciones.append(_limpiar(op.group(1)))
            elif linea.strip():
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
        elif tipo == "alternativas" and opciones:
            opciones_finales = opciones
        else:
            opciones_finales = None

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
            titulo = oa_m.group(3).strip()
            oa_actual = ObjetivoParseado(
                codigo_oficial=f"OA {numero}",
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
