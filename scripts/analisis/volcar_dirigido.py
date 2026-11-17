"""Igual que volcar_curso.py, pero muestra el texto de la guía solo en los OA con algún indicador de baja coincidencia."""
import json, os, re, sys
sys.path.insert(0, os.path.dirname(__file__))
import cobertura_temario as ct
import psycopg2
curso, ruta, umbral = sys.argv[1], sys.argv[2], float(sys.argv[3]) if len(sys.argv) > 3 else 0.6
d = json.load(open(ruta))
con = psycopg2.connect(re.sub(r"\+\w+", "", os.environ["E2E_DATABASE_URL"], count=1)); cur = con.cursor()
for x in d:
    if x["curso"] != curso: continue
    bajos = [i for i in x["indicadores"] if i["en_guia"] < umbral]
    print(f"\n######## {x['asignatura']} — {x['codigo']} | guía {x['palabras_guia']} pal. | g/p/s {x['guia']}/{x['prueba']}/{x['simulacro']}")
    for i, ind in enumerate(x["indicadores"], 1):
        print(f"  I{i} [{ind['en_guia']}/{ind['en_preguntas']}] {ind['indicador'][:230]}")
    if bajos:
        cur.execute("""select o.contenido_guia, a.nombre from objetivo_aprendizaje o join asignatura a on a.id=o.asignatura_id
                       join nivel n on n.id=a.nivel_id where n.nombre=%s and o.codigo_oficial=%s""", (curso, ct.clave_oa(x["codigo"])))
        for g, a in cur.fetchall():
            if ct.clave_asig(a)[:5] == ct.clave_asig(x["asignatura"])[:5]:
                print("GUÍA:", re.sub(r"\n\s*\n", "\n", re.sub(r"::emoji::[^\n]*", "", g or "")).strip())
