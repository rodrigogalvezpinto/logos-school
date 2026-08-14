"""Parser de Pruebas de unidad y Exámenes simulacro — formato distinto al de las guías
(contenido/{curso}/pruebas/*.md y /examenes/*.md).

Descubierto al implementar (no asumido de antemano): estos archivos tienen las
preguntas SIN respuesta embebida, seguidas de una sección de pauta separada al final,
en dos formatos posibles:
  - Lista numerada: "## Pauta de respuestas" o "## Respuestas (Pauta)", con entradas
    "1. **d) Unidad de mil.** explicación..." o "**1.** b) ... explicación...".
  - Tabla markdown: "# PAUTA DE CORRECCIÓN", con una fila por pregunta y una columna
    "Clave / criterio" o "Clave / Respuesta esperada" que trae la respuesta y la
    explicación juntas.
"""

import re
from dataclasses import dataclass

RE_Q_START = re.compile(
    # Toda pregunta real cumple AL MENOS UNO de dos rasgos: (a) el número está en negrita
    # ("**1.**", "**Pregunta 1 (alternativas).**") o (b) trae una etiqueta de tipo entre
    # paréntesis justo después, en cursiva o negrita ("1. *(Alternativas)*", usado en 3°-4°
    # medio). Las instrucciones numeradas al inicio de los exámenes ("1. Este examen
    # contiene 25 preguntas...") no cumplen ninguno de los dos — sin exigir esto, se colaban
    # como preguntas falsas y desalineaban la pauta de respuestas con las preguntas reales.
    r"(?m)^\s*\*{0,2}(?:Pregunta\s+)?(\d+)\.?"
    r"(?:\*{0,2}\s*\*{0,2}\(([^)]+)\)\*{0,2}\.?\s*|\*\*\s*)"
)
RE_OPCION = re.compile(r"^\s*[a-d]\)\s+(.*)$")
RE_PAUTA_HEADING = re.compile(r"^#{1,2}\s*.*pauta.*$", re.IGNORECASE)
RE_PAUTA_ENTRADA = re.compile(r"(?m)^\s*\*{0,2}(\d+)\.\*{0,2}\s*")
RE_TABLA_FILA = re.compile(r"^\|\s*(\d+)\s*\|(.*)\|\s*$")
RE_LETRA_INICIAL = re.compile(r"^\(?([a-dA-D])[\.\)]")
# La pauta de Verdadero/Falso a veces trae la explicación pegada en la misma entrada
# ("Verdadero. Es una consecuencia porque...") — sin esto, el texto completo (truncado a
# 60 caracteres) quedaba como respuesta_correcta y nunca calzaba con la opción real.
RE_VF_INICIAL = re.compile(r"(?i)^(verdadero|falso)\b")


def _resolver_respuesta_pauta(cuerpo: str) -> str:
    letra = RE_LETRA_INICIAL.match(cuerpo)
    if letra:
        return letra.group(1).lower()
    vf = RE_VF_INICIAL.match(cuerpo)
    if vf:
        return vf.group(1).capitalize()
    return cuerpo[:60]


@dataclass
class PreguntaSinRespuesta:
    numero: int
    tipo: str
    enunciado: str
    opciones: list[str] | None


@dataclass
class RespuestaPauta:
    respuesta_correcta: str
    retroalimentacion: str
    codigo_oa: str | None = None


def _limpiar(texto: str) -> str:
    texto = texto.replace("**", "").replace("*", "")
    texto = re.sub(r"\s+", " ", texto).strip()
    return re.sub(r"\s*-{3,}\s*$", "", texto).strip()


def _extraer_preguntas(texto_preguntas: str) -> list[PreguntaSinRespuesta]:
    matches = list(RE_Q_START.finditer(texto_preguntas))
    preguntas = []
    for idx, m in enumerate(matches):
        inicio = m.end()
        fin = matches[idx + 1].start() if idx + 1 < len(matches) else len(texto_preguntas)
        numero = int(m.group(1))
        cuerpo = texto_preguntas[inicio:fin]

        opciones: list[str] = []
        enunciado_partes: list[str] = []
        for linea in cuerpo.splitlines():
            op = RE_OPCION.match(linea)
            if op:
                opciones.append(_limpiar(op.group(1)))
            elif linea.strip():
                # Ver el mismo fix y comentario en parser_contenido.py: una opción larga
                # puede ajustarse a la línea siguiente sin repetir "b)" — esa continuación
                # pertenece a la última opción, no al enunciado.
                if opciones:
                    opciones[-1] = _limpiar(opciones[-1] + " " + linea.strip())
                else:
                    enunciado_partes.append(linea.strip())

        if opciones:
            tipo = "verdadero_falso" if set(o.lower() for o in opciones) <= {"verdadero", "falso"} else "alternativas"
        else:
            tipo = "desarrollo_breve"

        preguntas.append(
            PreguntaSinRespuesta(
                numero=numero,
                tipo=tipo,
                enunciado=_limpiar(" ".join(enunciado_partes)),
                opciones=opciones or None,
            )
        )
    return preguntas


def _extraer_pauta_lista(texto_pauta: str) -> dict[int, RespuestaPauta]:
    matches = list(RE_PAUTA_ENTRADA.finditer(texto_pauta))
    resultado = {}
    for idx, m in enumerate(matches):
        numero = int(m.group(1))
        inicio = m.end()
        fin = matches[idx + 1].start() if idx + 1 < len(matches) else len(texto_pauta)
        cuerpo = _limpiar(texto_pauta[inicio:fin])
        respuesta = _resolver_respuesta_pauta(cuerpo)
        resultado[numero] = RespuestaPauta(respuesta_correcta=respuesta, retroalimentacion=cuerpo)
    return resultado


def _extraer_pauta_tabla(texto_pauta: str) -> dict[int, RespuestaPauta]:
    filas = [l for l in texto_pauta.splitlines() if l.strip().startswith("|")]
    if not filas:
        return {}
    encabezado = [c.strip().lower() for c in filas[0].strip("|").split("|")]
    idx_clave = next((i for i, c in enumerate(encabezado) if "clave" in c or "respuesta" in c), None)
    idx_oa = next((i for i, c in enumerate(encabezado) if c.strip() == "oa" or "objetivo" in c), None)
    if idx_clave is None:
        return {}

    resultado = {}
    for fila in filas[2:]:  # fila 0 = encabezado, fila 1 = separador "---"
        m = RE_TABLA_FILA.match(fila.strip())
        if not m:
            continue
        numero = int(m.group(1))
        columnas = [c.strip() for c in m.group(2).split("|")]
        # columnas[0] es la 2ª columna de la tabla (la 1ª, N°, ya se extrajo con el regex)
        idx_ajustado = idx_clave - 1
        if idx_ajustado < 0 or idx_ajustado >= len(columnas):
            continue
        cuerpo = _limpiar(columnas[idx_ajustado])
        respuesta = _resolver_respuesta_pauta(cuerpo)

        codigo_oa = None
        if idx_oa is not None:
            idx_oa_ajustado = idx_oa - 1
            if 0 <= idx_oa_ajustado < len(columnas):
                oa_match = re.search(r"OA\s*N?°?\s*(\d+)", columnas[idx_oa_ajustado])
                if oa_match:
                    codigo_oa = f"OA {oa_match.group(1)}"

        resultado[numero] = RespuestaPauta(
            respuesta_correcta=respuesta, retroalimentacion=cuerpo, codigo_oa=codigo_oa
        )
    return resultado


def parsear_prueba_o_examen(texto: str) -> list[tuple[PreguntaSinRespuesta, RespuestaPauta | None]]:
    lineas = texto.splitlines()
    idx_pauta = next((i for i, l in enumerate(lineas) if RE_PAUTA_HEADING.match(l)), None)
    if idx_pauta is None:
        texto_preguntas, texto_pauta = texto, ""
    else:
        texto_preguntas = "\n".join(lineas[:idx_pauta])
        texto_pauta = "\n".join(lineas[idx_pauta:])

    preguntas = _extraer_preguntas(texto_preguntas)

    pautas = _extraer_pauta_tabla(texto_pauta)
    if not pautas:
        pautas = _extraer_pauta_lista(texto_pauta)

    resultado = []
    for p in preguntas:
        pauta = pautas.get(p.numero)
        if pauta and p.opciones and len(pauta.respuesta_correcta) == 1 and pauta.respuesta_correcta.lower() in "abcd":
            # La pauta trae solo la letra ("a", "b"...) — IntentoEvaluacion.entregar()
            # compara la respuesta del alumno (el TEXTO de la opción que clickeó, nunca
            # la letra) contra `respuesta_correcta`, así que hay que resolver la letra al
            # texto real de esa opción acá, una sola vez, en la fuente de verdad — si no,
            # ninguna pregunta de alternativas se puede corregir bien jamás (encontrado
            # simulando un examen completo con las respuestas correctas reales).
            idx = ord(pauta.respuesta_correcta.lower()) - ord("a")
            if 0 <= idx < len(p.opciones):
                pauta.respuesta_correcta = p.opciones[idx]
        resultado.append((p, pauta))
    return resultado
