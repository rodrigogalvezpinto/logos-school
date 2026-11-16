from pathlib import Path
import sys,re; sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from difflib import SequenceMatcher
from parser_contenido import parsear_guia
from parser_prueba_examen import parsear_prueba_o_examen
from solapamiento_pruebas_guias import normalizar
C=Path(__file__).resolve().parents[3] / 'contenido'
def match(archivo, n):
    curso=archivo.split('/')[0]
    g=[(q, normalizar(q.enunciado)) for r in (C/curso).glob('*.md') if not r.name.startswith('00') for oa in parsear_guia(r.read_text()) for q in oa.preguntas]
    p,r={x.numero:(x,y) for x,y in parsear_prueba_o_examen((C/archivo).read_text())}[n]
    e=normalizar(p.enunciado.split('\n\n')[-1])
    q=max(g,key=lambda x:SequenceMatcher(None,e,x[1]).ratio())[0]
    print(f'== {archivo}#{n} [{p.tipo}] OA {r.codigo_oa}\nP: {p.enunciado.split(chr(10)*2)[-1][:260]}')
    for i,o in enumerate(p.opciones): print(f'   {"abcdefgh"[i]}) {o[:110]}{"  ✅" if o==r.respuesta_correcta else ""}')
    print(f'G: {q.enunciado[:160]}')


def candidatos(curso):
    """Muestra, para un curso (p. ej. '02-basico'), cada pregunta que el detector marca como «misma pregunta y clave»
    o «escenario de la guía repetido», junto a la pregunta más parecida de la guía."""
    import solapamiento_pruebas_guias as s
    carpeta_curso = C / curso
    vistos = set()
    for carpeta in ('pruebas', 'examenes'):
        for fn in (s.escenarios_copiados, s.misma_clave):
            for archivo, nums in fn(carpeta_curso, carpeta).items():
                for n in nums:
                    if (archivo, n) not in vistos:
                        vistos.add((archivo, n))
                        match(archivo, n)
