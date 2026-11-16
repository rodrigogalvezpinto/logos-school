import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from forma_a import P, armar  # noqa: E402
C=Path(__file__).resolve().parents[4]/'contenido'/'07-basico/examenes'
SM="**{n}.** *(Selección múltiple)* "; CO="**{n}.** *(Alternativas — completar)* "; VO="**{n}.** *(Alternativas — vocabulario)* "
Q=[]
def q(sec,cab,en,ops,l,ex,oa):
    if len(l)>1: en=en+" Marca **todas** las correctas."
    Q.append(P(sec,cab,en,ops,l,ex,oa))
def vf(sec,en,v,ex,oa): Q.append(P(sec,"**{n}.** *(Verdadero o falso)* ",en,[],"V" if v else "F",ex,oa,{"clave":"True (Verdadero)" if v else "False (Falso)"}))
q("## OA N°9 — Comprender la idea general y la información explícita de un texto\n\n",SM,'Read: *"Last Sunday, a group of neighbours planted forty native trees in a park in Temuco. They worked all morning and then shared lunch together."* What is the text mainly about?',
 ["*Neighbours planting trees in a park","A football match in Temuco","A school trip to the mountains","A family cooking lunch at home"],"b","El texto cuenta que unos vecinos plantaron cuarenta árboles nativos en un parque: esa es la idea general. El almuerzo compartido es solo un detalle.","OA9")
q("",SM,'Read: *"Hello! I\'m Amara. I live in Nairobi, Kenya. I run every morning with my older sister, because I want to be an athlete."* How often does Amara run?',
 ["*Every morning","Once a week","Only on Sundays","Every evening"],"a","El texto dice *\"I run every morning\"*: corre todas las mañanas.","OA9")
q("",CO,'Read: *"The Atacama Desert is one of the driest places on Earth. Some areas receive almost no rain for years."* Complete with one word from the text: *"Some areas of the Atacama receive almost no ___ for years."*',
 ["*rain","sun","sand","wind"],"c","El texto dice *almost no rain*: casi nada de lluvia. Es un dato explícito.","OA9")
vf("",'Read: *"Our library opens at 8 am and closes at 6 pm. On Saturdays, it opens only in the morning."* Write True or False: *The library is open on Saturday afternoons.*',False,
 "Falso: el texto dice que los sábados abre solo en la mañana (*only in the morning*).","OA9")
q("","**{n}.** *(Alternativas — función)* ",'¿Qué función cumple la oración *"In my opinion, the new park is the best place in town."*?',
 ["Dar un dato explícito que aparece en un texto informativo","Dar una instrucción para llegar al parque","Describir el orden en que ocurrieron unos hechos","*Expresar una opinión personal sobre el parque"],"d","*In my opinion* (en mi opinión) introduce una valoración personal, no un dato comprobable ni una instrucción.","OA9")
q("","**{n}.** *(Varias correctas — opinión, desafiante)* ",'Read: *"Our school wants to start a vegetable garden. Students will take care of it after class."* Which completions of *"I ___ with this idea because ___."* express a position with a coherent reason?',
 ["I agree with this idea because students can learn where food comes from.","I disagree with this idea because tomatoes are blue cars.","I disagree with this idea because students already have a lot of homework after class.","I agree with this idea because the garden is a Monday."],"ac","a y c. *I agree... students can learn where food comes from* y *I disagree... a lot of homework after class* son posturas válidas, porque cada una da una razón coherente con el tema. Las otras razones no tienen sentido.","OA9")
q("## OA N°10 — Comprender textos no literarios: secuencia, conectores y causa-efecto\n\n",SM,'Read: *"Violeta Parra was born in San Carlos, Chile, in 1917. She was a singer, a poet and a folklorist. In 1966, her song *Gracias a la vida* was released."* What happened in 1966?',
 ["*Her song *Gracias a la vida* was released.","She was born in San Carlos.","She started working as a teacher.","She traveled to Europe for the first time."],"c","El texto dice *\"In 1966, her song Gracias a la vida was released\"*: ese año se publicó su canción. En 1917 nació.","OA10")
q("",CO,'Complete with the correct connector: *"I was very tired, ___ I went to bed early."*',
 ["*so","but","because","before"],"a","*So* (así que) introduce una consecuencia: estaba cansado, así que se acostó temprano. *Because* introduciría la causa.","OA10")
vf("",'Read: *"Football is the most popular sport in Chile. I think it is the most exciting sport in the world."* Write True or False: *The second sentence expresses a fact.*',False,
 "Falso: *I think* introduce una opinión personal; la primera oración es la que presenta un hecho.","OA10")
q("",VO,'What does *"careful"* mean?',
 ["Cariñoso","*Cuidadoso","Descuidado","Cansado"],"b","*Care* significa cuidado y el sufijo *-ful* indica «lleno de»: *careful* es cuidadoso. *Careless* sería descuidado.","OA10")
q("",SM,'Read: *"The river flooded the streets because it rained for three days."* What relationship between the ideas does the text show?',
 ["*Cause and effect","Sequence of steps","Comparison","Description of a person"],"a","*Because* une la causa (llovió tres días) con el efecto (el río inundó las calles).","OA10")
q("",CO,'Complete: *"The children played ___ in the snow."* (happy + -ly)',
 ["*happily","happyly","happy","happier"],"d","Para decir cómo jugaron (modo) se usa el adverbio *happily*: a *happy* se le agrega *-ly* y la *y* cambia a *i*.","OA10")
q("## OA N°13 — Escribir historias e información con apoyo de imágenes\n\n",SM,'Which connector best completes this story? *"Sofía was reading in the garden. ___, it started to rain heavily and she ran inside."*',
 ["*Suddenly","Because","First of all","Although"],"c","*Suddenly* (de repente) introduce un hecho inesperado en la historia: empezó a llover.","OA13")
q("",SM,'Which sentence would you include in a short text about the **traditions** of another country?',
 ["*In Japan, people take off their shoes before entering a house.","My bedroom has a blue door and a very big window.","Yesterday I ate rice with chicken at home with Mom.","The weather is very cold and windy today in my city."],"b","*In Japan, people take off their shoes* describe una costumbre japonesa: es información sobre tradiciones. Las otras oraciones hablan de la vida personal o del clima.","OA13")
q("",CO,'Complete about a personal experience: *"Last summer, we ___ to the beach and ___ ice cream every day."* (go / eat, simple past)',
 ["*went / ate","go / eat","goed / eated","going / eating"],"d","Ambos verbos son irregulares en pasado simple: *go → went* y *eat → ate*.","OA13")
q("","**{n}.** *(Alternativas — completar siguiendo modelo)* ",'Which option completes the model *"My grandparents are ___. I think this is important because ___."* correctly?',
 ["*recycling at home / it reduces garbage","recycle at home / the garbage bag","recycling at home / because yes yes","recycled at home / is very important"],"a","Después de *are* se necesita un verbo en -ing (*recycling*), y después de *because* una razón completa y coherente.","OA13")
q("","**{n}.** *(Alternativas — escribir siguiendo modelo)* ",'Model: *"On weekends, I usually play football with my friends in the park."* Which option follows the model *"On weekends, I usually ___ with ___ in ___."*?',
 ["*ride my bike / my brother / the square","my brother / ride my bike / the square","rides my bike / my brother / the square","ride my bike / the square / my brother"],"c","El orden del modelo es: actividad, con quién y dónde. *I ride* va sin -s, porque el sujeto es *I*.","OA13")
q("","**{n}.** *(Varias correctas — consejos, desafiante)* ",'You are writing a poster about a heat wave. Which sentences with *must* or *mustn\'t* give safe advice?',
 ["You must drink water often.","You mustn\'t stay in the sun at midday.","You must wear heavy winter clothes.","You mustn\'t drink any water during the day."],"ab","a y b. *You must drink water often* y *you mustn\'t stay in the sun at midday* protegen del calor. Usar ropa gruesa de invierno o no tomar agua son consejos peligrosos.","OA13")
q("## OA N°16 — Usar estructuras gramaticales variadas al escribir\n\n",VO,'What does *"I\'m bored"* mean?',
 ["Estoy cansado","*Estoy aburrido","Estoy enojado","Estoy asustado"],"b","*Bored* significa aburrido: *I\'m bored* = estoy aburrido. Cansado es *tired*.","OA16")
q("",CO,'Complete: *"She answered all the questions ___."* (correct, adverb of manner)',
 ["*correctly","correct","more correct","correction"],"d","Para describir cómo respondió se usa el adverbio de modo *correctly*.","OA16")
q("",SM,'Which sentence uses *if* correctly to show a cause and its effect?',
 ["*If you heat ice, it melts.","If you heat ice, it melt.","If you heats ice, it melts.","You heat ice if, it melts."],"a","Con *if* se expresa la condición (calentar el hielo) y su efecto (se derrite). *It melts* lleva -s porque el sujeto es *it*.","OA16")
q("",CO,'Complete with past continuous and past simple: *"While I ___ my homework, the lights ___ out."* (do / go)',
 ["*was doing / went","did / was going","was doing / goed","am doing / go"],"c","La acción en curso va en pasado continuo (*was doing*) y la que la interrumpe, en pasado simple (*went*).","OA16")
q("","**{n}.** *(Varias correctas — respuesta corta)* ",'*"— Are you coming to the party on Saturday? — ___"* Which short answers are correct?',
 ["Yes, I am.","No, I\'m not.","Yes, I do.","No, I don\'t."],"ab","a y b. Una pregunta con *are* se responde con *am* (*Yes, I am* / *No, I\'m not*). *Do* y *don\'t* responden preguntas con *do*.","OA16")
q("",SM,'Complete: *"Can you pass me ___ book here, next to you?"*',
 ["*this","those","these","them"],"d","*This* se usa para un solo objeto cercano (*here, next to you*). *These* y *those* son plurales.","OA16")
q("",CO,'Complete: *"How ___ apples are there in the box?"*',
 ["*many","much","old","long"],"b","*Apples* es contable y está en plural, por eso se usa *How many*. *Much* se usa con incontables, como *water*.","OA16")
armar(C/'ingles-examen-forma-b.md', C/'ingles-examen-forma-a.md', Q,
  fila=lambda i,p,cl: (f"| {i} | {cl}: {p.explicacion.split(': ',1)[1]} | {p.oa} |" if not p.opciones else f"| {i} | **{cl}.** {p.explicacion.split('. ',1)[1] if len(p.letra)>1 else p.explicacion} | {p.oa} |"),
  reemplazos={"— Forma B":"— Forma A","FORMA B":"FORMA A","ultima_actualizacion: 2026-11-01":"ultima_actualizacion: 2026-11-16","(estímulos nuevos para los mismos OA)":"(estímulos nuevos para los mismos OA, distintos de la Forma B)"},
  inicio_preguntas="## OA N°9", nota_varias="")
if __name__=="__main__":
    from collections import Counter; print(Counter(p.letra for p in Q), len(Q))
