import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from forma_a import P, armar  # noqa: E402
C=Path(__file__).resolve().parents[4]/'contenido'/'05-basico/examenes'
SM="**{n}.** *(Selección múltiple)* "; AL="**{n}.** *(Alternativas — completar)* "; VF="**{n}.** *(Verdadero o falso)* "
Q=[]
def q(sec,cab,en,ops,l,ex,oa): Q.append(P(sec,cab,en,ops,l,ex,oa))
q("## OA N°5 — Comprensión de textos cortos cotidianos\n\n",SM,'Read: *"Hi! I am Tomás. I have a dog. My dog is black and white. His name is Max."* What color is Max?',
 ["Black and white","Brown","Black and blue","White and yellow"],"a","El texto dice *\"My dog is black and white\"*: Max, el perro de Tomás, es blanco y negro.","OA5")
q("",SM,'Read: *"Put your bag under the desk. Put your book on the desk."* Which sentence follows the instructions?',
 ["The bag goes under the desk.","The book goes under the desk.","The bag goes on the chair.","The book goes in the bag."],"c","*Under the desk* significa «debajo del escritorio»: ahí va la mochila (*bag*). El libro va *on the desk*, sobre el escritorio.","OA5")
q("",AL,'Read: *"I like apples. I don\'t like bananas."* Join both ideas with **but**: *"I like apples ___ I don\'t like bananas."*',
 ["but","and","or","is"],"b","*But* (pero) une dos ideas que se oponen: me gustan las manzanas, pero no los plátanos.","OA5")
q("","**{n}.** *(Alternativas — comprensión)* ",'Read: *"On Saturday, Ana goes to the park. On Sunday, she visits her grandmother."* What does Ana do on Sunday?',
 ["She visits her grandmother.","She goes to the park.","She goes to school.","She visits her friend."],"d","El texto dice *\"On Sunday, she visits her grandmother\"*: el domingo visita a su abuela. Al parque va el sábado (*Saturday*).","OA5")
Q.append(P("",VF,'Read: *"There are two cats and one dog in my house."* Write True or False: *There are two dogs in the house.*',[],"F","Falso: el texto dice que hay dos gatos (*two cats*) y un solo perro (*one dog*).","OA5",{"clave":"False (Falso)"}))
q("## OA N°6 — Notas, postales, invitaciones y otros textos cotidianos\n\n",SM,'Read: *"Happy Birthday, Sofía! Have a great day! Love, Carlos."* What type of text is this?',
 ["A birthday card","A menu","A weather report","A shopping list"],"b","*Happy Birthday* (feliz cumpleaños) y el saludo final *Love, Carlos* muestran que es una tarjeta de cumpleaños.","OA6")
q("",SM,'Read the note: *"Mom, I am at Pedro\'s house. I am back at six. Love, Daniel."* Where is Daniel?',
 ["At Pedro's house","At school","At the park","At home with Mom"],"c","La nota dice *\"I am at Pedro's house\"*: Daniel está en la casa de Pedro y vuelve a las seis.","OA6")
q("",AL,'Read the dialogue: *"— I\'m sorry, I\'m late. — ___"* Complete with a kind answer to an apology.',
 ["That's OK.","Happy birthday!","Good night.","Thank you."],"a","*That's OK* (no importa, está bien) es una respuesta amable a una disculpa. *Thank you* se usa para agradecer, no para responder a *I'm sorry*.","OA6")
q("","**{n}.** *(Alternativas — comprensión)* ",'Read: *"Come to my party on Saturday at three o\'clock. Bring your swimsuit! We can swim in the pool. From, Lucas."* What should the guests bring?',
 ["A swimsuit","A birthday cake","A football","A book"],"d","*Bring your swimsuit* significa «trae tu traje de baño», porque en la fiesta podrán nadar en la piscina (*pool*).","OA6")
Q.append(P("",VF,'Read: *"Dear Grandpa, I am at the beach with Mom. The water is cold, but the sand is hot. Love, Maite."* Write True or False: *Maite is at the beach with her father.*',[],"F","Falso: Maite está en la playa con su mamá (*with Mom*), no con su papá.","OA6",{"clave":"False (Falso)"}))
q("## OA N°8 — Reaccionar y opinar sobre lo leído\n\n",SM,'Read: *"My favorite fruit is mango. It is sweet and yellow."* Which response expresses **your own opinion** about mangoes?',
 ["I think mangoes are delicious.","Mangoes are yellow.","The mango is on the table.","There is one mango."],"b","*I think...* (yo creo...) expresa una opinión propia. Las otras oraciones solo describen o informan.","OA8")
q("",SM,'Read: *"Pablo plays football every day. He loves sports."* You don\'t like football. Which response compares Pablo\'s preference with yours?',
 ["I don't like football, but I like swimming.","Pablo has a red ball and new boots.","The football field near my school is big.","It is sunny and warm in the city today."],"d","*I don't like football, but I like swimming* compara: a Pablo le gusta el fútbol y a ti no, aunque te gusta nadar. Las otras no hablan de tus gustos.","OA8")
q("",AL,'Read: *"My brother eats pizza every Friday."* Complete with **like** or **likes**: *"My brother ___ pizza."*',
 ["likes","like","liking","to like"],"b","Con *he/she/it* (aquí, *my brother*) el verbo lleva -s: *likes*. Con *I* se usa *like*.","OA8")
q("","**{n}.** *(Alternativas — responder en inglés)* ",'Read: *"My dog sleeps in my bedroom."* Do you like dogs? Which short answer is grammatically correct?',
 ["Yes, I do.","Yes, I does.","Yes, I am.","Yes, I like."],"a","A *Do you like...?* se responde *Yes, I do* o *No, I don't*. *Does* es para *he/she*, *I am* responde a preguntas con *Are you...?* y *Yes, I like* queda incompleta.","OA8")
Q.append(P("",VF,'Read: *"Ema likes cats. I like cats, too."* Write True or False: *Ema and the narrator like the same animal.*',[],"V","Verdadero: a Ema le gustan los gatos y al narrador también (*too* = también).","OA8",{"clave":"True (Verdadero)"}))
q("## OA N°14 — Completar y escribir textos siguiendo un modelo\n\n",SM,'Model: *"Dear Ana, I am at the park. Love, Tim."* Complete the end of another postcard following the model: *"Dear Mom, I am at the zoo. ___, Tim."*',
 ["Love","Under","Seven","Rainy"],"a","Como en el modelo, la postal se despide con *Love* (con cariño) antes del nombre.","OA14")
q("",SM,'Complete with the opposite of **hot**: *"The soup is hot. The ice cream is ___."*',
 ["cold","tall","happy","open"],"c","Lo contrario de *hot* (caliente) es *cold* (frío): la sopa está caliente y el helado, frío.","OA14")
q("",AL,'Complete this note with the correct weather word: *"It is raining. Take your umbrella. Today is ___."*',
 ["rainy","sunny","hot"],"b","*It is raining* (está lloviendo) y el paraguas (*umbrella*) indican un día lluvioso: *rainy*.","OA14")
q("",AL,'Complete this list of winter clothes: *"I need a scarf, gloves and a ___."*',
 ["coat","swimsuit","pair of sandals"],"a","*Coat* (abrigo) es ropa de invierno, como la bufanda (*scarf*) y los guantes (*gloves*). El traje de baño y las sandalias son para el verano.","OA14")
q("","**{n}.** *(Alternativas — escribir siguiendo modelo)* ",'Model: *"My name is Sara. I am ten."* Which sentence follows the model with **other information**?',
 ["My name is Diego. I am eleven.","My name is Sara. I am ten.","My name are Diego. I am eleven.","My name is Diego. I eleven."],"c","Sigue el modelo con otro nombre y otra edad. Las otras repiten el modelo o tienen errores (*are* con *my name*, falta *am*).","OA14")
q("## OA N°15 — Escribir oraciones para describir, preguntar y contar\n\n",SM,'La pelota está debajo de la mesa. Complete the sentence: *"The ball is ___ the table."*',
 ["under","on","in","and"],"c","*Under* significa «debajo de». *On* es «sobre» e *in*, «dentro de».","OA15")
q("",SM,'Hablas del libro de tu amiga Paula. Complete: *"This is ___ book."*',
 ["her","his","my","your"],"d","*Her* se usa para algo que pertenece a una mujer o niña: *her book* (su libro, el de Paula). *His* es para un hombre o niño.","OA15")
q("","**{n}.** *(Alternativas — completar con número)* ",'Completa con el número **15** en inglés: *"There are ___ students in my class."*',
 ["fifteen","fifty","five","fifteenth"],"d","15 = *fifteen*. *Fifty* es 50, *five* es 5 y *fifteenth* es el ordinal (decimoquinto).","OA15")
q("","**{n}.** *(Alternativas — completar diálogo)* ",'Complete the negative answer: *"— Are these your shoes? — No, ___."*',
 ["they aren't","it isn't","they are","I'm not"],"b","*These* (estos) es plural, así que la respuesta corta usa *they*: *No, they aren't*. *It isn't* sería para una sola cosa.","OA15")
q("",AL,'Complete the question: *"— ___ is your birthday? — It\'s in May."*',
 ["When","Where","Who","What color"],"a","*When* (cuándo) pregunta por el momento; la respuesta *in May* (en mayo) es una fecha.","OA15")
armar(C/'ingles-examen-forma-b.md', C/'ingles-examen-forma-a.md', Q,
  fila=lambda i,p,cl: (f"| {i} | {cl}: {p.explicacion.split(': ',1)[1]} | {p.oa} |" if not p.opciones else f"| {i} | **{cl}.** {p.explicacion} | {p.oa} |"),
  reemplazos={"— Forma B":"— Forma A","FORMA B":"FORMA A","ultima_actualizacion: 2026-11-01":"ultima_actualizacion: 2026-11-16","(estímulos nuevos para los mismos OA)":"(estímulos nuevos para los mismos OA, distintos de la Forma B)"},
  inicio_preguntas="## OA N°5")
from collections import Counter; print(Counter(p.letra for p in Q), len(Q))
