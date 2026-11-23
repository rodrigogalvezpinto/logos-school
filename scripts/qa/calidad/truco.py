import re, sys, json, collections as C
from sqlalchemy import create_engine, text
c = create_engine(sys.argv[1]).connect()
P = c.execute(text("""select p.id, p.opciones, p.respuesta_correcta, n.nombre, n.id, (exists(select 1 from conjunto_evaluacion ce where ce.pregunta_ids::jsonb @> to_jsonb(p.id))) en_eval
 from pregunta p join objetivo_aprendizaje o on o.id=p.oa_id join asignatura a on a.id=o.asignatura_id join nivel n on n.id=a.nivel_id
 where p.tipo='alternativas' order by n.id""")).fetchall()
ABS = re.compile(r"\b(nunca|siempre|solo|sólo|únicamente|todos|todas|ninguno|ninguna|jamás|exactamente|completamente|totalmente|cualquier)\b", re.I)
r = C.defaultdict(lambda: [0, 0, 0, 0]); azar = C.defaultdict(float)
for pid, ops, k, nn, nid, ev in P:
    ops = ops or []
    if len(ops) < 3 or k not in ops: continue
    cand = [o for o in ops if not ABS.search(o)] or ops
    elegida = max(cand, key=len)
    clave = (nn, 'evaluaciones' if ev else 'guías')
    r[clave][0] += elegida == k; r[clave][1] += 1; azar[clave] += 1 / len(ops)
    solo_larga = max(ops, key=len)
    r[clave][2] += solo_larga == k
print("curso | material | n | azar | solo «la más larga» | «descartar absolutos + la más larga»")
for (nn, tipo), (ok, n, ol, _) in r.items():
    print(f"{nn} | {tipo} | {n} | {100*azar[(nn,tipo)]/n:.0f}% | {100*ol/n:.0f}% | {100*ok/n:.0f}%")
