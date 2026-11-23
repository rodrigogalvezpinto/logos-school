"""Lectura de las guías (2026-11-24): reemplaza el bloque n.º n (desde 1) de «**Explicación pedagógica**» de una guía
por una versión con oraciones cortas, verificando con el parser que las preguntas del banco no cambien.

    import sys; sys.path.insert(0, 'scripts/herramientas_auditoria')
    from lectura import bloques, explicacion
    bloques('02-basico/ciencias-naturales.md')            # muestra los bloques numerados
    explicacion('02-basico/ciencias-naturales.md', 1, 'Texto nuevo…')
"""
import re
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(RAIZ / 'backend/scripts'))
from parser_contenido import parsear_guia  # noqa: E402

RE_BLOQUE = re.compile(r'(\*\*Explicación pedagógica\*\*\s*\n)(.*?)(?=\n\*\*[A-ZÁÉÍÓÚ][^*\n]+\*\*|\n### |\Z)', re.S)


def bloques(archivo):
    t = (RAIZ / 'contenido' / archivo).read_text(encoding='utf-8')
    for i, m in enumerate(RE_BLOQUE.finditer(t), start=1):
        print(f'=== {i}\n{m.group(2).strip()}\n')


def _firma(texto):
    return [(o.codigo_oficial, o.modulo, [(p.tipo, p.enunciado, p.opciones, p.respuesta_correcta, p.retroalimentacion)
                                          for p in o.preguntas]) for o in parsear_guia(texto)]


def explicacion(archivo, n, nuevo, ancho=88):
    ruta = RAIZ / 'contenido' / archivo
    t = ruta.read_text(encoding='utf-8')
    ms = list(RE_BLOQUE.finditer(t))
    m = ms[n - 1]
    # Ajusta cada párrafo a `ancho` columnas, como el resto del archivo.
    parrafos = []
    for p in re.split(r'\n\s*\n', nuevo.strip()):
        palabras, lineas, linea = p.split(), [], ''
        for w in palabras:
            if linea and len(linea) + 1 + len(w) > ancho:
                lineas.append(linea)
                linea = w
            else:
                linea = f'{linea} {w}' if linea else w
        lineas.append(linea)
        parrafos.append('\n'.join(lineas))
    t2 = t[:m.start(2)] + '\n' + '\n\n'.join(parrafos) + '\n' + t[m.end(2):]
    assert _firma(t2) == _firma(t), 'cambió el banco de preguntas'
    ruta.write_text(t2, encoding='utf-8')
    oraciones = [o for o in re.split(r'(?<=[.!?:;])\s+', ' '.join(nuevo.split())) if len(o.split()) > 2]
    print(f'ok {archivo} bloque {n}: {sum(len(o.split()) for o in oraciones) / len(oraciones):.0f} palabras por oración')


def seccion(archivo, n, nuevo, inicio='#### Explicación\n\n'):
    """Reemplaza el cuerpo de la n-ésima sección que empieza con `inicio` (1 = primera) hasta el
    siguiente encabezado. `nuevo` va tal cual (con viñetas). Verifica que las preguntas no cambien."""
    ruta = RAIZ / 'contenido' / archivo
    texto = ruta.read_text()
    pos = -1
    for _ in range(n):
        pos = texto.index(inicio, pos + 1)
    a = pos + len(inicio)
    m = re.compile(r'\n(?=#{1,4} |---\n)').search(texto, a)
    b = m.start() if m else len(texto)
    nuevo_texto = texto[:a] + nuevo.strip() + '\n' + texto[b:]
    assert _firma(nuevo_texto) == _firma(texto), 'cambiaron las preguntas'
    ruta.write_text(nuevo_texto)
    ors = [o for o in re.split(r'(?<=[.!?:])\s+', ' '.join(nuevo.split())) if len(o.split()) > 2]
    print(f'{archivo} §{n}: {sum(len(o.split()) for o in ors) / len(ors):.1f} palabras por oración')
