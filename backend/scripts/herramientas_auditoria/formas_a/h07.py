import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from forma_a import P, armar  # noqa: E402
C=Path(__file__).resolve().parents[4]/'contenido'/'07-basico/examenes'
Q=[]
def q(sec,pts,en,ops,l,ex,oa,eje):
    Q.append(P(sec,"**Pregunta {n}.** (%d punto%s)"%(pts,"" if pts==1 else "s"),en,ops,l,ex,oa,{"pts":pts,"eje":eje}))
H,G,F="Historia","Geografía","Formación Ciudadana"
q("## EJE 1 — HISTORIA (preguntas 1 a 14)\n\n### La Revolución neolítica y sus consecuencias (OA 2)\n\n",1,"¿Cuál fue el cambio central de la Revolución neolítica?",
 ["La agricultura y la domesticación de animales, que permitieron vivir en un lugar","La invención de la escritura para registrar las leyes y los impuestos","La construcción de grandes imperios con ejércitos permanentes y caminos","El uso del hierro para fabricar armas y herramientas para la guerra"],"b",
 "Al cultivar y criar animales, los grupos humanos ya no dependían solo de la caza y la recolección, y pudieron asentarse en aldeas permanentes (sedentarismo). La escritura y los imperios llegaron mucho después.","OA 2",H)
q("",1,"¿Por qué el sedentarismo favoreció el aumento de la población en el Neolítico?",
 ["Porque producir alimentos era más seguro y en aldeas fijas se podía criar a más hijos","Porque las personas dejaron de comer carne y así vivieron muchos más años","Porque los grupos se separaron y cada uno buscó un territorio vacío para vivir","Porque se dejó de trabajar la tierra y las familias tenían más tiempo libre"],"a",
 "Cultivar y guardar alimentos dio mayor seguridad que la caza y la recolección; además, vivir en un lugar fijo facilitó cuidar a más niños. Así creció la población.","OA 2",H)
q("### El surgimiento de las primeras civilizaciones (OA 3)\n\n",1,"¿Qué tienen en común Mesopotamia, Egipto, el valle del Indo y China en sus orígenes?",
 ["Surgieron junto a grandes ríos, que permitían regar los cultivos","Surgieron en zonas heladas, cerca de los polos","Surgieron en islas pequeñas, aisladas del continente","Surgieron en la cima de altas montañas, lejos del agua"],"c",
 "Las primeras civilizaciones se formaron junto a ríos como el Tigris y el Éufrates, el Nilo, el Indo y el Amarillo: el agua y los suelos fértiles permitían producir excedentes de alimentos.","OA 3",H)
q("",2,"¿Por qué la escritura fue tan importante para las primeras civilizaciones?",
 ["Porque permitió registrar impuestos, leyes y comercio para administrar el Estado","Porque reemplazó a la agricultura como la principal fuente de alimento","Porque solo servía para escribir cuentos y poemas en las escuelas de niños","Porque eliminó la necesidad de tener gobernantes, jueces y sacerdotes"],"d",
 "La escritura nació en buena parte para llevar cuentas: cosechas, tributos, intercambios y leyes, como el Código de Hammurabi. Con ella se pudo organizar una sociedad grande y compleja.","OA 3",H)
q("### La democracia en la Atenas clásica (OA 6)\n\n",1,"En la democracia de la Atenas clásica, ¿quiénes podían participar en la Asamblea?",
 ["Solo los hombres libres hijos de padres atenienses","Todas las personas que vivían en Atenas","Las mujeres, los esclavos y los extranjeros","Solo el rey y su familia más cercana"],"a",
 "En Atenas solo los ciudadanos (hombres libres, hijos de atenienses) participaban en la Asamblea. Mujeres, esclavos y extranjeros (metecos) estaban excluidos, a diferencia de la democracia actual.","OA 6",H)
q("### La civilización romana y su expansión (OA 7)\n\n",1,"Observa el mapa del mar Mediterráneo:\n\n::mapa::mediterraneo::A@37.98,23.73;B@41.9,12.5;C@31.2,29.9;D@36.85,10.32::rosa=si::\n\n¿Qué letra señala la ciudad de Roma, centro del Imperio romano?",
 ["B","A","C","D"],"b",
 "Roma está en el centro de la península itálica, la península con forma de bota en medio del Mediterráneo: la letra B. La A está en Grecia (Atenas), la C en Egipto (Alejandría) y la D en el norte de África (Cartago).","OA 7",H)
q("",2,"¿Por qué se dice que el latín, la lengua de los romanos, sigue presente en nuestra vida diaria?",
 ["Porque el castellano y otras lenguas romances se formaron a partir del latín","Porque en Chile el latín es el idioma oficial de las leyes","Porque todos los idiomas del mundo provienen del latín","Porque el latín se habla todavía en la mayoría de las casas de Italia"],"c",
 "El castellano, el italiano, el francés, el portugués y el rumano derivan del latín (lenguas romances). Por eso muchas palabras nuestras tienen origen latino.","OA 7",H)
q("### La formación de la civilización europea medieval (OA 9)\n\n",1,"¿Qué institución dio unidad cultural y religiosa a Europa occidental durante la Edad Media?",
 ["La Iglesia católica","El Senado romano","La Asamblea ateniense","El Imperio azteca"],"d",
 "Tras la caída del Imperio romano de Occidente, la Iglesia católica se extendió por toda Europa occidental: organizó la vida religiosa, conservó libros en los monasterios y tuvo gran influencia política.","OA 9",H)
q("### Las transformaciones de Europa desde el siglo XII (OA 12)\n\n",1,"¿Qué cambio ocurrió en Europa a partir del siglo XII?",
 ["Crecieron las ciudades (burgos) y el comercio, y surgió la burguesía","Desaparecieron todas las ciudades y la población volvió al campo","Se abandonó la agricultura y la gente vivió solo de la caza","Los reinos europeos se unieron en un solo imperio sin reyes"],"a",
 "Con más producción agrícola y rutas comerciales, las ciudades se reactivaron; en ellas surgió la burguesía, un grupo dedicado al comercio y la artesanía.","OA 12",H)
q("",2,"¿Por qué la imprenta de tipos móviles, difundida en Europa por Johannes Gutenberg en el siglo XV, transformó la difusión del conocimiento?",
 ["Porque permitió producir libros más rápido y más baratos, y más personas pudieron leerlos","Porque prohibió copiar libros a mano en los monasterios de toda Europa","Porque hizo que los libros solo pudieran leerse en latín y en las iglesias","Porque reemplazó a las universidades, que cerraron por falta de estudiantes"],"b",
 "Antes los libros se copiaban a mano y eran escasos y caros. La imprenta permitió hacer muchas copias iguales en poco tiempo, y las ideas se difundieron con mayor rapidez.","OA 12",H)
q("### Las civilizaciones maya y azteca (OA 13)\n\n",1,"Los aztecas construyeron su capital, Tenochtitlan, sobre un lago. ¿Qué eran las chinampas?",
 ["Islas artificiales de cultivo construidas sobre el lago","Templos en forma de pirámide dedicados al Sol","Caminos de piedra que unían las ciudades mayas","Barcos de madera para cruzar el océano Atlántico"],"c",
 "Las chinampas eran parcelas hechas con barro y plantas sobre el lago: permitían cultivar maíz, frijoles y otras plantas en un medio acuático.","OA 13",H)
q("",1,"¿Cuál fue un aporte de la civilización maya al conocimiento?",
 ["Un calendario muy preciso y una numeración que usaba el cero","La invención de la imprenta de tipos móviles en Europa","La construcción del primer gran acueducto de la ciudad de Roma","La creación del alfabeto que usamos hoy en castellano"],"d",
 "Los mayas observaron los astros, elaboraron calendarios muy exactos y usaron un sistema numérico con el cero. La imprenta y el acueducto son europeos, y nuestro alfabeto viene del latino.","OA 13",H)
q("### El legado de las civilizaciones en la cultura latinoamericana actual (OA 16)\n\n",1,"Las palabras «chocolate», «tomate» y «aguacate» llegaron al castellano desde el náhuatl. ¿De qué pueblo es este legado?",
 ["De los aztecas (mexicas)","De los griegos","De los romanos","De los mayas de Guatemala"],"a",
 "El náhuatl era la lengua de los aztecas o mexicas. Muchas palabras de alimentos americanos provienen de esa lengua.","OA 16",H)
q("",3,"¿Por qué es importante conservar sitios patrimoniales como Chichén Itzá, en México, o Machu Picchu, en Perú?",
 ["Porque son parte de la identidad latinoamericana y permiten conocer su historia","Porque son lugares abandonados que no tienen ningún valor para las personas de hoy","Porque solo sirven como lugares de vacaciones y no enseñan nada sobre el pasado","Porque fueron construidos por europeos y muestran solo la historia de Europa"],"b",
 "Estos sitios conservan el legado de civilizaciones americanas; cuidarlos permite que las nuevas generaciones conozcan su historia y fortalezcan su identidad.","OA 16",H)
q("## EJE 2 — GEOGRAFÍA (preguntas 15 a 19)\n\n### Adaptación y transformación en la relación ser humano-medio (OA 21)\n\n",1,"En la cordillera de los Andes, distintos pueblos construyeron terrazas de cultivo en las laderas. ¿Qué muestra esta práctica?",
 ["Que adaptaron el relieve de pendientes para poder cultivar","Que preferían vivir en zonas planas cerca del mar","Que no necesitaban producir alimentos para vivir","Que destruyeron los cerros para construir ciudades"],"c",
 "Las terrazas son escalones en las laderas que evitan que el agua arrastre la tierra: transforman el medio para cultivar en zonas con pendiente.","OA 21",G)
q("",1,"¿Por qué construir viviendas en el cauce seco de una quebrada aumenta el riesgo para las personas?",
 ["Porque con lluvias intensas puede bajar un aluvión por ese cauce","Porque en las quebradas nunca llega la luz del sol","Porque en las quebradas está prohibido plantar árboles","Porque el suelo de las quebradas es demasiado blando para caminar"],"d",
 "Un cauce seco puede volver a llevar agua y barro con lluvias fuertes. Vivir ahí aumenta la vulnerabilidad de la población ante un aluvión.","OA 21",G)
q("",2,"La construcción de un embalse en un río permite guardar agua para regar en verano. ¿Qué efecto puede tener también sobre el medio?",
 ["Puede inundar valles y cambiar el caudal, afectando a las especies del río","No tiene ningún efecto, porque el agua del río sigue exactamente igual","Hace que el agua del río se vuelva salada, como el agua de mar","Aumenta las lluvias en toda la región durante todo el año"],"a",
 "Transformar el medio trae beneficios y costos: el embalse asegura agua para riego, pero inunda terrenos y altera el río, lo que afecta a la flora y fauna.","OA 21",G)
q("### Impactos de la acción humana en el medio y medidas de mitigación (OA 22)\n\n",1,"En invierno, Santiago y otras ciudades del centro-sur de Chile sufren contaminación del aire. ¿Qué medida ayuda a mitigarla?",
 ["Usar calefacción limpia en vez de leña húmeda y preferir el transporte público","Quemar las hojas secas en las veredas para limpiar las calles del barrio","Usar más el auto particular para pasar menos tiempo afuera, en la calle","Cerrar todas las áreas verdes de la ciudad durante el invierno"],"b",
 "La leña húmeda y el tráfico de autos emiten gran parte de los contaminantes. Calefaccionarse con sistemas limpios y usar transporte público reduce esas emisiones.","OA 22",G)
q("",2,"En una zona donde se talaron bosques nativos, una comunidad decide reforestar con especies nativas. ¿Qué efectos positivos puede tener esta medida?",
 ["Disminuye la erosión, recupera el hábitat de la fauna y conserva el agua","Hace que el suelo se vuelva más seco y deje de ser útil para cultivar","Aumenta la contaminación del aire en toda la zona reforestada","No tiene ningún efecto, porque los árboles no influyen en el medio"],"c",
 "Las raíces sujetan el suelo, los bosques dan refugio y alimento a la fauna, y ayudan a que el agua se infiltre. Por eso la reforestación nativa es una medida de mitigación.","OA 22",G)
q("## EJE 3 — FORMACIÓN CIUDADANA (preguntas 20 a 25)\n\n### Conceptos políticos del mundo clásico y medieval en la sociedad actual (OA 18)\n\n",1,"¿En qué se diferencia la ciudadanía de la Atenas clásica de la ciudadanía en el Chile actual?",
 ["En Atenas era solo de algunos hombres; en Chile votan todas las personas chilenas desde los 18 años","En Atenas votaban todos sus habitantes; hoy en Chile solo votan los hombres","En los dos casos solo pueden votar las personas que son dueñas de tierras","No hay diferencias: en ambos casos votan todas las personas, sin importar la edad"],"d",
 "La ciudadanía ateniense excluía a mujeres, esclavos y extranjeros. En Chile, todas las personas chilenas mayores de 18 años pueden votar, sin distinción de sexo ni de riqueza.","OA 18",F)
q("",2,"La palabra «Senado» viene de la Roma antigua. ¿Qué función cumple hoy el Senado en Chile?",
 ["Forma parte del Congreso Nacional y participa en la aprobación de las leyes","Es el tribunal que juzga todos los delitos cometidos en el país","Es el grupo de ministros que gobierna el país junto al Presidente","Es un consejo de sacerdotes que organiza las fiestas religiosas del año"],"a",
 "En Chile el Senado y la Cámara de Diputados forman el Congreso Nacional, que elabora y aprueba las leyes. El nombre recuerda al Senado romano, aunque su función hoy es distinta.","OA 18",F)
q("### El valor de la diversidad cultural (OA 19)\n\n",1,"¿Qué conocimiento llegó a Europa medieval a través del contacto con el mundo musulmán?",
 ["El sistema de numeración indoarábigo, que usamos hoy","El uso del hierro para fabricar herramientas","La construcción de pirámides escalonadas","La domesticación del caballo y del perro"],"b",
 "Los sabios musulmanes difundieron en Europa los números indoarábigos (0 al 9), además de conocimientos de medicina, astronomía y matemáticas, como el álgebra.","OA 19",F)
q("",2,"En un curso hay estudiantes nacidos en Chile, Venezuela, Haití y Perú. ¿Qué actitud refleja que se valora la diversidad cultural?",
 ["Conocer las costumbres de cada uno y compartirlas, respetando sus diferencias","Pedir que todos dejen de lado sus costumbres para ser iguales","Formar grupos de trabajo solo con compañeros del mismo país","Burlarse de los acentos distintos para hacer reír al curso"],"c",
 "Valorar la diversidad es reconocer que cada cultura aporta conocimientos y experiencias, y convivir con respeto. Excluir o burlarse genera discriminación.","OA 19",F)
q("### Convivencia y conflicto entre culturas (OA 20)\n\n",1,"¿Qué fueron las Cruzadas, entre los siglos XI y XIII?",
 ["Guerras de reinos cristianos europeos contra musulmanes por el control de Tierra Santa","Viajes de comercio pacífico entre Roma y China por la antigua Ruta de la Seda","Reuniones de paz entre aztecas y mayas para dividir su territorio en América","Campañas para llevar la imprenta a todas las ciudades y aldeas de Europa"],"d",
 "Las Cruzadas fueron guerras de motivación religiosa en las que reinos cristianos buscaron controlar Jerusalén, en manos musulmanas. Son un ejemplo de conflicto entre culturas.","OA 20",F)
q("",3,"> **Estímulo — caso:** En un barrio de Santiago llegaron muchas familias de otros países. Algunos vecinos reclaman por la música en las fiestas; otros organizaron una feria para compartir comidas típicas de cada país.\n\n¿Qué conclusión sobre la convivencia entre culturas se puede obtener del caso?",
 ["Que pueden existir conflictos y también encuentros, y que el diálogo y el respeto ayudan a convivir","Que la convivencia entre culturas distintas es imposible y siempre termina en conflicto","Que los conflictos se resuelven expulsando a quienes tienen costumbres distintas","Que la feria no sirve de nada, porque las comidas no tienen relación con la cultura"],"c",
 "El caso muestra a la vez tensión (reclamos) y encuentro (la feria). La convivencia se construye con diálogo, acuerdos y respeto mutuo, no con la exclusión.","OA 20",F)
armar(C/'historia-geografia-y-cs-sociales-examen-forma-b.md', C/'historia-geografia-y-cs-sociales-examen-forma-a.md', Q,
  fila=lambda i,p,cl: f"| {i} | Alternativas | **{cl}.** {p.explicacion} | {p.oa} | {p.extra['eje']} | {p.extra['pts']} |",
  reemplazos={"Forma B":"Forma A","**Forma B**":"**Forma A**","última actualización: 2026-08-10":"última actualización: 2026-11-16","Forma\nA, de modo que ambas":"Forma\nB, de modo que ambas"},
  inicio_preguntas="## EJE 1")
if __name__=="__main__":
    from collections import Counter; print(Counter(p.letra for p in Q), len(Q))
