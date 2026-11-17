import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from forma_a import P, armar  # noqa: E402
C=Path(__file__).resolve().parents[4]/'contenido'/'02-medio/examenes'
Q=[]
def q(sec,en,ops,l,ex,oa,pts=1,tipo="Alternativas"):
    cab=f"**{{n}}.** *({tipo})* " if pts==1 else f"**{{n}}.** *({tipo}, {pts} puntos)* "
    Q.append(P(sec,cab,en,ops,l,ex,oa))
q("## Eje 1: Biología (Preguntas 1 a 11)\n\n### OA N°1 — Sistema nervioso: coordinación, respuesta a estímulos y autocuidado\n\n","¿Qué función cumplen las neuronas motoras (eferentes)?",
 ["*Llevan la orden desde el sistema nervioso central hasta los músculos o glándulas","Detectan los estímulos del ambiente, como la luz, el sonido o la temperatura","Conectan solo neuronas del cerebro entre sí, sin salir nunca del encéfalo","Producen las hormonas que regulan el crecimiento durante la adolescencia"],"b","Las neuronas motoras llevan la respuesta desde el sistema nervioso central hasta los efectores: músculos o glándulas.","OA 1")
q("","En el reflejo rotuliano, un golpe suave bajo la rodilla hace que la pierna se estire sin que la persona lo decida. ¿Qué estructura procesa este reflejo?",
 ["El cerebro, en la corteza que controla los movimientos voluntarios","El cerebelo, que coordina el equilibrio y la postura del cuerpo","*La médula espinal, que responde sin pasar por el cerebro","El mismo músculo de la pierna, que actúa sin ningún nervio"],"c","En un reflejo, la médula espinal recibe la señal y envía la respuesta sin esperar una decisión del cerebro: por eso es rápido e involuntario.","OA 1")
q("","Una persona bebe alcohol antes de manejar. ¿Cómo afecta esto a su sistema nervioso y a su seguridad?",
 ["*Es un depresor: hace más lentos los reflejos y la coordinación, y aumenta el riesgo de accidentes","Es un estimulante: mejora los reflejos y permite manejar con más atención y seguridad","No afecta al sistema nervioso, porque el alcohol solo actúa sobre el estómago y el hígado","Solo afecta la memoria al día siguiente, sin cambiar los reflejos mientras se maneja"],"a","El alcohol es un depresor del sistema nervioso: retrasa los reflejos y empeora la coordinación y el juicio, por lo que aumenta el riesgo de accidentes.","OA 1",2)
q("### OA N°3 — Sexualidad humana y reproducción: dimensiones biológica, social y afectiva\n\n","¿En qué parte del sistema reproductor femenino ocurre normalmente la fecundación?",
 ["*En las trompas de Falopio","En el interior del útero","En la superficie del ovario","En el cuello del útero"],"d","La fecundación ocurre normalmente en las trompas de Falopio; luego el embrión baja al útero, donde se implanta.","OA 3")
q("","¿Qué método previene a la vez el embarazo y las infecciones de transmisión sexual?",
 ["La píldora anticonceptiva","*El preservativo","El dispositivo intrauterino","El método del calendario"],"b","El preservativo es una barrera física: impide el paso de espermatozoides y también de los microorganismos que causan infecciones de transmisión sexual.","OA 3")
q("","En una relación de pololeo, uno de los dos revisa el celular del otro sin permiso y le prohíbe juntarse con sus amigos. ¿Cómo se evalúa esa conducta?",
 ["Es una muestra de amor, porque quien cela demuestra cuánto le importa la otra persona y la quiere proteger","Es normal en todas las parejas jóvenes, no daña a nadie y desaparece sola con el tiempo sin conversarlo","*Es una conducta de control que vulnera la autonomía; una relación sana se basa en la confianza y el respeto","Es correcta si la otra persona no reclama, porque el silencio significa que está de acuerdo con las reglas"],"c","Revisar el celular sin permiso y aislar de los amigos son conductas de control: vulneran la autonomía. Una relación sana se basa en la confianza, el respeto y el consentimiento.","OA 3",3)
q("### OA N°6 — Transmisión del material genético: mitosis, meiosis y alteraciones\n\n","¿Qué tipo de división celular permite que un niño crezca, formando células idénticas a las originales?",
 ["*La mitosis","La meiosis","La fecundación","La mutación"],"a","La mitosis produce dos células hijas idénticas a la célula madre: permite el crecimiento y la reparación de los tejidos.","OA 6")
q("","¿Cuántos cromosomas tiene un óvulo humano?",
 ["*23","46","92","22"],"d","Los gametos son haploides: tienen la mitad de los cromosomas (23). Al unirse con un espermatozoide (23), el cigoto tiene 46.","OA 6")
q("","El síndrome de Down se asocia a tener tres copias del cromosoma 21. ¿Qué proceso puede originarlo?",
 ["La mitosis normal de las células de la piel durante la infancia","*Una no disyunción en la meiosis, que deja un gameto con dos copias del cromosoma 21","Una infección viral durante el embarazo que agrega un cromosoma nuevo","Una mutación causada por la exposición al sol durante la adolescencia"],"b","Si en la meiosis los cromosomas 21 no se separan (no disyunción), un gameto queda con dos copias; al fecundarse, el cigoto tiene tres.","OA 6",2)
q("### OA N°8 — Aplicaciones de la manipulación genética: implicancias éticas y sociales\n\n","A una planta de maíz se le inserta un gen de una bacteria que la hace resistente a ciertos insectos. ¿Cómo se clasifica esta planta?",
 ["Como un clon","Como un híbrido natural","*Como un organismo transgénico","Como una mutación espontánea"],"c","Al recibir un gen de otra especie (una bacteria), el maíz es un organismo transgénico, un tipo de organismo genéticamente modificado.","OA 8")
Q.append(P("","**{n}.** *(Varias correctas, 2 puntos)* ","La terapia génica busca corregir genes defectuosos en personas con enfermedades hereditarias. ¿Qué afirmaciones corresponden a una evaluación ética responsable de su uso? Marca **todas** las correctas.",
 ["Al ser un avance médico, puede aplicarse sin estudios previos","Podría tratar enfermedades que hoy no tienen cura","Debe asegurar el consentimiento informado de los pacientes","Debe considerar el acceso justo, porque podría ser muy costosa"],"bcd",
 "Evaluar la terapia génica implica sopesar su beneficio, asegurar el consentimiento informado y el acceso justo; ningún avance se aplica sin estudios previos.","OA 8"))
q("## Eje 2: Física (Preguntas 12 a 19)\n\n### OA N°9 — Cinemática del movimiento rectilíneo: posición, velocidad y aceleración\n\n","En un gráfico de velocidad en función del tiempo, la línea que describe el movimiento de un auto es horizontal. ¿Qué indica?",
 ["Que el auto está detenido","Que el auto acelera de forma constante","Que el auto frena hasta detenerse","*Que el auto mantiene su velocidad constante"],"d","Una línea horizontal en un gráfico velocidad-tiempo indica que la velocidad no cambia: la velocidad es constante y la aceleración es cero.","OA 9")
q("","Un auto pasa de 0 a 20 m/s en 5 s con aceleración constante. ¿Cuál es su aceleración?",
 ["*4 m/s²","100 m/s²","25 m/s²","0,25 m/s²"],"a","a = Δv / Δt = (20 − 0) / 5 = 4 m/s². 100 m/s² multiplica en vez de dividir.","OA 9")
q("","Un bus viaja a 20 m/s y frena con una desaceleración constante de 4 m/s² hasta detenerse. ¿Cuánto tiempo tarda en detenerse y qué distancia recorre mientras frena?",
 ["*5 s y 50 m","5 s y 100 m","80 s y 50 m","4 s y 80 m"],"b","t = 20 / 4 = 5 s. La distancia es d = v² / (2a) = 400 / 8 = 50 m. 100 m multiplica 20 × 5 como si la velocidad no disminuyera.","OA 9",3)
q("### OA N°10 — Leyes de Newton y diagrama de cuerpo libre\n\n","Una persona en patines empuja una pared y ella misma retrocede. ¿Qué ley de Newton explica este hecho?",
 ["La primera ley, de inercia","La segunda ley, F = m · a","*La tercera ley, de acción y reacción","La ley de gravitación universal"],"c","Al empujar la pared (acción), la pared empuja a la persona con una fuerza igual y opuesta (reacción): por eso retrocede.","OA 10")
q("","Un libro está en reposo sobre una mesa. ¿Qué se puede concluir sobre las fuerzas que actúan sobre él?",
 ["*La fuerza neta es cero: su peso está equilibrado por la fuerza normal de la mesa","No actúa ninguna fuerza sobre el libro, porque no se mueve ni hacia arriba ni hacia abajo","Solo actúa el peso del libro, que lo empuja hacia abajo, contra la superficie de la mesa","La mesa ejerce hacia arriba una fuerza mayor que el peso del libro, y por eso este no cae"],"a","Si el libro está en reposo, la fuerza neta es cero: el peso hacia abajo se equilibra con la fuerza normal que la mesa ejerce hacia arriba.","OA 10")
q("","Una caja de 4 kg recibe una fuerza horizontal de 30 N y un roce de 10 N en sentido contrario. ¿Cuáles son la fuerza neta y la aceleración de la caja?",
 ["*20 N y 5 m/s²","40 N y 10 m/s²","20 N y 80 m/s²","30 N y 7,5 m/s²"],"d","Fuerza neta = 30 − 10 = 20 N; a = F / m = 20 / 4 = 5 m/s². 40 N suma el roce en vez de restarlo.","OA 10",3)
q("### OA N°13 — Modelos del Universo: geocéntrico, heliocéntrico y Big Bang\n\n","¿Qué modelo del Universo propuso Nicolás Copérnico en el siglo XVI?",
 ["El geocéntrico, con la Tierra inmóvil en el centro","*El heliocéntrico, con el Sol en el centro y la Tierra girando a su alrededor","El del Big Bang, con un universo en expansión desde un estado muy denso","Un modelo con la Luna en el centro y los planetas girando a su alrededor"],"b","Copérnico propuso el modelo heliocéntrico: el Sol en el centro y la Tierra, como los demás planetas, girando a su alrededor.","OA 13")
q("","¿Qué evidencias apoyan la teoría del Big Bang sobre el origen del Universo?",
 ["Que la Tierra está en el centro y todas las estrellas giran a su alrededor","Que el Universo es inmóvil y siempre ha tenido el mismo tamaño que hoy","*La expansión del Universo y la radiación de fondo de microondas","Que las estrellas se apagan cada noche y se encienden al día siguiente"],"c","Las galaxias se alejan (el Universo se expande) y existe una radiación de fondo de microondas, restos del Universo temprano: ambas evidencias apoyan el Big Bang.","OA 13",2)
q("## Eje 3: Química (Preguntas 20 a 25)\n\n### OA N°15 — Soluciones químicas: componentes, concentración y solubilidad\n\n","En una bebida gaseosa, el dióxido de carbono (CO₂) está disuelto en agua. ¿Cuál es el solvente?",
 ["*El agua","El dióxido de carbono","El azúcar de la bebida","La botella plástica"],"a","El solvente es el componente en mayor cantidad, que disuelve a los demás: el agua. El CO₂ es un soluto.","OA 15")
q("","¿Qué cambio aumenta, en general, la cantidad de azúcar que se puede disolver en una taza de agua?",
 ["Usar una taza más pequeña","Agregar el azúcar más rápido","Enfriar el agua con hielo","*Calentar el agua"],"d","En la mayoría de los sólidos, la solubilidad aumenta con la temperatura: en agua caliente se disuelve más azúcar que en agua fría.","OA 15")
q("","Se disuelven 25 g de azúcar en 225 g de agua. ¿Cuál es la concentración de la solución en % m/m?",
 ["*10 % m/m","11,1 % m/m","25 % m/m","9 % m/m"],"b","La masa de la solución es 25 + 225 = 250 g; % m/m = 25 / 250 × 100 = 10 %. 11,1 % divide por la masa del agua y no por la de la solución.","OA 15",2)
q("### OA N°17 — El carbono como base de las moléculas orgánicas\n\n","¿Qué tienen en común todos los hidrocarburos, como el metano o el butano?",
 ["Contienen nitrógeno y oxígeno","Son siempre sólidos a temperatura ambiente","*Están formados solo por carbono e hidrógeno","Se disuelven fácilmente en agua"],"c","Los hidrocarburos están formados únicamente por átomos de carbono e hidrógeno, como el metano (CH₄) y el butano (C₄H₁₀).","OA 17")
q("","El etino (C₂H₂) tiene un enlace triple entre sus dos átomos de carbono. ¿Qué tipo de hidrocarburo es?",
 ["*Un alquino","Un alcano","Un alqueno","Un alcohol"],"a","Los hidrocarburos con al menos un enlace triple entre carbonos son alquinos; los alcanos tienen solo enlaces simples y los alquenos, al menos uno doble.","OA 17")
q("","¿Qué propiedad del átomo de carbono explica que existan millones de compuestos orgánicos distintos?",
 ["Que es un metal que conduce la electricidad y forma sales con el agua","Que solo puede unirse a átomos de hidrógeno y formar moléculas pequeñas","Que es un gas noble que no reacciona con ningún otro elemento químico","*Que forma cuatro enlaces covalentes y se une a otros carbonos en cadenas y anillos"],"d","El carbono forma cuatro enlaces covalentes y puede unirse a otros átomos de carbono en cadenas largas, ramificadas y anillos: así surge la enorme variedad de compuestos orgánicos.","OA 17",3)
armar(C/'ciencias-naturales-examen-forma-b.md', C/'ciencias-naturales-examen-forma-a.md', Q,
  fila=lambda i,p,cl: f"| {i} | {'Varias correctas' if len(p.letra)>1 else 'Alternativas'} | **{cl}.** {p.explicacion} | {p.oa} |",
  reemplazos={"— Forma B":"— Forma A","— FORMA B":"— FORMA A","última actualización: 2026-08-10":"última actualización: 2026-11-17","Esta es la **Forma B**":"Esta es la **Forma A**","> una segunda versión, con preguntas propias, pero que cubre los mismos":"> una versión con preguntas propias, distintas de la Forma B, que cubre los mismos"},
  inicio_preguntas="## Eje 1")
if __name__=="__main__":
    from collections import Counter; print(Counter(p.letra for p in Q), len(Q))
