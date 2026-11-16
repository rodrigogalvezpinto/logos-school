import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from forma_a import P, armar  # noqa: E402
C=Path(__file__).resolve().parents[4]/'contenido'/'06-basico/examenes'
Q=[]
def q(sec,pts,en,ops,l,ex,oa):
    tipo="Varias correctas" if len(l)>1 else "Alternativas"
    cab="**{n}.** *(%s%s)* "%(tipo,"" if pts==1 else f", {pts} puntos")
    Q.append(P(sec,cab,en,ops,l,ex,oa,{"tipo":tipo}))
q("## Eje 1: Ciencias de la Vida (Preguntas 1 a 12)\n\n### OA N°1 — La fotosíntesis\n\n",1,"¿En qué parte de la planta ocurre principalmente la fotosíntesis?",
 ["En las hojas, en células que tienen clorofila","En las raíces, que están bajo la tierra","En las flores, que atraen a los insectos","En la corteza seca del tronco"],"c",
 "Las hojas tienen muchas células con clorofila, el pigmento verde que capta la luz del sol. Las raíces absorben agua y las flores participan en la reproducción.","OA 1")
q("",1,"¿Qué gas liberan las plantas al ambiente durante la fotosíntesis?",
 ["Oxígeno","Dióxido de carbono","Nitrógeno","Monóxido de carbono"],"a",
 "En la fotosíntesis la planta toma dióxido de carbono y agua, y con la energía de la luz fabrica glucosa y libera oxígeno, que respiran los seres vivos.","OA 1")
q("",3,"Dos plantas iguales se dejan junto a una ventana con buena luz. Una se riega todos los días y la otra no recibe agua durante dos semanas. ¿Qué le ocurrirá a la planta sin agua y por qué?",
 ["Se marchitará, porque el agua es un ingrediente que necesita para fabricar su alimento","Crecerá más rápido, porque al no tener agua aprovecha mejor la luz que recibe por la ventana","No le pasará nada, porque las plantas obtienen todo su alimento solo de la luz del sol","Producirá más oxígeno, porque sin agua la fotosíntesis ocurre con mucha más rapidez"],"b",
 "Sin agua la planta no puede hacer fotosíntesis aunque tenga luz: no fabrica su alimento y se marchita. La luz es necesaria, pero no basta por sí sola.","OA 1")
q("### OA N°2 — Cadenas y redes alimentarias\n\n",1,"¿Qué función cumple un organismo **productor** en una cadena alimentaria?",
 ["Fabrica su propio alimento mediante la fotosíntesis y es el primer eslabón de la cadena","Se alimenta solo de otros animales y ocupa el último eslabón de la cadena","Descompone los restos de seres vivos y devuelve nutrientes al suelo","Se alimenta de plantas y es comido por los carnívoros de la cadena"],"d",
 "Los productores, como las plantas y las algas, fabrican su alimento con la luz del sol y son la base de la que dependen todos los demás eslabones.","OA 2")
q("",1,"En un ecosistema de la zona central existe la cadena: pasto → conejo → zorro culpeo. Si desaparecieran los zorros, ¿qué ocurriría con mayor probabilidad?",
 ["Aumentaría la cantidad de conejos y disminuiría el pasto","Disminuiría la cantidad de conejos y aumentaría el pasto","Desaparecerían al mismo tiempo los conejos y el pasto","No cambiaría nada, porque los zorros no comen pasto"],"c",
 "Sin su depredador, los conejos aumentarían; al haber más conejos, comerían más pasto y este disminuiría. Un cambio en un eslabón afecta a toda la cadena.","OA 2")
q("",3,"¿Por qué una **red** alimentaria representa mejor lo que ocurre en un ecosistema que una sola cadena alimentaria?",
 ["Porque muestra que un ser vivo puede comer y ser comido por varios otros seres vivos","Porque en una red cada animal se alimenta de una sola especie y nunca cambia de alimento","Porque las redes solo incluyen a los productores y dejan fuera a todos los consumidores","Porque una red tiene siempre exactamente cuatro eslabones, ni más ni menos que eso"],"a",
 "En la naturaleza un zorro puede comer conejos, roedores o aves, y un conejo puede ser presa de varios animales. La red muestra todas esas relaciones conectadas; una cadena muestra solo un camino.","OA 2")
q("### OA N°5 — Cambios en la pubertad\n\n",1,"¿Cuál de los siguientes cambios de la pubertad ocurre principalmente en los **hombres**?",
 ["La voz se vuelve más grave y aparece vello en la cara","Comienza la menstruación cada cierto tiempo","Se desarrollan las mamas","El cuerpo deja de crecer por completo a los 10 años"],"b",
 "La voz más grave y el vello facial son cambios típicos de los hombres en la pubertad. La menstruación y el desarrollo de las mamas ocurren en las mujeres, y el crecimiento continúa durante la adolescencia.","OA 5")
q("",1,"¿Qué es la pubertad?",
 ["La etapa en que el cuerpo y las emociones cambian al pasar de la niñez a la adultez","Una enfermedad que aparece a los 12 años y que se cura con medicamentos","La etapa de la vejez en que el cuerpo empieza a perder fuerza","Un cambio del cuerpo que solo ocurre en las mujeres y nunca en los hombres"],"d",
 "La pubertad es una etapa normal del desarrollo, con cambios físicos (crecimiento, vello, cambios en la voz o la menstruación) y emocionales, en hombres y mujeres. No es una enfermedad.","OA 5")
q("",2,"Joaquín tiene 12 años y está preocupado porque varios de sus amigos ya son más altos y tienen la voz más grave que él. ¿Qué idea le ayudaría a entender su situación?",
 ["Cada persona vive la pubertad a su propio ritmo; es normal y puede conversarlo con un adulto de confianza","Algo está mal en su cuerpo, porque todos deben cambiar exactamente a la misma edad","Debe dejar de hacer deporte para que su cuerpo crezca más rápido que el de sus amigos","Debe ocultar lo que siente, porque de los cambios del cuerpo no se habla con nadie"],"c",
 "La pubertad no empieza a la misma edad para todos: puede comenzar antes o después y eso es normal. Hablar con un adulto de confianza ayuda a resolver dudas y a sentirse tranquilo.","OA 5")
q("### OA N°6 — Actividad física e higiene corporal en la pubertad\n\n",1,"¿Por qué en la pubertad se vuelve especialmente importante ducharse todos los días?",
 ["Porque aumentan el sudor y la grasa de la piel, y lavarse evita el mal olor e infecciones","Porque el agua hace que el cuerpo crezca más rápido durante la pubertad","Porque en la pubertad la piel deja de producir sudor y se reseca con mucha facilidad","Porque ducharse todos los días reemplaza la necesidad de hacer actividad física"],"a",
 "En la pubertad las glándulas de la piel producen más sudor y grasa; si no se lavan, aparecen mal olor, espinillas o infecciones.","OA 6")
q("",1,"¿Cuánto tiempo de actividad física se recomienda, como mínimo, para niños y adolescentes?",
 ["Unos 60 minutos al día","Unos 10 minutos a la semana","Una hora al mes","Solo los días de clases de educación física"],"b",
 "Se recomienda al menos una hora diaria de actividad física moderada o intensa, como correr, andar en bicicleta, jugar o bailar.","OA 6")
q("",2,"¿Qué opción describe correctamente beneficios de practicar actividad física de forma regular?",
 ["Fortalece el corazón y los pulmones, ayuda a dormir mejor y disminuye el estrés","Hace innecesario comer frutas y verduras durante la semana","Evita por completo resfriarse y enfermarse durante todo el año","Solo sirve para bajar de peso y no tiene otros efectos en la salud"],"d",
 "La actividad física regular mejora el funcionamiento del corazón y los pulmones, el sueño y el ánimo. No reemplaza una alimentación equilibrada ni garantiza no enfermarse nunca.","OA 6")
q("## Eje 2: Ciencias Físicas y Químicas (Preguntas 13 a 21)\n\n### OA N°8 — La energía y los procesos vitales\n\n",1,"¿De dónde obtiene el cuerpo humano la energía que necesita para moverse, crecer y mantener su temperatura?",
 ["De los alimentos que consume","Del aire que exhala al respirar","De la luz del sol, igual que las plantas","De la ropa que lo abriga en invierno"],"c",
 "Los alimentos contienen energía química que el cuerpo transforma para moverse, crecer y mantener su temperatura. Las personas no hacen fotosíntesis, y la ropa solo ayuda a no perder calor.","OA 8")
q("",1,"Al encender una linterna a pilas, ¿qué transformación de energía ocurre?",
 ["La energía química de las pilas se transforma en eléctrica y luego en luz","La energía de la luz se transforma en energía química dentro de las pilas","La energía del sonido que hace la linterna se transforma en luz y calor","La energía eléctrica de la ampolleta se transforma en energía química"],"a",
 "Las pilas guardan energía química; al cerrar el circuito, se transforma en energía eléctrica, y la ampolleta la convierte en energía lumínica y un poco de calor.","OA 8")
q("",3,"Una bicicleta tiene un dínamo: un pequeño generador que, al girar la rueda, enciende la luz delantera. ¿Qué secuencia de energías ocurre mientras la ciclista pedalea de noche?",
 ["Energía de movimiento (cinética) de la rueda → energía eléctrica en el dínamo → energía lumínica en la luz","Energía lumínica de la luz → energía eléctrica en el dínamo → movimiento de la rueda","Energía eléctrica de un enchufe → energía química en el dínamo → energía sonora","Energía sonora del pedaleo → energía química en la luz → energía de movimiento de la rueda"],"d",
 "La ciclista mueve la rueda (energía cinética, que viene de la energía química de sus alimentos); el dínamo transforma ese movimiento en energía eléctrica, y la luz la transforma en energía lumínica.","OA 8")
q("### OA N°11 — Recursos energéticos renovables y no renovables\n\n",1,"¿Qué recurso energético tardó millones de años en formarse bajo tierra y, por eso, se agota cuando se usa?",
 ["El carbón","El viento","La luz del sol","El agua de los ríos"],"b",
 "El carbón se formó durante millones de años y, una vez usado, no se recupera en el tiempo humano: es no renovable. El viento, el sol y el agua de los ríos se renuevan constantemente.","OA 11")
q("",1,"¿Qué ventaja tienen las fuentes de energía renovables frente a las no renovables?",
 ["No se agotan con el uso y, en general, contaminan menos el aire","Siempre son más baratas y funcionan igual en cualquier lugar del mundo","Producen energía sin necesidad de ninguna instalación ni aparato","Pueden guardarse en barriles igual que el petróleo"],"c",
 "El sol, el viento o el agua se renuevan y su uso libera pocos gases contaminantes. Sin embargo, dependen del lugar y del clima, y requieren instalaciones como paneles o turbinas.","OA 11")
q("",2,"¿Qué acciones ayudan a ahorrar energía en la casa?",
 ["Dejar el cargador del celular enchufado todo el día","Apagar las luces de las piezas en las que no hay nadie","Usar ampolletas LED de bajo consumo","Secar la ropa al sol en vez de usar la secadora"],"bcd",
 "b, c y d. Apagar luces innecesarias, usar ampolletas LED y aprovechar el sol para secar la ropa reducen el consumo. Un cargador enchufado sin uso sigue gastando energía.","OA 11")
q("### OA N°13 — Cambios de estado de la materia\n\n",1,"¿Cómo se llama el cambio de estado en que un líquido pasa a sólido, como cuando el agua se congela?",
 ["Solidificación","Fusión","Evaporación","Condensación"],"a",
 "La solidificación es el paso de líquido a sólido al enfriarse. La fusión es lo contrario (sólido a líquido), la evaporación es de líquido a gas y la condensación, de gas a líquido.","OA 13")
q("",1,"La ropa mojada colgada al sol se seca después de unas horas. ¿Qué cambio de estado explica esto?",
 ["La evaporación del agua, que pasa de líquido a gas","La condensación del agua, que pasa de gas a líquido","La solidificación del agua, que pasa de líquido a sólido","La fusión del agua, que pasa de sólido a líquido"],"d",
 "El calor del sol hace que el agua líquida de la ropa pase a vapor y se mezcle con el aire: es evaporación.","OA 13")
q("",3,"Un cubo de hielo se derrite sobre un plato a temperatura ambiente. ¿Qué ocurre con sus partículas durante este cambio?",
 ["Absorben calor, se mueven más y dejan sus posiciones fijas, pero siguen siendo partículas de agua","Pierden calor, se quedan quietas y se convierten en partículas de otra sustancia","Desaparecen poco a poco, porque el agua líquida no tiene partículas","Se agrandan cada una al calentarse, por eso el agua líquida ocupa todo el plato"],"b",
 "Al recibir calor, las partículas vibran con más fuerza y se deslizan unas sobre otras: el sólido pasa a líquido (fusión). La sustancia sigue siendo agua; solo cambia cómo se ordenan y se mueven sus partículas.","OA 13")
q("## Eje 3: Ciencias de la Tierra y el Universo (Preguntas 22 a 25)\n\n### OA N°16 — Las capas de la Tierra\n\n",1,"¿Cómo se llama la capa sólida externa de la Tierra, donde se encuentran los continentes y el fondo de los océanos?",
 ["Litosfera","Hidrosfera","Atmósfera","Núcleo"],"c",
 "La litosfera es la capa rocosa y sólida de la superficie. La hidrosfera es el agua del planeta, la atmósfera es el aire y el núcleo es la parte más interna de la Tierra.","OA 16")
q("",2,"Una fábrica vierte sus desechos sin tratar en un río. ¿Qué capa de la Tierra se afecta directamente y qué medida ayudaría a protegerla?",
 ["La hidrosfera; tratar las aguas residuales antes de devolverlas al río","La atmósfera; prohibir que las personas se bañen en el río","La litosfera; cambiar el nombre del río por uno nuevo","El núcleo; construir la fábrica a mayor altura sobre el río"],"a",
 "El río es parte de la hidrosfera, el agua del planeta. Tratar las aguas residuales elimina sustancias dañinas antes de que lleguen al río y afecten a los seres vivos.","OA 16")
q("### OA N°18 — La erosión\n\n",1,"En el desierto, la arena se acumula y forma dunas que cambian de lugar con el tiempo. ¿Qué agente de erosión las forma principalmente?",
 ["El viento","El agua de los ríos","El hielo de los glaciares","Las olas del mar"],"b",
 "El viento arrastra granos de arena y los deposita formando dunas, que se desplazan cuando sigue soplando. En el desierto casi no hay ríos ni glaciares.","OA 18")
q("",2,"¿Qué acciones humanas **aumentan** la erosión del suelo?",
 ["Talar los bosques de las laderas","Dejar demasiado ganado en un mismo terreno (sobrepastoreo)","Plantar árboles nativos en los cerros","Quemar los pastizales para limpiar el terreno"],"abd",
 "a, b y d. Talar, sobrepastorear y quemar dejan el suelo descubierto, y la lluvia y el viento lo arrastran con facilidad. Plantar árboles nativos, en cambio, sujeta el suelo con las raíces y reduce la erosión.","OA 18")
armar(C/'ciencias-naturales-examen-forma-b.md', C/'ciencias-naturales-examen-forma-a.md', Q,
  fila=lambda i,p,cl: f"| {i} | {p.extra['tipo']} | **{cl}.** {p.explicacion.split('. ',1)[1] if len(p.letra)>1 else p.explicacion} | {p.oa} |",
  reemplazos={"Forma B":"Forma A","FORMA B":"FORMA A","Forma A (segunda versión, preguntas propias)":"Forma A (versión de práctica distinta de la Forma B, preguntas propias)","ultima_actualizacion: 2026-11-02":"ultima_actualizacion: 2026-11-16","Esta Forma A evalúa":"Esta Forma A evalúa","del banco de contenido, de modo que ambas":"del banco de contenido y de la Forma B, de modo que las tres"},
  inicio_preguntas="## Eje 1")
if __name__=="__main__":
    from collections import Counter; print(Counter(p.letra for p in Q), len(Q))
