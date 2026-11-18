import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from forma_a import P, armar  # noqa: E402
C=Path(__file__).resolve().parents[4]/'contenido'/'03-medio/examenes'
Q=[]
def q(sec,tipo,en,ops,l,ex,oa): Q.append(P(sec,"**{n}.** *(%s)* "%tipo,en,ops,l,ex,oa))
S1='''## OA N°1 — Comprender, organizar y comparar información central sobre otras culturas

*(Lee el o los textos y responde las preguntas 1 a 8.)*

**Texts A and B — Sharing food**

**A — A neighbourhood blog in Berlin, Germany**
> Our community fridge stands outside a bakery. Anyone can leave food that is still good, and anyone can take it, no questions asked. Volunteers check the dates every evening and remove anything that has expired. The fridge started after a shop owner noticed how much bread was thrown away. Today, the volunteers say that the fridge is less about free food and more about trust between strangers.

**B — A school bulletin in Valparaíso, Chile**
> Every Friday, our class cooks a community pot with vegetables donated by market stallholders. Neighbours bring their own containers and take a portion home. We do not write down names, because nobody should feel watched when asking for food. Unlike the fridge in Berlin, we cook the food together, so students also learn to plan a menu. Still, both projects use food that would otherwise be wasted.

'''
S3='''## OA N°3 — Analizar textos y construir una postura personal crítica

*(Lee el o los textos y responde las preguntas 9 a 16.)*

**Texts C and D — Phones in the library?**

**C — Student newspaper editorial**
> Many students research their homework on their phones, but phones are banned in the school library. We propose allowing phones for study purposes during the afternoon. Students would keep them on silent and use headphones. We are not asking for permission to play games or watch videos: responsible use is the point.

**D — Librarian's response**
> I agree that phones can be useful research tools. However, the library is the only quiet place for students who need to concentrate. Allowing phones everywhere might increase noise. I suggest reserving two tables near the entrance for phone research during one month, and then asking users whether the rest of the room stayed quiet. A trial might show us problems we cannot predict.

'''
S4='''## OA N°4 — Producir textos claros para interactuar y reflexionar sobre la identidad

*(Lee el o los textos y responde las preguntas 17 a 25.)*

**Model email**

> Hi Sam,
> Our school magazine is collecting stories about objects that represent our families. I chose my grandmother's old teapot, although nobody uses it anymore. She brought it from Chiloé when she moved to the city, and it reminds me that our family story started far from here. Readers are invited to send photos of their own objects. Could you tell us about an object that matters to you?
> Best,
> Jamie

Puedes usar experiencias reales o inventadas; no incluyas datos privados ni direcciones.

'''
q(S1,"Alternativas — organizador","Which option completes the organizer correctly? Berlin / Main activity / What volunteers do — Valparaíso / Main activity / What students learn",
 ["Berlin: people cook together / sell bread — Valparaíso: a fridge / repair containers","Berlin: a bakery sale / bake bread — Valparaíso: a fridge / check dates","*Berlin: a community fridge / check dates every evening — Valparaíso: a community pot / plan a menu","Berlin: a community pot / plan a menu — Valparaíso: a fridge / check dates"],"c",
 "Text A describes a community fridge whose volunteers check the dates every evening; Text B describes a community pot where students learn to plan a menu.","OA1")
q("","Alternativas — comprensión","According to the volunteers, why is the Berlin fridge more than a source of free food?",
 ["*Because it builds trust between strangers","Because it sells bread at very low prices","Because it teaches people how to bake bread","Because it only accepts food from the bakery"],"a",
 "The text says the fridge «is less about free food and more about trust between strangers»: it builds trust between strangers.","OA1")
q("","Selección múltiple","Which comparison captures the main difference between the two projects?",
 ["Berlin uses fresh food from the bakery, whereas Valparaíso uses only expired food from shops","Berlin asks for everyone's name, whereas Valparaíso records every neighbour in a notebook","Berlin charges a small fee for each item, whereas Valparaíso is completely free for everyone","*In Valparaíso students cook the food together, whereas in Berlin people simply leave and take food"],"d",
 "Text B says «Unlike the fridge in Berlin, we cook the food together»: in Valparaíso students cook together, whereas in Berlin people leave and take food.","OA1")
q("","Alternativas — completar","Reuse a three-word structure from Text A: *\"Volunteers check the fridge. People can take food, ___.\"*",
 ["no money needed","*no questions asked","nobody is there","only on Fridays"],"b",
 "Text A uses the fixed expression *no questions asked* (sin preguntas): anyone can take food without explaining why.","OA1")
q("","Alternativas — resumen","A neighbour wants to take a portion from the Valparaíso project. Which summary is accurate?",
 ["*Bring your own container on Friday and take a portion home; nobody writes down your name","Leave food that is still good in the fridge outside the bakery at any time of the day","Write your name on the list and cook the menu with the students every afternoon","Pay for your portion at the market stall that donated the vegetables to the class"],"a",
 "Text B says neighbours bring their own containers on Friday and take a portion home, and that names are not written down.","OA1")
q("","Alternativas — comparación","Which pair of sentences uses *both* and *whereas* correctly with evidence from the texts?",
 ["Both projects sell food, whereas Berlin is more expensive than Valparaíso.","Both projects are in Germany, whereas Valparaíso is a big city.","*Both projects use food that would be wasted, whereas only Valparaíso cooks it together.","Both projects check dates every evening, whereas Berlin cooks on Fridays."],"c",
 "Text B states that «both projects use food that would otherwise be wasted», and only Valparaíso cooks the food together: *both* marks the similarity and *whereas* the difference.","OA1")
q("","Alternativas — inferencia","Why might writing down neighbours' names undermine the Valparaíso project's purpose?",
 ["Because the class would need more vegetables from the market","*Because people might feel watched and stop asking for food","Because names would make the community pot more expensive","Because the students do not know how to write names in English"],"b",
 "The text says «nobody should feel watched when asking for food»: recording names could make people feel watched and stop participating.","OA1")
q("","Selección múltiple","Which heading best fits both texts?",
 ["*Turning surplus food into community","How to bake bread in Germany","A cooking competition in Chile","Why fridges are expensive today"],"a",
 "Both texts describe projects that use food that would be wasted to bring people together: «Turning surplus food into community» integrates both.","OA1")
q(S3,"Alternativas — análisis","In Text C, what does *\"responsible use\"* refer to?",
 ["Playing games quietly in the library during the afternoon","Watching videos with the volume very low at every table","Using phones freely in every room of the school building","*Using phones only for study, on silent and with headphones"],"d",
 "Text C explains that students would keep phones «on silent» and use «headphones» for «study purposes», not to play games or watch videos: that is responsible use.","OA3")
q("","Alternativas — resumen guiado","Which summary of Text C follows the model *proposal / reason / what is NOT requested*?",
 ["Students want to close the library completely, because nobody uses it for research anymore.","*Students propose allowing phones for study, because they research on them, but they are not asking to play games.","Students propose banning phones everywhere in the school, because they make too much noise.","Students want new computers in the library, because phones are too small for homework."],"b",
 "The summary follows the model: proposal (allow phones for study), reason (students research on their phones) and what is not requested (games or videos).","OA3")
q("","Alternativas — comparación","Which option states one point of agreement and one difference between C and D?",
 ["Both want to ban phones in the whole school; they disagree only about the price of headphones.","Both want a new and bigger library; they disagree only about its opening hours on Fridays.","*Both see phones as useful for research; D worries more about noise for students who need quiet.","Both agree to allow phones everywhere at once; they disagree only about which games are allowed."],"c",
 "C and D agree that phones can be useful research tools; the difference is that D worries about noise for students who need to concentrate.","OA3")
q("","Varias correctas — postura crítica","Should the library allow phones everywhere at once or try the two reserved tables first? Which answers give a position with a reason grounded in the texts? Marca **todas** las correctas.",
 ["Try the two tables first, because the library is the only quiet place and a trial can show problems.","Allow phones everywhere, because I like my phone more than books.","Do nothing, because the texts are about community fridges.","Allow phones everywhere only if users later confirm the room stayed quiet during the trial."],"ad",
 "Positions a and d give a reason based on the texts (the library is the only quiet place; checking with users after a trial). b gives only a personal taste and c misreads the texts.","OA3")
q("","Alternativas — lenguaje en contexto","In *\"A trial might show us problems we cannot predict\"*, what does *might* tell us about the result?",
 ["*It expresses possibility, not certainty","It expresses a strong obligation","It expresses a habit in the past","It expresses a definite, proven fact"],"a",
 "*Might* expresses possibility: the trial could reveal problems, but it is not certain that it will.","OA3")
q("","Alternativas — audiencia y propósito","Which notice for younger students explains the librarian's trial clearly and invites feedback?",
 ["Phones are banned forever in the library. Please do not ask the librarian about this again.","Phones are allowed everywhere from today. You can play any game you like at any table.","The library will be closed next month for a phone trial. Please study at home instead.","*For one month, you can use phones for research at the two tables by the door. Tell us if the room stays quiet!"],"d",
 "This notice explains the trial in simple words (one month, two tables, research) and invites students to give feedback about the noise.","OA3")
q("","Alternativas — límite de la evidencia","The librarian has not yet tested the idea. Which question to library users would help assess the proposal?",
 ["\"Do you prefer red or blue headphones when you study at home in the evening?\"","\"How many phones and computers does your family have at home right now?\"","*\"Was the rest of the room quiet enough while people used phones at the two tables?\"","\"Which video games do you usually play at home with your friends on weekends?\""],"c",
 "The trial must check whether the rest of the room stayed quiet: asking users that question provides the evidence the proposal needs.","OA3")
q("","Selección múltiple","Which concluding sentence fairly represents both texts?",
 ["The librarian rejects every possible use of phones, so students should stop asking for anything.","*Both sides value research, so a short trial could balance useful phone use with a quiet space.","The students want to turn the quiet library into a noisy games room for everyone.","Neither text mentions noise, silence or concentration at any point in the discussion."],"b",
 "The conclusion integrates both texts: students value research on phones and the librarian values silence; a short trial could balance both needs.","OA3")
q(S4,"Alternativas — planificación","Which plan for your reply to Jamie is appropriate?",
 ["Audience: a teacher. Purpose: complain about the school magazine. Content: a long list of prices of old objects.","Audience: anyone on the internet. Purpose: sell an old object. Content: an advertisement with prices.","Audience: Jamie. Purpose: ask for a job at the magazine. Content: your phone number and home address.","*Audience: Jamie, a friend. Purpose: share an object that matters to you. Content: the object, its story and a question."],"d",
 "The reply is for Jamie (a friend); its purpose is to share an object that matters to you, with its story and a question, without private data.","OA4")
q("","Alternativas — producción","Which two connected sentences explain how an object can shape your sense of belonging?",
 ["*My grandfather's guitar is very old. Because he taught me my first song with it, it makes me feel part of a family tradition.","My grandfather's guitar is very old and brown. The weather in Chiloé is usually rainy and cold in winter.","My grandfather's guitar is old. I like pizza with cheese, and my school starts at eight every morning.","Guitars are usually made of wood. Some guitars are very expensive in the big music shops downtown."],"a",
 "The two sentences are connected by *because* and explain how the object (the guitar) creates a sense of belonging to a family tradition.","OA4")
q("","Alternativas — voz pasiva","Using *\"photos / send / by readers / every week\"*, which sentence uses the present simple passive correctly?",
 ["Photos sends by readers every week.","Photos are send by readers every week.","*Photos are sent by readers every week.","Photos is sent by readers every week."],"c",
 "Present simple passive with a plural subject: *are* + past participle (*sent*).","OA4")
q("","Alternativas — oración de relativo","Combine without repeating *teapot*: *\"This is the teapot. My grandmother brought it from Chiloé.\"*",
 ["This is the teapot who my grandmother brought it from Chiloé.","This is the teapot where my grandmother brought from Chiloé.","This is the teapot. Which my grandmother brought from Chiloé.","*This is the teapot that my grandmother brought from Chiloé."],"d",
 "*That* (or *which*) refers to a thing (*the teapot*); the object pronoun *it* is not repeated.","OA4")
q("","Alternativas — reflexión","Which sentence uses the frame *\"If I had not ___, I would not have ___\"* correctly?",
 ["If I have not joined the club, I will not meet my friends.","*If I had not joined the choir, I would not have met my best friends.","If I had not join the choir, I would not have meet my friends.","If I did not joined the choir, I would not met my friends."],"b",
 "The third conditional uses *had not* + past participle (*joined*) and *would not have* + past participle (*met*).","OA4")
q("","Alternativas — revisión de registro","A reply to Jamie ends *\"Send me your magazine NOW.\"* Which rewrite is a polite request suited to a friend?",
 ["*Could you send me a copy of the magazine when it is ready?","SEND THE MAGAZINE TO MY HOUSE IMMEDIATELY OR ELSE, JAMIE!!!","You must send me the magazine right now, Jamie, no excuses.","Magazine. Now. Thanks a lot for nothing, Jamie, bye bye."],"a",
 "*Could you…?* makes a polite request in a friendly register, unlike an order in capital letters.","OA4")
q("","Selección múltiple","Which sentence would best connect to *\"I used to think old objects were useless\"* and show a change of opinion?",
 ["I still think old objects are useless and should be thrown away.","Old objects are made of many different materials.","*Now I understand that they can keep a family's memories alive.","I bought a new phone last weekend in the city."],"c",
 "*Now I understand that…* contrasts the past belief (*used to think*) with a new opinion: old objects can keep family memories alive.","OA4")
q("","Selección múltiple","Which closing best fulfils Jamie's invitation to exchange experiences?",
 ["That is all I wanted to say. Please do not write back to me.","Please send me your home address and your phone number soon.","I have nothing more to say about objects or about families.","*What object did you choose for the magazine? I'd love to hear its story."],"d",
 "The closing continues the exchange: it asks Jamie about the object chosen and shows interest in its story.","OA4")
q("","Alternativas — correo","Which reply to Jamie includes a greeting, an object, its effect on identity, a question, a relative clause and two linked sentences?",
 ["Hi. Object: a guitar. It is old and made of wood. My grandfather had it in his house in the south for many years. Bye.","*Hi Jamie, I chose a guitar that my grandfather played every Sunday. Because he taught me my first song with it, it reminds me where I come from. What does your teapot look like? Best, Sam","Hello Jamie, guitars are wooden instruments with six strings, and many people around the world play them at parties, concerts and family meetings, especially in summer when the weather is good. Bye, Sam.","Dear magazine, please publish my full home address and my phone number on the next page, next to a big photo of me and my grandfather's old guitar, so everybody can visit us."],"b",
 "This reply has a greeting (*Hi Jamie*), an object, a relative clause (*that my grandfather played*), linked sentences with *because*, its effect on identity, a question and a closing.","OA4")
armar(C/'ingles-examen-forma-b.md', C/'ingles-examen-forma-a.md', Q,
  fila=lambda i,p,cl: f"| {i} | **{cl}.** {p.explicacion} | {p.oa} |",
  reemplazos={"— Forma B":"— Forma A","(Forma B)":"(Forma A)","ultima_actualizacion: 2026-11-01":"ultima_actualizacion: 2026-11-17"},
  inicio_preguntas="## OA N°1")
if __name__=="__main__":
    from collections import Counter; print(Counter(p.letra for p in Q), len(Q))
