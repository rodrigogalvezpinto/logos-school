import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from forma_a import P, armar  # noqa: E402
C=Path(__file__).resolve().parents[4]/'contenido'/'06-basico/examenes'
H="**Pregunta {n} (alternativas).** "
Q=[]
def q(sec,en,ops,l,ex,oa,eje): Q.append(P(sec,H,en,ops,l,ex,oa,{"eje":eje}))
N="Números y Operaciones"; PA="Patrones y Álgebra"; G="Geometría"; M="Medición y Datos y Probabilidades"
q("## Eje 1: Números y Operaciones\n\n","Un estadio vendió 2.340 entradas a $4.500 cada una. Usando calculadora, ¿cuánto dinero se recaudó en total?",
 ["$10.530.000","$1.053.000","$10.350.000","$6.840"],"b","2.340 × 4.500 = 10.530.000. Sumar 2.340 + 4.500 = 6.840 no corresponde: hay 2.340 entradas de igual precio.","OA 2",N)
q("","Una escuela tiene $25.000.000 para comprar computadores que cuestan $380.000 cada uno. ¿Cuántos computadores completos puede comprar y cuánto dinero le sobra?",
 ["65 computadores y sobran $300.000","66 computadores y no sobra dinero","65 computadores y sobran $3.000","64 computadores y sobran $680.000"],"a","25.000.000 ÷ 380.000 = 65,78…: alcanzan 65 computadores completos. 65 × 380.000 = 24.700.000, y 25.000.000 − 24.700.000 = 300.000.","OA 2",N)
q("","En un curso hay 18 niñas y 12 niños. ¿Cuál es la razón simplificada entre niñas y niños?",
 ["3:2","2:3","18:30","6:4"],"c","18:12 dividido por 6 es 3:2. 2:3 invierte el orden pedido (niñas:niños), 18:30 compara niñas con el total y 6:4 aún se puede simplificar.","OA 3",N)
q("","Una receta usa harina y azúcar en la razón 4:3. Si se usan 12 tazas de harina, ¿cuántas tazas de azúcar se necesitan?",
 ["9 tazas","11 tazas","16 tazas","3 tazas"],"d","12 ÷ 4 = 3 es el factor de amplificación; 3 × 3 = 9 tazas de azúcar. Así la razón 12:9 sigue siendo equivalente a 4:3. Restar 1 a cada término (11) no mantiene la razón.","OA 3",N)
q("","¿Qué porcentaje representa la fracción 2/5?",
 ["40 %","25 %","20 %","52 %"],"a","2/5 = 40/100 = 40 %. Para pasar a centésimos se amplifica por 20.","OA 4",N)
q("","Una bicicleta cuesta $120.000 y tiene un 15 % de descuento. ¿Cuánto se paga por ella?",
 ["$102.000","$18.000","$105.000","$138.000"],"c","El descuento es 0,15 × 120.000 = 18.000; se paga 120.000 − 18.000 = 102.000. $18.000 es solo el descuento y $138.000 suma en vez de restar.","OA 4",N)
q("","En una encuesta a 240 estudiantes, el 35 % prefiere el básquetbol. ¿Cuántos estudiantes prefieren el básquetbol?",
 ["84 estudiantes","35 estudiantes","156 estudiantes","70 estudiantes"],"b","0,35 × 240 = 84. Los 156 restantes son los que prefieren otro deporte.","OA 4",N)
q("","¿Qué fracción impropia es equivalente al número mixto 4 3/7?",
 ["31/7","43/7","28/7","19/7"],"d","4 enteros son 28/7; 28/7 + 3/7 = 31/7. 43/7 solo junta las cifras del número mixto y 28/7 olvida la parte fraccionaria.","OA 5",N)
q("","¿Cuál es el número mixto equivalente a 27/6, simplificado?",
 ["4 1/2","4 1/3","3 1/2","4 2/3"],"a","27 ÷ 6 = 4, resto 3 → 4 3/6, y 3/6 simplificado es 1/2: 4 1/2.","OA 5",N)
q("","Calcula: 4 1/6 − 1 3/4 = ?",
 ["2 5/12","3 7/12","2 7/12","2 1/12"],"c","4 1/6 = 50/12 y 1 3/4 = 21/12; 50/12 − 21/12 = 29/12 = 2 5/12. Restar «al revés» las fracciones (3/4 − 1/6) para no canjear un entero lleva al error 3 7/12.","OA 8",N)
q("","Una piscina inflable tenía 45,6 litros de agua y se le agregaron 18,75 litros. ¿Cuántos litros tiene ahora?",
 ["64,35 litros","63,35 litros","46,35 litros","64,81 litros"],"b","Alineando la coma: 45,60 + 18,75 = 64,35. 46,35 sale de sumar 0,75 en vez de 18,75.","OA 8",N)
q("## Eje 2: Patrones y Álgebra\n\n","Resuelve: x − 38 = 75. ¿Cuál es el valor de x?",
 ["113","37","103","123"],"d","x = 75 + 38 = 113. Comprobación: 113 − 38 = 75. Restar (75 − 38 = 37) no despeja la incógnita.","OA 11",PA)
q("","Una biblioteca prestó algunos libros el lunes y 27 el martes. Entre los dos días prestó 81 libros. Si x es la cantidad del lunes, ¿qué ecuación representa la situación y cuál es su solución?",
 ["x + 27 = 81; x = 54 libros","x − 27 = 81; x = 108 libros","x + 81 = 27; x = 54 libros","x + 27 = 81; x = 108 libros"],"a","Lo del lunes (x) más lo del martes (27) es el total (81): x = 81 − 27 = 54. Comprobación: 54 + 27 = 81.","OA 11",PA)
q("## Eje 3: Geometría\n\n","Dos calles rectas se cruzan. Uno de los ángulos que forman mide 112°. ¿Cuánto mide el ángulo opuesto por el vértice a ese ángulo?",
 ["112°","68°","248°","78°"],"c","Los ángulos opuestos por el vértice miden lo mismo: 112°. 68° es el adyacente (180° − 112°).","OA 16",G)
q("","Dos rectas se cortan y uno de los cuatro ángulos que forman mide 90°. ¿Cuánto miden los otros tres ángulos?",
 ["90°, 90° y 90°","90°, 180° y 90°","45°, 45° y 90°","90°, 270° y 90°"],"b","El opuesto por el vértice mide 90°, y cada adyacente mide 180° − 90° = 90°: las rectas son perpendiculares y los cuatro ángulos son rectos.","OA 16",G)
q("## Eje 4: Medición y Datos y Probabilidades\n\n","¿Cuál es el área total de un cubo cuyas aristas miden 7 cm?",
 ["294 cm²","343 cm²","49 cm²","196 cm²"],"d","Una cara mide 7 × 7 = 49 cm²; el cubo tiene 6 caras: 6 × 49 = 294 cm². 343 es el volumen en cm³ y 49 es una sola cara.","OA 18",M)
q("","¿Cuál es el área total de una caja con forma de paralelepípedo de 12 cm de largo, 5 cm de ancho y 3 cm de alto?",
 ["222 cm²","180 cm²","111 cm²","444 cm²"],"a","2 × (12 × 5) + 2 × (12 × 3) + 2 × (5 × 3) = 120 + 72 + 30 = 222 cm². 180 es el volumen en cm³ y 111 resulta de no duplicar las caras.","OA 18",M)
q("","Se quiere pintar por fuera un contenedor cúbico de 2 m de arista, todas sus caras **excepto la base**, que va apoyada en el suelo. ¿Cuántos m² se deben pintar?",
 ["20 m²","24 m²","8 m²","16 m²"],"c","Cada cara mide 2 × 2 = 4 m²; sin la base quedan 5 caras: 5 × 4 = 20 m². 24 m² incluye la base y 8 m³ es el volumen.","OA 18",M)
q("","¿Cuál es el volumen de una caja de 8 cm de largo, 4 cm de ancho y 3 cm de alto?",
 ["96 cm³","136 cm³","15 cm³","48 cm³"],"b","Volumen = largo × ancho × alto = 8 × 4 × 3 = 96 cm³. 136 es el área total y 15 es la suma de las medidas.","OA 19",M)
q("","Una pecera mide 50 cm de largo, 25 cm de ancho y 40 cm de alto. Si 1.000 cm³ equivalen a 1 litro, ¿cuántos litros de agua caben en ella?",
 ["50 litros","5 litros","500 litros","115 litros"],"d","50 × 25 × 40 = 50.000 cm³, y 50.000 ÷ 1.000 = 50 litros. 115 es la suma de las medidas.","OA 19",M)
q("","Se lanza un dado común 240 veces. ¿Aproximadamente cuántas veces esperarías obtener un número **mayor que 4**?",
 ["80 veces","40 veces","120 veces","160 veces"],"a","Los números mayores que 4 son 5 y 6: 2 de 6 resultados, un tercio. 240 ÷ 3 = 80. 40 veces sería lo esperado para un solo número.","OA 23",M)
q("","Un local de sándwiches ofrece 3 tipos de pan y 5 rellenos. Usando la idea de diagrama de árbol, ¿cuántos sándwiches distintos de un pan y un relleno se pueden formar?",
 ["15 sándwiches","8 sándwiches","5 sándwiches","3 sándwiches"],"c","Por cada pan hay 5 rellenos: 3 × 5 = 15. Sumar 3 + 5 = 8 no cuenta todas las combinaciones.","OA 23",M)
q("","El gráfico circular muestra el deporte preferido de 360 personas encuestadas:\n\n::circular::Fútbol=45;Otros deportes=55::\n\n¿Cuántas personas prefieren el fútbol?",
 ["162 personas","45 personas","198 personas","315 personas"],"b","El 45 % de 360 es 0,45 × 360 = 162. 198 son las que prefieren otros deportes (55 %).","OA 24",M)
q("","El gráfico de barras dobles muestra cuántos libros leyeron dos cursos en marzo y abril:\n\n::barras::Marzo=24/30;Abril=35/28::leyenda=Curso A/Curso B;y=Libros leídos;valores=si::\n\n¿En qué mes el curso A leyó más libros que el curso B, y cuántos más?",
 ["En abril, con 7 libros más que el curso B","En marzo, con 6 libros más que el curso B","En abril, con 35 libros más que el curso B","En marzo, con 54 libros más que el curso B"],"d","En abril el curso A leyó 35 y el B, 28: 35 − 28 = 7 más. En marzo el curso A leyó menos (24 contra 30).","OA 24",M)
q("","El gráfico circular muestra cómo se reparte el presupuesto de un paseo de curso:\n\n::circular::Alimentación=50;Transporte=30;Entradas=20::\n\nSi el curso cuenta con $2.400.000, ¿cuánto dinero corresponde a cada categoría?",
 ["Alimentación $1.200.000, transporte $720.000 y entradas $480.000","Alimentación $50.000, transporte $30.000 y entradas $20.000","Alimentación $1.200.000, transporte $700.000 y entradas $500.000","$800.000 para cada una de las tres categorías"],"a","Alimentación: 50 % de 2.400.000 = 1.200.000; transporte: 30 % = 720.000; entradas: 20 % = 480.000. Las tres cantidades suman 2.400.000.","OA 24",M)
armar(C/'matematica-examen-forma-b.md', C/'matematica-examen-forma-a.md', Q,
  fila=lambda i,p,cl: f"| {i} | **{cl}.** {p.explicacion} | {p.oa} | {p.extra['eje']} |",
  reemplazos={"Forma B":"Forma A","relación con otras formas: versión alternativa":"relación con otras formas: versión alternativa a la Forma B","última actualización: 2026-08-11":"última actualización: 2026-11-16"},
  inicio_preguntas="## Eje 1")
if __name__=="__main__":
    from collections import Counter; print(Counter(p.letra for p in Q), len(Q))
