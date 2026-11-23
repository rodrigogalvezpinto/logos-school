"""Pistas de forma en las alternativas (auditoría de calidad 2026-11-23, docs/auditorias/CALIDAD-MATERIAL-2026-11-23.md).

Un alumno que no sabe la materia puede acertar descartando las alternativas con palabras absolutas («nunca»,
«siempre», «solo»…) y marcando la más larga de las que quedan. `adivina()` simula ese truco.

    import sys; sys.path.insert(0, 'scripts/herramientas_auditoria')
    from pistas import listar, distractores, resumen
    listar('04-medio/examenes/filosofia-examen-forma-a.md')          # preguntas donde el truco acierta
    distractores('04-medio/examenes/filosofia-examen-forma-a.md', 7, {'a': 'texto nuevo', 'c': '…'})

`distractores` cambia SOLO alternativas incorrectas y verifica con el parser real que la clave (texto y letra),
el tipo, el OA y las demás preguntas no cambien. Si algo cambia, aborta sin escribir.
"""
import glob
import re
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(RAIZ / 'backend/scripts'))
from parser_prueba_examen import parsear_prueba_o_examen  # noqa: E402

ABSOLUTAS = re.compile(r"\b(nunca|siempre|solo|sólo|únicamente|todos|todas|ninguno|ninguna|jamás|exactamente|"
                       r"completamente|totalmente|cualquier)\b", re.I)


def adivina(opciones):
    """Índice que marcaría el alumno que adivina por la forma (la más larga sin absolutos)."""
    candidatas = [i for i, o in enumerate(opciones) if not ABSOLUTAS.search(o)] or list(range(len(opciones)))
    return max(candidatas, key=lambda i: len(opciones[i]))


def prob_acierto(opciones, k):
    """Probabilidad de que el truco acierte la clave k. Una diferencia de largo menor al 10 % no se nota: entre las
    alternativas de largo parecido a la más larga, el alumno elige al azar."""
    candidatas = [i for i, o in enumerate(opciones) if not ABSOLUTAS.search(o)] or list(range(len(opciones)))
    largo = max(len(opciones[i]) for i in candidatas)
    empatadas = [i for i in candidatas if len(opciones[i]) >= 0.9 * largo]
    return (1 / len(empatadas)) if k in empatadas else 0.0


def _preguntas(texto):
    return {p.numero: (p, r) for p, r in parsear_prueba_o_examen(texto)}


def con_pista(archivo):
    """[(n, pregunta, pauta)] de alternativas donde el truco acierta."""
    t = (RAIZ / 'contenido' / archivo).read_text(encoding='utf-8')
    salida = []
    for n, (p, r) in sorted(_preguntas(t).items()):
        if p.tipo != 'alternativas' or not p.opciones or len(p.opciones) < 3 or r.respuesta_correcta not in p.opciones:
            continue
        if prob_acierto(p.opciones, p.opciones.index(r.respuesta_correcta)) >= 0.5:
            salida.append((n, p, r))
    return salida


def listar(archivo, enunciado=True):
    t = (RAIZ / 'contenido' / archivo).read_text(encoding='utf-8')
    total = sum(1 for p, r in _preguntas(t).values() if p.tipo == 'alternativas' and p.opciones and len(p.opciones) >= 3)
    lista = con_pista(archivo)
    print(f'{archivo}: el truco acierta {len(lista)} de {total}')
    for n, p, r in lista:
        k = p.opciones.index(r.respuesta_correcta)
        print(f'\n#{n}' + (f'  {re.sub(chr(10) + "+", " ", p.enunciado)[-260:]}' if enunciado else ''))
        for i, o in enumerate(p.opciones):
            marca = '✔' if i == k else ('✗' if ABSOLUTAS.search(o) else ' ')
            print(f'   {marca} {"abcd"[i]}) [{len(o)}] {o}')


def resumen(patron='*/*/*.md'):
    """Porcentaje de acierto del truco por curso, en pruebas y simulacros."""
    por_curso = {}
    for f in sorted(glob.glob(str(RAIZ / 'contenido' / patron))):
        rel = f.split('contenido/')[1]
        if '/pruebas/' not in rel and '/examenes/' not in rel:
            continue
        t = Path(f).read_text(encoding='utf-8')
        try:
            qs = _preguntas(t).values()
        except Exception:
            continue
        for p, r in qs:
            if p.tipo != 'alternativas' or not p.opciones or len(p.opciones) < 3 or r.respuesta_correcta not in p.opciones:
                continue
            c = por_curso.setdefault(rel.split('/')[0], [0, 0])
            c[1] += 1
            c[0] += prob_acierto(p.opciones, p.opciones.index(r.respuesta_correcta))
    for curso, (ok, n) in por_curso.items():
        print(f'{curso}: {100 * ok / n:.0f}% (n={n})')
    return por_curso


def distractores(archivo, n, nuevos):
    ruta = RAIZ / 'contenido' / archivo
    t = ruta.read_text(encoding='utf-8')
    antes = _preguntas(t)
    p0, r0 = antes[n]
    assert p0.tipo == 'alternativas', p0.tipo
    k = p0.opciones.index(r0.respuesta_correcta)
    for letra, texto in nuevos.items():
        i = 'abcd'.index(letra)
        assert i != k, f'{archivo}#{n}: «{letra}» es la clave; solo se cambian distractores'
        assert texto.strip() and texto.strip() != r0.respuesta_correcta
        viejo = p0.opciones[i]
        # Línea de la alternativa: «c) texto» (con o sin sangría/viñeta). Debe ser única en el archivo.
        # El texto puede venir ajustado en varias líneas (con sangría): se aceptan espacios y saltos entre palabras.
        cuerpo = r'\s+'.join(re.escape(w) for w in viejo.split())
        patron = re.compile(rf'(?m)^([ \t>*-]*\(?{letra}\)[ \t]+){cuerpo}[ \t]*$')
        ms = list(patron.finditer(t))
        if len(ms) != 1:
            # Si el texto se repite en otra pregunta, se acota al bloque de esta pregunta.
            ini = re.search(rf'(?m)^(?:\*\*(?:Pregunta )?{n}[.* ]|{n}\. \*|\*\*{n}\.)', t)
            assert ini, (n, 'no encontré el inicio de la pregunta')
            ms = [m for m in patron.finditer(t, ini.start())][:1]
        assert len(ms) == 1, f'{archivo}#{n}: no ubico la alternativa {letra}) «{viejo[:50]}»'
        m = ms[0]
        t = t[:m.start()] + m.group(1) + texto.strip() + t[m.end():]
    despues = _preguntas(t)
    p1, r1 = despues[n]
    assert set(despues) == set(antes)
    assert p1.tipo == p0.tipo and r1.codigo_oa == r0.codigo_oa
    assert r1.respuesta_correcta == r0.respuesta_correcta and p1.opciones.index(r1.respuesta_correcta) == k, 'cambió la clave'
    for letra, texto in nuevos.items():
        assert p1.opciones['abcd'.index(letra)] == texto.strip(), (letra, p1.opciones)
    for m2, (p, r) in antes.items():
        if m2 != n:
            assert (despues[m2][0].opciones, despues[m2][1].respuesta_correcta) == (p.opciones, r.respuesta_correcta), m2
    ruta.write_text(t, encoding='utf-8')
    print(f'ok {archivo}#{n} — prob. de acierto del truco: {prob_acierto(p1.opciones, k):.0%}')


# ---------------------------------------------------------------------------------------------------------------
# Guías (bancos de autoevaluación), 2026-11-24. Las preguntas se identifican por (OA, n.º dentro del OA), ambos desde 1
# en el orden del archivo. `listar_guia` los muestra como «OA 4·2».
from parser_contenido import parsear_guia  # noqa: E402


def _preguntas_guia(texto):
    salida = []
    for o in parsear_guia(texto):
        for i, p in enumerate(o.preguntas, start=1):
            salida.append(((o.codigo_oficial, o.modulo), i, p))
    return salida


def _alternativas_guia(texto):
    return [(k, i, p) for k, i, p in _preguntas_guia(texto)
            if p.tipo == 'alternativas' and p.opciones and len(p.opciones) >= 3 and p.respuesta_correcta in p.opciones]


def resumen_guias(patron='*/*.md'):
    por_curso = {}
    for f in sorted(glob.glob(str(RAIZ / 'contenido' / patron))):
        rel = f.split('contenido/')[1]
        if rel.count('/') != 1 or '/00-' in rel:
            continue
        for _, _, p in _alternativas_guia(Path(f).read_text(encoding='utf-8')):
            c = por_curso.setdefault(rel.split('/')[0], [0, 0])
            c[1] += 1
            c[0] += prob_acierto(p.opciones, p.opciones.index(p.respuesta_correcta))
    for curso, (ok, n) in sorted(por_curso.items()):
        print(f'{curso}: {100 * ok / n:.1f}% (n={n})')
    return por_curso


def con_pista_guia(archivo):
    t = (RAIZ / 'contenido' / archivo).read_text(encoding='utf-8')
    return [(k, i, p) for k, i, p in _alternativas_guia(t)
            if prob_acierto(p.opciones, p.opciones.index(p.respuesta_correcta)) >= 0.5]


def listar_guia(archivo, enunciado=True):
    lista = con_pista_guia(archivo)
    print(f'{archivo}: {len(lista)} con pista')
    for (oa, mod), i, p in lista:
        k = p.opciones.index(p.respuesta_correcta)
        print(f'\n[{oa}{"/" + mod if mod else ""}·{i}]' + (f'  {re.sub(chr(10) + "+", " ", p.enunciado)[-200:]}' if enunciado else ''))
        for j, o in enumerate(p.opciones):
            marca = '✔' if j == k else ('✗' if ABSOLUTAS.search(o) else ' ')
            print(f'   {marca} {"abcd"[j]}) [{len(o)}] {o}')


def distractores_guia(archivo, oa, i, nuevos, modulo=None):
    """Cambia distractores de la pregunta i (desde 1) del OA `oa` (p. ej. 'OA 4') de una guía."""
    ruta = RAIZ / 'contenido' / archivo
    t = ruta.read_text(encoding='utf-8')
    antes = _preguntas_guia(t)
    objetivo = [(k, j, p) for k, j, p in antes if k[0] == oa and j == i and (modulo is None or k[1] == modulo)]
    assert len(objetivo) == 1, f'{archivo}: no ubico {oa}·{i} ({len(objetivo)} coincidencias)'
    p0 = objetivo[0][2]
    assert p0.tipo == 'alternativas'
    k = p0.opciones.index(p0.respuesta_correcta)
    # Ancla: las primeras palabras del enunciado (última línea, sin marcadores), para acotar la búsqueda.
    palabras = re.sub(r'[*_>#]', ' ', p0.enunciado).split()[-6:]
    ancla = re.compile(r'\s+'.join(re.escape(w) for w in palabras))
    ms_ancla = list(ancla.finditer(t))
    if not ms_ancla:
        # Respaldo: la línea de la alternativa correcta, retrocediendo hasta la primera alternativa («a)»).
        cuerpo_k = r'\s+'.join(re.escape(w) for w in p0.opciones[k].split())
        ancla = re.compile(rf'(?m)^[ \t>*-]*\(?{"abcd"[k]}\)[ \t]+{cuerpo_k}[ \t]*$')
        ms_k = list(ancla.finditer(t))
        ms_ancla = [type('M', (), {'end': (lambda s, v=max(0, m.start() - 1500): v)})() for m in ms_k]
    assert ms_ancla, f'{archivo}: no ubico el enunciado de {oa}·{i}'
    for letra, texto in nuevos.items():
        j = 'abcd'.index(letra)
        assert j != k, f'{archivo} {oa}·{i}: «{letra}» es la clave'
        viejo = p0.opciones[j]
        cuerpo = r'\s+'.join(re.escape(w) for w in viejo.split())
        patron = re.compile(rf'(?m)^([ \t>*-]*\(?{letra}\)[ \t]+){cuerpo}[ \t]*$')
        candidatos = [m for a in ms_ancla for m in [patron.search(t, a.end())] if m and m.start() - a.end() < 3000]
        if len({c.start() for c in candidatos}) > 1:
            candidatos = [min(candidatos, key=lambda c: c.start())]
        candidatos = list({m.start(): m for m in candidatos}.values())
        assert len(candidatos) == 1, f'{archivo} {oa}·{i}: no ubico {letra}) «{viejo[:40]}» ({len(candidatos)})'
        m = candidatos[0]
        t = t[:m.start()] + m.group(1) + texto.strip() + t[m.end():]
        ms_ancla = list(ancla.finditer(t)) or ms_ancla
    despues = _preguntas_guia(t)
    assert len(despues) == len(antes)
    for (ka, ia, pa), (kd, idd, pd) in zip(antes, despues):
        assert (ka, ia, pa.tipo, pa.respuesta_correcta, pa.retroalimentacion) == (kd, idd, pd.tipo, pd.respuesta_correcta, pd.retroalimentacion), (ka, ia)
        if (ka[0], ia) != (oa, i):
            assert pa.opciones == pd.opciones and pa.enunciado == pd.enunciado, (ka, ia)
        else:
            assert pd.opciones.index(pd.respuesta_correcta) == k
            for letra, texto in nuevos.items():
                assert pd.opciones['abcd'.index(letra)] == texto.strip()
    ruta.write_text(t, encoding='utf-8')
    print(f'ok {archivo} {oa}·{i} — {prob_acierto(pd.opciones, k):.0%}' if False else
          f'ok {archivo} {oa}·{i} — prob. del truco: {prob_acierto([q for q in despues if q[0][0] == oa and q[1] == i][0][2].opciones, k):.0%}')


def seguras_guia(patron):
    """Preguntas de guía donde el truco acierta con certeza (100 %), las más rentables de corregir."""
    for f in sorted(glob.glob(str(RAIZ / 'contenido' / patron))):
        rel = f.split('contenido/')[1]
        if rel.count('/') != 1 or '/00-' in rel:
            continue
        for (oa, mod), i, p in _alternativas_guia(Path(f).read_text(encoding='utf-8')):
            k = p.opciones.index(p.respuesta_correcta)
            if prob_acierto(p.opciones, k) == 1:
                print(f'\n{rel} [{oa}{"/" + mod if mod else ""}·{i}]')
                for j, o in enumerate(p.opciones):
                    print(f'   {"✔" if j == k else ("✗" if ABSOLUTAS.search(o) else " ")} {"abcd"[j]}) [{len(o)}] {o}')
