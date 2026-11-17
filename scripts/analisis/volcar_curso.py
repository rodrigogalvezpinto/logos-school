"""Vuelca, para un curso, cada OA del temario con sus indicadores y el texto de la guía (para revisión humana)."""
import json, os, re, sys
sys.path.insert(0, os.path.dirname(__file__))
import cobertura_temario as ct
import psycopg2

curso = sys.argv[1]
d = json.load(open(sys.argv[2]))
con = psycopg2.connect(re.sub(r"\+\w+", "", os.environ["E2E_DATABASE_URL"], count=1))
cur = con.cursor()
for x in d:
    if x["curso"] != curso: continue
    cur.execute("""select o.contenido_guia from objetivo_aprendizaje o join asignatura a on a.id=o.asignatura_id
                   join nivel n on n.id=a.nivel_id where n.nombre=%s and o.codigo_oficial=%s""", (curso, ct.clave_oa(x["codigo"])))
    filas = cur.fetchall()
    guia = next((g for (g,) in filas if g), "")
    if len(filas) > 1:  # varias asignaturas con el mismo código: elegir por asignatura
        cur.execute("""select o.contenido_guia, a.nombre from objetivo_aprendizaje o join asignatura a on a.id=o.asignatura_id
                       join nivel n on n.id=a.nivel_id where n.nombre=%s and o.codigo_oficial=%s""", (curso, ct.clave_oa(x["codigo"])))
        for g, a in cur.fetchall():
            if ct.clave_asig(a)[:5] == ct.clave_asig(x["asignatura"])[:5]: guia = g
    print(f"\n######## {x['asignatura']} — {x['codigo']} | guía {x['palabras_guia']} palabras | preguntas guía/prueba/simulacro {x['guia']}/{x['prueba']}/{x['simulacro']}")
    print("TEMARIO:", x["texto"])
    for i, ind in enumerate(x["indicadores"], 1):
        print(f"  I{i} [{ind['en_guia']}/{ind['en_preguntas']}] {ind['indicador']}")
    print("GUÍA:", re.sub(r"\n\s*\n", "\n", guia).strip())
