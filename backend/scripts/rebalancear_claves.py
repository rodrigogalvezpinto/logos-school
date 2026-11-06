"""Rebalancea la posición de la clave en preguntas de alternativas (auditoría 2026-11-06).

Problema medido: en el corpus la letra «b» era la clave del 39 % de las preguntas de
alternativas (lo esperable con 4 opciones es ~25 %). Un estudiante que aprende ese patrón
acierta sin saber, y el simulacro deja de parecerse al examen real.

Qué hace, archivo por archivo y de forma determinista:

1. Elige las preguntas de alternativas cuya letra correcta está sobrerrepresentada en ese
   archivo y la intercambia con la opción de la letra menos usada (solo DOS opciones se
   mueven; el resto queda igual).
2. Dentro de esa pregunta, intercambia también las referencias a esas dos letras en la
   clave y la retroalimentación/pauta («b)», «**b)**», «Respuesta correcta: b.», «opción
   b»…), para que las explicaciones del tipo «la a) describe al Ejecutivo» sigan siendo
   ciertas.
3. Omite preguntas cuyo orden de opciones importa («todas las anteriores», «a y b»…).
4. Verifica con los parsers que, antes y después, cada pregunta conserve tipo, enunciado,
   conjunto de opciones y TEXTO de la clave. Si algo no cuadra, no escribe el archivo.

Uso: python backend/scripts/rebalancear_claves.py [--escribir] <archivos.md...>
Sin --escribir solo informa lo que haría.
"""

import collections
import math
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from conversion_alternativas import (  # noqa: E402
    RE_PAUTA_ENTRADA,
    bloques_guia,
    bloques_prueba,
    es_evaluacion,
    partir,
    preguntas_parseadas,
)
from parser_prueba_examen import parsear_prueba_o_examen  # noqa: E402

LETRAS = "abcde"
RE_ORDEN_IMPORTA = re.compile(r"(?i)anteriores|\bambas\b|\btodas las\b|\bninguna de\b|\b[a-e]\) y [a-e]\)|\b[a-e] y [a-e]\b")
RE_RESPUESTA_GUIA = re.compile(r"Respuesta correcta|✅")


def intercambiar_letras(texto: str, k: str, t: str) -> str:
    """Intercambia las referencias a las opciones k y t (no toca «(a)», palabras ni otras letras)."""
    marca = {k: "\x00K\x00", t: "\x00T\x00"}
    patrones = [
        rf"(?<![\w(\[])([{k}{t}])(?=\))",                                        # b)  **b)**
        rf"(?<=Respuesta correcta:\*\* )([{k}{t}])(?=[.\s*)])",                    # **Respuesta correcta:** b.
        rf"(?<=Respuesta correcta: )([{k}{t}])(?=[.\s*)])",                        # *Respuesta correcta: b.*
        rf"(?<=Respuesta correcta: \*\*)([{k}{t}])(?=[.\s*)])",                    # ✅ Respuesta correcta: **b)
        rf"(?<=\*\*)([{k}{t}])(?=\.\*\*)",                                         # **b.**
    ] + [
        rf"(?<=\b{palabra} )([{k}{t}])\b"                                          # opción b
        for palabra in ("opción", "opcion", "alternativa", "letra")
    ]
    for patron in patrones:
        texto = re.sub(patron, lambda m: marca[m.group(1)], texto)
    # Pauta en lista «N. b — …» / «N. b. …» / «N. **b.** …»: la letra justo tras el número
    texto = re.sub(rf"(?<=\| )([{k}{t}])(?= \|)", lambda m: marca[m.group(1)], texto)
    texto = re.sub(rf"^(\s*(?:\*\*)?\d+\.(?:\*\*)?\s+(?:\*\*)?)([{k}{t}])(?=\s*—|\.|\*\*|,|\s+y\s|\s*$)",
                   lambda m: m.group(1) + marca[m.group(2)], texto)
    return texto.replace(marca[k], t).replace(marca[t], k)


def huella(ruta: Path, texto: str):
    """Por pregunta: (tipo, opciones ordenadas, clave). El enunciado se compara aparte."""
    return [(t, tuple(sorted(o or [])), c) for _, t, o, c in preguntas_parseadas(ruta, texto)]


def letra_clave_guia(bloque: str) -> str | None:
    m = RE_RESPUESTA_GUIA.search(bloque)
    if not m:
        return None
    resto = bloque[m.end():m.end() + 30]
    m2 = re.search(r"([a-e])(?=[).]|\*\*|\s*$)", resto.lstrip(":* "))
    return m2.group(1) if m2 else None


def candidatos(ruta: Path, texto: str):
    """Lista de (clave_bloque, letra_actual, n_opciones, inicio, fin, inicio_respuesta)."""
    salida = []
    if es_evaluacion(ruta):
        parseadas = {p.numero: (p, r) for p, r in parsear_prueba_o_examen(texto)}
        bloques = bloques_prueba(texto)
        for n, (ini, fin) in bloques.items():
            if n not in parseadas:
                continue
            p, r = parseadas[n]
            if p.tipo != "alternativas" or not p.opciones or r is None or r.respuesta_correcta not in p.opciones:
                continue
            if any(RE_ORDEN_IMPORTA.search(o) for o in p.opciones):
                continue
            salida.append((n, LETRAS[p.opciones.index(r.respuesta_correcta)], len(p.opciones), ini, fin, None))
    else:
        for clave, (ini, fin) in bloques_guia(texto).items():
            bloque = texto[ini:fin]
            m = RE_RESPUESTA_GUIA.search(bloque)
            letra = letra_clave_guia(bloque)
            if not m or not letra:
                continue
            opciones = re.findall(r"(?m)^[ \t]*([a-e])\) (.*)$", bloque[:m.start()])
            if len(opciones) < 3 or [o[0] for o in opciones] != list(LETRAS[:len(opciones)]):
                continue
            if any(RE_ORDEN_IMPORTA.search(o[1]) for o in opciones) or re.search(r"Varias correctas|todas\*\* las correctas", bloque[:m.start()]):
                continue
            salida.append((clave, letra, len(opciones), ini, fin, ini + m.start()))
    return salida


def planificar(cands):
    cuenta = collections.Counter(c[1] for c in cands)
    techo = math.ceil(len(cands) / 4) if cands else 0
    plan = []
    for clave, letra, n_ops, *_ in cands:
        if cuenta[letra] <= techo:
            continue
        posibles = [x for x in LETRAS[:n_ops] if x != letra and cuenta[x] < cuenta[letra] - 1]
        if not posibles:
            continue
        destino = min(posibles, key=lambda x: (cuenta[x], -LETRAS.index(x)))
        cuenta[letra] -= 1
        cuenta[destino] += 1
        plan.append((clave, letra, destino))
    return plan


def regiones_pauta(texto: str, n: int) -> list[tuple[int, int]]:
    """Todas las entradas de pauta (lista y filas de tabla) del número n."""
    inicio = partir(texto)
    pauta = texto[inicio:]
    regiones = []
    entradas = list(RE_PAUTA_ENTRADA.finditer(pauta))
    for i, m in enumerate(entradas):
        if int(m.group(1)) == n:
            fin = entradas[i + 1].start() if i + 1 < len(entradas) else len(pauta)
            regiones.append((inicio + m.start(), inicio + fin))
    for m in re.finditer(rf"(?m)^(?:\|\s*{n}\s*\||\*\*Pregunta {n}\b).*$", pauta):
        regiones.append((inicio + m.start(), inicio + m.end()))
    # sin solapes: quedarse con las regiones exteriores
    regiones.sort()
    limpias = []
    for a, b in regiones:
        if limpias and a < limpias[-1][1]:
            limpias[-1] = (limpias[-1][0], max(b, limpias[-1][1]))
        else:
            limpias.append((a, b))
    return limpias


def extensiones_opciones(bloque: str, corte: int) -> dict[str, tuple[int, int]]:
    """letra -> (inicio del texto tras «x) », fin) incluyendo líneas de continuación."""
    inicios = [m for m in re.finditer(r"(?m)^[ \t]*([a-e])\) ", bloque) if m.start() < corte]
    resultado = {}
    for i, m in enumerate(inicios):
        limite = inicios[i + 1].start() if i + 1 < len(inicios) else corte
        vacia = re.search(r"\n[ \t]*\n", bloque[m.end():limite])
        fin = m.end() + vacia.start() if vacia else limite
        texto = bloque[m.end():fin]
        fin = m.end() + len(texto.rstrip())
        if m.group(1) in resultado:
            return {}
        resultado[m.group(1)] = (m.end(), fin)
    return resultado


def aplicar_intercambio(texto: str, ini: int, fin: int, k: str, t: str, ini_resp: int | None):
    bloque = texto[ini:fin]
    corte = (ini_resp - ini) if ini_resp is not None else len(bloque)
    corte = bloque.rfind("\n", 0, corte) + 1 if ini_resp is not None else corte
    ext = extensiones_opciones(bloque, corte)
    if k not in ext or t not in ext:
        return None
    (ak, bk), (at, bt) = ext[k], ext[t]
    txt_k, txt_t = bloque[ak:bk], bloque[at:bt]
    for a, b, nuevo in sorted([(ak, bk, txt_t), (at, bt, txt_k)], reverse=True):
        bloque = bloque[:a] + nuevo + bloque[b:]
    if ini_resp is not None:
        # la respuesta va después de las opciones: recalcular su posición
        m = RE_RESPUESTA_GUIA.search(bloque)
        c = m.start() if m else len(bloque)
        bloque = bloque[:c] + intercambiar_letras(bloque[c:], k, t)
    return texto[:ini] + bloque + texto[fin:]


def procesar(ruta: Path, escribir: bool) -> tuple[int, int]:
    original = ruta.read_text(encoding="utf-8")
    cands = candidatos(ruta, original)
    plan = planificar(cands)
    if not plan:
        return 0, len(cands)
    referencia = huella(ruta, original)
    texto = original
    aplicados, rechazados = 0, []
    # Cada intercambio se verifica por separado (el archivo completo debe conservar tipo,
    # opciones y TEXTO de cada clave); si no cuadra, se revierte solo ese intercambio.
    for clave, k, t in plan:
        if es_evaluacion(ruta):
            ini, fin = bloques_prueba(texto)[clave]
            ini_resp = None
        else:
            ini, fin = bloques_guia(texto)[clave]
            m = RE_RESPUESTA_GUIA.search(texto, ini, fin)
            ini_resp = m.start() if m else None
        nuevo = aplicar_intercambio(texto, ini, fin, k, t, ini_resp)
        if nuevo is None:
            rechazados.append(clave)
            continue
        if es_evaluacion(ruta):
            for a, b in sorted(regiones_pauta(nuevo, clave), reverse=True):
                nuevo = nuevo[:a] + intercambiar_letras(nuevo[a:b], k, t) + nuevo[b:]
        try:
            ok = huella(ruta, nuevo) == referencia
        except Exception:  # noqa: BLE001 - un parseo roto también es rechazo
            ok = False
        if ok:
            texto, aplicados = nuevo, aplicados + 1
        else:
            rechazados.append(clave)
    letras = collections.Counter()
    for _, tipo, o, c in preguntas_parseadas(ruta, texto):
        if tipo == "alternativas" and o and c in o:
            letras[LETRAS[o.index(c)]] += 1
    if escribir and texto != original:
        ruta.write_text(texto, encoding="utf-8")
    extra = f"; rechazados {rechazados}" if rechazados else ""
    print(f"{ruta}: {aplicados}/{len(plan)} intercambios; letras {dict(sorted(letras.items()))}{extra}")
    return aplicados, len(cands)


def main() -> None:
    escribir = "--escribir" in sys.argv
    rutas = [Path(a) for a in sys.argv[1:] if a != "--escribir"]
    total = 0
    for ruta in rutas:
        total += procesar(ruta, escribir)[0]
    print(f"Total intercambios: {total}{'' if escribir else ' (simulación: usar --escribir)'}")


if __name__ == "__main__":
    main()
