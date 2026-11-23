import json, re, sys, statistics as st, collections as C
from sqlalchemy import create_engine, text
e = create_engine(sys.argv[1])
q = lambda s: e.connect().execute(text(s)).fetchall()
niv = {r[0]: r[1] for r in q("select id, nombre from nivel order by id")}
asig = {r[0]: (r[1], r[2]) for r in q("select id, nombre, nivel_id from asignatura")}
oas = q("select id, asignatura_id from objetivo_aprendizaje")
P = q("select id, oa_id, tipo, enunciado, opciones, respuesta_correcta, retroalimentacion, nivel_dificultad, asignatura_id from pregunta")
conj = q("select tipo, nivel_id, asignatura_id, pregunta_ids from conjunto_evaluacion")
en_conj = {}
for t, n, a, ids in conj:
    for i in (ids if isinstance(ids, list) else json.loads(ids or '[]')): en_conj.setdefault(i, set()).add(t)
nivel_de = {}
for p in P:
    a = p[8]
    if a is None and p[1]:
        a = next((x[1] for x in oas if x[0] == p[1]), None)
    nivel_de[p[0]] = asig[a][1] if a in asig else None
print("Tipos de conjunto:", C.Counter(t for t, *_ in conj))
# --- Por curso
print("\n## Por curso")
print("curso | preguntas | banco guía | en pruebas/simulacros | OA | OA sin autoeval | OA sin prueba/simulacro | %clave más larga | palabras enunciado (mediana)")
oa_niv = C.defaultdict(set)
for oid, aid in oas: oa_niv[asig[aid][1]].add(oid)
for nid, nn in niv.items():
    ps = [p for p in P if nivel_de[p[0]] == nid]
    banco = [p for p in ps if p[0] not in en_conj]
    evals = [p for p in ps if p[0] in en_conj]
    oa_auto = {p[1] for p in banco}; oa_eval = {p[1] for p in evals}
    larga = tot = 0
    for p in ps:
        ops = p[4] if isinstance(p[4], (list, dict)) else json.loads(p[4] or 'null')
        if p[2] == 'alternativas' and isinstance(ops, list) and len(ops) >= 3:
            corr = p[5].strip()
            textos = [str(o) for o in ops]
            idx = next((i for i, o in enumerate(textos) if o.strip() == corr or o.strip().startswith(corr + ')') or o.strip()[:2] == corr[:1] + ')'), None)
            if idx is None and len(corr) == 1 and corr.lower() in 'abcdef': idx = 'abcdef'.index(corr.lower())
            if idx is not None and idx < len(textos):
                tot += 1; L = [len(t) for t in textos]
                if L[idx] == max(L) and L.count(max(L)) == 1: larga += 1
    pal = st.median([len(p[3].split()) for p in ps]) if ps else 0
    print(f"{nn} | {len(ps)} | {len(banco)} | {len(evals)} | {len(oa_niv[nid])} | {len(oa_niv[nid]-oa_auto)} | {len(oa_niv[nid]-oa_eval)} | {100*larga/max(tot,1):.0f}% de {tot} | {pal}")
# --- Posición de la clave
print("\n## Posición de la clave (alternativas)")
pos = C.Counter(); muestra = []
for p in P:
    if p[2] != 'alternativas': continue
    r = p[5].strip().lower()
    if len(r) == 1: pos[r] += 1
    else: muestra.append(r[:30])
print(pos, "| no-letra:", len(muestra), muestra[:3])
print("\n## Formato de opciones y respuesta (muestra)")
for t in ('alternativas', 'varias_correctas', 'verdadero_falso'):
    p = next(x for x in P if x[2] == t); print(t, '| opciones:', str(p[4])[:160], '| resp:', p[5][:60])
# --- Retroalimentación
lr = [len(p[6]) for p in P]
print("\n## Retroalimentación: mediana", st.median(lr), "caracteres; vacías:", sum(1 for x in lr if x < 5), "; < 40 car.:", sum(1 for x in lr if x < 40))
# --- Duplicados de enunciado dentro del curso
norm = lambda s: re.sub(r'\W+', ' ', s.lower()).strip()
dup = C.Counter((nivel_de[p[0]], norm(p[3])) for p in P)
d = [(k, v) for k, v in dup.items() if v > 1]
print("\n## Enunciados repetidos idénticos dentro de un curso:", len(d), "grupos,", sum(v for _, v in d), "preguntas")
for (n, s), v in sorted(d, key=lambda x: -x[1])[:8]: print(f"  {niv.get(n)} ×{v}: {s[:110]}")
# --- Malas prácticas de redacción
todas = sum(1 for p in P if re.search(r'todas las anteriores|ninguna de las anteriores', str(p[4]).lower()))
neg = sum(1 for p in P if re.search(r'\b(NO|EXCEPTO|INCORRECTA)\b', p[3]))
print("\n## Redacción: 'todas/ninguna de las anteriores':", todas, "| enunciados en negativo (NO/EXCEPTO/INCORRECTA):", neg)
print("## Dificultad:", C.Counter(p[7] for p in P))
print("## Sin OA:", sum(1 for p in P if not p[1]))
nops = C.Counter(len(p[4]) if isinstance(p[4], list) else (len(json.loads(p[4])) if p[4] else 0) for p in P if p[2] == 'alternativas')
print("## N.º de alternativas:", nops)
vf = C.Counter(p[5].strip().lower()[:10] for p in P if p[2] == 'verdadero_falso'); print("## V/F claves:", vf)
print("\n## Posición real de la clave (alternativas con 4 opciones), por curso")
for nid, nn in niv.items():
    c = C.Counter(); larga = cortas = n = 0; ej = []
    for p in P:
        if nivel_de[p[0]] != nid or p[2] != 'alternativas': continue
        ops = p[4] if isinstance(p[4], list) else json.loads(p[4] or '[]')
        if len(ops) != 4 or p[5] not in ops: continue
        i = ops.index(p[5]); c['abcd'[i]] += 1; n += 1
        L = [len(o) for o in ops]; otros = [l for j, l in enumerate(L) if j != i]
        if L[i] > max(otros): larga += 1
        if L[i] >= 1.25 * max(otros) and L[i] - max(otros) >= 10: cortas += 1; ej.append(p[0])
    print(f"{nn}: {dict(sorted(c.items()))} | correcta estrictamente más larga {100*larga/max(n,1):.0f}% | ≥25% más larga que todas: {cortas} ({100*cortas/max(n,1):.0f}%)")
print("\n## 'todas/ninguna de las anteriores'")
for p in P:
    if re.search(r'todas las anteriores|ninguna de las anteriores', str(p[4]).lower()):
        print(" ", niv.get(nivel_de[p[0]]), p[0], p[3][:70], '|', p[4])
print("\n## Alternativas con solo 2 opciones")
for p in P:
    ops = p[4] if isinstance(p[4], list) else json.loads(p[4] or '[]')
    if p[2] == 'alternativas' and len(ops) == 2: print(" ", niv.get(nivel_de[p[0]]), p[3][:80], ops)
