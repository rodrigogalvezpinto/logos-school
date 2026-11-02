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

import json
import re
from dataclasses import dataclass

from parser_contenido import extraer_modulo

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
RE_PAUTA_ENTRADA = re.compile(
    r"(?m)^[ \t]*(?:-[ \t]+)?\*{0,2}(?:Pregunta[ \t]+)?(\d+)"
    r"(?:[ \t]+\([^\n)]+\))?\.(?:\*\*)?(?=[ \t]|$)[ \t]*"
)
# Una línea que ABRE con un encabezado real en negrita ("**Subtotal ...**",
# "**Puntaje total ...**", "**Preguntas de ...**", "**Pauta de ...**", con o sin
# detalle después del cierre de la negrita) es límite de entrada — la respuesta
# misma a veces viene toda en negrita en la línea del número ("2. **about / how.**")
# y el patrón anterior ("cualquier línea negrita") cortaba la entrada en la posición
# 0, dejando vacías 98 pautas reales (bug encontrado en la revalidación del corpus).
RE_PAUTA_LIMITE = re.compile(
    r"(?m)^[ \t]*(?:#{1,6}[ \t]+|\*\*[ \t]*(?:Subtotal|Puntaje|Pauta\s+de"
    r"|Preguntas\s+de|Distribuci[oó]n|Relaci[oó]n|Tipo\s+de)\b|\|)"
)
RE_TABLA_FILA = re.compile(r"^\|\s*(\d+)\s*\|(.*)\|\s*$")
## Variante encontrada en 3°-4° medio: la pauta a veces escribe la letra seguida de un
# em-dash y la explicación ("b — se identifican directamente dos términos...") en vez de
# "b." o "b)" — sin tolerar el em-dash, la letra no se resolvía y el texto completo
# (truncado a 60 caracteres) quedaba como respuesta_correcta, sin calzar nunca con
# ninguna opción real.
RE_LETRA_INICIAL = re.compile(r"^\(?([a-dA-D])(?:[\.\)]|\s*—|$)")
# La pauta de Verdadero/Falso a veces trae la explicación pegada en la misma entrada
# ("Verdadero. Es una consecuencia porque...") — sin esto, el texto completo (truncado a
# 60 caracteres) quedaba como respuesta_correcta y nunca calzaba con la opción real.
RE_VF_INICIAL = re.compile(r"(?i)^(verdadero|falso)\b")
# Ver el mismo bug y comentario en parser_contenido.py: preguntas de "Relacionar / emparejar"
# escriben sus dos listas en línea ("a) A — b) B — c) C"), RE_OPCION las confunde con
# alternativas reales (una sola opción pegada e ilegible) y la pauta ("1-b, 2-c, 3-a") nunca
# calza con ninguna opción — quedan permanentemente sin poder responderse bien.
RE_EMPAREJAR = re.compile(r"relacion|emparej|parea", re.IGNORECASE)
# Ver el mismo comentario en parser_contenido.py: algunas pruebas escriben la pregunta de
# emparejamiento sin ninguna etiqueta entre paréntesis (ej. "**4.** Une cada derecho..."),
# así que además de la etiqueta se detecta la fusión estructuralmente.
RE_OPCION_FUSIONADA = re.compile(r"^\s*a\)\s.*—\s*[b-d]\)\s", re.IGNORECASE)


def _resolver_respuesta_pauta(cuerpo: str) -> str:
    letra = RE_LETRA_INICIAL.match(cuerpo)
    if letra:
        return letra.group(1).lower()
    vf = RE_VF_INICIAL.match(cuerpo)
    if vf:
        return vf.group(1).capitalize()
    return cuerpo


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
    modulo: str | None = None
    asignatura: str | None = None
    codigos_oa: tuple[str, ...] = ()


def _limpiar(texto: str) -> str:
    texto = texto.replace("**", "").replace("*", "")
    texto = re.sub(r"\s+", " ", texto).strip()
    return re.sub(r"\s*-{3,}\s*$", "", texto).strip()


def _extraer_preguntas(texto_preguntas: str) -> list[PreguntaSinRespuesta]:
    matches = list(RE_Q_START.finditer(texto_preguntas))
    declaraciones = list(re.finditer(
        r"(?mi)^(?:#{1,6}[ \t]+)?\*{0,2}\(?[ \t]*(?:Lee|Lea|Observa|Utiliza|Usa|Textos?\s+\d+)\b[^\n]*\bpreguntas?\s+\d[^\n]*$", texto_preguntas,
    ))
    contextos: dict[int, list[str]] = {}
    numeros = {int(m.group(1)) for m in matches}
    for i, declaracion in enumerate(declaraciones):
        siguiente = next((m.start() for m in matches if m.start() > declaracion.end()), None)
        if siguiente is None:
            continue
        fin_contexto = min(siguiente, declaraciones[i + 1].start()) if i + 1 < len(declaraciones) else siguiente
        contexto = texto_preguntas[declaracion.start():fin_contexto].strip()
        destinos = set()
        for grupo in re.finditer(r"preguntas?\s+(\d+(?:\s*(?:,|y|a|[-–])\s*\d+)*)", declaracion.group(), re.IGNORECASE):
            for tramo in re.finditer(r"(\d+)(?:\s*(?:a|[-–])\s*(\d+))?", grupo.group(1), re.IGNORECASE):
                inicio_rango = int(tramo.group(1))
                fin_rango = int(tramo.group(2) or inicio_rango)
                if not numeros or not 1 <= inicio_rango <= fin_rango <= max(numeros):
                    raise ValueError("Rango de estímulo fuera de las preguntas existentes")
                destinos.update(range(inicio_rango, fin_rango + 1))
        if not destinos <= numeros:
            raise ValueError("Estímulo asociado a preguntas inexistentes")
        for numero in destinos:
            contextos.setdefault(numero, []).append(contexto)
    preguntas = []
    for idx, m in enumerate(matches):
        inicio = m.end()
        fin = matches[idx + 1].start() if idx + 1 < len(matches) else len(texto_preguntas)
        numero = int(m.group(1))
        etiqueta = m.group(2) or ""
        fin = next((d.start() for d in declaraciones if inicio <= d.start() < fin), fin)
        cuerpo = texto_preguntas[inicio:fin]
        es_emparejamiento = bool(RE_EMPAREJAR.search(etiqueta)) or any(
            RE_OPCION_FUSIONADA.match(linea) for linea in cuerpo.splitlines()
        )

        opciones: list[str] = []
        enunciado_partes: list[str] = []
        for linea in cuerpo.splitlines():
            if re.match(r"^\s{0,3}#{1,6}\s+", linea) and (
                opciones or re.match(r"^\s*#{1,6}\s+(?:OA\b|OA\d|Objetivos?\s+de\s+Aprendizaje\b)", linea, re.IGNORECASE)
            ):
                break
            if re.fullmatch(r"\s*-{3,}\s*", linea):
                continue
            op = None if es_emparejamiento else RE_OPCION.match(linea)
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

        es_vf = bool(re.search(r"\b(?:verdadero\s*(?:o|/|y)?\s*falso|v\s*/\s*f)\b", etiqueta, re.IGNORECASE))
        requiere_escrito = bool(re.search(r"justific|explic|fundament|corrig|corr[ií]j|argument|razona|\b(?:explain|justify)\b|\bcorrect\s+(?:the|any|each|false)\b",
                                          etiqueta + " " + " ".join(enunciado_partes), re.IGNORECASE))
        opciones_vf = bool(opciones) and set(o.lower() for o in opciones) <= {"verdadero", "falso"}
        if requiere_escrito and (opciones_vf or (es_vf and not opciones)):
            tipo = "desarrollo_breve"
            opciones = []
        elif es_vf and not opciones:
            tipo = "verdadero_falso"
            opciones = ["Verdadero", "Falso"]
        elif opciones:
            tipo = "verdadero_falso" if opciones_vf else "alternativas"
        else:
            tipo = "desarrollo_breve"

        enunciado = _limpiar(" ".join(enunciado_partes))
        if numero in contextos:
            enunciado = "\n\n".join([*contextos[numero], enunciado])
        preguntas.append(
            PreguntaSinRespuesta(
                numero=numero,
                tipo=tipo,
                enunciado=enunciado,
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
        bloque = texto_pauta[inicio:fin]
        principal_re = re.compile(r"(?mi)^[ \t]*\*{0,2}OA principal\*{0,2}:\*{0,2}[ \t]*([^\n]*)$")
        principales = list(principal_re.finditer(bloque))
        codigos = _codigos_oa(principales[0].group(1)) if principales else ()
        if principales and (len(principales) != 1 or len(codigos) != 1):
            raise ValueError(f"OA principal inválido o duplicado en pregunta {numero}")
        modulo = extraer_modulo(principales[0].group(1)) if principales else None
        bloque = principal_re.sub("", bloque)
        limite = RE_PAUTA_LIMITE.search(bloque)
        cuerpo = _limpiar(bloque[:limite.start()] if limite else bloque)
        respuesta = _resolver_respuesta_pauta(cuerpo)
        resultado[numero] = RespuestaPauta(
            respuesta_correcta=respuesta, retroalimentacion=cuerpo,
            codigo_oa=codigos[0] if codigos else None, modulo=modulo, codigos_oa=codigos,
        )
    return resultado


def _codigos_oa(texto: str) -> tuple[str, ...]:
    bloques = re.finditer(
        r"\bOAs?\s*(?:N[°º.]?\s*)?(\d+(?:\s*(?:,|/|y|e|[-–])\s*\d+)*)",
        texto, re.IGNORECASE,
    )
    return tuple(dict.fromkeys(f"OA {numero}" for bloque in bloques for numero in re.findall(r"\d+", bloque.group(1))))


def _celdas_tabla(texto: str) -> list[str]:
    celdas = []
    inicio = 0
    escapada = False
    for posicion, caracter in enumerate(texto):
        if caracter == "|" and not escapada:
            celdas.append(texto[inicio:posicion].strip())
            inicio = posicion + 1
        escapada = caracter == "\\" and not escapada
    celdas.append(texto[inicio:].strip())
    return celdas


def _extraer_pauta_tabla(texto_pauta: str) -> dict[int, RespuestaPauta]:
    # La pauta puede traer VARIAS tablas (grilla de respuestas vacía, rúbrica manual
    # "Completo/Parcial/Insuficiente" y recién después la tabla de claves, ej.
    # 04-medio/examenes/lengua-y-literatura-examen-forma-b.md) — mirar solo la primera
    # perdía las 25 pautas del examen. Se recorre cada bloque de líneas "|" por
    # separado: las tablas con columna "clave/respuesta" aportan la respuesta, las
    # demás tablas con filas numeradas se tratan como rúbricas manuales por número.
    bloques: list[list[str]] = []
    actual: list[str] = []
    for linea in texto_pauta.splitlines():
        if linea.strip().startswith("|"):
            actual.append(linea)
        elif actual:
            bloques.append(actual)
            actual = []
    if actual:
        bloques.append(actual)

    resultado: dict[int, RespuestaPauta] = {}
    rubricas: dict[int, str] = {}
    for filas in bloques:
        if len(filas) < 2:
            continue
        encabezado_orig = _celdas_tabla(filas[0].strip())[1:-1]
        encabezado = [c.lower() for c in encabezado_orig]
        idx_clave = next((i for i, c in enumerate(encabezado) if "clave" in c or "respuesta" in c), None)
        idx_oa = next((i for i, c in enumerate(encabezado) if re.search(r"\boa\b|objetivo", c)), None)
        idx_asignatura = next((i for i, c in enumerate(encabezado) if "asignatura" in c), None)

        for fila in filas[1:]:  # fila 0 = encabezado; el separador "---" no calza \d+
            m = RE_TABLA_FILA.match(fila.strip())
            if not m:
                continue
            numero = int(m.group(1))
            columnas = _celdas_tabla(m.group(2))
            # columnas[0] es la 2ª columna de la tabla (la 1ª, N°, ya se extrajo con el regex)
            if idx_clave is not None:
                idx_ajustado = idx_clave - 1
                if idx_ajustado < 0 or idx_ajustado >= len(columnas):
                    continue
                cuerpo = _limpiar(columnas[idx_ajustado])
                respuesta = _resolver_respuesta_pauta(cuerpo)

                codigos_oa = ()
                modulo = None
                if idx_oa is not None:
                    idx_oa_ajustado = idx_oa - 1
                    if 0 <= idx_oa_ajustado < len(columnas):
                        modulo = extraer_modulo(columnas[idx_oa_ajustado])
                        codigos_oa = _codigos_oa(columnas[idx_oa_ajustado])

                resultado[numero] = RespuestaPauta(
                    respuesta_correcta=respuesta, retroalimentacion=cuerpo,
                    codigo_oa=codigos_oa[0] if len(codigos_oa) == 1 else None,
                    modulo=modulo, codigos_oa=codigos_oa,
                    asignatura=_limpiar(columnas[idx_asignatura - 1])
                    if idx_asignatura is not None and 0 < idx_asignatura <= len(columnas) else None,
                )
            else:
                # Rúbrica manual por número: cada columna de criterio se conserva con
                # el nombre de SU encabezado, solo para este número — sin mezclar los
                # criterios de las filas vecinas.
                criterios = [
                    f"{encabezado_orig[i + 1]}: {columnas[i]}"
                    for i in range(min(len(columnas), len(encabezado) - 1))
                    if columnas[i]
                ]
                if criterios:
                    rubricas[numero] = _limpiar(" | ".join(criterios))

    for numero, rubrica in rubricas.items():
        pauta = resultado.get(numero)
        if pauta is None:
            resultado[numero] = RespuestaPauta(
                respuesta_correcta=_resolver_respuesta_pauta(rubrica),
                retroalimentacion=rubrica,
            )
        else:
            pauta.retroalimentacion = _limpiar(
                f"{pauta.retroalimentacion} — Pauta manual: {rubrica}"
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

    pautas = _extraer_pauta_lista(texto_pauta)
    pautas.update(_extraer_pauta_tabla(texto_pauta))

    modulos_por_pregunta = {}
    codigos_por_pregunta = {}
    codigos_globales = ()
    principales = {}
    metadatos = re.match(r"\s*---[ \t]*\n(.*?)\n---(?:\n|$)", texto_preguntas, re.DOTALL)
    if metadatos:
        mapa = re.search(r"(?mi)^oa_por_pregunta[ \t]*:[ \t]*(.*)$", metadatos.group(1))
        if mapa:
            try:
                if not mapa.group(1).lstrip().startswith("{"):
                    raise ValueError("se requiere objeto JSON")
                pares = json.loads(mapa.group(1), object_pairs_hook=list)
                for clave, valor in pares:
                    if not re.fullmatch(r"[1-9]\d*", clave) or not isinstance(valor, str):
                        raise ValueError("número o código inválido")
                    numero = int(clave)
                    codigos = _codigos_oa(valor)
                    if numero in principales or numero not in {p.numero for p in preguntas} or len(codigos) != 1:
                        raise ValueError("pregunta duplicada/inexistente u OA ambiguo")
                    principales[numero] = (codigos[0], extraer_modulo(valor))
            except (ValueError, TypeError) as exc:
                raise ValueError(f"Mapa OA inválido: {exc}") from exc
        for campo in ("oa_evaluados", "unidad", "eje"):
            valor = re.search(rf"(?mi)^{campo}[ \t]*:[ \t]*(.*)$", metadatos.group(1))
            if valor:
                codigos_globales = _codigos_oa(valor.group(1))
                if codigos_globales:
                    break
    modulo_actual = None
    pila_oa = []
    for linea in texto_preguntas.splitlines():
        encabezado = re.match(r"^(#{1,6})\s+(.*)$", linea)
        if encabezado:
            nivel = len(encabezado.group(1))
            while pila_oa and pila_oa[-1][0] >= nivel:
                pila_oa.pop()
            pila_oa.append((nivel, _codigos_oa(encabezado.group(2))))
            modulo = extraer_modulo(linea)
            if modulo is not None:
                modulo_actual = modulo
        inicio = RE_Q_START.match(linea)
        if inicio:
            numero = int(inicio.group(1))
            modulos_por_pregunta[numero] = modulo_actual
            codigos_por_pregunta[numero] = next(
                (codigos for _, codigos in reversed(pila_oa) if codigos), codigos_globales,
            )

    resultado = []
    for p in preguntas:
        pauta = pautas.get(p.numero)
        if pauta:
            if p.numero in principales:
                codigo, modulo_principal = principales[p.numero]
                if pauta.codigo_oa and pauta.codigo_oa != codigo:
                    raise ValueError(f"Mapa OA contradictorio en pregunta {p.numero}")
                if pauta.modulo and modulo_principal and pauta.modulo != modulo_principal:
                    raise ValueError(f"Mapa OA con módulo contradictorio en pregunta {p.numero}")
                pauta.codigo_oa = codigo
                pauta.codigos_oa = (codigo,)
                pauta.modulo = modulo_principal or pauta.modulo
            modulo = modulos_por_pregunta.get(p.numero)
            if pauta.modulo and modulo and pauta.modulo != modulo:
                raise ValueError(f"Módulo contradictorio en pregunta {p.numero}")
            pauta.modulo = pauta.modulo or modulo
            pauta.codigos_oa = pauta.codigos_oa or (
                (pauta.codigo_oa,) if pauta.codigo_oa else codigos_por_pregunta.get(p.numero, ())
            )
            if len(pauta.codigos_oa) == 1:
                pauta.codigo_oa = pauta.codigo_oa or pauta.codigos_oa[0]
        if pauta and p.tipo == "verdadero_falso":
            vf = re.match(r"(verdadero|falso|true|false|v|f)\b", pauta.respuesta_correcta, re.IGNORECASE)
            if vf:
                pauta.respuesta_correcta = "Verdadero" if vf.group(1).casefold() in {"verdadero", "true", "v"} else "Falso"
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
