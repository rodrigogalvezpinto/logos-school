import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from forma_a import P, armar  # noqa: E402
C=Path(__file__).resolve().parents[4]/'contenido'/'02-medio/examenes'
A="**{n}. (Alternativas)** "
Q=[]
def q(sec,en,ops,l,ex,oa,cab=A): Q.append(P(sec,cab,en,ops,l,ex,oa))
def vf(sec,en,v,ex,oa): Q.append(P(sec,"**{n}. (Verdadero o Falso)** ",en,[],"V" if v else "F",ex,oa,{"clave":"Verdadero" if v else "Falso"}))
T1='''## Texto 1 (para las preguntas 1 a 5): "La caja de lata" (fragmento)

> Cuando vendieron la casa de la abuela en Lota, a Daniela le tocó vaciar el entretecho. Entre sacos de ropa vieja encontró una caja de galletas oxidada, cerrada con un elástico que se deshizo al tocarlo. Su madre le había advertido: «No abras nada de la abuela sin mí; ella guardaba cosas que nunca quiso contar». Daniela la abrió igual.
>
> Adentro había fotos de hombres con cascos y lámparas, y una carta doblada en cuatro, con letra temblorosa:
>
> *«Lota, junio de 1960. Hermana: el chiflón se tragó a tres compañeros de Ramiro el martes. Él dice que no le tiene miedo al carbón, como los mineros de esos cuentos de Lillo que lee en las noches, pero yo lo veo rezar antes de bajar. Si algún día me pasa algo, no le cuentes a mi hija cómo vivimos. Quiero que crea que fuimos felices».*
>
> Daniela miró las fotos otra vez. En todas, su abuelo Ramiro sonreía. Bajó del entretecho con la caja apretada contra el pecho y, por primera vez, no supo si debía contarle a su madre lo que había leído.

'''
q(T1,"¿Qué situación del presente del relato lleva a Daniela a encontrar la caja de lata?",
 ["Su madre le pide que busque las fotos del abuelo para un homenaje en la mina","*La venta de la casa de la abuela obliga a vaciar el entretecho","Un temblor derriba el entretecho y deja a la vista las cosas de la abuela","La abuela, antes de morir, le indica dónde estaba escondida la caja"],"b",
 "El relato comienza con la venta de la casa: por eso Daniela debe vaciar el entretecho, donde encuentra la caja de lata.","OA N°3 — situación que desencadena la acción")
vf("","\"La carta revela, de manera implícita, que la familia vivía con miedo, aunque las fotografías muestren lo contrario.\"",True,
 "Verdadero. La abuela no dice «tenemos miedo», pero lo sugiere (el chiflón que «se tragó» a tres compañeros, Ramiro que reza antes de bajar), mientras las fotos muestran al abuelo sonriendo.","OA N°3 — información explícita e implícita")
q("","¿Qué consecuencia tiene, al final del fragmento, la decisión de Daniela de abrir la caja sin su madre?",
 ["Recibe un castigo de su madre, que descubre la caja abierta en el entretecho","Pierde las fotos del abuelo, porque el elástico se deshace al tocarlo","Decide quemar la carta para que nadie más conozca la historia familiar","*Queda frente al dilema de contar o callar lo que la abuela quiso ocultar"],"d",
 "Al desobedecer la advertencia («No abras nada de la abuela sin mí»), Daniela descubre un secreto y queda ante el dilema de contarlo o respetar el deseo de la abuela.","OA N°3 — análisis de personajes: dichos y consecuencias")
q("","¿Qué indicio anticipa, antes de la carta, que la caja guarda una historia difícil?",
 ["*La advertencia de la madre: la abuela guardaba cosas que nunca quiso contar","El elástico que se deshace, porque la caja era muy antigua y frágil","Los sacos de ropa vieja que Daniela encuentra en el entretecho de la casa","La venta de la casa, que ocurre porque la familia ya no vive en Lota"],"a",
 "La advertencia de la madre («ella guardaba cosas que nunca quiso contar») anticipa que la caja esconde un secreto doloroso antes de que aparezca la carta.","OA N°3 — efecto del indicio")
q("","¿Qué efecto produce presentar la historia de la mina en una carta intercalada, y con qué obra dialoga el fragmento?",
 ["Hace que el relato sea más corto, y no dialoga con ninguna otra obra literaria chilena","Permite que el narrador opine sobre la minería, y dialoga con un cuento de terror europeo","*Da voz directa al pasado, en las palabras de la abuela, y dialoga con *Subterra* de Baldomero Lillo","Reemplaza al narrador por la madre de Daniela, y dialoga con una noticia de prensa de 1960"],"c",
 "La carta intercalada hace oír directamente la voz de la abuela en 1960; la mención de «esos cuentos de Lillo» remite a *Subterra*, de Baldomero Lillo, sobre la vida de los mineros del carbón en Lota.","OA N°3 — recurso narrativo y relación intertextual")
T2='''## Texto 2 (para las preguntas 6 a 9): "La micro de las seis" (fragmento de obra teatral)

> **Personajes**: DON HUGO (66 años, chofer de micro en su último día de trabajo), KEVIN (22 años, chofer nuevo), SEÑORA ELBA (pasajera de siempre).
> **Escenario**: interior de una micro en el terminal, a las seis de la tarde. En el tablero, junto al volante, cuelga una gorra gastada.
>
> *(DON HUGO limpia el parabrisas con un paño. KEVIN revisa una tablet.)*
>
> **KEVIN**: Don Hugo, desde mañana todo es con la tarjeta y el GPS. Ya no va a hacer falta saberse el recorrido de memoria.
>
> **DON HUGO**: Cuarenta años me lo sé de memoria. Sé dónde se sube la señora Elba, dónde hay un hoyo, dónde se cruzan los niños del liceo.
>
> *(Sube la SEÑORA ELBA.)*
>
> **SEÑORA ELBA**: ¿Es cierto que se va, don Hugo? ¿Y quién me va a esperar cuando llegue atrasada?
>
> *(DON HUGO no responde. Toma la gorra del tablero y la mira largo rato. Afuera, las luces de la ciudad se encienden una a una.)*
>
> **DON HUGO**: *(le pone la gorra a KEVIN)* El GPS le dice por dónde ir, mijo. La gente le dice para qué.

'''
q(T2,"¿Cuál es el conflicto central de la escena?",
 ["*La tensión entre la experiencia humana de don Hugo y un sistema nuevo que parece reemplazarla","La pelea entre Kevin y la señora Elba por el precio del pasaje en la micro","El miedo de don Hugo a manejar de noche cuando se encienden las luces de la ciudad","La competencia entre dos empresas de buses por quedarse con el recorrido"],"a",
 "Don Hugo defiende lo que sabe de memoria (la gente, el recorrido), mientras Kevin anuncia que la tarjeta y el GPS lo harán innecesario: esa tensión organiza la escena.","OA N°5 — conflicto central")
q("","¿Qué elemento funciona principalmente como símbolo del oficio y de la experiencia de don Hugo?",
 ["La tablet de Kevin","El paño de limpiar","El parabrisas","*La gorra gastada"],"d",
 "La gorra gastada, que cuelga en el tablero y que don Hugo entrega a Kevin, representa su oficio y los años de experiencia que transmite.","OA N°5 — símbolo")
q("","¿Qué efecto produce la acotación de las luces de la ciudad que «se encienden una a una» mientras don Hugo mira la gorra?",
 ["Indica que se cortó la electricidad en el terminal y que la micro no podrá salir","*Marca el fin de una jornada y de una etapa, y da solemnidad al silencio del personaje","Anuncia que la señora Elba llegará atrasada porque ya es de noche en la ciudad","Describe el horario de la micro para que el público sepa cuándo sale el recorrido"],"b",
 "Las luces que se encienden marcan el paso del día a la noche: simbolizan el término de una etapa y dan solemnidad al silencio de don Hugo antes de entregar la gorra.","OA N°5 — elementos de la puesta en escena")
q("","¿Qué idea cuestiona don Hugo con su frase final y por qué sigue siendo relevante hoy?",
 ["Que los jóvenes sean buenos choferes; es relevante porque Kevin no sabe manejar","Que la micro sea un buen trabajo; es relevante porque los choferes ganan poco","*Que la tecnología baste para hacer bien un trabajo; es relevante porque muchos oficios se automatizan","Que las tarjetas sean seguras; es relevante porque hay muchos robos en el transporte"],"c",
 "Con «El GPS le dice por dónde ir, mijo. La gente le dice para qué», don Hugo cuestiona que la tecnología baste: el trabajo también exige trato humano, un tema vigente ante la automatización.","OA N°5 — creencias y visión de mundo")
T3='''## Texto 3 (para las preguntas 10 a 13): "La máscara" (microcuento)

> Todos los julios, mi padre viajaba a La Tirana a bailar de diablo. Decía que era una manda: la Virgen del Carmen lo había sanado cuando era niño, y él le debía el baile hasta que las piernas le dieran.
>
> Este año, en Santiago, encontré su máscara de yeso en el clóset, con los cuernos pintados de rojo y los ojos de vidrio. Mi padre ya no puede caminar. Me la probé frente al espejo. Pesaba más de lo que pensaba, y entendí por qué él bailaba con los ojos cerrados: no era para no ver a la gente, sino para cargar la promesa.

'''
q(T3,"¿A qué celebración cultural alude explícitamente el microcuento?",
 ["La Fiesta de San Pedro de los pescadores","El We Tripantu del pueblo mapuche","La Fiesta de Cuasimodo del valle central","*La Fiesta de La Tirana, en el norte de Chile"],"d",
 "El microcuento nombra La Tirana, el mes de julio, la Virgen del Carmen y el baile de diablo: alude a la Fiesta de La Tirana, en la Región de Tarapacá.","OA N°8 — antecedente cultural")
vf("","\"El narrador considera que la manda de su padre fue una costumbre sin sentido, que terminó cuando él dejó de caminar.\"",False,
 "Falso. Al probarse la máscara, el narrador comprende el peso de la promesa («entendí por qué él bailaba con los ojos cerrados»): valora la manda, no la desprecia.","OA N°8 — antecedente cultural y visión de mundo")
q("","¿Qué citas sustentan la hipótesis de que la máscara representa el peso de la promesa y no solo un objeto? Marca todas las correctas.",
 ["«Pesaba más de lo que pensaba»","«Mi padre ya no puede caminar»","«no era para no ver a la gente, sino para cargar la promesa»","«Decía que era una manda»"],"acd",
 "«Pesaba más de lo que pensaba», «para cargar la promesa» y «era una manda» vinculan la máscara con el compromiso del padre; «Mi padre ya no puede caminar» informa una situación, pero no sustenta esa hipótesis.","OA N°8 — hipótesis fundamentada con citas",cab="**{n}. (Varias correctas)** ")
q("","¿Qué interpretación del microcuento integra un punto de vista, una cita y la relación con su contexto cultural?",
 ["*Desde la tradición religiosa popular, la máscara simboliza una promesa que pasa de padre a hijo: «no era para no ver a la gente, sino para cargar la promesa», como en las mandas de La Tirana","Desde la vida familiar, el microcuento trata sobre un hombre enfermo que viaja a Santiago, y la máscara es solo un adorno que el hijo guarda en el clóset por cariño a su padre, como cualquier recuerdo","Desde el miedo infantil, la máscara es aterradora porque tiene «cuernos pintados de rojo» y ojos de vidrio, lo que demuestra que la fiesta del norte es un rito peligroso para los niños","Desde la salud, el narrador critica la fiesta porque su padre perdió la capacidad de caminar por bailar tantos años, cada julio, con una máscara de yeso tan pesada"],"a",
 "La interpretación mejor construida declara un punto de vista (la tradición religiosa popular), cita el texto y lo relaciona con las mandas de La Tirana.","OA N°8 — interpretación literaria integrada")
T4='''## Texto 4 (para las preguntas 14 a 17): columna de opinión "La feria no es el pasado"

> Cada domingo, la feria libre de mi barrio reúne a cientos de vecinos. Sin embargo, algunos dicen que las aplicaciones de reparto la volverán innecesaria. Me parece un error: la feria no es solo un lugar para comprar, sino un espacio de encuentro que ninguna aplicación puede reemplazar.
>
> La feria es el pulmón del barrio: ahí se conversa, se pregunta por los enfermos, se fía a quien no le alcanza. Mi vecina dejó de ir a la feria cuando empezó a pedir por aplicación, y a los pocos meses se enfermó; está claro, entonces, que las aplicaciones dañan la salud de las personas.
>
> Quienes creen que las ferias están anticuadas simplemente no han puesto un pie en una. Solo un ciego no ve que perderlas sería perder parte de nuestra comunidad.

'''
q(T4,"¿Cuál es la tesis principal de la columna?",
 ["Las aplicaciones de reparto son más baratas que la feria y deberían reemplazarla","Los vecinos deberían comprar solo por aplicación para no perder el tiempo los domingos","*La feria libre es un espacio de encuentro comunitario que ninguna aplicación puede reemplazar","Las ferias libres deberían cerrar los domingos para que los feriantes puedan descansar"],"c",
 "El autor sostiene que la feria «no es solo un lugar para comprar, sino un espacio de encuentro que ninguna aplicación puede reemplazar»: esa es la tesis.","OA N°9 — tesis del autor")
q("","¿Qué figura retórica corresponde a la expresión «la feria es el pulmón del barrio»?",
 ["Una hipérbole, porque exagera la cantidad de personas","*Una metáfora, porque identifica la feria con un órgano vital","Una ironía, porque dice lo contrario de lo que piensa","Una pregunta retórica, porque no espera respuesta"],"b",
 "Es una metáfora: identifica la feria con el pulmón, un órgano vital, para expresar que le da vida al barrio.","OA N°9 — figura retórica")
q("","¿Qué falla de argumentación hay en el caso de la vecina, en el segundo párrafo?",
 ["Usa una cita de un experto que no tiene relación con el tema de las ferias","Presenta demasiados datos estadísticos, que confunden al lector común","Ataca a la persona de un feriante en vez de discutir sus argumentos","*Saca una conclusión general a partir de un solo caso y supone una causa sin probarla"],"d",
 "Del caso de una sola vecina concluye que «las aplicaciones dañan la salud»: es una generalización apresurada que, además, supone sin pruebas que una cosa causó la otra.","OA N°9 — fallas de argumentación")
q("","¿Por qué expresiones como «simplemente no han puesto un pie en una» y «solo un ciego no ve» pueden debilitar la columna ante un lector que piensa distinto?",
 ["*Porque descalifican a quienes discrepan en vez de responder a sus razones, y eso aleja a ese lector","Porque son demasiado formales y técnicas para una columna de opinión publicada en el diario","Porque entregan datos precisos que el lector puede verificar fácilmente en otras fuentes","Porque repiten exactamente la tesis del primer párrafo, sin agregar ninguna idea nueva"],"a",
 "Estas expresiones descalifican a quien piensa distinto («solo un ciego») en vez de discutir sus razones: un lector que no está de acuerdo se siente atacado, no persuadido.","OA N°9 — postura personal y evaluación de recursos léxicos")
T5='''## Texto 5 (para las preguntas 18 a 21): "Marea roja en la costa de Chiloé"

**Texto A — Nota de un portal de noticias**

> **Autoridad sanitaria prohíbe extraer mariscos en la costa oeste de Chiloé**
> La Seremi de Salud decretó la prohibición de extraer y consumir mariscos en la costa oeste de Chiloé, tras detectar toxinas de marea roja sobre el límite permitido. «La medida busca proteger la salud de la población», explicó la autoridad. La nota incluye un mapa con la zona afectada pintada de rojo.

**Texto B — Video de un pescador artesanal en una red social**

> "Llevamos tres semanas sin poder trabajar. En mi caleta somos 40 familias y nadie nos ha dicho cuándo se levanta la prohibición ni cómo vamos a pagar las cuentas." El video muestra botes amarrados y redes vacías, con una música lenta de fondo.

'''
q(T5,"¿Qué información entrega el Texto B que el Texto A no menciona?",
 ["La razón sanitaria de la prohibición de extraer mariscos en la zona","*El efecto económico de la prohibición en las familias de pescadores","El nombre de la autoridad que decretó la prohibición en la costa","La ubicación exacta de la zona afectada por la marea roja"],"b",
 "El Texto B muestra el impacto económico: 40 familias de la caleta llevan tres semanas sin trabajar. El Texto A informa la medida sanitaria, pero no sus consecuencias para los pescadores.","OA N°10 — evidencias entregadas y omitidas")
q("","¿Qué muestra principalmente la comparación entre el Texto A y el Texto B?",
 ["Que el Texto A miente sobre la marea roja y el Texto B dice toda la verdad","Que los dos textos tienen exactamente el mismo propósito y el mismo público","*Que un mismo hecho se presenta desde la salud pública o desde la vida de los afectados","Que las redes sociales son siempre más confiables que los portales de noticias"],"c",
 "El Texto A enfoca la medida desde la salud pública y el B desde la vida de los pescadores afectados: un mismo hecho visto desde puntos de vista distintos, ambos parciales.","OA N°10 — comparación de fuentes")
q("","¿Qué efecto producen los recursos no lingüísticos de cada texto?",
 ["Los dos textos usan solo palabras, sin ningún recurso visual ni sonoro de apoyo","El mapa del Texto A emociona al lector y la música del B le entrega datos precisos","Ambos recursos sirven únicamente para decorar los textos, sin cambiar su efecto","*El mapa del A ubica la zona con precisión; los botes amarrados y la música del B buscan conmover"],"d",
 "El mapa del Texto A informa dónde está la zona afectada; las imágenes de botes amarrados y redes vacías, con música lenta, buscan conmover a quien ve el video del Texto B.","OA N°10 — recursos no lingüísticos")
q("","¿Qué fortalece y qué riesgo tiene el uso del testimonio personal en el Texto B?",
 ["Fortalece la precisión científica del texto; su riesgo es que use demasiadas cifras técnicas","*Fortalece la cercanía con quien lo ve; su riesgo es que la emoción lleve a juzgar sin conocer la razón sanitaria","Fortalece la neutralidad del texto; su riesgo es que no muestre ninguna opinión del pescador","No fortalece nada, porque un testimonio personal nunca sirve como evidencia de ningún hecho"],"b",
 "El testimonio acerca la situación a quien ve el video, pero la emoción (la música, las redes vacías) puede llevar a juzgar la medida sin considerar su razón sanitaria.","OA N°10 — recursos emocionales, evidencia e influencia en las propias opiniones")
T6='''## Sección de Escritura — Ensayo persuasivo (para las preguntas 22 a 25)

> Como escritor o escritora de 2° medio, debes ser capaz de escribir **ensayos persuasivos**: textos que presentan una hipótesis clara, la sustentan con evidencia pertinente —literaria y no literaria—, usan contraargumentos cuando corresponde, incorporan recursos variados (anécdotas, citas, síntesis, infografías) para mantener el interés de quien lee sin perder la coherencia temática, y cierran con una conclusión coherente, usando citas y referencias. Las siguientes preguntas toman como referencia el ensayo modelo **"¿Debe la tradición quedarse quieta?"**, que se apoya en los textos "La micro de las seis" y "La máscara" trabajados en esta misma prueba, y el tema: **"¿Deberían los municipios apoyar a las ferias libres?"** (relacionado con el Texto 4 de esta prueba).
>
> *Fragmento del ensayo modelo*: "Sostengo que una tradición se mantiene viva cuando se transmite, no cuando se congela: don Hugo entrega su gorra a un chofer que usará GPS, y el hijo de la máscara carga la promesa a su manera. [...] Alguien podría responder que adaptar una tradición es traicionarla. Es una objeción seria [...] Pero una encuesta municipal de la comuna, citada por el diario local, muestra que las ferias que incorporaron pago con tarjeta mantuvieron a sus clientes sin perder su carácter de encuentro."

'''
q(T6,"Un estudiante escribe un ensayo con la hipótesis «Los municipios deberían apoyar a las ferias libres». Para mantener el interés agrega una anécdota sobre su abuela feriante, pero luego dedica dos párrafos a contar sus vacaciones en la playa. ¿Qué debe corregir?",
 ["Debe eliminar la anécdota, porque los recursos como las anécdotas no se usan nunca en un ensayo","Debe agregar más párrafos sobre las vacaciones, porque así el ensayo será más entretenido","*La anécdota de la abuela sirve, pero los párrafos de las vacaciones rompen la coherencia temática","Debe cambiar la hipótesis por «Las vacaciones en la playa son lo mejor del año escolar»"],"c",
 "Los recursos variados, como una anécdota, sirven si apoyan la hipótesis; los párrafos sobre las vacaciones no se relacionan con ella y rompen la coherencia temática.","OA N°14 — recursos variados y coherencia temática")
q("","¿Qué función cumple en el ensayo modelo la referencia a la encuesta municipal citada por el diario local?",
 ["*Aporta evidencia no literaria, con su fuente, para responder al contraargumento","Introduce un tema nuevo, sin relación con la hipótesis que el autor defiende","Reemplaza la hipótesis del ensayo por la opinión de otra institución","Sirve como conclusión final, porque no hay nada más que agregar al texto"],"a",
 "La encuesta municipal, con su fuente, es evidencia no literaria: el autor la usa para responder a la objeción de que adaptar una tradición es traicionarla.","OA N°14 — evidencia no literaria y citas")
q("","Para un ensayo sobre «¿Deberían los municipios apoyar a las ferias libres?», ¿qué planificación es la más adecuada?",
 ["Hipótesis: ninguna, porque basta con describir una feria. Recursos: una lista de las frutas que se venden en la feria de mi barrio","Hipótesis: las ferias libres son mejores que todo lo demás. Recursos: frases como «solo un ciego no ve», para convencer con fuerza","Escribir sin hipótesis y decidir la postura al final, según cómo quede el texto, agregando datos si sobra espacio en la hoja","*Hipótesis: el apoyo municipal ayuda a mantener un espacio comunitario. Recursos: una anécdota, el dato de la encuesta municipal y un contraargumento"],"d",
 "Una buena planificación define una hipótesis clara y elige recursos pertinentes: una anécdota, un dato con su fuente y un contraargumento para responder.","OA N°14 — planificación: hipótesis y recursos")
q("","¿Qué opción reúne hipótesis, contraargumento y una conclusión coherente para el ensayo sobre el apoyo municipal a las ferias libres?",
 ["Hipótesis: «Las ferias son lindas.» Contraargumento: ninguno. Conclusión: «Por eso, las aplicaciones de reparto deberían ser gratuitas para todos los vecinos de la comuna.»","*Hipótesis: «Los municipios deben apoyar a las ferias porque son espacios de encuentro.» Contraargumento: «Algunos dicen que cuesta dinero público.» Conclusión: «Por eso, ese apoyo es una inversión en comunidad.»","Hipótesis: «Los municipios deben apoyar a las ferias.» Contraargumento: «Las ferias son malas.» Conclusión: «Por eso, los municipios deben cerrar todas las ferias de la comuna desde mañana.»","Solo una conclusión, sin hipótesis ni contraargumento: «En conclusión, las ferias tienen cosas buenas y malas, y cada vecino sabrá qué hacer con ellas.»"],"b",
 "La opción correcta presenta una hipótesis clara, considera un contraargumento (el costo público) y cierra con una conclusión coherente con la hipótesis.","OA N°14 — hipótesis, contraargumento, coherencia temática y conclusión")
armar(C/'lengua-y-literatura-examen-forma-b.md', C/'lengua-y-literatura-examen-forma-a.md', Q,
  fila=lambda i,p,cl: f"| {i} | **{cl}.** {p.explicacion} | {p.oa} |",
  reemplazos={"— Forma B":"— Forma A","— FORMA B":"— FORMA A","última actualización: 2026-08-11":"última actualización: 2026-11-17",
    "*Segunda versión del examen de ensayo de la asignatura, construida a partir del banco de preguntas de estudio (`lengua-y-literatura.md`), con textos y preguntas distintos a los del banco de contenido.":"*Forma A del examen de ensayo de la asignatura, construida a partir del banco de preguntas de estudio (`lengua-y-literatura.md`), con textos y preguntas propios, distintos de la Forma B y del banco de contenido."},
  inicio_preguntas="## Texto 1")
if __name__=="__main__":
    from collections import Counter; print(Counter(p.letra for p in Q), len(Q))
