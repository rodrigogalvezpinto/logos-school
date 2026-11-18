import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from forma_a import P, armar  # noqa: E402
C=Path(__file__).resolve().parents[4]/'contenido'/'04-medio/examenes'
H="**Pregunta {n} (alternativas).** "
Q=[]
def q(sec,en,ops,l,ex,oa,eje): Q.append(P(sec,H,en,ops,l,ex,oa,{"eje":eje}))
A="Álgebra y Funciones"; E="Probabilidad y Estadística"
q("## Eje 1: Álgebra y Funciones — Matemática financiera (OA1)\n\n","¿Qué caracteriza al interés compuesto?",
 ["Los intereses se calculan siempre solo sobre el capital inicial","*Los intereses se suman al capital y generan nuevos intereses","Los intereses son iguales en todos los períodos del depósito","Los intereses se pagan solo al final, sin ninguna capitalización"],"b","En el interés compuesto, los intereses de cada período se suman al capital y, en el siguiente, también generan intereses: el monto crece de forma exponencial.","OA 1",A)
q("","Dos créditos tienen la misma tasa nominal anual: uno capitaliza diariamente y el otro una vez al año. Para la persona que pide el crédito, ¿cuál resulta más caro?",
 ["El que capitaliza una vez al año, porque cobra todos los intereses juntos","Los dos cuestan lo mismo, porque tienen la misma tasa nominal anual","*El que capitaliza diariamente, porque su tasa efectiva anual es mayor","Ninguno, porque la capitalización no afecta el costo de un crédito"],"c","Mientras más veces se capitaliza en el año, mayor es la tasa efectiva anual: el crédito que capitaliza diariamente cobra más intereses en total.","OA 1",A)
q("","¿Qué es la Unidad de Fomento (UF)?",
 ["*Una unidad de cuenta que se reajusta según la inflación, para mantener el valor real","Una moneda de papel que se usa en lugar del peso chileno en las tiendas","Un impuesto que se cobra cada mes a quienes tienen una cuenta bancaria","Un tipo de crédito que entregan los bancos sin cobrar ningún interés"],"a","La UF es una unidad de cuenta que se reajusta según la variación del IPC: se usa en créditos, arriendos y seguros para mantener su valor real frente a la inflación.","OA 1",A)
q("","¿Qué es la inflación?",
 ["La disminución de la cantidad de dinero que imprime el Banco Central","El aumento del sueldo mínimo que se fija cada año por ley","El precio de un producto en particular en un supermercado","*El aumento sostenido y generalizado de los precios en una economía"],"d","La inflación es el alza sostenida y generalizada de los precios; en Chile se mide con la variación del IPC.","OA 1",A)
q("","Un capital de $1.200.000 se invierte a interés compuesto del 3 % anual durante 4 años. ¿Cuál es, aproximadamente, el monto final?",
 ["$1.344.000","*$1.350.611","$1.236.000","$1.380.000"],"b","M = 1.200.000 · (1,03)⁴ ≈ 1.200.000 · 1,1255 ≈ $1.350.611. $1.344.000 corresponde a interés simple (3 % de 1.200.000 cuatro veces).","OA 1",A)
q("","Un crédito tiene una tasa nominal anual del 12 %, capitalizada mensualmente (n = 12). ¿Cuál es, aproximadamente, la tasa efectiva anual (TEA)?",
 ["*12,68 %","12 %","1 %","144 %"],"a","TEA = (1 + 0,12/12)¹² − 1 = (1,01)¹² − 1 ≈ 0,1268 = 12,68 %. Es mayor que la tasa nominal porque los intereses se capitalizan cada mes.","OA 1",A)
q("","Una persona compara dos créditos de igual monto y plazo: el Crédito R anuncia una tasa mensual de 1,5 % y tiene un CAE de 22 %; el Crédito S anuncia una tasa mensual de 1,2 % y tiene un CAE de 25 %. ¿Cuál conviene?",
 ["El Crédito S, porque su tasa mensual anunciada es más baja","Los dos convienen igual, porque tienen el mismo monto","*El Crédito R, porque su CAE, que incluye todos los costos, es menor","El Crédito S, porque su CAE más alto indica mejor servicio"],"c","El CAE (carga anual equivalente) incluye intereses, comisiones y seguros: es el indicador para comparar créditos. R tiene menor CAE (22 % contra 25 %), aunque su tasa anunciada sea mayor.","OA 1",A)
q("","Hace un año, el sueldo mensual de una persona era $500.000; hoy es $530.000. En ese período, el IPC acumulado fue de 4 %. ¿Qué ocurrió con su poder adquisitivo real?",
 ["Disminuyó, porque cualquier inflación reduce el poder adquisitivo","Se mantuvo igual, porque el sueldo subió en pesos","Disminuyó, porque el sueldo subió menos que los precios","*Aumentó, porque el sueldo subió 6 % y los precios solo 4 %"],"d","El sueldo subió 30.000/500.000 = 6 %, más que la inflación (4 %): el poder adquisitivo real aumentó, cerca de un 1,9 %.","OA 1",A)
q("## Eje 1: Álgebra y Funciones — Modelos de crecimiento, decrecimiento y periódicos (OA3)\n\n","¿Cuál de las siguientes es una función potencia con exponente entero negativo?",
 ["*f(x) = 3x⁻²","f(x) = 3ˣ","f(x) = 3x + 2","f(x) = sen(3x)"],"a","Una función potencia tiene la forma f(x) = k · xⁿ; con n = −2 el exponente es entero y negativo. 3ˣ es exponencial, porque la variable está en el exponente.","OA 3",A)
q("","En el modelo f(x) = A · sen(Bx) + D, ¿qué representa el parámetro A?",
 ["El valor medio, alrededor del cual oscila la función hacia arriba y hacia abajo","*La amplitud: cuánto se aleja la función de su valor medio","El período completo de la oscilación, medido en grados o en radianes","El desplazamiento horizontal de la curva hacia la derecha o la izquierda"],"b","A es la amplitud: la distancia entre el valor medio y el máximo (o el mínimo). D es el valor medio y B determina el período.","OA 3",A)
q("","¿Qué ocurre con el período de f(x) = sen(2x) en comparación con el de g(x) = sen(x)?",
 ["Se duplica: pasa de 360° a 720°","Se mantiene igual: sigue siendo 360°","*Se reduce a la mitad: pasa de 360° a 180°","Desaparece: la función deja de ser periódica"],"c","El período de sen(Bx) es 360°/B; con B = 2 el período es 180°: la función completa su ciclo en la mitad del tiempo.","OA 3",A)
q("","El área de un cuadrado se modela como A(l) = l². Si el lado se triplica, ¿qué ocurre con el área?",
 ["Se triplica","Se multiplica por 6","Se mantiene igual","*Se multiplica por 9"],"d","En una función potencia de exponente 2, al multiplicar l por 3 el área se multiplica por 3² = 9.","OA 3",A)
q("","Si f(x) = 2x³, ¿cuánto vale f(4) y en qué factor aumenta el resultado al duplicar x (de 2 a 4)?",
 ["*f(4) = 128; aumenta en un factor de 8","f(4) = 24; aumenta en un factor de 2","f(4) = 128; aumenta en un factor de 2","f(4) = 512; aumenta en un factor de 6"],"a","f(4) = 2 · 4³ = 2 · 64 = 128 y f(2) = 2 · 8 = 16; 128/16 = 8 = 2³: al duplicar x, el resultado se multiplica por 8.","OA 3",A)
q("","La intensidad de la luz de una ampolleta a una distancia d (metros) se modela como I(d) = 900/d². ¿Qué ocurre al pasar de 3 a 6 metros?",
 ["Pasa de 100 a 50: se reduce a la mitad","*Pasa de 100 a 25: se reduce a la cuarta parte","Pasa de 300 a 150: se reduce a la mitad","Pasa de 100 a 200: se duplica"],"b","I(3) = 900/9 = 100 e I(6) = 900/36 = 25: al duplicar la distancia, la intensidad se reduce a la cuarta parte (se divide por 2² = 4).","OA 3",A)
q("","Los visitantes mensuales de un parque se modelan como V(m) = 2.000 · cos((π/6)(m − 1)) + 5.000, con m el número del mes. ¿Cuáles son la cantidad máxima, la mínima y el período?",
 ["Máxima 2.000, mínima −2.000 y período de 6 meses","Máxima 5.000, mínima 2.000 y período de 1 mes","*Máxima 7.000, mínima 3.000 y período de 12 meses","Máxima 7.000, mínima 5.000 y período de 24 meses"],"c","El valor medio es 5.000 y la amplitud 2.000: máxima 7.000 y mínima 3.000. El período es 2π / (π/6) = 12 meses.","OA 3",A)
q("","Una analista debe modelar (1) las horas de luz solar de cada día a lo largo de varios años y (2) el área de un terreno cuadrado según la medida de su lado. ¿Qué modelos son adecuados?",
 ["(1) potencia y (2) periódico, porque ambos crecen sin límite","(1) lineal y (2) exponencial, porque cambian con el tiempo","(1) exponencial y (2) lineal, porque ambos tienen valor inicial","*(1) periódico, porque se repite cada año, y (2) potencia, porque A = l²"],"d","Las horas de luz suben y bajan cada año: modelo periódico. El área de un cuadrado es A = l²: modelo potencia.","OA 3",A)
q("## Eje 2: Probabilidad y Estadística — Modelos binomial y normal (OA2)\n\n","¿Cuál de las siguientes situaciones se modela mejor con una distribución **binomial**?",
 ["*El número de caras al lanzar 10 veces una moneda","La estatura de los estudiantes de un liceo","El tiempo que demora un bus en llegar al paradero","La temperatura máxima de cada día del año"],"a","La binomial cuenta éxitos en un número fijo de ensayos independientes con dos resultados posibles: las caras en 10 lanzamientos de una moneda.","OA 2",E)
q("","Según la regla empírica de la distribución normal, ¿qué porcentaje aproximado de los datos se encuentra dentro de 1 desviación estándar de la media (μ ± σ)?",
 ["50 %","*68 %","95 %","99,7 %"],"b","En una distribución normal, cerca del 68 % de los datos está a menos de una desviación estándar de la media; el 95 %, a menos de dos; y el 99,7 %, a menos de tres.","OA 2",E)
q("","En un modelo binomial con n = 50 y p = 0,2, ¿cuál es el valor esperado (media) del número de éxitos?",
 ["*10","2,5","50","8"],"c","El valor esperado de una binomial es n · p = 50 · 0,2 = 10 éxitos.","OA 2",E)
q("","Una encuesta realizada solo a socios de un gimnasio concluye que «el 80 % de los chilenos hace ejercicio cada semana». ¿Cuál es el principal problema de esta conclusión?",
 ["Que la encuesta debió hacerse por teléfono y no en persona, para que fuera más rápida","Que el 80 % es un número demasiado alto para aparecer en una encuesta seria del país","Que los gimnasios no tienen permiso legal para hacer encuestas a las personas que entrenan","*Que la muestra no es representativa: los socios de un gimnasio hacen más ejercicio que el promedio"],"d","La muestra tiene un sesgo de selección: quienes van a un gimnasio hacen más ejercicio que la población general, así que no se puede generalizar a todos los chilenos.","OA 2",E)
q("","Un estudiante responde al azar 5 preguntas de verdadero o falso (p = 0,5). ¿Cuál es la probabilidad de que acierte exactamente 3?",
 ["*10/32 = 31,25 %","3/5 = 60 %","1/32 ≈ 3,1 %","5/32 ≈ 15,6 %"],"a","C(5, 3) = 10 formas de acertar 3; cada una tiene probabilidad (0,5)⁵ = 1/32. P(X = 3) = 10/32 = 31,25 %.","OA 2",E)
q("","La probabilidad de que un envío llegue dañado es 0,05. Se despachan 400 envíos. ¿Cuáles son el número esperado de envíos dañados y la desviación estándar?",
 ["μ = 20 y σ = 19","*μ = 20 y σ ≈ 4,36","μ = 5 y σ ≈ 2,24","μ = 380 y σ ≈ 4,36"],"b","μ = n · p = 400 · 0,05 = 20; σ² = n · p · (1 − p) = 400 · 0,05 · 0,95 = 19; σ = √19 ≈ 4,36. μ = 20 y σ = 19 confunde la varianza con la desviación.","OA 2",E)
q("","La estatura de los jóvenes de una ciudad se distribuye normalmente con μ = 170 cm y σ = 6 cm. ¿Entre qué valores se encuentra, aproximadamente, la estatura del 95 % de ellos?",
 ["Entre 164 y 176 cm","Entre 152 y 188 cm","*Entre 158 y 182 cm","Entre 165 y 175 cm"],"c","El 95 % está en μ ± 2σ: 170 − 12 = 158 y 170 + 12 = 182 cm. Entre 164 y 176 cm corresponde a μ ± σ (68 %).","OA 2",E)
q("","En verano aumentan tanto las ventas de helados como los casos de quemaduras de sol, y ambas variables tienen una fuerte correlación. ¿Qué conclusión es correcta?",
 ["Comer helados causa quemaduras de sol, porque la correlación entre ambas variables es fuerte","Las quemaduras de sol hacen que la gente compre más helados para aliviar el dolor de la piel","Si se prohíben los helados en verano, desaparecen las quemaduras de sol en las playas","*No se puede concluir causalidad: ambas aumentan por una tercera variable, el calor del verano"],"d","Una correlación no prueba causalidad: helados y quemaduras aumentan juntos por una variable común, el calor y la mayor exposición al sol en verano.","OA 2",E)
q("","Una tienda en línea recibe el 70 % de sus productos del proveedor A, con un 2 % de devoluciones, y el 30 % del proveedor B, con un 10 % de devoluciones. ¿Qué regla se usa y cuál es la probabilidad de que un producto al azar sea devuelto?",
 ["Regla de la suma simple: 2 % + 10 % = 12 %","Promedio de las tasas: (2 % + 10 %) ÷ 2 = 6 %","Regla del producto: 2 % · 10 % = 0,2 %","*Probabilidad total: 0,70 · 0,02 + 0,30 · 0,10 = 4,4 %"],"d","Se pondera cada tasa por la proporción de productos de cada proveedor (probabilidad total): 0,014 + 0,030 = 0,044 = 4,4 %.","OA 2",E)
armar(C/'matematica-examen-forma-b.md', C/'matematica-examen-forma-a.md', Q,
  fila=lambda i,p,cl: f"| {i} | **{cl}.** {p.explicacion} | {p.oa} | {p.extra['eje']} |",
  reemplazos={"— Forma B":"— Forma A","última actualización: 2026-08-11":"última actualización: 2026-11-17"},
  inicio_preguntas="## Eje 1")
if __name__=="__main__":
    from collections import Counter; print(Counter(p.letra for p in Q), len(Q))
