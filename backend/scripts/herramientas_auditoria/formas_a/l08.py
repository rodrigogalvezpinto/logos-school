import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from forma_a import P, armar  # noqa: E402
C=Path(__file__).resolve().parents[4]/'contenido'/'08-basico/examenes'
A="**{n}. (Alternativas)** "
Q=[]
def q(sec,en,ops,l,ex,oa,cab=A): Q.append(P(sec,cab,en,ops,l,ex,oa))
def vf(sec,en,v,ex,oa): Q.append(P(sec,"**{n}. (Verdadero o Falso)** ",en,[],"V" if v else "F",ex,oa,{"clave":"Verdadero" if v else "Falso"}))
T1='''## Texto 1 (para las preguntas 1 a 5): "El guardián del reloj" (fragmento de la novela *La estación de los inviernos*)

> En el pueblo todos decían que don Efraín era el hombre más amargado del mundo. Vivía solo frente a la estación de trenes, nunca saludaba y espantaba a los niños que jugaban a la pelota cerca de su reja. Yo tenía doce años aquel invierno y, como todos, le tenía miedo.
>
> La noche en que se cortó la luz, salí a buscar a mi perro y lo vi: don Efraín, con una linterna en la boca, subía por una escalera hasta el viejo reloj de la estación. Lo escuché trabajar durante horas. Al amanecer, el reloj —que llevaba años detenido en las cuatro y diez— volvió a marcar la hora.
>
> Nunca se lo conté a nadie. Él tampoco dijo nada; solo, desde ese día, me saludaba con un leve movimiento de cabeza.
>
> Treinta años después, cuando volví al pueblo para su funeral, el reloj seguía andando. Entonces entendí que don Efraín no espantaba a los niños por odio: tenía miedo de que un pelotazo rompiera el vidrio del reloj que cuidaba en secreto, el mismo que su padre había instalado cuando llegó el primer tren.

'''
q(T1,"¿Cuál es el conflicto central del fragmento?",
 ["*La distancia entre la fama de amargado de don Efraín y lo que él hacía en secreto","La pelea entre la narradora y su perro durante la noche en que se cortó la luz","La competencia entre dos relojeros del pueblo por arreglar el reloj de la estación","El accidente del primer tren que llegó al pueblo justo cuando el reloj se detuvo"],"b",
 "El relato contrapone el prejuicio del pueblo («el hombre más amargado del mundo») con la verdad que la narradora descubre: don Efraín cuidaba en secreto el reloj de la estación.","OA N°3 — conflicto central")
q("","¿A qué **personaje tipo** parece corresponder don Efraín al comienzo, aunque el relato termine mostrando otra cara de él?",
 ["*El viejo gruñón y solitario que espanta a los niños","El héroe valiente que salva al pueblo de un peligro","El villano que planea dañar a los demás en secreto","El joven enamorado que lucha por conquistar a alguien"],"d",
 "Al inicio don Efraín encaja en el personaje tipo del viejo gruñón y solitario: no saluda y espanta a los niños. El final muestra que esa imagen era incompleta.","OA N°3 — personaje tipo")
vf("","«La narradora de este fragmento y el autor de la novela *La estación de los inviernos* son necesariamente la misma persona, con las mismas ideas y experiencias.»",False,
 "La narradora es una voz creada por el autor dentro de la ficción: cuenta la historia en primera persona, pero no tiene por qué ser el autor ni compartir su vida.","OA N°3 — narrador versus autor")
q("","¿Por qué el reloj de la estación puede considerarse un **símbolo** dentro del relato?",
 ["Porque es el objeto más caro del pueblo y todos querían comprarlo para venderlo","Porque solo sirve para saber a qué hora pasa el tren por el pueblo","*Porque representa la memoria del pueblo y el cuidado silencioso de don Efraín","Porque es un objeto peligroso que la narradora quería destruir desde niña"],"c",
 "Más allá de marcar la hora, el reloj une al padre de don Efraín, la historia del pueblo (el primer tren) y el cuidado secreto de su hijo: por eso adquiere un sentido simbólico.","OA N°3 — símbolo")
q("","¿Cómo cambia la comprensión de la narradora sobre don Efraín y qué expresión marca un salto temporal?",
 ["*Pasa del miedo a comprender su cuidado secreto; «Treinta años después» marca el salto","Pasa de admirarlo a odiarlo para siempre; «Al amanecer» marca el salto temporal","No cambia, porque siempre supo que él arreglaba el reloj; «aquel invierno» marca el salto","Pasa de conocerlo a olvidarlo por completo; «la noche en que se cortó la luz» marca el salto"],"a",
 "De niña le tenía miedo; de adulta, «treinta años después», entiende por qué espantaba a los niños. Esa expresión lleva el relato del pasado al presente de la narradora.","OA N°3 — evolución de personajes y disposición temporal")
T2='''## Texto 2 (para las preguntas 6 a 9): Poema "Amaso, madre, amaso"

> Amaso el pan de la mañana,
> amaso aunque la luz no llega,
> amaso, amaso, amaso, como el mar amasa
> la arena blanda de la orilla.
>
> La harina vuela, nieve tibia,
> el horno canta su canción de fuego;
> amaso el pan de los que duermen,
> amaso el pan de los que vuelven.

'''
q(T2,"¿Qué efecto produce principalmente la repetición de la palabra «amaso» a lo largo del poema?",
 ["Muestra que la hablante está aburrida y quiere terminar pronto","*Transmite el ritmo constante de un trabajo diario y paciente","Indica que la hablante cambia de actividad en cada verso","Hace que el poema sea más corto y fácil de memorizar"],"b",
 "Repetir «amaso» imita el movimiento repetido de las manos sobre la masa y transmite la constancia de una tarea que se hace cada día, aunque «la luz no llega».","OA N°4 — efecto de las repeticiones")
q("","¿Qué figura del lenguaje se reconoce en «La harina vuela, nieve tibia»?",
 ["*Una metáfora, porque identifica la harina con nieve tibia","Una onomatopeya, porque imita el sonido de la harina","Una hipérbole, porque exagera la cantidad de harina","Una comparación, porque une dos ideas con la palabra «como»"],"a",
 "La harina que flota en el aire se nombra directamente como «nieve tibia», sin usar «como»: es una metáfora que la muestra blanca y suave, pero cálida.","OA N°4 — lenguaje figurado")
q("","¿Qué idea transmite la comparación «amaso, amaso, amaso, como el mar amasa / la arena blanda de la orilla»?",
 ["Que el pan se hace mezclando arena blanda y agua salada de mar","Que la hablante vive lejos del mar y lo extraña todas las mañanas","*Que amasar es un gesto repetido y paciente, como el ir y venir de las olas","Que el mar es peligroso y destruye todo lo que toca en la orilla"],"c",
 "Las olas mueven la arena una y otra vez sin descanso; la comparación muestra el amasado como un gesto rítmico, constante y natural.","OA N°4 — interpretación de una comparación")
q("","¿Qué efecto produce la repetición de la estructura «amaso el pan de los que...» al final del poema?",
 ["Indica que la hablante vende pan en una panadería cerca de la playa","Hace que el poema pierda el ritmo y se vuelva confuso para quien lee","Muestra que el pan se prepara cada mañana solo para una persona","*Insiste en que el pan es un modo de cuidar a quienes duermen y a quienes vuelven"],"d",
 "La estructura repetida extiende el trabajo a otras personas: el pan es para los que duermen y los que regresan. Así la acción de amasar se vuelve un gesto de cuidado.","OA N°4 — repeticiones y su efecto")
T3='''## Texto 3 (para las preguntas 10 a 13): "Barro en Chañaral"

> Joaquín llevaba un año entrenando ajedrez para el campeonato regional de Copiapó. El viaje estaba fijado para el 26 de marzo de 2015. Pero la noche del 25, después de lluvias como nadie recordaba en el desierto, el río El Salado se desbordó y un aluvión de barro cubrió calles y casas de Chañaral.
>
> A la mañana siguiente, la casa de su familia seguía en pie, pero la de la señora Elena, su vecina de ochenta años, estaba llena de barro hasta las ventanas. El bus a Copiapó salía igual, en un camino que estaba siendo despejado. Su papá le dijo que la decisión era suya.
>
> Joaquín miró su tablero, guardado en la mochila, y luego a la señora Elena, sentada en la vereda con una foto mojada en las manos. Dejó la mochila en la cocina, tomó una pala y cruzó la calle.
>
> Meses después ganó un torneo pequeño en el colegio. Cuando le entregaron la medalla, pensó que la partida más difícil la había jugado con una pala, en el barro.

'''
q(T3,"¿Cuál es el dilema principal que enfrenta Joaquín en el relato?",
 ["Elegir entre estudiar ajedrez o fútbol durante las vacaciones de verano","*Elegir entre viajar al campeonato que preparó o ayudar a su vecina","Decidir si se cambia de colegio después del aluvión en Chañaral","Elegir entre dos tableros de ajedrez para llevar al campeonato"],"b",
 "Joaquín debe escoger entre su meta personal (el campeonato que preparó durante un año) y ayudar a la señora Elena, cuya casa quedó llena de barro.","OA N°8 — identificación del dilema")
vf("","«Las lluvias y el aluvión de marzo de 2015 en la Región de Atacama, mencionados en el relato, son hechos ficticios inventados por el autor.»",False,
 "Las lluvias y aluviones de marzo de 2015 en la Región de Atacama, que afectaron a Chañaral y Copiapó, fueron hechos reales. El relato usa ese contexto histórico, aunque Joaquín y la señora Elena son personajes de ficción.","OA N°8 — contexto histórico")
q("","Frente al dilema de Joaquín, ¿qué respuesta es un posicionamiento fundamentado en el texto?",
 ["Se equivocó, porque el ajedrez es lo único importante y las vecinas pueden arreglarse solas","Hizo mal, porque su papá le prohibió viajar al campeonato de Copiapó","*Acertó, porque la vecina mayor necesitaba ayuda urgente y él pudo jugar otros torneos después","No hubo dilema, porque el bus a Copiapó no salió ese día por el barro"],"c",
 "La postura se apoya en el texto: la señora Elena tiene ochenta años y su casa está llena de barro, y Joaquín gana otro torneo meses después. Las otras contradicen el relato (su papá lo dejó decidir y el bus sí salía).","OA N°8 — posicionamiento frente a un dilema")
q("","¿Qué interpretación del relato integra mejor el dilema, el contexto histórico y el final?",
 ["*Que en una catástrofe real, como la de 2015, la solidaridad puede pesar más que una meta personal","Que los campeonatos de ajedrez deben suspenderse siempre que llueve en el desierto","Que Joaquín nunca volvió a jugar ajedrez porque perdió su tablero en el barro","Que el aluvión de Chañaral no afectó a nadie y Joaquín ayudó solo por aburrimiento"],"a",
 "El final («la partida más difícil la había jugado con una pala») muestra que, en la catástrofe real de 2015, Joaquín puso la solidaridad con su vecina por sobre su meta personal.","OA N°8 — interpretación integrada")
T4='''## Texto 4 (para las preguntas 14 a 17): columna de opinión "Los sellos que nos cuidan"

> Desde 2016, en Chile los alimentos con exceso de azúcares, sodio, grasas saturadas o calorías llevan sellos negros con la frase «ALTO EN». Algunos dicen que son exagerados. Yo creo que son una de las mejores decisiones que hemos tomado como país.
>
> Los sellos no prohíben nada: solo informan. Gracias a ellos, cualquier persona puede saber en segundos qué está comiendo, sin leer tablas llenas de números. Y la misma ley impide vender esos productos dentro de los colegios.
>
> Cuidemos esta ley y exijamos que se cumpla en cada kiosco escolar. Ojalá algún día no necesitáramos sellos, porque todos elegiríamos alimentos sanos sin que nadie nos lo recordara.

'''
q(T4,"¿Cuál es la postura principal del autor o autora de la columna?",
 ["Que los sellos «ALTO EN» deberían eliminarse porque asustan a los consumidores","Que los colegios deberían vender más productos con sellos en sus kioscos","Que las tablas nutricionales son más claras que los sellos negros","*Que los sellos «ALTO EN» son una buena medida que hay que cuidar y hacer cumplir"],"d",
 "La autora dice que los sellos «ALTO EN» son «una de las mejores decisiones» y al final pide cuidar la ley y hacerla cumplir.","OA N°9 — postura del autor")
q("","¿Cuál de las siguientes oraciones del texto corresponde a un **hecho**, y no a una opinión?",
 ["«Yo creo que son una de las mejores decisiones que hemos tomado como país»","*«Desde 2016, en Chile los alimentos con exceso de azúcares […] llevan sellos»","«Ojalá algún día no necesitáramos sellos, porque todos elegiríamos alimentos sanos»","«Algunos dicen que son exagerados y que no ayudan a nadie a comer mejor»"],"b",
 "Que los sellos existen desde 2016 se puede comprobar en la ley y en los envases: es un hecho. «Yo creo» y «ojalá» introducen una opinión y un deseo.","OA N°9 — hecho versus opinión")
q("","¿Qué intención tiene la autora al usar el imperativo en «Cuidemos esta ley y exijamos que se cumpla en cada kiosco escolar»?",
 ["*Invitar a los lectores a una acción común en defensa de la ley","Contar lo que ocurrió en el pasado con la ley de etiquetado","Expresar una duda sobre si los sellos sirven o no","Describir con objetividad cómo se ven los sellos negros"],"a",
 "El imperativo en primera persona plural («cuidemos», «exijamos») incluye a la autora y a los lectores en una acción conjunta: busca movilizar, no solo informar.","OA N°9 — intención en el uso de modos verbales")
q("","¿Qué intención tiene el subjuntivo en «Ojalá algún día no necesitáramos sellos»?",
 ["Dar una orden que los lectores deben cumplir de inmediato","Informar un hecho comprobable sobre los alimentos","*Expresar el deseo de algo que todavía no ocurre","Contar una acción que ya ocurrió en el pasado"],"c",
 "«Ojalá» con subjuntivo («necesitáramos») expresa un deseo sobre una situación que aún no es real: que todos elijan alimentos sanos sin necesidad de sellos.","OA N°9 — modos verbales y postura personal")
T5='''## Texto 5 (para las preguntas 18 a 21): "Cierre de la piscina municipal"

**Texto A — Nota de la Radio Comunal de Las Araucarias**

> **Piscina municipal cerrará tres meses por reparaciones**
> La Municipalidad de Las Araucarias informó que la piscina temperada cerrará desde el 1 de abril por tres meses, para cambiar el sistema de calefacción y reparar filtraciones. Según el municipio, las obras son necesarias para la seguridad de los usuarios.

| Usuarios inscritos (promedio mensual) | Cantidad |
|---|---|
| Estudiantes de colegios municipales | 1.200 |
| Adultos mayores | 800 |

**Texto B — Publicación en redes sociales del Club de Natación Delfines**

> "¡Tres meses sin piscina justo antes del campeonato regional! Nadie consultó a los deportistas. Exigimos que el municipio nos diga YA dónde vamos a entrenar. ¡Comparte esta publicación!"

*(Las Araucarias es una comuna ficticia, creada para esta prueba.)*

'''
q(T5,"¿Cuál es el propósito **implícito** del Texto B?",
 ["Explicar con datos técnicos por qué se debe reparar la calefacción","Felicitar al municipio por cuidar la seguridad de los usuarios","Informar el horario de entrenamiento del club durante abril","*Presionar públicamente al municipio para que ofrezca un lugar donde entrenar"],"d",
 "Al pedir que se comparta la publicación y exigir una respuesta «YA», el club busca generar presión pública. No entrega datos técnicos ni felicita.","OA N°10 — propósito implícito")
q("","¿Qué evidencia la comparación entre el Texto A y el Texto B sobre un mismo hecho?",
 ["*Que el punto de vista de quien escribe influye en qué aspectos del hecho se destacan","Que los dos textos entregan exactamente la misma información con las mismas palabras","Que una radio comunal nunca puede informar sobre temas deportivos","Que las redes sociales siempre publican información más completa que las radios"],"a",
 "La radio destaca las razones de seguridad; el club, el perjuicio para sus deportistas. El mismo cierre se presenta distinto según el interés de cada emisor.","OA N°10 — comparación de fuentes")
q("","Según la tabla del Texto A, ¿cuántos usuarios inscritos se ven afectados en promedio cada mes y qué información relevante **no** entrega?",
 ["2.000 usuarios; no indica cuántos estudiantes hay en total","*2.000 usuarios; no indica dónde podrán nadar mientras dure el cierre","1.200 usuarios; no indica por qué se cerrará la piscina","400 usuarios; no indica cuánto durará el cierre de la piscina"],"b",
 "1.200 estudiantes + 800 adultos mayores = 2.000 usuarios. El texto dice por qué y cuánto dura el cierre, pero no ofrece una alternativa para los usuarios mientras tanto.","OA N°10 — interpretación de una tabla (texto discontinuo)")
q("","¿En qué se diferencian el tono y el propósito de los textos A y B?",
 ["El A es emotivo y busca protestar; el B es neutro y busca informar con cifras","Ambos son neutros y solo buscan informar el horario de la piscina","*El A es informativo y apoya los datos en el municipio; el B es emotivo y busca movilizar","Ambos son emotivos y buscan vender entradas para el campeonato regional"],"c",
 "La nota de radio usa un tono neutro y cita al municipio; la publicación usa mayúsculas y signos de exclamación para provocar una reacción y que otros la compartan.","OA N°10 — comparación de propósitos y tono")
S6="## Sección de Escritura (para las preguntas 22 a 25)\n\n"
q(S6,"¿Por qué sería inadecuado escribir a la directora del liceo un correo que diga «Hola, profe, ¿cómo va? Oiga, queremos un torneo de ajedrez, ¿le tinca?»?",
 ["Porque los correos a una directora deben escribirse siempre en inglés","Porque las preguntas no se pueden usar en ningún correo electrónico","Porque es demasiado largo y debería tener solo una palabra","*Porque usa un registro informal que no corresponde a una autoridad del colegio"],"d",
 "A una autoridad se le escribe con registro formal: saludo como «Estimada directora», sin coloquialismos como «¿le tinca?». El problema no es el idioma ni el largo.","OA N°16 — adecuación del registro")
q("","¿Cuál es la versión corregida de «Los niños se lavó las manos y la profesora les dijo a nosotros que los cuadernos estaban rompidos»?",
 ["*Los niños se lavaron las manos y la profesora nos dijo que los cuadernos estaban rotos","Los niños se lavó las manos y la profesora nos dijo que los cuadernos estaban rotos","Los niños se lavaron las manos y la profesora les dijo a nosotros que estaban rompidos","Los niño se lavaron las mano y la profesora nos dijo que los cuadernos estaba roto"],"a",
 "«Se lavaron» concuerda con «los niños»; «nos dijo» reemplaza a «les dijo a nosotros»; y el participio de «romper» es irregular: «rotos».","OA N°16 — pronombres, conjugaciones y participios")
q("","Debes escribir un texto breve sobre «el cuidado del agua en el liceo». ¿Qué plan de escritura es el más adecuado?, ¿qué opción es adecuada?",
 ["Ideas: mis vacaciones, mi comida favorita y mi mascota. Destinatario: cualquier persona","*Ideas: por qué el agua es escasa y qué puede hacer el liceo. Destinatario: la comunidad escolar","Ideas: todo en un solo párrafo, sin ningún orden. Destinatario: un amigo de otro país","Ideas: copiar un texto de internet sin citar la fuente. Destinatario: el profesor jefe"],"b",
 "Planificar es definir ideas relacionadas con el tema, ordenarlas y pensar en el destinatario. Las otras opciones se salen del tema, no ordenan las ideas o copian sin citar.","OA N°16 — planificación de un texto")
q("","Se enviarán dos mensajes sobre un torneo de ajedrez: uno al grupo del curso y otro a la directora. ¿Qué par usa el registro adecuado para cada destinatario? ¿Qué par de mensajes adecua correctamente el registro a cada destinatario?",
 ["Curso: «Estimados compañeros: junto con saludar, informamos el torneo.» / Directora: «¡Hola dire! ¿Hacemos un torneo?»","Curso: «Torneo de ajedrez el viernes, nada más.» / Directora: «Torneo de ajedrez el viernes, nada más.»","*Curso: «¡Chiquillos, se viene el torneo! Inscríbanse.» / Directora: «Estimada directora: le solicitamos autorizar un torneo.»","Curso: «Les solicitamos formalmente su autorización.» / Directora: «¡Chiquillos, se viene el torneo! Inscríbanse.»"],"c",
 "Entre compañeros cabe un registro informal; a la directora se le escribe con registro formal. Las otras opciones invierten los registros o no comunican nada.","OA N°16 — registro y corrección gramatical")
armar(C/'lengua-y-literatura-examen-forma-b.md', C/'lengua-y-literatura-examen-forma-a.md', Q,
  fila=lambda i,p,cl: f"| {i} | **{cl}.** {p.explicacion} | {p.oa} |",
  reemplazos={"— Forma B":"— Forma A","relación con otras formas: segunda versión (Forma B), con preguntas propias":"relación con otras formas: Forma A, con preguntas propias distintas de la Forma B","última actualización: 2026-08-10":"última actualización: 2026-11-16","*Segunda versión (Forma B) del examen":"*Versión Forma A (distinta de la Forma B) del examen"},
  inicio_preguntas="## Texto 1")
if __name__=="__main__":
    from collections import Counter; print(Counter(p.letra for p in Q), len(Q))
