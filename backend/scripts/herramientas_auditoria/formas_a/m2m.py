import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from forma_a import P, armar  # noqa: E402
C=Path(__file__).resolve().parents[4]/'contenido'/'02-medio/examenes'
H="**Pregunta {n} (alternativas).** "
Q=[]
def q(sec,en,ops,l,ex,oa,eje): Q.append(P(sec,H,en,ops,l,ex,oa,{"eje":eje}))
N="Números y Operaciones"; A="Álgebra y Funciones"; G="Geometría"; E="Probabilidad y Estadística"
q("## Eje 1: Números y Operaciones\n\n","Simplifica √72.",["*6√2","2√6","36√2","3√8"],"a","72 = 36 × 2 y 36 es cuadrado perfecto: √72 = √36 × √2 = 6√2. 3√8 todavía se puede simplificar.","OA 1",N)
q("","Racionaliza la expresión 10/√5.",["*2√5","10√5","√5/2","5√2"],"c","Se amplifica por √5: 10√5 / 5 = 2√5. 10√5 olvida dividir por 5.","OA 1",N)
q("","Usando propiedades de los logaritmos, ¿cuánto vale log₃(27) + log₃(9)?",["*5","6","36","1"],"d","log₃(27) = 3 y log₃(9) = 2; la suma de logaritmos de igual base es log₃(27 · 9) = log₃(243) = 5. 6 multiplica los resultados en vez de sumarlos.","OA 1",N)
q("","Un terreno cuadrado tiene un área de 200 m². ¿Cuánto mide su lado?",["*10√2 m, aproximadamente 14,1 m","100 m, porque es la mitad del área","20√10 m, aproximadamente 63,2 m","50 m, porque es un cuarto del área"],"b","El lado es √200 = √(100 × 2) = 10√2 ≈ 14,1 m. 100 m y 50 m dividen el área en vez de sacar la raíz.","OA 1",N)
q("","¿Cuál es el valor de log₅(125)?",["*3","25","5","1/3"],"a","log₅(125) = 3 porque 5³ = 125. 25 divide 125 por 5.","OA 2",N)
q("","Expresa ∛(5⁴) como una potencia de exponente racional.",["*5^(4/3)","5^(3/4)","5^12","5^(1/12)"],"c","La raíz de índice n se escribe como exponente 1/n: ∛(5⁴) = 5^(4/3). 5^(3/4) invierte el índice y el exponente.","OA 2",N)
q("","¿Cuál es la forma de raíz de 16^(3/4) y su valor exacto?",["*(⁴√16)³ = 8","(∛16)⁴ = 12","⁴√16 · 3 = 6","(⁴√16)³ = 12"],"d","El denominador 4 es el índice de la raíz y el numerador 3 es el exponente: (⁴√16)³ = 2³ = 8.","OA 2",N)
q("","El nivel de un sonido en decibeles es L = 10 · log(I / I₀). Si un sonido tiene una intensidad I = 10⁶ · I₀, ¿cuál es su nivel?",["*60 dB","6 dB","600 dB","10⁶ dB"],"b","L = 10 · log(10⁶) = 10 · 6 = 60 dB. 6 dB olvida multiplicar por 10.","OA 2",N)
q("## Eje 2: Álgebra y Funciones\n\n","Para f(x) = x² − 6x + 2, ¿cuál es la coordenada x del vértice?",["*x = 3","x = −3","x = 6","x = 2"],"c","x = −b/(2a) = −(−6)/(2 · 1) = 3. x = −3 olvida el signo negativo de b.","OA 3",A)
q("","Para f(x) = −3x² + 6x + 1, ¿cuál es su concavidad y qué tipo de punto extremo tiene?",["*Hacia abajo, con un máximo","Hacia arriba, con un mínimo","Hacia abajo, con un mínimo","Hacia arriba, con un máximo"],"a","Como a = −3 < 0, la parábola se abre hacia abajo y su vértice es un máximo.","OA 3",A)
q("","Para f(x) = x² − 2x − 8, ¿cuáles son el vértice y las intersecciones con el eje x?",["*Vértice (1, −9); corta el eje x en x = 4 y x = −2","Vértice (1, −9); corta el eje x en x = −4 y x = 2","Vértice (1, −8); corta el eje x en x = 4 y x = −2","Vértice (2, −8); corta el eje x en x = 2 y x = −4"],"d","x del vértice = 2/2 = 1 y f(1) = 1 − 2 − 8 = −9. Factorizando, (x − 4)(x + 2) = 0: x = 4 y x = −2.","OA 3",A)
q("","La ganancia semanal de un taller (en miles de pesos) es G(x) = −x² + 40x − 300, donde x es la cantidad de mochilas vendidas. ¿Cuántas mochilas maximizan la ganancia y cuál es esa ganancia?",["*20 mochilas; ganancia máxima de $100 mil","40 mochilas; ganancia máxima de $300 mil","20 mochilas; ganancia máxima de $400 mil","10 mochilas; ganancia máxima de $0 mil"],"b","El máximo está en el vértice: x = −40/(2 · (−1)) = 20 y G(20) = −400 + 800 − 300 = 100 mil pesos.","OA 3",A)
q("","¿Pertenece el punto (2, 1) a la región de soluciones de y < x² − 3x + 4?",["*Sí, porque 1 < 2","No, porque 1 > 2","Sí, porque 2 < 1","No, porque está sobre la parábola"],"a","Con x = 2, x² − 3x + 4 = 4 − 6 + 4 = 2. Como 1 < 2, el punto cumple la desigualdad y pertenece a la región.","OA 3",A)
q("","¿Cuál es la inversa de f(x) = x − 8?",["*f⁻¹(x) = x + 8","f⁻¹(x) = 8 − x","f⁻¹(x) = x/8","f⁻¹(x) = −x − 8"],"d","Si y = x − 8, despejando x = y + 8; al intercambiar variables, f⁻¹(x) = x + 8: deshace la resta de 8.","OA 5",A)
q("","Determina la inversa de f(x) = (x + 1)/3.",["*f⁻¹(x) = 3x − 1","f⁻¹(x) = 3x + 1","f⁻¹(x) = (x − 1)/3","f⁻¹(x) = 3(x + 1)"],"b","Se despeja: y = (x + 1)/3 → 3y = x + 1 → x = 3y − 1. Al intercambiar variables, f⁻¹(x) = 3x − 1.","OA 5",A)
q("","¿Cuál es la inversa de f(x) = 2x + 6?",["*f⁻¹(x) = (x − 6)/2","f⁻¹(x) = (x + 6)/2","f⁻¹(x) = 2x − 6","f⁻¹(x) = x/2 + 6"],"c","Se despeja: y = 2x + 6 → x = (y − 6)/2. Primero se deshace la suma de 6 y luego la multiplicación por 2.","OA 5",A)
q("","¿Cuál es la inversa de f(x) = x² − 7, considerando x ≥ 0?",["*f⁻¹(x) = √(x + 7), con x ≥ −7","f⁻¹(x) = √x + 7, con x ≥ 0","f⁻¹(x) = (x + 7)², con x ≥ −7","f⁻¹(x) = √(x − 7), con x ≥ 7"],"a","y = x² − 7 → x² = y + 7 → x = √(y + 7). La raíz exige y + 7 ≥ 0, por eso el dominio de la inversa es x ≥ −7.","OA 5",A)
q("## Eje 3: Geometría\n\n","En un triángulo rectángulo, el cateto adyacente a un ángulo θ mide 12 cm y la hipotenusa mide 13 cm. ¿Cuál es cos θ, aproximadamente?",["*12/13 ≈ 0,92","5/13 ≈ 0,38","13/12 ≈ 1,08","12/5 = 2,4"],"d","El coseno es cateto adyacente sobre hipotenusa: cos θ = 12/13 ≈ 0,92. 13/12 es mayor que 1, imposible para un coseno.","OA 8",G)
q("","Un triángulo rectángulo tiene un ángulo de 60° y su cateto adyacente mide 5 cm. ¿Cuánto mide, aproximadamente, el cateto opuesto?",["*8,66 cm","2,89 cm","10 cm","4,33 cm"],"c","tan 60° = opuesto/adyacente, así que opuesto = 5 · tan 60° ≈ 5 · 1,732 ≈ 8,66 cm. 2,89 cm usa tan 30°.","OA 8",G)
q("","En un triángulo rectángulo, la hipotenusa mide 20 cm y un ángulo agudo mide 35°. ¿Cuánto mide el cateto adyacente a ese ángulo?",["*Aproximadamente 16,4 cm","Aproximadamente 11,5 cm","Aproximadamente 24,4 cm","Aproximadamente 14,0 cm"],"b","cos 35° = adyacente/hipotenusa, así que adyacente = 20 · cos 35° ≈ 20 · 0,819 ≈ 16,4 cm. 11,5 cm usa el seno, que corresponde al cateto opuesto.","OA 8",G)
q("","Una rampa de 10 m de largo forma un ángulo de 8° con el suelo. ¿A qué altura llega su extremo superior?",["*Aproximadamente 1,39 m","Aproximadamente 9,90 m","Aproximadamente 71,9 m","Aproximadamente 0,8 m"],"d","La rampa es la hipotenusa y la altura es el cateto opuesto: altura = 10 · sen 8° ≈ 10 · 0,139 ≈ 1,39 m. 9,90 m usa el coseno.","OA 8",G)
q("## Eje 4: Probabilidad y Estadística\n\n","Un menú permite elegir 1 de 3 entradas, 1 de 5 platos de fondo y 1 de 2 postres. ¿Cuántos menús distintos se pueden armar?",["*30","10","15","60"],"a","Principio multiplicativo: 3 × 5 × 2 = 30 menús. 10 suma las opciones en vez de multiplicarlas.","OA 11",E)
q("","Calcula 7!/5!.",["*42","2","7/5","35"],"c","7!/5! = 7 × 6 × 5!/5! = 7 × 6 = 42. 2 resulta de restar 7 − 5.","OA 11",E)
q("","¿De cuántas formas distintas pueden sentarse 6 amigos en una fila de 6 butacas del cine?",["*720","36","21","6"],"b","Es una permutación de 6 elementos: 6! = 6 × 5 × 4 × 3 × 2 × 1 = 720. 36 es 6 × 6.","OA 11",E)
q("","Un club debe elegir a 3 de sus 8 socios para formar una comisión, donde todos tienen el mismo rol (el orden no importa). ¿De cuántas formas puede hacerlo?",["*56","336","24","11"],"d","Como el orden no importa, es una combinación: C(8, 3) = 8 × 7 × 6 / (3 × 2 × 1) = 56. 336 cuenta los ordenamientos.","OA 11",E)
armar(C/'matematica-examen-forma-b.md', C/'matematica-examen-forma-a.md', Q,
  fila=lambda i,p,cl: f"| {i} | **{cl}.** {p.explicacion} | {p.oa} | {p.extra['eje']} |",
  reemplazos={"(Forma B)":"(Forma A)","— Forma B":"— Forma A","versión: Forma B (preguntas propias)":"versión: Forma A (preguntas propias, distintas de la Forma B)","última actualización: 2026-08-10":"última actualización: 2026-11-17","Ninguna pregunta de esta Forma B repite":"Ninguna pregunta de esta Forma A repite"},
  inicio_preguntas="## Eje 1")
if __name__=="__main__":
    from collections import Counter; print(Counter(p.letra for p in Q), len(Q))
