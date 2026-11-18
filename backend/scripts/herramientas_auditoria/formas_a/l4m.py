import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from forma_a import P, armar  # noqa: E402
C=Path(__file__).resolve().parents[4]/'contenido'/'04-medio/examenes'
A="**{n}. (Alternativas)** "
Q=[]
def q(sec,en,ops,l,ex,oa,cab=A): Q.append(P(sec,cab,en,ops,l,ex,oa))
def vf(sec,en,v,ex,oa): Q.append(P(sec,"**{n}. (Verdadero o Falso)** ",en,[],"V" if v else "F",ex,oa,{"clave":"Verdadero" if v else "Falso"}))
T12='''## Textos 1 y 2 (para las preguntas 1 a 8): dos miradas sobre migrar

**Marco didáctico ficticio:** ambos fragmentos son creaciones contemporáneas de Logos School. La ambientación de 1960 no demuestra una fecha de escritura. Para comparar producción, imagina el Texto 1 escrito en 1975 para recuperar la memoria de las familias que llegaron a la capital y el Texto 2 escrito en 2026 en un debate sobre la migración internacional; estas fechas son hipótesis, no datos bibliográficos. Para recepción considera dos audiencias de 2026: familias cuyos abuelos migraron del sur a Santiago y jóvenes que llegaron a Chile desde otros países. Son experiencias que pueden orientar lecturas, no reacciones universales.

**Texto 1 — "La maleta de cartón" (fragmento de novela, ambientada en 1960, Santiago)**

> Mi madre llegó a Santiago en junio de 1960, pocos días después del terremoto de Valdivia, con una maleta de cartón amarrada con un cordel. Adentro traía dos vestidos, una foto de su casa derrumbada y una bolsa de harina. Nadie la esperaba en la estación. Con otras familias del sur levantó una mediagua de tablas en una toma, al borde de la ciudad, donde no había agua ni luz.
>
> "Aquí nadie nos esperaba", decía siempre, "pero tampoco nadie nos iba a echar".

**Texto 2 — "Dos acentos" (fragmento de cuento, ambientado en la actualidad, Antofagasta)**

> Valentina llegó desde Caracas hace un año. En el liceo ya dice «cachai» y «al tiro», pero sus compañeros todavía la llaman «la venezolana», aunque ella preferiría que la llamaran por su nombre. En la casa, su madre le pide que no olvide cómo se preparan las arepas del domingo.
>
> "Tengo dos acentos", piensa mientras camina por la costanera, "y ninguno me alcanza para estar completa".

'''
q(T12,"¿Qué contexto histórico de producción y de ambientación ayuda a comprender la experiencia narrada en el Texto 1?",
 ["La llegada de inmigrantes europeos a los puertos del país a fines del siglo XIX","*El terremoto de 1960 y la migración hacia Santiago, con familias que levantaron tomas en la periferia","La Guerra del Pacífico y el traslado de soldados desde el norte hacia la capital","La crisis del salitre y el cierre de las oficinas de la pampa en la década de 1930"],"b",
 "El Texto 1 se ambienta tras el terremoto de 1960, cuando muchas familias del sur migraron a Santiago y se instalaron en tomas en la periferia, sin agua ni luz.","OA N°1 — contexto de producción")
q("","¿Desde qué perspectiva se narra principalmente la llegada a Santiago en el Texto 1?",
 ["Desde la mirada de un funcionario que recibe a los damnificados en la estación","Desde un narrador omnisciente que conoce los pensamientos de todas las familias","*Desde la voz de un hijo o una hija que recuerda la experiencia de su madre","Desde la perspectiva de los vecinos de la ciudad que observan la toma"],"c",
 "El narrador dice «Mi madre llegó…»: es la voz de un hijo o una hija que reconstruye, desde la memoria familiar, la experiencia de su madre.","OA N°1 — perspectiva adoptada")
q("","¿Qué elemento comparten ambos textos, a pesar de sus contextos distintos?",
 ["*La llegada a un lugar ajeno y el esfuerzo por construir pertenencia en él","Un narrador en primera persona que cuenta su propia llegada a la ciudad","La descripción detallada de un terremoto y de sus consecuencias en el norte","La crítica explícita a las autoridades que no ayudaron a las familias"],"a",
 "Ambos textos tratan la llegada a un lugar donde nadie espera a sus protagonistas y el esfuerzo por pertenecer: la mediagua en la toma y los «dos acentos» de Valentina.","OA N°1 — comparación del tratamiento del tema")
vf("","\"El Texto 2 muestra que Valentina se siente dividida entre dos identidades culturales, sin sentirse completa en ninguna.\"",True,
 "Verdadero. La frase «Tengo dos acentos… y ninguno me alcanza para estar completa» expresa que Valentina se siente entre dos identidades sin pertenecer del todo a ninguna.","OA N°1 — perspectiva adoptada")
q("","¿Cómo influye el contexto del Texto 1 en la elección de la «maleta de cartón» como imagen central?",
 ["Indica que la familia era rica y podía comprar maletas nuevas en cada viaje","Muestra que la madre trabajaba en una fábrica de maletas de la capital","Representa la tecnología moderna que llegó al país después del terremoto","*Condensa la pobreza de quienes lo perdieron todo y llegaron solo con lo esencial"],"d",
 "La maleta de cartón amarrada con un cordel, con dos vestidos y una foto de la casa derrumbada, condensa la pérdida y la pobreza de quienes migraron tras el terremoto con lo mínimo.","OA N°1 — contexto de producción y recursos literarios")
q("","¿Qué tipo de dificultad enfrenta principalmente cada personaje?",
 ["Texto 1: aprender un idioma nuevo en la ciudad. Texto 2: conseguir una vivienda en una toma de terreno","*Texto 1: la falta de vivienda y de recibimiento. Texto 2: la pertenencia y la identidad cultural","Texto 1: un conflicto con su hija mayor. Texto 2: un conflicto con sus profesores del liceo","Ambos textos: la falta de trabajo en el puerto de Antofagasta y en la capital"],"b",
 "La madre del Texto 1 enfrenta la falta de vivienda y de recibimiento (nadie la esperaba, una mediagua sin agua ni luz); Valentina, la pertenencia y la identidad (la llaman «la venezolana»).","OA N°1 — comparación del tratamiento del tema")
q("","¿Qué efecto produce que el Texto 2 esté narrado en tercera persona, pero centrado en lo que piensa Valentina?",
 ["*Permite acceder a su conflicto interior y, a la vez, mostrarlo con cierta distancia","Impide conocer lo que siente Valentina, porque solo describe lo que hace","Convierte el relato en una noticia objetiva sobre la migración en Chile","Hace que el narrador critique abiertamente a los compañeros de Valentina"],"a",
 "La tercera persona centrada en Valentina da acceso a su conflicto interior («Tengo dos acentos…») y, al mismo tiempo, lo muestra con cierta distancia, como observado desde fuera.","OA N°1 — perspectiva y su efecto")
q("","Considerando los contextos hipotéticos de producción y las dos audiencias descritas al inicio, ¿qué afirmaciones son pertinentes y no universalizan reacciones? Marca **todas** las correctas.",
 ["Familias cuyos abuelos migraron del sur pueden reconocer su historia en la maleta y leer el Texto 2 como una continuidad","Jóvenes que llegaron de otros países pueden identificarse con los dos acentos y releer el Texto 1 como un antecedente","Todos los lectores reaccionarán de la misma forma ante ambos textos, sin importar su propia experiencia","La producción hipotética contrapone la memoria de 1975 con un debate sobre la migración en 2026"],"abd",
 "a, b y d relacionan la producción y la recepción con experiencias posibles de cada audiencia; c universaliza una reacción, algo que el marco pide evitar.","OA N°1 — comparación de producción, recepción, perspectiva y efecto estético",cab="**{n}. (Varias correctas)** ")
T3='''## Texto 3 (para las preguntas 9 a 16): "Un viernes distinto: por qué los liceos deberían probar los talleres" (columna de opinión)

> Llevo veinte años dirigiendo un liceo técnico de Rancagua y he visto cómo el viernes se convierte en el día con más ausencias. Por eso propongo que los liceos prueben, durante un semestre, un viernes dedicado a talleres prácticos —electricidad, cocina, robótica, teatro— en lugar de clases tradicionales.
>
> Un estudio de un centro de investigación educacional de una universidad, citado por un diario nacional, habría encontrado que los liceos con un día de talleres redujeron la inasistencia en un 12 %. En nuestro liceo hicimos un ensayo durante un mes y los talleres se llenaron.
>
> No se trata de enseñar menos, sino de aprender de otra manera. Quien se oponga a probarlo solo defiende la costumbre por miedo al cambio.

'''
q(T3,"¿Cuál es la intención explícita de la columna?",
 ["Informar sin opinar sobre las ausencias de los viernes en los liceos del país","Criticar a los estudiantes que faltan los viernes por motivos personales","*Proponer que los liceos prueben un viernes de talleres prácticos durante un semestre","Pedir al Ministerio que elimine las clases del viernes en todos los liceos"],"c",
 "El autor lo dice directamente: «propongo que los liceos prueben, durante un semestre, un viernes dedicado a talleres prácticos». Esa es la intención explícita.","OA N°3 — intención explícita")
q("","¿Qué afirmación de la columna entrega pistas para intentar contrastarla con otras fuentes, aunque por sí sola no basta para verificarla?",
 ["«Llevo veinte años dirigiendo un liceo técnico de Rancagua y he visto cómo el viernes se convierte en el día con más ausencias»","«No se trata de enseñar menos, sino de aprender de otra manera», en el último párrafo de la columna","«Quien se oponga a probarlo solo defiende la costumbre por miedo al cambio», al cierre de la columna","*«Un estudio de un centro de investigación… habría encontrado que… redujeron la inasistencia en un 12 %»"],"d",
 "La mención de un estudio, un centro universitario, un diario y un porcentaje da pistas para buscar la fuente; pero, sin el nombre del estudio ni sus datos, la afirmación no puede verificarse por sí sola.","OA N°3 — veracidad de la información")
q("","¿Qué rol NO asume el autor de la columna frente a su audiencia?",
 ["*El de un investigador que presenta un estudio propio con su metodología completa","El de un director con experiencia que habla desde su trayectoria en un liceo","El de alguien que propone una medida concreta para los liceos","El de un testigo que cuenta lo que ocurrió en su propio liceo"],"a",
 "El autor cita un estudio ajeno («habría encontrado»), pero no lo realizó ni presenta su metodología: no asume el rol de investigador; sí habla como director, testigo y proponente.","OA N°3 — posicionamiento y rol del enunciador")
vf("","\"La frase final ('Quien se oponga a probarlo solo defiende la costumbre por miedo al cambio') es una evidencia verificable que demuestra la tesis de la columna.\"",False,
 "Falso. Es una generalización que atribuye a todos los opositores un mismo motivo (el miedo); no aporta evidencia y descalifica en lugar de argumentar.","OA N°3 — intención implícita")
q("","¿Qué rol asume el autor de la columna frente a su audiencia y en qué lo apoya?",
 ["El de un estudiante que habla desde su propia experiencia en clases los viernes","*El de un directivo con experiencia, que apoya su propuesta en su trayectoria y en un dato citado","El de un periodista neutral que solo informa, sin opinar, los dos lados del debate","El de un político que promete una ley nueva para todos los liceos del país"],"b",
 "El autor se presenta como director con veinte años de experiencia y apoya su propuesta en esa trayectoria, en el ensayo de su liceo y en un estudio citado.","OA N°3 — posicionamiento y rol del enunciador")
q("","¿Qué visión de fondo sostiene la columna y qué permite reconocerla?",
 ["Que los estudiantes deberían ir menos días al liceo; permite saber que el autor solo quiere más días de vacaciones","Que las clases tradicionales son inútiles; permite concluir que deben eliminarse por completo en todos los niveles","*Que el aprendizaje práctico y la motivación importan tanto como las horas en sala; permite evaluar si compartimos ese valor","Que los talleres solo sirven para entretener a los estudiantes; permite descartar la propuesta sin leerla con atención"],"c",
 "La frase «No se trata de enseñar menos, sino de aprender de otra manera» revela una visión que valora el aprendizaje práctico y la motivación; reconocerla permite evaluar si compartimos ese valor.","OA N°3 — ideología, creencias y puntos de vista")
q("","¿Qué par ejemplifica correctamente la intención explícita y una posible intención implícita de la columna?",
 ["Explícita: criticar a los profesores del liceo. Implícita: cerrar el liceo todos los viernes del año","Explícita: informar sobre la robótica. Implícita: vender herramientas de electricidad a los liceos","Explícita: pedir más vacaciones de invierno. Implícita: reducir el trabajo de los docentes del liceo","*Explícita: proponer el viernes de talleres. Implícita: mostrar a su liceo y a sí mismo como innovadores"],"d",
 "Lo explícito es la propuesta del viernes de talleres; de manera implícita, al hablar del ensayo exitoso de «nuestro liceo», el autor también proyecta una imagen innovadora de su liceo y de sí mismo.","OA N°3 — intenciones explícitas e implícitas")
q("","Sobre el estudio citado y el ensayo del liceo que menciona la columna, ¿qué afirmaciones evalúan correctamente la evidencia? Marca **todas** las correctas.",
 ["El dato del 12 % necesita la referencia completa del estudio para poder verificarse","La columna demuestra con certeza que la propuesta funcionará en todos los liceos de Chile","El cierre generaliza sobre los opositores en vez de responder a sus posibles razones","La experiencia del autor es pertinente, pero un mes de ensayo en un solo liceo no reemplaza un estudio"],"acd",
 "a, c y d evalúan los límites de la evidencia (fuente incompleta, generalización del cierre, ensayo breve en un solo liceo); b exagera lo que la columna puede demostrar.","OA N°3 — evaluación crítica integrada: intenciones, veracidad e ideología",cab="**{n}. (Varias correctas)** ")
T4='''## Sección de Producción de Textos (para las preguntas 17 a 25)

> Como autor o autora de 4° medio, debes ser capaz de **comunicar tus análisis e interpretaciones** en textos coherentes y cohesionados, adecuados al género y a la audiencia a la que te diriges. Las siguientes preguntas toman como referencia dos versiones de un mismo análisis sobre los Textos 1 y 2 de esta prueba (la comparación sobre migrar): un párrafo para un ensayo comparativo formal y el guion de un pódcast breve ("Cinco minutos de literatura") dirigido a otros estudiantes de 4° medio.
>
> *Versión (a) — párrafo de ensayo comparativo*: "Ambos textos abordan la experiencia de migrar, aunque desde épocas y desafíos distintos. 'La maleta de cartón' retrata una migración forzada por un desastre natural, centrada en la falta de vivienda, mientras que 'Dos acentos' retrata una migración internacional centrada en la identidad. Sin embargo, en los dos la pertenencia no está dada: hay que construirla. En consecuencia, comparar ambos textos permite comprender que migrar no termina al llegar, sino que continúa en el esfuerzo por ser parte de un lugar."
>
> *Versión (b) — guion de pódcast, con errores de cohesión*: "Hoy dos historias de migrar. Una es del sur, terremoto. Valentina es de Caracas. Los acentos son difíciles. Escúchenlo."

'''
q(T4,"¿Cuál es la principal diferencia de propósito entre la versión (a) y la versión (b)?",
 ["*La versión (a) argumenta una comparación fundamentada; la (b) busca despertar interés en un formato oral y breve","La versión (a) busca entretener con humor; la (b) busca informar con datos estadísticos sobre la migración","Las dos versiones tienen exactamente el mismo propósito y la misma audiencia","La versión (a) es un resumen de la noticia; la (b) es una entrevista a Valentina"],"a",
 "La versión (a) argumenta una comparación con evidencia de ambos textos; la (b), como guion de pódcast, busca despertar el interés de otros estudiantes en un formato oral y breve.","OA N°5 — propósito, género y audiencia")
q("","¿Por qué un tono cercano y oraciones breves en el guion de un pódcast para compañeros no es, por sí solo, un error?",
 ["Porque en todos los géneros, incluido el ensayo, se debe escribir de la manera más informal posible","*Porque en un pódcast dirigido a estudiantes, un tono cercano y oraciones breves son convenciones válidas del género","Porque la audiencia de 4° medio no es capaz de entender oraciones largas ni vocabulario formal","Porque en un pódcast no importa la cohesión entre las ideas que se presentan a quienes escuchan"],"b",
 "Las convenciones dependen del género y la audiencia: en un pódcast para compañeros, el tono cercano y las oraciones breves son válidos; el problema de la versión (b) es la falta de cohesión, no el registro.","OA N°5 — adecuación al género y a la audiencia")
vf("","\"En la versión (b), la oración 'Los acentos son difíciles' ayuda a avanzar en la comparación entre los dos textos.\"",False,
 "Falso. Es un comentario suelto que no se conecta con la comparación entre la madre del Texto 1 y Valentina: interrumpe la progresión temática.","OA N°5 — progresión temática")
vf("","\"Revisar un texto antes de publicarlo permite mejorar su coherencia y su cohesión, y no solo corregir la ortografía.\"",True,
 "Verdadero. La revisión permite reorganizar ideas (coherencia), mejorar los conectores (cohesión) y adecuar el texto a la audiencia, además de corregir la ortografía.","OA N°5 — proceso de escritura")
q("","¿Qué función cumplen los conectores «mientras que», «sin embargo» y «en consecuencia» en la versión (a)?",
 ["Los tres introducen ejemplos concretos y citas textuales tomados de los dos textos comparados","Los tres repiten la misma idea con palabras distintas, sin ninguna relación lógica entre las oraciones","*«Mientras que» contrasta los dos textos, «sin embargo» introduce un punto común y «en consecuencia» presenta la conclusión","Los tres indican el orden temporal en que ocurrieron los hechos narrados en ambos relatos"],"c",
 "«Mientras que» contrasta los dos tipos de migración, «sin embargo» introduce lo que ambos comparten (la pertenencia por construir) y «en consecuencia» introduce la conclusión.","OA N°5 — cohesión: conectores")
q("","¿Qué reescritura mejora la cohesión de «Una es del sur, terremoto. Valentina es de Caracas.» con un conector adecuado?",
 ["«Una historia es del sur, del terremoto, y además Valentina es de Caracas, en otro país.»","«Una historia comienza en el sur, después del terremoto. Por lo tanto, la otra sigue a Valentina, que llegó a Antofagasta desde Caracas.»","«Una historia comienza con una familia del sur, después del terremoto; porque la otra sigue a Valentina, que llegó a Chile desde Caracas.»","*«Una historia comienza con una familia que huye del terremoto del sur, mientras que la otra sigue a Valentina, que llegó desde Caracas.»"],"d",
 "La relación entre las dos ideas es de contraste: «mientras que» la expresa, y la oración completa nombra a quién se refiere cada historia. «Por lo tanto» o «porque» indicarían relaciones que no existen.","OA N°5 — cohesión (aplicación)")
q("","¿Por qué adecuar un ensayo comparativo a un guion de pódcast no implica necesariamente perder rigor?",
 ["*Porque se pueden mantener la comparación central y la evidencia de los textos, cambiando el registro y la extensión","Porque el rigor depende solo de usar muchas palabras técnicas y oraciones muy largas y complejas","Porque los pódcast nunca necesitan evidencia de los textos, solo opiniones personales del locutor","Porque adecuar significa leer en voz alta el mismo párrafo sin cambiar ninguna palabra"],"a",
 "Adecuar no es empobrecer: la comparación central y la evidencia se pueden conservar, ajustando el registro, la extensión y los recursos al nuevo formato y audiencia.","OA N°5 — adecuación al género y a la audiencia")
q("","¿Qué planificación de un texto que evalúe críticamente la columna «Un viernes distinto» es coherente?",
 ["Propósito: resumir la columna en pocas líneas. Criterios: ninguno en particular. Audiencia: no definida todavía","*Propósito: evaluar la columna. Criterios: veracidad del dato, rol del autor y visión de fondo. Audiencia: estudiantes de 4° medio","Propósito: vender talleres a otros liceos. Criterios: precio y horario de cada taller. Audiencia: empresas de la zona","Propósito: opinar sin leer la columna. Criterios: si me cae bien el autor. Audiencia: mi familia y mis amigos"],"b",
 "Una planificación coherente define el propósito (evaluar), criterios pertinentes (veracidad del dato, rol del enunciador, visión de fondo) y una audiencia concreta.","OA N°5 — planificación")
q("","Al reflexionar sobre cuál de los tres OA del año (comparar obras, evaluar críticamente discursos, producir textos propios) resultó más desafiante, ¿qué respuestas están fundamentadas con un ejemplo de esta prueba? Marca **todas** las correctas.",
 ["\"Comparar obras, porque tuve que relacionar la maleta de cartón con los dos acentos de Valentina sin confundir sus épocas.\"","\"Evaluar discursos, porque en la columna del viernes tuve que distinguir entre la experiencia del autor y la evidencia de un estudio.\"","\"Producir textos, porque al corregir la versión (b) noté que necesitaba conectores precisos y más de una revisión.\"","\"Todos fueron fáciles, porque respondí rápido y no necesité revisar nada.\""],"abc",
 "Las respuestas sobre comparar obras (la maleta de cartón y los dos acentos), evaluar discursos (la columna del viernes) y producir textos (corregir la versión b) se fundamentan con un ejemplo concreto de la prueba; la última no da ningún ejemplo.","OA N°5 — reflexión sobre el propio aprendizaje",cab="**{n}. (Varias correctas — cierre del ciclo)** ")
armar(C/'lengua-y-literatura-examen-forma-b.md', C/'lengua-y-literatura-examen-forma-a.md', Q,
  fila=lambda i,p,cl: f"| {i} | **{cl}.** {p.explicacion} | {p.oa} |",
  reemplazos={"— Forma B":"— Forma A","(Forma B)":"(Forma A)","ultima_actualizacion: 2026-11-02":"ultima_actualizacion: 2026-11-17","Esta es la **Forma B** de este examen de práctica: una segunda versión, con textos y preguntas distintos a los del banco de contenido":"Esta es la **Forma A** de este examen de práctica, con textos y preguntas propios, distintos de la Forma B y del banco de contenido"},
  inicio_preguntas="## Textos 1 y 2")
if __name__=="__main__":
    from collections import Counter; print(Counter(p.letra for p in Q), len(Q))
