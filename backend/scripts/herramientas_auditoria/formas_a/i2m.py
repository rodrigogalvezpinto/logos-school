import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from forma_a import P, armar  # noqa: E402
C=Path(__file__).resolve().parents[4]/'contenido'/'02-medio/examenes'
Q=[]
def q(sec,tipo,en,ops,l,ex,oa): Q.append(P(sec,"**{n}.** *(%s)* "%tipo,en,ops,l,ex,oa))
def vf(sec,en,v,ex,oa): Q.append(P(sec,"**{n}.** *(Verdadero o falso)* ",en,[],"V" if v else "F",ex,oa,{"clave":"True (Verdadero)" if v else "False (Falso)"}))
S9="## OA N°9 — Comprender ideas generales e información explícita en textos variados\n\n"
S10="## OA N°10 — Comprender textos no literarios: propósito, relaciones de importancia, problema-solución y formación de palabras\n\n"
S13="## OA N°13 — Escribir sobre experiencias, temas interdisciplinarios, problemas globales y culturas\n\n"
S16="## OA N°16 — Usar estructuras gramaticales de presente perfecto continuo, pasado perfecto, estilo indirecto, condicionales y conectores avanzados al escribir\n\n"
q(S9,"Selección múltiple","Read: *\"Solar-powered water pumps are helping farmers in dry regions of Africa. With them, farmers can irrigate their crops without buying expensive diesel fuel.\"* What information is explicit in the text?",
 ["Solar pumps have completely ended droughts in all African countries.","*Solar pumps help farmers irrigate their crops without using diesel.","Farmers in Africa prefer diesel because it is cheaper than solar energy.","Solar pumps only work at night, when the temperature is lower."],"b","El texto dice explícitamente que, con las bombas solares, los agricultores riegan sus cultivos sin comprar diésel (*irrigate their crops without buying expensive diesel fuel*).","OA9")
q("","Alternativas — completar","Complete: *\"This report is ___ the effects of fast fashion. It explains ___ so many clothes end up in landfills.\"*",
 ["*about / why","about / who","of / what","for / where"],"d","*About* introduce el tema del informe y *why* introduce la explicación de las causas (por qué tanta ropa termina en vertederos).","OA9")
vf("","Read: *\"Many glaciers in Patagonia are shrinking quickly because of rising temperatures.\"* Statement: *According to the text, the glaciers in Patagonia are growing.*",False,
 "False (Falso) — el texto dice que los glaciares se están reduciendo (*shrinking*) por el aumento de las temperaturas, no que crecen.","OA9")
q("","Alternativas — comprensión","Read: *\"The Chilean poet Pablo Neruda won the Nobel Prize in Literature in 1971.\"* *When did Pablo Neruda win the Nobel Prize, and in which field?*",
 ["*He won it in 1971, in Literature.","He won it in 1945, in Peace.","He won it in 1971, in Chemistry.","He won it in 1917, in Medicine."],"a","La respuesta debe incluir los dos datos explícitos: el año (*1971*) y el área (*Literature*).","OA9")
q("","Alternativas — completar esquema","Read: *\"Marie Curie was a Polish-French scientist. She was born in 1867 and won two Nobel Prizes.\"* Nationality / Year of birth / Achievement:",
 ["*Polish-French / 1867 / two Nobel Prizes","British / 1867 / one Nobel Prize","Polish-French / 1934 / one Nobel Prize","French / 1876 / two Olympic medals"],"c","Completar el esquema exige extraer los datos explícitos: *Polish-French*, *1867* y *two Nobel Prizes*.","OA9")
q("","Selección múltiple — desafiante","You need to know quickly what a long article about social media is mainly about. What is the best strategy?",
 ["Read every word slowly and translate each one with a dictionary first.","Read only the last word of each paragraph and guess the topic from it.","Look only at the pictures and ignore the title and all the paragraphs.","*Skim it: read the title, the first and the last paragraphs to get the main idea."],"d","Para captar rápidamente la idea general se hace una lectura rápida (*skimming*): título, primer y último párrafo.","OA9")
q(S10,"Selección múltiple","Read: *\"Save energy! Turn off the lights when you leave a room and unplug your charger.\"* What is the main purpose of this text?",
 ["To explain how electricity is produced.","*To persuade readers to save energy at home.","To describe the history of electric lights.","To sell a new kind of phone charger."],"b","Los imperativos *Save energy!*, *Turn off* y *unplug* buscan persuadir al lector de ahorrar energía.","OA10")
q("","Alternativas — completar","Complete: *\"___ you water the plants every day, they will grow strong and healthy.\"*",
 ["*As long as","Unless","Although","Instead of"],"a","*As long as* (siempre que) expresa una condición: si se riegan cada día, las plantas crecerán fuertes.","OA10")
vf("","Read: *\"Many teenagers feel stressed before exams. Some schools now offer short breathing sessions to help them relax.\"* Statement: *The text presents a problem and a possible solution.*",True,
 "True (Verdadero) — el problema es el estrés antes de los exámenes; la solución propuesta son sesiones breves de respiración.","OA10")
q("","Alternativas — completar","Complete: *\"Flying without wings is ___.\"* (possible + prefix)",
 ["*impossible","unpossible","inpossible","dispossible"],"c","Ante adjetivos que comienzan con *p* se usa el prefijo *im-*: *possible* → *impossible*.","OA10")
q("","Alternativas — vocabulario","What is the antonym of *\"honest\"*?",
 ["*dishonest","unhonest","inhonest","imhonest"],"d","El antónimo de *honest* se forma con el prefijo *dis-*: *dishonest* (deshonesto).","OA10")
q("","Selección múltiple — desafiante","Read: *\"Either the teacher or the students will present the project on Friday.\"* What does the sentence mean?",
 ["Both the teacher and the students will present the project together.","*Only one of the two, the teacher or the students, will present it.","Neither the teacher nor the students will present the project.","The project will be presented every Friday by everyone."],"b","*Either… or* indica una alternativa: lo presentará solo uno de los dos, el profesor o los estudiantes.","OA10")
q(S13,"Alternativas — completar","Complete: *\"___ the one hand, technology helps us learn; on the other hand, it can distract us.\"*",
 ["*On","In","At","By"],"c","La expresión fija es *On the one hand… on the other hand*, que presenta dos aspectos de un tema.","OA13")
q("","Selección múltiple","¿Qué oración expresa una opinión justificada sobre la deforestación?",
 ["*I believe we must protect native forests, because they store water and are home to many species.","Native forests have many trees, and some of them are very tall and very old.","Forests are green. Trees are big. Animals live there and birds sing every morning.","I don't care about forests, and I never think about them when I go to the city."],"a","*I believe we must…* expresa una opinión y *because they store water and are home to many species* la justifica con razones.","OA13")
q("","Alternativas — completar","Complete: *\"Last weekend, we ___ a museum and I ___ a lot about Rapa Nui.\"* (visit / learn, simple past)",
 ["*visited / learned","visit / learn","visited / learnd","visits / learned"],"d","Los dos verbos son regulares en pasado simple: *visited* y *learned*.","OA13")
vf("","La oración *\"As a result, many species are now in danger.\"* introduce una consecuencia de lo dicho antes.",True,
 "True (Verdadero) — *As a result* (como resultado) introduce una consecuencia.","OA13")
q("","Alternativas — escribir siguiendo modelo","Which option completes the model *\"If I could change one thing in my school, I would ___, because ___.\"* coherently?",
 ["eat pizza every single day / the Moon is round and far away","*build a bigger library / students need quiet places to study","build a bigger library / yesterday was a sunny Sunday in my city","sleep during every class / teachers are very tall and wear glasses"],"b","Se propone un cambio realista (*build a bigger library*) y se justifica con una razón relacionada (*students need quiet places to study*).","OA13")
q("","Selección múltiple — desafiante","Estás escribiendo sobre un artículo que leíste acerca de la cueca. ¿Qué oración lo resume correctamente usando estilo indirecto?",
 ["The author explain that the cueca become the national dance in 1979.","The author explained me the cueca is national dance since 1979 years.","*The author explained that the cueca had become the national dance in 1979.","The author is explaining that cueca will become national dance in 1979."],"c","En estilo indirecto, *explained that* va seguido del pasado perfecto (*had become*) para hablar de algo anterior. Las otras opciones tienen errores verbales.","OA13")
q(S16,"Alternativas — completar","Complete: *\"There are ___ jobs in the factory than last year.\"*",
 ["*fewer","less","little","much"],"a","Con sustantivos contables en plural (*jobs*) se usa *fewer*; *less* se usa con incontables.","OA16")
q("","Selección múltiple","Completa la oración: \"Sofía is wet because she ______ in the rain for an hour.\"",
 ["*has been walking","walks","is walk","have been walked"],"d","El presente perfecto continuo (*has been walking*) expresa una acción que empezó en el pasado, continuó y explica el estado actual.","OA16")
q("","Alternativas — completar","Complete with the second conditional: *\"I don't have a bike. If I ___ a bike, I ___ to school every day.\"*",
 ["*had / would ride","have / will ride","had / will ride","would have / rode"],"c","El segundo condicional usa *if* + pasado simple (*had*) y *would* + verbo base (*would ride*) para una situación hipotética.","OA16")
vf("","La oración *\"When we arrived at the station, the train had already left.\"* indica que el tren salió después de que llegamos.",False,
 "False (Falso) — el pasado perfecto (*had already left*) indica que el tren salió antes de que llegáramos.","OA16")
q("","Alternativas — duración","*\"How long have you been learning English?\"* Which answer is correct?",
 ["Three years ago.","*For three years.","Since three years.","In three years."],"b","Con el presente perfecto continuo, *How long* se responde con *for* + período: *For three years*. *Since* se usa con un punto de inicio.","OA16")
q("","Alternativas — estilo indirecto","My sister said: *\"I am studying for the test.\"* → *My sister said she ___ for the test.*",
 ["*was studying","is studying","has studied","studies"],"a","En estilo indirecto, el presente continuo (*am studying*) pasa a pasado continuo: *was studying*.","OA16")
q("","Selección múltiple — desafiante","Completa la oración: \"We painted the school mural ______; nobody helped us.\"",
 ["*ourselves","us","ours","ourself"],"d","El pronombre reflexivo de *we* es *ourselves*: indica que lo hicimos nosotros mismos, sin ayuda.","OA16")
armar(C/'ingles-examen-forma-b.md', C/'ingles-examen-forma-a.md', Q,
  fila=lambda i,p,cl: (f"| {i} | {p.explicacion} | {p.oa} |" if not p.opciones else f"| {i} | **{cl}.** {p.explicacion} | {p.oa} |"),
  reemplazos={"— Forma B":"— Forma A","FORMA B":"FORMA A","Esta Forma B usa":"Esta Forma A usa","ultima_actualizacion: 2026-11-01":"ultima_actualizacion: 2026-11-17"},
  inicio_preguntas="## OA N°9")
if __name__=="__main__":
    from collections import Counter; print(Counter(p.letra for p in Q), len(Q))
