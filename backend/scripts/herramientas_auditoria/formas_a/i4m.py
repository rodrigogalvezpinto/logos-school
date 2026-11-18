import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from forma_a import P, armar  # noqa: E402
C=Path(__file__).resolve().parents[4]/'contenido'/'04-medio/examenes'
Q=[]
def q(sec,tipo,en,ops,l,ex,oa): Q.append(P(sec,"**{n}.** *(%s)* "%tipo,en,ops,l,ex,oa))
SA='''## OA N°1 — Comprender información relevante para un propósito específico

*(Lee el o los textos y responde las preguntas 1 a 5.)*

**Text A — Review in an Australian school magazine**

> **Silent Streets: a novel worth discussing**
> In a near-future town, every street sign has been replaced by a talking app that guides people around the city. The council calls it "a city for everyone". Mara, a sixteen-year-old cyclist, soon notices that the app only speaks English and gives no visual information, so her deaf neighbour and the elderly speakers of other languages on her street keep getting lost. Mara paints simple signs with words and pictures and asks the council to keep them next to the app. Although the middle chapters move slowly, the novel asks a valuable question: who is a city really designed for? Recommended for readers aged fourteen and above who are interested in cities and inclusion.

'''
SB='''*(Lee el o los textos y responde las preguntas 6 a 8.)*

**Text B — Notice from a community centre in Edinburgh, Scotland**

> **Which languages live on your street?**
> On 9 August, from 10 a.m. to 12 p.m., our community centre will host a workshop to map the languages spoken in our neighbourhood. Bring a list of words you hear on your street, in any language, or write it here with our volunteers. You do not need to record anyone. We will ask permission before displaying anybody's words, and participants can remove them later. The workshop is free; book by 5 August so that we can prepare enough materials. Contact the centre if you need a sign language interpreter.

'''
SC='''## OA N°3 — Comprender y producir textos claros con postura personal crítica

*(Lee el o los textos y responde las preguntas 9 a 16.)*

**Text C — A proposal for a school theatre club**

> **Proposal: a ramp before new lights**
> Our theatre club performs in the school hall and has a small budget for one purchase this year. At Monday's meeting, actor Ana said, "I have measured the entrance." Ana reported that the hall's entrance has two steps and no handrail. Director Tomás proposed buying stage lights to make our shows more attractive. However, two families wrote that a relative who uses a wheelchair could not attend our last performance. We recommend buying a portable ramp first and asking the audience to test the access at the next show. New lights can wait until everyone can enter the hall. This proposal does not prove that a ramp will increase ticket sales; it argues that people who already want to see our shows should be able to come in.

'''
SD='''## OA N°4 — Producir y comprender textos para interactuar y explorar identidad

*(Lee el o los textos y responde las preguntas 17 a 25.)*

**Text D — A student exhibition introduction**

> Our exhibition, "Voices of Home", presents short recordings by students who have moved to this city from other regions or countries. Each recording describes one place where someone first felt that they belonged, such as a library, a football pitch or a market stall. We do not claim that moving means the same for everyone. Some contributors talk about new opportunities; others talk about what they miss. Each recording ends with a word that means "home" to its maker.

**Text E — Transcript of an exhibition interview**

> Interviewer: Your recording is about the school library, not your house. Why?
> Student: When I arrived, nobody could pronounce my name, and I felt invisible. The librarian asked me to teach her how to say it, and the next day she greeted me correctly. After that, I started helping at the library desk. I still miss my grandmother's kitchen, but I don't think belonging means choosing between two places.

'''
q(SA,"Selección múltiple","Which statement best expresses the central conflict of *Silent Streets*?",
 ["Mara wants to win the town's cycling race, but the new talking app keeps changing the route of the competition every day.","The council and Mara argue about the price of the new talking app for the town.","*The app is presented as a city for everyone, but it leaves out people who cannot use it, and Mara challenges this.","Mara's neighbour wants to move to another town because the streets are too noisy."],"c",
 "The council calls the app «a city for everyone», but it excludes deaf people and speakers of other languages; Mara challenges this with her own signs.","OA1")
q("","Alternativas — propósito y audiencia","Which option identifies the review's purpose and intended audience correctly?",
 ["*To evaluate and recommend the novel to readers aged fourteen and above interested in cities and inclusion.","To sell talking apps to councils and companies that want to replace all their old street signs with modern technology.","To explain to young children how to ride a bicycle safely in a city.","To report a real news event about a town that lost its street signs."],"a",
 "The review evaluates the novel («a valuable question») and ends by recommending it to readers aged fourteen and above interested in cities and inclusion.","OA1")
q("","Alternativas — tabla","Which option completes the table with relevant information from the review? Technology / Mara's discovery / Action she takes",
 ["A bicycle / the streets are dangerous / she stops cycling","A talking app / it is too expensive for the council to maintain / she writes a newspaper article against the council","Street signs / they are too colourful / she removes them","*A talking app / it excludes people who cannot hear it or speak English / she paints signs with words and pictures"],"d",
 "The technology is a talking app; Mara discovers that it excludes deaf people and speakers of other languages; her action is to paint signs with words and pictures and ask the council to keep them.","OA1")
q("","Alternativas — análisis de género","Which sentence is an **evaluation**, rather than plot information, that helps identify the text as a review?",
 ["\"Mara paints simple signs with words and pictures.\"","*\"Although the middle chapters move slowly, the novel asks a valuable question.\"","\"Every street sign in the town has been replaced by a talking app that guides people.\"","\"The council calls it a city for everyone.\""],"b",
 "Judging the middle chapters as slow and the question as valuable is an evaluation, typical of a review; the other sentences only report the plot.","OA1")
q("","Alternativas — interpretación","How do Mara's hand-painted signs connect to the residents who keep getting lost?",
 ["*They make visible the people that the talking app ignored.","They show that the residents do not want to live in the town.","They prove that the talking app works perfectly for everyone.","They are decorations that Mara paints only for a school project."],"a",
 "The signs, with words and pictures, include the residents the app left out (deaf people and speakers of other languages): they make them visible.","OA1")
q(SB,"Alternativas — localizar para actuar","You use sign language and would like to take part in the workshop. According to the notice, what can you do?",
 ["Bring a recording of your street so that the volunteers can listen to it","Arrive after 12 p.m., when the volunteers have more free time","*Contact the centre to ask for a sign language interpreter","Pay an extra fee for a special table near the entrance"],"c",
 "The notice says: «Contact the centre if you need a sign language interpreter.» No recording or fee is needed.","OA1")
q("","Selección múltiple","Which statement accurately compares how the two texts deal with community voices?",
 ["Both texts are fictional stories about a girl who paints street signs.","Text A is a real news report about a town, whereas Text B is a novel about languages in Scotland.","Both texts ask readers to record their neighbours without permission.","*Both value voices that are usually left out: A through a novel, B through a community workshop."],"d",
 "Text A reviews a novel about residents left out by an app; Text B invites people to map the languages of their street. Both value voices that are usually ignored.","OA1")
q("","Alternativas — organizador","Which option completes the planning table for Text B? Event date and time / Booking deadline / Participation cost / Permission rule",
 ["5 August, 10 a.m. / 9 August / a small fee / words are displayed automatically","9 August, 2–4 p.m. / 15 July / free / nobody can remove their words","*9 August, 10 a.m.–12 p.m. / 5 August / free / permission is asked before displaying words","9 August, 10 a.m.–12 p.m. / 9 August / free / recordings are required"],"b",
 "The workshop is on 9 August from 10 a.m. to 12 p.m.; booking closes on 5 August; it is free; and permission is asked before displaying anybody's words.","OA1")
q(SC,"Alternativas — discurso indirecto","Ana said, \"I have measured the entrance.\" Which option reports the statement correctly?",
 ["*Ana said that she had measured the entrance.","Ana said that she has measure the entrance.","Ana said that I had measured the entrance.","Ana said she measures the entrance tomorrow."],"a",
 "In reported speech the present perfect (*have measured*) becomes the past perfect (*had measured*), and *I* becomes *she*.","OA3")
q("","Selección múltiple","The hall's entrance has two steps and no handrail; the club has not investigated why. Which sentence expresses a **possible** explanation?",
 ["The hall was certainly built by people who hate the theatre club.","The entrance has steps because the club asked for them last year.","*The hall might have been built before accessibility rules existed.","The steps must disappear if the club buys new stage lights."],"c",
 "*Might have been built* expresses a possibility about the past, without claiming it as a fact, which is appropriate because the club has not investigated the cause.","OA3")
q("","Alternativas — estructura","Which option identifies the recommendation and a supporting reason in Text C?",
 ["Recommendation: buy stage lights first. Reason: Tomás believes brighter shows will attract more people to the hall.","Recommendation: stop performing. Reason: the hall has two steps.","Recommendation: sell more tickets. Reason: the budget is small.","*Recommendation: buy a portable ramp first. Reason: two families said a relative in a wheelchair could not attend."],"d",
 "The text recommends «buying a portable ramp first», supported by the families' messages about a relative who uses a wheelchair and could not attend.","OA3")
q("","Alternativas — tabla","Which option completes the table? Number of purchases this year / Competing purchase / Evidence from the audience / Proposed way to evaluate",
 ["Two / a new stage / Tomás's opinion / count ticket sales","*One / stage lights / two families' messages / ask the audience to test the access","One / a portable ramp / Ana's measurements of the steps / ask the council for advice","Three / costumes / ticket sales / buy the lights later"],"b",
 "The club can make one purchase; the competing option is stage lights; the evidence comes from two families' messages; and the proposal is to ask the audience to test the access.","OA3")
q("","Alternativas — articulación","Which sentence combines the ideas with *although*, keeping the contrast and meaning? \"Stage lights may attract audiences. A ramp lets everyone enter the hall.\"",
 ["*Although stage lights may attract audiences, a ramp lets everyone enter the hall.","Although a ramp lets everyone enter, stage lights never attract any audience.","Although stage lights attract audiences, so a ramp is not needed.","Although stage lights may attract audiences, because a ramp is expensive."],"a",
 "*Although* introduces the concession (lights may attract audiences) and the main clause keeps the contrasting idea (a ramp lets everyone enter).","OA3")
q("","Alternativas — crítica","What does the proposal NOT establish?",
 ["That the hall's entrance has two steps","That two families wrote to the club","*That a ramp will increase ticket sales","That the club has a small budget"],"c",
 "The text itself admits: «This proposal does not prove that a ramp will increase ticket sales.» The other facts are stated in the proposal.","OA3")
q("","Selección múltiple","Which outline matches the proposal's structure?",
 ["Recommendation → the history of theatre → a poem → a joke","Ticket prices → the director's biography → a list of costumes → the date of the next show","Evidence → conclusion → problem → nothing about limitations","*Context and problem → competing proposal → evidence → recommendation and evaluation → limitation"],"d",
 "The proposal presents the context and problem, the competing idea (lights), the families' evidence, the recommendation with a way to evaluate it and, finally, its limitation.","OA3")
q("","Alternativas — propuesta escrita","Which proposal includes a recommendation, evidence from C, a limitation and a next step, and uses reported speech and a passive?",
 ["We want lights. Lights are nice. Buy lights now.","*Ana said that the entrance had two steps. Because two families wrote that a relative could not attend, a ramp should be bought first. It may not increase sales, so the access will be tested at the next show.","Tomás said that he had bought new stage lights. Because they are bright, more people will come to the shows. The lights were installed yesterday, so nothing else needs to be done this year.","Ana says the hall is big. We recommend nothing until next year."],"b",
 "This option reports Ana's words (*said that… had*), uses passives (*should be bought*, *will be tested*), gives evidence (the families), a limitation (it may not increase sales) and a next step (testing the access).","OA3")
q(SD,"Selección múltiple","Which sentence best represents the student's understanding of belonging in Text E?",
 ["*Belonging can grow when others recognise you, without forgetting where you come from.","Belonging means forgetting your old home and your first language as quickly as possible.","Belonging only depends on living in a big house in the city.","Belonging is impossible for people who move to a new place."],"a",
 "The student felt recognised when the librarian learned her name, and says that belonging does not mean choosing between two places: it grows through recognition, without forgetting her origins.","OA4")
q("","Alternativas — léxico en contexto","Which caption uses *\"sense of belonging\"* correctly with a concrete detail from Text E?",
 ["My sense of belonging is a kind of library book with a red cover.","The library has a sense of belonging of twenty tables.","*My sense of belonging grew when the librarian learned to say my name.","I lost my sense of belonging at the football pitch yesterday."],"c",
 "*Sense of belonging* means the feeling of being part of a place or group; the caption connects it to a concrete detail from E: the librarian learning to say the student's name.","OA4")
q("","Alternativas — síntesis","Which option correctly explains a shared idea in D and E and attributes each source?",
 ["Both texts say that moving is always a happy experience for everyone.","Text D says the library is the only place to belong; Text E disagrees.","Both texts claim that every student who moves misses their grandmother's kitchen, and that libraries are the only places where students can belong.","*Text D says moving can mean opportunities or loss; Text E shows both, as the student belongs at the library but misses her grandmother's kitchen."],"d",
 "D states that some contributors talk about opportunities and others about what they miss; E shows both feelings in one person. The answer attributes each idea to its source.","OA4")
q("","Alternativas — comprensión y precisión","Which caption is faithful to Text E?",
 ["The student hated the library until the end of the year.","*The librarian learned to pronounce the student's name, and later the student helped at the library desk.","The student's grandmother worked as the school librarian.","The student taught the librarian to cook, and she no longer misses anything at all about her old home."],"b",
 "Text E says the librarian learned to say the student's name and that the student later helped at the library desk; the other captions contradict or invent details.","OA4")
q("","Alternativas — adaptar registro","Which email is polite and appropriately formal for the exhibition organisers?",
 ["*Dear organisers, I would like to contribute a recording to \"Voices of Home\". Could you tell me how long it should be? Kind regards, Camila","Hey guys!!! Put my audio in your thing now, ok? Bye","Organisers. Recording. Send me the rules immediately.","Hey organisers!!! I want my audio in your show, so just put it in and text me whenever you want, I don't care about the rules, ok? Bye bye"],"a",
 "The email greets formally (*Dear organisers*), uses a polite request (*Could you tell me…?*) and closes appropriately (*Kind regards*).","OA4")
q("","Alternativas — perspectiva personal","Which answer clearly explains whether an **activity**, rather than a place, could provide belonging, with an example linked to E?",
 ["No: activities are boring, and places like a house are always better than activities, because they never change.","I like libraries because they have many books and big windows.","*Yes: helping at the library desk gave the student a role, so an activity like volunteering can create belonging too.","No, because nobody can feel they belong anywhere after moving."],"c",
 "The answer takes a position (yes), explains it (an activity gives a role) and links it to E (the student helping at the library desk).","OA4")
q("","Selección múltiple","Which conclusion avoids generalising beyond the two sources?",
 ["All students who move to a new city feel invisible for exactly one day and then belong.","Every library in the world helps people feel at home.","Moving always means losing your culture forever.","*In these texts, small acts of recognition helped at least one student feel she belonged."],"d",
 "The conclusion limits itself to what the texts show (*in these texts*, *at least one student*) and does not generalise to all students or all libraries.","OA4")
q("","Alternativas — oración y perspectiva","A contributor says, \"The librarian welcomed me at the library.\" Which sentence uses the passive **and** a relative clause correctly?",
 ["The librarian was welcomed me, who learned my name.","*I was welcomed by the librarian, who learned to say my name.","I welcomed by the librarian which learn my name.","The librarian who welcomed was me at the library."],"b",
 "*I was welcomed by the librarian* is a correct passive, and *who learned to say my name* is a relative clause about a person.","OA4")
q("","Alternativas — reflexión de cierre","Which reflection for \"Voices of Home\" introduces a place, explains its effect on identity, connects to BOTH D and E, and ends with a question?",
 ["My place is a park. Parks are green. The end.","My place is the bus terminal, because I arrived there. Buses are big and noisy, and the terminal has many shops and a big clock. I go there sometimes with my cousins on Saturdays in summer.","Libraries are important for students because they have computers.","*My place is the community market, where a stallholder taught me local words. Like the student in E, I felt recognised, and, as D says, moving brought both gains and loss. Which place made you feel at home?"],"d",
 "This reflection names a place (the market), explains its effect (feeling recognised), connects to E (recognition) and to D (gains and loss) and closes with a question.","OA4")
armar(C/'ingles-examen-forma-b.md', C/'ingles-examen-forma-a.md', Q,
  fila=lambda i,p,cl: f"| {i} | {cl}. {p.explicacion} | {p.oa} |",
  reemplazos={"— Forma B":"— Forma A","FORMA B":"FORMA A","textos e ítems nuevos para esta Forma B":"textos e ítems nuevos para esta Forma A, distintos de la Forma B","ultima_actualizacion: 2026-11-01":"ultima_actualizacion: 2026-11-17"},
  inicio_preguntas="## OA N°1")
if __name__=="__main__":
    from collections import Counter; print(Counter(p.letra for p in Q), len(Q))
