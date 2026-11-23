import json, sys, random
from sqlalchemy import create_engine, text
e = create_engine(sys.argv[1]); c = e.connect()
def ver(r):
    print(f"\n[{r.nivel} · {r.asig} · OA {r.oa} · id {r.id} · {r.tipo}]\n{r.enunciado}")
    for i, o in enumerate(r.opciones or []): print(f"   {'abcdef'[i]}) {o}")
    print(f"   ✔ {r.respuesta_correcta}\n   ↳ {r.retroalimentacion[:400]}")
base = """select p.id, p.tipo, p.enunciado, p.opciones, p.respuesta_correcta, p.retroalimentacion, n.nombre nivel, a.nombre asig, o.codigo_oficial oa
 from pregunta p join objetivo_aprendizaje o on o.id=p.oa_id join asignatura a on a.id=o.asignatura_id join nivel n on n.id=a.nivel_id"""
if sys.argv[2] == 'ids':
    for r in c.execute(text(base + " where p.id = any(:ids)"), {"ids": [int(x) for x in sys.argv[3].split(',')]}): ver(r)
else:
    random.seed(int(sys.argv[3]))
    for (nid,) in c.execute(text("select id from nivel order by id")):
        ids = [x[0] for x in c.execute(text("select p.id from pregunta p join objetivo_aprendizaje o on o.id=p.oa_id join asignatura a on a.id=o.asignatura_id where a.nivel_id=:n"), {"n": nid})]
        for i in random.sample(ids, int(sys.argv[2])):
            for r in c.execute(text(base + " where p.id=:i"), {"i": i}): ver(r)
