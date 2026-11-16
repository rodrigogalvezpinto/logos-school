import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from forma_a import P, armar  # noqa: E402
C=Path(__file__).resolve().parents[4]/'contenido'/'06-basico/examenes'
Q=[]
def q(sec,pts,en,ops,l,ex,oa,eje):
    Q.append(P(sec,"**Pregunta {n}.** (%d punto%s)"%(pts,"" if pts==1 else "s"),en,ops,l,ex,oa,{"pts":pts,"eje":eje,"tipo":"Varias correctas" if len(l)>1 else "Alternativas"}))
H,G,F="Historia","Geografía","Formación Ciudadana"
q("## EJE 1 — HISTORIA (preguntas 1 a 13)\n\n### Los antecedentes de la Independencia americana (OA 1)\n\n",1,"¿Qué idea de la Ilustración influyó en los movimientos de independencia de América?",
 ["Que el poder debe residir en el pueblo y que las personas tienen derechos y libertades","Que el rey recibe su poder directamente de Dios y nadie puede cuestionarlo","Que las colonias deben comerciar solo con su metrópoli para ser más ricas","Que la sociedad debe organizarse en grupos que no pueden cambiar de lugar"],"a",
 "Los pensadores ilustrados defendieron la soberanía del pueblo, la libertad y la igualdad ante la ley. Esas ideas llevaron a los criollos a cuestionar el poder absoluto del rey.","OA 1",H)
q("",1,"¿Qué hecho ocurrido en España en 1808 fue un antecedente directo de la formación de juntas de gobierno en América?",
 ["La invasión de Napoleón y la prisión del rey Fernando VII","El primer viaje de Cristóbal Colón hacia América","La independencia de las trece colonias de Estados Unidos","La fundación de la ciudad de Santiago por Pedro de Valdivia"],"b",
 "Con Fernando VII prisionero de Napoleón, en América se discutió quién debía gobernar en su ausencia; así surgieron las juntas, como la chilena de 1810.","OA 1",H)
q("### El desarrollo de la Independencia de Chile (OA 2)\n\n",1,"¿Qué batalla, ocurrida en abril de 1818, aseguró la independencia de Chile?",
 ["La batalla de Maipú","La batalla de Rancagua","La batalla de Chacabuco","La batalla de Curalaba"],"c",
 "En Maipú (5 de abril de 1818) el ejército patriota venció a los realistas y consolidó la independencia, proclamada en febrero de ese año. Rancagua (1814) fue una derrota patriota y Chacabuco (1817) abrió el camino a Santiago.","OA 2",H)
q("",2,"Tras la derrota patriota en Rancagua (1814), los españoles recuperaron el control de Chile hasta 1817 y persiguieron a los patriotas. ¿Cómo se llama ese período?",
 ["La Reconquista","La Patria Vieja","La Patria Nueva","La Organización de la República"],"d",
 "La Reconquista (1814-1817) fue el período de vuelta al dominio español. La Patria Vieja fue antes (1810-1814) y la Patria Nueva comenzó después de Chacabuco (1817).","OA 2",H)
q("### La organización de la república (OA 3)\n\n",1,"¿Qué constitución organizó el Estado chileno durante casi un siglo, con un Presidente de la República con mucho poder?",
 ["La Constitución de 1833","La Constitución de 1925","La Constitución de 1980","El Reglamento de 1810"],"b",
 "La Constitución de 1833 rigió hasta 1925 y estableció un Ejecutivo fuerte. Las de 1925 y 1980 son posteriores, y en 1810 aún no había constitución.","OA 3",H)
q("",1,"¿Qué ministro de la década de 1830 se asocia a la idea de un gobierno fuerte, ordenado e impersonal, que influyó en la organización del Estado?",
 ["Diego Portales","Bernardo O'Higgins","José Miguel Carrera","Arturo Prat"],"a",
 "Diego Portales defendió un gobierno con autoridad fuerte y respeto al orden, ideas que marcaron la Constitución de 1833. O'Higgins y Carrera son de la Independencia, y Prat es un marino de la Guerra del Pacífico.","OA 3",H)
q("### La conformación del territorio chileno en el siglo XIX (OA 5)\n\n",1,"¿Qué territorios incorporó Chile tras la Guerra del Pacífico (1879-1884)?",
 ["Las regiones de Antofagasta y Tarapacá, ricas en salitre","La isla de Chiloé y el archipiélago de las Guaitecas, al sur","La Araucanía, el territorio al sur del río Biobío","El Estrecho de Magallanes y toda la Patagonia oriental"],"c",
 "Después de la guerra contra Perú y Bolivia, Chile incorporó Antofagasta y Tarapacá, con grandes yacimientos de salitre (Arica quedó en Chile por el tratado de 1929). La Araucanía y Magallanes se incorporaron por otros procesos.","OA 5",H)
q("",2,"Entre 1861 y 1883 el Estado chileno ocupó militarmente la Araucanía. ¿Qué consecuencia tuvo este proceso para el pueblo mapuche?",
 ["Perdió gran parte de sus tierras y fue reducido a terrenos pequeños llamados reducciones","Recibió más tierras que antes y se convirtió en dueño de todo el sur","No tuvo ningún efecto, porque el pueblo mapuche se trasladó a Argentina","Obtuvo el control del gobierno de Chile y de su capital, Santiago"],"d",
 "Con la ocupación, el Estado tomó las tierras mapuche, las vendió o entregó a colonos, y a las comunidades les asignó reducciones pequeñas. Esto afectó profundamente su forma de vida.","OA 5",H)
q("### La progresiva democratización de la sociedad en el siglo XX (OA 7)\n\n",1,"¿Qué grupos obtuvieron el derecho a votar con la reforma constitucional de 1970?",
 ["Los jóvenes desde los 18 años y las personas que no sabían leer ni escribir","Solo los hombres mayores de 25 años que fueran dueños de tierras","Las mujeres, que votaron por primera vez en una elección municipal","Los extranjeros que vivieran en Chile, sin importar su edad"],"a",
 "La reforma de 1970 bajó la edad para votar a 18 años y permitió votar a quienes no sabían leer ni escribir. El voto municipal femenino es anterior (1934-1935).","OA 7",H)
q("",1,"En 1920 se dictó la Ley de Instrucción Primaria Obligatoria. ¿Por qué fue un paso hacia una sociedad más democrática?",
 ["Porque obligó a todos los niños y niñas a asistir a la escuela primaria","Porque permitió que solo los hijos de familias ricas estudiaran en las universidades","Porque cerró las escuelas públicas para que toda la educación fuera privada","Porque eliminó la lectura de las clases para dedicarlas al trabajo agrícola"],"b",
 "Hacer obligatoria la educación primaria permitió que más personas aprendieran a leer y escribir, participaran en la vida pública y accedieran a mejores trabajos.","OA 7",H)
q("### El quiebre y la recuperación de la democracia (OA 8)\n\n",1,"¿Quién asumió en marzo de 1990 como el primer presidente elegido democráticamente después del régimen militar?",
 ["Patricio Aylwin","Salvador Allende","Eduardo Frei Montalva","Arturo Alessandri Palma"],"c",
 "Patricio Aylwin ganó la elección de diciembre de 1989 y asumió en marzo de 1990, lo que marcó el retorno a la democracia. Allende, Frei Montalva y Alessandri gobernaron antes de 1973.","OA 8",H)
q("",3,"Después de recuperar la democracia, en 1990 se creó la Comisión Nacional de Verdad y Reconciliación. ¿Para qué sirvió y por qué es importante?",
 ["Para investigar las violaciones a los derechos humanos del régimen militar y conocer la verdad","Para organizar las elecciones municipales y elegir a los alcaldes de todas las comunas del país","Para escribir una nueva constitución que reemplazara de inmediato a la de 1980","Para decidir qué partidos políticos podían participar en el plebiscito de octubre de 1988"],"d",
 "La Comisión, conocida como Comisión Rettig, investigó violaciones graves a los derechos humanos ocurridas entre 1973 y 1990. Reconocer la verdad ayuda a reparar a las víctimas y a que la sociedad no repita esos hechos.","OA 8",H)
q("### Continuidad y cambio en la sociedad chilena (OA 9)\n\n",1,"¿Cuál de los siguientes elementos es una **continuidad** entre el Chile de 1900 y el Chile actual?",
 ["La celebración de las Fiestas Patrias en septiembre","El uso de internet para comunicarse","Que la mayoría de la población viva en ciudades","El derecho de las mujeres a votar en elecciones presidenciales"],"a",
 "Una continuidad es algo que se mantiene en el tiempo: las Fiestas Patrias se celebran desde el siglo XIX. Internet, la mayoría urbana y el voto femenino presidencial son cambios del siglo XX y XXI.","OA 9",H)
q("## EJE 2 — GEOGRAFÍA (preguntas 14 a 17)\n\n### Las regiones político-administrativas de Chile (OA 11)\n\n",1,"¿Cuántas regiones tiene Chile actualmente?",
 ["16 regiones","15 regiones","13 regiones","12 regiones"],"c",
 "Chile tiene 16 regiones desde 2018, cuando se creó la Región de Ñuble a partir de una parte de la Región del Biobío.","OA 11",G)
q("",1,"¿Cuál es la capital de la Región del Biobío?",
 ["Concepción","Chillán","Talca","Temuco"],"b",
 "Concepción es la capital del Biobío. Chillán es la capital de Ñuble, Talca la del Maule y Temuco la de La Araucanía.","OA 11",G)
q("### Los ambientes naturales de Chile (OA 12)\n\n",1,"En el ambiente mediterráneo de la zona central, con inviernos lluviosos y veranos secos y cálidos, ¿qué actividad económica se ve especialmente favorecida?",
 ["La agricultura de frutales y viñas","La crianza de llamas y alpacas","La pesca en canales y fiordos","La extracción de hielo de los glaciares"],"d",
 "El clima templado y los valles fértiles favorecen los frutales y las viñas. Las llamas se crían en el altiplano y los fiordos están en la zona austral.","OA 12",G)
q("",2,"En el ambiente frío de la Patagonia, con vientos fuertes y bajas temperaturas, ¿cómo se han adaptado sus habitantes?",
 ["Con viviendas abrigadas, calefacción a leña y crianza de ovejas, que resisten el frío","Con casas sin ventanas para protegerse del calor del desierto todo el año","Con cultivos de plátanos y piñas, que necesitan mucho calor y humedad para crecer","Con atrapanieblas, porque en la Patagonia nunca llueve ni nieva durante el año"],"a",
 "Las personas adaptan su vivienda, su calefacción y sus actividades al clima: en la Patagonia se crían ovejas y las casas se construyen para conservar el calor.","OA 12",G)
q("## EJE 3 — FORMACIÓN CIUDADANA (preguntas 18 a 25)\n\n### La organización democrática de Chile (OA 15)\n\n",1,"¿Qué poder del Estado tiene como función principal elaborar y aprobar las leyes?",
 ["El Poder Legislativo, formado por el Senado y la Cámara de Diputados","El Poder Judicial, formado por los tribunales de justicia","El Poder Ejecutivo, encabezado por el Presidente de la República","La municipalidad de cada comuna, encabezada por el alcalde"],"c",
 "El Congreso Nacional (Poder Legislativo) discute y aprueba las leyes. El Poder Judicial las aplica en los juicios y el Ejecutivo gobierna y administra el país.","OA 15",F)
q("",1,"¿Cada cuántos años se elige al Presidente o Presidenta de la República en Chile?",
 ["Cada 4 años, sin reelección inmediata","Cada 6 años, con reelección inmediata","Cada 2 años, junto con los alcaldes","Una sola vez, porque el cargo dura toda la vida"],"b",
 "El período presidencial dura 4 años y quien gobierna no puede postular de inmediato al período siguiente. Así se renuevan las autoridades periódicamente.","OA 15",F)
q("### La Constitución Política de Chile (OA 16)\n\n",1,"¿Qué es la Constitución Política de la República?",
 ["La ley fundamental que organiza el Estado y reconoce derechos y deberes","Un reglamento interno que solo se aplica dentro de los colegios del país","Un documento histórico que ya no tiene ningún valor legal","Una lista con los nombres de las autoridades elegidas en la última elección"],"d",
 "La Constitución es la ley más importante: organiza los poderes del Estado y reconoce derechos y deberes. Ninguna otra ley puede contradecirla.","OA 16",F)
q("",2,"La Constitución reparte el poder entre el Ejecutivo, el Legislativo y el Judicial. ¿Por qué es importante esta separación de poderes?",
 ["Porque evita que una sola autoridad concentre todo el poder y cometa abusos","Porque permite que el Presidente haga las leyes y también juzgue a las personas","Porque así las autoridades no necesitan rendir cuentas a nadie","Porque hace que los tribunales elijan a los diputados y senadores"],"a",
 "Al estar repartido, cada poder controla a los otros: así se protege la democracia y los derechos de las personas frente a posibles abusos.","OA 16",F)
q("### Todas las personas tienen derechos que deben ser respetados (OA 17)\n\n",1,"Los derechos humanos no se pueden vender, regalar ni renunciar a ellos. ¿Cómo se llama esta característica?",
 ["Son irrenunciables","Son temporales","Son opcionales","Son exclusivos"],"c",
 "Los derechos humanos son irrenunciables (e inalienables): nadie puede quitárselos ni renunciar a ellos, ni siquiera por voluntad propia. Además son universales y permanentes.","OA 17",F)
q("",2,"¿Qué situaciones **vulneran** derechos de las personas?",
 ["Negarle la matrícula a un niño por su nacionalidad","Ofrecer clases de reforzamiento gratuitas en un colegio","Impedir que una persona exprese su opinión de forma pacífica","No atender en un consultorio a un adulto mayor por su edad"],"acd",
 "a, c y d. Discriminar por nacionalidad o por edad y silenciar una opinión pacífica vulneran derechos (educación, salud, libertad de expresión). Ofrecer reforzamiento gratuito, en cambio, ayuda a ejercer el derecho a la educación.","OA 17",F)
q("### Los derechos generan deberes y responsabilidades (OA 18)\n\n",1,"¿Qué deber se relaciona con el derecho a vivir en un medio ambiente libre de contaminación?",
 ["Cuidar el entorno: no botar basura y reciclar","Exigir que otros limpien lo que uno ensucia","Usar el auto incluso para trayectos muy cortos","Quemar la basura del hogar en el patio"],"b",
 "Si todos tenemos derecho a un ambiente limpio, todos debemos cuidarlo. Quemar basura o usar el auto sin necesidad contamina el aire.","OA 18",F)
q("",3,"> **Estímulo — caso:** En un curso de sexto básico se elegirá la directiva. Hay tres candidaturas y cada estudiante puede votar.\n\n¿Qué deberes acompañan el derecho a elegir la directiva y por qué son importantes?",
 ["Informarse, votar con responsabilidad y respetar el resultado aunque pierda su opción, porque la democracia necesita participación","Ninguno, porque si tienen derecho a votar pueden hacerlo sin pensar y después ignorar por completo el resultado","Votar por quien diga la mayoría de los amigos, porque así se evitan todos los conflictos dentro del curso","Votar solo si la candidatura favorita tiene posibilidades de ganar; si no, es mucho mejor no participar"],"d",
 "Votar es un derecho que trae deberes: informarse, decidir con responsabilidad y aceptar el resultado. Sin esos deberes, la elección perdería sentido y la convivencia se debilitaría.","OA 18",F)
armar(C/'historia-geografia-y-cs-sociales-examen-forma-b.md', C/'historia-geografia-y-cs-sociales-examen-forma-a.md', Q,
  fila=lambda i,p,cl: f"| {i} | {p.extra['tipo']} | **{cl}.** {p.explicacion.split('. ',1)[1] if len(p.letra)>1 else p.explicacion} | {p.oa} | {p.extra['eje']} | {p.extra['pts']} |",
  reemplazos={"Forma B":"Forma A","**Forma B**":"**Forma A**","ultima_actualizacion: 2026-11-02":"ultima_actualizacion: 2026-11-16","(misma asignatura, preguntas distintas)":"(misma asignatura, preguntas distintas de la guía y de la Forma B)"},
  inicio_preguntas="## EJE 1")
if __name__=="__main__":
    from collections import Counter; print(Counter(p.letra for p in Q), len(Q))
