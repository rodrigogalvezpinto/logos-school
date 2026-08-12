---
título: Matemática — 4° Medio
asignatura: Matemática
curso: 4° Medio
fuente curricular: Bases Curriculares, Decreto 193/2019 "Plan Común" (Mineduc/UCE) — temario oficial del Examen Libre de Validación de Estudios
última actualización: 2026-08-10
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
a) el interés simple se cobra solo una vez, y el compuesto todos los meses
b) el interés compuesto se calcula sobre el capital más los intereses ya acumulados; el simple, siempre sobre el capital inicial
c) el interés simple es siempre mayor que el compuesto
d) no hay diferencia, son dos nombres para lo mismo

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

**Pregunta 4 (completar).** La UF es una unidad de cuenta que se reajusta según la variación del ______, y se usa principalmente en contratos de ______ plazo, como los créditos hipotecarios.

**Respuesta esperada:** **IPC** (índice de precios al consumidor); **largo** plazo.
*Retroalimentación:* al estar indexada a la inflación, la UF protege el valor real del dinero en contratos que duran años, evitando que la inflación erosione lo pactado.

**Pregunta 5 (desarrollo — interés compuesto).** Un ahorro de $2.000.000 se deposita a una tasa de interés compuesto del 4% anual. Calcula el monto acumulado después de 6 años.

**Respuesta esperada:** M = 2.000.000×(1,04)⁶ ≈ 2.000.000×1,2653 ≈ **$2.530.600**.
*Retroalimentación:* con interés compuesto, cada año la base sobre la que se calcula el 4% crece, por lo que el monto no aumenta en una cantidad fija de pesos cada año.

**Pregunta 6 (desarrollo — tasa efectiva).** Una cuenta de ahorro ofrece una tasa nominal anual del 12%, capitalizada trimestralmente (n=4). Calcula la tasa efectiva anual.

**Respuesta esperada:** TEA = (1+0,12/4)⁴−1 = (1,03)⁴−1 ≈ 1,1255−1 = **0,1255 ≈ 12,55%**.
*Retroalimentación:* aunque la tasa nominal es 12%, capitalizar 4 veces al año hace que el rendimiento real (efectivo) sea levemente mayor.

**Pregunta 7 (problema en contexto — IPC).** En enero, un kilo de pan cuesta $1.200. Si el IPC acumulado en el año fue de 5%, ¿cuál es el precio estimado del mismo kilo de pan en diciembre, si su precio varió igual que el IPC promedio?

**Respuesta esperada:** 1.200×(1,05) = **$1.260**.
*Retroalimentación:* el IPC resume la variación promedio de precios de toda una canasta de bienes; un producto específico puede variar más, menos, o distinto que el promedio, pero esta estimación asume que sigue exactamente la variación del IPC.

**Pregunta 8 (problema en contexto — UF).** Un arriendo se pacta en 15 UF mensuales. Si el valor de la UF ese día es $38.500, ¿cuánto se debe pagar ese mes en pesos?

**Respuesta esperada:** 15×38.500 = **$577.500**.
*Retroalimentación:* para convertir un monto en UF a pesos, se multiplica por el valor de la UF vigente ese día; por eso un arriendo pactado en UF varía levemente en pesos de un mes a otro, aunque su valor en UF se mantenga fijo.

**Pregunta 9 (comparar — CAE).** Un estudiante compara dos créditos de igual monto y plazo: el Crédito X tiene una tasa de interés anunciada del 10% pero un CAE de 15%; el Crédito Y tiene una tasa anunciada del 12% y un CAE de 13%. ¿Cuál conviene más, y por qué no basta con mirar solo la tasa anunciada?

**Respuesta esperada:** conviene el **Crédito Y**, porque su CAE (13%) es menor que el del Crédito X (15%). No basta con mirar la tasa anunciada porque esta no incluye comisiones, seguros u otros cargos asociados al crédito; el CAE sí los incorpora, por lo que refleja mejor el costo real total.
*Retroalimentación:* comparar créditos únicamente por su tasa de interés nominal puede llevar a decisiones equivocadas; el CAE existe precisamente para hacer comparables ofertas que estructuran sus costos de forma distinta.

**Pregunta 10 (desarrollo — evaluar alternativas de ahorro).** Un joven tiene $300.000 para ahorrar durante 2 años y debe elegir entre la Opción A (interés simple del 8% anual) y la Opción B (interés compuesto del 7% anual). Calcula el monto final de cada una y determina cuál conviene.

**Respuesta esperada:** A: M = 300.000×(1+0,08×2) = 300.000×1,16 = **$348.000**. B: M = 300.000×(1,07)² = 300.000×1,1449 ≈ **$343.470**. **Conviene la Opción A**, porque a pesar de tener una tasa menor a la vista, el plazo (2 años) es demasiado corto para que el interés compuesto de la Opción B alcance a superar al simple con mayor tasa.
*Retroalimentación:* el interés compuesto solo supera claramente al simple en plazos largos; en plazos cortos, una tasa simple más alta puede ser más conveniente. Por eso siempre conviene calcular ambos casos concretos, no asumir cuál es "mejor" en abstracto.

**Pregunta 11 (leer datos — tabla de créditos).** Un estudiante recibe esta información de tres créditos para financiar un curso de $1.500.000:

| Crédito | Tasa anunciada | CAE |
|---|---|---|
| P | 9% | 11,2% |
| Q | 10% | 10,5% |
| R | 8,5% | 12,0% |

¿Cuál crédito conviene elegir, y cuál sería un error común al leer esta tabla?

**Respuesta esperada:** conviene el **Crédito Q**, porque tiene el menor CAE (10,5%), aunque no tenga la tasa anunciada más baja. Un **error común** sería elegir el Crédito R por tener la tasa anunciada más baja (8,5%), sin notar que su CAE —el costo real total— es en realidad el más alto de los tres.
*Retroalimentación:* esta pregunta ilustra por qué el CAE es el indicador que se debe comparar al decidir, y no la tasa de interés anunciada, que muchas veces subestima el costo real de un crédito.

**Pregunta 12 (calcular — ajustar el plazo).** Un capital de $600.000 se invierte a interés compuesto del 5% anual. ¿Cuánto tiempo aproximado (en años enteros) se necesita para que el monto supere $700.000?

**Respuesta esperada:** probando: t=1 → 630.000; t=2 → 661.500; t=3 → 694.575; t=4 → 729.304. Se necesitan **4 años** para superar los $700.000.
*Retroalimentación:* "ajustar" un modelo financiero muchas veces significa evaluarlo para distintos valores de un parámetro (aquí, el tiempo) hasta encontrar el que cumple la condición buscada.

**Pregunta 13 (verdadero o falso).** El CAE permite comparar el costo real de dos créditos, incluso si tienen plazos distintos, porque expresa el costo como una tasa anual equivalente.

**Respuesta correcta: Verdadero.**
*Retroalimentación:* al expresarse como una tasa anual, el CAE permite comparar créditos aunque difieran en plazo, monto o estructura de cobros, algo que la tasa de interés simple anunciada no siempre permite hacer de forma directa.

**Pregunta 14 (problema no rutinario — inflación y poder adquisitivo).** El sueldo de una persona era de $500.000 mensuales hace un año y hoy es de $520.000. En ese mismo período, el IPC acumulado fue de 6%. ¿Aumentó, se mantuvo, o disminuyó el poder adquisitivo real de esta persona? Justifica con un cálculo.

**Respuesta esperada:** el sueldo aumentó un 520.000/500.000 − 1 = **4%**, mientras que los precios (IPC) aumentaron un **6%**. Como el aumento del sueldo (4%) fue **menor** que la inflación (6%), el poder adquisitivo real **disminuyó**: con el nuevo sueldo se pueden comprar menos bienes y servicios que antes, en términos reales.
*Retroalimentación:* comparar el aumento nominal de un sueldo con la inflación del mismo período es la forma correcta de saber si una persona realmente "ganó" poder de compra o no; un aumento nominal no siempre es un aumento real.

**Pregunta 15 (desarrollo — comparar tasa nominal vs. efectiva de dos ofertas).** Dos bancos ofrecen depósitos a plazo con tasa nominal anual de 10%: el Banco A capitaliza mensualmente (n=12) y el Banco B capitaliza semestralmente (n=2). ¿Cuál conviene más para depositar dinero, y por qué?

**Respuesta esperada:** Banco A: TEA = (1+0,10/12)¹²−1 ≈ 10,47%. Banco B: TEA = (1+0,10/2)²−1 = (1,05)²−1 = 10,25%. **Conviene el Banco A**, porque su capitalización más frecuente genera una tasa efectiva anual mayor, aunque ambos anuncien la misma tasa nominal.
*Retroalimentación:* al ahorrar (a diferencia de al pedir un crédito), una mayor frecuencia de capitalización beneficia a quien deposita el dinero, porque los intereses empiezan a generar nuevos intereses antes.

**Pregunta 16 (problema en contexto — evaluar decisión de crédito hipotecario).** Una familia evalúa un crédito hipotecario en UF, con una tasa de interés anual de 4,5% sobre un monto de 2.000 UF a 20 años. Si el valor de la UF hoy es $38.000 y se espera que crezca aproximadamente con la inflación, ¿por qué se dice que este tipo de crédito "traspasa" el riesgo de inflación al deudor en lugar de al banco?

**Respuesta esperada:** porque la deuda está expresada en **UF**, que se reajusta automáticamente según el IPC. Si la inflación sube, el valor en pesos de la UF (y por lo tanto de la deuda pendiente) también sube, independientemente de lo que gane el deudor; es el deudor quien asume ese riesgo, mientras que el banco mantiene protegido el valor real de lo prestado.
*Retroalimentación:* entender que un crédito en UF no es "más barato" solo porque su tasa de interés nominal parece baja es clave: hay que sumar el efecto del reajuste por inflación para conocer el costo real a lo largo de un plazo largo, como 20 años.

**Pregunta 17 (calcular — comparar simple y compuesto a mayor plazo).** Repite el cálculo del Ejemplo 1 (capital $500.000, tasa 6% anual) pero para un plazo de 15 años. Calcula ambos montos y compara la diferencia con la obtenida a 3 años.

**Respuesta esperada:** Simple: M = 500.000×(1+0,06×15) = 500.000×1,9 = **$950.000**. Compuesto: M = 500.000×(1,06)¹⁵ ≈ 500.000×2,3966 ≈ **$1.198.300**. La diferencia ahora es de casi **$248.300**, mucho mayor que los ≈$5.508 obtenidos a 3 años.
*Retroalimentación:* la brecha entre interés simple y compuesto crece de forma acelerada con el tiempo, porque el compuesto genera intereses sobre intereses; en plazos largos (como un crédito hipotecario a 20 o 30 años), esa diferencia es enorme.

**Pregunta 18 (problema no rutinario — fundamentar una decisión completa).** Un joven de 18 años recibe $1.000.000 y debe decidir entre: (A) gastarlo ahora, (B) ahorrarlo 5 años a interés compuesto del 6% anual, o (C) invertirlo en un fondo con retorno esperado de 9% anual pero con riesgo de pérdida. Redacta un argumento breve (2-3 ideas) sobre qué información adicional necesitaría para fundamentar esta decisión, más allá de solo comparar las tasas.

**Respuesta esperada (abierta, ejemplo de buena respuesta):** además de las tasas, se necesitaría saber: (1) si el joven tiene alguna necesidad de liquidez a corto plazo (gastar ahora podría ser necesario, o ahorrar podría implicar no poder usar el dinero si surge una emergencia); (2) el nivel de riesgo que está dispuesto a asumir, ya que la opción C tiene mayor retorno esperado pero también posibilidad de pérdida, a diferencia de B; (3) el efecto de la inflación proyectada sobre el poder adquisitivo real de cada alternativa en 5 años.
*Retroalimentación:* fundamentar una decisión financiera no es solo comparar números: implica considerar el contexto personal (necesidad de liquidez), la tolerancia al riesgo, y el efecto de la inflación sobre el resultado final; esta es exactamente la habilidad que evalúa este Objetivo de Aprendizaje.

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
c) 108
d) 64

**Respuesta correcta: c) 108.**
*Retroalimentación:* f(3) = 4×3³ = 4×27 = 108.

**Pregunta 4 (completar).** En el modelo f(x) = A·sen(B(x−C))+D, el parámetro A se llama ______ y determina cuánto se aleja el valor de la función respecto al ______, representado por el parámetro D.

**Respuesta esperada:** **amplitud**; **valor medio** (o valor central).
*Retroalimentación:* la amplitud A indica el "alcance" de la oscilación hacia arriba y hacia abajo desde el valor medio D; el valor de la función siempre queda entre D−A y D+A.

**Pregunta 5 (desarrollo — período).** Un modelo periódico está dado por f(x) = 5·sen(2x). Calcula su período.

**Respuesta esperada:** T = 2π/B = 2π/2 = **π** (aproximadamente 3,14 unidades de x por ciclo).
*Retroalimentación:* mientras mayor es B, más rápido se repite el ciclo, es decir, menor es el período; ambos son inversamente proporcionales.

**Pregunta 6 (desarrollo — potencia negativa en contexto).** La fuerza de atracción gravitacional entre dos objetos sigue aproximadamente F(d) = k/d², donde d es la distancia entre ellos. Si a una distancia de 3 unidades la fuerza es de 20 N, ¿cuál es aproximadamente la fuerza a una distancia de 6 unidades (el doble)?

**Respuesta esperada:** al duplicar la distancia, la fuerza se divide por 2²=4 (por el exponente −2): F ≈ 20/4 = **5 N**.
*Retroalimentación:* en un modelo con exponente −2, duplicar la variable independiente no reduce el resultado a la mitad, sino a un cuarto; esta es la conocida "ley del inverso del cuadrado", presente en luz, sonido y gravedad.

**Pregunta 7 (problema en contexto — mareas).** La altura de la marea en una caleta chilena se modela como h(t) = 1,5·sen((π/6)t) + 3 (metros, t en horas desde la medianoche). Calcula la altura máxima, la altura mínima, y el período del ciclo de mareas.

**Respuesta esperada:** altura máxima = D+A = 3+1,5 = **4,5 m**; altura mínima = D−A = 3−1,5 = **1,5 m**; período T = 2π/(π/6) = **12 horas**.
*Retroalimentación:* en un modelo A·sen(Bt)+D, el máximo y el mínimo se obtienen sumando y restando la amplitud al valor medio, sin necesidad de evaluar la función; el período se calcula directamente de B.

**Pregunta 8 (desarrollo — construir modelo desde datos).** Un péndulo oscila de modo que su posición horizontal x(t) (cm) varía entre −10 cm y 10 cm, completando un ciclo cada 4 segundos, comenzando en x=0 y moviéndose inicialmente hacia el lado positivo. Escribe un modelo trigonométrico x(t) adecuado.

**Respuesta esperada:** amplitud A=10; valor medio D=0 (oscila simétricamente); período T=4, por lo tanto B=2π/T=2π/4=π/2; como parte en 0 y sube, se usa seno sin desfase: **x(t) = 10·sen((π/2)t)**.
*Retroalimentación:* construir un modelo periódico consiste en "leer" del enunciado los cuatro parámetros —amplitud (extensión de la oscilación), valor medio (centro), período (duración de un ciclo, que da B), y desfase (punto de partida, que decide entre seno o coseno y si hay corrimiento horizontal)—.

**Pregunta 9 (comparar — variar el exponente).** Compara los modelos f(x)=x² y g(x)=x³ para valores de x mayores que 1. ¿Cuál crece más rápido a medida que x aumenta, y qué ocurre para valores de x entre 0 y 1?

**Respuesta esperada:** para **x>1**, g(x)=x³ **crece más rápido** que f(x)=x² (por ejemplo, en x=4: f=16, g=64). Sin embargo, para **0<x<1**, ocurre lo contrario: g(x)=x³ es **menor** que f(x)=x² (por ejemplo, en x=0,5: f=0,25, g=0,125), porque multiplicar un número entre 0 y 1 por sí mismo una vez más lo hace aún más pequeño.
*Retroalimentación:* comparar exponentes no tiene una respuesta única para "todo x": el comportamiento relativo entre dos funciones potencia puede invertirse según si x es mayor o menor que 1, un punto que suele generar errores si no se verifica con casos concretos.

**Pregunta 10 (leer datos — identificar el exponente).** Una tabla muestra cómo varía el volumen V de una serie de cubos según la longitud L de su arista: L=1→V=1; L=2→V=8; L=3→V=27; L=4→V=64. ¿Qué función potencia f(L)=a·Lⁿ describe esta relación?

**Respuesta esperada:** los valores corresponden exactamente a L³ (1³=1, 2³=8, 3³=27, 4³=64), por lo tanto **f(L) = L³** (con a=1, n=3).
*Retroalimentación:* reconocer el exponente n a partir de una tabla se puede hacer probando si los valores corresponden a elevar la variable independiente al cuadrado, al cubo, u otra potencia; en este caso corresponde exactamente a la fórmula del volumen de un cubo.

**Pregunta 11 (alternativas — coseno vs. seno).** ¿Cuál es la diferencia principal entre los modelos f(x)=A·sen(Bx) y g(x)=A·cos(Bx), ambos con el mismo valor medio D=0?
a) tienen distinta amplitud
b) tienen distinto período
c) representan el mismo tipo de oscilación, pero con distinto punto de partida (desfase)
d) el coseno no puede modelar fenómenos periódicos

**Respuesta correcta: c).**
*Retroalimentación:* sen(x) parte en 0 (el valor medio) y sube; cos(x) parte en el valor máximo (A); ambas curvas tienen la misma forma, solo que una está desplazada horizontalmente respecto a la otra.

**Pregunta 12 (verdadero o falso).** Un modelo de potencia f(x)=a·xⁿ y un modelo exponencial g(x)=a·bˣ pueden dar el mismo valor en algunos puntos específicos, pero tienen la variable en distinta posición (base vs. exponente).

**Respuesta correcta: Verdadero.**
*Retroalimentación:* es un error común confundir ambos tipos de modelo por su forma "parecida"; la diferencia clave y definitoria es dónde está la variable: en la base (potencia) o en el exponente (exponencial), lo que produce comportamientos muy distintos a largo plazo.

**Pregunta 13 (calcular — desfase).** Un modelo de temperatura diaria es T(h) = 6·sen((π/12)(h−9)) + 18 (°C, h=hora del día, 0 a 24). ¿A qué hora ocurre aproximadamente la temperatura máxima?

**Respuesta esperada:** el máximo de sen ocurre cuando su argumento es π/2, es decir cuando (π/12)(h−9) = π/2 → (h−9)=6 → **h=15 (15:00 horas, 3 PM)**.
*Retroalimentación:* el desfase C (aquí, 9) desplaza horizontalmente el ciclo completo; encontrar el máximo requiere ubicar cuándo el argumento del seno alcanza π/2 (donde sen vale 1), no simplemente leer el valor de C directamente.

**Pregunta 14 (desarrollo — potencia y escalamiento).** El costo de fabricar una plancha de metal cuadrada de lado L sigue el modelo C(L) = 25·L² (en miles de pesos). Si se decide fabricar una plancha con el doble de lado, ¿en qué factor aumenta el costo? Justifica sin calcular valores específicos.

**Respuesta esperada:** el costo aumenta en un factor de **4**, porque C(2L) = 25×(2L)² = 25×4L² = 4×(25L²) = 4×C(L); al duplicar la variable de un modelo de potencia con exponente 2, el resultado se multiplica por 2²=4.
*Retroalimentación:* en un modelo de potencia f(x)=a·xⁿ, multiplicar x por un factor k multiplica el resultado por kⁿ; esta propiedad permite razonar sobre cómo cambia un modelo sin tener que recalcular todo desde cero.

**Pregunta 15 (problema en contexto — comparar modelo periódico con no periódico).** Un analista debe elegir un modelo para dos situaciones: (1) el número de horas de luz solar en Santiago a lo largo del año, y (2) el crecimiento de una inversión a interés compuesto. ¿Qué tipo de modelo (potencia, exponencial, o trigonométrico periódico) es más adecuado para cada una, y por qué?

**Respuesta esperada:** para (1), horas de luz solar a lo largo del año, corresponde un modelo **trigonométrico periódico** (seno o coseno), porque el fenómeno se repite cíclicamente cada 12 meses (más horas de luz en verano, menos en invierno, y vuelve a repetirse). Para (2), el crecimiento de una inversión a interés compuesto, corresponde un modelo **exponencial**, porque el monto no oscila, sino que crece indefinidamente y de forma acelerada mientras más tiempo pasa.
*Retroalimentación:* reconocer si un fenómeno se repite en ciclos (periódico) o crece/decrece sin repetirse (exponencial o potencia) es el primer paso —y el más importante— para elegir correctamente el tipo de modelo matemático a aplicar.

**Pregunta 16 (desarrollo — variar amplitud y valor medio).** Compara los modelos f(x)=2·sen(x)+10 y g(x)=5·sen(x)+10. Sin graficar, indica entre qué valores oscila cada uno y cuál tiene mayor variación.

**Respuesta esperada:** f(x) oscila entre 10−2=**8** y 10+2=**12**. g(x) oscila entre 10−5=**5** y 10+5=**15**. **g(x) tiene mayor variación** (rango de 10 unidades, entre 5 y 15) que f(x) (rango de 4 unidades, entre 8 y 12), porque su amplitud (5) es mayor que la de f (2), aunque ambos compartan el mismo valor medio (10).
*Retroalimentación:* la amplitud es el parámetro que controla directamente cuánto se "abre" la oscilación alrededor del valor medio; dos modelos pueden compartir el mismo centro y diferir mucho en su rango de variación.

**Pregunta 17 (problema no rutinario — construir y comparar con datos reales).** Un estudiante registra la profundidad del agua en un muelle cada 3 horas durante un día: 0h→2,0 m; 3h→3,2 m; 6h→2,0 m; 9h→0,8 m; 12h→2,0 m. ¿Es razonable modelar estos datos con una función trigonométrica? Estima la amplitud, el valor medio y el período aproximado.

**Respuesta esperada:** **sí es razonable**, porque los valores suben y bajan de forma simétrica alrededor de un valor central, y el patrón sugiere que se repetirá (a las 12h vuelve al mismo valor que a las 0h). Valor medio D ≈ (3,2+0,8)/2 = **2,0 m**; amplitud A ≈ 3,2−2,0 = **1,2 m**; el ciclo parece completarse en **12 horas** (de 0h a 12h vuelve al mismo valor y tendencia), consistente con un ciclo típico de marea semidiurna.
*Retroalimentación:* antes de ajustar los parámetros exactos de un modelo trigonométrico a partir de datos, conviene primero verificar que el patrón sea efectivamente oscilatorio (sube y baja de forma repetida alrededor de un centro), y estimar visualmente el valor medio, la amplitud y el período aproximado.

**Pregunta 18 (calcular — exponente negativo aplicado a intensidad de sonido).** La intensidad de un sonido sigue I(d) = 500/d² (unidades relativas), donde d es la distancia en metros. ¿A qué distancia la intensidad se reduce a 5 (unidades relativas)?

**Respuesta esperada:** 500/d² = 5 → d² = 500/5 = 100 → d = **10 metros**.
*Retroalimentación:* al despejar la variable independiente en un modelo de potencia con exponente negativo, se debe "invertir" la operación aplicando la raíz correspondiente al valor absoluto del exponente (aquí, raíz cuadrada, porque el exponente es −2).

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

**Pregunta 4 (completar).** El modelo binomial se aplica a variables ______ (que se cuentan), mientras que el modelo normal se aplica a variables ______ (que se miden en una escala continua).

**Respuesta esperada:** **discretas**; **continuas**.
*Retroalimentación:* esta distinción —contar éxitos en ensayos discretos vs. medir una magnitud continua— es el primer criterio para decidir qué modelo usar frente a una situación nueva.

**Pregunta 5 (desarrollo — calcular probabilidad binomial).** Un vendedor tiene una probabilidad de 0,3 de cerrar una venta en cada visita a un cliente. Si realiza 4 visitas, calcula la probabilidad de que cierre exactamente 2 ventas.

**Respuesta esperada:** n=4, p=0,3, k=2. C(4,2)=6. P(X=2)=6×(0,3)²×(0,7)²=6×0,09×0,49≈**0,2646 (26,46%)**.
*Retroalimentación:* el factor combinatorio C(n,k) cuenta de cuántas formas distintas se pueden ordenar los k éxitos entre los n ensayos (por ejemplo, cuáles 2 de las 4 visitas fueron exitosas), y se multiplica por la probabilidad de cada una de esas secuencias específicas.

**Pregunta 6 (desarrollo — media y varianza binomial).** En un proceso de control de calidad, la probabilidad de que un producto tenga un defecto es 0,05. Se revisan 200 productos. Calcula el número esperado de productos defectuosos y la desviación estándar.

**Respuesta esperada:** μ = n×p = 200×0,05 = **10 productos defectuosos esperados**. σ² = n×p×(1−p) = 200×0,05×0,95 = 9,5. σ = √9,5 ≈ **3,08**.
*Retroalimentación:* incluso conociendo el valor esperado (10), la desviación estándar indica cuánta variación es "normal" alrededor de ese valor esperado en distintos lotes de 200 productos.

**Pregunta 7 (problema en contexto — regla empírica).** El tiempo de reacción de los conductores ante una señal de alerta se distribuye normalmente con media μ=0,8 segundos y desviación estándar σ=0,1 segundos. ¿Entre qué valores se encuentra el tiempo de reacción del 95% de los conductores, aproximadamente?

**Respuesta esperada:** μ±2σ = 0,8±0,2, es decir, entre **0,6 y 1,0 segundos**.
*Retroalimentación:* aplicar la regla empírica no requiere calcular nada más que sumar y restar 2 veces la desviación estándar a la media, siempre que los datos sigan (al menos aproximadamente) una distribución normal.

**Pregunta 8 (problema en contexto — elegir modelo y justificar).** Una farmacéutica estudia dos variables: (1) si cada paciente de un ensayo clínico presenta o no un efecto secundario (sí/no), evaluado en 50 pacientes; (2) la presión arterial sistólica (en mmHg) de esos mismos 50 pacientes. ¿Qué modelo es más adecuado para cada variable?

**Respuesta esperada:** (1) corresponde a un modelo **binomial**, porque cada paciente tiene un resultado binario (presenta o no el efecto secundario) y se cuenta cuántos de los 50 lo presentan. (2) corresponde a un modelo **normal**, porque la presión arterial es una variable continua que típicamente se distribuye simétricamente alrededor de un valor promedio.
*Retroalimentación:* dentro de un mismo estudio pueden convivir variables que requieren distintos modelos; identificar correctamente el tipo de cada variable (discreta de dos resultados vs. continua) es el paso previo indispensable antes de aplicar cualquier fórmula.

**Pregunta 9 (calcular — probabilidad de "al menos").** En un examen de alternativas con 5 preguntas de verdadero/falso, un estudiante responde al azar (p=0,5 de acertar cada una). Calcula la probabilidad de que acierte las 5 preguntas.

**Respuesta esperada:** n=5, p=0,5, k=5. C(5,5)=1. P(X=5) = 1×(0,5)⁵×(0,5)⁰ = (0,5)⁵ = **0,03125 (3,125%)**.
*Retroalimentación:* cuando k=n (todos son éxitos), la fórmula binomial se simplifica a pⁿ, ya que C(n,n)=1 y (1−p)⁰=1; responder al azar y acertar todo es, como muestra este cálculo, poco probable incluso en pruebas cortas.

**Pregunta 10 (verdadero o falso — límites de un argumento).** Una encuesta a 30 personas en un centro comercial de un solo barrio de Santiago concluye que "el 70% de los chilenos prefiere el producto X". Esta conclusión está bien fundamentada.

**Respuesta correcta: Falso.**
*Retroalimentación:* la muestra es pequeña (30 personas) y, sobre todo, **no representa** a la población de interés ("los chilenos"): fue tomada en un solo lugar y con un perfil probablemente muy específico de personas; generalizar sus resultados a todo el país es un error de alcance del argumento estadístico.

**Pregunta 11 (desarrollo — correlación vs. causalidad).** Un estudio encuentra que, en distintas ciudades, existe una fuerte correlación entre el número de heladerías y el número de ahogamientos en piscinas durante el año. ¿Se puede concluir que las heladerías causan ahogamientos? Explica.

**Respuesta esperada:** **No**. Ambas variables están relacionadas con una tercera: la **temperatura** (en meses o ciudades más calurosas, hay más heladerías abiertas y también más gente nadando, lo que aumenta el riesgo de ahogamientos). Esto es un ejemplo clásico de **correlación sin causalidad**: dos variables se mueven juntas por la influencia de una variable oculta, no porque una cause directamente a la otra.
*Retroalimentación:* evaluar los "alcances y límites" de un argumento estadístico incluye revisar si una correlación observada realmente implica una relación de causa y efecto, o si ambas variables podrían estar siendo influidas por un factor externo común.

**Pregunta 12 (desarrollo — pertinencia del modelo).** Un analista quiere modelar el número de artículos defectuosos en lotes de 20 unidades producidas en una fábrica (con una probabilidad fija de defecto por unidad), pero decide usar un modelo normal en lugar de uno binomial. ¿Es esto pertinente? Justifica.

**Respuesta esperada:** **No es la elección más pertinente**, al menos no directamente: se trata de una variable **discreta** (número de artículos defectuosos, un conteo entero entre 0 y 20), con un número fijo de ensayos y una probabilidad fija de "éxito" (defecto) por unidad — exactamente las condiciones de un modelo **binomial**. El modelo normal es apropiado para variables continuas, no para conteos discretos de este tipo (aunque, con n grande, el binomial puede aproximarse razonablemente por uno normal, pero esa es una decisión adicional, no la primera opción).
*Retroalimentación:* evaluar la "pertinencia" de un modelo implica verificar que sus supuestos (variable discreta vs. continua, número fijo de ensayos, independencia) calcen con la situación real antes de aplicarlo, y no elegir un modelo solo porque es más familiar o fácil de calcular.

**Pregunta 13 (leer datos — comparar dos experimentos binomiales).** Dos tratamientos médicos se prueban en grupos de 10 pacientes cada uno. El Tratamiento A tiene probabilidad de éxito p=0,6 por paciente; el Tratamiento B tiene p=0,75. Sin calcular las probabilidades exactas, ¿qué tratamiento esperarías que tenga un mayor número promedio de pacientes exitosos, y cuántos en promedio?

**Respuesta esperada:** el **Tratamiento B**, porque tiene mayor p. En promedio: A: μ=10×0,6=**6 pacientes**; B: μ=10×0,75=**7,5 pacientes**.
*Retroalimentación:* comparar el valor esperado (μ=n×p) de dos modelos binomiales con el mismo n es tan simple como comparar sus probabilidades p, sin necesidad de calcular la distribución completa.

**Pregunta 14 (problema en contexto — evaluar límites de una encuesta).** Antes de una elección, una encuesta telefónica solo logra contactar a personas mayores de 60 años, y concluye una preferencia de voto determinada para "toda la población". ¿Qué límite tiene este argumento estadístico?

**Respuesta esperada:** el límite es un **sesgo de muestra** (o sesgo de selección): al contactar solo a un grupo etario específico (mayores de 60 años), la muestra **no es representativa** de toda la población votante, que incluye otros grupos de edad con posiblemente preferencias distintas; generalizar el resultado a "toda la población" no está fundamentado.
*Retroalimentación:* un argumento estadístico puede tener un tamaño de muestra grande y aun así estar mal fundamentado si esa muestra no representa adecuadamente a la población sobre la que se quiere concluir.

**Pregunta 15 (calcular — probabilidad "al menos uno").** La probabilidad de que un vuelo se retrase es 0,1. Se analizan 3 vuelos independientes. Calcula la probabilidad de que **al menos uno** se retrase.

**Respuesta esperada:** es más simple calcular el complemento: P(ninguno se retrasa) = (0,9)³ = 0,729. P(al menos uno se retrasa) = 1−0,729 = **0,271 (27,1%)**.
*Retroalimentación:* para eventos de tipo "al menos uno", casi siempre conviene calcular la probabilidad del complemento (que no ocurra ninguno) y restarla de 1, en lugar de sumar las probabilidades de cada caso posible por separado.

**Pregunta 16 (problema no rutinario — combinar dispersión y modelo normal).** Dos máquinas envasadoras llenan bolsas de arroz con un peso medio de 1.000 g. La Máquina 1 tiene σ=5 g y la Máquina 2 tiene σ=20 g, ambas con distribución aproximadamente normal. Si el control de calidad rechaza bolsas con menos de 970 g, ¿qué máquina generará más bolsas rechazadas? Explica usando la regla empírica.

**Respuesta esperada:** 970 g está a 30 g bajo la media. Para la Máquina 1 (σ=5), eso equivale a 30/5=**6 desviaciones estándar** bajo la media: prácticamente ninguna bolsa caerá tan lejos (muy por fuera del 99,7%). Para la Máquina 2 (σ=20), 970 g equivale a 30/20=**1,5 desviaciones estándar** bajo la media, un rango donde sí cae una proporción notable de las bolsas. **La Máquina 2 generará muchas más bolsas rechazadas**, porque su mayor dispersión hace que sea mucho más probable que un valor se aleje tanto de la media.
*Retroalimentación:* dos procesos con el mismo promedio pueden tener tasas de "fallas" muy distintas si difieren en su desviación estándar; expresar cuántas desviaciones estándar representa un límite (aquí, 970 g) es la forma correcta de comparar el riesgo entre ambos procesos.

**Pregunta 17 (comparar — evaluar un argumento probabilístico).** Un titular de prensa afirma: "Un estudio de 15 personas demuestra que el suplemento X mejora la memoria". ¿Qué pregunta(s) deberías hacerte antes de aceptar esta conclusión?

**Respuesta esperada (abierta, ejemplo de buena respuesta):** ¿el tamaño de la muestra (15 personas) es suficiente para sacar una conclusión generalizable? ¿Hubo un grupo de control (personas que no tomaron el suplemento) para comparar? ¿Se controlaron otras variables que podrían explicar la mejora (por ejemplo, cambios en el sueño o la dieta durante el estudio)? ¿El resultado fue estadísticamente significativo, o pudo deberse al azar dado el tamaño pequeño de la muestra?
*Retroalimentación:* evaluar los alcances y límites de un argumento estadístico antes de tomar una decisión (por ejemplo, comprar el suplemento) es exactamente la habilidad central de este Objetivo de Aprendizaje: no se trata de rechazar todo estudio, sino de identificar qué preguntas hacer para juzgar su solidez.

**Pregunta 18 (desarrollo — probabilidad binomial con complemento).** En una línea de producción, cada artículo tiene una probabilidad de 0,02 de salir defectuoso. Se revisa una muestra de 5 artículos. Calcula la probabilidad de que **ninguno** salga defectuoso, y la probabilidad de que **al menos uno** salga defectuoso.

**Respuesta esperada:** P(ninguno defectuoso) = (0,98)⁵ ≈ **0,9039 (90,39%)**. P(al menos uno defectuoso) = 1−0,9039 = **0,0961 (9,61%)**.
*Retroalimentación:* este es un caso particular útil en control de calidad: aunque la probabilidad de defecto por artículo es baja (2%), la probabilidad de que aparezca al menos un defecto al revisar varios artículos juntos ya no es tan pequeña.

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
