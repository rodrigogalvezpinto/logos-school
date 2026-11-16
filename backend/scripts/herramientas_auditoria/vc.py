from pathlib import Path
import sys; sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from parser_prueba_examen import parsear_prueba_o_examen
from explicaciones_pobres import buscar as lista
C=Path(__file__).resolve().parents[3] / 'contenido'
def vc(archivo, maxe=230):
    ns=lista().get(archivo,[])
    d={p.numero:(p,r) for p,r in parsear_prueba_o_examen((C/archivo).read_text())}
    print('#####',archivo,ns)
    for n in ns:
        p,r=d[n]; e=p.enunciado.split('\n\n')[-1]
        ops=' | '.join(f"{'abcd'[i]}){'*' if o==r.respuesta_correcta else ''} {o[:70]}" for i,o in enumerate(p.opciones)) if p.tipo!='verdadero_falso' else f'VF={r.respuesta_correcta}'
        if p.tipo=='varias_correctas': ops+=f' || CLAVE {r.respuesta_correcta[:120]}'
        print(f'{n}. {e[:maxe]}\n   {ops}')
if __name__=='__main__':
    for a in sys.argv[1:]: vc(a)
