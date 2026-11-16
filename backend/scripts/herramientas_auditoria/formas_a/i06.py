import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from forma_a import P, armar  # noqa: E402
C=Path(__file__).resolve().parents[4]/'contenido'/'06-basico/examenes'
SM="**{n}.** *(Selección múltiple)* "; CO="**{n}.** *(Alternativas — completar)* "; CP="**{n}.** *(Alternativas — comprensión)* "; OP="**{n}.** *(Alternativas — opinión con razón)* "
Q=[]
def q(sec,cab,en,ops,l,ex,oa): Q.append(P(sec,cab,en,ops,l,ex,oa))
q("## OA N°5 — Habilidades, direcciones, hora y presente vs. pasado\n\n",SM,'Read: *"My aunt is a nurse. She can drive an ambulance and help sick people, but she can\'t swim."* What can\'t she do?',
 ["Swim","Drive an ambulance","Help sick people","Work at a hospital"],"b","*She can\'t swim* significa «no sabe nadar». Sí puede manejar una ambulancia y ayudar a enfermos (*she can drive... and help*).","OA5")
q("",SM,'Read: *"Walk along Main Street and turn left at the bank. The library is next to the bakery."* Where is the library?',
 ["Next to the bakery","Behind the bank","Opposite the school","In front of the park"],"c","*Next to the bakery* significa «al lado de la panadería». El banco (*bank*) es donde se dobla a la izquierda, no donde está la biblioteca.","OA5")
q("",CO,'The train to Temuco leaves at 8:45. Complete with one word: *"The train leaves at a quarter ___ nine."*',
 ["to","past","half","after"],"a","8:45 son las nueve menos cuarto: *a quarter to nine*. *A quarter past nine* sería 9:15.","OA5")
q("",CP,'Read: *"Now Tomás lives in Santiago. Two years ago, he lived in Arica, near the beach."* Where did Tomás live two years ago?',
 ["He lived in Arica.","He lives in Arica.","He lived in Santiago.","He lives near the beach in Santiago."],"d","*Two years ago* (hace dos años) pide el pasado: *he lived in Arica*. Ahora (*now*) vive en Santiago.","OA5")
q("",CO,'Read: *"There are thirty students in my class, and nineteen are girls."* Complete with the number in words: *"There are ___ girls in my class."*',
 ["nineteen","ninety","nine","eleven"],"c","19 = *nineteen*. *Ninety* es 90 y *nine* es 9.","OA5")
q("## OA N°6 — Notas, recetas, avisos y correos sobre temas cotidianos\n\n",SM,'Read: *"LOST CAT! Grey cat with white paws. Her name is Luna. Please call 9 8765 4321."* What is the purpose of this notice?',
 ["To find a lost cat","To sell a grey cat","To advertise a pet shop","To invite people to a party"],"a","*Lost cat* (gata perdida), la descripción y el teléfono muestran que el aviso busca encontrar a Luna.","OA6")
q("",SM,'Read: *"Hi Ms. Pérez, Sofía is sick today. She has a cold. She will be back on Thursday. Best wishes, Mrs. Rojas."* When will Sofía come back to school?',
 ["On Thursday","Today","Next month","On Monday"],"b","El correo dice *She will be back on Thursday*: volverá el jueves. Hoy (*today*) está enferma.","OA6")
q("",CP,'Read the recipe: *"First, cut the bananas. Then, put them in a glass with milk. Finally, mix everything."* What do you do **first**?',
 ["Cut the bananas.","Mix everything.","Put the milk in a glass.","Drink the milkshake."],"d","*First* (primero) indica el primer paso: cortar los plátanos. *Then* y *finally* marcan los pasos siguientes.","OA6")
q("",CP,'Read the notice: *"Swimming pool. Open: Tuesday to Sunday, 10 am – 7 pm. Closed on Mondays."* Which sentence is true?',
 ["It is closed on Mondays.","It opens at 7 am.","It is open every day.","It closes at 10 pm."],"c","El aviso dice *Closed on Mondays*: los lunes está cerrada. Abre a las 10 am y cierra a las 7 pm.","OA6")
Q.append(P("","**{n}.** *(Verdadero o falso)* ",'Read the note: *"Dad, I\'m at the library with Camila. We are doing our homework. I\'ll be home at 5. Tomás."* Write True or False: *Tomás is at the library with Camila.*',[],"V","Verdadero: la nota dice *I\'m at the library with Camila*.","OA6",{"clave":"True (Verdadero)"}))
q("## OA N°8 — Reaccionar y opinar sobre lo que leo en inglés\n\nLa pregunta 12 comprueba comprensión literal (OA 5) como apoyo; las demás preguntas de este apartado evalúan la reacción a lo leído (OA 8).\n\n",SM,'Read: *"During the storm, the lights went out and we heard loud thunder all night."* Which response expresses **your own feeling** about the text?',
 ["I would feel scared in a storm like that.","The lights in the house went out.","There was loud thunder all night long.","The storm was at night, not in the day."],"d","*I would feel scared* (yo sentiría miedo) expresa un sentimiento propio frente a lo leído. Las otras repiten datos del texto.","OA8")
q("",SM,'Read: *"Martín won the chess game, and he felt very proud."* How did Martín feel?',
 ["Proud","Sad","Angry","Bored"],"a","El texto dice *he felt very proud*: se sintió muy orgulloso.","OA5")
q("",CO,'Complete with the correct word: *"I like the story, ___ the ending is very sad."*',
 ["but","because","so","or"],"b","*But* (pero) une dos ideas que se oponen: me gusta la historia, pero el final es triste. *Because* daría una razón.","OA8")
q("",OP,'Read: *"In the story, a brave girl climbs a mountain to save a lost dog."* Which answer to *Which character do you like more? Why?* gives a character and a reason that fits the story?',
 ["I like the girl because she is brave and saves the dog.","I like the dog because it climbs the mountain to save the girl.","I likes the girl because she is brave and climbs.","The girl is a story about a dog and a mountain."],"c","La respuesta nombra un personaje (*the girl*) y una razón que coincide con el cuento: *she is brave* y salva al perro (*saves the dog*). Las otras cambian los hechos, tienen errores (*I likes*) o no responden.","OA8")
q("",OP,'Read: *"Diego reads comics every night. He thinks they are exciting because of the pictures."* Which is a correct answer to *Do you like reading comics? Why or why not?*',
 ["Yes, I do, because the pictures are exciting.","Yes, I does, because comics are a lot.","Diego reads comics every night in bed.","No, I don\'t, because pictures the night is."],"d","Responde con *Yes, I do* y una razón con sentido: los dibujos (*pictures*) son emocionantes (*exciting*). También valdría *No, I don\'t* con una razón. Las otras tienen errores (*I does*), repiten el texto o no forman una oración.","OA8")
q("## OA N°14 — Escribir textos siguiendo un modelo\n\n",SM,'Which word completes the invitation correctly? *"Come to my birthday party! It starts ___ 4 pm."*',
 ["at","on","in","under"],"a","Con horas se usa *at*: *at 4 pm*. *On* se usa con días y fechas, e *in*, con meses.","OA14")
q("",SM,'Choose the word that rhymes and completes the poem: *"I have a big red ball, / it bounces on the ___."*',
 ["wall","chair","table","box"],"b","*Wall* (muralla) rima con *ball* (pelota): ambas terminan en *-all*.","OA14")
q("",CO,'Complete the email with the greeting and the closing: *"___ Aunt Rosa, We are in Chiloé. It is windy, but beautiful. ___, Valentina."*',
 ["Dear / Love","Goodbye / Hello","Love / Dear","Hello / Goodbye"],"c","*Dear* inicia el correo y *Love* (con cariño) lo cierra antes del nombre.","OA14")
q("",CO,'Complete the comic strip. Panel 1: A girl says, *"I\'m hungry!"* Panel 2: Her mother says, *"___"* Panel 3: The girl eats a sandwich.',
 ["Here is a sandwich for you.","Good night, see you tomorrow.","It is raining outside.","Your shoes are under the bed."],"d","Es la única opción coherente con el panel 1 (la niña tiene hambre) y el panel 3 (come un sándwich).","OA14")
q("","**{n}.** *(Alternativas — escribir siguiendo un modelo)* ",'Model: *"Dear ___, I am visiting ___ with my family. Today we ___. Love, ___."* Which message follows the model correctly?',
 ["Dear Tomás, I am visiting Pucón with my family. Today we swam in the lake. Love, Clara.","Dear Pucón, I am visiting Tomás with my family. Today we lake. Love, swam.","Dear Tomás, I is visiting Pucón with my family. Today we swam in the lake. Love, Clara.","Dear Tomás, I am visiting Pucón with my family. Today we swimming in the lake. Love, Clara."],"a","El mensaje a Tomás desde Pucón pone cada dato en su lugar (nombre, lugar, actividad, firma) y los verbos están bien escritos. Las otras confunden los datos o tienen errores (*I is*, *we swimming*).","OA14")
q("## OA N°15 — Describir, contrastar, presente continuo y preguntar\n\n",SM,'Complete the dialogue: *"— Are your parents at home? — Yes, ___. They are cooking dinner."*',
 ["they are","they aren\'t","he is","it is"],"b","A *Are your parents...?* se responde con *they*: *Yes, they are*. Después dice que están cocinando, así que la respuesta es afirmativa.","OA15")
q("",SM,'Choose the correct word: *"Three ___ are crossing the street."*',
 ["women","womans","woman","womens"],"c","*Woman* tiene plural irregular: *women*. No se le agrega -s.","OA15")
q("",CO,'Complete to express necessity: *"She ___ to study for the test tomorrow."*',
 ["has","have","having","is"],"d","Con *she* se dice *she has to*: tiene que estudiar. *Have to* se usa con *I, you, we, they*.","OA15")
q("","**{n}.** *(Alternativas — completar con contraste)* ",'Complete: *"A cheetah runs ___ than a horse."*',
 ["faster","fast","more fast","fastest"],"a","Para comparar dos animales se usa el comparativo con *than*: *faster than*. *Fastest* es el superlativo.","OA15")
q("","**{n}.** *(Alternativas — formular preguntas)* ",'Which question matches this answer? *"— ___ is this T-shirt? — It\'s 8,000 pesos."*',
 ["How much","How many","How old","How far"],"b","*How much* pregunta por el precio; la respuesta es una cantidad de dinero. *How many* pregunta cuántos objetos hay.","OA15")
armar(C/'ingles-examen-forma-b.md', C/'ingles-examen-forma-a.md', Q,
  fila=lambda i,p,cl: (f"| {i} | {cl}: {p.explicacion.split(': ',1)[1]} | {p.oa} |" if not p.opciones else f"| {i} | **{cl}.** {p.explicacion} | {p.oa} |"),
  reemplazos={"— Forma B":"— Forma A","FORMA B":"FORMA A","ultima_actualizacion: 2026-11-01":"ultima_actualizacion: 2026-11-16","(estímulos nuevos para los mismos OA)":"(estímulos nuevos para los mismos OA, distintos de la Forma B)"},
  inicio_preguntas="## OA N°5")
if __name__=="__main__":
    from collections import Counter; print(Counter(p.letra for p in Q), len(Q))
