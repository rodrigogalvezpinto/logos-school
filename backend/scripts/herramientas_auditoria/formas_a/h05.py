import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from forma_a import P, armar  # noqa: E402
C=Path(__file__).resolve().parents[4]/'contenido'/'05-basico/examenes'
H="**Pregunta {n}.** (%d punto%s)"
def h(p): return H%(p,"" if p==1 else "s")
Q=[]
def q(sec,pts,en,ops,l,ex,oa,eje): Q.append(P(sec,h(pts),en,ops,l,ex,oa,{"pts":pts,"eje":eje}))
S1="## EJE 1 — HISTORIA (preguntas 1 a 13)\n\n### Conquista de América y de Chile (OA 2)\n\n"
q(S1,1,"¿Qué conquistador español dirigió la primera expedición por tierra hacia Chile, en 1536, y por qué regresó al Perú?",
 ["Diego de Almagro, porque no encontró las riquezas de oro que esperaba","Pedro de Valdivia, porque los mapuches lo derrotaron en Curalaba","Hernán Cortés, porque prefirió volver a gobernar México","Francisco Pizarro, porque prefirió quedarse a vivir en Santiago"],"b",
 "Almagro organizó la primera expedición a Chile (1536); al no encontrar oro como el de Perú, volvió decepcionado. Valdivia llegó después, en 1541.","OA 2","Historia")
q("",1,"> **Estímulo — fuente adaptada:** En una carta al rey, Pedro de Valdivia escribió que esta tierra era tal que «para poder vivir en ella y perpetuarse no la hay mejor en el mundo».\n\nSegún la fuente, ¿qué intención tenía Valdivia respecto del territorio de Chile?",
 ["Quedarse a vivir en él y poblarlo de forma permanente","Volver pronto a España con el oro que encontrara","Entregar el territorio a las autoridades del Imperio inca","Recorrerlo como explorador sin fundar ninguna ciudad"],"a",
 "«Perpetuarse» significa quedarse para siempre: Valdivia quería poblar y vivir en Chile, a diferencia de Almagro. Por eso fundó ciudades como Santiago.","OA 2","Historia")
q("",1,"¿Qué ocurrió en 1598 en la batalla de Curalaba?",
 ["Los mapuches vencieron y los españoles dejaron las ciudades al sur del Biobío","Pedro de Valdivia fundó Santiago a los pies del cerro Huelén","Diego de Almagro llegó al valle de Copiapó en su primera expedición","Españoles y mapuches firmaron su primer acuerdo de paz y comercio en la frontera"],"c",
 "En Curalaba los mapuches, dirigidos por Pelantaro, derrotaron a los españoles y murió el gobernador Martín García Óñez de Loyola. En los años siguientes los españoles abandonaron las ciudades al sur del Biobío.","OA 2","Historia")
q("",2,"Un grupo de soldados españoles cruzó el desierto y la cordillera con pocos alimentos y, al llegar a los valles, fue atacado por pueblos que defendían sus tierras. ¿Qué dificultades de la conquista de Chile muestra esta situación?",
 ["La geografía difícil del territorio y la resistencia de los pueblos originarios","El desinterés de la Corona española y el clima tropical de los valles","La presencia de ejércitos de otros países europeos en el territorio","La ausencia de pueblos que habitaran el territorio antes de su llegada"],"d",
 "El desierto y la cordillera hacían muy duros los viajes, y los pueblos originarios resistieron la ocupación de sus tierras. Ambas cosas hicieron lenta y difícil la conquista.","OA 2","Historia")
q("### Impacto de la conquista para Europa y América (OA 3)\n\n",1,"¿Cuál de estos productos llegó a América desde Europa con la conquista?",
 ["El trigo","La papa","El maíz","El tomate"],"c",
 "El trigo se trajo desde Europa y llegó a ser un cultivo muy importante en Chile. La papa, el maíz y el tomate son originarios de América y viajaron en sentido contrario.","OA 3","Historia")
q("",1,"Enfermedades como la viruela y el sarampión causaron la muerte de muchísimos indígenas después de la conquista. ¿Por qué los afectaron tanto?",
 ["Porque no tenían defensas contra enfermedades que no existían en América","Porque no conocían ninguna hierba medicinal para curarse","Porque esas enfermedades las transmitían los animales americanos","Porque en América no había agua suficiente para lavarse"],"a",
 "Esas enfermedades llegaron desde Europa; como nunca habían existido en América, los cuerpos de los indígenas no tenían defensas contra ellas y se contagiaban y morían con facilidad.","OA 3","Historia")
q("",2,"¿Cuál de los siguientes hechos fue una consecuencia de la conquista **para Europa**?",
 ["La llegada de oro y plata americanos y de alimentos nuevos, como la papa y el maíz","La disminución de su población por las enfermedades que llegaron desde América","La pérdida de todos los territorios que España tenía dentro de Europa","El abandono de la religión católica por parte de los reyes españoles"],"b",
 "Los metales preciosos americanos aumentaron la riqueza de España, y la papa y el maíz cambiaron la alimentación europea. La disminución de la población fue una consecuencia para América, no para Europa.","OA 3","Historia")
q("### Aspectos centrales de la Colonia (OA 6)\n\n",1,"En la sociedad colonial de Chile, ¿qué grupo ocupaba los cargos más altos del gobierno, como el de gobernador?",
 ["Los españoles nacidos en España, llamados peninsulares","Los criollos, hijos de españoles nacidos en América","Los mestizos que trabajaban en las haciendas","Los esclavos traídos desde África"],"d",
 "La Corona confiaba los cargos más altos a los peninsulares. Los criollos tenían riqueza y tierras, pero casi no llegaban a esos cargos, lo que después generó descontento.","OA 6","Historia")
q("",1,"¿Cuál fue la principal actividad económica de Chile durante la Colonia?",
 ["La agricultura y la ganadería en las haciendas","La fabricación de telas en grandes industrias","La extracción de petróleo en el extremo sur","El turismo de visitantes que llegaban de Europa"],"b",
 "Durante la Colonia, Chile producía sobre todo trigo, sebo, cueros y charqui en las haciendas, y vendía parte de esa producción al Perú.","OA 6","Historia")
q("",2,"En las haciendas coloniales vivían inquilinos. ¿Qué relación tenían con el dueño de la hacienda?",
 ["Recibían un terreno para vivir y cultivar, y a cambio trabajaban para el hacendado","Eran dueños de la hacienda y le arrendaban una casa al hacendado","Trabajaban en la ciudad y solo visitaban la hacienda en las fiestas","Eran funcionarios del rey que cobraban impuestos al hacendado"],"c",
 "El hacendado entregaba al inquilino un pedazo de tierra para vivir y cultivar; a cambio, el inquilino y su familia debían trabajar en las tierras del hacendado. Así se formó una relación de dependencia.","OA 6","Historia")
q("### Españoles y mapuches en el período colonial (OA 7)\n\n",1,"¿Qué fue la Guerra de Arauco?",
 ["Un largo conflicto entre españoles y mapuches por el control del territorio del sur","Una guerra entre España y Portugal por las tierras del norte de Chile","Una rebelión de los criollos para separarse de la Corona española","Un enfrentamiento entre incas y diaguitas antes de la llegada de los españoles"],"a",
 "La Guerra de Arauco enfrentó a españoles y mapuches durante gran parte de la Colonia, porque los mapuches defendían su territorio al sur del Biobío.","OA 7","Historia")
q("",1,"¿Qué eran los parlamentos durante la Colonia?",
 ["Reuniones de autoridades españolas con lonkos mapuches para acordar paz y límites","Tribunales del rey que juzgaban los delitos cometidos en las ciudades coloniales","Escuelas fundadas por la Iglesia para enseñar a leer a los criollos","Ejércitos formados por mapuches y españoles para defender la costa"],"d",
 "En los parlamentos, como el de Quillín (1641), los españoles y los lonkos mapuches negociaban acuerdos de paz, intercambio y fronteras. Fueron una forma de relación distinta de la guerra.","OA 7","Historia")
q("",3,"> **Estímulo — caso:** A comienzos del siglo XVII, el sacerdote jesuita Luis de Valdivia propuso al rey detener las campañas militares al sur del Biobío, respetar ese río como frontera y acercarse a los mapuches solo con misioneros.\n\n¿Cómo se llamó esta propuesta y qué buscaba?",
 ["La guerra defensiva: terminar los ataques españoles y evangelizar a los mapuches de forma pacífica","La encomienda: entregar a los mapuches a un español para que trabajaran para él","La fundación de ciudades: poblar el sur con españoles para ocuparlo por completo","El comercio libre: permitir que los mapuches vendieran sus productos a otros países"],"c",
 "Con la guerra defensiva (1612-1626) los españoles solo debían defender la frontera del Biobío, sin atacar, y la relación con los mapuches quedaba en manos de los misioneros. Buscaba poner fin a una guerra muy costosa.","OA 7","Historia")
S2="## EJE 2 — GEOGRAFÍA (preguntas 14 a 20)\n\n### Grandes zonas naturales de Chile (OA 9)\n\n"
q(S2,1,"¿Qué zona natural de Chile tiene un valle fértil entre dos cordilleras, clima templado con inviernos lluviosos y concentra la mayor parte de la población del país?",
 ["La Zona Central","El Norte Grande","La Zona Austral","El Norte Chico"],"b",
 "La Zona Central tiene la depresión intermedia más ancha y fértil y clima mediterráneo; ahí están Santiago, Valparaíso y otras grandes ciudades.","OA 9","Geografía")
q("",1,"¿En qué zona natural se encuentra el desierto de Atacama, uno de los más secos del mundo, y donde se desarrolla principalmente la minería del cobre?",
 ["El Norte Grande","El Norte Chico","La Zona Sur","La Zona Austral"],"a",
 "El Norte Grande tiene clima desértico, casi sin lluvias, y allí están las grandes minas de cobre, como Chuquicamata y Escondida.","OA 9","Geografía")
q("",1,"¿Cuál de las siguientes ciudades se ubica en la Zona Sur de Chile?",
 ["Temuco","Antofagasta","La Serena","Punta Arenas"],"b",
 "Temuco está en la Zona Sur, con lluvias abundantes, bosques y lagos. Antofagasta está en el Norte Grande, La Serena en el Norte Chico y Punta Arenas en la Zona Austral.","OA 9","Geografía")
q("",2,"¿Por qué la Zona Austral es la zona menos poblada de Chile?",
 ["Porque su clima frío y lluvioso y sus fiordos y canales dificultan la vida y las comunicaciones","Porque es un desierto muy seco donde casi nunca llueve y no hay agua suficiente para beber","Porque allí está prohibido vivir, ya que todo su territorio es un parque nacional","Porque su clima es caluroso todo el año y no permite cultivar alimentos ni criar animales"],"d",
 "El frío, las lluvias y el viento, junto con un relieve muy fragmentado por fiordos, canales y campos de hielo, hacen difícil vivir y conectarse con el resto del país.","OA 9","Geografía")
q("### Recursos naturales y desarrollo sostenible (OA 10)\n\n",1,"¿Cuál de los siguientes es un recurso natural **renovable**?",
 ["La energía del sol","El cobre","El petróleo","El carbón"],"c",
 "La energía del sol no se agota al usarla, así que es renovable. El cobre, el petróleo y el carbón tardan millones de años en formarse: son no renovables.","OA 10","Geografía")
q("",1,"¿Qué significa que el uso de un recurso natural sea **sostenible**?",
 ["Usarlo para cubrir las necesidades de hoy sin agotarlo para las generaciones futuras","Usarlo lo más rápido posible para obtener la mayor ganancia en el menor tiempo","Dejar de usar todos los recursos naturales para que nunca se agoten","Usarlo solo en las ciudades y prohibir su uso en el campo"],"a",
 "El desarrollo sostenible busca equilibrar el uso de los recursos con su cuidado, para que también existan para quienes vivan en el futuro.","OA 10","Geografía")
q("",2,"Si se pescara la merluza durante todo el año, incluso en la época en que se reproduce, ¿qué podría pasar y qué medida ayudaría a evitarlo?",
 ["Disminuiría hasta agotarse; ayuda la veda, que prohíbe pescarla en su reproducción","Aumentaría su cantidad, porque al pescarla quedan más espacios libres en el mar","No pasaría nada, porque los peces del mar se reproducen tan rápido que nunca se agotan","Cambiaría de color; ayuda pescarla solo de noche para no asustarla"],"d",
 "Aunque los peces son un recurso renovable, si se pescan más rápido de lo que se reproducen la población disminuye. La veda protege la reproducción para que el recurso se renueve.","OA 10","Geografía")
S3="## EJE 3 — FORMACIÓN CIUDADANA (preguntas 21 a 25)\n\n### Todas las personas son sujetos de derecho (OA 13)\n\n"
q(S3,1,"¿A quiénes protege la Convención sobre los Derechos del Niño, firmada por Chile en 1990?",
 ["A todas las personas menores de 18 años","Solo a los niños y niñas que nacieron en Chile","Solo a los niños y niñas que van al colegio","Solo a los niños y niñas menores de 6 años"],"b",
 "La Convención reconoce derechos a todas las personas menores de 18 años, sin importar su nacionalidad, si estudian o su edad exacta.","OA 13","Formación Ciudadana")
q("",1,"¿Cuál de los siguientes es un derecho de todos los niños y niñas?",
 ["Recibir educación","Votar en las elecciones presidenciales","Trabajar en lugar de ir al colegio","Conducir un automóvil"],"c",
 "La educación es un derecho de todos los niños y niñas. Votar y conducir son derechos o permisos de los adultos, y trabajar en lugar de estudiar va contra sus derechos.","OA 13","Formación Ciudadana")
q("",2,"¿Quién tiene el deber principal de garantizar y proteger los derechos de las personas en un país?",
 ["El Estado, a través de sus leyes e instituciones","Solo las familias de cada persona","Las empresas que dan trabajo a las personas","Cada persona, sin ayuda de ninguna institución"],"a",
 "El Estado debe asegurar que los derechos se respeten, por ejemplo con leyes, escuelas, hospitales y tribunales. Las familias y la comunidad también colaboran, pero la responsabilidad principal es del Estado.","OA 13","Formación Ciudadana")
q("### Los derechos generan deberes y responsabilidades (OA 14)\n\n",1,"¿Qué deber se relaciona con el derecho a la educación de un estudiante?",
 ["Asistir a clases y respetar a sus compañeros y profesores","Elegir qué días ir al colegio según el clima","Pedir que sus compañeros hagan sus tareas","Exigir que el colegio no le haga pruebas ni evaluaciones"],"d",
 "Quien tiene derecho a educarse debe aprovecharlo: asistir, estudiar y respetar a los demás, para que todos puedan aprender.","OA 14","Formación Ciudadana")
q("",3,"> **Estímulo — caso:** En la plaza de un barrio, los niños y niñas juegan todas las tardes. Algunos dejan basura y rayan los juegos.\n\nLos niños y niñas tienen derecho a jugar y recrearse. ¿Qué deber les corresponde en esta situación y por qué?",
 ["Cuidar los juegos y no dejar basura, porque la plaza es de todos y así otros también podrán usarla","Ninguno, porque si tienen derecho a jugar pueden usar la plaza como quieran","Jugar solo ellos, porque quienes llegan primero tienen más derecho a la plaza","Pedir a los adultos que limpien, porque el cuidado de la plaza no es tarea de los niños"],"c",
 "Ejercer el derecho a la recreación trae el deber de cuidar lo que es de todos. Si cada uno cuida la plaza, todos los vecinos pueden seguir usándola.","OA 14","Formación Ciudadana")
armar(C/'historia-geografia-y-cs-sociales-examen-forma-b.md', C/'historia-geografia-y-cs-sociales-examen-forma-a.md', Q,
  fila=lambda i,p,cl: f"| {i} | Alternativas | **{cl}.** {p.explicacion} | {p.oa} | {p.extra['eje']} | {p.extra['pts']} |",
  reemplazos={"Forma B":"Forma A","**Forma B**: una versión de práctica adicional":"**Forma A**: una versión de práctica adicional, distinta de la Forma B,","última actualización: 2026-11-02":"última actualización: 2026-11-16"},
  inicio_preguntas="## EJE 1")
from collections import Counter; print(Counter(p.letra for p in Q), len(Q))
