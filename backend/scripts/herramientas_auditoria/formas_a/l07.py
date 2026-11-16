import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from forma_a import P, armar  # noqa: E402
C=Path(__file__).resolve().parents[4]/'contenido'/'07-basico/examenes'
A="**{n}. (Alternativas)** "; VF="**{n}. (Verdadero o Falso)** "
Q=[]
def q(sec,en,ops,l,ex,oa,cab=A): Q.append(P(sec,cab,en,ops,l,ex,oa))
def vf(sec,en,v,ex,oa): Q.append(P(sec,VF,en,[],"V" if v else "F",ex,oa,{"clave":"Verdadero" if v else "Falso"}))
T1='''## Texto 1 (para las preguntas 1 a 5): "La segunda función"

> Detrás del telón, Ignacio escuchaba el murmullo del público que llenaba el gimnasio del liceo. Tenía las manos heladas y repetía en voz baja la primera frase de su personaje. Faltaban cinco minutos para que comenzara la obra de fin de año.
>
> Un año antes, en ese mismo escenario, le había tocado decir un poema en el acto de aniversario. Había avanzado hasta el centro, había mirado al público y su mente se había quedado completamente en blanco. Desde la tercera fila alguien soltó una carcajada, y después otra. Ignacio bajó del escenario sin decir una palabra y se encerró en el baño hasta que terminó el acto.
>
> Durante semanas evitó todo lo que tuviera que ver con hablar en público. Fue la profesora Marta, de Lenguaje, quien un día le ofreció un papel pequeño en el taller de teatro: "Solo una línea, Ignacio. Una sola. La segunda vez siempre es distinta", le dijo.
>
> —Ignacio, te toca —susurró ahora la profesora Marta, con una sonrisa tranquila.
>
> Él respiró hondo, salió a escena y, cuando abrió la boca, su voz sonó firme y clara, como si nunca se hubiera ido.

'''
q(T1,"¿Cuál es el conflicto central del texto?",
 ["El miedo de Ignacio a quedarse en blanco frente al público, como el año anterior","La pelea entre Ignacio y la profesora Marta por el papel que le tocó en la obra","La competencia entre dos liceos para presentar la mejor obra de teatro de fin de año","La decisión de Ignacio de abandonar el liceo para no volver a actuar nunca más"],"b",
 "El problema que mueve la historia es interno: Ignacio teme repetir lo que le pasó al decir el poema. Todo el relato gira en torno a si podrá enfrentar ese miedo.","OA N°3 — conflicto central")
q("","¿Qué rol cumple la profesora Marta en el desarrollo del conflicto?",
 ["Es quien se rió de Ignacio desde la tercera fila durante el acto de aniversario","Es quien le prohíbe a Ignacio volver a subir al escenario del liceo","Es quien lo ayuda a enfrentar su miedo dándole primero un papel pequeño","Es quien reemplaza a Ignacio en la obra porque no confía en él"],"c",
 "La profesora le ofrece «solo una línea» y lo acompaña tras bambalinas: con esas acciones permite que Ignacio enfrente su miedo poco a poco.","OA N°3 — efecto de las acciones de un personaje")
vf("","«El relato comienza con el episodio en que Ignacio se quedó en blanco y luego avanza en orden cronológico hasta la obra de fin de año.»",False,
 "El relato comienza en el presente (Ignacio detrás del telón), salta al pasado para contar lo que le pasó un año antes (flashback) y luego vuelve al presente.","OA N°3 — disposición temporal")
q("","¿Cuál de estos fragmentos corresponde a la **voz de un personaje** y no a la del narrador?",
 ["«Durante semanas evitó todo lo que tuviera que ver con hablar en público»","«Tenía las manos heladas y repetía en voz baja la primera frase»","«Detrás del telón, Ignacio escuchaba el murmullo del público»","*«Solo una línea, Ignacio. Una sola. La segunda vez siempre es distinta»"],"d",
 "Esas palabras las dice la profesora Marta, entre comillas y dirigidas a Ignacio: es la voz de un personaje. Los otros fragmentos son del narrador, que cuenta lo que hace y siente Ignacio.","OA N°3 — narrador versus personajes")
q("","¿Qué efecto produce el salto al pasado (flashback) en la construcción del conflicto?",
 ["*Explica por qué Ignacio está tan nervioso y aumenta la tensión antes de salir a escena","Hace que el lector olvide el miedo de Ignacio y se concentre solo en la obra","Muestra que lo ocurrido el año anterior no tiene relación con la obra actual","Elimina el suspenso, porque cuenta desde el principio cómo termina la obra"],"a",
 "Al conocer lo que le pasó un año antes, el lector comprende sus manos heladas y su nerviosismo, y espera con más tensión el momento en que sale a escena.","OA N°3 — análisis del tiempo narrativo")
T2='''## Texto 2 (para las preguntas 6 a 9): Poema "Invierno en la cordillera"

> La cordillera se pone su poncho blanco
> y mira en silencio la ciudad dormida;
> el humo de las estufas sube lento,
> oliendo a leña, a pan y a despedida.
>
> Susurra la sombra sobre la sierra,
> el frío muerde los dedos del río;
> el invierno es un viejo de manos grises
> que cuenta despacio los días de frío.

'''
q(T2,"¿A qué sentido apela principalmente la expresión «oliendo a leña, a pan y a despedida»?",
 ["Al oído","Al tacto","*Al olfato","Al gusto"],"c",
 "«Oliendo» apela al olfato: la imagen invita a imaginar el aroma de la leña y del pan en un día de invierno.","OA N°4 — lenguaje poético y sentidos")
q("","En los versos 1 y 2, la cordillera «se pone su poncho blanco» y «mira» la ciudad, como si fuera una persona. ¿Cómo se llama este recurso?",
 ["*Personificación","Hipérbole","Comparación","Onomatopeya"],"a",
 "La cordillera «se pone» un poncho y «mira», acciones propias de personas: es una personificación. No usa «como» ni imita sonidos.","OA N°4 — lenguaje figurado")
q("","¿Qué idea transmite la metáfora «el invierno es un viejo de manos grises / que cuenta despacio los días de frío»?",
 ["Que el invierno es una estación alegre y llena de energía","*Que el invierno se siente largo, lento y triste, como si no terminara nunca","Que en invierno las personas mayores salen más a la calle","Que el invierno dura exactamente lo mismo que las otras estaciones"],"b",
 "Un viejo que cuenta «despacio» los días sugiere que el tiempo pasa lento; las «manos grises» evocan el cielo nublado y el frío. El invierno se percibe largo y melancólico.","OA N°4 — interpretación de lenguaje figurado")
q("","¿Qué recurso de sonoridad hay en «Susurra la sombra sobre la sierra» y qué efecto produce?",
 ["Una rima consonante entre todas las palabras, que da un tono alegre","Una onomatopeya del ruido de un trueno, que crea un ambiente violento","Una enumeración de lugares, que describe un viaje por la montaña","*Una aliteración del sonido «s», que imita un susurro y crea un ambiente silencioso"],"d",
 "La repetición del sonido «s» (susurra, sombra, sobre, sierra) es una aliteración: suena como un susurro y refuerza la calma y el silencio del paisaje.","OA N°4 — ritmo y sonoridad")
T3='''## Texto 3 (para las preguntas 10 a 13): "Lo que cabe en una mochila"

> La madrugada del 2 de mayo de 2008, en Chaitén, Daniela despertó con un ruido sordo que hacía temblar las ventanas. Por la mañana, una columna gris se levantaba detrás de los cerros y la ceniza empezaba a cubrir los techos. Por la radio, las autoridades anunciaron que todo el pueblo debía evacuar por mar y que cada persona podía llevar solo una mochila.
>
> Daniela vivía con su abuela Tránsito, que tomaba remedios para el corazón todos los días. En el living estaban los álbumes con las fotos del abuelo, que había muerto hacía dos años. La abuela los miraba casi todas las tardes. En la mochila no cabían los álbumes y los remedios a la vez.
>
> Daniela guardó las cajas de remedios, la receta y una chaqueta para su abuela. Al cerrar la puerta, miró los álbumes por última vez.
>
> Semanas después, ya en Puerto Montt, supieron que el río había arrastrado barro y ceniza hasta muchas casas del pueblo. Un día, un vecino pescador les llevó una bolsa: había rescatado algunas fotos del abuelo, manchadas, pero todavía reconocibles. La abuela las tomó, las apretó contra el pecho y, mirando a Daniela, le dijo: "Lo importante lo trajiste tú".

'''
q(T3,"¿Cuál es el dilema principal que enfrenta Daniela en el relato?",
 ["*Elegir entre llevar los remedios de su abuela o los álbumes de fotos de su abuelo","Decidir si se queda en Chaitén o se va a vivir sola a Puerto Montt","Elegir entre ayudar al vecino pescador o cuidar a su abuela","Decidir si escucha la radio o sale a mirar la columna de ceniza"],"a",
 "Como solo puede llevar una mochila y no caben ambas cosas, Daniela debe escoger entre la salud de su abuela (los remedios) y los recuerdos familiares (los álbumes).","OA N°7 — identificación del dilema")
q("","¿Con qué hecho histórico real se relaciona directamente el relato?",
 ["El terremoto y maremoto de Valdivia de 1960","El terremoto de Valparaíso de agosto de 1906","El gran incendio de Valparaíso de 2014","*La erupción del volcán Chaitén de 2008"],"d",
 "El relato menciona Chaitén, la fecha (mayo de 2008), la ceniza y la evacuación por mar: corresponde a la erupción del volcán Chaitén, que obligó a evacuar a la población.","OA N°7 — contexto histórico")
q("","Frente al dilema de Daniela, ¿cuál de estas respuestas es una **postura fundamentada** en el texto?",
 ["Se equivocó, porque las fotos son lo único que importa en una emergencia","Hizo mal, porque debió quedarse en Chaitén para cuidar la casa familiar","*Acertó, porque la abuela necesitaba sus remedios cada día, como ella reconoce","No importa lo que eligió, porque al final no pasó nada grave en el pueblo"],"c",
 "La postura se apoya en datos del texto: la abuela toma remedios «todos los días» y al final dice «Lo importante lo trajiste tú». Las otras contradicen el relato o no dan razones.","OA N°7 — postura personal frente a un dilema")
q("","¿Qué interpretación del sentido general del relato integra mejor el dilema, el contexto histórico y el final?",
 ["Que en una erupción lo mejor es salvar los objetos de valor y dejar a las personas atrás","*Que en una emergencia como la de 2008 cuidar la vida es lo primero, y los recuerdos viven en las personas","Que los vecinos de Chaitén nunca se ayudaron entre sí durante la evacuación de 2008","Que las fotos se perdieron todas, por lo que la decisión de Daniela fue un grave error"],"b",
 "El relato muestra que Daniela prioriza la salud de su abuela en una emergencia real, y el final (las fotos rescatadas y la frase de la abuela) sugiere que lo esencial son las personas y los lazos.","OA N°7 — interpretación integrada")
T4='''## Texto 4 (para las preguntas 14 a 17): columna de opinión "Recreos con la cabeza levantada"

> En muchos colegios, el recreo se ha vuelto silencioso: grupos de estudiantes sentados uno al lado del otro, cada uno mirando su celular. Creo que ha llegado el momento de que los colegios limiten el uso del teléfono durante los recreos.
>
> El recreo es el espacio donde aprendemos a convivir: a jugar, a conversar, a resolver conflictos sin un adulto que dirija. Si lo pasamos frente a una pantalla, perdemos esa oportunidad. Además, un informe de la UNESCO publicado en 2023 advirtió que el uso del celular sin fines educativos puede distraer a los estudiantes y afectar su aprendizaje.
>
> Limitar no significa prohibir para siempre: los teléfonos pueden quedar guardados y usarse en clases cuando el profesor lo indique. Un recreo con la cabeza levantada es un recreo con más amigos.

'''
q(T4,"¿Cuál es la postura principal del autor de la columna?",
 ["*Que los colegios deberían limitar el uso del celular durante los recreos","Que los celulares deben prohibirse para siempre en todos los lugares","Que los recreos deberían eliminarse para dedicar más tiempo a las clases","Que los estudiantes deberían usar más el celular para aprender a convivir"],"a",
 "El autor lo dice en el primer párrafo: «ha llegado el momento de que los colegios limiten el uso del teléfono durante los recreos». Aclara que limitar no es prohibir para siempre.","OA N°8 — postura del autor")
vf("","«La frase “un informe de la UNESCO publicado en 2023 advirtió que el uso del celular sin fines educativos puede distraer a los estudiantes” es solo una opinión personal del autor.»",False,
 "Es un hecho verificable, porque cita una fuente concreta (un informe de la UNESCO de 2023) que puede consultarse. Una opinión, en cambio, expresa una valoración del autor, como «creo que ha llegado el momento».","OA N°8 — hecho versus opinión")
q("","¿Cuál de estos es un **argumento** que usa el autor para sostener su postura?",
 ["Que los recreos duran quince minutos en todos los colegios del país","Que los celulares nuevos tienen pantallas cada vez más grandes","Que muchos estudiantes llevan el celular guardado en la mochila","*Que en el recreo se aprende a convivir y la pantalla lo impide"],"d",
 "El autor afirma que el recreo es el espacio para aprender a convivir y que la pantalla hace perder esa oportunidad: es una razón que apoya su postura. Las otras opciones no aparecen en la columna o no apoyan la tesis.","OA N°8 — argumentos que sostienen una postura")
q("","¿Qué **contraargumento** podría plantear una persona que no está de acuerdo con la columna?",
 ["Que en el recreo se conversa más cuando no se usa el celular","Que la UNESCO publicó un informe sobre el celular en 2023","*Que el celular sirve para avisar a la familia en una emergencia","Que un recreo con la cabeza levantada tiene más amigos"],"c",
 "Avisar a la familia en una emergencia es una razón para no limitar el celular: se opone a la postura del autor. Un contraargumento se opone a la tesis con una razón. Las otras opciones repiten o apoyan lo que dice la columna.","OA N°8 — evaluación crítica de la argumentación")
T5='''## Texto 5 (para las preguntas 18 a 21): "Campeonato de robótica escolar"

**Texto A — Noticia de un medio digital nacional**

> **Liceo de Coyhaique gana el campeonato nacional de robótica escolar**
> Un equipo de cuatro estudiantes de un liceo público de Coyhaique ganó el campeonato nacional de robótica escolar, con un robot que separa residuos para reciclar. El equipo trabajó durante seis meses en el taller del liceo, con apoyo de su profesor de Tecnología. Este año participó la mayor cantidad de equipos desde que comenzó el campeonato.

::barras::2021=18;2022=25;2023=31;2024=46::y=Equipos inscritos;valores=si::

**Texto B — Comentario publicado en una red social**

> "Seguro que el robot lo hicieron los profesores. Es difícil creer que unos niños de región sepan tanto de tecnología. Esos premios siempre deberían quedarse en Santiago."

'''
q(T5,"¿Cuál es el propósito **implícito** del Texto B?",
 ["Informar los resultados del campeonato con datos precisos","*Descalificar el logro de los estudiantes por el lugar donde viven","Felicitar al equipo de Coyhaique por su esfuerzo y su robot","Invitar a más liceos a inscribirse en el próximo campeonato"],"b",
 "Sin decirlo directamente, el comentario busca restar mérito al triunfo, suponiendo que estudiantes de región no podrían lograrlo. No informa ni felicita.","OA N°9 — propósito implícito")
q("","Según el gráfico del Texto A, ¿cuántos equipos más se inscribieron en 2024 que en 2021?",
 ["*28 equipos","46 equipos","15 equipos","64 equipos"],"a",
 "En 2024 se inscribieron 46 equipos y en 2021, 18: 46 − 18 = 28. 15 equipos es la diferencia entre 2024 y 2023.","OA N°9 — interpretación de un gráfico (texto discontinuo)")
q("","¿Qué prejuicio presenta el Texto B y por qué lo es?",
 ["Un prejuicio de género, porque supone que solo las niñas saben de robótica","Un prejuicio de edad, porque supone que los profesores son demasiado jóvenes","*Un prejuicio territorial, porque supone sin pruebas que quienes viven en regiones saben menos","No presenta prejuicios, porque se basa en datos que aparecen en la noticia"],"c",
 "Juzga la capacidad de los estudiantes solo por vivir en una región, sin ninguna evidencia: eso es un prejuicio territorial. La noticia, en cambio, cuenta seis meses de trabajo del equipo.","OA N°9 — estereotipos y prejuicios")
q("","¿En qué se diferencian los propósitos del Texto A y del Texto B, y por qué importa reconocer prejuicios en las redes sociales?",
 ["Los dos informan exactamente lo mismo; reconocer prejuicios no cambia en nada la forma de leer","El A opina sin datos y el B informa con cifras; los prejuicios ayudan a entender mejor","El B es una noticia oficial y el A un comentario; las redes sociales nunca tienen prejuicios","*El A informa el triunfo con datos y el B lo desacredita; reconocer prejuicios evita difundir ideas injustas"],"d",
 "La noticia entrega hechos (equipo, robot, tiempo de trabajo, cifras) y el comentario expresa una idea prejuiciosa. Detectarlo permite leer críticamente y no replicar discriminaciones.","OA N°9 — comparación de propósitos y pensamiento crítico")
S6="## Sección de Escritura (para las preguntas 22 a 25)\n\n"
q(S6,"¿Qué conector expresa una **consecuencia** en la oración «El equipo trabajó seis meses; ___, logró ganar el campeonato»?",
 ["sin embargo","*por lo tanto","en cambio","aunque"],"b",
 "«Por lo tanto» presenta el resultado de lo anterior: el trabajo de seis meses llevó al triunfo. «Sin embargo», «en cambio» y «aunque» expresan oposición.","OA N°15 — uso de conectores")
q("","¿Cuál es la versión corregida de «Las niña ponió los libros sobre la mesa, que estaban rota»?",
 ["*La niña puso los libros sobre la mesa, que estaba rota","Las niñas ponió los libros sobre la mesa, que estaban rotas","La niña ponió los libros sobre la mesa, que estaba rota","Las niña puso los libros sobre la mesa, que estaban rota"],"a",
 "«La niña» concuerda en número; el pasado de «poner» es irregular: «puso» (no «ponió»); y «rota» concuerda con «la mesa»: «que estaba rota».","OA N°15 — concordancia y verbos irregulares")
q("","¿Qué se debe hacer en la etapa de **revisión** de un texto?",
 ["Inventar un título nuevo sin volver a leer lo que se escribió","Copiar el texto de un compañero para compararlo con el propio","*Releer y corregir la ortografía, la concordancia y las ideas","Borrar todo el borrador y empezar de nuevo sin planificar"],"c",
 "Revisar es releer el borrador para corregir errores y mejorar la claridad antes de entregarlo. Copiar o borrar todo no corresponde a esa etapa.","OA N°15 — revisión de la escritura")
q("","Para un correo a la directora proponiendo un taller de robótica, ¿qué párrafo cuida un registro formal, usa un conector y no tiene errores de concordancia?",
 ["«Hola dire, queremos un taller de robótica porfa, sería bacán.»","«Estimada directora: Nosotros quiere proponer un taller de robótica, porque los estudiante está interesado.»","«Directora, el taller. Robótica. Martes. Sala 5. Gracias.»","*«Estimada directora: Le proponemos crear un taller de robótica, ya que muchos estudiantes están interesados.»"],"d",
 "Ese párrafo usa un saludo formal, el conector «ya que» y concordancias correctas («proponemos», «estudiantes están»). Las otras usan registro informal, tienen errores o no forman oraciones.","OA N°15 — registro formal y corrección gramatical")
armar(C/'lengua-y-literatura-examen-forma-b.md', C/'lengua-y-literatura-examen-forma-a.md', Q,
  fila=lambda i,p,cl: f"| {i} | **{cl}.** {p.explicacion} | {p.oa} |",
  reemplazos={"— Forma B":"— Forma A","(Forma B)":"(Forma A)","Esta es la **Forma B**: una segunda versión":"Esta es la **Forma A**: una versión","a los del banco de contenido":"a los del banco de contenido y de la Forma B","última actualización: 2026-08-10":"última actualización: 2026-11-16"},
  inicio_preguntas="## Texto 1")
if __name__=="__main__":
    from collections import Counter; print(Counter(p.letra for p in Q), len(Q))
