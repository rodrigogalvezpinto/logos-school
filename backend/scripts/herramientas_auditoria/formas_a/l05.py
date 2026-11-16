import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from forma_a import P, armar  # noqa: E402
C=Path(__file__).resolve().parents[4]/'contenido'/'05-basico/examenes'
A="**{n}. (Alternativas)** "; V="**{n}. (Varias correctas)** "
Q=[]
def q(sec,en,ops,l,ex,oa): Q.append(P(sec,V if len(l)>1 else A,en,ops,l,ex,oa))
T1='''## Texto 1 (para las preguntas 1 a 4)

### "El violín de la abuela Elsa"

> Martina encontró el estuche negro arriba del ropero, cubierto de polvo, mientras buscaba una frazada en la casa de su abuela, en Chillán. Adentro había un violín con una grieta larga en la madera y dos cuerdas cortadas. "¿Es tuyo, abuela?", preguntó emocionada. La abuela Elsa miró el instrumento con sus dedos torcidos y temblorosos entrelazados sobre el delantal, y respondió en voz baja: "Guárdalo, mijita. Eso ya pasó".
>
> Pero Martina no lo guardó. Al día siguiente lo llevó, con permiso de su mamá, al taller de don Hernán, un luthier que arreglaba instrumentos en una calle cercana a la feria. Don Hernán pasó la mano por la grieta como quien acaricia a un gato y dijo: "Este violín estuvo dormido mucho tiempo, pero no está muerto". Tardó tres semanas en repararlo.
>
> Martina practicó todas las tardes una tonada que su abuela tarareaba mientras cocinaba. Al principio el violín chillaba como una puerta vieja, pero poco a poco las notas salieron limpias. El día del acto de fin de año, Martina tocó la tonada frente a todo el colegio. En la tercera fila, la abuela Elsa escuchaba con los ojos cerrados y, cuando terminó la música, se secó las lágrimas con la punta del pañuelo.

'''
q(T1,"¿Qué característica física de la abuela Elsa es relevante en el relato y qué permite comprender?",
 ["Sus dedos torcidos y temblorosos, que permiten comprender por qué ya no toca el violín","Su pelo blanco y largo, que permite comprender que vive sola en Chillán","Su delantal de cocina, que permite comprender que no le gusta la música","Su voz baja, que permite comprender que está enferma y no puede ir al acto"],"c",
 "Los dedos torcidos y temblorosos explican que la abuela ya no puede tocar; por eso guardó el violín y dice «Eso ya pasó». El texto no dice que viva sola, que no le guste la música ni que esté enferma.","OA N°4 — características físicas relevantes")
q("",'¿Qué afirmaciones sobre la frase de don Hernán «Este violín estuvo dormido mucho tiempo, pero no está muerto» son correctas?',
 ["Es una personificación, porque le atribuye al violín algo propio de un ser vivo: dormir","Sugiere que el violín puede volver a sonar si se repara y se toca","Significa que el violín está roto para siempre y ya no se puede usar","Es una comparación, porque usa la palabra «como» para unir dos ideas"],"ab",
 "Decir que el violín «dormía» y «no está muerto» es una personificación, y sugiere que, aunque estuvo sin usarse, puede volver a sonar. No es una comparación: en esa frase no aparece «como».","OA N°4 — lenguaje figurado en narraciones")
q("","Cuando Martina le pregunta por el violín, la abuela responde en voz baja: «Guárdalo, mijita. Eso ya pasó». ¿Qué se puede inferir de esta reacción?",
 ["Que el violín le trae recuerdos que la ponen triste, porque ya no puede tocarlo","Que está enojada con Martina por haber revisado el ropero sin permiso","Que nunca le gustó el violín y quiere botarlo lo antes posible","Que el violín es de otra persona y no quiere que Martina lo toque"],"a",
 "La voz baja y la frase «eso ya pasó» muestran nostalgia: el violín es parte de su pasado y le recuerda algo que ya no puede hacer. El final, cuando llora al escuchar la tonada, confirma que el violín era importante para ella.","OA N°4 — inferencia sobre personajes")
q("","¿Por qué la abuela se seca las lágrimas al final del relato?",
 ["Porque se emociona al escuchar su tonada en el violín que creía perdido, tocada por su nieta","Porque la música estaba muy fuerte y le molestaron los oídos durante el acto","Porque se enojó al ver que Martina se llevó el violín sin preguntarle a ella","Porque se aburrió esperando en la tercera fila hasta que terminara el acto"],"d",
 "La abuela escucha «con los ojos cerrados» la tonada que ella misma tarareaba, en su propio violín reparado: las lágrimas son de emoción. Nada en el texto indica enojo, molestia ni aburrimiento.","OA N°4 — interpretación del desenlace")
T2='''## Texto 2 (para las preguntas 5 a 8)

### Poema: "Tarde de lluvia"

> Estrofa 1
> La lluvia toca el techo de zinc            (verso 1)
> con dedos finos de cristal.                (verso 2)
> La calle es un río sin prisa               (verso 3)
> que lleva las hojas hacia el mar.          (verso 4)
>
> Estrofa 2
> Mi perro duerme junto al fuego,            (verso 1)
> el viento silba en el portón,              (verso 2)
> y el pan caliente de la tarde              (verso 3)
> perfuma toda la habitación.                (verso 4)

'''
q(T2,"¿Qué tipo de rima forman las palabras «portón» y «habitación»?",
 ["Rima consonante, porque coinciden vocales y consonantes desde la última vocal tónica","Rima asonante, porque solo coinciden las vocales desde la última vocal acentuada","No riman, porque las dos palabras tienen distinta cantidad de sílabas y de letras","Rima consonante, porque las dos palabras empiezan con una letra consonante"],"b",
 "Desde la última vocal acentuada, «portÓN» y «habitaciÓN» terminan igual, con vocal y consonante (-ón): es rima consonante. La cantidad de sílabas y la letra inicial no importan para la rima.","OA N°5 — elementos formales del poema (rima)")
q("","¿Cuál de los siguientes versos del poema es una **metáfora** (y no una personificación)?",
 ["«La calle es un río sin prisa»","«La lluvia toca el techo de zinc»","«el viento silba en el portón»","«Mi perro duerme junto al fuego»"],"d",
 "«La calle es un río» identifica directamente la calle con un río, sin usar «como»: es una metáfora. La lluvia que «toca» y el viento que «silba» son personificaciones, y el perro que duerme es una descripción literal.","OA N°5 — lenguaje figurado (metáfora)")
q("","En el verso «La lluvia toca el techo de zinc», ¿qué figura se usa y qué imagen transmite?",
 ["Una personificación: la lluvia «toca» como un músico, y transmite el sonido rítmico de las gotas","Una comparación: la lluvia es como el zinc, y transmite que el techo está frío","Una metáfora: el techo es una lluvia, y transmite que la casa se está inundando","Una exageración: la lluvia rompe el techo, y transmite una tormenta peligrosa"],"a",
 "Tocar es una acción humana; atribuida a la lluvia, la convierte en un músico que hace sonar el techo, y el lector imagina el golpeteo rítmico de las gotas.","OA N°5 — personificación explicada")
q("","¿A qué sentidos apelan los versos «el viento silba en el portón» y «el pan caliente de la tarde / perfuma toda la habitación», y qué atmósfera crean?",
 ["Al oído y al olfato; crean una atmósfera acogedora de hogar en un día de lluvia","A la vista y al gusto; crean una atmósfera de miedo por la tormenta","Al tacto y a la vista; crean una atmósfera de soledad y frío","Solo al olfato; crean una atmósfera de apuro antes de que llegue la noche"],"c",
 "El silbido del viento se escucha (oído) y el pan perfuma (olfato). Junto al perro que duerme junto al fuego, dan una sensación de calma y abrigo dentro de la casa mientras llueve afuera.","OA N°5 — sentidos y atmósfera")
T3='''## Texto 3 (para las preguntas 9 a 13)

### "El huemul, un ciervo que necesita ayuda"

> **Un símbolo de Chile**
> El huemul es un ciervo nativo de la cordillera del sur de Chile y de Argentina. Es tan importante para nuestro país que aparece junto al cóndor en el escudo nacional. Vive en bosques y laderas de montaña, y se alimenta de hojas, brotes y pastos.
>
> **Cada vez menos huemules**
> Hoy el huemul está en peligro de extinción: quedan muy pocos ejemplares, repartidos en grupos pequeños y separados entre sí. Sus principales amenazas son la caza ilegal, la pérdida de los bosques donde vive y los ataques de perros. Además, el ganado puede transmitirle enfermedades.
>
> **Cómo protegerlo**
> Parte de los huemules vive dentro de parques y reservas nacionales, donde guardaparques vigilan su territorio y registran cuántos animales observan. En varias de estas áreas se pide a los visitantes no llevar perros y no salir de los senderos.

Tabla: ciervos nativos de Chile

| Especie | Dónde vive | Altura aproximada | Estado de conservación |
|---|---|---|---|
| Huemul | Cordillera de Ñuble y desde Aysén hasta Magallanes | Cerca de 1 m | En peligro |
| Pudú | Bosques húmedos del sur, del Maule a Aysén | Unos 40 cm | Vulnerable |
| Taruca | Altiplano de Arica y Parinacota | Unos 75 cm | En peligro |

'''
q(T3,"Según el texto, ¿cuáles son las principales amenazas del huemul?",
 ["La caza ilegal, la pérdida de los bosques y los ataques de perros","El frío de la cordillera y la falta de pasto en invierno","Los cóndores que lo atacan en las laderas de montaña","Los guardaparques que lo cuentan dentro de las reservas"],"b",
 "El segundo párrafo nombra la caza ilegal, la pérdida de los bosques y los ataques de perros, y agrega las enfermedades que transmite el ganado. El frío, los cóndores y los guardaparques no se mencionan como amenazas.","OA N°6 — información explícita")
q("","El texto no explica por qué en algunas reservas se pide a los visitantes no llevar perros. ¿Qué información del propio texto permite inferirlo?",
 ["Que los ataques de perros son una de las principales amenazas del huemul","Que el huemul aparece junto al cóndor en el escudo nacional de Chile","Que el huemul se alimenta de hojas, brotes y pastos de la montaña","Que los guardaparques registran cuántos huemules observan cada año"],"d",
 "Si los perros atacan a los huemules, pedir que no entren a las reservas los protege. La inferencia une dos partes del texto: las amenazas del segundo párrafo y la medida del tercero.","OA N°6 — inferencia")
q("","Según la tabla, ¿qué ciervo vive en una zona muy alejada de la de los otros dos?",
 ["La taruca, porque vive en el altiplano del extremo norte","El huemul, porque solo vive en Magallanes","El pudú, porque vive en los bosques húmedos","Ninguno, porque los tres viven en la misma región"],"c",
 "La taruca vive en el altiplano de Arica y Parinacota, en el extremo norte; el huemul y el pudú viven en el centro-sur y el sur. Además, el huemul no vive solo en Magallanes: también está en Ñuble y en Aysén.","OA N°6 — lectura de textos discontinuos (tabla)")
q("","Al comparar la información de la tabla, ¿qué afirmación es correcta?",
 ["El pudú es el más pequeño y el único de los tres que está «vulnerable»","El huemul es el más pequeño de los tres y es el único que está en peligro","La taruca es la más alta de los tres y es la única que vive en bosques","Los tres ciervos tienen la misma altura y el mismo estado de conservación"],"a",
 "El pudú mide unos 40 cm, menos que la taruca (75 cm) y el huemul (1 m), y es el único «vulnerable»; los otros dos están «en peligro».","OA N°6 — relación entre datos de una tabla")
q("","¿Qué opinión sobre los parques y reservas nacionales está mejor fundamentada en el texto?",
 ["Son importantes, porque el huemul está en peligro y allí se vigila su territorio y se evitan los perros","Son innecesarios, porque el huemul ya aparece en el escudo y eso basta para protegerlo","Son peligrosos para el huemul, porque los guardaparques lo molestan cada vez que lo cuentan","Son útiles solo para los turistas, porque allí pueden caminar tranquilos por los senderos"],"b",
 "Una opinión fundamentada se apoya en información del texto: el segundo párrafo dice que el huemul está en peligro y el tercero, que en las reservas se vigila su territorio y se limitan amenazas.","OA N°6 — relación entre párrafos y opinión fundamentada")
T4='''## Texto 4 (para las preguntas 14 a 17)

### Afiche: "Gran Jornada de Reciclaje"

> **¡Gran Jornada de Reciclaje en Villa Los Aromos!**
> La Junta de Vecinos N.° 14 invita a todos los vecinos y vecinas a traer sus botellas plásticas, latas y cartones limpios el **sábado 12 de octubre, de 10:00 a 13:00 horas**, en la sede vecinal (Los Aromos 345).
>
> Por cada bolsa de materiales reciclables, recibirás un plantín de árbol nativo para plantar en tu casa o en la plaza.
>
> ¡Cuidar el barrio es tarea de todos!
>
> — Junta de Vecinos N.° 14, Villa Los Aromos

'''
q(T4,"¿Cuál es el propósito principal del afiche?",
 ["Invitar a los vecinos a llevar materiales reciclables y motivarlos a cuidar el barrio","Explicar cómo se fabrica el plástico de las botellas y por qué contamina","Vender plantines de árboles nativos a los vecinos de la villa","Informar el reglamento de la Junta de Vecinos para elegir a su directiva"],"d",
 "El afiche invita a una actividad con fecha, hora y lugar, ofrece un incentivo (el plantín) y cierra con una frase que motiva a participar. No explica procesos, no vende ni presenta un reglamento.","OA N°7 — propósito del texto")
q("","Un vecino quiere saber si puede llevar frascos de vidrio a la jornada. ¿Qué afirmación es correcta?",
 ["No lo dice: solo nombra plástico, latas y cartones; conviene preguntar a la Junta de Vecinos","Sí: el afiche dice que se reciben todos los materiales que se puedan reciclar","Sí: el afiche dice que cada bolsa de vidrio se cambia por dos plantines de árbol nativo","No: el afiche prohíbe llevar vidrio a la sede porque es peligroso para los niños"],"c",
 "El afiche menciona solo botellas plásticas, latas y cartones; no dice nada del vidrio, ni para aceptarlo ni para prohibirlo. Para saberlo hay que consultar al emisor, la Junta de Vecinos.","OA N°7 — suficiencia de la información")
q("","¿Para qué sirve la frase final del afiche, «¡Cuidar el barrio es tarea de todos!»?",
 ["Para convencer a los lectores de participar, haciéndolos sentir responsables del barrio","Para informar la dirección exacta de la sede vecinal donde será la jornada","Para explicar qué materiales se pueden reciclar en la jornada y cuáles no","Para indicar el horario exacto en que se entregarán los plantines de árboles"],"a",
 "Es una frase persuasiva: apela a la responsabilidad compartida para motivar a participar. La dirección, los materiales y el horario aparecen en otras partes del afiche.","OA N°7 — recursos persuasivos")
q("","¿Qué datos del afiche ayudan a saber **cuándo y dónde** llevar los materiales?",
 ["«sábado 12 de octubre»","«de 10:00 a 13:00 horas»","«¡Cuidar el barrio es tarea de todos!»","«en la sede vecinal (Los Aromos 345)»"],"abd",
 "La fecha y el horario dicen cuándo, y la sede vecinal con su dirección dice dónde. La frase «¡Cuidar el barrio es tarea de todos!» motiva a participar, pero no entrega información de fecha ni lugar.","OA N°7 — evaluación de la información")
S5="## Sección de Escritura narrativa (para las preguntas 18 a 21)\n\n"
q(S5,"¿Qué función cumple el **desenlace** de un cuento?",
 ["Muestra cómo se resuelve el conflicto y cómo termina la historia","Presenta a los personajes, el lugar y el momento de la historia","Plantea por primera vez el problema que enfrentan los personajes","Enumera las fuentes que el autor consultó para escribir"],"b",
 "El desenlace es la parte final: allí se resuelve (o no) el conflicto. La presentación de personajes y lugar corresponde al inicio, y el problema aparece en el desarrollo.","OA N°14 — estructura narrativa")
q("","¿Qué descripción del ambiente de un mercado en la mañana usa **detalles sensoriales** de al menos dos sentidos?",
 ["Los gritos de los vendedores se mezclaban con el aroma de las frutillas maduras","El mercado abre a las ocho de la mañana y cierra a las cuatro de la tarde, todos los días","En el mercado venden frutas, verduras, pescados, quesos y muchos otros productos","El mercado es un lugar grande que queda en el centro de la ciudad"],"d",
 "Los gritos se oyen y el aroma de las frutillas se huele: la descripción apela al oído y al olfato. Las otras opciones solo informan horarios, productos o ubicación.","OA N°14 — descripción del ambiente")
q("","¿Qué conector sirve para introducir un **cambio inesperado** en un relato?",
 ["De pronto","Primero","Finalmente","Al día siguiente"],"b",
 "«De pronto» anuncia algo que ocurre sin aviso y cambia el rumbo de la historia. «Primero», «al día siguiente» y «finalmente» solo ordenan los hechos en el tiempo.","OA N°14 — conectores en la narración")
q("","¿Qué inicio de cuento presenta mejor al **personaje**, el **lugar** y el **momento** de la historia?",
 ["Una mañana de invierno, en una caleta de Chiloé, Ignacio despertó con el ruido de los botes","Y entonces todos aplaudieron, y la fiesta terminó muy tarde esa noche","Había muchas cosas que hacer ese día y nadie sabía muy bien por dónde empezar","Los cuentos tienen inicio, desarrollo y desenlace, y siempre deben llevar un título"],"c",
 "Esa opción dice cuándo («una mañana de invierno»), dónde («una caleta de Chiloé») y quién («Ignacio»). Las demás son un final, una oración sin datos concretos o una explicación sobre los cuentos.","OA N°14 — inicio de una narración")
S6="## Sección de Escritura informativa (para las preguntas 22 a 25)\n\n"
q(S6,"¿Qué debe lograr la **introducción** de un artículo informativo?",
 ["Presentar el tema y despertar el interés de quien lee","Contar una historia inventada con personajes y diálogos","Dar la opinión personal del autor sin ningún dato","Enumerar las fuentes consultadas sin explicar el tema"],"a",
 "La introducción presenta de qué tratará el artículo y motiva a seguir leyendo; el desarrollo entrega la información y las fuentes se indican al final.","OA N°15 — organización del artículo")
T6='''### Texto adicional (para la pregunta 23): "Las abejas nativas de Chile"

> Cuando pensamos en abejas, solemos imaginar a la abeja de miel, que vive en colmenas. Sin embargo, esa abeja llegó desde Europa. En Chile existen cientos de especies de abejas nativas, muchas de las cuales solo viven en nuestro país.
>
> A diferencia de la abeja de miel, la mayoría de las abejas nativas vive sola: cada hembra construye su propio nido en el suelo, en la madera o en tallos huecos, y allí deja alimento para sus crías. Por eso no forman colmenas ni producen miel para las personas.
>
> Aunque no den miel, las abejas nativas son muy importantes, porque polinizan plantas silvestres y cultivos. Hoy están amenazadas por la pérdida de las flores nativas y el uso de plaguicidas.

'''
q(T6,"Según el artículo «Las abejas nativas de Chile», ¿cuál es la idea central del **segundo párrafo**?",
 ["Que la mayoría de las abejas nativas vive sola, en su nido, y no produce miel","Que la abeja de miel llegó a Chile desde Europa y vive en grandes colmenas","Que las abejas nativas polinizan plantas y cultivos, y están amenazadas","Que en Chile hay cientos de especies de abejas nativas y muchas son únicas"],"d",
 "El segundo párrafo explica cómo viven las abejas nativas: solas, en nidos propios y sin formar colmenas. La abeja de miel y la cantidad de especies son del primer párrafo; la polinización y las amenazas, del tercero.","OA N°15 — idea central de un párrafo")
q("","¿Qué oración usa un **conector de causa** de forma adecuada para un artículo informativo?",
 ["Las abejas nativas son importantes, porque polinizan muchas plantas silvestres","Las abejas nativas son importantes; sin embargo, polinizan muchas plantas silvestres","Las abejas nativas son importantes; finalmente, polinizan muchas plantas silvestres","Las abejas nativas son importantes; por ejemplo, el cielo estaba nublado"],"c",
 "«Porque» introduce la causa: explica por qué son importantes. «Sin embargo» indica oposición y «finalmente» cierra una enumeración, así que no corresponden; la última oración, además, no tiene relación con el tema.","OA N°15 — conectores en textos informativos")
q("","Debes escribir un artículo informativo sobre la importancia de dormir bien. ¿Qué título es más adecuado?",
 ["«Dormir bien: por qué importa y cómo lograrlo»","«La noche en que la almohada aprendió a hablar»","«Mi opinión sobre todas las cosas que me pasan»","«Había una vez un niño que tenía mucho sueño»"],"b",
 "El título «Dormir bien» anuncia el tema y «por qué importa y cómo lograrlo» dice lo que encontrará el lector. Un título informativo anuncia con claridad el tema y lo que encontrará el lector. Los otros parecen títulos de cuentos o son tan generales que no dicen de qué trata el artículo.","OA N°15 — planificación de un artículo informativo")
armar(C/'lenguaje-y-comunicacion-examen-forma-b.md', C/'lenguaje-y-comunicacion-examen-forma-a.md', Q,
  fila=lambda i,p,cl: f"| {i} | **{cl}.** {p.explicacion} | {p.oa} |",
  reemplazos={"(Forma B)":"(Forma A)","denominada \"Forma B\"":"denominada \"Forma A\"","denominada **Forma B**":"denominada **Forma A**","ni con la guía de estudio)":"ni con la guía de estudio ni con la Forma B)","última actualización: 2026-08-11":"última actualización: 2026-11-16"},
  inicio_preguntas="## Texto 1")
from collections import Counter; print(Counter(p.letra for p in Q), len(Q))
