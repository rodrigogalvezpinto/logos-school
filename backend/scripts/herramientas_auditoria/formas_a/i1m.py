import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from forma_a import P, armar  # noqa: E402
C=Path(__file__).resolve().parents[4]/'contenido'/'01-medio/examenes'
Q=[]
def q(sec,tipo,en,ops,l,ex,oa): Q.append(P(sec,"**{n}.** *(%s)* "%tipo,en,ops,l,ex,oa))
def vf(sec,en,v,ex,oa): Q.append(P(sec,"**{n}.** *(Verdadero o falso)* ",en,[],"V" if v else "F",ex,oa,{"clave":"True (Verdadero)" if v else "False (Falso)"}))
S9="## OA N°9 — Comprender ideas generales e información explícita en textos variados\n\n"
S10="## OA N°10 — Comprender textos no literarios: propósito, contraste, problema-solución y formación de palabras\n\n"
S13="## OA N°13 — Escribir sobre experiencias, temas interdisciplinarios, problemas globales y culturas\n\n"
S16="## OA N°16 — Usar estructuras gramaticales de presente perfecto, hábitos pasados, cualidades y oraciones subordinadas al escribir\n\n"
q(S9,"Selección múltiple","Read: *\"Violeta Parra was a Chilean singer, composer and artist. She travelled around Chile collecting traditional songs, and in 1964 her tapestries were exhibited at the Louvre Museum in Paris.\"* What information is explicit in the text?",
 ["*She collected traditional songs while travelling around Chile.","She won the Nobel Prize in Literature for her famous songs.","She was born in Paris and moved to Chile in the year 1964.","She painted only portraits and never wrote any songs at all."],"b","El texto dice explícitamente que viajó por Chile recopilando canciones tradicionales (*travelled around Chile collecting traditional songs*). No menciona un Nobel ni que naciera en París.","OA9")
q("","Alternativas — completar","Complete: *\"The article ___ two cities. It describes ___ long it takes people to get to work in each one.\"*",
 ["*compares / how","compare / what","comparing / how","compares / who"],"d","*Compares* lleva -s porque el sujeto es *the article* (tercera persona) y *how long* pregunta por la duración del viaje.","OA9")
vf("","Read: *\"Hummingbirds can fly backwards, and their wings can beat up to 80 times per second. Most species live in the Americas.\"* Statement: *According to the text, most hummingbirds live in Africa.*",False,
 "False (Falso) — el texto dice que la mayoría de las especies vive en América (*Most species live in the Americas*), no en África.","OA9")
q("","Alternativas — comprensión","Read: *\"ALMA is located 5,000 metres above sea level in northern Chile. It has 66 antennas that work together as one giant telescope.\"* *How many antennas does ALMA have, and where is it?*",
 ["*It has 66 antennas, and it is in northern Chile.","It has 5,000 antennas, and it is in southern Chile.","It has 66 antennas, and it is in the centre of Santiago.","It has one antenna that is 66 metres high, in the sea."],"a","La respuesta debe incluir los dos datos explícitos: 66 antenas (*66 antennas*) y su ubicación en el norte de Chile (*northern Chile*).","OA9")
q("","Alternativas — completar esquema","Read: *\"Neil Armstrong was an American astronaut. He was born in 1930 and walked on the Moon in 1969.\"* Nationality / Year of birth / Achievement:",
 ["*American / 1930 / walked on the Moon","Russian / 1969 / walked on the Moon","American / 1969 / was born on the Moon","British / 1930 / built the first rocket"],"c","Completar un esquema exige extraer los datos explícitos: *American* (nacionalidad), *1930* (año de nacimiento) y *walked on the Moon* (logro).","OA9")
q("","Selección múltiple — desafiante","You read: *\"The lake was so serene that you could hear birds singing from far away.\"* You don't know the word *serene*. What is the best strategy to understand it?",
 ["Stop reading the text, because one unknown word makes it impossible to understand anything.","Translate every single word of the sentence with a dictionary before reading the rest.","Ignore the sentence completely, because unknown words are never important in a text.","*Use the context: if you could hear birds far away, the lake was probably calm and quiet."],"d","El contexto ayuda a inferir el significado: si se oían pájaros a lo lejos, el lago estaba tranquilo y silencioso (*serene* = sereno, tranquilo).","OA9")
q(S10,"Selección múltiple","Read: *\"Join our free coding workshop for teenagers! Every Saturday at the public library. Sign up at the front desk.\"* What is the main purpose of this text?",
 ["*To invite teenagers to join a free workshop.","To explain the history of the public library.","To criticise teenagers who use computers.","To describe how a computer works inside."],"b","*Join our free coding workshop* y *Sign up at the front desk* invitan a los adolescentes a inscribirse en el taller: ese es el propósito del texto.","OA10")
q("","Alternativas — completar","Complete: *\"It was raining heavily. ___, the match continued until the end.\"*",
 ["*Nevertheless","Because","For example","So that"],"a","*Nevertheless* (sin embargo) marca el contraste: aunque llovía mucho, el partido continuó.","OA10")
vf("","Read: *\"Many students arrive late because the bus comes only once an hour. The school asked the bus company to add more buses in the morning.\"* Statement: *The text presents a problem and a possible solution.*",True,
 "True (Verdadero) — el problema es que los estudiantes llegan tarde porque el bus pasa una vez por hora; la solución propuesta es agregar más buses en la mañana.","OA10")
q("","Alternativas — completar","Complete with the antonym of *clear*: *\"The instructions were ___: nobody understood what to do.\"*",
 ["*unclear","disclear","inclear","imclear"],"c","El prefijo *un-* forma el antónimo de *clear*: *unclear* (poco claro). Las otras formas no existen en inglés.","OA10")
q("","Alternativas — vocabulario","What is the occupation noun formed from *\"journal\"*?",
 ["*journalist","journaler","journalor","journalian"],"d","El sufijo *-ist* forma la ocupación: *journal* → *journalist* (periodista).","OA10")
q("","Selección múltiple — desafiante","Read: *\"The new phone is not only cheaper but also faster than the old one.\"* What does the sentence mean?",
 ["The new phone is cheaper, but it is slower than the old one.","*The new phone is both cheaper and faster than the old one.","The new phone is faster, but it costs more than the old one.","The old phone is cheaper and faster than the new phone."],"b","*Not only… but also* suma dos cualidades: *the new phone is both cheaper and faster than the old one* (más barato y también más rápido).","OA10")
q(S13,"Alternativas — completar","Complete: *\"___ the other hand, online classes can make some students feel isolated.\"*",
 ["*On","In","At","By"],"c","La expresión fija es *On the other hand* (por otra parte), que introduce un punto de vista contrario.","OA13")
q("","Selección múltiple","¿Qué oración expresa una opinión justificada sobre la basura plástica?",
 ["*I think we should use fewer plastic bags, because they pollute the oceans for hundreds of years.","Plastic bags are made in factories, and many shops give them to customers every single day.","I don't know anything about plastic, and I don't think about it when I go to the supermarket.","Plastic is a material. Bags are useful. Oceans are big and blue, and many fish live there."],"a","*I think we should…* expresa una opinión y *because they pollute the oceans* la justifica con una razón. Las otras solo dan datos o no opinan.","OA13")
q("","Alternativas — completar","Complete: *\"Last summer, my cousins ___ to Chiloé and ___ curanto for the first time.\"* (travel / eat, simple past)",
 ["*travelled / ate","travel / eat","travelled / eated","travels / ate"],"d","*Travel* es regular (*travelled*) y *eat* es irregular (*ate*). *Eated* no existe.","OA13")
vf("","La oración *\"However, many people still throw batteries in the normal trash.\"* introduce un ejemplo que apoya la idea anterior.",False,
 "False (Falso) — *However* introduce un contraste, no un ejemplo; para dar un ejemplo se usa *for example* o *for instance*.","OA13")
q("","Alternativas — escribir siguiendo modelo","Which option completes the model *\"One problem in my city is ___. To solve it, ___.\"* coherently?",
 ["my birthday party / I like pizza with cheese","*air pollution / we could use public transport more often","air pollution / the Moon is very far from the Earth","public transport / yesterday I was very happy at home"],"b","Se debe nombrar un problema real (*air pollution*) y proponer una solución relacionada (*use public transport more often*). Las otras opciones no son coherentes.","OA13")
q("","Selección múltiple — desafiante","Estás escribiendo sobre un texto que leíste acerca de una celebración chilena. ¿Qué oración lo resume correctamente usando una oración subordinada?",
 ["The text was about Fiestas Patrias. Chileans. Dance cueca. September.","The text were about Fiestas Patrias, who Chileans dancing cueca in September.","*The text was about Fiestas Patrias, a celebration in which Chileans dance cueca in September.","The text is about Fiestas Patrias because September, cueca and empanadas."],"c","*A celebration in which Chileans dance cueca* es una subordinada bien construida que explica qué es la celebración; las otras opciones tienen errores o son frases sueltas.","OA13")
q(S16,"Alternativas — completar","Complete: *\"More than ___ people visited the book fair last weekend.\"*",
 ["*two thousand","two thousands","two thousand of","twos thousand"],"a","*Thousand* no lleva -s cuando va precedido de un número exacto: *two thousand people*.","OA16")
q("","Selección múltiple","Completa la oración: \"She ______ English since she was ten years old.\"",
 ["*has studied","studies","is studied","have study"],"d","Con *since* se usa el presente perfecto: *has studied* (sujeto *she*), para una acción que empezó en el pasado y sigue.","OA16")
q("","Alternativas — completar","Complete with the past simple passive: *\"These houses ___ after the earthquake in 2010.\"* (rebuild)",
 ["*were rebuilt","was rebuilt","rebuilt were","are rebuild"],"c","Pasiva en pasado con sujeto plural: *were* + participio (*rebuilt*).","OA16")
vf("","La oración *\"When I was a child, I used to walk to school every day.\"* describe un hábito del pasado.",True,
 "True (Verdadero) — *used to* + verbo describe una acción habitual en el pasado que ya no ocurre.","OA16")
q("","Alternativas — duración","*\"How long have you lived in Temuco?\"* Which answer is correct?",
 ["In 2018 ago.","*Since 2018.","Two years before.","Since three years."],"b","*Since* + punto de inicio (*2018*) responde a *how long*. *Since three years* es incorrecto: con un período se usa *for*.","OA16")
q("","Alternativas — completar","Complete: *\"The book ___ I borrowed from the library is about volcanoes. The girl ___ brother is my classmate lent it to me.\"*",
 ["*that / whose","who / where","where / which","whose / that"],"a","*That* se refiere a una cosa (*the book*) y *whose* indica posesión (el hermano de la niña).","OA16")
q("","Selección múltiple — desafiante","¿Qué oración describe correctamente a una persona usando el presente perfecto y una cualidad?",
 ["My grandfather has be a fisherman for forty years and he very patient.","My grandfather was been a fisherman for forty years and is patient.","My grandfather have been a fisherman since forty years and is patient.","*My grandfather has been a fisherman for forty years and he is very patient."],"d","*Has been* + *for forty years* usa bien el presente perfecto, y *he is very patient* describe una cualidad. Las otras opciones tienen errores verbales.","OA16")
armar(C/'ingles-examen-forma-b.md', C/'ingles-examen-forma-a.md', Q,
  fila=lambda i,p,cl: (f"| {i} | {p.explicacion} | {p.oa} |" if not p.opciones else f"| {i} | **{cl}.** {p.explicacion} | {p.oa} |"),
  reemplazos={"— Forma B":"— Forma A","FORMA B":"FORMA A","Esta es la **Forma B** de la prueba":"Esta es la **Forma A** de la prueba","Esta Forma B utiliza textos":"Esta Forma A utiliza textos","ultima_actualizacion: 2026-11-01":"ultima_actualizacion: 2026-11-17"},
  inicio_preguntas="## OA N°9")
if __name__=="__main__":
    from collections import Counter; print(Counter(p.letra for p in Q), len(Q))
