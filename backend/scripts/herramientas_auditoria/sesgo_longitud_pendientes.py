"""C.6: lista las alternativas con sesgo de longitud y el largo mínimo que necesita el distractor más largo.
Uso desde backend/: .venv/bin/python scripts/herramientas_auditoria/sesgo_longitud_pendientes.py '02-medio/pruebas/*.md'
"""
import sys; sys.path.insert(0, str(__import__('pathlib').Path(__file__).resolve().parents[1]))
from ajustar_distractores import items, sesgada, RAIZ
from pathlib import Path
import math
for patron in sys.argv[1:]:
    for ruta in sorted((RAIZ/'contenido').glob(patron)):
        for k,(tipo,_,ops,clave,_) in items(ruta,ruta.read_text()).items():
            if tipo=='alternativas' and sesgada(ops,clave):
                otros=[(chr(97+i),o) for i,o in enumerate(ops) if o!=clave]
                l,o=max(otros,key=lambda x:len(x[1]))
                print(f'{ruta.relative_to(RAIZ/"contenido")} #{k} clave={len(clave)} necesita≥{math.ceil(len(clave)*0.9)+1} | mayor {l})[{len(o)}] {o}')
