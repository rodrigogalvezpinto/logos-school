"""Lista, en pruebas y simulacros, las líneas de texto citado (>) que no quedan dentro del enunciado de ninguna pregunta: lecturas que el alumno no ve (§15.37). Uso: cd backend && python scripts/estimulos_huerfanos.py"""
import sys,re
from pathlib import Path
sys.path.insert(0,'scripts')
from parser_prueba_examen import parsear_prueba_o_examen
tot=0
for f in sorted(Path('../contenido').glob('*/*/*.md')):
    if f.parent.name not in ('pruebas','examenes'): continue
    t=f.read_text(); r=parsear_prueba_o_examen(t)
    enun=" ".join(p.enunciado for p,_ in r)
    norm=lambda s: re.sub(r"\W+"," ",s).strip()
    E=norm(enun)
    corte=t.find('Pauta'); cuerpo=t[:corte] if corte>0 else t
    huer=[l for l in cuerpo.splitlines() if l.startswith('>') and len(norm(l[1:]))>25 and norm(l[1:].replace('**','')) not in E]
    if huer:
        tot+=1; print(f.relative_to('../contenido'), len(huer), '|', huer[0][:90])
print('archivos con estímulos huérfanos:', tot)
