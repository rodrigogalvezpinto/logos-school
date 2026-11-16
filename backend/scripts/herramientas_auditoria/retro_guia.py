"""Reemplaza la retroalimentación de una pregunta de GUÍA (control C.4b, 2026-11-16).

    from retro_guia import cambiar, ver
    ver('05-basico')                                    # lista las candidatas del detector, numeradas
    cambiar('05-basico/ciencias-naturales.md', 'Los distintos depósitos', 'Texto nuevo que explica la respuesta.')

`cambiar` busca la pregunta cuya retroalimentación (ya limpia) empieza con `inicio`; reemplaza el texto completo de
la retroalimentación en el archivo (aunque ocupe varias líneas) y verifica con el parser que solo cambió esa
retroalimentación: mismas preguntas, enunciados, opciones y claves. Si algo no calza, no escribe.
"""
import re
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(RAIZ / 'backend/scripts'))
from parser_contenido import parsear_guia  # noqa: E402

MARCA = re.compile(r'(?:💬\s*)?\**\s*Retroalimentaci[óo]n\s*\**\s*:\s*\**\s*', re.IGNORECASE)
FIN = re.compile(r'^\s*$|^\s*(?:\*\*)?\d+[.)]|^\s*#|^\s*---|^\s*(?:\*\*)?(?:Pregunta|Ejercicio)\b|^\s*✅|^\s*\*?Respuesta', re.I)


def _todas(texto):
    return [(oa.codigo_oficial, i, q) for oa in parsear_guia(texto) for i, q in enumerate(oa.preguntas, 1)]


def _norm(s):
    return re.sub(r'\s+', ' ', s.replace('*', '')).strip()


def cambiar(archivo, inicio, nueva):
    ruta = RAIZ / 'contenido' / archivo
    t = ruta.read_text(encoding='utf-8')
    antes = _todas(t)
    objetivo = [x for x in antes if _norm(x[2].retroalimentacion).startswith(_norm(inicio))]
    if len(objetivo) != 1:
        raise SystemExit(f'{archivo}: {len(objetivo)} retroalimentaciones empiezan con «{inicio[:40]}»')
    actual = _norm(objetivo[0][2].retroalimentacion)
    lineas = t.split('\n')
    # Ubicar la marca de retroalimentación cuyo texto (con sus líneas de continuación) coincide con la retroalimentación
    # completa de la pregunta objetivo. Debe haber exactamente una: dos retroalimentaciones pueden empezar igual (2026-11-16
    # se reemplazó por error la de otra pregunta que compartía las primeras palabras).
    ubicaciones = []
    for k, linea in enumerate(lineas):
        m = MARCA.search(linea)
        if not m:
            continue
        f = k + 1
        while f < len(lineas) and not FIN.match(lineas[f]) and not MARCA.search(lineas[f]):
            f += 1
        texto = _norm(' '.join([linea[m.end():]] + lineas[k + 1:f]))
        if texto.startswith(actual[:120]) or actual.startswith(texto[:120]):
            ubicaciones.append((k, m.end(), f))
    if len(ubicaciones) != 1:
        raise SystemExit(f'{archivo}: {len(ubicaciones)} lugares coinciden con «{actual[:50]}»; usa un inicio más largo')
    idx, col, fin = ubicaciones[0]
    cola_marca = lineas[idx][:col]
    # conservar cierre de cursiva/negrita del formato original si la línea terminaba con «*»
    nueva_linea = cola_marca + ' '.join(nueva.split())
    nuevo_t = '\n'.join(lineas[:idx] + [nueva_linea] + lineas[fin:])
    despues = _todas(nuevo_t)
    assert len(despues) == len(antes), 'cambió el número de preguntas'
    cambios = 0
    for (oa0, i0, q0), (oa1, i1, q1) in zip(antes, despues):
        assert (oa0, i0, q0.tipo, q0.enunciado, q0.opciones, q0.respuesta_correcta) == \
               (oa1, i1, q1.tipo, q1.enunciado, q1.opciones, q1.respuesta_correcta), f'cambió otra parte de {oa0} #{i0}'
        if q0.retroalimentacion != q1.retroalimentacion:
            cambios += 1
            assert (oa0, i0) == objetivo[0][:2], f'cambió la pregunta {oa0} #{i0}, no la buscada {objetivo[0][:2]}'
            assert _norm(q1.retroalimentacion) == _norm(nueva), (q1.retroalimentacion, nueva)
    assert cambios == 1, f'{cambios} retroalimentaciones cambiaron'
    ruta.write_text(nuevo_t, encoding='utf-8')
    print(f'ok {archivo} «{actual[:40]}…»')


def ver(curso):
    import retro_guia_pobres as d  # noqa: E402
    for n, (rel, oa, i, q) in enumerate(d.candidatas(curso), 1):
        ops = '\n'.join(f'      {"*" if o == q.respuesta_correcta or o in q.respuesta_correcta else " "} {o[:120]}'
                        for o in (q.opciones or []))
        print(f'[{n}] {rel} | {oa.codigo_oficial} #{i}\n   P: {q.enunciado[:300]}\n{ops}\n'
              f'   CLAVE: {q.respuesta_correcta[:160]}\n   RETRO: {q.retroalimentacion[:220]}')
