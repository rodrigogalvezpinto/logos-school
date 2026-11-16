"""Control C.5 (2026-11-16): sesgo de posición en preguntas de «varias correctas».

Medición: en pruebas y simulacros, el 46 % de las preguntas de «varias correctas» tenía a, b y c correctas y la última
incorrecta, y la «a» era correcta en casi todas; en las guías, igual. La app baraja el orden de las preguntas, pero no el
de las alternativas, así que el alumno podía acertar por posición.

`rotar(texto, n_o_id, k, tipo_archivo)` rota k posiciones las alternativas de una pregunta (conserva su orden relativo),
actualiza las letras de la clave y verifica con el parser que las respuestas correctas, el enunciado y la explicación
sigan iguales. `rotar_archivo(ruta)` aplica una rotación distinta a cada pregunta de «varias correctas» del archivo,
saltando las que mencionan letras en su explicación u opciones (deben revisarse a mano).
"""
import json
import re
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(RAIZ / 'backend/scripts'))
from parser_contenido import parsear_guia  # noqa: E402
from parser_prueba_examen import parsear_prueba_o_examen  # noqa: E402

LETRAS = 'abcdefgh'
REF_LETRA = re.compile(r'(?<![\w])\(?[a-f]\)|\bopci[oó]n(es)? [a-f]\b|\bla [a-f]\b|\(([a-f])\)')
RE_PAUTA = re.compile(r'(?mi)^#{1,6}\s*(?:respuestas \(pauta\)|pauta|hoja de respuestas)|^\*\*Pauta')


def etiqueta(letras):
    return letras[0] if len(letras) == 1 else ', '.join(letras[:-1]) + ' y ' + letras[-1]


def _sin_prefijo(e):
    return re.sub(r'^\s*\**\(?[a-h](?:, [a-h])*(?: y [a-h])?(?:[).]|(?=\s*[—:-]))\**\s*[—:-]?\s*', '', e)


def _menciona_letras(enunciado, opciones, explicacion):
    if any(re.search(r'anteriores|ninguna de las|todas las (opciones|alternativas)', o, re.I) for o in opciones):
        return True
    return bool(REF_LETRA.search(_sin_prefijo(explicacion)) or any(REF_LETRA.search(o) for o in opciones))


def _reemplazar_opciones(bloque, opciones_nuevas):
    """Reemplaza, en orden, el texto de las líneas «x) …» del bloque de la pregunta."""
    lineas = bloque.split('\n')
    idx = [i for i, l in enumerate(lineas) if re.match(r'^\s*[a-h]\)\s', l)]
    assert len(idx) == len(opciones_nuevas), ('opciones en el bloque', len(idx), len(opciones_nuevas))
    for k, i in enumerate(idx):
        m = re.match(r'^(\s*)([a-h])\)\s', lineas[i])
        assert m.group(2) == LETRAS[k], ('orden de letras', lineas[i][:30])
        lineas[i] = f'{m.group(1)}{LETRAS[k]}) {opciones_nuevas[k]}'
    return '\n'.join(lineas)


def rotar_prueba(texto, n, k):
    preguntas = {p.numero: (p, r) for p, r in parsear_prueba_o_examen(texto)}
    p, r = preguntas[n]
    assert p.tipo == 'varias_correctas'
    ops = list(p.opciones)
    correctas = json.loads(r.respuesta_correcta)
    nuevas = ops[-k:] + ops[:-k] if k else ops
    viejas_letras = [LETRAS[ops.index(c)] for c in correctas]
    nuevas_letras = sorted(LETRAS[nuevas.index(c)] for c in correctas)
    corte = RE_PAUTA.search(texto).start()
    cab, cola = texto[:corte], texto[corte:]
    ini = re.compile(rf'(?m)^(?:\*\*(?:Pregunta )?{n}[.* ]|{n}\. \*|{n}\. \*\*|\*\*{n}\.)')
    ms = list(ini.finditer(cab))
    assert len(ms) == 1, ('inicio', n, len(ms))
    fin = re.compile(rf'(?m)^(?:\*\*(?:Pregunta )?{n + 1}[.* ]|{n + 1}\. \*|\*\*{n + 1}\.|---$|#|\*{{0,2}}\(?[ \t]*(?:Lee|Lea|Observa|Utiliza|Usa)\b)')
    mf = fin.search(cab, ms[0].end())
    j = mf.start() if mf else len(cab)
    cab = cab[:ms[0].start()] + _reemplazar_opciones(cab[ms[0].start():j], nuevas) + cab[j:]
    # pauta: entrada de n (lista o fila de tabla); se cambia solo la etiqueta de letras
    vieja, nueva = etiqueta(sorted(viejas_letras)), etiqueta(nuevas_letras)
    entrada = re.compile(rf'(?m)^(?:\| *{n} *\|.*|(?:\*\*(?:Pregunta )?{n}[.)]?(?: \([^)]*\))?\.?\*\*|{n}\.) .*)$')
    me = [x for x in entrada.finditer(cola)]
    assert len(me) == 1, ('pauta', n, len(me))
    linea = me[0].group(0)
    pos = linea.find(vieja)
    assert pos >= 0, ('etiqueta', vieja, linea[:80])
    linea_nueva = linea[:pos] + nueva + linea[pos + len(vieja):]
    cola = cola[:me[0].start()] + linea_nueva + cola[me[0].end():]
    nuevo = cab + cola
    p1, r1 = {x.numero: (x, y) for x, y in parsear_prueba_o_examen(nuevo)}[n]
    assert p1.opciones == nuevas and sorted(json.loads(r1.respuesta_correcta)) == sorted(correctas)
    assert p1.enunciado == p.enunciado and _sin_prefijo(r1.retroalimentacion) == _sin_prefijo(r.retroalimentacion)
    return nuevo


def rotar_guia(texto, oa_codigo, i_preg, k, idx_global=None):
    """idx_global: posición de la pregunta en el archivo (para guías donde un código de OA se repite en dos módulos)."""
    antes = [(oa.codigo_oficial, i, q) for oa in parsear_guia(texto) for i, q in enumerate(oa.preguntas, 1)]
    obj = [antes[idx_global]] if idx_global is not None else [x for x in antes if x[0] == oa_codigo and x[1] == i_preg]
    assert len(obj) == 1, ('pregunta ambigua', oa_codigo, i_preg)
    q = obj[0][2]
    assert q.tipo == 'varias_correctas'
    ops = list(q.opciones)
    correctas = json.loads(q.respuesta_correcta)
    nuevas = ops[-k:] + ops[:-k] if k else ops
    vieja = etiqueta(sorted(LETRAS[ops.index(c)] for c in correctas))
    nueva = etiqueta(sorted(LETRAS[nuevas.index(c)] for c in correctas))
    # ubicar el bloque de opciones: líneas consecutivas «a) texto» con exactamente esos textos, en orden
    lineas = texto.split('\n')
    pos = None
    for s in range(len(lineas) - len(ops) + 1):
        ventana = lineas[s:s + len(ops)]
        if all(re.match(rf'^\s*{LETRAS[t]}\)\s', ventana[t]) and ' '.join(ventana[t].split()[1:]) == ' '.join(ops[t].split())
               for t in range(len(ops))):
            assert pos is None, 'opciones repetidas en el archivo'
            pos = s
    assert pos is not None, ('no encontré las opciones', ops[0][:40])
    for t in range(len(ops)):
        m = re.match(r'^(\s*)', lineas[pos + t])
        lineas[pos + t] = f'{m.group(1)}{LETRAS[t]}) {nuevas[t]}'
    # la clave: primera línea con «Respuesta correcta» después de las opciones
    for s in range(pos + len(ops), min(pos + len(ops) + 6, len(lineas))):
        if re.search(r'Respuesta correcta', lineas[s], re.I):
            assert vieja in lineas[s], ('clave', vieja, lineas[s][:80])
            lineas[s] = lineas[s].replace(vieja, nueva, 1)
            break
    else:
        raise AssertionError('no encontré la línea de la clave')
    nuevo = '\n'.join(lineas)
    despues = [(oa.codigo_oficial, i, q) for oa in parsear_guia(nuevo) for i, q in enumerate(oa.preguntas, 1)]
    objetivo = antes.index(obj[0])
    for g, ((a0, i0, q0), (a1, i1, q1)) in enumerate(zip(antes, despues)):
        if g == objetivo:
            assert q1.opciones == nuevas and sorted(json.loads(q1.respuesta_correcta)) == sorted(correctas)
            assert q1.retroalimentacion == q0.retroalimentacion and q1.enunciado == q0.enunciado
        else:
            assert (q0.enunciado, q0.opciones, q0.respuesta_correcta) == (q1.enunciado, q1.opciones, q1.respuesta_correcta)
    return nuevo


def rotar_archivo(ruta, semilla=0):
    """Rota cada pregunta de «varias correctas» del archivo (k = 1, 2, 3, … cíclico). Devuelve (rotadas, saltadas)."""
    texto = ruta.read_text(encoding='utf-8')
    rotadas, saltadas = 0, []
    es_eval = ruta.parent.name in ('pruebas', 'examenes')
    if es_eval:
        items = [(p.numero, p, r.retroalimentacion) for p, r in parsear_prueba_o_examen(texto) if p.tipo == 'varias_correctas']
    else:
        items = [((oa.codigo_oficial, i), q, q.retroalimentacion) for oa in parsear_guia(texto)
                 for i, q in enumerate(oa.preguntas, 1) if q.tipo == 'varias_correctas']
    for t, (ident, q, expl) in enumerate(items):
        if _menciona_letras(q.enunciado, q.opciones, expl):
            saltadas.append(ident)
            continue
        k = (semilla + t) % len(q.opciones) or 1
        texto = rotar_prueba(texto, ident, k) if es_eval else rotar_guia(texto, ident[0], ident[1], k)
        rotadas += 1
    ruta.write_text(texto, encoding='utf-8')
    return rotadas, saltadas
