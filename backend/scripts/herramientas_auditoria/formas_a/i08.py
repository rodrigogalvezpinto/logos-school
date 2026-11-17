import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from forma_a import P, armar  # noqa: E402
C=Path(__file__).resolve().parents[4]/'contenido'/'08-basico/examenes'
SM="**{n}.** *(Selección múltiple)* "; CO="**{n}.** *(Alternativas — completar)* "
Q=[]
def q(sec,cab,en,ops,l,ex,oa):
    if len(l)>1: en=en+" Marca **todas** las correctas."
    Q.append(P(sec,cab,en,ops,l,ex,oa))
def vf(sec,en,v,ex,oa): Q.append(P(sec,"**{n}.** *(Verdadero o falso)* ",en,[],"V" if v else "F",ex,oa,{"clave":"True (Verdadero)" if v else "False (Falso)"}))
q("## OA N°9 — Comprender, resumir y cuestionar un texto\n\n",SM,'Read: *"Many schools in Chile now have recycling points. Students separate paper, plastic and cans, and some schools sell the material to buy new books for the library."* What is the text mainly about?',
 ["*School recycling points and how they help schools","How to make paper from old plastic bottles","A library that sells books to students","The history of cans and plastic bottles"],"b","El texto presenta los *recycling points* de los colegios (*schools*) y cómo el material vendido sirve para comprar libros: esa es la idea principal.","OA9")
q("",CO,'Read: *"Diego\'s class started a podcast about Chilean music. Every week, a student interviews a local musician."* Complete with a synonym of *started* and the correct verb form: *"Diego\'s class ___ a podcast. Every week, a student ___ a musician."*',
 ["*began / interviews","begins / interviewed","finished / interviews","began / interview"],"c","*Began* es sinónimo de *started* y va en pasado, porque el podcast ya se creó; *interviews* lleva -s porque el sujeto es *a student* y describe algo habitual.","OA9")
vf("",'Read: *"Humboldt penguins live on the coasts of Chile and Peru. They eat small fish and nest in caves or holes. Their population is decreasing because of fishing nets and pollution."* Write True or False: *"Humboldt penguins live on the Chilean and Peruvian coast, eat fish and are in danger" is a good summary of the text.*',True,
 "Verdadero: la oración recoge las ideas principales (dónde viven, qué comen y que su población disminuye) con pocas palabras.","OA9")
q("","**{n}.** *(Alternativas — conectar con el propio contexto)* ",'Read: *"In Japan, people celebrate Hanami in spring: they have picnics under the cherry blossoms with family and friends."* *How do people celebrate in your town?* Which answer connects the text with your own context?',
 ["*In my town, we celebrate Fiestas Patrias with empanadas and cueca.","In Japan, people have picnics under the cherry blossoms.","Hanami is a celebration that happens in spring in Japan.","In my town celebrate we Fiestas Patrias with empanadas."],"a","La respuesta conecta lo leído con una celebración propia y está bien escrita. Las otras repiten el texto o tienen el orden de palabras incorrecto.","OA9")
q("","**{n}.** *(Selección múltiple — desafiante)* ",'Read: *"Some libraries now lend tablets to students, so they can read e-books and do homework at home."* Which question would best expand the information in the text?',
 ["*How could lending tablets change the way students study?","What color are the tablets that the libraries lend?","Do libraries lend tablets to students?","Is a tablet a kind of book?"],"d","Preguntar cómo el préstamo de *tablets* cambiaría la forma de estudiar (*study*) amplía la información y lleva a pensar en consecuencias. Las otras preguntan detalles sin importancia o algo que el texto ya responde.","OA9")
q("","**{n}.** *(Alternativas — completar tabla)* ",'Read: *"Hi, I\'m Kwame. I\'m Ghanaian and I live in Accra. I\'m 15, and I practice the drums for an hour every day."* Complete the table: *Nationality: ___ / City: ___ / Practice time: ___*',
 ["*Ghanaian / Accra / an hour","Accra / Ghanaian / 15 years","Ghana / Accra / every day","Ghanaian / drums / an hour"],"b","Nacionalidad: *Ghanaian*; ciudad: *Accra*; tiempo de práctica: *an hour* (una hora). Las otras confunden los datos de cada casilla.","OA9")
q("## OA N°10 — Comprender textos no literarios: propósito, condición y formación de palabras\n\n",SM,'Read the sign at a zoo: *"Warning! Do not feed the animals. Human food can make them sick."* What is the purpose of this text?',
 ["*To warn visitors about a rule","To explain how to cook for animals","To sell food to the visitors","To describe a trip to the zoo"],"a","*Warning* y el imperativo *do not feed* muestran que el letrero advierte una regla (*rule*) a los visitantes (*visitors*) y explica por qué.","OA10")
q("",CO,'Complete with the correct connector: *"___ it was raining, we played football in the park."*',
 ["*Although","Because","So","Until"],"c","*Although* (aunque) une dos ideas que se oponen: llovía y aun así jugaron. *Because* daría una causa.","OA10")
vf("",'Read: *"Unless you water the plants, they will die."* Write True or False: *This sentence means the same as "If you don\'t water the plants, they will die."*',True,
 "Verdadero: *unless* significa «a menos que» y equivale a *if... not*: si no riegas las plantas, se morirán.","OA10")
q("",CO,'Complete: *"This exam was ___ than the last one."* (difficult, comparative)',
 ["*more difficult","difficulter","most difficult","difficult"],"d","Los adjetivos largos forman el comparativo con *more*: *more difficult than*. *Most difficult* es el superlativo.","OA10")
q("","**{n}.** *(Selección múltiple — desafiante)* ",'Read: *"I\'m sure the bus will arrive in five minutes."* What does *I\'m sure* express?',
 ["*Certainty","Possibility","Obligation","Permission"],"b","*I\'m sure* (estoy seguro) expresa certeza. *Maybe* o *might* expresarían posibilidad.","OA10")
q("",CO,'Complete with the noun formed from the verb *discover*: *"The ___ of penicillin saved millions of lives."*',
 ["*discovery","discoverion","discovering","discovered"],"a","El sustantivo de *discover* es *discovery* (descubrimiento), formado con el sufijo *-y*.","OA10")
q("## OA N°13 — Escribir sobre experiencias, culturas y preferencias\n\n",CO,'Complete: *"I prefer reading ___ watching TV, because books make me imagine."*',
 ["*to","than","that","of"],"c","La estructura es *prefer A to B*: *I prefer reading to watching TV*. *Than* se usa con *rather* o con comparativos.","OA13")
q("",SM,'You are asked: *Which sport do you like more, and why?* Which answer gives a preference **and** a reason?',
 ["*I prefer basketball to football because I like teamwork.","Basketball is a sport that people play with a big ball.","I prefer basketball. Football. Tennis. Swimming. Running.","I prefers basketball because it is a sport with a ball."],"d","Expresa una preferencia (*I prefer... to...*) y la justifica con razones (*because...*). Las otras no expresan preferencia, no tienen razón o tienen errores (*I prefers*).","OA13")
q("",CO,'Complete about a trip: *"Last winter, we ___ to Pucón and ___ in the hot springs."* (go / swim, simple past)',
 ["*went / swam","goed / swimmed","go / swim","went / swimmed"],"b","*Go* y *swim* son irregulares en pasado: *went* y *swam*.","OA13")
vf("",'La oración *"Chilean empanadas are the best food in the world"* es un hecho comprobable. Write True or False.',False,
 "False (Falso): *the best food in the world* expresa una opinión, no un hecho que se pueda comprobar.","OA13")
q("","**{n}.** *(Alternativas — vocabulario)* ",'What does *"I\'m looking forward to the holidays"* mean?',
 ["*Tengo muchas ganas de que lleguen las vacaciones","Estoy mirando las fotos de las vacaciones pasadas","Me olvidé por completo de las vacaciones de invierno","Las vacaciones ya terminaron y vuelvo a clases"],"a","*Look forward to* significa esperar algo con entusiasmo: tengo muchas ganas de que lleguen las vacaciones.","OA13")
q("","**{n}.** *(Alternativas — escribir siguiendo modelo)* ",'Model: *"Festival: Holi. Country: India. Why I want to go: I want to see the colors."* Which option follows the model correctly?',
 ["*Festival: La Tirana. Country: Chile. Why I want to go: I want to see the dances.","Festival: Chile. Country: La Tirana. Why I want to go: dances.","Festival: La Tirana. Country: Chile. Why I want to go: I wants to see the dances.","La Tirana Chile dances I want go see festival country."],"c","Cada dato va en su lugar (festival, país, razón) y la razón es una oración correcta. Las otras confunden los datos, tienen errores (*I wants*) o no siguen el modelo.","OA13")
q("## OA N°16 — Usar estructuras gramaticales de futuro, comparación y preferencia al escribir\n\n",CO,'Complete: *"May is the ___ month of the year."*',
 ["*fifth","five","fourth","sixth"],"d","Mayo es el quinto mes: se usa el ordinal *fifth*. *Five* es el número cardinal.","OA16")
q("","**{n}.** *(Alternativas — comprensión)* ",'Read the poster: *"Science Fair. Friday 14th November, 10 am – 1 pm. School gym."* *Where is the Science Fair?*',
 ["*It is in the school gym.","It is on Friday 14th November.","It starts at 10 am.","It is in the science lab."],"b","El afiche dice *School gym*: la feria es en el gimnasio. La fecha y la hora responden otras preguntas (*when?*).","OA16")
q("","**{n}.** *(Alternativas — completar, desafiante)* ",'Complete (a plan already decided): *"— What are your plans for the weekend? — I ___ visit my grandparents. I already bought the bus tickets."*',
 ["*am going to","will","going to","am go to"],"c","Para un plan ya decidido (ya compró los pasajes) se usa *be going to*: *I am going to visit*. *Will* se usa para decisiones espontáneas.","OA16")
q("","**{n}.** *(Selección múltiple — desafiante)* ",'¿Qué oración describe correctamente en inglés a «el niño de pelo crespo es mi primo»?',
 ["*The boy with curly hair is my cousin.","The boy with hair curly is my cousin.","The boy of curly hair is my cousin.","The curly boy with hair is my cousin."],"a","En inglés el adjetivo va antes del sustantivo (*curly hair*) y para describir rasgos se usa *with*: *the boy with curly hair*.","OA16")
q("",CO,'Complete: *"She ___ eats meat because she is vegetarian."*',
 ["*never","always","usually","often"],"d","Una persona vegetariana no come carne: *never* (nunca). *Always* y *usually* dirían lo contrario.","OA16")
q("","**{n}.** *(Varias correctas — preferencia, desafiante)* ",'*"Would you prefer to study in the morning or in the afternoon? Why?"* Which answers justify the preference correctly?',
 ["I prefer to study in the morning because my mind is fresh.","I prefer study morning because yes.","I prefers the afternoon because it is afternoon.","I\'d rather study in the afternoon because I have more free time."],"ad","a y d. Ambas expresan una preferencia con una estructura correcta (*I prefer to...*, *I\'d rather...*) y una razón coherente después de *because*. Las otras tienen errores y no justifican.","OA16")
q("","**{n}.** *(Alternativas — completar, desafiante)* ",'Complete: *"We got ___ the train in Chillán and got ___ in Concepción."*',
 ["*on / off","in / out","off / on","into / of"],"c","Con trenes y buses se usa *get on* (subir) y *get off* (bajar). *Get in / out* se usa con autos.","OA16")
armar(C/'ingles-examen-forma-b.md', C/'ingles-examen-forma-a.md', Q,
  fila=lambda i,p,cl: (f"| {i} | {cl}: {p.explicacion.split(': ',1)[1]} | {p.oa} |" if not p.opciones else f"| {i} | **{cl}.** {p.explicacion.split('. ',1)[1] if len(p.letra)>1 else p.explicacion} | {p.oa} |"),
  reemplazos={"— Forma B":"— Forma A","FORMA B":"FORMA A","ultima_actualizacion: 2026-11-01":"ultima_actualizacion: 2026-11-16","(estímulos nuevos para los mismos OA)":"(estímulos nuevos para los mismos OA, distintos de la Forma B)"},
  inicio_preguntas="## OA N°9", nota_varias="")
if __name__=="__main__":
    from collections import Counter; print(Counter(p.letra for p in Q), len(Q))
