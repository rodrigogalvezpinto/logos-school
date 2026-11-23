"""Quita la palabra «OA» de los textos que lee el alumno (2026-11-23). El alumno no sabe qué es un Objetivo de
Aprendizaje; los títulos «OA N°…» y las columnas OA de las pautas (metadatos) no se tocan. Idempotente."""
import glob, re, sys
R = [
    ("según lo estudiado en este OA", "según lo estudiado"),
    ("respetando la finalidad del OA", "respetando la finalidad del texto"),
    ("cumpliendo con lo que pide el OA para escribir", "como corresponde al escribir"),
    ("cumpliendo con lo que pide el OA sobre escribir", "como corresponde al escribir"),
    (", cumpliendo lo que pide el OA.", "."),
    (", tal como pide este OA", ""),
    ("es parte de lo que exige este OA", "es parte de lo que se trabaja en esta unidad"),
    ("es parte de las habilidades que exige este OA", "es parte de las habilidades de esta unidad"),
    ("es parte de lo que este OA espera que puedas hacer", "es parte de lo que se espera que puedas hacer"),
    ("es parte del OA", "es parte de lo que se trabaja en esta unidad"),
    ("que trabaja este OA", "que se trabaja en esta unidad"),
    ("y este OA exige dominar ambas", "y conviene dominar ambas"),
    ("distintas que exige este OA", "distintas que conviene dominar"),
    ("Este OA exige explícitamente", "Aquí se exige explícitamente"),
    ("El OA pide explícitamente", "Se pide explícitamente"),
    ("El OA pide", "Se pide"),
    ("Este OA pide", "Aquí se pide"),
    ("El OA exige", "Se exige"),
    ("El OA busca que", "Se busca que"),
    ("El OA busca", "Se busca"),
    ("Este OA plantea", "Lo estudiado plantea"),
    ("pero este OA pide reconocer", "pero hay que reconocer"),
    ("por eso este OA habla del", "por eso se habla del"),
    ("según este OA", "según lo estudiado"),
    ("según el OA", "según lo estudiado"),
    ("revisadas en este OA", "revisadas en esta unidad"),
    ("reconocida en este OA", "reconocida en esta unidad"),
    ("mencionada en este OA", "mencionada en esta unidad"),
    ("estudiado en este OA", "estudiado en esta unidad"),
    ("ejemplo relevante para este OA", "ejemplo relevante para este tema"),
    ("¿Qué concepto de este OA", "¿Qué concepto estudiado"),
    ("conceptos éticos del OA N°2", "conceptos éticos estudiados"),
    ("conceptos éticos del OA 2", "conceptos éticos estudiados"),
    ("Conectar este OA con el OA 12 (distribución del agua)", "Conectar este tema con la distribución del agua"),
    ("Este es un buen puente hacia el OA 2, donde verás", "Este es un buen puente hacia el tema siguiente, donde verás"),
    ("lo aprendido en el OA 1 sobre fotosíntesis", "lo aprendido sobre fotosíntesis"),
    ("se profundiza en el OA 2,", "se profundiza más adelante,"),
    ("explícitos del OA", "explícitos de esta unidad"),
    (", tal como indica el OA.", "."),
    ("vimos en el OA anterior", "vimos antes"),
    ("trabajadas en este OA", "trabajadas en esta unidad"),
    ("que este OA pide identificar", "que hay que saber identificar"),
    ("Uno de los indicadores centrales de este OA pide precisamente", "Lo que se pide aquí es precisamente"),
    ("uno de los riesgos centrales de este OA", "uno de los riesgos centrales de estas tecnologías"),
    ("Se acepta cualquier OA si", "Se acepta cualquier tema si"),
    ("en los otros OA del año", "en los otros temas del año"),
    ("según los tres OA de este año", "según los tres grandes temas de este año"),
    ("cuál de los tres OA del año", "cuál de los tres grandes temas del año"),
]
total = 0
for f in glob.glob(sys.argv[1] + "/**/*.md", recursive=True):
    s = o = open(f).read()
    for a, b in R:
        # Tolera que la frase esté partida entre dos líneas del Markdown (texto ajustado a 80 columnas).
        patron = re.compile(r"\s+".join(re.escape(w) for w in a.split(" ")))
        s, n = patron.subn(b.replace("\\", "\\\\"), s)
        total += n
    if s != o: open(f, "w").write(s); print("  ", f.split("contenido/")[1])
print("reemplazos:", total)
