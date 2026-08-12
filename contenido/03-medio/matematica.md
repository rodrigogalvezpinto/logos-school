---
título: Matemática — 3° Medio
asignatura: Matemática
curso: 3° Medio
fuente curricular: Bases Curriculares, Decreto 193/2019 "Plan Común" (Mineduc/UCE) — temario oficial del Examen Libre de Validación de Estudios
última actualización: 2026-08-10
---

# Matemática — 3° Medio

> Este apunte se basa fielmente en el temario oficial del Mineduc/UCE para el Examen Libre de Validación de Estudios de 3° medio, bajo el **Decreto de Bases Curriculares N°193, del año 2019 ("Plan Común")**. **CAMBIO IMPORTANTE respecto a 1°-2° medio:** desde este nivel el currículum cambia de decreto (1°-2° medio usan el Decreto N°614/2013), y la selección de Objetivos de Aprendizaje se reduce a solo **3 OA** de Matemática, provenientes de los ejes Álgebra y Funciones, Geometría, y Probabilidad y Estadística. Que sean pocos OA no significa que sean simples: cada uno agrupa un abanico amplio de contenidos, por lo que este apunte los cubre en profundidad, con más ejemplos y preguntas que en los cursos anteriores.

## Antes de empezar

**Sobre el formato del examen:** cada asignatura se rinde en una prueba **separada e independiente**, de **25 preguntas** y **90 minutos** de duración (máximo 2 pruebas por día). En la prueba de Matemática **se permite el uso de calculadora**. Úsala con criterio: para potencias, logaritmos y razones trigonométricas que no son "redondos", pero sigues siendo tú quien decide qué operación aplicar, cómo plantear el problema, y si el resultado tiene sentido en el contexto.

Este año trabajas con tres grandes bloques de contenido, cada uno correspondiente a un único Objetivo de Aprendizaje:

1. **Álgebra y Funciones (OA3)** — modelos de **crecimiento y decrecimiento exponencial y logarítmico**: población, ahorro, depreciación, desintegración radiactiva, propagación de información. Aprenderás a construir estos modelos, usarlos para proyectar valores, identificar en qué intervalos tienen sentido, y ajustar sus parámetros.
2. **Geometría (OA4)** — **relaciones métricas en la circunferencia**: cómo se relacionan los ángulos (centrales, inscritos, formados por cuerdas y secantes) con los arcos que subtienden, y cómo se relacionan los segmentos de cuerdas, secantes y tangentes entre sí.
3. **Probabilidad y Estadística (OA2)** — **toma de decisiones bajo incertidumbre**: usar medidas de dispersión (rango, varianza, desviación estándar) para comparar situaciones, y usar probabilidad condicional (árboles, tablas de doble entrada) para tomar decisiones informadas.

En todo momento vas a practicar las habilidades matemáticas de **resolver problemas**, **argumentar y comunicar**, **modelar** situaciones reales, y **representar** información de distintas formas —incluyendo la búsqueda, selección y verificación de información en ambientes digitales, algo que el propio Mineduc destaca como relevante para este nivel. ¡Empecemos!

---

## Eje: Álgebra y Funciones

### OA 3 — Aplicar modelos exponenciales y logarítmicos de crecimiento y decrecimiento

Vas a **aplicar modelos matemáticos que describen fenómenos de crecimiento y decrecimiento**, usando las funciones **exponencial** y **logarítmica**: determinando valores o haciendo proyecciones a partir de un modelo, identificando los intervalos donde el modelo tiene sentido según la situación real, variando sus parámetros para ajustarlo, y construyendo tú mismo un modelo a partir de datos —de forma manuscrita y también con calculadora u otras herramientas tecnológicas—.

**¿Por qué importa?** Muchos fenómenos no cambian de a poco y de forma constante (como en una función lineal), sino que su velocidad de cambio depende de su tamaño actual: mientras más grande es una población, más rápido crece en términos absolutos; mientras menos queda de una sustancia radiactiva, más lento se desintegra en términos absolutos. Ese comportamiento —crecer o decrecer "proporcionalmente a lo que ya se tiene"— es exactamente lo que describe una función exponencial. Se usa para modelar ahorros e intereses, poblaciones, epidemias, la depreciación de un vehículo, la eliminación de un fármaco en el cuerpo, o la viralización de una noticia en redes sociales. Y como el Mineduc lo enfatiza especialmente en este OA: saber leer y cuestionar este tipo de modelos —por ejemplo, los que aparecen en redes sociales sobre el crecimiento de una enfermedad o de una inversión— es una herramienta clave de ciudadanía digital.

**Modelo exponencial general:** f(x) = a·bˣ, donde **a** es el valor inicial (en x=0) y **b>0, b≠1** es el factor por el cual se multiplica la cantidad en cada unidad de x.

| Si... | Entonces... |
|---|---|
| b > 1 | el modelo es de **crecimiento** |
| 0 < b < 1 | el modelo es de **decrecimiento** |
| b = 1 | la cantidad se mantiene **constante** (no es un modelo de crecimiento ni decrecimiento) |

**Tasa porcentual:** si una cantidad crece a una tasa r (en decimal) por período, b = 1+r; si decrece a una tasa r, b = 1−r. Así, el modelo también se escribe como f(x) = a·(1±r)ˣ.

**Vida media (semidesintegración):** tiempo que demora una cantidad en reducirse a la mitad. Si h es la vida media, el modelo se escribe N(t) = N₀·(1/2)^(t/h).

**Función logarítmica y modelos:** la función logarítmica y = log_b(x) es la inversa de la exponencial b^x. Se usa para **despejar el exponente** (por ejemplo, el tiempo) cuando se conoce el valor final de una cantidad que crece o decrece exponencialmente: si b^x = k, entonces x = log_b(k).

**Intervalo donde el modelo tiene sentido:** todo modelo exponencial que representa una situación real tiene límites prácticos —por ejemplo, el tiempo no puede ser negativo, o una cantidad no puede superar una capacidad máxima (un estanque, una población limitada por recursos)—. Antes de usar un modelo para proyectar, siempre hay que preguntarse en qué rango de valores de x sigue siendo razonable.

#### Ejemplos resueltos

**Ejemplo 1 — Proyectar un valor: interés compuesto**

Un estudiante deposita $100.000 en una cuenta de ahorro con interés compuesto anual del 4%. El modelo es A(t) = 100.000×(1,04)ᵗ. Calcula el monto aproximado después de 5 años.

A(5) = 100.000×(1,04)⁵ = 100.000×1,2167 ≈ **$121.665**. Cada año, el monto no crece en una cantidad fija de pesos, sino en un 4% del monto que ya se tiene —por eso el crecimiento se acelera con el tiempo.

**Ejemplo 2 — Vida media: desintegración de un isótopo**

El yodo-131, usado en algunos tratamientos médicos, tiene una vida media de 8 días. Si se administra una dosis inicial de 40 mg, ¿cuánto queda después de 24 días?

24 días equivalen a 24÷8 = 3 vidas medias. N(24) = 40×(1/2)³ = 40×(1/8) = **5 mg**.

**Ejemplo 3 — Despejar el tiempo con logaritmos**

Una población de una especie protegida crece según P(t) = 200×(1,15)ᵗ (t en años). ¿En cuántos años aproximadamente se duplicará la población (llegará a 400)?

Se plantea 200×(1,15)ᵗ = 400, es decir (1,15)ᵗ = 2. Aplicando logaritmo: t = log(2)/log(1,15) ≈ 0,3010/0,0607 ≈ **4,96 ≈ 5 años**.

#### Preguntas de autoevaluación

**Pregunta 1 (alternativas).** El modelo f(x) = 500×(0,85)ˣ representa una situación de:
a) crecimiento, porque 500 es positivo
b) decrecimiento, porque 0 < 0,85 < 1
c) crecimiento, porque 0,85 es positivo
d) no se puede determinar sin más información

**Respuesta correcta: b) decrecimiento, porque 0 < 0,85 < 1.**
*Retroalimentación:* el signo de a solo indica que la cantidad inicial es positiva; lo que determina si el modelo crece o decrece es si el factor b es mayor o menor que 1.

**Pregunta 2 (verdadero o falso).** En un modelo exponencial f(x) = a·bˣ con b>1, mientras mayor es b, más rápido crece la función.

**Respuesta correcta: Verdadero.**
*Retroalimentación:* b representa el factor multiplicativo por unidad de x; un b más grande implica multiplicar por una cantidad mayor en cada período, acelerando el crecimiento.

**Pregunta 3 (calcular).** Si el factor de crecimiento de un modelo exponencial es b = 1,08, ¿cuál es la tasa de crecimiento porcentual?
a) 0,08%
b) 8%
c) 108%
d) 1,08%

**Respuesta correcta: b) 8%.**
*Retroalimentación:* como b=1+r, entonces r = 0,08 = 8%; b siempre se descompone en "1" (lo que ya había) más la tasa de cambio r.

**Pregunta 4 (completar).** La fórmula de interés compuesto es A(t) = P×(1+r)ᵗ, donde P es el ______, r es la ______ (como decimal) y t es el ______.

**Respuesta esperada:** P es el **capital inicial** (monto depositado); r es la **tasa de interés** por período; t es el **tiempo transcurrido** (número de períodos).
*Retroalimentación:* reconocer qué representa cada parámetro de la fórmula es indispensable para poder aplicarla correctamente a una situación nueva.

**Pregunta 5 (desarrollo — depreciación).** Un auto nuevo cuesta $12.000.000 y se deprecia un 12% anual, según el modelo V(t) = 12.000.000×(0,88)ᵗ. Calcula su valor aproximado después de 4 años.

**Respuesta esperada:** (0,88)⁴ ≈ 0,5997. V(4) = 12.000.000×0,5997 ≈ **$7.196.160**.
*Retroalimentación:* en la depreciación, el valor no baja en una cantidad fija de pesos cada año, sino en un porcentaje del valor actual; por eso baja más rápido al principio (en pesos) que al final.

**Pregunta 6 (desarrollo — vida media).** El carbono-14 tiene una vida media aproximada de 5.730 años. Si una muestra tiene inicialmente 80 g, ¿cuánto quedará después de 11.460 años?

**Respuesta esperada:** 11.460 ÷ 5.730 = 2 vidas medias. N = 80×(1/2)² = 80×(1/4) = **20 g**.
*Retroalimentación:* cuando el tiempo transcurrido es un múltiplo exacto de la vida media, no es necesario usar la fórmula completa: basta con dividir por 2 tantas veces como vidas medias hayan pasado.

**Pregunta 7 (problema con logaritmo — despejar tiempo).** Un rumor se difunde en redes sociales según M(t) = 50×(1,6)ᵗ (t en horas, M = número de personas que lo han visto). ¿Después de cuántas horas aproximadamente 800 personas lo habrán visto?

**Respuesta esperada:** se plantea 50×(1,6)ᵗ = 800, es decir (1,6)ᵗ = 16. t = log(16)/log(1,6) ≈ 1,2041/0,2041 ≈ **5,9 ≈ 6 horas**.
*Retroalimentación:* cuando la incógnita está en el exponente, se despeja aplicando logaritmo a ambos lados de la igualdad; esta es precisamente la utilidad de la función logarítmica como "inversa" de la exponencial.

**Pregunta 8 (problema en contexto — intervalo donde el modelo tiene sentido).** Un estanque de riego tiene capacidad máxima de 5.000 litros y se llena según V(t) = 200×(1,25)ᵗ (litros, t en horas). ¿Para qué valores de t tiene sentido este modelo?

**Respuesta esperada:** el modelo deja de tener sentido cuando V(t) supera 5.000 L. Resolviendo 200×(1,25)ᵗ = 5.000: (1,25)ᵗ = 25, t = log(25)/log(1,25) ≈ **14,4 horas**. El modelo tiene sentido solo para **0 ≤ t ≤ 14,4 horas aproximadamente**; más allá de eso, el estanque ya está lleno y no puede seguir acumulando agua según esa regla.
*Retroalimentación:* un modelo exponencial matemático puede seguir creciendo indefinidamente, pero la situación real que describe casi siempre tiene un límite físico; identificar ese límite es parte de interpretar correctamente el modelo.

**Pregunta 9 (comparar — variar parámetros).** Compara los modelos f(x) = 100×(1,1)ˣ y g(x) = 100×(1,05)ˣ. ¿Cuál crece más rápido, y por qué?

**Respuesta esperada:** **f crece más rápido**, porque ambos parten del mismo valor inicial (100), pero el factor de crecimiento de f (1,1, es decir 10% por período) es mayor que el de g (1,05, es decir 5% por período).
*Retroalimentación:* al comparar dos modelos exponenciales con el mismo valor inicial, basta con comparar sus factores b (o sus tasas r) para saber cuál crecerá más rápido, sin necesidad de calcular valores específicos.

**Pregunta 10 (leer datos — tabla).** Una colonia de pingüinos en la costa registra la siguiente población: t=0 → 80; t=1 → 96; t=2 → 115; t=3 → 138. ¿Corresponde este crecimiento a un modelo exponencial? Justifica calculando las razones entre términos consecutivos.

**Respuesta esperada:** 96/80 = 1,20; 115/96 ≈ 1,198; 138/115 ≈ 1,20. Como la **razón entre términos consecutivos es aproximadamente constante** (≈1,2), **sí corresponde a un crecimiento exponencial**, con un factor b≈1,2 (20% de crecimiento por período).
*Retroalimentación:* la señal distintiva de un crecimiento exponencial en una tabla de valores es que la razón (cuociente) entre términos consecutivos se mantiene aproximadamente constante, a diferencia del crecimiento lineal, donde lo constante es la diferencia.

**Pregunta 11 (alternativas — modelo logarítmico aplicado).** El nivel de un sonido, en decibeles, se calcula como L = 10·log₁₀(I/I₀). Si la razón I/I₀ = 1.000, ¿cuál es el nivel L?
a) 30 dB
b) 3 dB
c) 1.000 dB
d) 300 dB

**Respuesta correcta: a) 30 dB.**
*Retroalimentación:* log₁₀(1.000) = 3, porque 10³=1.000; entonces L = 10×3 = 30.

**Pregunta 12 (desarrollo — decrecimiento porcentual).** Un medicamento se elimina del organismo según C(t) = 250×(0,8)ᵗ (mg, t en horas). ¿Cuánto queda después de 3 horas, y qué porcentaje del medicamento se ha eliminado?

**Respuesta esperada:** (0,8)³ = 0,512. C(3) = 250×0,512 = **128 mg**. Eliminado: 250−128 = 122 mg, que corresponde a 122/250 = **48,8%**.
*Retroalimentación:* aunque el factor de decrecimiento es 0,8 (20% menos por hora), el porcentaje total eliminado después de varias horas no es simplemente 20%×3=60%, porque cada hora se elimina un 20% de lo que queda en ese momento, no del total inicial.

**Pregunta 13 (verdadero o falso).** Si b=1 en un modelo f(x)=a·bˣ, el modelo representa una situación de crecimiento.

**Respuesta correcta: Falso.**
*Retroalimentación:* cuando b=1, la cantidad se multiplica por 1 en cada período, es decir, se mantiene **constante**; no hay crecimiento ni decrecimiento.

**Pregunta 14 (calcular con logaritmo — decrecimiento).** La población de peces de una laguna disminuye según N(t) = 3.000×(0,9)ᵗ. ¿En cuántos años aproximadamente la población bajará a la mitad (1.500)?

**Respuesta esperada:** (0,9)ᵗ = 0,5. t = log(0,5)/log(0,9) ≈ (−0,3010)/(−0,0458) ≈ **6,6 años**.
*Retroalimentación:* el mismo procedimiento de despejar con logaritmos se usa tanto en modelos de crecimiento como de decrecimiento; solo cambia que el factor b es menor que 1.

**Pregunta 15 (problema en contexto — construir un modelo y proyectar).** Una aplicación chilena de transporte compartido tiene 2.000 usuarios el día de su lanzamiento y crece un 30% diario. Escribe el modelo U(t) y calcula el número aproximado de usuarios después de 10 días.

**Respuesta esperada:** U(t) = 2.000×(1,3)ᵗ. (1,3)¹⁰ ≈ 13,786. U(10) ≈ 2.000×13,786 ≈ **27.572 usuarios**.
*Retroalimentación:* construir el modelo consiste en identificar el valor inicial (2.000) y el factor de crecimiento a partir de la tasa porcentual (30% → b=1,3); una vez planteado, se evalúa en el valor de t que se necesite.

**Pregunta 16 (desarrollo — construir modelo desde dos datos).** Una población de conejos era de 50 individuos y, tras 3 años de crecimiento exponencial constante, llegó a 135. Determina la tasa de crecimiento anual aproximada.

**Respuesta esperada:** 135 = 50×(1+r)³, entonces (1+r)³ = 2,7, y 1+r = ∛2,7 ≈ 1,392. Por lo tanto, **r ≈ 0,392 ≈ 39,2% anual**.
*Retroalimentación:* cuando se conocen el valor inicial, el valor final y el tiempo transcurrido, se puede despejar el factor de crecimiento aplicando una raíz (el "inverso" de elevar a una potencia), y de ahí obtener la tasa r.

**Pregunta 17 (problema no rutinario — comparar crecimiento y decrecimiento).** Dos modelos parten del mismo valor, 1.000: f crece un 10% anual, g decrece un 10% anual. Después de 5 años, ¿cuál de los dos se aleja más de 1.000 en valor absoluto? Explica por qué no son simétricos.

**Respuesta esperada:** f(5) = 1.000×(1,1)⁵ ≈ 1.610,5 (610,5 sobre 1.000). g(5) = 1.000×(0,9)⁵ ≈ 590,5 (409,5 bajo 1.000). **f se aleja más de 1.000.** No son simétricos porque el crecimiento compuesto se acelera cada vez más (se multiplica repetidamente por un factor mayor que 1 sobre cantidades cada vez más grandes), mientras que el decrecimiento tiene un límite natural: la cantidad nunca puede bajar de 0, lo que restringe cuánto puede alejarse hacia abajo.
*Retroalimentación:* un error común es asumir que "crecer 10%" y "decrecer 10%" son cambios opuestos de igual magnitud; en un modelo exponencial no lo son, precisamente porque el crecimiento no tiene techo, pero el decrecimiento sí tiene un piso (el cero).

**Pregunta 18 (leer datos — distinguir de un modelo lineal).** Una tabla registra el valor de un bien en el tiempo: t=0 → 100; t=1 → 150; t=2 → 200; t=3 → 250. ¿Corresponde este comportamiento a un crecimiento exponencial? Justifica tu respuesta.

**Respuesta esperada:** **No**, porque las **diferencias** entre términos consecutivos son constantes (siempre +50), no las razones (150/100=1,5; 200/150≈1,33; 250/200=1,25, que no son iguales). Esto corresponde a un **crecimiento lineal**, no exponencial.
*Retroalimentación:* distinguir un modelo exponencial de uno lineal a partir de una tabla es clave: en el lineal, lo constante es la diferencia entre valores consecutivos; en el exponencial, lo constante es la razón (cuociente) entre ellos.

---

## Eje: Geometría

### OA 4 — Resolver problemas de relaciones métricas en la circunferencia

Vas a **resolver problemas de geometría euclidiana que involucran relaciones métricas entre ángulos, arcos, cuerdas y secantes en la circunferencia**: utilizando estas relaciones para determinar medidas desconocidas, justificando el uso de las propiedades correspondientes, y explicándolas mediante dibujos, esquemas o proposiciones —de forma manuscrita y con apoyo de herramientas tecnológicas—.

**¿Por qué importa?** La circunferencia esconde una red muy ordenada de relaciones entre sus ángulos, arcos y segmentos. Estas relaciones permiten resolver problemas de diseño e ingeniería que aparecen todo el tiempo en la vida real: desde calcular tensiones en los cables de un puente, hasta determinar distancias en un radar, pasando por el diseño de ruedas, antenas parabólicas y trazados urbanos con rotondas.

**Elementos básicos:** una **cuerda** une dos puntos de la circunferencia; una **secante** es una recta que corta la circunferencia en dos puntos; una **tangente** toca la circunferencia en un único punto. Un **arco** es una porción de la circunferencia, medida en grados, igual que un ángulo.

**Relaciones entre ángulos y arcos:**

| Ángulo | Vértice | Fórmula |
|---|---|---|
| Central | en el centro de la circunferencia | = el arco que subtiende |
| Inscrito | en la circunferencia, formado por dos cuerdas | = ½ del arco que subtiende |
| Semiinscrito | en la circunferencia, entre una tangente y una cuerda | = ½ del arco que abarca |
| Interior (dos cuerdas que se cortan dentro del círculo) | dentro del círculo | = ½ (arco 1 + arco 2), los dos arcos opuestos por el vértice |
| Exterior (dos secantes, dos tangentes, o secante y tangente, desde un punto exterior) | fuera del círculo | = ½ (arco mayor − arco menor) |

**Relaciones entre segmentos:**

| Situación | Fórmula |
|---|---|
| Dos cuerdas que se cortan dentro del círculo | (segmento 1)×(segmento 2) = (segmento 3)×(segmento 4) |
| Dos secantes desde un mismo punto exterior | (externa 1)×(completa 1) = (externa 2)×(completa 2) |
| Una tangente y una secante desde un mismo punto exterior | (tangente)² = (externa)×(completa) |

#### Ejemplos resueltos

**Ejemplo 1 — Ángulo central y ángulo inscrito**

En una circunferencia, un ángulo central mide 80°. ¿Cuánto mide un ángulo inscrito que subtiende el mismo arco?

El ángulo inscrito siempre mide la mitad del ángulo central que subtiende el mismo arco: 80°÷2 = **40°**.

**Ejemplo 2 — Segmentos de cuerdas que se cortan**

Dos cuerdas se cortan dentro de una circunferencia. Los segmentos de una cuerda miden 4 cm y 9 cm; uno de los segmentos de la otra cuerda mide 6 cm. Calcula el segmento restante.

Se aplica la relación de productos iguales: 4×9 = 6×x → 36 = 6x → x = **6 cm**.

**Ejemplo 3 — Dos secantes desde un punto exterior**

Desde un punto exterior a una circunferencia se trazan dos secantes. Una tiene una parte externa de 3 cm y una longitud total de 12 cm. La otra secante tiene una parte externa de 4 cm. Calcula su longitud total.

Se aplica la relación: (externa 1)×(completa 1) = (externa 2)×(completa 2): 3×12 = 4×x → 36 = 4x → x = **9 cm**.

#### Preguntas de autoevaluación

**Pregunta 1 (alternativas).** Un ángulo central mide 130°. ¿Cuánto mide el arco que subtiende?
a) 130°
b) 65°
c) 260°
d) 50°

**Respuesta correcta: a) 130°.**
*Retroalimentación:* un ángulo central es siempre igual, en grados, al arco que subtiende.

**Pregunta 2 (verdadero o falso).** El ángulo inscrito que subtiende el mismo arco que un ángulo central de 90° mide 45°.

**Respuesta correcta: Verdadero.**
*Retroalimentación:* el ángulo inscrito equivale a la mitad del ángulo central sobre el mismo arco: 90°÷2=45°.

**Pregunta 3 (calcular).** Un ángulo inscrito mide 35°. ¿Cuánto mide el arco que subtiende?
a) 70°
b) 35°
c) 17,5°
d) 140°

**Respuesta correcta: a) 70°.**
*Retroalimentación:* como el ángulo inscrito es la mitad del arco, el arco es el doble del ángulo inscrito: 35°×2=70°.

**Pregunta 4 (completar).** El ángulo ______ tiene su vértice en el centro de la circunferencia y es igual a la medida del arco que subtiende; el ángulo ______ tiene su vértice en la propia circunferencia y equivale a la mitad de ese arco.

**Respuesta esperada:** **central**; **inscrito**.
*Retroalimentación:* distinguir el vértice de cada tipo de ángulo (centro vs. circunferencia) es la clave para saber qué fórmula aplicar.

**Pregunta 5 (desarrollo — ángulo interior).** Dos cuerdas se cortan dentro de una circunferencia, formando un ángulo. Los arcos que abarcan (el arco opuesto y su arco vertical) miden 100° y 40°. Calcula la medida del ángulo formado.

**Respuesta esperada:** ½(100°+40°) = 140°÷2 = **70°**.
*Retroalimentación:* el ángulo formado por dos cuerdas que se cruzan dentro del círculo es el promedio de los dos arcos que quedan "enfrentados" por ese cruce.

**Pregunta 6 (desarrollo — segmentos de cuerdas).** Dos cuerdas se cortan dentro de un círculo. Los segmentos de una cuerda miden 5 cm y 8 cm. Si uno de los segmentos de la otra cuerda mide 4 cm, calcula el segmento restante.

**Respuesta esperada:** 5×8 = 4×x → 40 = 4x → x = **10 cm**.
*Retroalimentación:* en dos cuerdas que se cruzan, el producto de los segmentos de una es siempre igual al producto de los segmentos de la otra.

**Pregunta 7 (desarrollo — ángulo exterior).** Desde un punto exterior a una circunferencia se trazan dos secantes que interceptan arcos de 150° y 50°. Calcula la medida del ángulo formado en el punto exterior.

**Respuesta esperada:** ½(150°−50°) = 100°÷2 = **50°**.
*Retroalimentación:* a diferencia del ángulo interior (que usa la suma de los arcos), el ángulo exterior usa la **diferencia** entre el arco mayor y el arco menor, dividida en 2.

**Pregunta 8 (desarrollo — secante-secante).** Desde un punto exterior a una circunferencia, una secante tiene parte externa de 5 cm y longitud total de 20 cm. Otra secante tiene parte externa de 4 cm. Calcula su longitud total.

**Respuesta esperada:** 5×20 = 4×x → 100 = 4x → x = **25 cm**.
*Retroalimentación:* en dos secantes trazadas desde el mismo punto exterior, el producto (externa×completa) es el mismo para ambas.

**Pregunta 9 (desarrollo — tangente-secante).** Desde un punto exterior se traza una tangente de 12 cm y una secante cuya parte externa mide 8 cm. Calcula la longitud total de la secante.

**Respuesta esperada:** (tangente)² = externa×completa: 12² = 8×x → 144 = 8x → x = **18 cm**.
*Retroalimentación:* cuando una de las rectas es tangente, su longitud se eleva al cuadrado y se iguala al producto de la parte externa y la longitud total de la secante.

**Pregunta 10 (leer datos).** En una circunferencia de centro O, el arco AB (menor) mide 76°. Un ángulo inscrito ACB que subtiende ese mismo arco, con C ubicado en el arco mayor, ¿cuánto mide?

**Respuesta esperada:** ½×76° = **38°**.
*Retroalimentación:* no importa en qué punto exacto del arco mayor se ubique C: todo ángulo inscrito que subtiende el mismo arco mide siempre la mitad de ese arco.

**Pregunta 11 (alternativas — ángulo semiinscrito).** Una tangente y una cuerda se cortan en el punto de tangencia, formando un ángulo semiinscrito que abarca un arco de 96°. ¿Cuánto mide ese ángulo?
a) 48°
b) 96°
c) 192°
d) 24°

**Respuesta correcta: a) 48°.**
*Retroalimentación:* el ángulo semiinscrito, igual que el inscrito, mide la mitad del arco que abarca: 96°÷2=48°.

**Pregunta 12 (verdadero o falso).** En un triángulo inscrito en una circunferencia donde uno de sus lados es un diámetro, el ángulo opuesto a ese diámetro siempre mide 90°.

**Respuesta correcta: Verdadero.**
*Retroalimentación:* ese ángulo es un ángulo inscrito que subtiende una semicircunferencia (arco de 180°), por lo tanto mide ½×180°=90° (este resultado también se conoce como Teorema de Tales aplicado a la circunferencia).

**Pregunta 13 (problema en contexto — rueda de la fortuna).** En la rueda de la fortuna de un parque de diversiones, dos cabinas A y B están ubicadas de modo que el ángulo central entre ellas, medido desde el eje de la rueda, es 60°. Un operador observa ambas cabinas desde un punto fijo en el borde opuesto de la rueda. ¿Qué ángulo inscrito forma esa observación?

**Respuesta esperada:** ½×60° = **30°**.
*Retroalimentación:* el eje de la rueda funciona como el centro de la circunferencia, y el borde donde se ubica el operador es un punto sobre la propia circunferencia: exactamente la situación de un ángulo central y uno inscrito sobre el mismo arco.

**Pregunta 14 (problema en contexto — plaza circular).** En una plaza circular, dos caminos rectos (secantes) parten desde un mismo punto exterior a la plaza y cruzan la circunferencia, delimitando arcos de 120° y 40° sobre el borde de la plaza. ¿Cuál es el ángulo entre los dos caminos en el punto donde se juntan, fuera de la plaza?

**Respuesta esperada:** ½(120°−40°) = 80°÷2 = **40°**.
*Retroalimentación:* al tratarse de dos secantes desde un punto exterior a la circunferencia, se aplica la fórmula del ángulo exterior: la mitad de la diferencia entre los arcos.

**Pregunta 15 (problema en contexto — cables de un puente).** Dos cables tensores de un puente colgante se cruzan, actuando como cuerdas dentro del arco circular de un soporte. Los segmentos de uno de los cables, a cada lado del cruce, miden 6 m y 10 m; uno de los segmentos del otro cable mide 5 m. ¿Cuánto mide el segmento restante?

**Respuesta esperada:** 6×10 = 5×x → 60 = 5x → x = **12 m**.
*Retroalimentación:* aunque el contexto sea de ingeniería, la relación matemática es la misma que la de dos cuerdas cualesquiera que se cruzan dentro de una circunferencia.

**Pregunta 16 (problema en contexto — reserva marina).** La trayectoria de un barco pesquero (una secante) cruza cerca de una reserva marina circular. La parte de su trayectoria fuera de la reserva mide 6 millas náuticas, y la trayectoria completa (hasta salir por el otro lado) mide 15 millas. Desde el mismo punto de partida del barco, un faro tiene una línea de visión tangente a la reserva. ¿Cuánto mide esa línea tangente?

**Respuesta esperada:** (tangente)² = externa×completa = 6×15 = 90. tangente = √90 ≈ **9,49 millas náuticas**.
*Retroalimentación:* la relación tangente-secante permite calcular la longitud de una tangente sin medirla directamente, a partir de los datos de una secante trazada desde el mismo punto exterior.

**Pregunta 17 (comparar).** Compara un ángulo central y un ángulo inscrito que subtienden el mismo arco de una circunferencia. ¿Qué relación se cumple siempre entre ellos, sin importar la medida del arco?

**Respuesta esperada:** el ángulo inscrito **siempre mide la mitad** del ángulo central que subtiende el mismo arco; esa relación de 1 a 2 se mantiene sin importar cuál sea la medida específica del arco.
*Retroalimentación:* esta relación (inscrito = mitad del central) es la base de casi todas las demás propiedades de ángulos en la circunferencia, incluyendo la del ángulo semiinscrito.

**Pregunta 18 (problema no rutinario — justificar).** Un electricista debe ubicar un poste de modo que, desde su base, dos cables tensores lleguen tangentes a una tubería circular subterránea. Explica, usando las relaciones métricas de la circunferencia, por qué ambos cables tangentes desde ese mismo punto deben medir exactamente lo mismo.

**Respuesta esperada:** desde un mismo punto exterior, cualquier segmento tangente trazado hacia la circunferencia forma, con el radio en el punto de tangencia, un ángulo recto (el radio es perpendicular a la tangente). Esto genera dos triángulos rectángulos congruentes —comparten la hipotenusa (la distancia entre el punto exterior y el centro) y tienen catetos iguales (el radio)—, por lo tanto sus otros catetos, que corresponden a los dos segmentos tangentes, **son necesariamente iguales**.
*Retroalimentación:* esta propiedad —que los dos segmentos tangentes trazados desde un mismo punto exterior son siempre congruentes— es consecuencia directa de la relación entre el radio y la tangente, y se usa con frecuencia en problemas de diseño e ingeniería.

**Pregunta 19 (desarrollo — arco como fracción de la circunferencia).** Un arco corresponde a 1/6 de la circunferencia completa. ¿Cuántos grados mide el ángulo central que lo subtiene?

**Respuesta esperada:** 360°÷6 = **60°**.
*Retroalimentación:* como la circunferencia completa mide 360°, cualquier fracción de ella se puede convertir directamente a grados multiplicando (o dividiendo) por 360°.

**Pregunta 20 (leer datos — suma de arcos).** En una circunferencia, cuatro arcos consecutivos que la completan miden 90°, 70°, x° y 110°. Determina el valor de x, sabiendo que los arcos de una circunferencia completa suman 360°.

**Respuesta esperada:** 90°+70°+110° = 270°. x = 360°−270° = **90°**.
*Retroalimentación:* los arcos que dividen una circunferencia completa siempre deben sumar 360°, exactamente igual que los ángulos alrededor de un punto.

---

## Eje: Probabilidad y Estadística

### OA 2 — Tomar decisiones usando dispersión y probabilidad condicional

Vas a **tomar decisiones en situaciones de incerteza** que involucran dos herramientas: por un lado, el análisis de datos estadísticos mediante **medidas de dispersión**, para comparar situaciones y comunicar una decisión; por otro, el cálculo de **probabilidades condicionales**, representadas mediante árboles o tablas de doble entrada, también para tomar decisiones.

**¿Por qué importa?** Hasta ahora has usado el **promedio** para resumir un conjunto de datos, pero dos conjuntos pueden tener el mismo promedio y comportarse de manera muy distinta: por ejemplo, dos rutas de transporte pueden demorar en promedio lo mismo, pero una puede ser mucho más impredecible que la otra. Las **medidas de dispersión** capturan justamente esa variabilidad, y son claves para decidir qué opción es más confiable, no solo cuál es "mejor en promedio". Por su parte, la **probabilidad condicional** te permite responder preguntas del tipo "¿qué tan probable es A, sabiendo que ya ocurrió B?" —esencial para interpretar resultados de exámenes médicos, encuestas, y decisiones cotidianas donde la información se va actualizando.

**Medidas de dispersión:**

| Medida | Fórmula | Qué indica |
|---|---|---|
| Rango | máximo − mínimo | la amplitud total de los datos |
| Varianza (σ²) | promedio de las desviaciones al cuadrado respecto a la media | qué tan dispersos están los datos, en unidades al cuadrado |
| Desviación estándar (σ) | √(varianza) | la dispersión típica, en las mismas unidades que los datos originales |

A menor desviación estándar, los datos están más concentrados alrededor de la media (más "parejos" o predecibles); a mayor desviación estándar, están más dispersos.

**Probabilidad condicional:** la probabilidad de que ocurra un evento A, sabiendo que ya ocurrió un evento B, se calcula como:

**P(A|B) = P(A∩B) / P(B)**, con P(B) > 0.

Se puede representar con un **diagrama de árbol** (las probabilidades sucesivas se multiplican a lo largo de cada rama) o con una **tabla de doble entrada** (donde se puede leer directamente la información dentro de una categoría, dividiendo por el total de esa fila o columna).

#### Ejemplos resueltos

**Ejemplo 1 — Comparar dispersión para tomar una decisión**

Dos micros (buses) que van a un mismo destino tienen el mismo tiempo promedio de viaje: 10 minutos. Los tiempos registrados (en minutos) para el Micro A fueron 8, 9, 10, 11, 12; para el Micro B fueron 2, 6, 10, 14, 18. ¿Cuál es más confiable (predecible)?

Micro A: desviaciones respecto a la media (−2,−1,0,1,2), al cuadrado (4,1,0,1,4), suma=10, varianza=10/5=2, desviación estándar=√2≈1,41.
Micro B: desviaciones (−8,−4,0,4,8), al cuadrado (64,16,0,16,64), suma=160, varianza=160/5=32, desviación estándar=√32≈5,66.

Aunque ambos tienen el mismo promedio, el **Micro A es mucho más confiable**, porque su desviación estándar (1,41 min) es mucho menor que la del Micro B (5,66 min): sus tiempos de viaje varían mucho menos.

**Ejemplo 2 — Árbol de probabilidades: prueba diagnóstica**

Una prueba rápida para detectar una enfermedad tiene una sensibilidad del 90% (P(positivo|enfermo)=0,90), y en la población general un 2% de las personas está enferma (P(enfermo)=0,02). Calcula la probabilidad de que una persona elegida al azar esté enferma y dé positivo.

Usando la rama del árbol correspondiente: P(enfermo y positivo) = P(enfermo)×P(positivo|enfermo) = 0,02×0,90 = **0,018 (1,8%)**.

**Ejemplo 3 — Tabla de doble entrada**

Se encuesta a 200 estudiantes de un liceo sobre su cercanía al establecimiento y su medio de transporte:

| | Camina | Usa transporte | Total |
|---|---|---|---|
| Vive cerca | 60 | 20 | 80 |
| Vive lejos | 10 | 110 | 120 |
| Total | 70 | 130 | 200 |

Calcula P(camina | vive cerca).

Se trabaja solo dentro de la fila "vive cerca" (80 estudiantes en total), de los cuales 60 caminan: P(camina|vive cerca) = 60/80 = **0,75 (75%)**.

#### Preguntas de autoevaluación

**Pregunta 1 (alternativas).** Calcula el rango del conjunto de datos {12, 15, 9, 20, 14}.
a) 11
b) 20
c) 9
d) 5

**Respuesta correcta: a) 11.**
*Retroalimentación:* el rango es el máximo menos el mínimo: 20−9=11.

**Pregunta 2 (verdadero o falso).** La desviación estándar siempre se expresa en las mismas unidades que los datos originales, a diferencia de la varianza.

**Respuesta correcta: Verdadero.**
*Retroalimentación:* la varianza queda en unidades "al cuadrado" (por ejemplo, minutos²), mientras que al sacar la raíz cuadrada, la desviación estándar vuelve a las unidades originales (minutos).

**Pregunta 3 (calcular).** Calcula la varianza del conjunto de datos {2, 4, 6}.
a) 2,67
b) 8
c) 2
d) 4

**Respuesta correcta: a) 2,67.**
*Retroalimentación:* la media es 4; las desviaciones son (−2,0,2), al cuadrado (4,0,4), suma=8, y varianza=8/3≈2,67.

**Pregunta 4 (completar).** La varianza es el promedio de las ______ de las desviaciones respecto a la media, y la desviación estándar es su ______.

**Respuesta esperada:** **cuadrados**; **raíz cuadrada**.
*Retroalimentación:* elevar al cuadrado evita que las desviaciones positivas y negativas se cancelen entre sí al promediarlas; luego, sacar la raíz cuadrada devuelve la medida a la escala original.

**Pregunta 5 (desarrollo — comparar dispersión).** Dos cursos rindieron la misma prueba, con el mismo promedio: 5,5. El curso A tiene una desviación estándar de 0,4; el curso B, de 1,3. ¿Qué curso tuvo resultados más homogéneos entre sus estudiantes? Justifica.

**Respuesta esperada:** el **curso A**, porque una menor desviación estándar indica que las notas están más concentradas alrededor del promedio, es decir, resultados más parejos u homogéneos.
*Retroalimentación:* dos grupos con el mismo promedio pueden tener realidades muy distintas; la desviación estándar es la medida que permite distinguir esa diferencia.

**Pregunta 6 (desarrollo — rango en contexto).** Un puesto de la Vega Central registra las siguientes ventas diarias de kilos de tomate durante una semana: 40, 45, 38, 42, 50, 35, 48. Determina el rango de las ventas.

**Respuesta esperada:** máximo=50, mínimo=35, rango = 50−35 = **15 kg**.
*Retroalimentación:* el rango es la medida de dispersión más simple de calcular, pero solo usa dos datos (el máximo y el mínimo), por lo que no refleja qué tan dispersos están todos los demás valores.

**Pregunta 7 (desarrollo — varianza y desviación estándar).** Los tiempos (en minutos) que demoran 4 trámites en una municipalidad son: 10, 12, 14, 16. Calcula la varianza y la desviación estándar.

**Respuesta esperada:** media=13; desviaciones (−3,−1,1,3), al cuadrado (9,1,1,9), suma=20; varianza=20/4=**5**; desviación estándar=√5≈**2,24 minutos**.
*Retroalimentación:* el procedimiento siempre sigue el mismo orden: calcular la media, restarla a cada dato, elevar al cuadrado, promediar (varianza), y sacar raíz cuadrada (desviación estándar).

**Pregunta 8 (problema en contexto — decisión con dispersión).** Dos rutas de transporte al aeropuerto tienen el mismo tiempo promedio de viaje (45 minutos), pero la Ruta 1 tiene desviación estándar de 5 minutos y la Ruta 2 de 20 minutos. Si necesitas llegar con certeza a tiempo para tu vuelo, ¿qué ruta recomendarías, y por qué?

**Respuesta esperada:** la **Ruta 1**, porque su menor desviación estándar indica tiempos de viaje más predecibles y consistentes, reduciendo el riesgo de una demora inesperada, aunque ambas rutas compartan el mismo promedio.
*Retroalimentación:* cuando lo que importa no es solo el valor típico sino la certeza del resultado, la decisión correcta se basa en la dispersión, no solo en el promedio.

**Pregunta 9 (alternativas — fórmula).** ¿Cuál es la fórmula correcta de la probabilidad condicional P(A|B)?
a) P(A∩B) / P(B)
b) P(A∩B) / P(A)
c) P(A) × P(B)
d) P(A) + P(B) − P(A∩B)

**Respuesta correcta: a) P(A∩B) / P(B).**
*Retroalimentación:* la probabilidad condicional "reduce" el espacio muestral al evento que ya se sabe que ocurrió (B), por eso se divide por P(B).

**Pregunta 10 (verdadero o falso).** Si dos eventos A y B son independientes, entonces P(A|B) = P(A).

**Respuesta correcta: Verdadero.**
*Retroalimentación:* que dos eventos sean independientes significa exactamente eso: que saber que ocurrió B no cambia en nada la probabilidad de A.

**Pregunta 11 (calcular — árbol sin reposición).** En una bolsa hay 5 bolitas rojas y 3 azules. Se extraen dos bolitas al azar, sin reposición. Usando un diagrama de árbol, calcula la probabilidad de que ambas sean rojas.

**Respuesta esperada:** P(1ª roja)=5/8; P(2ª roja|1ª roja)=4/7. P(ambas rojas) = 5/8×4/7 = 20/56 = **5/14 ≈ 0,357 (35,7%)**.
*Retroalimentación:* en un diagrama de árbol, la probabilidad de una secuencia de eventos se obtiene multiplicando las probabilidades a lo largo de las ramas correspondientes; al no reponer, las probabilidades del segundo evento dependen del resultado del primero.

**Pregunta 12 (desarrollo — comparar con y sin reposición).** Repite el cálculo de la pregunta anterior, pero esta vez con reposición (se devuelve la bolita extraída antes de sacar la segunda). Compara el resultado con el de la pregunta 11.

**Respuesta esperada:** con reposición: P = 5/8×5/8 = 25/64 ≈ **0,391 (39,1%)**, un valor **mayor** que sin reposición (≈0,357). Esto ocurre porque, al reponer la bolita, la proporción de bolitas rojas se mantiene igual en la segunda extracción, mientras que sin reposición esa proporción disminuye levemente después de sacar una roja.
*Retroalimentación:* comparar ambos escenarios ayuda a entender por qué la independencia (con reposición) y la dependencia (sin reposición) entre eventos sucesivos producen resultados distintos, aunque parecidos.

**Pregunta 13 (leer datos — tabla de doble entrada).** Se encuesta a 150 personas sobre si practican deporte y si fuman:

| | Fuma | No fuma | Total |
|---|---|---|---|
| Practica deporte | 10 | 70 | 80 |
| No practica deporte | 25 | 45 | 70 |
| Total | 35 | 115 | 150 |

Calcula P(fuma | no practica deporte).

**Respuesta esperada:** dentro de la fila "no practica deporte" (70 personas), 25 fuman: P = 25/70 ≈ **0,357 (35,7%)**.
*Retroalimentación:* para leer una probabilidad condicional en una tabla de doble entrada, se trabaja únicamente con los datos de la fila (o columna) de la condición dada, dividiendo por su total.

**Pregunta 14 (desarrollo — misma tabla).** Usando la tabla de la pregunta 13, calcula P(practica deporte | no fuma).

**Respuesta esperada:** dentro de la columna "no fuma" (115 personas), 70 practican deporte: P = 70/115 ≈ **0,609 (60,9%)**.
*Retroalimentación:* el orden de la condición importa: aquí se condiciona sobre "no fuma" (columna), por lo que el total de referencia cambia respecto a la pregunta anterior.

**Pregunta 15 (problema en contexto — árbol con prueba médica).** Un examen médico tiene una sensibilidad del 95% (detecta correctamente a una persona enferma el 95% de las veces) y se aplica en una población donde el 5% está enferma. Describe el árbol de probabilidades y calcula P(enfermo y resultado positivo).

**Respuesta esperada:** P(enfermo y positivo) = P(enfermo)×P(positivo|enfermo) = 0,05×0,95 = **0,0475 (4,75%)**.
*Retroalimentación:* la rama del árbol que interesa es la que combina "estar enfermo" con "dar positivo", y su probabilidad se obtiene multiplicando las probabilidades a lo largo de esa rama específica.

**Pregunta 16 (problema no rutinario — combinar condicionales).** Una empresa de delivery en Santiago analiza sus pedidos: el 30% llega tarde cuando llueve, y solo el 8% llega tarde cuando no llueve. En la región llueve un 20% de los días. ¿Qué regla debes usar para calcular la probabilidad total de que un pedido llegue tarde (combinando ambos escenarios), y cuál es esa probabilidad?

**Respuesta esperada:** se usa la **regla de la probabilidad total**, sumando cada probabilidad condicional ponderada por la probabilidad de su escenario: P(tarde) = P(tarde|lluvia)×P(lluvia) + P(tarde|no lluvia)×P(no lluvia) = 0,30×0,20 + 0,08×0,80 = 0,06+0,064 = **0,124 (12,4%)**.
*Retroalimentación:* cuando un evento puede ocurrir bajo distintos escenarios (aquí, lluvia o no lluvia), su probabilidad total se obtiene combinando cada probabilidad condicional con la probabilidad de que ocurra ese escenario, tal como se ve en las ramas de un árbol de probabilidades.

**Pregunta 17 (comparar — sin calcular).** Se presentan dos evaluaciones de un mismo curso, ambas con promedio 5,0. En la evaluación 1, casi todas las notas están entre 4,5 y 5,5. En la evaluación 2, las notas se reparten ampliamente entre 2,0 y 7,0. ¿Cuál evaluación tiene mayor desviación estándar? Explica sin calcular.

**Respuesta esperada:** la **evaluación 2**, porque sus notas están mucho más alejadas del promedio (más dispersas), lo que se traduce en una mayor desviación estándar, aun cuando ambas evaluaciones comparten el mismo promedio.
*Retroalimentación:* no siempre es necesario calcular para comparar dispersión: describir visualmente qué tan "esparcidos" están los datos alrededor del promedio ya permite anticipar cuál desviación estándar es mayor.

**Pregunta 18 (calcular — tabla con incógnita).** Se encuesta a 100 personas sobre su preferencia musical (Cumbia o Rock) según edad (Joven o Adulto). Se sabe que hay 40 adultos en total, que 55 personas en total prefieren Rock, y que 15 de los adultos prefieren Cumbia. Calcula P(Rock | Adulto).

**Respuesta esperada:** de los 40 adultos, 15 prefieren Cumbia, por lo tanto 40−15=25 prefieren Rock. P(Rock|Adulto) = 25/40 = **0,625 (62,5%)**.
*Retroalimentación:* antes de calcular una probabilidad condicional a partir de una tabla incompleta, conviene completar primero los datos faltantes usando que las filas y columnas deben sumar sus totales correspondientes.

---

## Glosario

- **Función exponencial:** función de la forma f(x)=a·bˣ (con a>0, b>0, b≠1), donde a es el valor inicial y b es el factor de cambio por unidad de x; modela crecimiento (b>1) o decrecimiento (0<b<1).
- **Tasa de crecimiento/decrecimiento (r):** porcentaje de cambio por período, relacionado con el factor b mediante b=1+r (crecimiento) o b=1−r (decrecimiento).
- **Vida media (semidesintegración):** tiempo que demora una cantidad en reducirse exactamente a la mitad, en un modelo de decrecimiento exponencial.
- **Función logarítmica:** función y=log_b(x), inversa de la función exponencial b^x; permite despejar el exponente cuando se conoce el valor final de un modelo exponencial.
- **Ángulo central:** ángulo con vértice en el centro de una circunferencia; su medida es igual a la del arco que subtiende.
- **Ángulo inscrito:** ángulo con vértice en la circunferencia, formado por dos cuerdas; mide la mitad del arco que subtiende.
- **Ángulo semiinscrito:** ángulo formado por una tangente y una cuerda que se cortan en el punto de tangencia; mide la mitad del arco que abarca.
- **Cuerda:** segmento que une dos puntos de una circunferencia.
- **Secante:** recta que corta a una circunferencia en dos puntos.
- **Tangente:** recta que toca a una circunferencia en un único punto, siempre perpendicular al radio en ese punto.
- **Arco:** porción de una circunferencia, medida en grados al igual que un ángulo.
- **Rango:** medida de dispersión más simple, igual a la diferencia entre el valor máximo y el mínimo de un conjunto de datos.
- **Varianza (σ²):** promedio de las desviaciones al cuadrado de los datos respecto a su media; mide la dispersión en unidades al cuadrado.
- **Desviación estándar (σ):** raíz cuadrada de la varianza; mide la dispersión típica de los datos, en las mismas unidades que los datos originales.
- **Probabilidad condicional P(A|B):** probabilidad de que ocurra un evento A, dado que ya se sabe que ocurrió un evento B; se calcula como P(A∩B)/P(B).
- **Diagrama de árbol:** representación gráfica de eventos sucesivos, donde las probabilidades a lo largo de cada rama se multiplican para obtener la probabilidad de esa secuencia completa.
- **Tabla de doble entrada (o de contingencia):** tabla que cruza dos variables categóricas, útil para leer directamente probabilidades condicionales dividiendo un valor de la tabla por el total de su fila o columna correspondiente.
