import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from forma_a import P, armar  # noqa: E402
C=Path(__file__).resolve().parents[4]/'contenido'/'07-basico/examenes'
H="**Pregunta {n} (alternativas).** "
Q=[]
def q(sec,en,ops,l,ex,oa,eje): Q.append(P(sec,H,en,ops,l,ex,oa,{"eje":eje}))
N="Números y Operaciones"; PA="Patrones y Álgebra"; G="Geometría"; D="Datos y Probabilidades"
q("## Eje 1: Números y Operaciones\n\n","Un ascensor está en el piso −3 (tercer subterráneo) y sube 8 pisos. ¿En qué piso queda?",
 ["Piso 5","Piso −11","Piso 11","Piso −5"],"c","Subir es sumar: −3 + 8 = 5. Partiendo en −3, se pasa por el 0 y se llega al piso 5. −11 resulta de restar en vez de sumar.","OA 1",N)
q("","En Calama, a las 5:00 la temperatura era −4 °C y a las 14:00 llegó a 22 °C. ¿Cuántos grados subió la temperatura?",
 ["26 °C","18 °C","−26 °C","22 °C"],"a","22 − (−4) = 22 + 4 = 26 °C. 18 °C resulta de restar 4 en vez de sumarlo.","OA 1",N)
q("","Calcula: −8 − (−15).",
 ["7","−23","−7","23"],"d","Restar un número negativo equivale a sumar su opuesto: −8 − (−15) = −8 + 15 = 7.","OA 1",N)
q("","Calcula: 5/6 × 3/10.",
 ["1/4","8/16","15/6","1/2"],"b","(5 × 3)/(6 × 10) = 15/60, que simplificado por 15 es 1/4. 8/16 suma numeradores y denominadores en vez de multiplicar.","OA 3",N)
q("","Calcula: 7,2 ÷ 0,9.",
 ["8","0,8","80","6,48"],"a","Amplificando ambos números por 10 se elimina la coma: 72 ÷ 9 = 8. 6,48 es el producto 7,2 × 0,9, no el cociente.","OA 3",N)
q("","Una botella tiene 2 1/4 litros de jugo y se reparte en vasos de 1/4 de litro cada uno. ¿Cuántos vasos se llenan?",
 ["9 vasos","8 vasos","12 vasos","5 vasos"],"c","2 1/4 = 9/4; 9/4 ÷ 1/4 = 9/4 × 4/1 = 9. Dividir el total por la capacidad de cada vaso indica cuántos vasos se llenan.","OA 3",N)
q("","Usando la relación entre porcentajes y fracciones, ¿cuánto es el 25 % de $96.000?",
 ["$24.000","$2.400","$25.000","$72.000"],"d","El 25 % es la cuarta parte: 96.000 ÷ 4 = 24.000. $72.000 es el 75 % restante y $2.400, el 2,5 %.","OA 4",N)
q("","Un sueldo de $600.000 aumenta en un 8 %. ¿Cuál es el nuevo sueldo?",
 ["$648.000","$608.000","$48.000","$680.000"],"b","Aumento: 0,08 × 600.000 = 48.000; nuevo sueldo: 600.000 + 48.000 = 648.000. $608.000 confunde 8 % con $8.000 y $48.000 es solo el aumento.","OA 4",N)
q("","Una polera cuesta $16.000 después de un descuento del 20 %. ¿Cuál era su precio original?",
 ["$20.000","$19.200","$12.800","$16.200"],"a","Si se descontó el 20 %, $16.000 es el 80 % del precio original: 16.000 ÷ 0,8 = 20.000. Comprobación: 20 % de 20.000 = 4.000 y 20.000 − 4.000 = 16.000. $19.200 resulta de sumar el 20 % de 16.000.","OA 4",N)
q("## Eje 2: Patrones y Álgebra\n\n","¿Qué expresión algebraica representa «el cuádruple de un número, disminuido en 9»?",
 ["4x − 9","4(x − 9)","9 − 4x","x⁴ − 9"],"c","Primero se multiplica el número por 4 (4x) y luego se resta 9: 4x − 9. 4(x − 9) restaría 9 antes de multiplicar, y x⁴ es una potencia, no el cuádruple.","OA 6",PA)
q("","Una secuencia de figuras tiene 6 cuadraditos en la figura 1, 11 en la figura 2 y 16 en la figura 3. ¿Qué expresión representa la cantidad de cuadraditos en la figura n?",
 ["5n + 1","n + 5","6n","5n + 6"],"b","Cada figura agrega 5 cuadraditos, así que la expresión es 5n + algo; para n = 1 debe dar 6: 5 · 1 + 1 = 6. Comprobación: 5 · 2 + 1 = 11 y 5 · 3 + 1 = 16.","OA 6",PA)
q("","La suma de dos números pares consecutivos es 54. Si x es el menor, ¿qué ecuación se plantea y cuáles son los números?",
 ["x + (x + 2) = 54; 26 y 28","x + (x + 1) = 54; 26 y 27","2x = 54; 27 y 27","x + 2x = 54; 18 y 36"],"d","Dos pares consecutivos se diferencian en 2: x + (x + 2) = 54 → 2x + 2 = 54 → x = 26. Los números son 26 y 28, que suman 54.","OA 6",PA)
q("","Si 4 kg de paltas cuestan $10.800, ¿cuánto cuestan 7 kg manteniendo la misma proporción?",
 ["$18.900","$19.000","$75.600","$13.500"],"a","Un kilo cuesta 10.800 ÷ 4 = 2.700; 7 × 2.700 = 18.900. $75.600 multiplica 10.800 × 7 sin calcular primero el precio por kilo.","OA 8",PA)
q("","Para recorrer siempre la misma distancia, ¿qué relación hay entre la rapidez de un vehículo y el tiempo que demora?",
 ["Proporcionalidad inversa: a mayor rapidez, menos tiempo","Proporcionalidad directa: a mayor rapidez, más tiempo","No hay ninguna relación entre la rapidez y el tiempo","Son siempre iguales: la rapidez y el tiempo valen lo mismo"],"c","Si la rapidez se duplica, el tiempo se reduce a la mitad: el producto rapidez × tiempo (la distancia) se mantiene constante. Eso es proporcionalidad inversa.","OA 8",PA)
q("","Ocho albañiles construyen un muro en 15 días. Trabajando al mismo ritmo, ¿cuántos días demorarían 10 albañiles?",
 ["12 días","18 días","13 días","10 días"],"b","Es proporcionalidad inversa: albañiles × días es constante, 8 × 15 = 120; con 10 albañiles, 120 ÷ 10 = 12 días. Pensar que más albañiles demoran más (18 días) sería tratarla como directa.","OA 8",PA)
q("## Eje 3: Geometría\n\n","Un plato tiene 24 cm de diámetro. ¿Cuánto mide su radio?",
 ["12 cm","48 cm","6 cm","75,36 cm"],"d","El radio es la mitad del diámetro: 24 ÷ 2 = 12 cm. 48 cm duplica el diámetro y 75,36 cm es el perímetro del plato.","OA 11",G)
q("","Una rueda tiene 10 cm de radio. ¿Cuál es su perímetro aproximado? (usa π ≈ 3,14)",
 ["62,8 cm","31,4 cm","314 cm","20 cm"],"a","Perímetro = 2 × π × r = 2 × 3,14 × 10 = 62,8 cm. 31,4 cm olvida multiplicar por 2 y 314 corresponde al área (π × r²).","OA 11",G)
q("","Un aspersor riega un círculo de 6 m de radio. ¿Cuál es el área aproximada que riega? (π ≈ 3,14)",
 ["113,04 m²","37,68 m²","36 m²","18,84 m²"],"c","Área = π × r² = 3,14 × 6 × 6 = 3,14 × 36 = 113,04 m². 37,68 es el perímetro (2πr) y 36 es solo r².","OA 11",G)
q("","¿Cuál de los siguientes puntos se ubica en el **cuadrante III** del plano cartesiano?",
 ["(−6, −1)","(6, −1)","(−6, 1)","(6, 1)"],"b","En el cuadrante III las dos coordenadas son negativas (izquierda y abajo del origen): (−6, −1). (6, −1) está en el IV, (−6, 1) en el II y (6, 1) en el I.","OA 14",G)
q("","El punto Q(2, −4) se mueve 5 unidades a la izquierda y 6 unidades hacia arriba. ¿Cuáles son sus nuevas coordenadas?",
 ["(−3, 2)","(7, 2)","(−3, −10)","(7, −10)"],"d","A la izquierda se resta a x: 2 − 5 = −3; hacia arriba se suma a y: −4 + 6 = 2. Cada movimiento cambia solo su coordenada.","OA 14",G)
q("## Eje 4: Datos y Probabilidades\n\n","La tabla muestra cómo llegan al colegio 50 estudiantes:\n\n| Medio de transporte | Frecuencia absoluta |\n|---|---|\n| Bus | 15 |\n| Auto | 10 |\n| Caminando | 20 |\n| Bicicleta | 5 |\n\n¿Cuál es la frecuencia relativa porcentual de quienes llegan en bus?",
 ["30 %","15 %","25 %","3 %"],"a","15 ÷ 50 = 0,3 = 30 %. La frecuencia relativa divide la frecuencia absoluta por el total de datos; 15 % confunde la frecuencia absoluta con el porcentaje.","OA 16",D)
q("","Un club quiere mostrar qué parte de su presupuesto total se destina a cada actividad. ¿Qué gráfico es más apropiado?",
 ["Un gráfico circular","Un gráfico de línea","Un gráfico de puntos sobre una recta numérica","Una tabla de valores sin gráfico"],"b","El gráfico circular muestra cómo se reparte un total entre sus partes. El de línea sirve para mostrar cambios a lo largo del tiempo.","OA 16",D)
q("","De 25 estudiantes de un curso, 5 practican natación. ¿Cuál es la frecuencia relativa porcentual de quienes practican natación?",
 ["20 %","5 %","25 %","0,5 %"],"c","5 ÷ 25 = 0,2 = 20 %. 5 % confunde la frecuencia absoluta con la relativa.","OA 16",D)
q("","Una caja tiene 10 fichas iguales: 4 rojas, 5 azules y 1 verde. Si se saca una al azar, ¿cuál es la probabilidad de sacar una ficha azul?",
 ["1/2","1/5","4/10","5/6"],"d","Casos favorables: 5 fichas azules; casos posibles: 10 fichas. P = 5/10 = 1/2. 4/10 es la probabilidad de sacar una roja.","OA 18",D)
q("","Un dado se lanzó 150 veces y salió el número 6 en 27 lanzamientos. ¿Cuál es la frecuencia relativa porcentual de obtener un 6 en ese experimento?",
 ["18 %","27 %","Cerca de 17 %","6 %"],"a","27 ÷ 150 = 0,18 = 18 %. «Cerca de 17 %» es la probabilidad teórica (1/6); en un experimento real la frecuencia relativa se acerca a ese valor, pero no tiene por qué ser igual.","OA 18",D)
armar(C/'matematica-examen-forma-b.md', C/'matematica-examen-forma-a.md', Q,
  fila=lambda i,p,cl: f"| {i} | **{cl}.** {p.explicacion} | {p.oa} | {p.extra['eje']} |",
  reemplazos={"(Forma B)":"(Forma A)","— Forma B":"— Forma A","relación con otras formas: segunda versión (Forma B), con preguntas propias":"relación con otras formas: Forma A, con preguntas propias distintas de la Forma B","última actualización: 2026-08-10":"última actualización: 2026-11-16"},
  inicio_preguntas="## Eje 1")
if __name__=="__main__":
    from collections import Counter; print(Counter(p.letra for p in Q), len(Q))
