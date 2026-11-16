import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from forma_a import P, armar  # noqa: E402
C=Path(__file__).resolve().parents[4]/'contenido'/'06-basico/examenes'
A="**{n}. (Alternativas)** "; VFJ="**{n}. (Alternativas — verdadero o falso justificado)** "; V="**{n}. (Varias correctas)** "
Q=[]
def q(sec,en,ops,l,ex,oa,cab=None): Q.append(P(sec,cab or (V if len(l)>1 else A),en,ops,l,ex,oa))
T1='''## Texto 1 (para las preguntas 1 a 2)

### "La olla de la plaza Victoria"

> Rosa tenía once años cuando, la noche del 16 de agosto de 1906, la tierra se sacudió con tanta fuerza en Valparaíso que las casas del plan se vinieron abajo como castillos de naipes. A los temblores siguieron los incendios: desde los cerros, Rosa vio cómo el fuego avanzaba por las calles cercanas al puerto, donde su padre trabajaba cargando barcos.
>
> Esa noche nadie durmió bajo techo. Las familias se refugiaron en la plaza Victoria, envueltas en frazadas, porque el frío de agosto calaba los huesos y nadie se atrevía a volver a las casas agrietadas. Al amanecer, la madre de Rosa juntó a otras vecinas, consiguió una olla enorme y empezó a cocinar porotos con lo que cada familia pudo aportar.
>
> Rosa repartió platos durante tres días seguidos. Le dolían los brazos y tenía las manos llenas de hollín, pero cuando vio llegar a su padre, sucio y cansado, desde el puerto destruido, entendió que esa olla era mucho más que comida: era la forma en que el barrio se mantenía en pie.

### Texto 2 (para las preguntas 3 a 4)

### "El trafkintu de la abuela"

> A Benjamín le parecía aburrido acompañar a su abuela Rosario al trafkintu, el encuentro mapuche de intercambio de semillas que se hacía cada primavera en una escuela rural cerca de Temuco. "¿Para qué cambiar semillas, si en la ferretería las venden en sobres?", le preguntó mientras ella ordenaba, en pequeños paquetes de papel, porotos de colores, quínoa y semillas de maíz.
>
> La abuela no se enojó. Le explicó que esas semillas habían pasado de mano en mano por muchas generaciones, que se adaptaban a la lluvia y al frío de la zona, y que cambiarlas era también una forma de compartir y de conversar. "Si una semilla se pierde, se pierde una historia", le dijo.
>
> En el encuentro, Benjamín vio cómo cada persona contaba de dónde venían sus semillas antes de entregarlas. Una señora le regaló unos porotos con manchas moradas que, según ella, su bisabuela había sembrado. De vuelta a casa, Benjamín los guardó en un frasco con una etiqueta escrita con su mejor letra.

'''
q(T1,"Para entender por qué tantas familias dormían en la plaza en el Texto 1, ¿qué contexto histórico y geográfico conviene conocer?",
 ["El terremoto de 1906, que destruyó gran parte de Valparaíso, una ciudad puerto con cerros y un plan","La Guerra del Pacífico, que obligó a las familias de Valparaíso a huir hacia el norte","La fundación de Valparaíso por los españoles, cuando aún no existían casas en la ciudad","Una gran sequía en el desierto de Atacama, que dejó a las familias sin agua"],"a",
 "El relato menciona la fecha (16 de agosto de 1906), el temblor, los incendios, los cerros y el puerto: corresponde al terremoto que destruyó gran parte de Valparaíso.","OA N°4 — época y lugar")
q("","¿Cómo influye el ambiente del Texto 1 (casas agrietadas, incendios y el frío de agosto) en las acciones de los personajes?",
 ["Las familias duermen en la plaza abrigadas con frazadas y las vecinas organizan una olla común para alimentarse","Las familias se quedan en sus casas porque el frío les impide salir a la calle durante la noche","Los personajes se van de vacaciones al campo porque en invierno no hay trabajo en el puerto","El padre de Rosa decide dejar de trabajar porque el puerto queda lejos de su casa"],"b",
 "Por miedo a las casas dañadas, las familias pasan la noche al aire libre y se abrigan por el frío; al no poder cocinar en sus casas, las vecinas se organizan para compartir alimento.","OA N°4 — influencia del ambiente en las acciones")
q("","«Benjamín acompañó a su abuela al trafkintu porque le interesaba mucho intercambiar semillas desde el principio». ¿Es verdadero o falso, y qué información del texto lo justifica?",
 ["Falso: al comienzo le parecía aburrido y preguntó para qué cambiar semillas si se venden en sobres","Verdadero: el texto dice que Benjamín había organizado el trafkintu de su escuela","Verdadero: Benjamín llevaba años coleccionando semillas en frascos con etiquetas","Falso: Benjamín no fue al trafkintu; solo su abuela participó en el encuentro"],"c",
 "El texto dice que «le parecía aburrido» acompañarla y que cuestionó el intercambio. Su interés aparece después, cuando escucha a su abuela y vive el encuentro.","OA N°4 — motivaciones de los personajes",VFJ)
q("","¿Qué opción presenta una opinión fundamentada sobre el cambio de Benjamín y una conclusión sustentada en el Texto 2 sobre el valor del trafkintu?",
 ["Benjamín cambia al entender que las semillas guardan historias; el trafkintu conserva semillas de la zona y une a la comunidad","Benjamín no cambia, porque al final bota los porotos; el trafkintu solo sirve para vender semillas caras a los vecinos","Benjamín cambia porque su abuela lo castiga; el trafkintu es una actividad obligatoria que organiza la escuela rural","Benjamín cambia porque prefiere las semillas de la ferretería; el trafkintu dejó de realizarse en Chile hace muchos años"],"d",
 "Al final guarda los porotos con cuidado y una etiqueta: valora lo que aprendió. El texto explica que las semillas están adaptadas a la zona y que el intercambio permite compartir y conversar.","OA N°4 — opinión y conclusión")
T3='''## Texto 3 (para las preguntas 5 a 8)

### Poema: "Viaje en el tren del sur"

> Estrofa 1
> Sale el tren de la estación,            (verso 1)
> chucu-chucu, va cantando,               (verso 2)
> **como una oruga de fierro**            (verso 3)
> que entre los cerros va avanzando.      (verso 4)
>
> Estrofa 2
> Por la ventana, los campos              (verso 1)
> pasan verdes y mojados;                 (verso 2)
> llevo un millón de preguntas            (verso 3)
> y los ojos bien abiertos.               (verso 4)

'''
q(T3,"¿Qué figura del lenguaje se usa en el verso «**como una oruga de fierro**»?",
 ["Comparación, porque relaciona el tren con una oruga usando la palabra «como»","Onomatopeya, porque imita el sonido que hace una oruga al moverse","Hipérbole, porque exagera la cantidad de vagones que lleva el tren","Personificación, porque le atribuye al tren la capacidad de pensar"],"b",
 "El verso relaciona dos elementos (el tren y la oruga) mediante «como»: es una comparación. Ambos son largos, tienen partes unidas y avanzan ondulando.","OA N°5 — lenguaje figurado (comparación)")
q("","¿Cuál de las siguientes afirmaciones sobre el poema corresponde a información **explícita** (dicha directamente en el texto)?",
 ["Los campos que se ven por la ventana están verdes y mojados","El hablante viaja a visitar a sus abuelos en el sur","El tren va lleno de pasajeros que conversan entre ellos","El viaje dura toda la noche hasta llegar a Puerto Montt"],"a",
 "El poema dice «los campos / pasan verdes y mojados». Quién visita el hablante, cuántos pasajeros hay o cuánto dura el viaje no aparece en el texto.","OA N°5 — información explícita e implícita")
q("","¿Qué ocurre en la **primera estrofa** del poema, y qué sonido imita la onomatopeya «chucu-chucu»?",
 ["El tren llega a su destino final; imita el silbato del tren al detenerse","Los pasajeros bajan del tren; imita los pasos de las personas en el andén","El hablante mira la lluvia; imita el sonido de las gotas en la ventana","*El tren sale de la estación y avanza entre cerros; imita el ruido del tren en marcha"],"d",
 "La primera estrofa cuenta la salida del tren y su avance entre los cerros. «Chucu-chucu» es una onomatopeya: reproduce con palabras el ruido rítmico del tren al andar.","OA N°5 — interpretación y onomatopeya")
q("","¿Qué opción interpreta correctamente la comparación con la oruga, lo que ocurre en la **segunda estrofa** y un ejemplo de **hipérbole** del poema?",
 ["*El tren es largo y avanza ondulando como una oruga; en la estrofa 2 el hablante mira el paisaje; «un millón de preguntas» es hipérbole","El tren es pequeño y lento como una oruga; en la estrofa 2 el tren se detiene en una estación; «chucu-chucu» es hipérbole","El tren es verde como una oruga; en la estrofa 2 llueve dentro del vagón y todos se mojan; «los ojos bien abiertos» es hipérbole","El tren come hojas como una oruga; en la estrofa 2 el hablante se queda dormido junto a la ventana; «sale el tren» es hipérbole"],"c",
 "La oruga sugiere un tren largo, con partes unidas, que avanza ondulando. En la segunda estrofa el hablante observa el paisaje con curiosidad. Decir «un millón de preguntas» exagera: es una hipérbole.","OA N°5 — interpretación, estrofas e hipérbole")
T4='''## Texto 4 (para las preguntas 9 a 13 y 22): "Agua que viene de la niebla"

**Texto A — "Una comunidad que bebe niebla"**

> En una caleta de la costa de la Región de Coquimbo, donde casi nunca llueve, las familias instalaron hace algunos años grandes mallas en un cerro frente al mar. Cada mañana, la neblina queda atrapada en ellas, y el agua que se junta baja por cañerías hasta un estanque. Gracias a este sistema, la escuela cuenta con agua para el huerto y para los baños, y las familias ya no dependen solo del camión aljibe, que llegaba una vez por semana. Los vecinos se turnan para limpiar las mallas y revisar las cañerías.

Tabla: litros de agua reunidos por día en la caleta (promedio, datos ilustrativos)

| Mes | Litros por día |
|---|---|
| Mayo | 110 |
| Julio | 170 |
| Agosto | 190 |
| Octubre | 130 |

**Texto B — "¿Cómo funciona un atrapanieblas?"**

> En la costa del norte de Chile se forma con frecuencia la camanchaca, una niebla espesa que llega desde el mar y choca con los cerros. Un atrapanieblas es una malla tensada entre dos postes: cuando la niebla la atraviesa, sus pequeñísimas gotas quedan pegadas en los hilos, se juntan, forman gotas más grandes y caen a una canaleta. En Chile, el científico Carlos Espinosa comenzó a estudiar en la década de 1950 cómo capturar agua de la niebla, y hoy existen atrapanieblas en distintas zonas secas del mundo.

'''
q(T4,"Según el Texto B, ¿qué es la camanchaca?",
 ["Una niebla espesa que llega desde el mar y choca con los cerros de la costa","Un tipo de malla que se usa para guardar el agua en los estanques","Una lluvia intensa que cae en el norte de Chile durante el invierno","El nombre del camión aljibe que reparte agua en la caleta"],"c",
 "El Texto B la define directamente: «una niebla espesa que llega desde el mar y choca con los cerros».","OA N°6 — información explícita")
q("","El Texto A no explica por qué las mallas se instalaron en un cerro **frente al mar**. ¿Qué se puede inferir al relacionar ambos textos?",
 ["Que ahí la malla queda protegida de la niebla y nunca se moja con el agua","Que en ese lugar no vive nadie y las mallas no molestan a ningún vecino","Que desde el cerro se ve mejor cuándo llega el camión aljibe a la caleta","*Que la niebla viene del mar y choca con los cerros, donde atraviesa las mallas"],"d",
 "El Texto B dice que la camanchaca llega desde el mar y choca con los cerros; por eso un cerro frente al mar es el lugar donde más niebla atraviesa las mallas. La inferencia une información de los dos textos.","OA N°6 — inferencia a partir de información implícita")
q("","Según la tabla del Texto A, ¿cuál es el **promedio** de litros reunidos por día, considerando los cuatro meses registrados?",
 ["150 litros","600 litros","190 litros","140 litros"],"a",
 "Se suman los cuatro valores: 110 + 170 + 190 + 130 = 600, y se dividen por 4: 600 ÷ 4 = 150 litros. 600 es la suma, no el promedio, y 190 es solo el valor más alto.","OA N°6 — lectura y cálculo a partir de una tabla (texto discontinuo)")
q("","«El Texto A explica cómo se forman las gotas en la malla, y el Texto B cuenta lo que cambió para las familias de la caleta.» ¿Es verdadero o falso?",
 ["Falso: es al revés; el Texto A cuenta lo que cambió en la caleta y el B explica cómo funciona la malla","Verdadero: los dos textos explican exactamente lo mismo, solo que con distintas palabras","Verdadero: el Texto B menciona el huerto de la escuela y los turnos de limpieza de los vecinos","Falso: ninguno de los dos textos habla de atrapanieblas ni de cómo se obtiene el agua de la niebla"],"b",
 "El Texto A narra la experiencia de la caleta (agua para la escuela, menos dependencia del camión aljibe) y el Texto B explica el funcionamiento de la malla y la camanchaca.","OA N°6 — comparación de información entre dos textos",VFJ)
q("","¿Qué opción identifica qué tienen en común el Texto A y el Texto B y da una opinión fundamentada en ambos sobre instalar atrapanieblas en otras zonas secas?",
 ["Ambos hablan del mar; conviene instalar atrapanieblas en cualquier lugar del mundo, aunque allí no haya niebla","Ambos critican los atrapanieblas; no conviene instalarlos porque el agua de la niebla es salada y no sirve","Ambos cuentan la vida de Carlos Espinosa; conviene instalarlos solo en la Región de Coquimbo y en ninguna otra","*Ambos tratan de sacar agua de la niebla; conviene instalarlos donde hay camanchaca, porque dan agua sin lluvia"],"d",
 "Los dos textos tratan sobre captar agua de la niebla. La opinión se fundamenta en ambos: el B explica que se necesita niebla que choque con los cerros y el A muestra el beneficio para una comunidad sin lluvia.","OA N°6 — comparación y opinión fundamentada")
T5='''## Texto 5 (para las preguntas 14 a 17): "Nueva ciclovía en avenida Los Robles"

**Fuente 1 — Comunicado de la Municipalidad de Puerto Claro**

> **¡Nueva ciclovía segura en avenida Los Robles!**
> La Municipalidad de Puerto Claro informa que ya está abierta la nueva ciclovía de 3 kilómetros en avenida Los Robles, que conecta tres colegios con la plaza principal. La obra busca que niñas, niños y adultos se trasladen de forma segura, sana y sin contaminar. Se espera que cientos de estudiantes la usen cada día.
> — Departamento de Comunicaciones, Municipalidad de Puerto Claro

**Fuente 2 — Reportaje del diario local *El Vecino***

> **La nueva ciclovía divide opiniones en avenida Los Robles**
> Mientras muchos ciclistas celebran la nueva vía, algunos comerciantes de la avenida reclaman porque se eliminaron estacionamientos frente a sus locales y temen perder clientes. La Municipalidad respondió que habilitará estacionamientos en una calle lateral, aunque todavía no ha indicado cuándo.

*(Puerto Claro es una comuna ficticia, creada para esta prueba.)*

'''
q(T5,"¿Quién es el **emisor** de la Fuente 2?",
 ["El diario local *El Vecino*","La Municipalidad de Puerto Claro","Los comerciantes de la avenida","Los ciclistas de la comuna"],"c",
 "La Fuente 2 es un reportaje publicado por el diario *El Vecino*: el diario es el emisor. Los comerciantes y los ciclistas son personas cuyas opiniones recoge el reportaje.","OA N°7 — emisor")
q("","¿Cuál de las siguientes afirmaciones es **verdadera** según la Fuente 2?",
 ["Algunos comerciantes reclaman porque se eliminaron estacionamientos frente a sus locales","Todos los vecinos de la avenida están en contra de la ciclovía y quieren que la eliminen","La ciclovía tiene 10 kilómetros y llega desde la plaza principal hasta la costa","La Municipalidad ya construyó los nuevos estacionamientos en una calle lateral"],"a",
 "La Fuente 2 dice que «algunos comerciantes» reclaman por los estacionamientos. No dice que todos los vecinos estén en contra, y los estacionamientos nuevos aún no tienen fecha.","OA N°7 — información explícita en textos comparados")
q("","Si quisieras saber **cuántos estacionamientos** se eliminaron en la avenida, ¿qué afirmación es correcta?",
 ["La Fuente 1 lo dice: se eliminaron 3 estacionamientos, uno por cada colegio","*Ninguna fuente lo dice; habría que consultar a la Municipalidad o a otra fuente confiable","La Fuente 2 lo dice: se eliminaron cientos de estacionamientos","No es necesario saberlo, porque la información de un texto siempre es completa"],"b",
 "Ninguna de las dos fuentes entrega esa cifra: los «3 kilómetros» y los «cientos de estudiantes» se refieren a otra cosa. Cuando un texto no basta, hay que buscar otra fuente confiable.","OA N°7 — suficiencia de la información")
q("","¿Qué opción describe correctamente el propósito de cada fuente y por qué conviene identificarlo antes de aceptar lo que dice un texto?",
 ["Las dos fuentes buscan vender bicicletas a los vecinos; identificar el propósito de un texto no cambia nada","La Fuente 1 critica la ciclovía y la Fuente 2 solo la celebra; por eso ambas entregan la misma información","*La Fuente 1 destaca su propia obra y la Fuente 2 recoge opiniones distintas; saberlo ayuda a leer críticamente","La Fuente 2 fue escrita por la Municipalidad; por eso es imposible que contenga errores o que omita información"],"c",
 "La Municipalidad presenta su obra de forma positiva; el diario muestra a favor y en contra. Saber para qué escribe cada emisor ayuda a detectar lo que destaca u omite.","OA N°7 — propósito del emisor")
S6="## Sección de Escritura narrativa (para las preguntas 18 a 21)\n\n"
q(S6,"¿Qué es el **clímax** de un relato?",
 ["El momento de mayor tensión, cuando el conflicto llega a su punto más intenso","La presentación de los personajes y del lugar donde ocurre la historia","La lista de palabras difíciles que aparece al final del cuento","El título del relato, que resume en pocas palabras lo que ocurre"],"a",
 "El clímax es el punto de mayor tensión del conflicto, justo antes de que empiece a resolverse. La presentación de personajes y lugar corresponde al inicio.","OA N°14 — estructura del conflicto en una narración")
q("","En el fragmento: «Tomás y Diego encontraron un perro perdido. Él lo tomó en brazos y lo llevó a su casa», ¿qué problema tiene la segunda oración y cómo se corrige?",
 ["Tiene una falta de ortografía; se corrige escribiendo «perro» con una sola r","Es demasiado corta; se corrige agregando muchos adjetivos sobre el perro","No tiene problema; los pronombres siempre dejan claro de quién se habla","*No se sabe quién es «él»; se corrige escribiendo el nombre: «Diego lo tomó en brazos»"],"d",
 "Hay dos personajes masculinos y «él» puede referirse a cualquiera: es un referente ambiguo. Escribir el nombre deja claro quién realiza la acción.","OA N°14 — identificación de referentes ambiguos")
q("","Elige el **comienzo** de relato que mejor presenta a un personaje y un lugar, incluye un conector y deja claro de quién se habla:",
 ["Ella llegó al lugar y él también, y después pasó eso que nadie esperaba ni se imaginaba","*Apenas sonó la campana, Florencia corrió por el pasillo frío del colegio hacia la biblioteca","Fin. Y así todos fueron muy felices, comieron perdices y nunca más se volvieron a ver","Había una vez. Un colegio. Un pasillo muy largo. Una biblioteca. Una campana. Una niña"],"b",
 "Presenta a Florencia, el lugar (el pasillo frío del colegio) y usa el conector «apenas». La primera opción no dice quiénes son «ella» y «él», y las otras no presentan personaje ni ambiente.","OA N°14 — escritura del inicio de una narración")
q("","Elige el **diálogo** que presenta un problema y su solución, indica quién dice cada línea y describe dónde ocurre:",
 ["—Hola, ¿cómo estás? —dijo alguien en algún lugar. —Bien, gracias, ¿y tú? —respondió otro. Y después los dos se fueron","—¿Vamos ahora o más tarde? —Ya, vamos cuando quieras. —Bueno, como tú digas. —Chao, nos vemos mañana entonces","*—Se cortó la luz y no encuentro la linterna —dijo Javiera en la sala oscura. / —Tengo una aquí —respondió Martín, y la encendió","—Me gusta mucho el helado de chocolate —dijo Pedro en el patio soleado. —A mí también me gusta mucho —dijo Ana."],"c",
 "El diálogo correcto plantea un problema (se cortó la luz y no hay linterna), lo resuelve (Martín la enciende), indica quién habla y describe el ambiente (la sala oscura).","OA N°14 — diálogo con conflicto resuelto y referentes claros")
S7="## Sección de Escritura informativa (para las preguntas 22 a 25)\n\n"
q(S7,"Dentro del **Texto 4**, ¿cuál es la idea central del **Texto A** («Una comunidad que bebe niebla»)?",
 ["Que la camanchaca se forma porque la niebla del mar choca con los cerros de la costa","Que el científico Carlos Espinosa estudió la niebla en Chile durante la década de 1950","Que el camión aljibe llegaba a la caleta una sola vez por semana con agua para beber","*Que los atrapanieblas cambiaron la vida de una caleta sin lluvia y de su escuela"],"d",
 "Los atrapanieblas dieron agua a la caleta y a su escuela: de eso trata el Texto A. La formación de la camanchaca y Carlos Espinosa son ideas del Texto B, y el camión aljibe es solo un detalle.","OA N°15 — idea central por párrafo")
q("","¿Para qué sirven los **subtítulos** en un artículo informativo?",
 ["Para anticipar de qué trata cada sección y ayudar a ubicar la información","Para reemplazar los párrafos y no tener que escribir el artículo completo","Para contar el final del artículo antes de que el lector empiece","Para agregar chistes que hagan más entretenido el texto"],"a",
 "Los subtítulos organizan el artículo por secciones: el lector sabe de qué tratará cada parte y encuentra más fácil lo que busca.","OA N°15 — estructura y organización del artículo informativo")
q("","En un artículo sobre los atrapanieblas, ¿qué conector es adecuado para introducir un **ejemplo**?",
 ["«Por ejemplo», como en: «Hay zonas secas con niebla; por ejemplo, la costa del norte de Chile»","«Sin embargo», como en: «Hay zonas secas con niebla; sin embargo, la costa del norte de Chile»","«En cambio», como en: «Hay zonas secas con niebla; en cambio, la costa del norte de Chile»","«Aunque», como en: «Hay zonas secas con niebla; aunque la costa del norte de Chile»"],"b",
 "«Por ejemplo» introduce un caso concreto de lo que se acaba de decir. «Sin embargo», «en cambio» y «aunque» expresan oposición, y las oraciones quedan sin sentido.","OA N°15 — conectores en el artículo informativo")
q("","Debes planificar un artículo informativo breve sobre «los beneficios de leer todos los días». ¿Qué elementos debería incluir tu planificación?",
 ["Una oración inicial que presente el tema con claridad","Dos ideas centrales distintas, una por párrafo, unidas con conectores","Un final con una opinión sobre un tema que no tiene relación con la lectura","Al menos dos fuentes confiables, como una biblioteca pública o un estudio sobre lectura"],"abd",
 "a, b y d. Un buen artículo presenta el tema, desarrolla una idea central por párrafo y se apoya en fuentes confiables. Cerrar con un tema sin relación rompe la coherencia del texto.","OA N°15 — planificación de un artículo informativo con fuentes")
armar(C/'lenguaje-y-comunicacion-examen-forma-b.md', C/'lenguaje-y-comunicacion-examen-forma-a.md', Q,
  fila=lambda i,p,cl: f"| {i} | **{cl}.** {p.explicacion.split('. ',1)[1] if len(p.letra)>1 else p.explicacion} | {p.oa} |",
  reemplazos={"— Forma B":"— Forma A","(Forma B)":"(Forma A)","ultima_actualizacion: 2026-11-02":"ultima_actualizacion: 2026-11-16"},
  inicio_preguntas="## Texto 1")
if __name__=="__main__":
    from collections import Counter; print(Counter(p.letra for p in Q), len(Q))
