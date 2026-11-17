"""Análisis de cobertura (2026-11-17): temario oficial (Temarios/analisis) vs material (base E2E).

Para cada curso, asignatura, OA e indicador de evaluación del temario:
- ¿existe el OA en el material?, largo de la explicación de la guía, preguntas por fuente
  (autoevaluación de guía, pruebas de unidad, simulacros);
- evidencia por indicador: proporción de palabras clave del indicador que aparecen en la guía o en las
  preguntas de ese OA (heurística: raíz de 5 letras). Es un filtro para revisar a mano, no un veredicto.
Uso: E2E_DATABASE_URL=... python3 scripts/analisis/cobertura_temario.py > salida.json
"""
import json, os, re, sys, unicodedata
from pathlib import Path
import psycopg2 as psycopg

RAIZ = Path(__file__).resolve().parents[2]
CURSOS = {"01-primero-basico":"1° básico","02-segundo-basico":"2° básico","03-tercero-basico":"3° básico","04-cuarto-basico":"4° básico",
 "05-quinto-basico":"5° básico","06-sexto-basico":"6° básico","07-septimo-basico":"7° básico","08-octavo-basico":"8° básico",
 "09-primero-medio":"1° medio","10-segundo-medio":"2° medio","11-tercero-medio":"3° medio","12-cuarto-medio":"4° medio"}
VACIAS = set("""identifican reconocen explican describen comparan utilizan aplican resuelven analizan elaboran
establecen evaluan evalúan demuestran representan interpretan relacionan distinguen formulan argumentan proponen
seleccionan ejemplifican expresan extraen ordenan calculan determinan usan escriben leen responden clasifican
caracterizan asocian infieren localizan ubican fundamentan opinan entre sobre según desde hasta durante mediante
cuando donde forma través tipos otros otras algunos algunas diferentes diversos diversas propios propias dados dadas
partir respecto acuerdo cada misma mismo cuales cuáles como para pero sino también ellos ellas texto textos""".split())

def norm(s):
    s = unicodedata.normalize("NFD", s.lower())
    return "".join(c for c in s if unicodedata.category(c) != "Mn")

def clave_asig(nombre):
    n = norm(nombre)
    return "ingles" if "ingles" in n else n[:12]


def clave_oa(cod):
    return re.sub(r"OA\s*0*(\d+)", r"OA \1", cod.strip())


def raices(s):
    return {w[:5] for w in re.findall(r"[a-zñ]+", norm(s)) if len(w) >= 5 and w not in {norm(v) for v in VACIAS}}

def temario(ruta):
    asig, oas, actual = None, [], None
    for linea in ruta.read_text(encoding="utf-8").splitlines():
        m = re.match(r"^## (.+)", linea)
        if m and not m.group(1).startswith("Formato"):
            asig = m.group(1).strip(); actual = None; continue
        m = re.match(r"^\*\*OA(?: N°\s*(\d+))?[^*]*\*\*:?\s*(.*)", linea)
        if m and asig:
            actual = {"asignatura": asig, "codigo": f"OA {m.group(1)}" if m.group(1) else "OA", "texto": m.group(2), "indicadores": []}
            oas.append(actual); continue
        if actual and linea.startswith("- "):
            actual["indicadores"].append(linea[2:].strip())
        elif linea.startswith("#"):
            actual = None if linea.startswith("## ") else actual
    return oas

def main():
    url = re.sub(r"\+\w+", "", os.environ["E2E_DATABASE_URL"], count=1)
    con = psycopg.connect(url)
    cur = con.cursor()
    cur.execute("""select n.nombre, a.nombre, o.id, o.codigo_oficial, o.descripcion, o.contenido_guia
                   from objetivo_aprendizaje o join asignatura a on a.id=o.asignatura_id join nivel n on n.id=a.nivel_id""")
    oa_db = {}
    for nivel, asig, oid, cod, desc, guia in cur.fetchall():
        oa_db.setdefault((nivel, clave_asig(asig), clave_oa(cod)), []).append((oid, desc, guia or ""))
    cur.execute("select id, tipo, pregunta_ids from conjunto_evaluacion")
    fuente = {}
    for cid, tipo, ids in cur.fetchall():
        for pid in ids or []:
            fuente[pid] = "simulacro" if tipo == "examen_simulacro" else "prueba"
    cur.execute("select id, oa_id, enunciado, opciones, retroalimentacion from pregunta")
    preg = {}
    for pid, oid, en, ops, ret in cur.fetchall():
        preg.setdefault(oid, []).append((fuente.get(pid, "guia"), f"{en} {json.dumps(ops, ensure_ascii=False) if ops else ''} {ret}"))
    salida = []
    for clave, nivel in CURSOS.items():
        for oa in temario(RAIZ / "Temarios/analisis" / f"{clave}.md"):
            cands = oa_db.get((nivel, clave_asig(oa["asignatura"]), clave_oa(oa["codigo"])), [])
            if not cands:  # nombre de asignatura distinto: buscar por código dentro del nivel
                cands = [v for (n, a, c), vs in oa_db.items() if n == nivel and c == clave_oa(oa["codigo"]) and a[:5] == clave_asig(oa["asignatura"])[:5] for v in vs]
            reg = {"curso": nivel, "asignatura": oa["asignatura"], "codigo": oa["codigo"], "texto": oa["texto"][:200], "en_material": bool(cands)}
            if cands:
                oid, desc, guia = cands[0]
                ps = preg.get(oid, [])
                reg.update(palabras_guia=len(guia.split()), guia=sum(1 for f, _ in ps if f == "guia"),
                           prueba=sum(1 for f, _ in ps if f == "prueba"), simulacro=sum(1 for f, _ in ps if f == "simulacro"))
                r_guia = raices(guia); r_preg = raices(" ".join(t for _, t in ps))
                inds = []
                for ind in oa["indicadores"]:
                    r = raices(ind)
                    if not r: continue
                    inds.append({"indicador": ind, "en_guia": round(len(r & r_guia) / len(r), 2), "en_preguntas": round(len(r & r_preg) / len(r), 2)})
                reg["indicadores"] = inds
            salida.append(reg)
    json.dump(salida, sys.stdout, ensure_ascii=False, indent=1)

if __name__ == "__main__":
    main()
