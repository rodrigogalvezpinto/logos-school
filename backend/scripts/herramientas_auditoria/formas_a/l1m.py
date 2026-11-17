import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from forma_a import P, armar  # noqa: E402
C=Path(__file__).resolve().parents[4]/'contenido'/'01-medio/examenes'
A="**{n}. (Alternativas)** "
Q=[]
def q(sec,en,ops,l,ex,oa,cab=A): Q.append(P(sec,cab,en,ops,l,ex,oa))
def vf(sec,en,v,ex,oa): Q.append(P(sec,"**{n}. (Verdadero o Falso)** ",en,[],"V" if v else "F",ex,oa,{"clave":"Verdadero" if v else "Falso"}))
T1='''## Texto 1 (para las preguntas 1 a 5): "La brújula de Punta Ángeles" (fragmento)

> Valparaíso, invierno de 1998.
>
> Florencia tenía quince años y llevaba tres días con un sobre de la Armada escondido en su mochila. Lo había encontrado sobre la mesa de la cocina, abierto: el faro de Punta Ángeles sería automatizado en marzo y ya no necesitaría guardián. Su abuelo Ernesto, que lo cuidaba desde hacía treinta y dos años, todavía no lo sabía.
>
> —No le digas nada hasta después de su cumpleaños —le pidió su madre en voz baja—. Que tenga una última fiesta tranquila.
>
> Florencia asintió, pero cada tarde, cuando subía con su abuelo los ochenta y cuatro escalones de la torre, sentía que la mentira pesaba más que el sobre. Él le enseñaba a limpiar el lente y a leer la brújula de bronce que había sido de su propio padre, un marino de Ancud.
>
> —Fíjate: el barco gira para todos lados, pero la aguja sigue apuntando al norte —le decía—. Así hay que ser en la vida, Flor.
>
> Esa misma semana, el abuelo le contó la historia del Caleuche, el buque fantasma que navega iluminado de noche. «Dicen en Chiloé que se lleva a los que abandonan su puesto en el mar», murmuró, mirando el horizonte, como si hablara de sí mismo. Florencia pensó en el sobre y no pudo dormir.

'''
q(T1,"¿Cuál es el conflicto central del fragmento?",
 ["*El dilema de Florencia entre guardar el secreto que le pidió su madre o contarle la verdad a su abuelo","La disputa entre el abuelo Ernesto y la Armada por el sueldo que se le debe como guardián del faro","El miedo de Florencia a subir los ochenta y cuatro escalones de la torre durante las noches de invierno","La pelea entre la madre y el abuelo por la herencia de la brújula de bronce del bisabuelo marino"],"a",
 "Florencia debe elegir entre guardar el secreto que le pidió su madre y contarle la verdad al abuelo: ese dilema organiza el fragmento («sentía que la mentira pesaba más que el sobre»).","OA N°3 — conflicto central")
q("","¿A qué **personaje tipo** corresponde el abuelo Ernesto cuando le enseña a Florencia a leer la brújula y le explica su sentido?",
 ["El pícaro, que engaña a los demás para sacar provecho","El antagonista, que se opone a los deseos de la protagonista","*El sabio o mentor, que transmite experiencia y valores","El villano, que causa el problema central del relato"],"c",
 "Al enseñarle el oficio y explicarle el sentido de la brújula («Así hay que ser en la vida»), el abuelo transmite experiencia y valores: cumple el papel del sabio o mentor.","OA N°3 — personaje tipo")
vf("","\"El narrador del fragmento conoce y comunica tanto los pensamientos de Florencia como lo que el abuelo sabe en secreto sobre el cierre del faro.\"",False,
 "Falso. El narrador en tercera persona accede a la interioridad de Florencia (su culpa, su insomnio), pero no a la del abuelo: el texto dice que él «todavía no lo sabía», y su frase sobre el Caleuche solo se presenta «como si» hablara de sí mismo.","OA N°3 — tipo de narrador")
q("","¿Por qué la brújula de bronce, cuya aguja «sigue apuntando al norte» aunque el barco gire, puede considerarse un **símbolo** en el relato?",
 ["Porque es el objeto más valioso de la familia y Florencia teme que la Armada se lo lleve junto con el faro","*Porque representa la firmeza y la honestidad que el abuelo enseña, lo que agrava el dilema de Florencia al ocultarle la verdad","Porque solo sirve para orientarse en el mar y el relato la menciona para describir el trabajo diario del guardián","Porque se rompe al final del relato, cuando Florencia decide contarle a su abuelo que el faro será automatizado"],"b",
 "La aguja que no cambia de rumbo representa la firmeza y la honestidad («Así hay que ser en la vida»); por eso el secreto que guarda Florencia choca con lo que su abuelo le enseña.","OA N°3 — símbolo")
q("","¿Qué función cumple en el fragmento la historia del Caleuche que cuenta el abuelo?",
 ["Es un dato decorativo sobre Chiloé, sin relación con el conflicto ni con lo que siente ninguno de los personajes","Anuncia que el abuelo morirá en el mar, porque el Caleuche aparece en todos los relatos sobre faros chilenos","Demuestra que el abuelo ya sabe del cierre del faro y que su nieta le está mintiendo por orden de la madre","*Conecta el relato con la tradición oral chilota y refleja el temor del abuelo a «abandonar su puesto», que es justo lo que le espera"],"d",
 "La leyenda del Caleuche vincula el relato con la tradición oral chilota y anticipa el conflicto: el abuelo teme «abandonar su puesto», y eso es lo que el sobre de la Armada le impondrá.","OA N°3 — intertextualidad y visión de mundo")
T2='''## Texto 2 (para las preguntas 6 a 9): "La última función" (fragmento de obra teatral)

> **Personajes**: RAMÓN (64 años, titiritero), CAMILA (16 años, su sobrina), SEÑOR VALDÉS (dueño de un antiguo cine de barrio).
> **Escenario**: la sala vacía de un cine de barrio en Concepción, una tarde de lluvia. Sobre el escenario hay un pequeño teatrino de madera y un títere de pelo blanco, Don Pancho.
>
> *(La lluvia golpea el techo de zinc. RAMÓN pinta la nariz del títere con mucho cuidado. CAMILA entra con el celular en la mano.)*
>
> **CAMILA**: Tío, mire: si grabamos las funciones y las subimos a internet, las podrían ver miles de niños. Aquí vienen siete, con suerte.
>
> **RAMÓN**: *(sin levantar la vista)* Don Pancho no sabe hablarle a una pantalla, Camila. Necesita ver las caras.
>
> *(Entra el SEÑOR VALDÉS, sacudiendo un paraguas.)*
>
> **VALDÉS**: Ramón, firmé la venta. En un mes el cine se convierte en estacionamiento. Esta es la última función.
>
> *(Silencio. La gotera del techo empieza a caer sobre el teatrino. La luz del proyector parpadea.)*
>
> **RAMÓN**: *(después de un rato, le pasa el títere a CAMILA)* Tome. Usted sabrá cómo hacer que siga hablando.
>
> *(CAMILA sostiene a Don Pancho. La lluvia arrecia. Oscuro lento.)*

'''
q(T2,"¿Cuál es el conflicto principal de la escena?",
 ["La rivalidad entre Ramón y el señor Valdés por quién es el verdadero dueño del teatrino de madera","El enojo de Camila porque su tío no le permite ensayar con los títeres en la sala del cine","*La tensión entre seguir con las funciones presenciales que Ramón ama o adaptarse a un mundo que las deja sin lugar","La preocupación de Ramón porque la lluvia moje la pintura de Don Pancho antes de que empiece la función"],"c",
 "Ramón defiende las funciones presenciales («Necesita ver las caras»), pero la venta del cine y la propuesta de Camila muestran un mundo que ya no les da lugar: esa tensión organiza la escena.","OA N°5 — conflicto")
q("","¿Qué objeto de la escena funciona como **símbolo** del oficio y de la tradición que Ramón ha mantenido?",
 ["*El títere Don Pancho","El paraguas de Valdés","El celular de Camila","El techo de zinc"],"a",
 "El títere Don Pancho, que Ramón cuida y finalmente entrega, representa su oficio de titiritero y la tradición que debe seguir viva.","OA N°5 — símbolo")
q("","¿Qué efecto producen las acotaciones de la gotera que cae sobre el teatrino y la luz del proyector que parpadea?",
 ["Indican que la función se suspende por un problema eléctrico, sin relación con lo que sienten los personajes","Muestran que el cine está en perfecto estado y que la venta anunciada por Valdés es solo una broma","Describen el clima de Concepción para que el público sepa en qué estación del año ocurre la obra","*Refuerzan visualmente el deterioro y el final del cine, intensificando la pérdida sin que los personajes la nombren"],"d",
 "La gotera sobre el teatrino y la luz que parpadea muestran, sin palabras, el deterioro y el final del cine: la puesta en escena intensifica la pérdida que los personajes callan.","OA N°5 — puesta en escena y acotaciones")
q("","¿Qué revela el gesto final de Ramón al entregarle el títere a Camila?",
 ["Que se rinde por enojo y ya no quiere saber nada de los títeres ni de su sobrina","*Que acepta el cambio y confía en que su sobrina encuentre otra forma de mantener vivo el oficio","Que prefiere vender el títere a Valdés antes de que el cine se convierta en estacionamiento","Que nunca le importaron las funciones y solo esperaba una excusa para dejar de trabajar"],"b",
 "Al decir «Usted sabrá cómo hacer que siga hablando», Ramón acepta el cambio y confía en que Camila mantenga vivo el oficio con sus propios medios.","OA N°5 — personajes y motivaciones")
T3='''## Texto 3 (para las preguntas 10 a 13): "Desierto sin flores" (microcuento)

> Mi madre me contaba que la añañuca florece donde una muchacha de Monte Patria esperó en vano a su amado, un minero que se perdió buscando una veta de oro en el desierto. Cada vez que llovía, decía ella, la muchacha volvía convertida en flor roja para seguir esperando. Por eso, en los años de lluvia, el desierto se cubría de añañucas.
>
> Hoy leo que los científicos registran años seguidos de sequía en el Norte Chico y que el desierto florido aparece cada vez menos. Mi hija me pregunta por qué no hay flores este septiembre. Le cuento la leyenda y agrego, sin saber bien por qué, que quizás la muchacha se cansó de esperar una lluvia que ya no llega.

'''
q(T3,"¿Con qué relato tradicional dialoga el microcuento?",
 ["El mito de la Pincoya, ligado al mar de Chiloé","*La leyenda de la añañuca, propia del Norte Chico","La leyenda del Caleuche, el buque fantasma del sur","El mito del Trauco, de los bosques de Chiloé"],"b",
 "El microcuento recrea la leyenda de la añañuca: la muchacha de Monte Patria que, convertida en flor roja, sigue esperando a su amado minero cuando llueve en el Norte Chico.","OA N°8 — relación intertextual con un relato tradicional")
vf("","\"El narrador relaciona la leyenda con un problema actual sin que la explicación científica anule el valor del relato tradicional.\"",True,
 "Verdadero. El narrador pone en diálogo la sequía que registran los científicos con la leyenda: la cuenta a su hija y la actualiza («quizás la muchacha se cansó de esperar»), sin descartarla.","OA N°8 — interpretación de la visión de mundo")
q("","¿Qué problema de la realidad chilena aparece de fondo en el microcuento?",
 ["El abandono de las minas de oro en el desierto de Atacama","La contaminación de los ríos por la actividad minera","*La sequía prolongada del Norte Chico y su efecto en la naturaleza","El aumento de turistas que visitan el desierto florido cada año"],"c",
 "El texto menciona «años seguidos de sequía en el Norte Chico» y que el desierto florido aparece cada vez menos: ese es el problema actual de fondo.","OA N°8 — contexto de producción y problema actual")
q("","¿Qué interpretación del microcuento está mejor fundamentada en el texto?",
 ["El texto critica a la madre por contar leyendas falsas en vez de explicar a su hija las causas científicas de la sequía","El texto sostiene que las leyendas son más verdaderas que la ciencia, como muestra que el narrador no cree en los datos","El texto relata la historia de amor de un minero, y la sequía aparece solo como un dato sin importancia para el sentido","*El texto usa la leyenda para expresar la pérdida que causa la sequía, como muestra la frase «la muchacha se cansó de esperar una lluvia que ya no llega»"],"d",
 "La interpretación mejor fundamentada cita el texto: la frase final expresa con el lenguaje de la leyenda la pérdida que la sequía provoca, sin rechazar los datos científicos.","OA N°8 — interpretación con evidencia del texto")
T4='''## Texto 4 (para las preguntas 14 a 17): columna de opinión "El celular en el recreo"

> Desde que varios colegios decidieron que los estudiantes deben guardar el celular durante las clases, los profesores cuentan que las salas están más tranquilas. Hasta ahí, la medida parece razonable. El problema empieza cuando algunos establecimientos extienden la prohibición también a los recreos.
>
> Una encuesta aplicada a 800 estudiantes de una comuna de la Región de Valparaíso mostró que el 61 % reconoce distraerse con las notificaciones durante las clases. El dato respalda guardar el celular en la sala, pero no dice nada sobre lo que ocurre en el patio.
>
> Prohibir el celular en el recreo porque distrae en clases es como prohibir la pelota en el patio porque alguien rompió un vidrio de la sala. ¿No sería mejor enseñar a usarlo en el momento adecuado? Guardar el teléfono mientras se aprende es sensato; quitarlo también en el tiempo libre es una medida desproporcionada.

'''
q(T4,"¿Cuál es la tesis de la columna?",
 ["*Guardar el celular en clases es razonable, pero prohibirlo también en los recreos es una medida desproporcionada","Los celulares deben prohibirse en todo el colegio, porque el 61 % de los estudiantes se distrae con ellos","Los profesores deberían usar más el celular en sus clases para mantener la atención de los estudiantes","Los recreos deberían eliminarse, porque es el momento en que los estudiantes más usan el teléfono"],"a",
 "La autora acepta guardar el celular en clases, pero sostiene que prohibirlo en el recreo es una medida desproporcionada: esa es la tesis, que se repite en el cierre.","OA N°9 — tesis")
q("","¿Qué función cumple la comparación con «prohibir la pelota en el patio porque alguien rompió un vidrio»?",
 ["Informar sobre los daños que causan los juegos de pelota en los patios de los colegios de la región","Demostrar con un dato estadístico que la pelota distrae más que el celular durante los recreos","Cambiar de tema para hablar de la infraestructura escolar y de la seguridad de las ventanas","*Mostrar, mediante una analogía, que la prohibición castiga un uso legítimo por un problema que ocurre en otro momento"],"d",
 "Es una analogía: así como no se prohíbe la pelota por un vidrio roto en la sala, no tendría sentido prohibir el celular en el recreo por la distracción en clases.","OA N°9 — recursos argumentativos")
q("","¿Cómo se evalúa mejor el dato de la encuesta (61 % de 800 estudiantes) como evidencia de la tesis?",
 ["Es suficiente para probar toda la tesis, porque 800 estudiantes representan a todos los colegios de Chile","*Es pertinente para la primera parte de la tesis, pero es limitado: es de una sola comuna y no informa sobre los recreos","No tiene ninguna relación con la tesis, porque habla de notificaciones y no de celulares en la sala de clases","Es falso, porque la columna no indica el nombre de la persona que respondió cada pregunta de la encuesta"],"b",
 "El dato apoya guardar el celular en clases, pero es limitado: proviene de una sola comuna, es autoinformado y, como dice la propia columna, no dice nada sobre el recreo.","OA N°9 — suficiencia y pertinencia de la evidencia")
q("","¿Qué respuesta de un lector expresa una **postura propia fundamentada** frente a la columna?",
 ["\"Estoy de acuerdo con todo, porque la columna lo dice claramente y la autora seguramente sabe mucho del tema.\"","\"No me gustó la columna, porque es muy larga, tiene palabras difíciles y es aburrida para leerla en el celular.\"","*\"Creo que el recreo sin celular puede ser bueno si el colegio ofrece otras actividades, porque así se juega y se conversa más.\"","\"La columna está bien, porque todos los estudiantes del país usan el celular en el recreo y eso no va a cambiar.\""],"c",
 "Una postura fundamentada aporta una razón propia y verificable («si el colegio ofrece otras actividades»), no solo repite a la autora ni opina sobre la forma del texto.","OA N°9 — postura personal fundamentada")
T5='''## Texto 5 (para las preguntas 18 a 21): "Buses eléctricos en el recorrido 405"

**Texto A — Comunicado de la empresa de transporte**

> **Llegan los buses eléctricos al recorrido 405**
> Desde este lunes, el recorrido 405 opera con 20 buses eléctricos nuevos, que dejarán de emitir 1.200 toneladas de CO₂ al año. «Somos una empresa comprometida con el futuro de nuestros vecinos», declaró el gerente general. El comunicado incluye una fotografía del gerente sonriendo junto a un bus reluciente, rodeado de niños con globos verdes.

**Texto B — Video de una vecina en una red social**

> "Muy lindos los buses nuevos, silenciosos y con aire acondicionado 😊 El detalle: hoy esperé 40 minutos en el paradero, porque ahora pasan la mitad de buses que antes. ¿Me llevo una carpa para la próxima? 🙃 #405"

'''
q(T5,"Además de informar, ¿qué propósito tiene el Texto A?",
 ["*Proyectar una imagen positiva y comprometida de la empresa a partir de los buses nuevos","Denunciar que los buses eléctricos contaminan más que los buses diésel que había antes","Explicar a los vecinos cómo funciona y cómo se carga el motor de un bus eléctrico","Pedir disculpas a los vecinos por la baja frecuencia del recorrido 405 en hora punta"],"a",
 "Aunque parece informativo, el comunicado busca proyectar una imagen positiva de la empresa («Somos una empresa comprometida»), con cifras de CO₂ y una fotografía amable.","OA N°10 — propósito implícito")
q("","¿Qué permite concluir la comparación entre el Texto A y el Texto B?",
 ["Que el Texto A es completamente falso y el Texto B dice toda la verdad sobre el recorrido","Que los dos textos dicen exactamente lo mismo, aunque uno sea más formal que el otro","Que las redes sociales nunca deben usarse como fuente para informarse sobre la ciudad","*Que cada fuente destaca aspectos distintos de un mismo hecho según su interés, sin que una sea totalmente falsa"],"d",
 "La empresa destaca el beneficio ambiental y la vecina, la baja frecuencia: cada fuente selecciona lo que le interesa. Ninguna es totalmente falsa; juntas dan una imagen más completa del hecho.","OA N°10 — contraste de fuentes")
q("","¿Qué efecto busca la fotografía descrita en el Texto A?",
 ["Mostrar con exactitud cuántos pasajeros usan el recorrido 405 en las horas de mayor demanda","*Asociar la empresa con alegría y futuro, una imagen que puede ser más idealizada que el viaje diario","Probar con una imagen real que los buses nuevos pasan con mayor frecuencia que los antiguos","Informar a los vecinos el precio del pasaje en los buses eléctricos del recorrido nuevo"],"b",
 "El gerente sonriente, el bus reluciente y los niños con globos verdes asocian la empresa con alegría y futuro: es una imagen persuasiva que puede no reflejar la espera diaria en el paradero.","OA N°10 — recursos visuales de persuasión")
q("","¿Qué recursos de persuasión usa cada texto?",
 ["El A usa humor e ironía para criticar; el B, cifras exactas y la opinión de un experto","Ninguno de los dos textos usa recursos de persuasión, porque ambos solo informan hechos","*El A usa cifras y una cita institucional; el B, ironía y la experiencia personal de la vecina","Los dos textos usan solamente emojis y fotografías para convencer a quienes los leen"],"c",
 "El A apela al rigor con cifras (1.200 toneladas de CO₂) y la cita del gerente; el B usa la ironía («¿Me llevo una carpa?») y una experiencia directa, que también es una estrategia para convencer.","OA N°10 — recursos de persuasión")
T6='''## Sección de Escritura — Ensayo persuasivo (para las preguntas 22 a 25)

> Como escritor o escritora de 1° medio, debes ser capaz de escribir **ensayos persuasivos**: textos que presentan una hipótesis o afirmación clara, la sustentan con evidencia pertinente (literaria y no literaria), mantienen coherencia temática, cierran con una conclusión coherente, y usan citas y referencias para reconocer las ideas de otros.

'''
q(T6,"Una estudiante escribe un ensayo con la hipótesis «El liceo necesita más áreas verdes». Sus tres párrafos de desarrollo solo dicen «me gustan las plantas», «es más bonito» y «a todos les gustaría». ¿Qué debe mejorar?",
 ["*Sustentar la hipótesis con evidencia pertinente, como datos o estudios sobre los efectos de las áreas verdes","Cambiar la hipótesis por otra más difícil, porque un tema tan sencillo no sirve para un ensayo","Eliminar la conclusión, porque en un ensayo persuasivo basta con presentar la hipótesis","Escribir todos los párrafos en primera persona plural para que el lector se sienta incluido"],"a",
 "Las frases «me gustan las plantas» o «es más bonito» son opiniones sin respaldo: un ensayo persuasivo sustenta su hipótesis con evidencia pertinente, como datos o estudios.","OA N°14 — evidencia en el ensayo")
q("","¿Cuáles son formas correctas de incorporar las ideas de otros en un ensayo persuasivo? Marca todas las correctas.",
 ["Citar textualmente entre comillas e indicar quién lo dijo","Copiar un párrafo de internet sin comillas, como si fuera propio","Parafrasear la idea con palabras propias e indicar la fuente","Mencionar el medio y el año en que se publicó la información"],"acd",
 "Citar entre comillas, parafrasear con la fuente e indicar el medio y el año reconocen al autor y permiten verificar; copiar sin comillas es plagio.","OA N°14 — citas y referencias",cab="**{n}. (Varias correctas)** ")
q("","¿Qué opción presenta una planificación adecuada para un ensayo persuasivo sobre el uso del celular en el colegio?",
 ["Hipótesis: ninguna, porque en un ensayo basta con contar la propia experiencia. Evidencia: lo que hago con mi teléfono en el recreo y en la casa","*Hipótesis: el celular debe guardarse en clases, pero no prohibirse en los recreos. Evidencia: el dato del 61 % de la columna, aclarando que es de una sola comuna","Hipótesis: los celulares no existen en los liceos chilenos. Evidencia: el microcuento de la añañuca, una anécdota familiar y lo que dicen mis amigos","Escribir el ensayo sin hipótesis y decidir la postura al final, según cómo haya quedado el texto, agregando evidencia si sobra espacio"],"b",
 "Una buena planificación parte de una hipótesis clara y usa evidencia pertinente reconociendo sus límites: el dato del 61 % con la aclaración de que es de una sola comuna.","OA N°14 — planificación del ensayo")
q("","¿Qué par de párrafos (introducción y conclusión) cumple lo pedido para un ensayo persuasivo sobre el celular en el colegio?",
 ["Introducción: «Hoy los celulares son aparatos muy modernos que tienen muchísimas funciones distintas.» Conclusión: «Por eso, los celulares deberían ser más baratos para que todas las familias puedan tener uno.»","Introducción: «Prohibir el celular en todo el colegio es la única solución.» Conclusión: «Por eso, el celular nunca debería prohibirse en ningún momento del día escolar.»","Solo una conclusión, sin introducción: «En conclusión, el celular tiene cosas buenas y cosas malas, y cada estudiante sabrá qué hacer con el suyo en el colegio.»","*Introducción: «Guardar el celular en clases ayuda a concentrarse, pero prohibirlo en el recreo va demasiado lejos.» Conclusión: «Por eso, la regla debe limitarse a las clases, como muestran los argumentos revisados.»"],"d",
 "La introducción presenta una hipótesis clara y la conclusión la retoma de forma coherente; las otras opciones se desvían del tema, se contradicen o no tienen introducción.","OA N°14 — introducción y conclusión coherentes")
armar(C/'lengua-y-literatura-examen-forma-b.md', C/'lengua-y-literatura-examen-forma-a.md', Q,
  fila=lambda i,p,cl: f"| {i} | **{cl}.** {p.explicacion} | {p.oa} |",
  reemplazos={"— Forma B":"— Forma A","(Forma B)":"(Forma A)","última actualización: 2026-08-10":"última actualización: 2026-11-17",
    "Esta es la **Forma B**: una segunda versión del examen de práctica, con textos y preguntas distintos del banco de contenido":"Esta es la **Forma A**: una versión del examen de práctica con textos y preguntas propios, distintos de la Forma B y del banco de contenido"},
  inicio_preguntas="## Texto 1")
if __name__=="__main__":
    from collections import Counter; print(Counter(p.letra for p in Q), len(Q))
