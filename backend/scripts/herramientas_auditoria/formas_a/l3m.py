import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from forma_a import P, armar  # noqa: E402
C=Path(__file__).resolve().parents[4]/'contenido'/'03-medio/examenes'
A="**{n}. (Alternativas)** "
VC="**{n}. (Varias correctas)** "
Q=[]
def q(sec,en,ops,l,ex,oa,cab=A): Q.append(P(sec,cab,en,ops,l,ex,oa))
def vf(sec,en,v,ex,oa): Q.append(P(sec,"**{n}. (Verdadero o Falso)** ",en,[],"V" if v else "F",ex,oa,{"clave":"Verdadero" if v else "Falso"}))
T1='''## Texto 1 (para las preguntas 1 a 6): "La radio de mi abuelo" (fragmento de cuento)

> En Puerto Cisnes, a fines de los setenta, la radio de mi abuelo era la ventana por donde entraba el mundo. Él la atendía cada noche a las nueve: leía los mensajes que la gente le dejaba escritos en papelitos —«Para la familia Oyarzo, del canal Puyuhuapi: Rosa llegó bien a Coyhaique, el niño nació sano»— y los decía con una voz grave que, según mi abuela, hacía callar hasta a los lobos marinos.
>
> —¡Atención, sector Queulat! —gritaba, y se reía solo—. Si me están escuchando, prendan el farol, que esta noche viene temporal.
>
> Yo me sentaba en un cajón de manzanas a mirarlo. Nunca lo vi leer un libro, pero sabía de memoria el nombre de cada isla y de cada familia que vivía en ellas.
>
> Hoy, en el metro de Santiago, escucho pódcast con audífonos y nadie me nombra en voz alta. A veces, cuando el tren entra al túnel y se corta la señal, me sorprendo esperando que alguien diga mi nombre por la radio, como él decía el de todos.

'''
q(T1,"En la expresión «la radio de mi abuelo era la ventana por donde entraba el mundo», ¿qué figura literaria se reconoce?",
 ["Hipérbole: exagera el tamaño real del aparato de radio","*Metáfora: identifica la radio con una ventana que comunica con el mundo","Anáfora: repite la misma palabra al inicio de varias frases","Onomatopeya: imita el sonido que hacía la radio al encenderse"],"b",
 "Es una metáfora: la radio se identifica con una ventana, porque a través de ella las noticias del mundo llegaban a un pueblo aislado.","OA N°1 — figura literaria")
vf("","\"Para formular una hipótesis de sentido sobre 'La radio de mi abuelo' basta con resumir lo que ocurre en el fragmento, sin relacionarlo con sus recursos ni con su final.\"",False,
 "Falso. Una hipótesis de sentido propone qué significa el texto en su conjunto y se apoya en sus recursos (la metáfora, el contraste entre épocas, el final); resumir el argumento no basta.","OA N°1 — hipótesis de sentido")
q("","¿Cómo contribuye al sentido la combinación de la voz coloquial del abuelo («¡Atención, sector Queulat!») con la voz reflexiva del narrador adulto?",
 ["Muestra que el narrador se burla de la forma de hablar de su abuelo y de la gente del sur","Indica que el fragmento fue escrito por dos autores distintos que no se pusieron de acuerdo","*Contrasta la cercanía oral de la radio con la mirada nostálgica de quien recuerda ese mundo","Demuestra que el abuelo era locutor profesional y el narrador, un periodista de televisión"],"c",
 "La voz coloquial y alegre del abuelo trae al presente la cercanía de la radio; la voz reflexiva del narrador adulto la mira con nostalgia desde la distancia: el contraste construye el sentido.","OA N°1 — características del lenguaje")
q("","¿Por qué el narrador caracteriza al abuelo, sobre todo, por su voz y por su memoria de los nombres de cada familia?",
 ["*Porque su identidad está en su función de comunicar y de vincular a personas aisladas","Porque el abuelo no sabía leer y la radio era su único trabajo pagado en el pueblo","Porque el narrador nunca vio a su abuelo y solo conoce su voz por grabaciones","Porque en el sur de Chile todas las personas se conocen por sus nombres"],"a",
 "El abuelo no se describe por su aspecto, sino por su voz y por saber «el nombre de cada isla y de cada familia»: su identidad es la de quien comunica y une a una comunidad aislada.","OA N°1 — narrador y personajes")
q("","¿Qué relación con la novela *Ardiente paciencia*, de Antonio Skármeta (un cartero que lleva cartas a Pablo Neruda en Isla Negra), explica una semejanza y una diferencia?",
 ["No tienen ninguna relación, porque la novela trata solo de la política chilena y el cuento solo del clima del sur de Chile","Ambas cuentan la vida completa de Pablo Neruda; la diferencia es que el cuento ocurre en Puerto Cisnes y no en Isla Negra","Ambas son poemas escritos en verso; la diferencia es que la novela es bastante más corta que el cuento de la radio","*En ambas un medio de comunicación crea vínculos entre personas; en la novela son las cartas y la poesía, en el cuento la radio"],"d",
 "Es una relación intertextual temática: en las dos obras un medio de comunicación (las cartas y la poesía; la radio) crea lazos afectivos; difieren en el medio y en el contexto.","OA N°1 — relaciones intertextuales")
q("","Un compañero dice que el final del fragmento («en el metro de Santiago… esperando que alguien diga mi nombre por la radio») es solo un dato sobre dónde vive hoy el narrador. ¿Qué lectura es más adecuada?",
 ["El compañero tiene razón, porque los finales de los cuentos solo informan dónde viven los personajes cuando ya son adultos","*El final contrasta la comunicación anónima del presente con la comunidad que creaba la radio, y expresa la nostalgia de ser nombrado","El final muestra que el narrador odia el metro de Santiago y quiere volver a vivir en Puerto Cisnes de inmediato, sin su familia","El final anuncia que el narrador se convertirá pronto en locutor de radio en Santiago, igual que su abuelo en el sur"],"b",
 "El cierre no es un dato aislado: contrapone el anonimato del metro y los audífonos con la radio que nombraba a todos, y así expresa la nostalgia por una comunidad perdida.","OA N°1 — hipótesis de sentido y estructura")
T2='''## Texto 2 (para las preguntas 7 a 12): "Agua en camión: la otra cara de la sequía" (reportaje)

> En varias localidades rurales de la provincia de Petorca, el agua no sale de la llave: llega en camión aljibe dos veces por semana. Según el municipio, unas dos mil familias dependen de este abastecimiento.
>
> «Nos dejan cincuenta litros por persona al día. Con eso hay que cocinar, lavar y bañarse», cuenta Gladys Tapia, vecina de la zona, mientras llena baldes en el patio.
>
> Un vocero de una empresa agrícola del valle sostiene, en cambio, que «la empresa usa riego tecnificado y cumple con la ley». Expertos en recursos hídricos consultados para este reportaje explican que la escasez se debe a la combinación de la megasequía con la sobreexplotación de los acuíferos, y que el debate sobre el agua como derecho humano sigue abierto en el país.

'''
q(T2,"Un estudiante quiere saber si «Agua en camión» es un reportaje o una noticia breve. ¿Qué rasgo NO correspondería a un reportaje?",
 ["Reunir varias fuentes distintas, como vecinos, una empresa y expertos","Incluir testimonios directos y citados de las personas afectadas","*Informar en pocas líneas un hecho del día, sin contexto ni testimonios","Profundizar en las causas y en el contexto del problema que trata"],"c",
 "El reportaje profundiza: reúne fuentes, testimonios y contexto. Informar un hecho del día en pocas líneas, sin contexto, es propio de una noticia breve.","OA N°3 — género discursivo")
vf("","\"El reportaje presenta la versión de distintos actores: una vecina afectada, el municipio, una empresa agrícola y expertos en recursos hídricos.\"",True,
 "Verdadero. El texto cita a Gladys Tapia, al municipio, al vocero de una empresa agrícola y a expertos: contrasta varias voces sobre el mismo problema.","OA N°3 — razonamiento del discurso")
q("","¿Qué información del reportaje es verificable y cuál depende solo de lo que afirma una de las partes?",
 ["*Las familias abastecidas, atribuidas al municipio, se pueden verificar; que la empresa «cumple con la ley» es una afirmación de una de las partes","Todo el reportaje depende solo de la opinión de la periodista, porque no cita a ninguna fuente identificable ni entrega datos de ningún organismo","Las dos afirmaciones son igual de verificables, porque aparecen en el mismo reportaje y las dos fueron dichas por personas que viven en la zona","Ninguna información se puede verificar, porque los reportajes nunca entregan datos ni fuentes sobre los hechos que informan a sus lectores"],"a",
 "La cifra de familias se atribuye a una fuente institucional (el municipio) y puede contrastarse; la afirmación de que la empresa «cumple con la ley» es la versión de una de las partes.","OA N°3 — veracidad de la información")
q("","¿Por qué es relevante, para la audiencia chilena, que el reportaje mencione la megasequía y el debate sobre el agua como derecho humano?",
 ["Porque así el reportaje se vuelve más largo y parece más serio para los lectores","Porque el agua es un tema que solo interesa a los habitantes de la provincia de Petorca","Porque todos los reportajes deben terminar con una opinión del periodista sobre la ley","*Porque vincula el caso local con un problema nacional y con una discusión pública vigente"],"d",
 "Al mencionar la megasequía y el debate sobre el agua como derecho, el reportaje conecta el caso de Petorca con un problema nacional y con una discusión pública vigente en Chile.","OA N°3 — contexto sociocultural")
q("","¿Qué propósito cumple contrastar la declaración de la empresa («usa riego tecnificado») con el testimonio de Gladys Tapia («cincuenta litros por persona al día»)?",
 ["Demostrar que la empresa miente siempre y que la vecina dice toda la verdad sobre el agua","*Mostrar la tensión entre distintos usos del agua y que una declaración no basta para cerrar el problema","Explicar con detalle técnico cómo funciona el riego tecnificado en la agricultura del valle","Entretener al lector con dos historias distintas que no tienen ninguna relación entre sí"],"b",
 "El contraste muestra la tensión entre el uso agrícola y el consumo de las familias, y sugiere que la declaración de la empresa no resuelve la situación que vive la vecina.","OA N°3 — función de la información seleccionada")
q("","Si el reportaje se transformara en un reportaje audiovisual, ¿qué cambiaría y qué se mantendría?",
 ["*Cambiarían el lenguaje y los recursos (imágenes, sonido, entrevistas en cámara), pero se mantendrían el tema, las fuentes y el propósito","Cambiaría el tema, porque en video no se puede hablar de la sequía, pero se mantendría el texto escrito palabra por palabra","No cambiaría nada, porque un reportaje escrito y uno audiovisual usan exactamente los mismos recursos","Se mantendrían solo las imágenes, y se eliminarían los testimonios y los datos del municipio por ser aburridos"],"a",
 "Al cambiar de soporte cambian el lenguaje y los recursos (imagen, sonido, entrevistas en cámara), pero el tema, las fuentes y el propósito informativo se mantienen.","OA N°3 — género y contexto sociocultural")
T3='''## Texto 3 (para las preguntas 13 a 18): hilo de una red social sobre el cambio de nombre de una plaza

> **@vecina_del_sector**: Quieren cambiarle el nombre a la plaza Los Aromos. ¡Siempre se ha llamado así! Nadie nos preguntó.
>
> **@historiador_local**: Según las actas municipales de 1965, la plaza se llamó «Los Aromos» por los árboles que plantaron los primeros pobladores. Comparto la foto del acta para quien quiera revisarla.
>
> **@junta_vecinos_oficial**: Aclaramos: el cambio de nombre es solo una propuesta. Se hará una consulta ciudadana el 12 de mayo y publicaremos el resultado completo en esta cuenta.
>
> **@anonimo_99**: Los que defienden el nombre antiguo son unos ignorantes que no quieren el progreso.

'''
q(T3,"¿Qué rol asume @historiador_local en el hilo?",
 ["El de un vecino que se queja sin aportar información","El de una autoridad que decide el nombre de la plaza","*El de un especialista que aporta información histórica con su fuente","El de un usuario que insulta a quienes piensan distinto"],"c",
 "@historiador_local aporta un dato histórico y su fuente (las actas municipales de 1965, con la foto del acta): asume el rol de especialista que informa.","OA N°4 — rol del enunciador")
vf("","\"En Chile, los nombres de calles y plazas suelen recordar a personajes, hechos o rasgos de la historia local; por eso cambiarlos suele generar debate en la comunidad.\"",True,
 "Verdadero. Los nombres de los espacios públicos forman parte de la memoria local; por eso una propuesta de cambio suele abrir un debate en la comunidad.","OA N°4 — contexto sociocultural")
q("","¿Qué función cumple la intervención de @junta_vecinos_oficial?",
 ["Insultar a quienes se oponen al cambio de nombre de la plaza","Contar la historia de los primeros pobladores del barrio","Anunciar que el nombre de la plaza ya fue cambiado ayer","*Aclarar el procedimiento formal y corregir la idea de que nadie preguntará"],"d",
 "La junta aclara que se trata de una propuesta, que habrá una consulta ciudadana y que publicará el resultado: corrige la idea de que «nadie nos preguntó».","OA N°4 — rol del enunciador ante la audiencia")
q("","¿Qué modo de razonamiento usa @historiador_local para explicar el nombre de la plaza?",
 ["*Razona a partir de evidencia documental: las actas municipales de 1965","Razona por analogía, comparando la plaza con otra ciudad del país","Generaliza a partir de su experiencia personal en el barrio","Apela a las emociones de los vecinos, sin entregar ningún dato"],"a",
 "@historiador_local se apoya en un documento verificable (el acta de 1965) y ofrece revisarlo: razona a partir de evidencia documental.","OA N°4 — modos de razonamiento")
q("","¿Qué respuesta de la comunidad digital al comentario de @anonimo_99 está mejor fundamentada éticamente?",
 ["Responderle con insultos más fuertes, para que aprenda a respetar","*Responder con argumentos, sin descalificar, y pedir respeto por todas las opiniones","Compartir su perfil con datos personales para que todos lo critiquen","Ignorar todo el hilo y dejar de participar en los temas del barrio"],"b",
 "Ante una descalificación, lo fundamentado es responder con argumentos y pedir respeto, sin insultar ni exponer datos personales de nadie.","OA N°4 — postura ética fundamentada")
q("","Para formarse una opinión informada sobre el cambio de nombre, ¿qué evidencia es más sólida? Marca **todas** las correctas.",
 ["El acta municipal de 1965, citada con su fecha y su imagen","El resultado oficial de la consulta, que publicará la junta de vecinos","La frase «¡Siempre se ha llamado así!», sin ningún dato que la respalde","El comentario de @anonimo_99 sobre quienes defienden el nombre antiguo"],"ab",
 "Son sólidas las evidencias verificables: el acta de 1965 y el resultado oficial de la consulta. Una afirmación sin datos o una descalificación no son evidencia.","OA N°4 — calidad de la evidencia",cab=VC)
T4='''## Sección de Producción de Textos (para las preguntas 19 a 25)

> Como autor o autora de 3° medio, debes ser capaz de **comunicar tus análisis e interpretaciones** en textos coherentes y cohesionados, adecuados al género y a la audiencia. Las siguientes preguntas toman como referencia dos versiones de un mismo análisis sobre "La radio de mi abuelo" (Texto 1 de esta prueba): un párrafo para un ensayo escolar y una publicación para la cuenta de una biblioteca dirigida a estudiantes de 3° medio.
>
> *Versión (a) — párrafo analítico*: "El cuento 'La radio de mi abuelo' construye su sentido a partir del contraste entre dos formas de comunicarse. En primer lugar, la radio del abuelo nombraba a cada familia de las islas y creaba una comunidad. Luego, el final muestra al narrador en el metro, con audífonos, sin que nadie lo nombre. Por lo tanto, el relato expresa la nostalgia por una comunicación cercana que el presente no ha sabido reemplazar."
>
> *Versión (b) — publicación, con errores de cohesión*: "El cuento es de un abuelo con una radio. Después el nieto va en metro. Puerto Cisnes queda en Aysén. Se llamaba Queulat. Es buen cuento, léanlo."

'''
q(T4,"La estudiante debe transformar su párrafo analítico (versión a) en el guion de un video corto para la cuenta de la biblioteca. ¿Qué decisión es la más adecuada?",
 ["Leer el párrafo completo frente a la cámara, sin cambiar ninguna palabra","Eliminar la idea central y mostrar solo fotos del sur de Chile con música","*Mantener la idea central del contraste, con frases breves y apoyos visuales","Agregar opiniones sobre otros cuentos que no tienen relación con el análisis"],"c",
 "Adecuar al género y a la audiencia implica conservar la idea central (el contraste entre dos formas de comunicarse) y expresarla con frases breves y apoyos visuales propios del video.","OA N°6 — adecuación al género")
vf("","\"Para corregir la versión (b), bastaba con agregar emojis y hashtags, sin revisar la cohesión ni pensar en la audiencia.\"",False,
 "Falso. Corregir la versión (b) exige ordenar las ideas, conectarlas y eliminar los datos que no aportan (la región, el nombre del sector), pensando en la audiencia; los emojis no resuelven la falta de cohesión.","OA N°6 — proceso de escritura")
vf("","\"En el párrafo 'Las abejas polinizan muchos cultivos. Mi tía tiene un auto rojo. Por eso, cuidarlas protege nuestros alimentos', la oración 'Mi tía tiene un auto rojo' mantiene la progresión temática.\"",False,
 "Falso. Esa oración introduce un tema ajeno (el auto de la tía) y rompe la progresión: no se relaciona con las abejas ni con la conclusión sobre los alimentos.","OA N°6 — progresión temática")
q("","¿Qué planificación de un texto sobre el reportaje «Agua en camión» es coherente?",
 ["Propósito: entretener. Género: chiste. Tema: el clima de Santiago. Audiencia: no definida","Propósito: vender agua. Género: aviso. Tema: los camiones. Audiencia: empresas agrícolas","Propósito: ninguno. Género: cualquiera. Tema: la sequía. Audiencia: se define después","*Propósito: informar. Género: infografía. Tema: la sequía en Petorca. Audiencia: estudiantes de 3° medio"],"d",
 "Una planificación coherente define y relaciona propósito, género, tema y audiencia: informar, con una infografía, sobre la sequía en Petorca, a estudiantes de 3° medio.","OA N°6 — planificación: propósito, género, tema y audiencia")
q("","¿Por qué adecuar un texto a otra audiencia no significa necesariamente perder profundidad?",
 ["*Porque se pueden mantener la idea central y la evidencia, cambiando la extensión y el registro","Porque adecuar significa copiar el mismo texto sin cambios para todas las audiencias","Porque las audiencias jóvenes no entienden ideas profundas y hay que eliminarlas","Porque la profundidad depende solo de usar muchas palabras técnicas y difíciles"],"a",
 "Adecuar no es simplificar el contenido: la idea central y la evidencia pueden mantenerse, ajustando la extensión, el registro y los recursos a la nueva audiencia.","OA N°6 — adecuación al género y a la audiencia")
q("","¿Qué acciones corresponden a la etapa de **planificación** del proceso de escritura? Marca **todas** las correctas.",
 ["Definir el propósito del texto y su audiencia","Corregir la ortografía del texto ya terminado","Elegir el género más adecuado para el propósito","Ordenar las ideas principales en un esquema"],"acd",
 "Planificar es definir propósito y audiencia, elegir el género y ordenar las ideas antes de escribir; corregir la ortografía del texto terminado corresponde a la revisión.","OA N°6 — proceso de escritura: planificación",cab=VC)
q("","¿Cuál es la mejor corrección de «La radio conectaba a las islas. Hoy existen los celulares. Mucha gente se siente sola.»?",
 ["«La radio conectaba a las islas, hoy existen los celulares, mucha gente se siente sola.»","*«La radio conectaba a las islas. Hoy existen los celulares; sin embargo, mucha gente se siente sola.»","«La radio conectaba a las islas. Por lo tanto, hoy existen los celulares y la gente se siente sola.»","«La radio conectaba a las islas. Además, mucha gente tiene celular y además se siente sola.»"],"b",
 "«Sin embargo» marca el contraste entre la mayor conexión técnica (los celulares) y la soledad de muchas personas; «por lo tanto» indicaría una consecuencia que no corresponde.","OA N°6 — cohesión")
armar(C/'lengua-y-literatura-examen-forma-b.md', C/'lengua-y-literatura-examen-forma-a.md', Q,
  fila=lambda i,p,cl: f"| {i} | **{cl}.** {p.explicacion} | {p.oa} |",
  reemplazos={"(Forma B)":"(Forma A)","— Forma B":"— Forma A","última actualización: 2026-08-11":"última actualización: 2026-11-17",
    "*Segunda versión del examen de práctica de la asignatura,":"*Forma A del examen de práctica de la asignatura, distinta de la Forma B,",
    "Las preguntas y los textos de esta Forma B son propios":"Las preguntas y los textos de esta Forma A son propios",
    "(revisado el 2026-11-15 con `solapamiento_pruebas_guias.py`)":"(revisado el 2026-11-17 con `solapamiento_pruebas_guias.py` y las guardas de pytest)"},
  inicio_preguntas="## Texto 1")
if __name__=="__main__":
    from collections import Counter; print(Counter(p.letra for p in Q), len(Q))
