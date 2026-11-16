from pathlib import Path
"""Rehace una pregunta (enunciado + alternativas + pauta) en cualquier formato de numeración.
rehacer(archivo, n, enunciado, opciones, explicacion)  # opciones: lista; la clave queda en la MISMA letra
¡Ojo! La correcta debe ir en la letra de la clave original. Si la explicación empieza con «x)», se verifica esa letra.
Para V/F: opciones=None. Verifica con el parser: misma letra de clave, mismo tipo, mismo OA.
"""
import re
import sys

RAIZ = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(RAIZ / 'backend/scripts'))
from parser_prueba_examen import parsear_prueba_o_examen  # noqa: E402

RE_PAUTA = re.compile(r'(?mi)^#{1,6}\s*(?:respuestas \(pauta\)|pauta|hoja de respuestas)|^\*\*Pauta')


def _parse(t):
    return {p.numero: (p, r) for p, r in parsear_prueba_o_examen(t)}


def rehacer(archivo, n, enunciado, opciones, explicacion, clave_vf=None, solo_explicacion=False):
    """solo_explicacion=True: no toca el enunciado ni las alternativas; solo reemplaza la entrada de la pauta (C.4c)."""
    ruta = RAIZ / 'contenido' / archivo
    t = ruta.read_text(encoding='utf-8')
    antes = _parse(t)
    p0, r0 = antes[n]
    m = RE_PAUTA.search(t)
    corte = m.start() if m else len(t)
    cab, cola = t[:corte], t[corte:]
    if solo_explicacion:
        opciones = list(p0.opciones) if p0.tipo != 'verdadero_falso' else None
    # 1) inicio de la pregunta n (se omite con solo_explicacion)
    if not solo_explicacion:
        ini = re.compile(rf'(?m)^(?:\*\*(?:Pregunta )?{n}[.* ]|{n}\. \*|{n}\. \*\*|\*\*{n}\.)')
        ms = list(ini.finditer(cab))
        assert len(ms) == 1, (n, 'inicio', len(ms))
        i = ms[0].start()
        # fin: siguiente pregunta, separador, encabezado o declaración de estímulo
        fin_re = re.compile(rf'(?m)^(?:\*\*(?:Pregunta )?{n + 1}[.* ]|{n + 1}\. \*|\*\*{n + 1}\.|---$|#|\*{{0,2}}\(?[ \t]*(?:Lee|Lea|Observa|Utiliza|Usa)\b)')
        mf = fin_re.search(cab, ms[0].end())
        j = mf.start() if mf else len(cab)
        bloque = cab[i:j]
        # etiqueta: todo hasta el cierre de la marca de tipo (p. ej. «**3. (Alternativas)** » o «3. *(Alternativas)* »)
        me = re.match(r'(\*\*(?:Pregunta )?\d+\.?\*\*\s*(?:\*?\([^)]*\)\*?)?\s*|\*\*(?:Pregunta )?\d+\.?\s*\([^)]*\)\*\*\s*|\*\*(?:Pregunta )?\d+ \([^)]*\)\.?\*\*\s*|\d+\. \*\([^)]*\)\*\s*|\d+\. \*\*\([^)]*\)\*\*\s*)', bloque)
        assert me, (n, 'etiqueta', bloque[:80])
        etiqueta = me.group(1).rstrip() + ' '
        nuevo = etiqueta + enunciado.strip() + '\n'
        if opciones:
            nuevo += '\n' + '\n'.join(f"{'abcdefgh'[k]}) {o}" for k, o in enumerate(opciones)) + '\n'
        cab = cab[:i] + nuevo + '\n' + cab[j:].lstrip('\n') if not cab[j:].startswith('---') else cab[:i] + nuevo + '\n' + cab[j:]
    # 2) pauta: reemplaza la línea (tabla o lista) de n
    letra = None
    varias = p0.tipo == 'varias_correctas'
    if varias:
        import json
        idx_correctas = sorted(p0.opciones.index(c) for c in json.loads(r0.respuesta_correcta))
        letras = ['abcdefgh'[k] for k in idx_correctas]
        etiqueta_letras = ', '.join(letras[:-1]) + ' y ' + letras[-1] if len(letras) > 1 else letras[0]
    elif opciones:
        letra = 'abcdefgh'[p0.opciones.index(r0.respuesta_correcta)] if r0.respuesta_correcta in p0.opciones else None
    # Protección (2026-11-16): si la explicación empieza con letras («c) …», «a y c) …»), deben ser las de la clave,
    # que se conserva en la MISMA letra; si no coinciden, la correcta quedó en otra posición y la clave sería falsa.
    m_letras = re.match(r'\(?([a-h](?:, [a-h])*(?: y [a-h])?)\) +', explicacion.strip())
    if m_letras:
        esperadas = etiqueta_letras if varias else (letra if opciones else None)
        if esperadas and m_letras.group(1) != esperadas:
            raise SystemExit(f'{archivo}#{n}: la explicación dice «{m_letras.group(1)})» pero la clave está en «{esperadas}»; '
                             'reordena las opciones para que la correcta quede en esa letra')
        explicacion = explicacion.strip()[m_letras.end():]
    fila = re.compile(rf'(?m)^(\| *{n} *\|)(.*)$')
    mfila = [x for x in fila.finditer(cola)]
    if varias:
        cuerpo = f"**{etiqueta_letras}.** {explicacion.strip()}"
    elif opciones:
        clave_txt = opciones['abcdefgh'.index(letra)] if letra else None
        cuerpo = f"**{letra}) {clave_txt}.** {explicacion.strip()}" if letra else explicacion.strip()
    else:
        cuerpo = f"**{clave_vf or r0.respuesta_correcta}.** {explicacion.strip()}"
    if len(mfila) == 1:
        celdas = mfila[0].group(2).rstrip().rstrip('|').split('|')
        patron_celda = r'^\s*\**\s*\(?(?:[a-h](?:, [a-h])*(?: y [a-h])?[.)]|Verdadero|Falso)'
        candidatas_k = [x for x, c in enumerate(celdas) if re.search(patron_celda, c)] or \
                       [x for x, c in enumerate(celdas) if r0.respuesta_correcta[:10].lower() in c.lower()]
        assert len(candidatas_k) == 1, (n, 'celda de la pauta', celdas)
        k = candidatas_k[0]
        celdas[k] = ' ' + cuerpo + ' '
        cola = cola[:mfila[0].start()] + mfila[0].group(1) + '|'.join(celdas) + '|' + cola[mfila[0].end():]
    else:
        # La entrada incluye TODAS sus líneas de continuación (antes solo las sangradas: quedaban restos del texto viejo).
        item = re.compile(rf'(?m)^((?:\*\*{n}\.\*\*|\*\*{n}\.|{n}\.)) .*$'
                          r'(?:\n(?![ \t]*$)(?![ \t]*(?:\*\*)?\(?\d+[.)])(?![ \t]*[|#>])(?![ \t]*-{3}).*$)*')
        mi = list(item.finditer(cola))
        assert len(mi) == 1, (n, 'pauta', len(mi))
        cola = cola[:mi[0].start()] + mi[0].group(1) + ' ' + cuerpo + cola[mi[0].end():]
    nuevo_t = cab + cola
    despues = _parse(nuevo_t)
    p1, r1 = despues[n]
    assert p1.tipo == p0.tipo, (p0.tipo, p1.tipo)
    assert r1.codigo_oa == r0.codigo_oa
    if varias:
        import json
        assert sorted(p1.opciones.index(c) for c in json.loads(r1.respuesta_correcta)) == idx_correctas, 'letras correctas cambiaron'
    elif opciones:
        assert p1.opciones == [o.strip() for o in opciones] or len(p1.opciones) == len(opciones), p1.opciones
        assert p1.opciones.index(r1.respuesta_correcta) == p0.opciones.index(r0.respuesta_correcta), 'letra de clave cambió'
    else:
        assert r1.respuesta_correcta == r0.respuesta_correcta
    assert set(despues) == set(antes)
    final = re.sub(r'\s+', ' ', explicacion.strip())
    assert re.sub(r'\s+', ' ', r1.retroalimentacion).rstrip().endswith(final[-40:]), \
        f'la pauta de #{n} no termina en la explicación nueva (¿quedaron restos del texto anterior?)'
    ruta.write_text(nuevo_t, encoding='utf-8')
    print(f'ok {archivo}#{n}')
