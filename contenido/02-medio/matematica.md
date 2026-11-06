---
título: Matemática — 2° Medio
asignatura: Matemática
curso: 2° Medio
tipo: Guía de estudio
basado_en: Bases Curriculares, Decreto 614/2013 (Mineduc/UCE) — temario oficial del Examen Libre de Validación de Estudios
oa_evaluados: OA 1, OA 2, OA 3, OA 5, OA 8, OA 11
ultima_actualizacion: 2026-10-28
---

# Matemática — 2° Medio

> Este apunte se basa fielmente en el temario oficial del Mineduc/UCE para el Examen Libre de Validación de Estudios de 2° medio, bajo el **Decreto de Bases Curriculares N°614, del año 2013**. Cubre los **6 Objetivos de Aprendizaje (OA)** de Matemática seleccionados para este nivel, organizados en los ejes **Números y Operaciones**, **Álgebra y Funciones**, **Geometría**, y **Probabilidad y Estadística**. 2° medio es el último curso que rinde el examen bajo este régimen curricular: desde 3° medio, el temario cambia al Decreto N°193/2019.

## Antes de empezar

**Sobre el formato del examen:** cada asignatura se rinde en una prueba **separada e independiente**, de **25 preguntas** y **90 minutos** de duración (máximo 2 pruebas por día). En la prueba de Matemática **se permite el uso de calculadora**. Úsala con criterio: para calcular raíces, logaritmos o razones trigonométricas que no son "redondos", pero sigues siendo tú quien decide qué operación aplicar, cómo plantear el problema, y si el resultado tiene sentido.

Este año tu manejo de los números se extiende de los racionales a los **números reales**: vas a operar con **raíces** y a conocer los **logaritmos**, una herramienta que "deshace" a las potencias y que aparece en fenómenos tan distintos como la escala de Richter para medir sismos o el pH de una solución. En álgebra, das el salto de las funciones lineales a las **funciones cuadráticas** (las que producen parábolas), y aprendes qué significa "deshacer" una función mediante su **función inversa**. En geometría, incorporas las **razones trigonométricas** —seno, coseno y tangente— que te permiten calcular alturas y distancias inaccesibles a partir de ángulos. Y en probabilidades, das un paso más allá de contar casos "a mano": usas el **principio multiplicativo**, el **factorial** y las **permutaciones** para contar de forma sistemática situaciones con muchas posibilidades, como claves, sorteos y ordenamientos.

Vas a trabajar con cuatro grandes ejes:

1. **Números y Operaciones** — operatoria y propiedades de raíces; y relaciones entre potencias de exponente racional, raíces enésimas y logaritmos.
2. **Álgebra y Funciones** — la función cuadrática f(x)=ax²+bx+c (gráfico, vértice, concavidad, modelamiento); y el concepto de función inversa, para funciones lineales y cuadráticas.
3. **Geometría** — las razones trigonométricas seno, coseno y tangente en triángulos rectángulos.
4. **Probabilidad y Estadística** — permutaciones y combinatoria sencilla (principio multiplicativo, factorial) aplicadas al cálculo de probabilidades.

En todo momento vas a practicar cuatro habilidades importantes de un matemático: **resolver problemas**, **argumentar y comunicar** tus ideas, **modelar** situaciones reales con números y símbolos, y **representar** la información de distintas formas. ¡Empecemos!

---

## Eje 1: Números y Operaciones

### OA 1 — Operar con raíces y aplicar propiedades de los logaritmos

Vas a realizar **cálculos y estimaciones con números reales**: aplicando las propiedades de multiplicación y división de raíces para simplificar expresiones, descomponiendo raíces en factores para reducirlas a su forma más simple, transformando raíces en potencias (y viceversa), combinando raíces con números racionales en expresiones mixtas, y resolviendo problemas —incluso no rutinarios— que involucren las propiedades de los **logaritmos**.

**¿Por qué importa?** Hasta ahora, todos los números con los que has trabajado se podían escribir como fracciones (números racionales). Pero números como √2 o √5 no se pueden expresar como fracción: son **números irracionales**, y junto con los racionales forman el conjunto de los **números reales**. Saber simplificar y operar con raíces es indispensable para trabajar con áreas, volúmenes, y —como verás en el eje de Geometría— con triángulos rectángulos. Los logaritmos, por su parte, son la operación que "deshace" una potencia, y aparecen en escalas que usamos para medir fenómenos que varían enormemente en magnitud, como la intensidad de un sismo o la acidez de una sustancia.

**Propiedades de las raíces** (para a, b ≥ 0):

| Propiedad | Regla en Notación Matemática |
|---|---|
| Raíz de un producto | \( \sqrt[n]{a \cdot b} = \sqrt[n]{a} \cdot \sqrt[n]{b} \) |
| Raíz de un cuociente | \( \sqrt[n]{\frac{a}{b}} = \frac{\sqrt[n]{a}}{\sqrt[n]{b}} \) |
| Raíz de una potencia | \( \sqrt[n]{a^m} = (\sqrt[n]{a})^m = a^{m/n} \) |

**Racionalizar** un denominador significa transformar una fracción con raíz en el denominador en una expresión equivalente sin raíces abajo, multiplicando numerador y denominador por la misma raíz.

**Logaritmo:** el logaritmo en base a de un número b (con a>0, a≠1) es el exponente c al que hay que elevar a para obtener b: **\( \log_a(b) = c \iff a^c = b \)**. Sus propiedades básicas son: \( \log(a \cdot b) = \log(a) + \log(b) \), y \( \log(\frac{a}{b}) = \log(a) - \log(b) \).

#### Ejemplos resueltos

**Ejemplo 1 — Reducir términos semejantes con raíces**

Calcula: \( \sqrt{48} + \sqrt{27} \).

Primero se simplifica cada raíz por separado, buscando el mayor factor cuadrado perfecto: \( \sqrt{48} = \sqrt{16 \cdot 3} = 4\sqrt{3} \); y \( \sqrt{27} = \sqrt{9 \cdot 3} = 3\sqrt{3} \). Como ambas quedaron con la misma raíz (\( \sqrt{3} \)), son "semejantes" y se pueden sumar: \( 4\sqrt{3} + 3\sqrt{3} = \mathbf{7\sqrt{3}} \).

**Ejemplo 2 — Racionalizar un denominador**

Racionaliza: \( \frac{7}{\sqrt{5}} \).

Se multiplica numerador y denominador por \( \sqrt{5} \), para que el denominador deje de tener una raíz:

$$ \frac{7}{\sqrt{5}} = \frac{7 \cdot \sqrt{5}}{\sqrt{5} \cdot \sqrt{5}} = \frac{7\sqrt{5}}{5} $$

El resultado, **\( \frac{7\sqrt{5}}{5} \)**, es equivalente al original pero sin raíz en el denominador.

**Ejemplo 3 — Aplicar propiedades de logaritmos**

Calcula, usando propiedades: \( \log_3(9) + \log_3(27) \).

Se aplica la propiedad de la suma de logaritmos: \( \log_3(9) + \log_3(27) = \log_3(9 \cdot 27) = \log_3(243) \). Como \( 3^5 = 243 \), el resultado es **5**. (Se puede verificar por separado: \( \log_3(9) = 2 \) porque \( 3^2 = 9 \), y \( \log_3(27) = 3 \) porque \( 3^3 = 27 \); y 2+3=5, coincide).

#### Preguntas de autoevaluación

**Pregunta 1 (alternativas).** Simplifica √200.
a) 2√100
b) 20√5
c) 10√2
d) 100√2

**Respuesta correcta: c) 10√2.**
*Retroalimentación:* 200 = 100×2, y 100 es un cuadrado perfecto (10²), por lo tanto √200 = √100×√2 = 10√2.

**Pregunta 2 (verdadero o falso).** √8 × √2 = √16 = 4.

**Respuesta correcta: Verdadero.**
*Retroalimentación:* al multiplicar raíces de igual índice, se multiplican las cantidades subradicales: √8×√2 = √16 = 4.

**Pregunta 3 (calcular — propiedad del cuociente).** Simplifica: √5 × √20.
a) √25
b) 25
c) 10
d) 100

**Respuesta correcta: c) 10.**
*Retroalimentación:* √5×√20 = √(5×20) = √100 = 10.

**Pregunta 4 (alternativas — racionalizar).** Racionaliza: 5/√2.
a) √10/2
b) 5/2
c) 5√2
d) 5√2/2

**Respuesta correcta: d) 5√2/2.**
*Retroalimentación:* se amplifica por √2: (5√2)/(√2·√2) = 5√2/2.

**Pregunta 5 (alternativas — reducir términos semejantes).** Reduce: √75 − √12.
a) √63
b) 7√3
c) 3
d) 3√3

**Respuesta correcta: d) 3√3.**
*Retroalimentación:* √75 = 5√3 y √12 = 2√3; solo se restan raíces semejantes: 5√3 − 2√3 = 3√3 (√63 resulta de restar los radicandos, un error frecuente).

**Pregunta 6 (alternativas — terreno cuadrado).** Un terreno cuadrado tiene un área de 245 m². ¿Cuánto mide su lado, como raíz simplificada y aproximadamente?
a) 5√7 m ≈ 13,23 m
b) 7√5 m ≈ 15,65 m
c) 49√5 m ≈ 109,6 m
d) √245 m ≈ 122,5 m

**Respuesta correcta: b) 7√5 m ≈ 15,65 m.**
*Retroalimentación:* 245 = 49 · 5, así que √245 = 7√5 ≈ 15,65 m.

**Pregunta 7 (alternativas — pH).** Si pH = −log[H⁺] y una muestra de agua tiene [H⁺] = 10⁻⁷, ¿cuál es su pH?
a) −7
b) 10⁷
c) 7
d) 0,7

**Respuesta correcta: c) 7.**
*Retroalimentación:* −log(10⁻⁷) = −(−7) = 7, el pH del agua neutra.

**Pregunta 8 (alternativas — transformar registro).** ¿Cómo se escribe 5^(3/4) como raíz?
a) √(5^(3·4))
b) ³√(5⁴) = ³√625
c) ⁴√(5³) = ⁴√125
d) 5 · ⁴√3

**Respuesta correcta: c) ⁴√(5³) = ⁴√125.**
*Retroalimentación:* el denominador del exponente es el índice de la raíz y el numerador, la potencia del radicando.

**Pregunta 9 (alternativas — propiedades de logaritmos).** Sin calculadora, ¿cuánto vale log₂(16) − log₂(4)?
a) 12
b) log₂(12)
c) 4
d) 2

**Respuesta correcta: d) 2.**
*Retroalimentación:* la resta de logaritmos de igual base es el logaritmo del cociente: log₂(16/4) = log₂(4) = 2.

**Pregunta 10 (alternativas — comparar).** Sin calcular el decimal, ¿cuál es mayor: √50 o 6?
a) 6, porque 50 es menor que 60
b) √50, porque 6² = 36 < 50
c) Son iguales
d) No se puede saber sin calculadora

**Respuesta correcta: b) √50, porque 6² = 36 < 50.**
*Retroalimentación:* basta comparar los cuadrados: √50 > √36 = 6.

---

### OA 2 — Comprender las relaciones entre potencias, raíces y logaritmos

Vas a mostrar que comprendes las **relaciones entre potencias de exponente racional, raíces enésimas y logaritmos**: comparando y ubicando estas representaciones en la recta numérica, convirtiendo libremente entre los tres registros (potencia, raíz y logaritmo), y resolviendo problemas —rutinarios y no rutinarios— que las involucren.

**¿Por qué importa?** Potencias, raíces y logaritmos son tres formas distintas de expresar la **misma relación** entre tres números. Si sabes que 2³=8, entonces también sabes que ∛8=2 y que log₂(8)=3: son la misma información, "leída" desde ángulos distintos. Comprender esta equivalencia te permite elegir la forma más conveniente para resolver un problema, y es la base de escalas logarítmicas que se usan en ciencia (como la escala de Richter) y en tecnología.

**El triángulo de equivalencias:**

| Si sabes que... | También es cierto que... |
|---|---|
| aᵐ/ⁿ = c | ⁿ√(aᵐ) = c |
| aᵏ = b | log_a(b) = k |

**Potencia de exponente racional:** a^(m/n) = ⁿ√(aᵐ). El denominador del exponente racional (n) es el índice de la raíz; el numerador (m) es la potencia de la cantidad subradical.

#### Ejemplos resueltos

**Ejemplo 1 — Ubicar una potencia de exponente racional en la recta numérica**

Ubica aproximadamente 2^(3/2) en la recta numérica, convirtiéndolo primero a raíz.

2^(3/2) = √(2³) = √8. Como √8 no es exacto, se estima: 2²=4 y 3²=9, y como 8 está entre 4 y 9, √8 está entre 2 y 3 (con calculadora, √8 ≈ **2,83**).

**Ejemplo 2 — Convertir entre potencia y logaritmo**

Escribe la igualdad 5³=125 en su forma logarítmica equivalente.

Si 5³=125, entonces, por definición de logaritmo, **log₅(125) = 3**: "el logaritmo en base 5 de 125 es 3", porque 5 elevado a 3 da 125.

**Ejemplo 3 — Aplicación: escala de Richter**

La magnitud M de un sismo, en un modelo simplificado, se puede estimar como M = log₁₀(A/A₀), donde A es la amplitud de las ondas registradas y A₀ una amplitud de referencia. Si en un sismo la razón A/A₀ = 10.000, ¿cuál es su magnitud aproximada?

M = log₁₀(10.000). Como 10⁴=10.000, entonces **M = 4**. Este tipo de escala logarítmica es clave en un país sísmico como Chile: explica por qué un sismo de magnitud 7 libera muchísima más energía que uno de magnitud 5, aunque la diferencia entre ambos números parezca pequeña.

#### Preguntas de autoevaluación

**Pregunta 1 (alternativas).** ¿Cuál es el valor de log₄(64)?
a) 2
b) 4
c) 16
d) 3

**Respuesta correcta: d) 3.**
*Retroalimentación:* log₄(64)=3 porque 4³=64.

**Pregunta 2 (verdadero o falso).** 9^(1/2) es igual a √9.

**Respuesta correcta: Verdadero.**
*Retroalimentación:* por definición, un exponente 1/2 equivale exactamente a la raíz cuadrada: a^(1/2) = √a.

**Pregunta 3 (calcular — convertir raíz a potencia).** Expresa ⁵√(7³) como una potencia de exponente racional.
a) 7^15
b) 7^(5/3)
c) 7^(3/5)
d) 7^8

**Respuesta correcta: c) 7^(3/5).**
*Retroalimentación:* el índice de la raíz (5) pasa al denominador del exponente, y la potencia de la cantidad subradical (3) pasa al numerador.

**Pregunta 4 (alternativas — potencia a raíz).** ¿Cuál es la forma de raíz de 10^(2/5)?
a) √(10⁵)
b) ²√(10⁵)
c) ⁵√(10²) = ⁵√100
d) 10 · ⁵√2

**Respuesta correcta: c) ⁵√(10²) = ⁵√100.**
*Retroalimentación:* índice 5 (denominador) y potencia 2 (numerador).

**Pregunta 5 (alternativas — recta numérica).** ¿Entre qué enteros consecutivos se ubica 2^(1/3)?
a) Entre 3 y 4
b) Entre 0 y 1
c) Entre 2 y 3
d) Entre 1 y 2

**Respuesta correcta: d) Entre 1 y 2.**
*Retroalimentación:* 2^(1/3) = ∛2 ≈ 1,26, porque 1³ = 1 < 2 < 8 = 2³.

**Pregunta 6 (alternativas — comparar).** ¿Cuál es mayor: 3^(1/2) o 3^(1/3)?
a) 3^(1/3), porque al dividir por 3 la raíz es más grande que al dividir por 2
b) Son iguales, porque ambas potencias tienen la misma base 3
c) Depende del signo de la base, que aquí no se puede conocer
d) 3^(1/2), porque con base mayor que 1 un exponente mayor da un resultado mayor

**Respuesta correcta: d) 3^(1/2), porque con base mayor que 1 un exponente mayor da un resultado mayor.**
*Retroalimentación:* verificación: 3^(1/2) ≈ 1,73 y 3^(1/3) ≈ 1,44.

**Pregunta 7 (alternativas — escala de Richter).** Con M = log₁₀(A/A₀), si A/A₀ = 1.000.000, ¿cuál es la magnitud?
a) 1.000.000
b) 6
c) 60
d) 10

**Respuesta correcta: b) 6.**
*Retroalimentación:* log₁₀(10⁶) = 6.

**Pregunta 8 (alternativas — convertir registro).** Si log₁₀(x) = 3, ¿cuánto vale x?
a) 30
b) 3
c) 1.000
d) 0,001

**Respuesta correcta: c) 1.000.**
*Retroalimentación:* por definición, 10³ = x.

**Pregunta 9 (alternativas — propiedades combinadas).** Si log₂(5) ≈ 2,32, ¿cuánto vale aproximadamente log₂(20)?
a) 46,4
b) 9,28
c) 4,32
d) 2,32

**Respuesta correcta: c) 4,32.**
*Retroalimentación:* log₂(20) = log₂(4 · 5) = log₂(4) + log₂(5) = 2 + 2,32.

**Pregunta 10 (alternativas — de potencia a logaritmo).** ¿Cuál es la forma logarítmica de 7² = 49?
a) log₂(49) = 7
b) log₄₉(7) = 2
c) log₇(2) = 49
d) log₇(49) = 2

**Respuesta correcta: d) log₇(49) = 2.**
*Retroalimentación:* la base de la potencia es la base del logaritmo y el exponente es el resultado.

---

## Eje 2: Álgebra y Funciones

### OA 3 — Comprender la función cuadrática

Vas a mostrar que comprendes la **función cuadrática f(x)=ax²+bx+c (con a≠0)**: reconociéndola en situaciones de la vida diaria y de otras asignaturas, representándola en tablas y gráficos, determinando sus puntos especiales (vértice, eje de simetría, intersecciones con los ejes, concavidad), usándola para modelar situaciones de cambio cuadrático —en particular, problemas de oferta y demanda—, y determinando regiones de soluciones de inecuaciones cuadráticas del tipo y<ax²+bx+c o y>ax²+bx+c.

**¿Por qué importa?** El año pasado trabajaste principalmente con funciones lineales, cuya gráfica es una recta. La función cuadrática introduce un nuevo tipo de curva, la **parábola**, que aparece en trayectorias de proyectiles, en el diseño de antenas y puentes, y en modelos económicos de ganancia, costo o demanda, donde el resultado óptimo (máximo o mínimo) suele encontrarse en el vértice de la parábola.

**Elementos de \( f(x) = ax^2 + bx + c \) (con \( a \neq 0 \)):**

| Elemento | Cómo se determina | Notación Matemática |
|---|---|---|
| Concavidad | Si \( a > 0 \), abre hacia arriba (mínimo); si \( a < 0 \), abre hacia abajo (máximo) | Signo de \( a \) |
| Vértice | Coordenada \( x = -\frac{b}{2a} \). Coordenada \( y = f(x_v) \) | \( V = \left(-\frac{b}{2a}, f\left(-\frac{b}{2a}\right)\right) \) |
| Eje de simetría | La recta vertical que pasa por el vértice | \( x = -\frac{b}{2a} \) |
| Intersección con eje y | Se evalúa en \( x = 0 \) | Punto \( (0, c) \) |
| Intersecciones con eje x (raíces) | Valores donde \( f(x) = 0 \) con fórmula cuadrática general | \( x = \frac{-b \pm \sqrt{b^2 - 4ac}}{2a} \) |

#### Ejemplos resueltos

**Ejemplo 1 — Determinar los elementos de una parábola**

Analiza f(x) = x² − 4x + 3.

Concavidad: a=1>0, abre hacia arriba (mínimo). Vértice: x = −(−4)/(2×1) = 2; f(2) = 4−8+3 = −1, vértice **(2, −1)**. Eje de simetría: **x=2**. Intersección con eje y: **(0, 3)**. Raíces: factorizando, x²−4x+3 = (x−1)(x−3) = 0, por lo tanto **x=1 y x=3**.

**Ejemplo 2 — Modelar una situación de oferta y demanda**

Un vendedor de empanadas en la costa estima que su ganancia diaria G (en miles de pesos), según el precio x (en cientos de pesos) que cobra por cada empanada, sigue el modelo G(x) = −2x² + 20x − 32. ¿Qué precio maximiza su ganancia, y cuál es esa ganancia máxima?

Como a=−2<0, la parábola tiene un máximo en su vértice: x = −20/(2×(−2)) = 5. G(5) = −2(25)+100−32 = −50+100−32 = **18**. El precio óptimo es $500 (x=5, en cientos de pesos), con una ganancia máxima de **$18.000 diarios**.

**Ejemplo 3 — Región de soluciones de una inecuación**

Determina si el punto (2, 10) pertenece a la región de soluciones de la inecuación y > x² + 1.

Se evalúa x²+1 en x=2: 2²+1 = 5. Como 10 > 5, la desigualdad **se cumple**, por lo tanto el punto (2, 10) sí pertenece a la región de soluciones (la región "sobre" la parábola).

#### Preguntas de autoevaluación

**Pregunta 1 (alternativas).** Para f(x) = x² + 2x − 8, ¿cuál es la coordenada x del vértice?
a) −1
b) 1
c) −4
d) 4

**Respuesta correcta: a) −1.**
*Retroalimentación:* x = −b/(2a) = −2/(2×1) = −1.

**Pregunta 2 (verdadero o falso).** Si a<0 en f(x)=ax²+bx+c, la parábola abre hacia arriba y tiene un mínimo.

**Respuesta correcta: Falso.**
*Retroalimentación:* cuando a<0, la parábola abre hacia **abajo** y tiene un **máximo**; el caso a>0 es el que abre hacia arriba y tiene un mínimo.

**Pregunta 3 (calcular — eje de simetría).** Determina el eje de simetría de f(x) = −3x² + 6x + 1.
a) x = 1
b) x = −1
c) x = 2
d) x = 0

**Respuesta correcta: a) x = 1.**
*Retroalimentación:* x = −b/(2a) = −6/(2×(−3)) = −6/−6 = 1.

**Pregunta 4 (alternativas — vértice y concavidad).** ¿Cuáles son el vértice y la concavidad de f(x) = 2x² − 8x + 5?
a) (−2, 29), hacia arriba
b) (2, −3), hacia arriba
c) (2, −3), hacia abajo
d) (4, 5), hacia arriba

**Respuesta correcta: b) (2, −3), hacia arriba.**
*Retroalimentación:* x = −b/(2a) = 8/4 = 2; f(2) = −3; como a = 2 > 0, abre hacia arriba (mínimo).

**Pregunta 5 (alternativas — intersecciones con el eje x).** ¿En qué puntos f(x) = x² − x − 6 corta al eje x?
a) (−3, 0) y (2, 0)
b) (6, 0) y (−1, 0)
c) (3, 0) y (−2, 0)
d) (0, −6)

**Respuesta correcta: c) (3, 0) y (−2, 0).**
*Retroalimentación:* x² − x − 6 = (x − 3)(x + 2) = 0; (0, −6) es la intersección con el eje y.

**Pregunta 6 (alternativas — tabla de valores).** Para f(x) = x², la tabla da x = −2, −1, 0, 1, 2 → f(x) = 4, 1, 0, 1, 4. ¿Cuál es el eje de simetría?
a) x = 0
b) y = 0
c) x = 4
d) x = 1

**Respuesta correcta: a) x = 0.**
*Retroalimentación:* los valores son simétricos alrededor de x = 0: f(−2) = f(2) y f(−1) = f(1).

**Pregunta 7 (alternativas — modelamiento agrícola).** La producción de papas sigue P(x) = −0,01x² + 2x + 5 (x en kg de fertilizante). ¿Para qué cantidad se obtiene la máxima producción y cuánto es?
a) 200 kg; 5 toneladas
b) 100 kg; 205 toneladas
c) 50 kg; 80 toneladas
d) 100 kg; 105 toneladas

**Respuesta correcta: d) 100 kg; 105 toneladas.**
*Retroalimentación:* x = −2/(2 · (−0,01)) = 100; P(100) = −100 + 200 + 5 = 105.

**Pregunta 8 (alternativas — inecuación cuadrática).** ¿Pertenece el punto (2, 10) a la región de soluciones de y > x² + 1?
a) No, porque 10 < 5
b) Sí, porque 10 > 2² + 1 = 5
c) No, porque el punto está sobre la parábola
d) Sí, porque 2 > 1

**Respuesta correcta: b) Sí, porque 10 > 2² + 1 = 5.**
*Retroalimentación:* se evalúa el lado derecho en x = 2 y se compara con y = 10.

**Pregunta 9 (alternativas — comparar funciones).** ¿Qué afirmación sobre f(x) = x² − 4 y g(x) = −x² + 4 es correcta?
a) Tienen el mismo vértice (0, −4) y la misma concavidad, porque ambas son parábolas con coeficiente de x² igual a 1
b) Tienen ejes de simetría distintos (x = 4 y x = −4), porque el término independiente desplaza la parábola hacia los lados
c) Comparten el eje de simetría x = 0, pero f abre hacia arriba (mínimo −4) y g hacia abajo (máximo 4); son reflejos respecto al eje x
d) Ninguna de las dos tiene vértice, porque al no tener término en x no alcanzan un valor máximo ni mínimo

**Respuesta correcta: c) Comparten el eje de simetría x = 0, pero f abre hacia arriba (mínimo −4) y g hacia abajo (máximo 4); son reflejos respecto al eje x.**
*Retroalimentación:* de hecho g(x) = −f(x).

---

### OA 5 — Comprender la función inversa

Vas a mostrar que comprendes el concepto de **función inversa**: usando la metáfora de una máquina que "deshace" lo que otra máquina hizo, representándola con tablas y gráficos, reconociendo que su gráfica corresponde a la **reflexión** de la función original respecto a la recta y=x, y calculando la inversa de funciones **lineales** y **cuadráticas**.

**¿Por qué importa?** Muchas situaciones requieren "deshacer" una transformación: si conoces la temperatura en grados Celsius y necesitas convertirla a Fahrenheit usas una función; si tienes la temperatura en Fahrenheit y quieres volver a Celsius, necesitas la función **inversa**. Entender cómo obtener la inversa de una función te permite "regresar" desde un resultado hasta el dato que lo produjo.

**Metáfora de la máquina:** si f es una máquina que transforma una entrada x en una salida y, entonces f⁻¹ (la inversa) es una máquina que toma esa salida y y devuelve la entrada original x: deshace, en orden inverso, cada paso que hizo f.

**Cómo calcular la inversa de una función lineal:** se reemplaza f(x) por y, se intercambian x e y, y se despeja la nueva y. Por ejemplo, para f(x)=mx+b: y=mx+b → x=my+b → y=(x−b)/m.

**Sobre las funciones cuadráticas:** una función cuadrática f(x)=x² **no es invertible** si se considera todo su dominio (números reales), porque no es inyectiva: por ejemplo, f(2)=4 y f(−2)=4, dos entradas distintas producen la misma salida, y una inversa tendría que "devolver" dos valores para una misma entrada, lo cual no es una función. Por eso, para definir su inversa, se **restringe el dominio** (por ejemplo, a x≥0).

#### Ejemplos resueltos

**Ejemplo 1 — Inversa de una función lineal**

Encuentra la función inversa de f(x) = 3x − 6.

Se escribe y=3x−6, se intercambian las variables: x=3y−6, y se despeja y: x+6=3y → y=(x+6)/3. La inversa es **f⁻¹(x) = (x+6)/3**. (Verificación: f⁻¹(0) = 6/3 = 2, y f(2) = 3(2)−6 = 0 ✓).

**Ejemplo 2 — Inversa de una función cuadrática con dominio restringido**

Encuentra la inversa de f(x) = x², considerando solo x≥0.

Se escribe y=x², se intercambian las variables: x=y², y se despeja y (tomando la raíz positiva, ya que el dominio original era x≥0): y=√x. La inversa es **f⁻¹(x) = √x**.

**Ejemplo 3 — Aplicación: conversión de temperatura**

La fórmula F = (9/5)C + 32 convierte grados Celsius a Fahrenheit. Si en un día de verano en Santiago el termómetro marca 86°F, usa la función inversa para determinar la temperatura en grados Celsius.

Despejando C en la fórmula original: C = (5/9)(F−32). Reemplazando F=86: C = (5/9)(86−32) = (5/9)(54) = **30°C**.

#### Preguntas de autoevaluación

**Pregunta 1 (alternativas).** ¿Cuál es la inversa de f(x) = x + 5?
a) f⁻¹(x) = x − 5
b) f⁻¹(x) = x + 5
c) f⁻¹(x) = 5 − x
d) f⁻¹(x) = −x − 5

**Respuesta correcta: a) f⁻¹(x) = x − 5.**
*Retroalimentación:* si f suma 5, la inversa debe restar 5 para deshacer esa operación.

**Pregunta 2 (verdadero o falso).** La gráfica de la función inversa es siempre la reflexión de la gráfica de la función original respecto a la recta y=x.

**Respuesta correcta: Verdadero.**
*Retroalimentación:* como la inversa intercambia los roles de x e y, cada punto (a,b) de f se transforma en el punto (b,a) de f⁻¹, y ese intercambio corresponde geométricamente a una reflexión respecto a la recta y=x.

**Pregunta 3 (calcular).** Determina la inversa de f(x) = 4x.
a) f⁻¹(x) = x/4
b) f⁻¹(x) = 4x
c) f⁻¹(x) = x − 4
d) f⁻¹(x) = 1/(4x)

**Respuesta correcta: a) f⁻¹(x) = x/4.**
*Retroalimentación:* si f multiplica por 4, la inversa debe dividir por 4 para deshacer esa operación.

**Pregunta 4 (alternativas — función lineal).** ¿Cuál es la inversa de f(x) = 2x − 10?
a) f⁻¹(x) = (x + 10)/2
b) f⁻¹(x) = (x − 10)/2
c) f⁻¹(x) = 2x + 10
d) f⁻¹(x) = 1/(2x − 10)

**Respuesta correcta: a) f⁻¹(x) = (x + 10)/2.**
*Retroalimentación:* se intercambian x e y y se despeja: x = 2y − 10 → y = (x + 10)/2.

**Pregunta 5 (alternativas — función cuadrática).** ¿Cuál es la inversa de f(x) = x² − 3, considerando x ≥ 0?
a) f⁻¹(x) = √(x − 3)
b) f⁻¹(x) = x² + 3
c) f⁻¹(x) = −√(x + 3)
d) f⁻¹(x) = √(x + 3)

**Respuesta correcta: d) f⁻¹(x) = √(x + 3).**
*Retroalimentación:* y² = x + 3 y se toma la raíz positiva porque x ≥ 0 en la función original.

**Pregunta 6 (alternativas — a partir de puntos).** Una función lineal pasa por (0, 2) y (2, 6). ¿Qué punto pertenece con seguridad a su inversa?
a) (2, 6)
b) (6, 2)
c) (0, 2)
d) (−2, −6)

**Respuesta correcta: b) (6, 2).**
*Retroalimentación:* la inversa intercambia las coordenadas de cada punto; también (2, 0) pertenece a f⁻¹.

**Pregunta 7 (alternativas — conversión de temperatura).** Con C = (5/9)(F − 32), ¿a cuántos °C corresponden 86 °F?
a) 15,8 °C
b) 30 °C
c) 47,8 °C
d) 54 °C

**Respuesta correcta: b) 30 °C.**
*Retroalimentación:* (5/9)(86 − 32) = (5/9) · 54 = 30.

**Pregunta 8 (alternativas — máquina).** f(x) = x/3 + 1 divide por 3 y luego suma 1. ¿Qué hace su inversa?
a) Resta 1 y luego multiplica por 3: f⁻¹(x) = 3x − 3
b) Multiplica por 3 y luego resta 1: f⁻¹(x) = 3x − 1
c) Divide por 3 y resta 1: f⁻¹(x) = x/3 − 1
d) Suma 1 y multiplica por 3: f⁻¹(x) = 3x + 3

**Respuesta correcta: a) Resta 1 y luego multiplica por 3: f⁻¹(x) = 3x − 3.**
*Retroalimentación:* la inversa deshace los pasos en orden contrario.

**Pregunta 9 (alternativas — restricción de dominio).** ¿Por qué f(x) = x², con dominio en todos los reales, no tiene una inversa que sea función, y cómo se resuelve?
a) Porque no tiene recorrido definido (f(x) puede ser negativo); se agrega el cero al recorrido y entonces f⁻¹(x) = x²
b) Porque es una función lineal (f(2) = 4 y f(3) = 6); se eleva al cubo para que crezca, y entonces f⁻¹(x) = ∛x
c) Sí tiene inversa en todos los reales, porque cada x tiene una sola imagen (f(2) = 4); su inversa es f⁻¹(x) = √x
d) Porque no es inyectiva (f(2) = f(−2) = 4); se restringe el dominio, por ejemplo a x ≥ 0, y entonces f⁻¹(x) = √x

**Respuesta correcta: d) Porque no es inyectiva (f(2) = f(−2) = 4); se restringe el dominio, por ejemplo a x ≥ 0, y entonces f⁻¹(x) = √x.**
*Retroalimentación:* si se invirtiera sin restringir, a x = 4 le corresponderían dos valores de y.

---

## Eje 3: Geometría

### OA 8 — Comprender las razones trigonométricas

Vas a mostrar que comprendes las **razones trigonométricas de seno, coseno y tangente en triángulos rectángulos**: relacionándolas con las propiedades de la semejanza de triángulos, explicándolas de manera pictórica y simbólica, aplicándolas para determinar ángulos o medidas de lados desconocidos, y resolviendo problemas geométricos y de la vida cotidiana —incluyendo la **resolución completa de triángulos rectángulos** (determinar todos sus ángulos y lados).

**¿Por qué importa?** El año pasado usaste el teorema de Pitágoras para relacionar los tres lados de un triángulo rectángulo. Las razones trigonométricas van un paso más allá: te permiten relacionar los **lados con los ángulos**. Esto es extremadamente útil cuando no puedes medir una distancia directamente —como la altura de un cerro o de un edificio— pero sí puedes medir un ángulo con un instrumento y una distancia accesible en el suelo.

**Razones trigonométricas** (para un ángulo agudo θ de un triángulo rectángulo):

| Razón | Definición |
|---|---|
| Seno | sen θ = cateto opuesto ÷ hipotenusa |
| Coseno | cos θ = cateto adyacente ÷ hipotenusa |
| Tangente | tan θ = cateto opuesto ÷ cateto adyacente |

Con calculadora, puedes usar las funciones **sen⁻¹**, **cos⁻¹** y **tan⁻¹** (arcoseno, arcocoseno, arcotangente) para encontrar la medida de un ángulo cuando conoces la razón entre dos lados.

#### Ejemplos resueltos

**Ejemplo 1 — Calcular un lado conociendo el ángulo y la hipotenusa**

En un triángulo rectángulo, un ángulo agudo mide 30° y la hipotenusa mide 10 cm. Calcula el cateto opuesto a ese ángulo.

sen(30°) = cateto opuesto ÷ 10. Como sen(30°)=0,5: cateto opuesto = 10×0,5 = **5 cm**.

**Ejemplo 2 — Calcular un ángulo conociendo dos catetos**

En un triángulo rectángulo, el cateto opuesto a un ángulo θ mide 3 cm y el cateto adyacente mide 4 cm. Calcula θ.

tan θ = 3/4 = 0,75. Usando la función inversa de la calculadora: θ = tan⁻¹(0,75) ≈ **36,87°**.

**Ejemplo 3 — Aplicación: altura de un cerro**

Un dron se ubica a 50 m de la base de un cerro, sobre terreno plano, y mide un ángulo de elevación de 35° hasta la cima. Calcula la altura aproximada del cerro.

tan(35°) = altura ÷ 50. Altura = 50 × tan(35°) ≈ 50 × 0,7002 ≈ **35,0 m**.

#### Preguntas de autoevaluación

**Pregunta 1 (alternativas).** En un triángulo rectángulo, el cateto opuesto a un ángulo θ mide 6 cm y la hipotenusa mide 10 cm. ¿Cuál es sen θ?
a) 0,6
b) 0,4
c) 1,67
d) 0,167

**Respuesta correcta: a) 0,6.**
*Retroalimentación:* sen θ = cateto opuesto ÷ hipotenusa = 6/10 = 0,6.

**Pregunta 2 (verdadero o falso).** La tangente de un ángulo se calcula como el cateto opuesto dividido por la hipotenusa.

**Respuesta correcta: Falso.**
*Retroalimentación:* la tangente es el cateto opuesto dividido por el cateto **adyacente**; la razón que divide por la hipotenusa es el seno (si es el opuesto) o el coseno (si es el adyacente).

**Pregunta 3 (calcular).** Un triángulo rectángulo tiene un ángulo de 45° y cateto adyacente de 8 cm. Calcula el cateto opuesto.
a) 8 cm
b) 5,66 cm
c) 11,3 cm
d) 4 cm

**Respuesta correcta: a) 8 cm.**
*Retroalimentación:* tan(45°)=1, y cateto opuesto = cateto adyacente × tan(45°) = 8×1 = 8 cm.

**Pregunta 4 (alternativas — cateto opuesto).** En un triángulo rectángulo, la hipotenusa mide 15 cm y un ángulo agudo mide 50°. ¿Cuánto mide el cateto opuesto a ese ángulo?
a) ≈ 9,64 cm
b) ≈ 11,49 cm
c) ≈ 17,88 cm
d) ≈ 19,58 cm

**Respuesta correcta: b) ≈ 11,49 cm.**
*Retroalimentación:* cateto opuesto = 15 · sen(50°) ≈ 15 · 0,766; 9,64 cm usaría el coseno.

**Pregunta 5 (alternativas — encontrar un ángulo).** El cateto opuesto a θ mide 7 cm y el adyacente 24 cm. ¿Cuánto mide θ?
a) ≈ 73,74°
b) ≈ 16,96°
c) ≈ 16,26°
d) ≈ 0,29°

**Respuesta correcta: c) ≈ 16,26°.**
*Retroalimentación:* tan θ = 7/24 ≈ 0,2917 y θ = tan⁻¹(0,2917); 73,74° es el otro ángulo agudo.

**Pregunta 6 (alternativas — leer datos).** Un triángulo rectángulo tiene hipotenusa 13 cm y catetos 5 y 12 cm. Si θ es opuesto al cateto de 5 cm, ¿cuánto vale cos θ?
a) 12/13 ≈ 0,923
b) 5/13 ≈ 0,385
c) 5/12 ≈ 0,417
d) 13/12 ≈ 1,083

**Respuesta correcta: a) 12/13 ≈ 0,923.**
*Retroalimentación:* el cateto adyacente a θ es el de 12 cm: cos θ = adyacente/hipotenusa.

**Pregunta 7 (alternativas — rampa de acceso).** Una rampa debe tener 6° de inclinación y salvar una altura de 0,9 m. ¿Cuál es su longitud mínima aproximada?
a) ≈ 0,09 m
b) ≈ 0,91 m
c) ≈ 8,56 m
d) ≈ 8,61 m

**Respuesta correcta: d) ≈ 8,61 m.**
*Retroalimentación:* sen(6°) = 0,9/L → L = 0,9/0,1045 ≈ 8,61 m; 8,56 m sería la distancia horizontal (tangente).

**Pregunta 8 (alternativas — ángulo de depresión).** Desde un edificio de 40 m, un auto se ve con un ángulo de depresión de 25°. ¿A qué distancia horizontal está de la base?
a) ≈ 18,65 m
b) ≈ 85,79 m
c) ≈ 94,65 m
d) ≈ 36,25 m

**Respuesta correcta: b) ≈ 85,79 m.**
*Retroalimentación:* tan(25°) = 40/d → d = 40/0,4663.

**Pregunta 9 (alternativas — resolver un triángulo).** Un cateto mide 9 cm y el ángulo opuesto es 40°. ¿Cuánto miden la hipotenusa, el otro cateto y el otro ángulo agudo?
a) ≈ 11,7 cm; ≈ 7,5 cm; 50°
b) ≈ 14,0 cm; ≈ 9 cm; 40°
c) ≈ 14,0 cm; ≈ 10,72 cm; 50°
d) ≈ 5,8 cm; ≈ 10,72 cm; 140°

**Respuesta correcta: c) ≈ 14,0 cm; ≈ 10,72 cm; 50°.**
*Retroalimentación:* hip = 9/sen(40°) ≈ 14,0; otro cateto = hip · cos(40°) ≈ 10,72; otro ángulo: 90° − 40°.

---

## Eje 4: Probabilidad y Estadística

### OA 11 — Utilizar permutaciones y combinatoria sencilla para calcular probabilidades

Vas a utilizar el **principio multiplicativo**, el **factorial**, las **permutaciones** y la **combinatoria sencilla** para contar de manera sistemática el número de posibilidades de una situación, y aplicar ese conteo al cálculo de **probabilidades** de eventos en juegos de azar y en situaciones de la vida cotidiana.

**¿Por qué importa?** El año pasado calculaste probabilidades combinando eventos con las reglas aditiva y multiplicativa, contando casos "a mano". Pero cuando el número de posibilidades es grande —como las combinaciones de un candado, o el orden de llegada de varios corredores— contar caso por caso se vuelve poco práctico. El principio multiplicativo, el factorial y las permutaciones te dan herramientas para **contar sistemáticamente**, sin necesidad de enumerar todas las opciones una por una.

**Principio multiplicativo (regla del producto):** si una tarea se puede descomponer en pasos sucesivos con m, n, p, … opciones cada uno, el número total de formas de completarla es **m × n × p × …**.

**Factorial:** el factorial de un número natural n, escrito **n!**, es el producto de todos los números naturales desde n hasta 1: n! = n×(n−1)×(n−2)×…×2×1. Representa el número de formas de **ordenar** n objetos distintos (una **permutación**).

**Combinatoria sencilla:** cuando se eligen r elementos de un total de n, y el **orden no importa**, el número de formas se llama combinación, y se calcula como C(n,r) = n! / (r!×(n−r)!).

#### Ejemplos resueltos

**Ejemplo 1 — Principio multiplicativo**

Un local de comida ofrece 4 tipos de empanada y 3 bebidas distintas. ¿De cuántas formas puede un cliente elegir una empanada y una bebida?

Se multiplican las opciones de cada paso: 4 × 3 = **12 formas distintas**.

**Ejemplo 2 — Permutaciones (factorial)**

¿De cuántas formas distintas pueden ordenarse 5 corredores en la llegada de una carrera (sin empates)?

Cada corredor ocupa un lugar distinto, sin repetición: 5! = 5×4×3×2×1 = **120 formas distintas**.

**Ejemplo 3 — Combinatoria aplicada a la probabilidad**

En un sorteo se eligen 3 números al azar entre el 1 y el 10, sin repetición y sin importar el orden. Si una persona apostó a los mismos 3 números que resultarán elegidos, ¿cuál es la probabilidad de que gane?

El total de combinaciones posibles es C(10,3) = 10!/(3!×7!) = (10×9×8)/(3×2×1) = 720/6 = 120. Como solo hay 1 combinación ganadora: P(ganar) = 1/120 ≈ **0,83%**.

#### Preguntas de autoevaluación

**Pregunta 1 (alternativas).** Un menú de almuerzo tiene 3 entradas y 5 platos de fondo. ¿De cuántas formas distintas se puede elegir una entrada y un plato de fondo?
a) 8
b) 15
c) 3
d) 5

**Respuesta correcta: b) 15.**
*Retroalimentación:* por el principio multiplicativo, se multiplican las opciones de cada paso: 3×5=15.

**Pregunta 2 (verdadero o falso).** El número de formas de ordenar 4 personas distintas en una fila es 4×3=12.

**Respuesta correcta: Falso.**
*Retroalimentación:* ordenar n objetos distintos corresponde a n!, no solo a los dos primeros factores; en este caso es 4! = 4×3×2×1 = 24.

**Pregunta 3 (calcular — factorial).** Calcula 6!/4!.
a) 2
b) 30
c) 720
d) 15

**Respuesta correcta: b) 30.**
*Retroalimentación:* 6!/4! = (6×5×4×3×2×1)/(4×3×2×1) = 6×5 = 30 (los factores comunes se simplifican).

**Pregunta 4 (alternativas — permutaciones).** ¿De cuántas formas se pueden ordenar las 4 letras de "AMOR"?
a) 4
b) 16
c) 24
d) 256

**Respuesta correcta: c) 24.**
*Retroalimentación:* 4! = 4 · 3 · 2 · 1 = 24.

**Pregunta 5 (alternativas — probabilidad).** En una rifa de 200 números se sortea un ganador. Si una persona compró 5 números, ¿cuál es la probabilidad de que gane?
a) 1/200
b) 5%
c) 1/5
d) 1/40 (2,5%)

**Respuesta correcta: d) 1/40 (2,5%).**
*Retroalimentación:* 5/200 = 1/40 = 0,025.

**Pregunta 6 (alternativas — clave numérica).** Una clave tiene 3 dígitos distintos del 0 al 9. ¿Cuántas claves son posibles?
a) 1.000
b) 720
c) 120
d) 30

**Respuesta correcta: b) 720.**
*Retroalimentación:* principio multiplicativo sin repetición: 10 · 9 · 8 = 720; 1.000 permitiría repetir dígitos.

**Pregunta 7 (alternativas — combinación).** Entre 6 estudiantes se eligen 2 representantes con el mismo rol. ¿De cuántas formas?
a) 30
b) 12
c) 15
d) 36

**Respuesta correcta: c) 15.**
*Retroalimentación:* C(6, 2) = (6 · 5)/(2 · 1) = 15; 30 contaría el orden.

**Pregunta 8 (alternativas — probabilidad y permutaciones).** En una carrera de 8 corredores con iguales posibilidades, ¿cuál es la probabilidad de que uno específico gane?
a) 1/8
b) 1/8!
c) 7/8
d) 1/7

**Respuesta correcta: a) 1/8.**
*Retroalimentación:* también puede razonarse como 7!/8! = 1/8.

**Pregunta 9 (alternativas — principio multiplicativo).** Un local ofrece 3 panes, 4 salsas y la opción de agregar o no palta. ¿Cuántas combinaciones de pedido hay?
a) 9
b) 12
c) 14
d) 24

**Respuesta correcta: d) 24.**
*Retroalimentación:* 3 · 4 · 2 = 24; el factor 2 es "con palta" o "sin palta".

**Pregunta 10 (alternativas — propiedad del factorial).** ¿Cómo se comparan 5! y 4! × 5?
a) 5! es mayor
b) Son iguales (120), porque 5! = 5 · 4!
c) 4! × 5 es mayor
d) No se pueden comparar sin calcular

**Respuesta correcta: b) Son iguales (120), porque 5! = 5 · 4!.**
*Retroalimentación:* ambas representan exactamente la misma multiplicación.

---

## Glosario

- **Número real:** conjunto que incluye a todos los números racionales (que se pueden escribir como fracción) y a los números irracionales (como √2 o π, que no se pueden escribir como fracción).
- **Racionalizar:** transformar una fracción que tiene una raíz en el denominador en una expresión equivalente sin raíces en el denominador, multiplicando por una raíz conveniente.
- **Logaritmo:** el exponente al que hay que elevar una base a para obtener un número b: log_a(b)=c ⟺ aᶜ=b.
- **Potencia de exponente racional:** forma equivalente de escribir una raíz como potencia: a^(m/n) = ⁿ√(aᵐ).
- **Función cuadrática:** función de la forma f(x)=ax²+bx+c (con a≠0), cuya gráfica es una parábola.
- **Vértice:** punto más alto o más bajo de una parábola, donde la función alcanza su valor máximo o mínimo.
- **Concavidad:** dirección hacia la que abre una parábola: hacia arriba si a>0 (mínimo), hacia abajo si a<0 (máximo).
- **Eje de simetría:** recta vertical que pasa por el vértice de una parábola y respecto a la cual la gráfica es simétrica.
- **Función inversa:** función que "deshace" lo que hace otra función; si f(a)=b, entonces f⁻¹(b)=a. Su gráfica es la reflexión de la función original respecto a la recta y=x.
- **Razones trigonométricas:** relaciones entre los lados de un triángulo rectángulo y uno de sus ángulos agudos: seno (opuesto/hipotenusa), coseno (adyacente/hipotenusa) y tangente (opuesto/adyacente).
- **Ángulo de elevación / depresión:** ángulo que se forma entre la horizontal y la línea de visión hacia un objeto, ya sea hacia arriba (elevación) o hacia abajo (depresión).
- **Principio multiplicativo:** regla de conteo que establece que, si una tarea tiene varios pasos sucesivos con m, n, p, … opciones cada uno, el total de formas de realizarla es m×n×p×…
- **Factorial (n!):** producto de todos los números naturales desde n hasta 1; representa el número de formas de ordenar n objetos distintos.
- **Permutación:** cada una de las distintas formas de ordenar un conjunto de elementos, donde el orden importa.
- **Combinación:** cada una de las distintas formas de elegir un subconjunto de elementos de un conjunto mayor, donde el orden no importa.
