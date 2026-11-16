from pathlib import Path
"""C.4: agrega explicación a pautas que solo repiten la clave. Uso:
from explicar import ver, explicar
ver('03-basico/pruebas/x.md', [1,2])           # muestra pregunta + pauta
explicar('03-basico/pruebas/x.md', {1: 'texto'})  # agrega «. texto» a la pauta; verifica clave intacta
"""
import re
import sys

RAIZ = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(RAIZ / 'backend/scripts'))
from parser_prueba_examen import parsear_prueba_o_examen  # noqa: E402


def _parse(ruta):
    return {p.numero: (p, r) for p, r in parsear_prueba_o_examen(ruta.read_text(encoding='utf-8'))}


def ver(archivo, nums=None, ctx=False):
    ruta = RAIZ / 'contenido' / archivo
    d = _parse(ruta)
    for n in nums or sorted(d):
        p, r = d[n]
        e = p.enunciado if ctx else p.enunciado.split('\n\n')[-1]
        print(f'## {n} [{p.tipo}] {e[:600]}')
        for i, o in enumerate(p.opciones):
            print(f'   {"abcdef"[i]}) {o}')
        print(f'   CLAVE={r.respuesta_correcta!r}  RETRO={r.retroalimentacion!r}')


def explicar(archivo, textos):
    ruta = RAIZ / 'contenido' / archivo
    antes = _parse(ruta)
    t = ruta.read_text(encoding='utf-8')
    i = re.search(r'(?mi)^#{1,6}\s*(?:respuestas \(pauta\)|pauta)|^\*\*Pauta', t).start()
    cab, cola = t[:i], t[i:]
    for n, txt in textos.items():
        txt = txt.strip()
        fila = re.compile(rf'(?m)^(\| *{n} *\|)(.*)\|[ \t]*$')
        m = list(fila.finditer(cola))
        if len(m) == 1:
            celdas = m[0].group(2).split('|')
            # celda de la respuesta: la que contiene la clave; si no, la primera
            clave = antes[n][1].respuesta_correcta
            k = next((j for j, c in enumerate(celdas) if re.match(r'\s*\**[a-d]\)', c)), None)
            if k is None:
                k = next((j for j, c in enumerate(celdas) if clave[:12].lower() in c.lower()), 0)
            c = celdas[k].rstrip()
            c = c + ('' if c.endswith(('.', '!', '?', ')**', '**')) else '.') + ' ' + txt + ' '
            celdas[k] = c
            cola = cola[:m[0].start()] + m[0].group(1) + '|'.join(celdas) + '|' + cola[m[0].end():]
            continue
        item = re.compile(rf'(?m)^((?:\*\*{n}\.\*\*|\*\*{n}\.|{n}\.|\*\*Pregunta {n}\b[^*\n]*\*\*) .*?)[ \t]*$')
        m = list(item.finditer(cola))
        assert len(m) == 1, (n, len(m))
        linea = m[0].group(1).rstrip()
        sep = '' if linea.endswith(('.', '!', '?')) else '.'
        cola = cola[:m[0].start()] + linea + sep + ' ' + txt + cola[m[0].end():]
    despues = {p.numero: (p, r) for p, r in parsear_prueba_o_examen(cab + cola)}
    for n in textos:
        a, b = antes[n][1], despues[n][1]
        assert a.respuesta_correcta == b.respuesta_correcta, (n, a.respuesta_correcta, b.respuesta_correcta)
        assert textos[n].strip()[:20] in b.retroalimentacion, (n, b.retroalimentacion)
        assert a.codigo_oa == b.codigo_oa
    ruta.write_text(cab + cola, encoding='utf-8')
    print(f'{len(textos)} explicaciones en {archivo}')
