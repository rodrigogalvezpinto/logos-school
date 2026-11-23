import json, re, sys, collections as C
from sqlalchemy import create_engine, text
c = create_engine(sys.argv[1]).connect()
P = c.execute(text("""select p.id, p.tipo, p.enunciado, p.opciones, p.respuesta_correcta, p.retroalimentacion, n.nombre
 from pregunta p join objetivo_aprendizaje o on o.id=p.oa_id join asignatura a on a.id=o.asignatura_id join nivel n on n.id=a.nivel_id order by n.id""")).fetchall()
jerga = re.compile(r"\b(este OA|del OA|el OA|la clave|distractor(es)?|el ítem|ítems?|la pauta|sesgo|estímulo)\b", re.I)
hits = C.Counter(); ej = []
for p in P:
    for campo, t in (("enunciado", p[2]), ("retro", p[5]), ("opciones", json.dumps(p[3] or [], ensure_ascii=False))):
        if jerga.search(t or ""):
            hits[(p[6], campo)] += 1
            if len(ej) < 14: ej.append((p[6], p[0], campo, jerga.search(t).group(0), (t or "")[:120]))
print("Jerga interna visible al alumno:", sum(hits.values())); 
for k, v in sorted(hits.items()): print("  ", k, v)
for e in ej: print("   ·", e)
ABS = re.compile(r"\b(nunca|siempre|solo|sólo|únicamente|todos|todas|ninguno|ninguna|jamás|exactamente iguales|completamente|totalmente|cualquier)\b", re.I)
print("\nPalabras absolutas — % de claves vs % de distractores (alternativas de 4 opciones):")
for nivel in dict.fromkeys(p[6] for p in P):
    k = d = nk = nd = 0
    for p in P:
        if p[6] != nivel or p[1] != 'alternativas': continue
        ops = p[3] or []
        if len(ops) != 4 or p[4] not in ops: continue
        for o in ops:
            if o == p[4]: nk += 1; k += bool(ABS.search(o))
            else: nd += 1; d += bool(ABS.search(o))
    print(f"  {nivel}: claves {100*k/max(nk,1):.0f}% · distractores {100*d/max(nd,1):.0f}%")
minus = sum(1 for p in P if p[5] and p[5][0].islower())
print("\nRetroalimentación que empieza en minúscula:", minus, f"({100*minus/len(P):.0f}%)")
