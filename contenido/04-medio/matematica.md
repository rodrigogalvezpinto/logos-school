---
título: Matemática — 4° Medio
asignatura: Matemática
curso: 4° Medio
tipo: Guía de estudio
basado_en: Bases Curriculares, Decreto 193/2019 "Plan Común" (Mineduc/UCE) — temario oficial del Examen Libre de Validación de Estudios
oa_evaluados: OA 1, OA 2, OA 3
ultima_actualizacion: 2026-10-28
---

# Matemática — 4° Medio

> Este apunte se basa fielmente en el temario oficial del Mineduc/UCE para el Examen Libre de Validación de Estudios de 4° medio, bajo el **Decreto de Bases Curriculares N°193, del año 2019 ("Plan Común")**. 4° medio es el **último curso de todo el ciclo escolar**: lo que aprendas aquí es, en muchos casos, la última matemática formal que verás antes de enfrentar decisiones financieras, laborales y ciudadanas por tu cuenta. Igual que en 3° medio, la selección de Objetivos de Aprendizaje para el examen se reduce a solo **3 OA** de Matemática. Que sean pocos no los hace simples: cada uno agrupa un abanico amplio de contenidos, por lo que este apunte los cubre en profundidad, con abundantes ejemplos y preguntas.

## Antes de empezar

**Sobre el formato del examen:** cada asignatura se rinde en una prueba **separada e independiente**, de **25 preguntas** y **90 minutos** de duración (máximo 2 pruebas por día). En la prueba de Matemática **se permite el uso de calculadora**. Úsala con criterio: para potencias, raíces y razones trigonométricas que no son "redondas", pero sigues siendo tú quien decide qué operación aplicar, cómo plantear el problema, y si el resultado tiene sentido en el contexto.

Este año trabajas con tres grandes bloques de contenido, cada uno correspondiente a un único Objetivo de Aprendizaje, distribuidos en dos ejes:

1. **Álgebra y Funciones (OA1)** — **matemática financiera**: tasas de interés, índices económicos (IPC, UF), y cómo usarlos para evaluar y comparar créditos, ahorros e inversiones, y tomar decisiones financieras fundamentadas.
2. **Probabilidad y Estadística (OA2)** — **decisiones bajo incertidumbre con modelos binomial y normal**: calcular probabilidades en experimentos aleatorios, reconocer cuándo conviene usar cada modelo, y evaluar críticamente los alcances y límites de un argumento estadístico antes de confiar en él.
3. **Álgebra y Funciones (OA3)** — **modelos de crecimiento, decrecimiento y fenómenos periódicos**: funciones potencia de exponente entero (positivo y negativo) y funciones trigonométricas seno y coseno, para describir desde la intensidad de una señal hasta las mareas o las estaciones del año.

En todo momento vas a practicar las habilidades matemáticas de **resolver problemas**, **argumentar y comunicar**, **modelar** situaciones reales, y **representar** información de distintas formas —incluyendo la búsqueda, selección, contrastación y verificación de información en ambientes digitales y redes sociales, algo que el propio Mineduc destaca como especialmente relevante en este nivel, donde pronto tomarás decisiones financieras y cívicas de forma autónoma—. ¡Empecemos!

---

## Eje: Álgebra y Funciones

### OA 1 — Fundamentar decisiones financieras y económicas

Vas a **fundamentar decisiones en el ámbito financiero y económico**, personal o comunitario, a partir de modelos que consideran **tasas de interés e índices económicos**: interpretando información financiera que involucra porcentajes y tasas, evaluando distintas posibilidades de crédito para tomar una decisión informada, y ajustando esos modelos para encontrar la mejor alternativa en una situación dada.

**¿Por qué importa?** Al terminar 4° medio, muchas de las decisiones económicas de tu vida —pedir un crédito, elegir entre ahorrar en un banco o en otro instrumento, entender por qué suben los precios, decidir si conviene una oferta "en cuotas"— dejan de estar mediadas por un adulto y pasan a ser tuyas. Detrás de casi todas ellas hay una tasa de interés o un índice económico. Entender cómo funcionan no es un lujo académico: es lo que separa a alguien que puede leer un contrato de crédito y detectar si es conveniente, de alguien que firma sin entender cuánto terminará pagando en total.

**Interés simple vs. interés compuesto:**

| | Fórmula | Característica |
|---|---|---|
| Interés simple | I = C·i·t ; Monto final M = C·(1+i·t) | Los intereses se calculan **siempre sobre el capital inicial** C; crecen linealmente. |
| Interés compuesto | M = C·(1+i)ᵗ | Los intereses se calculan **sobre el capital + intereses ya acumulados**; crecen exponencialmente. |

(C = capital inicial, i = tasa de interés por período en decimal, t = número de períodos, M = monto final)

**Tasa nominal anual vs. tasa efectiva anual (TEA):** cuando una tasa anual se aplica varias veces al año (por ejemplo, mensualmente), la tasa efectivamente pagada en un año es mayor que la tasa nominal, porque cada capitalización genera intereses sobre intereses anteriores. Si i_nom es la tasa nominal anual y n es el número de capitalizaciones al año:

**TEA = (1 + i_nom/n)ⁿ − 1**

**Índices económicos usados en Chile:**

- **IPC (Índice de Precios al Consumidor):** mide la variación porcentual promedio de los precios de una canasta de bienes y servicios; su variación mensual/anual es lo que comúnmente se llama "inflación".
- **UF (Unidad de Fomento):** unidad de cuenta reajustable diariamente según la variación del IPC del mes anterior; se usa en créditos hipotecarios, arriendos y contratos de largo plazo para proteger su valor real frente a la inflación. Para pasar de UF a pesos se multiplica por el valor de la UF del día.
- **CAE (Carga Anual Equivalente):** indicador que resume, en una sola tasa porcentual anual, el costo total de un crédito (incluyendo intereses y otros cargos), permitiendo **comparar créditos de distintas instituciones** de forma más justa que comparando solo la tasa de interés nominal.

**Evaluar y ajustar un modelo financiero:** al comparar alternativas (por ejemplo, dos créditos o dos formas de ahorro), no basta con mirar la tasa de interés anunciada: hay que considerar el plazo, la frecuencia de capitalización, y el costo total. "Ajustar" el modelo significa variar uno de estos parámetros (plazo, tasa, capital) para ver cómo cambia el resultado y así encontrar la alternativa más conveniente para una situación concreta.

#### Ejemplos resueltos

**Ejemplo 1 — Interés simple vs. compuesto**

Un estudiante invierte $500.000 a una tasa del 6% anual durante 3 años. Compara el monto final con interés simple y con interés compuesto.

Simple: M = 500.000×(1+0,06×3) = 500.000×1,18 = **$590.000**.
Compuesto: M = 500.000×(1,06)³ = 500.000×1,191016 ≈ **$595.508**.

La diferencia (≈$5.508) son los "intereses sobre intereses" que genera la capitalización compuesta, y esa diferencia crece cada vez más mientras más largo sea el plazo.

**Ejemplo 2 — Tasa nominal vs. tasa efectiva**

Un banco ofrece una tarjeta con tasa nominal anual del 24%, capitalizada mensualmente (n=12). Calcula la tasa efectiva anual (TEA).

TEA = (1 + 0,24/12)¹² − 1 = (1+0,02)¹² − 1 = (1,02)¹² − 1 ≈ 1,2682 − 1 = **0,2682 = 26,82% efectivo anual**, más alto que el 24% nominal anunciado, precisamente por el efecto de capitalizar cada mes.

**Ejemplo 3 — Comparar créditos usando CAE**

Un estudiante que quiere financiar un curso técnico compara dos créditos de $1.000.000 a 12 meses: el Crédito A tiene CAE de 18%, y el Crédito B tiene una tasa de interés anunciada más baja, pero con cargos administrativos que elevan su CAE a 22%. ¿Cuál conviene más y por qué?

**Conviene el Crédito A**, porque el CAE ya incorpora tanto los intereses como los cargos adicionales en una sola cifra comparable: aunque la tasa "anunciada" del Crédito B parezca más atractiva, su costo total real (reflejado en el CAE de 22%) es mayor que el del Crédito A.

#### Preguntas de autoevaluación

**Pregunta 1 (alternativas).** ¿Cuál es la diferencia clave entre interés simple e interés compuesto?
a) el interés simple se cobra solo una vez al final del crédito, y el compuesto se cobra todos los meses sobre el capital inicial
b) el interés compuesto se calcula sobre el capital más los intereses ya acumulados; el simple, siempre sobre el capital inicial
c) el interés simple es siempre mayor que el compuesto, porque se calcula sobre el capital más los intereses acumulados
d) no hay diferencia: son dos nombres para lo mismo, que se usan según el banco que ofrece el crédito

**Respuesta correcta: b).**
*Retroalimentación:* esa es la diferencia esencial: en el interés compuesto, los intereses generan a su vez nuevos intereses; en el simple, siempre se calculan sobre la misma base (el capital inicial).

**Pregunta 2 (verdadero o falso).** A igual tasa nominal anual, mientras más veces al año se capitalice el interés, mayor es la tasa efectiva anual (TEA).

**Respuesta correcta: Verdadero.**
*Retroalimentación:* capitalizar más seguido significa que los intereses empiezan a generar nuevos intereses antes, lo que aumenta el monto final y, por lo tanto, la tasa efectiva respecto a la nominal.

**Pregunta 3 (calcular).** Calcula el monto final de un depósito de $800.000 a interés simple del 5% anual durante 4 años.
a) $960.000
b) $972.405
c) $840.000
d) $1.000.000

**Respuesta correcta: a) $960.000.**
*Retroalimentación:* M = 800.000×(1+0,05×4) = 800.000×1,2 = 960.000; con interés simple, cada año se suman los mismos $40.000 (5% del capital original).

**Pregunta 4 (alternativas — completar).** La UF se reajusta según la variación del ___ y se usa principalmente en contratos de ___ plazo, como los créditos hipotecarios.
a) IPC; largo
b) dólar; corto
c) sueldo mínimo; corto
d) precio del cobre; largo

**Respuesta correcta: a) IPC; largo.**
*Retroalimentación:* la UF mantiene el valor real frente a la inflación medida por el índice de precios al consumidor.

**Pregunta 5 (alternativas — interés compuesto).** Un ahorro de $2.000.000 se deposita al 4% anual compuesto. ¿Cuál es el monto aproximado a los 6 años?
a) $2.480.000
b) ≈ $2.080.000
c) $2.240.000
d) ≈ $2.530.638

**Respuesta correcta: d) ≈ $2.530.638.**
*Retroalimentación:* M = 2.000.000 · (1,04)⁶ ≈ 2.000.000 · 1,2653; $2.480.000 sería con interés simple.

**Pregunta 6 (alternativas — tasa efectiva).** Una cuenta ofrece 12% nominal anual capitalizado trimestralmente. ¿Cuál es la tasa efectiva anual?
a) 12%
b) ≈ 12,55%
c) 3%
d) 48%

**Respuesta correcta: b) ≈ 12,55%.**
*Retroalimentación:* TEA = (1 + 0,12/4)⁴ − 1 = (1,03)⁴ − 1 ≈ 0,1255.

**Pregunta 7 (alternativas — IPC).** En enero un kilo de pan cuesta $1.200. Si su precio varió igual que el IPC acumulado del año (5%), ¿cuánto cuesta en diciembre?
a) $1.205
b) $1.800
c) $1.140
d) $1.260

**Respuesta correcta: d) $1.260.**
*Retroalimentación:* 1.200 · 1,05 = 1.260.

**Pregunta 8 (alternativas — UF).** Un arriendo es de 15 UF mensuales y la UF vale $38.500. ¿Cuánto se paga ese mes?
a) $577.500
b) $38.515
c) $2.567
d) $385.000

**Respuesta correcta: a) $577.500.**
*Retroalimentación:* 15 · 38.500 = 577.500.

**Pregunta 9 (alternativas — comparar CAE).** El Crédito X anuncia 10% de tasa con CAE de 15%; el Y anuncia 12% con CAE de 13%. ¿Cuál conviene y por qué?
a) El X, porque su tasa anunciada (10%) es menor y refleja todo el costo del crédito
b) Ambos cuestan lo mismo, porque la diferencia entre la tasa y el CAE se compensa
c) No se puede saber sin conocer el nombre y el prestigio del banco que ofrece cada uno
d) El Y, porque su CAE es menor; el CAE incluye comisiones y seguros que la tasa anunciada no considera

**Respuesta correcta: d) El Y, porque su CAE es menor; el CAE incluye comisiones y seguros que la tasa anunciada no considera.**
*Retroalimentación:* el CAE refleja mejor el costo real total del crédito.

**Pregunta 10 (alternativas — evaluar alternativas de ahorro).** Para ahorrar $300.000 durante 2 años: A paga 8% anual simple y B, 7% anual compuesto. ¿Cuál conviene?
a) B: ≈ $343.470 frente a $348.000 de A
b) A: $348.000 frente a ≈ $343.470 de B
c) Ambas dan exactamente lo mismo
d) B, porque el interés compuesto siempre gana

**Respuesta correcta: b) A: $348.000 frente a ≈ $343.470 de B.**
*Retroalimentación:* A: 300.000 · 1,16; B: 300.000 · (1,07)²; en un plazo corto, la mayor tasa simple supera al compuesto.

**Pregunta 11 (alternativas — tabla de créditos).** Para un curso de $1.500.000:

| Crédito | Tasa anunciada | CAE |
|---|---|---|
| P | 9% | 11,2% |
| Q | 10% | 10,5% |
| R | 8,5% | 12,0% |

¿Cuál conviene y qué error es común?
a) Conviene R, por su tasa anunciada más baja; el error común es fijarse en el CAE
b) Conviene P, porque su tasa y su CAE están al medio entre las tres opciones
c) Conviene Q (menor CAE); el error común es elegir R por su tasa anunciada más baja
d) Todos cuestan lo mismo, porque el monto del curso es igual para los tres

**Respuesta correcta: c) Conviene Q (menor CAE); el error común es elegir R por su tasa anunciada más baja.**
*Retroalimentación:* el CAE de R es el más alto de los tres.

**Pregunta 12 (alternativas — ajustar el plazo).** Un capital de $600.000 se invierte al 5% anual compuesto. ¿Cuántos años enteros se necesitan para superar $700.000?
a) 2 años
b) 3 años
c) 4 años
d) 5 años

**Respuesta correcta: c) 4 años.**
*Retroalimentación:* t = 3 da $694.575 (aún bajo $700.000) y t = 4 da ≈ $729.304.

**Pregunta 13 (verdadero o falso).** El CAE permite comparar el costo real de dos créditos, incluso si tienen plazos distintos, porque expresa el costo como una tasa anual equivalente.

**Respuesta correcta: Verdadero.**
*Retroalimentación:* al expresarse como una tasa anual, el CAE permite comparar créditos aunque difieran en plazo, monto o estructura de cobros, algo que la tasa de interés simple anunciada no siempre permite hacer de forma directa.

**Pregunta 14 (alternativas — poder adquisitivo).** Un sueldo pasó de $500.000 a $520.000 en un año, con IPC acumulado de 6%. ¿Qué ocurrió con el poder adquisitivo real?
a) Aumentó, porque el sueldo subió $20.000
b) Se mantuvo igual, porque el sueldo y los precios subieron
c) Aumentó un 10%, porque se suman el 4% y el 6%
d) Disminuyó, porque el sueldo subió 4% y los precios 6%

**Respuesta correcta: d) Disminuyó, porque el sueldo subió 4% y los precios 6%.**
*Retroalimentación:* 520.000/500.000 − 1 = 4%, menos que la inflación.

**Pregunta 15 (alternativas — tasa nominal y efectiva).** Dos bancos ofrecen 10% nominal anual: A capitaliza mensualmente y B semestralmente. ¿Cuál conviene para depositar?
a) B: TEA ≈ 10,47% frente a 10,25% de A
b) A: TEA ≈ 10,47% frente a 10,25% de B
c) Ambos dan 10%
d) No se puede comparar

**Respuesta correcta: b) A: TEA ≈ 10,47% frente a 10,25% de B.**
*Retroalimentación:* la capitalización más frecuente genera una tasa efectiva mayor.

**Pregunta 16 (alternativas — crédito hipotecario en UF).** ¿Por qué un crédito hipotecario en UF "traspasa" el riesgo de inflación al deudor?
a) Porque la UF baja cuando sube la inflación, y el deudor debe pagar más cuotas para compensar
b) Porque el banco asume todas las pérdidas por inflación, y el deudor paga siempre la misma cantidad de pesos durante todo el crédito
c) Porque la deuda en UF se reajusta con el IPC: si sube la inflación, sube su valor en pesos aunque el deudor no gane más
d) Porque la UF no tiene relación con los precios

**Respuesta correcta: c) Porque la deuda en UF se reajusta con el IPC: si sube la inflación, sube su valor en pesos aunque el deudor no gane más.**
*Retroalimentación:* el banco mantiene protegido el valor real de lo prestado.

**Pregunta 17 (alternativas — simple y compuesto a mayor plazo).** Con capital $500.000 al 6% anual, a 15 años, ¿cuáles son los montos con interés simple y compuesto?
a) Simple $950.000; compuesto ≈ $1.198.279 (diferencia ≈ $248.279)
b) Simple ≈ $1.198.279; compuesto $950.000 (diferencia ≈ $248.279)
c) Ambos $950.000
d) Simple $590.000; compuesto ≈ $595.508 (diferencia ≈ $5.508)

**Respuesta correcta: a) Simple $950.000; compuesto ≈ $1.198.279 (diferencia ≈ $248.279).**
*Retroalimentación:* a 3 años la diferencia era de solo ≈ $5.508: el compuesto se aleja cada vez más con el tiempo.

**Pregunta 18 (varias correctas — fundamentar una decisión).** Un joven con $1.000.000 duda entre gastarlo, ahorrar 5 años al 6% compuesto o invertir en un fondo con retorno esperado de 9% y riesgo de pérdida. ¿Qué información adicional es pertinente? Marca **todas** las correctas.
a) Si tiene necesidades de liquidez a corto plazo
b) Qué nivel de riesgo está dispuesto a asumir
c) El efecto de la inflación proyectada sobre el poder adquisitivo de cada alternativa
d) El color del logo del banco

**Respuesta correcta: a, b y c.**
*Retroalimentación:* una decisión financiera se fundamenta en algo más que comparar tasas.

---

### OA 3 — Construir modelos de crecimiento, decrecimiento y periódicos

Vas a **construir modelos de situaciones o fenómenos de crecimiento, decrecimiento y periódicos**, usando **funciones potencia de exponente entero** y **funciones trigonométricas seno y coseno**: interpretando información a partir de estos modelos, variando sus parámetros para comparar resultados, describiendo modelos existentes, construyendo tus propios modelos a partir de una situación, y comparando distintos modelos entre sí para evaluar sus fortalezas y debilidades —de forma manuscrita y con apoyo de herramientas tecnológicas, promoviendo la búsqueda y verificación de información en ambientes digitales—.

**¿Por qué importa?** No todos los fenómenos crecen o decrecen de la misma forma que una función exponencial (que ya viste en 3° medio). Algunos, como la intensidad de la luz o el sonido a medida que te alejas de la fuente, siguen una relación de **potencia** con exponente negativo. Otros, como las mareas, la temperatura a lo largo del año, o el movimiento de un péndulo, no crecen ni decrecen indefinidamente, sino que se **repiten en ciclos**: para esos, la herramienta correcta son las funciones **trigonométricas**.

**Función potencia:** f(x) = a·xⁿ, con **n entero** (puede ser positivo o negativo) y a una constante.

| n | Ejemplo | Comportamiento |
|---|---|---|
| n=1 | f(x)=a·x | relación lineal (proporcionalidad directa) |
| n=2 | f(x)=a·x² | parábola: crece cada vez más rápido; el área de una figura crece con el cuadrado de su lado |
| n=3 | f(x)=a·x³ | crece aún más rápido que n=2; el volumen de un cubo crece con el cubo de su arista |
| n=−1 | f(x)=a/x | decrece rápidamente y **nunca llega a 0** (asíntota horizontal en y=0); nunca está definida en x=0 (asíntota vertical) |
| n=−2 | f(x)=a/x² | decrece aún más rápido que n=−1 a medida que x crece; modela, por ejemplo, la intensidad de la luz o el sonido según la distancia (ley del inverso del cuadrado) |

A diferencia del modelo exponencial (donde la variable está en el exponente), en la función potencia **la variable está en la base** y el exponente es fijo.

**Funciones trigonométricas como modelos periódicos:** la forma general de un modelo periódico basado en seno o coseno es:

**f(x) = A·sen(B(x−C)) + D** (o con cos en vez de sen)

| Parámetro | Nombre | Qué representa |
|---|---|---|
| A | Amplitud | qué tan lejos se aleja el valor máximo/mínimo del valor medio D (el valor oscila entre D−A y D+A) |
| B | relacionado con el período | el período T (tiempo que dura un ciclo completo) es T = 2π/B (en radianes) o T=360°/B (en grados) |
| C | Desfase (desplazamiento horizontal) | en qué momento comienza o se ubica el ciclo respecto al origen |
| D | Valor medio (desplazamiento vertical) | el valor "central" alrededor del cual oscila la función |

**Elegir entre seno y coseno** es, en el fondo, una elección de dónde ubicar el punto de partida del ciclo (en x=0, sen(x) parte en el valor medio D subiendo, y cos(x) parte en el máximo D+A); ambas describen la misma clase de fenómeno periódico y una se puede transformar en la otra ajustando el desfase C.

#### Ejemplos resueltos

**Ejemplo 1 — Función potencia con exponente negativo: intensidad luminosa**

La intensidad de la luz de una ampolleta a una distancia d (metros) sigue el modelo I(d) = 800/d² (en lux). Calcula la intensidad a 2 metros y a 4 metros, y compara.

I(2) = 800/2² = 800/4 = **200 lux**. I(4) = 800/4² = 800/16 = **50 lux**. Al duplicar la distancia (de 2 a 4 m), la intensidad no se reduce a la mitad, sino a un **cuarto** (de 200 a 50): esto es característico del exponente −2, donde el efecto de la distancia se eleva al cuadrado.

**Ejemplo 2 — Modelo periódico: temperatura a lo largo del año**

La temperatura promedio mensual en una ciudad chilena se modela como T(m) = 8·cos((π/6)(m−1)) + 15 (°C), donde m es el mes (1=enero). Calcula la amplitud, el período, el valor medio, y la temperatura estimada en enero (m=1) y en julio (m=7).

Amplitud A=8°C; B=π/6, período T = 2π/(π/6) = 12 meses (un ciclo anual, como se espera); valor medio D=15°C.
T(1) = 8·cos(0) + 15 = 8×1+15 = **23°C** (enero, verano en el hemisferio sur).
T(7) = 8·cos(π) + 15 = 8×(−1)+15 = **7°C** (julio, invierno).

**Ejemplo 3 — Comparar dos modelos de crecimiento**

Se comparan dos modelos para el área de manchas de un cultivo bacteriano en función del radio r (cm): f(r) = 3·r² (modelo de potencia) y una tabla de datos reales que muestra que al triplicar el radio, el área observada se multiplica por 9. ¿Es consistente el modelo de potencia con los datos observados?

En el modelo f(r)=3r², si el radio se triplica (r → 3r): f(3r) = 3(3r)² = 3×9r² = 9×(3r²) = 9×f(r). El área se multiplica exactamente por 9, **consistente con lo observado**. Esto confirma que el exponente n=2 es adecuado para este fenómeno, ya que el área escala con el cuadrado del radio.

#### Preguntas de autoevaluación

**Pregunta 1 (alternativas).** ¿Cuál de las siguientes es una función potencia con exponente entero negativo?
a) f(x) = 5x²
b) f(x) = 5x
c) f(x) = 5/x³
d) f(x) = 5ˣ

**Respuesta correcta: c) f(x) = 5/x³.**
*Retroalimentación:* 5/x³ = 5·x⁻³, exponente entero negativo (−3); en cambio, 5ˣ es una función exponencial (la variable está en el exponente, no en la base).

**Pregunta 2 (verdadero o falso).** En una función potencia f(x)=a·xⁿ con n negativo, el valor de f(x) nunca puede ser igual a 0.

**Respuesta correcta: Verdadero.**
*Retroalimentación:* como f(x)=a/xⁿ (con n positivo tras el cambio de signo), la función se acerca a 0 mientras x crece, pero nunca lo alcanza exactamente: 0 es una asíntota horizontal.

**Pregunta 3 (calcular).** Si f(x) = 4x³, ¿cuál es el valor de f(3)?
a) 12
b) 36
c) 64
d) 108

**Respuesta correcta: d) 108.**
*Retroalimentación:* f(3) = 4×3³ = 4×27 = 108.

**Pregunta 4 (alternativas — completar).** En f(x) = A·sen(B(x − C)) + D, el parámetro A se llama ___ y mide cuánto se aleja la función respecto del ___ (parámetro D).
a) período; desfase
b) desfase; período
c) valor medio; amplitud
d) amplitud; valor medio

**Respuesta correcta: d) amplitud; valor medio.**
*Retroalimentación:* la amplitud es la distancia máxima respecto del valor central.

**Pregunta 5 (alternativas — período).** ¿Cuál es el período de f(x) = 5·sen(2x)?
a) 2π
b) π
c) 5
d) 4π

**Respuesta correcta: b) π.**
*Retroalimentación:* T = 2π/B = 2π/2.

**Pregunta 6 (alternativas — potencia negativa).** Con F(d) = k/d², a 3 unidades la fuerza es 20 N. ¿Cuál es la fuerza a 6 unidades?
a) 10 N
b) 40 N
c) 5 N
d) 80 N

**Respuesta correcta: c) 5 N.**
*Retroalimentación:* al duplicar la distancia, la fuerza se divide por 2² = 4.

**Pregunta 7 (alternativas — mareas).** La marea se modela como h(t) = 1,5·sen((π/6)t) + 3 (m, t en horas). ¿Cuáles son la altura máxima, la mínima y el período?
a) 4,5 m; 1,5 m; 12 horas
b) 3 m; 1,5 m; 6 horas
c) 4,5 m; 0 m; 12 horas
d) 1,5 m; −1,5 m; 2π horas

**Respuesta correcta: a) 4,5 m; 1,5 m; 12 horas.**
*Retroalimentación:* máximo D + A, mínimo D − A, T = 2π/(π/6) = 12.

**Pregunta 8 (alternativas — construir modelo).** Un péndulo oscila entre −10 y 10 cm con un ciclo cada 4 s, partiendo de 0 hacia el lado positivo. ¿Qué modelo es adecuado?
a) x(t) = 10·sen(4t)
b) x(t) = 4·sen(10t)
c) x(t) = 10·cos((π/2)t)
d) x(t) = 10·sen((π/2)t)

**Respuesta correcta: d) x(t) = 10·sen((π/2)t).**
*Retroalimentación:* A = 10, D = 0, B = 2π/4 = π/2; parte en 0 y sube, por eso seno sin desfase (el coseno partiría en 10).

**Pregunta 9 (alternativas — variar el exponente).** ¿Qué afirmación sobre f(x) = x² y g(x) = x³ es correcta?
a) g siempre es mayor que f, para cualquier valor positivo de x
b) Para x > 1, g crece más rápido; para 0 < x < 1, g es menor que f
c) f siempre es mayor que g, porque el cuadrado crece más rápido
d) Son iguales para todo x, porque ambas son funciones potencia

**Respuesta correcta: b) Para x > 1, g crece más rápido; para 0 < x < 1, g es menor que f.**
*Retroalimentación:* en x = 4: f = 16 y g = 64; en x = 0,5: f = 0,25 y g = 0,125.

**Pregunta 10 (alternativas — identificar el exponente).** El volumen de cubos según su arista: L = 1 → 1; L = 2 → 8; L = 3 → 27; L = 4 → 64. ¿Qué función describe la relación?
a) f(L) = 3L
b) f(L) = L²
c) f(L) = L³
d) f(L) = 2ᴸ

**Respuesta correcta: c) f(L) = L³.**
*Retroalimentación:* 1³, 2³, 3³ y 4³ coinciden exactamente.

**Pregunta 11 (alternativas — coseno vs. seno).** ¿Cuál es la diferencia principal entre los modelos f(x)=A·sen(Bx) y g(x)=A·cos(Bx), ambos con el mismo valor medio D=0?
a) tienen distinta amplitud: el coseno alcanza valores más altos que el seno
b) tienen distinto período: el coseno completa su ciclo en la mitad del tiempo
c) representan el mismo tipo de oscilación, pero con distinto punto de partida (desfase)
d) el coseno no puede modelar fenómenos periódicos, porque comienza en su máximo

**Respuesta correcta: c).**
*Retroalimentación:* sen(x) parte en 0 (el valor medio) y sube; cos(x) parte en el valor máximo (A); ambas curvas tienen la misma forma, solo que una está desplazada horizontalmente respecto a la otra.

**Pregunta 12 (verdadero o falso).** Un modelo de potencia f(x)=a·xⁿ y un modelo exponencial g(x)=a·bˣ pueden dar el mismo valor en algunos puntos específicos, pero tienen la variable en distinta posición (base vs. exponente).

**Respuesta correcta: Verdadero.**
*Retroalimentación:* es un error común confundir ambos tipos de modelo por su forma "parecida"; la diferencia clave y definitoria es dónde está la variable: en la base (potencia) o en el exponente (exponencial), lo que produce comportamientos muy distintos a largo plazo.

**Pregunta 13 (alternativas — desfase).** La temperatura diaria es T(h) = 6·sen((π/12)(h − 9)) + 18. ¿A qué hora ocurre la máxima?
a) A las 15:00
b) A las 9:00
c) A las 12:00
d) A las 21:00

**Respuesta correcta: a) A las 15:00.**
*Retroalimentación:* el máximo del seno ocurre cuando (π/12)(h − 9) = π/2, es decir, h = 15.

**Pregunta 14 (alternativas — escalamiento).** El costo de una plancha cuadrada es C(L) = 25·L². Si se duplica el lado, ¿en qué factor aumenta el costo?
a) 2
b) 25
c) 50
d) 4

**Respuesta correcta: d) 4.**
*Retroalimentación:* C(2L) = 25·(2L)² = 4·C(L).

**Pregunta 15 (alternativas — elegir modelo).** ¿Qué modelos son adecuados para (1) las horas de luz solar en Santiago a lo largo del año y (2) una inversión a interés compuesto?
a) (1) exponencial creciente; (2) trigonométrico periódico
b) (1) trigonométrico periódico; (2) exponencial
c) Ambos lineales
d) (1) potencia; (2) trigonométrico periódico

**Respuesta correcta: b) (1) trigonométrico periódico; (2) exponencial.**
*Retroalimentación:* la luz solar se repite cada 12 meses; la inversión crece de forma acelerada sin oscilar.

**Pregunta 16 (alternativas — amplitud y valor medio).** ¿Entre qué valores oscilan f(x) = 2·sen(x) + 10 y g(x) = 5·sen(x) + 10, y cuál varía más?
a) f entre 5 y 15; g entre 8 y 12; f varía más
b) Ambos entre 8 y 12
c) f entre 8 y 12; g entre 5 y 15; g varía más
d) Ambos entre 10 y 15

**Respuesta correcta: c) f entre 8 y 12; g entre 5 y 15; g varía más.**
*Retroalimentación:* comparten el valor medio 10, pero g tiene mayor amplitud.

**Pregunta 17 (alternativas — datos reales).** La profundidad en un muelle cada 3 h es: 0 h → 2,0; 3 h → 3,2; 6 h → 2,0; 9 h → 0,8; 12 h → 2,0 m. ¿Es razonable un modelo trigonométrico y con qué parámetros?
a) Sí: valor medio ≈ 2,0 m, amplitud ≈ 1,2 m y período ≈ 12 h
b) No: los datos no se repiten
c) Sí: valor medio 3,2 m, amplitud 2,4 m y período 3 h
d) Sí: valor medio 0,8 m, amplitud 2 m y período 6 h exactas

**Respuesta correcta: a) Sí: valor medio ≈ 2,0 m, amplitud ≈ 1,2 m y período ≈ 12 h.**
*Retroalimentación:* los valores oscilan simétricamente en torno a 2,0 m, como una marea semidiurna.

**Pregunta 18 (alternativas — intensidad de sonido).** Con I(d) = 500/d², ¿a qué distancia la intensidad baja a 5?
a) 100 m
b) 50 m
c) 10 m
d) √5 m

**Respuesta correcta: c) 10 m.**
*Retroalimentación:* 500/d² = 5 → d² = 100.

---

## Eje: Probabilidad y Estadística

### OA 2 — Fundamentar decisiones con los modelos binomial y normal

Vas a **fundamentar decisiones en situaciones de incerteza**, a partir del **análisis crítico de datos estadísticos** y con base en los **modelos binomial y normal**: evaluando las distintas posibilidades de un experimento aleatorio para determinar su probabilidad, evaluando los alcances y límites de un argumento estadístico o probabilístico antes de confiar en él, y evaluando cuándo es pertinente usar el modelo binomial o el normal para interpretar una situación.

**¿Por qué importa?** Muchas decisiones importantes —desde si vale la pena vacunarse, hasta si confiar en una encuesta electoral, pasando por evaluar el riesgo de un examen médico— dependen de interpretar correctamente información probabilística y estadística. Este OA cierra tu formación en el eje con dos modelos muy usados: el **binomial**, para contar éxitos en experimentos con dos resultados posibles repetidos varias veces (por ejemplo, cuántos de 10 pacientes responden a un tratamiento), y el **normal**, para describir datos continuos que se agrupan en torno a un promedio con una forma de campana (por ejemplo, estaturas o puntajes de una prueba). Y, tan importante como saber calcular, es saber **cuestionar**: reconocer cuándo un argumento estadístico está bien fundamentado, y cuándo no.

**Modelo binomial:** describe experimentos con **n repeticiones independientes** de un ensayo con solo dos resultados posibles ("éxito" con probabilidad p, o "fracaso" con probabilidad 1−p). La probabilidad de obtener exactamente **k éxitos** en n ensayos es:

**P(X=k) = C(n,k) · pᵏ · (1−p)ⁿ⁻ᵏ**

donde C(n,k) = n!/(k!(n−k)!) es el número de combinaciones posibles de elegir k éxitos entre n ensayos.

**Media y varianza del modelo binomial:** μ = n·p ; σ² = n·p·(1−p).

**Modelo normal:** describe **datos continuos** que se distribuyen simétricamente en forma de campana alrededor de su media μ, con una dispersión dada por su desviación estándar σ.

**Regla empírica (68-95-99,7):** en una distribución normal, aproximadamente:
- el **68%** de los datos está dentro de 1 desviación estándar de la media (μ±σ)
- el **95%** está dentro de 2 desviaciones estándar (μ±2σ)
- el **99,7%** está dentro de 3 desviaciones estándar (μ±3σ)

**¿Cuándo usar binomial y cuándo usar normal?**

| Usa el modelo... | Cuando... |
|---|---|
| **Binomial** | los datos son **discretos** (se cuentan: número de éxitos), hay un número fijo n de ensayos independientes, y cada ensayo tiene solo dos resultados posibles |
| **Normal** | los datos son **continuos** (se miden: tiempo, altura, peso, puntaje), y se agrupan simétricamente alrededor de un promedio |

**Evaluar alcances y límites de un argumento estadístico:** antes de aceptar una conclusión basada en datos, conviene preguntarse: ¿el tamaño de la muestra es suficiente? ¿la muestra representa bien a la población de interés, o tiene algún sesgo? ¿se está confundiendo correlación con causalidad? ¿el modelo elegido (binomial o normal) es realmente adecuado para estos datos?

#### Ejemplos resueltos

**Ejemplo 1 — Modelo binomial**

Una vacuna tiene una efectividad del 80% (probabilidad de generar inmunidad en cada persona vacunada). Si se vacunan 5 personas, ¿cuál es la probabilidad de que exactamente 4 de ellas desarrollen inmunidad?

n=5, p=0,8, k=4. C(5,4)=5. P(X=4) = 5×(0,8)⁴×(0,2)¹ = 5×0,4096×0,2 = **0,4096 (40,96%)**.

**Ejemplo 2 — Modelo normal y regla empírica**

Los puntajes de una prueba estandarizada siguen una distribución normal con media μ=500 y desviación estándar σ=100. ¿Qué porcentaje aproximado de estudiantes obtiene un puntaje entre 400 y 600?

400 = μ−σ y 600 = μ+σ, es decir, el intervalo [400,600] corresponde exactamente a μ±1σ. Según la regla empírica, aproximadamente el **68%** de los estudiantes obtiene un puntaje en ese rango.

**Ejemplo 3 — Elegir el modelo adecuado**

Un investigador tiene dos conjuntos de datos: (A) el número de caras obtenidas al lanzar una moneda 20 veces, repetido en muchos experimentos; (B) el peso en gramos de 500 manzanas cosechadas en un huerto. ¿Qué modelo es más adecuado para cada uno?

(A) corresponde al modelo **binomial**: hay un número fijo de ensayos (20 lanzamientos), cada uno con dos resultados posibles (cara o sello), y se cuenta el número de éxitos (caras). (B) corresponde al modelo **normal**: el peso es una variable continua que típicamente se distribuye de forma simétrica alrededor de un peso promedio, con manzanas más pesadas o más livianas siendo cada vez menos frecuentes mientras más se alejan del promedio.

#### Preguntas de autoevaluación

**Pregunta 1 (alternativas).** ¿Cuál de las siguientes situaciones se modela mejor con una distribución binomial?
a) la estatura de 100 estudiantes de un curso
b) el número de veces que sale "6" al lanzar un dado 10 veces
c) el tiempo que demora un estudiante en resolver una prueba
d) el peso de 50 mochilas escolares

**Respuesta correcta: b).**
*Retroalimentación:* hay un número fijo de ensayos (10 lanzamientos), cada uno con dos resultados posibles ("sale 6" o "no sale 6"), y se cuenta un número de éxitos: exactamente las condiciones de un modelo binomial. Las otras opciones son variables continuas, propias de un modelo normal.

**Pregunta 2 (verdadero o falso).** En una distribución normal, aproximadamente el 95% de los datos se encuentra dentro de 2 desviaciones estándar de la media.

**Respuesta correcta: Verdadero.**
*Retroalimentación:* esta es la regla empírica 68-95-99,7: el 68% está dentro de 1σ, el 95% dentro de 2σ, y el 99,7% dentro de 3σ de la media.

**Pregunta 3 (calcular).** En un modelo binomial con n=8 y p=0,5, ¿cuál es el valor esperado (media) del número de éxitos?
a) 8
b) 0,5
c) 4
d) 2

**Respuesta correcta: c) 4.**
*Retroalimentación:* la media de un modelo binomial es μ=n×p = 8×0,5 = 4.

**Pregunta 4 (alternativas — completar).** El modelo binomial se aplica a variables ___ y el normal a variables ___.
a) continuas; discretas
b) discretas; continuas
c) cualitativas; nominales
d) aleatorias; fijas

**Respuesta correcta: b) discretas; continuas.**
*Retroalimentación:* el binomial cuenta resultados y el normal mide en una escala continua.

**Pregunta 5 (alternativas — probabilidad binomial).** Un vendedor cierra una venta con probabilidad 0,3 por visita. En 4 visitas, ¿cuál es la probabilidad de cerrar exactamente 2?
a) 0,09
b) 0,6
c) ≈ 0,2646
d) ≈ 0,0441

**Respuesta correcta: c) ≈ 0,2646.**
*Retroalimentación:* C(4,2) · 0,3² · 0,7² = 6 · 0,09 · 0,49; 0,0441 olvida el coeficiente C(4,2).

**Pregunta 6 (alternativas — media y desviación binomial).** La probabilidad de defecto es 0,05 y se revisan 200 productos. ¿Cuántos defectuosos se esperan y cuál es la desviación estándar?
a) 10 y ≈ 3,08
b) 10 y 9,5
c) 5 y ≈ 2,24
d) 190 y ≈ 3,08

**Respuesta correcta: a) 10 y ≈ 3,08.**
*Retroalimentación:* μ = 200 · 0,05; σ = √(200 · 0,05 · 0,95) = √9,5 (9,5 es la varianza).

**Pregunta 7 (alternativas — regla empírica).** El tiempo de reacción es normal con μ = 0,8 s y σ = 0,1 s. ¿Entre qué valores está aproximadamente el 95% de los conductores?
a) Entre 0,7 y 0,9 s
b) Entre 0,5 y 1,1 s
c) Entre 0 y 0,8 s
d) Entre 0,6 y 1,0 s

**Respuesta correcta: d) Entre 0,6 y 1,0 s.**
*Retroalimentación:* μ ± 2σ; 0,7–0,9 corresponde a μ ± σ (≈ 68%).

**Pregunta 8 (alternativas — elegir modelo).** En un ensayo con 50 pacientes se estudia (1) si cada uno presenta o no un efecto secundario y (2) su presión arterial sistólica. ¿Qué modelos corresponden?
a) (1) normal; (2) binomial
b) (1) binomial; (2) normal
c) Ambos binomiales
d) Ambos normales

**Respuesta correcta: b) (1) binomial; (2) normal.**
*Retroalimentación:* (1) es un conteo de resultados binarios; (2) es una variable continua.

**Pregunta 9 (alternativas — probabilidad binomial).** Un estudiante responde al azar 5 preguntas de verdadero o falso. ¿Cuál es la probabilidad de acertar las 5?
a) 0,5
b) 0,1
c) 0,03125
d) 0,25

**Respuesta correcta: c) 0,03125.**
*Retroalimentación:* (0,5)⁵ = 1/32.

**Pregunta 10 (verdadero o falso — límites de un argumento).** Una encuesta a 30 personas en un centro comercial de un solo barrio de Santiago concluye que "el 70% de los chilenos prefiere el producto X". Esta conclusión está bien fundamentada.

**Respuesta correcta: Falso.**
*Retroalimentación:* la muestra es pequeña (30 personas) y, sobre todo, **no representa** a la población de interés ("los chilenos"): fue tomada en un solo lugar y con un perfil probablemente muy específico de personas; generalizar sus resultados a todo el país es un error de alcance del argumento estadístico.

**Pregunta 11 (alternativas — corvínculo y causalidad).** En distintas ciudades hay una fuerte correlación entre el número de heladerías y de ahogamientos en piscinas. ¿Se puede concluir que las heladerías causan ahogamientos?
a) No: ambas variables dependen de una tercera, la temperatura
b) Sí: una correlación fuerte prueba causalidad
c) Sí: comer helado antes de nadar produce ahogamientos
d) No: no existe ninguna correlación entre ambas variables

**Respuesta correcta: a) No: ambas variables dependen de una tercera, la temperatura.**
*Retroalimentación:* correlación no implica causalidad cuando hay una variable oculta.

**Pregunta 12 (alternativas — pertinencia del modelo).** Un analista usa un modelo normal para el número de defectuosos en lotes de 20 unidades con probabilidad fija de defecto. ¿Es pertinente?
a) Sí: el número de defectuosos es una variable continua con distribución simétrica
b) Sí: el modelo normal sirve para cualquier conteo pequeño, como 20 unidades
c) No: debería usarse un modelo trigonométrico
d) No: es una variable discreta con n fijo y p fija, condiciones del modelo binomial

**Respuesta correcta: d) No: es una variable discreta con n fijo y p fija, condiciones del modelo binomial.**
*Retroalimentación:* con n grande el binomial puede aproximarse por el normal, pero esa es una decisión adicional.

**Pregunta 13 (alternativas — comparar experimentos).** Con 10 pacientes por grupo, el tratamiento A tiene p = 0,6 y el B, p = 0,75. ¿Qué número promedio de éxitos tiene cada uno?
a) A: 7,5; B: 6
b) A: 6; B: 7,5
c) A: 0,6; B: 0,75
d) Ambos 10

**Respuesta correcta: b) A: 6; B: 7,5.**
*Retroalimentación:* μ = n · p.

**Pregunta 14 (alternativas — límites de una encuesta).** Una encuesta telefónica solo contacta a mayores de 60 años y generaliza su resultado a "toda la población". ¿Qué límite tiene?
a) Ninguno: cualquier muestra grande representa a toda la población
b) Que hubo demasiados encuestados y eso aumenta el margen de error
c) Sesgo de muestra: la muestra no es representativa de toda la población votante
d) Que las encuestas telefónicas son ilegales si no se avisa con anticipación

**Respuesta correcta: c) Sesgo de muestra: la muestra no es representativa de toda la población votante.**
*Retroalimentación:* generalizar a toda la población no está fundamentado.

**Pregunta 15 (alternativas — al menos uno).** La probabilidad de retraso de un vuelo es 0,1. En 3 vuelos independientes, ¿cuál es la probabilidad de que al menos uno se retrase?
a) 0,271
b) 0,3
c) 0,001
d) 0,729

**Respuesta correcta: a) 0,271.**
*Retroalimentación:* 1 − (0,9)³ = 1 − 0,729; 0,729 es la probabilidad de que ninguno se retrase.

**Pregunta 16 (alternativas — dispersión y modelo normal).** Dos envasadoras tienen media 1.000 g; la 1 tiene σ = 5 g y la 2, σ = 20 g. Si se rechazan bolsas bajo 970 g, ¿cuál generará más rechazos?
a) La 1: 970 g está a 6σ bajo la media, más cerca que en la 2
b) Ambas igual, porque tienen la misma media de 1.000 g
c) Ninguna rechaza bolsas
d) La 2: 970 g está a 1,5σ bajo la media, frente a 6σ en la 1

**Respuesta correcta: d) La 2: 970 g está a 1,5σ bajo la media, frente a 6σ en la 1.**
*Retroalimentación:* a mayor dispersión, más probable que un valor se aleje tanto de la media.

**Pregunta 17 (varias correctas — evaluar un argumento).** "Un estudio de 15 personas demuestra que el suplemento X mejora la memoria." ¿Qué preguntas conviene hacerse? Marca **todas** las correctas.
a) ¿Es suficiente una muestra de 15 personas?
b) ¿Hubo un grupo de control?
c) ¿Se controlaron otras variables, como el sueño o la dieta?
d) ¿De qué color es la caja del suplemento?

**Respuesta correcta: a, b y c.**
*Retroalimentación:* también conviene preguntar si el resultado fue estadísticamente significativo.

**Pregunta 18 (alternativas — binomial con complemento).** Cada artículo tiene probabilidad 0,02 de ser defectuoso. En una muestra de 5, ¿cuál es la probabilidad de ninguno defectuoso y de al menos uno?
a) ≈ 9,61% y ≈ 90,39%
b) ≈ 90,39% y ≈ 9,61%
c) 98% y 2%
d) 10% y 90%

**Respuesta correcta: b) ≈ 90,39% y ≈ 9,61%.**
*Retroalimentación:* (0,98)⁵ ≈ 0,9039 y su complemento 0,0961.

---

## Glosario

- **Interés simple:** interés calculado siempre sobre el capital inicial; el monto crece linealmente en el tiempo (M=C(1+i·t)).
- **Interés compuesto:** interés calculado sobre el capital más los intereses ya acumulados; el monto crece exponencialmente en el tiempo (M=C(1+i)ᵗ).
- **Tasa nominal anual:** tasa de interés anunciada para un año, sin considerar el efecto de la frecuencia de capitalización.
- **Tasa efectiva anual (TEA):** tasa de interés que realmente se paga o gana en un año, considerando el efecto de capitalizar varias veces (TEA=(1+i_nom/n)ⁿ−1).
- **IPC (Índice de Precios al Consumidor):** indicador que mide la variación porcentual promedio de los precios de una canasta de bienes y servicios; su variación es la medida usual de la inflación.
- **UF (Unidad de Fomento):** unidad de cuenta chilena reajustada diariamente según el IPC, usada en contratos de largo plazo como créditos hipotecarios.
- **CAE (Carga Anual Equivalente):** tasa anual que resume el costo total real de un crédito, incluyendo intereses y otros cargos, para comparar ofertas de forma justa.
- **Función potencia:** función de la forma f(x)=a·xⁿ, con n entero (positivo o negativo); a diferencia de la exponencial, la variable está en la base, no en el exponente.
- **Ley del inverso del cuadrado:** relación de potencia con exponente −2, donde una magnitud (como luz, sonido o fuerza gravitacional) decrece según el cuadrado de la distancia.
- **Función periódica:** función cuyos valores se repiten en ciclos regulares; las funciones seno y coseno son los ejemplos fundamentales.
- **Amplitud (A):** en un modelo A·sen(B(x−C))+D, la distancia entre el valor medio y los valores máximo/mínimo de la función.
- **Período (T):** duración de un ciclo completo de una función periódica; T=2π/B (en radianes).
- **Desfase (C):** desplazamiento horizontal de un modelo periódico, que determina en qué punto comienza el ciclo.
- **Valor medio (D):** valor central alrededor del cual oscila una función periódica.
- **Modelo binomial:** modelo de probabilidad para variables discretas que cuentan el número de éxitos en n ensayos independientes con dos resultados posibles cada uno; P(X=k)=C(n,k)pᵏ(1−p)ⁿ⁻ᵏ.
- **Modelo normal:** modelo de probabilidad para variables continuas que se distribuyen simétricamente en forma de campana alrededor de una media, con dispersión dada por su desviación estándar.
- **Regla empírica (68-95-99,7):** en una distribución normal, el 68% de los datos está dentro de 1 desviación estándar de la media, el 95% dentro de 2, y el 99,7% dentro de 3.
- **Sesgo de muestra:** distorsión que ocurre cuando la muestra usada en un estudio no representa adecuadamente a la población sobre la que se quiere concluir.
- **Correlación sin causalidad:** situación en que dos variables se mueven juntas (correlacionan) sin que una sea la causa directa de la otra, muchas veces por la influencia de una tercera variable.
