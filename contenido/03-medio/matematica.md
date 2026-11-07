---
título: Matemática — 3° Medio
asignatura: Matemática
curso: 3° Medio
tipo: Guía de estudio
basado_en: Bases Curriculares, Decreto 193/2019 "Plan Común" (Mineduc/UCE) — temario oficial del Examen Libre de Validación de Estudios
oa_evaluados: OA 2, OA 3, OA 4
ultima_actualizacion: 2026-10-28
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

**Pregunta 2 (verdadero o falso).** En un modelo exponencial f(x) = a·bˣ con a>0 y b>1, la tasa de crecimiento porcentual por unidad de x aumenta cuando aumenta b.

**Respuesta correcta: Verdadero.**
*Retroalimentación:* b representa el factor multiplicativo por unidad de x; un b más grande implica multiplicar por una cantidad mayor en cada período, acelerando el crecimiento.

**Pregunta 3 (calcular).** Si el factor de crecimiento de un modelo exponencial es b = 1,08, ¿cuál es la tasa de crecimiento porcentual?
a) 0,08%
b) 8%
c) 108%
d) 1,08%

**Respuesta correcta: b) 8%.**
*Retroalimentación:* como b=1+r, entonces r = 0,08 = 8%; b siempre se descompone en "1" (lo que ya había) más la tasa de cambio r.

**Pregunta 4 (alternativas — completar).** En A(t) = P × (1 + r)ᵗ, ¿qué representan P, r y t?
a) P: número de períodos; r: capital inicial; t: interés ganado en cada período
b) P: tasa de interés por período; r: capital inicial; t: monto final acumulado
c) P: monto final acumulado; r: tiempo en años; t: tasa de interés por período
d) P: capital inicial; r: tasa de interés por período (decimal); t: número de períodos

**Respuesta correcta: d) P: capital inicial; r: tasa de interés por período (decimal); t: número de períodos.**
*Retroalimentación:* en el interés compuesto, el capital inicial se multiplica por (1 + r) en cada período.

**Pregunta 5 (alternativas — depreciación).** Un auto de $12.000.000 se deprecia un 12% anual según V(t) = 12.000.000 · (0,88)ᵗ. ¿Cuál es su valor aproximado a los 4 años?
a) ≈ $6.240.000
b) ≈ $10.560.000
c) ≈ $2.488.000
d) ≈ $7.196.344

**Respuesta correcta: d) ≈ $7.196.344.**
*Retroalimentación:* (0,88)⁴ ≈ 0,5997; conviene redondear solo al final. $6.240.000 resulta de restar 4 · 12% de forma lineal.

**Pregunta 6 (alternativas — vida media).** El carbono-14 tiene una vida media de unos 5.730 años. Si una muestra tiene 80 g, ¿cuánto quedará tras 11.460 años?
a) 10 g
b) 20 g
c) 40 g
d) 60 g

**Respuesta correcta: b) 20 g.**
*Retroalimentación:* 11.460 años son 2 vidas medias: 80 · (1/2)² = 20 g.

**Pregunta 7 (alternativas — despejar el tiempo).** Un rumor se difunde según M(t) = 50 · (1,6)ᵗ (t en horas). ¿Después de cuántas horas lo habrán visto unas 800 personas?
a) ≈ 16 horas
b) ≈ 10 horas
c) ≈ 6 horas
d) ≈ 3 horas

**Respuesta correcta: c) ≈ 6 horas.**
*Retroalimentación:* (1,6)ᵗ = 16, t = log 16 / log 1,6 ≈ 1,2041/0,2041 ≈ 5,9.

**Pregunta 8 (alternativas — dominio del modelo).** Un estanque de 5.000 L se llena según V(t) = 200 · (1,25)ᵗ. ¿Para qué valores de t tiene sentido el modelo?
a) Solo para t = 25, el número de horas
b) Para todo t ≥ 0, sin ningún límite
c) 0 ≤ t ≤ 14,4 horas aproximadamente
d) 0 ≤ t ≤ 25 horas, porque 5.000/200 = 25

**Respuesta correcta: c) 0 ≤ t ≤ 14,4 horas aproximadamente.**
*Retroalimentación:* (1,25)ᵗ = 25 → t ≈ 14,4; después el estanque ya está lleno.

**Pregunta 9 (alternativas — comparar parámetros).** ¿Cuál crece más rápido: f(x) = 100 · (1,1)ˣ o g(x) = 100 · (1,05)ˣ?
a) g, porque 1,05 está más cerca de 1 y por eso crece de forma más estable y rápida
b) Crecen igual, porque ambas funciones parten del mismo valor inicial de 100
c) Ninguno crece, porque ambos factores son muy cercanos a 1 y el valor se mantiene
d) f, porque con el mismo valor inicial su factor (10% por período) es mayor

**Respuesta correcta: d) f, porque con el mismo valor inicial su factor (10% por período) es mayor.**
*Retroalimentación:* con igual valor inicial, manda el factor de crecimiento.

**Pregunta 10 (alternativas — leer datos).** Una colonia de pingüinos registra: t = 0 → 80; t = 1 → 96; t = 2 → 115; t = 3 → 138. ¿Corresponde a un modelo exponencial?
a) No: las diferencias entre términos consecutivos no son constantes
b) Sí: la razón entre términos consecutivos es casi constante (≈ 1,2)
c) Sí: las diferencias entre términos consecutivos son constantes (+16)
d) No: la población disminuye con el tiempo, así que es un modelo decreciente

**Respuesta correcta: b) Sí: la razón entre términos consecutivos es casi constante (≈ 1,2).**
*Retroalimentación:* 96/80 = 1,20; 115/96 ≈ 1,198; 138/115 ≈ 1,20 (20% por período).

**Pregunta 11 (alternativas — modelo logarítmico aplicado).** El nivel de un sonido, en decibeles, se calcula como L = 10·log₁₀(I/I₀). Si la razón I/I₀ = 1.000, ¿cuál es el nivel L?
a) 300 dB
b) 3 dB
c) 1.000 dB
d) 30 dB

**Respuesta correcta: d) 30 dB.**
*Retroalimentación:* log₁₀(1.000) = 3, porque 10³=1.000; entonces L = 10×3 = 30.

**Pregunta 12 (alternativas — decrecimiento porcentual).** Un medicamento se elimina según C(t) = 250 · (0,8)ᵗ (mg). ¿Cuánto queda a las 3 horas y qué porcentaje se eliminó?
a) 190 mg; 24%
b) 128 mg; 51,2%
c) 128 mg; 48,8%
d) 50 mg; 80%

**Respuesta correcta: c) 128 mg; 48,8%.**
*Retroalimentación:* (0,8)³ = 0,512 → 128 mg; se eliminaron 122 mg, es decir 48,8% (51,2% es lo que queda).

**Pregunta 13 (verdadero o falso).** Si b=1 en un modelo f(x)=a·bˣ, el modelo representa una situación de crecimiento.

**Respuesta correcta: Falso.**
*Retroalimentación:* cuando b=1, la cantidad se multiplica por 1 en cada período, es decir, se mantiene **constante**; no hay crecimiento ni decrecimiento.

**Pregunta 14 (alternativas — logaritmo — decrecimiento).** Una población de peces disminuye según N(t) = 3.000 · (0,9)ᵗ. ¿En cuántos años bajará aproximadamente a la mitad?
a) ≈ 1,5 años
b) ≈ 5 años
c) ≈ 6,6 años
d) ≈ 10 años

**Respuesta correcta: c) ≈ 6,6 años.**
*Retroalimentación:* (0,9)ᵗ = 0,5 → t = log 0,5 / log 0,9 ≈ 6,6.

**Pregunta 15 (alternativas — construir y proyectar).** Una app tiene 2.000 usuarios al lanzarse y crece un 30% diario. ¿Qué modelo la describe y cuántos usuarios tendrá aprox. a los 10 días?
a) U(t) = 2.000 + 0,3t; ≈ 2.003
b) U(t) = 2.000 · (0,3)ᵗ; ≈ 0
c) U(t) = 2.000 · 1,3 · t; ≈ 26.000
d) U(t) = 2.000 · (1,3)ᵗ; ≈ 27.572

**Respuesta correcta: d) U(t) = 2.000 · (1,3)ᵗ; ≈ 27.572.**
*Retroalimentación:* (1,3)¹⁰ ≈ 13,786.

**Pregunta 16 (alternativas — modelo desde dos datos).** Una población de conejos pasó de 50 a 135 en 3 años con crecimiento exponencial. ¿Cuál es la tasa anual aproximada?
a) ≈ 57%
b) ≈ 39,2%
c) ≈ 170%
d) ≈ 2,7%

**Respuesta correcta: b) ≈ 39,2%.**
*Retroalimentación:* (1 + r)³ = 2,7 → 1 + r = ∛2,7 ≈ 1,392; 57% resulta de repartir el aumento total de forma lineal.

**Pregunta 17 (alternativas — comparar crecimiento y decrecimiento).** Desde 1.000, f crece 10% anual y g decrece 10% anual. A los 5 años, ¿cuál se aleja más de 1.000?
a) g se aleja más que f, porque al decrecer pierde más de lo que f gana al crecer
b) Se alejan exactamente lo mismo, porque el porcentaje de cambio es igual (10%)
c) f (≈ 1.610,5, sube 610,5) más que g (≈ 590,5, baja 409,5)
d) Ninguno se aleja, porque los aumentos y las disminuciones se compensan cada año

**Respuesta correcta: c) f (≈ 1.610,5, sube 610,5) más que g (≈ 590,5, baja 409,5).**
*Retroalimentación:* no son simétricos: el crecimiento compuesto se acelera y el decrecimiento nunca puede bajar de 0.

**Pregunta 18 (alternativas — distinguir de un modelo lineal).** Un bien vale: t = 0 → 100; t = 1 → 150; t = 2 → 200; t = 3 → 250. ¿Es crecimiento exponencial?
a) No: decrece
b) Sí: las razones entre valores consecutivos son constantes
c) Sí: crece cada vez más rápido, porque cada valor es mayor
d) No: las diferencias son constantes (+50), así que es lineal

**Respuesta correcta: d) No: las diferencias son constantes (+50), así que es lineal.**
*Retroalimentación:* las razones (1,5; 1,33; 1,25) no son iguales.

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
a) 50°
b) 65°
c) 130°
d) 260°

**Respuesta correcta: c) 130°.**
*Retroalimentación:* un ángulo central es siempre igual, en grados, al arco que subtiende.

**Pregunta 2 (verdadero o falso).** El ángulo inscrito que subtiende el mismo arco que un ángulo central de 90° mide 45°.

**Respuesta correcta: Verdadero.**
*Retroalimentación:* el ángulo inscrito equivale a la mitad del ángulo central sobre el mismo arco: 90°÷2=45°.

**Pregunta 3 (calcular).** Un ángulo inscrito mide 35°. ¿Cuánto mide el arco que subtiende?
a) 17,5°
b) 35°
c) 70°
d) 140°

**Respuesta correcta: c) 70°.**
*Retroalimentación:* como el ángulo inscrito es la mitad del arco, el arco es el doble del ángulo inscrito: 35°×2=70°.

**Pregunta 4 (alternativas — completar).** El ángulo ___ tiene su vértice en el centro y mide lo mismo que su arco; el ángulo ___ tiene su vértice en la circunferencia y mide la mitad del arco.
a) inscrito; central
b) exterior; interior
c) recto; agudo
d) central; inscrito

**Respuesta correcta: d) central; inscrito.**
*Retroalimentación:* el inscrito mide la mitad del central que subtiende el mismo arco.

**Pregunta 5 (alternativas — ángulo interior).** Dos cuerdas se cortan dentro de una circunferencia; los arcos que abarcan miden 100° y 40°. ¿Cuánto mide el ángulo formado?
a) 30°
b) 70°
c) 140°
d) 60°

**Respuesta correcta: b) 70°.**
*Retroalimentación:* el ángulo interior es la semisuma de los arcos: (100° + 40°)/2.

**Pregunta 6 (alternativas — segmentos de cuerdas).** Dos cuerdas se cortan: una tiene segmentos de 5 y 8 cm; la otra, uno de 4 cm. ¿Cuánto mide el segmento restante?
a) 9 cm
b) 6,4 cm
c) 10 cm
d) 2,5 cm

**Respuesta correcta: c) 10 cm.**
*Retroalimentación:* 5 · 8 = 4 · x → x = 10.

**Pregunta 7 (alternativas — ángulo exterior).** Dos secantes desde un punto exterior interceptan arcos de 150° y 50°. ¿Cuánto mide el ángulo en el punto exterior?
a) 50°
b) 100°
c) 200°
d) 75°

**Respuesta correcta: a) 50°.**
*Retroalimentación:* el ángulo exterior es la semidiferencia: (150° − 50°)/2.

**Pregunta 8 (alternativas — secante-secante).** Una secante tiene parte externa de 5 cm y longitud total de 20 cm; otra tiene parte externa de 4 cm. ¿Cuál es su longitud total?
a) 16 cm
b) 19 cm
c) 25 cm
d) 80 cm

**Respuesta correcta: c) 25 cm.**
*Retroalimentación:* 5 · 20 = 4 · x → x = 25.

**Pregunta 9 (alternativas — tangente-secante).** Desde un punto exterior, una tangente mide 12 cm y una secante tiene parte externa de 8 cm. ¿Cuánto mide la secante completa?
a) 12 cm
b) 18 cm
c) 1,5 cm
d) 20 cm

**Respuesta correcta: b) 18 cm.**
*Retroalimentación:* tangente² = externa · completa: 144 = 8x → x = 18.

**Pregunta 10 (alternativas — leer datos).** El arco menor AB mide 76°. ¿Cuánto mide el ángulo inscrito ACB, con C en el arco mayor?
a) 76°
b) 152°
c) 38°
d) 142°

**Respuesta correcta: c) 38°.**
*Retroalimentación:* un ángulo inscrito mide la mitad del arco que subtiende.

**Pregunta 11 (alternativas — ángulo semiinscrito).** Una tangente y una cuerda se cortan en el punto de tangencia, formando un ángulo semiinscrito que abarca un arco de 96°. ¿Cuánto mide ese ángulo?
a) 192°
b) 96°
c) 48°
d) 24°

**Respuesta correcta: c) 48°.**
*Retroalimentación:* el ángulo semiinscrito, igual que el inscrito, mide la mitad del arco que abarca: 96°÷2=48°.

**Pregunta 12 (verdadero o falso).** En un triángulo inscrito en una circunferencia donde uno de sus lados es un diámetro, el ángulo opuesto a ese diámetro siempre mide 90°.

**Respuesta correcta: Verdadero.**
*Retroalimentación:* ese ángulo es un ángulo inscrito que subtiende una semicircunferencia (arco de 180°), por lo tanto mide ½×180°=90° (este resultado también se conoce como Teorema de Tales aplicado a la circunferencia).

**Pregunta 13 (alternativas — rueda de la fortuna).** El ángulo central entre dos cabinas es 60°. Un operador las observa desde un punto del borde opuesto. ¿Qué ángulo inscrito forma?
a) 30°
b) 60°
c) 90°
d) 120°

**Respuesta correcta: a) 30°.**
*Retroalimentación:* el inscrito mide la mitad del central: 60°/2.

**Pregunta 14 (alternativas — plaza circular).** Dos caminos (secantes) desde un punto exterior delimitan arcos de 120° y 40°. ¿Qué ángulo forman donde se juntan?
a) 160°
b) 80°
c) 60°
d) 40°

**Respuesta correcta: d) 40°.**
*Retroalimentación:* semidiferencia de los arcos: (120° − 40°)/2.

**Pregunta 15 (alternativas — cables de un puente).** Dos cables que actúan como cuerdas se cruzan: uno con segmentos de 6 y 10 m, el otro con uno de 5 m. ¿Cuánto mide el otro segmento?
a) 12 m
b) 11 m
c) 8,3 m
d) 3 m

**Respuesta correcta: a) 12 m.**
*Retroalimentación:* 6 · 10 = 5 · x → x = 12.

**Pregunta 16 (alternativas — reserva marina).** Una secante tiene parte externa de 6 millas y longitud total de 15 millas. Desde el mismo punto, ¿cuánto mide la tangente a la reserva?
a) 9 millas
b) 90 millas
c) √90 ≈ 9,49 millas
d) √21 ≈ 4,58 millas

**Respuesta correcta: c) √90 ≈ 9,49 millas.**
*Retroalimentación:* tangente² = 6 · 15 = 90.

**Pregunta 17 (alternativas — comparar).** ¿Qué relación se cumple siempre entre un ángulo central y un inscrito que subtienden el mismo arco?
a) El inscrito mide la mitad del central
b) Miden lo mismo, porque comparten el arco
c) El inscrito mide el doble del central
d) Depende de la medida del arco

**Respuesta correcta: a) El inscrito mide la mitad del central.**
*Retroalimentación:* la relación de 1 a 2 se mantiene para cualquier arco.

**Pregunta 18 (alternativas — justificar).** ¿Por qué dos segmentos tangentes trazados desde un mismo punto exterior a una circunferencia miden lo mismo?
a) Porque todas las rectas que tocan una circunferencia miden lo mismo, ya que cada una corta a la circunferencia en dos puntos a igual distancia del centro
b) Porque los segmentos son paralelos entre sí y el punto exterior está a la misma distancia de ambos, lo que forma un paralelogramo con el centro
c) Solo es una coincidencia sin justificación: ocurre en algunos dibujos, pero si el punto exterior se aleja, un segmento queda más largo que el otro
d) Porque el radio es perpendicular a cada tangente y se forman dos triángulos rectángulos congruentes (misma hipotenusa y catetos iguales al radio)

**Respuesta correcta: d) Porque el radio es perpendicular a cada tangente y se forman dos triángulos rectángulos congruentes (misma hipotenusa y catetos iguales al radio).**
*Retroalimentación:* los otros catetos de esos triángulos congruentes son justamente los segmentos tangentes.

**Pregunta 19 (alternativas — arco como fracción).** Un arco corresponde a 1/6 de la circunferencia. ¿Cuánto mide su ángulo central?
a) 30°
b) 60°
c) 6°
d) 120°

**Respuesta correcta: b) 60°.**
*Retroalimentación:* 360° ÷ 6 = 60°.

**Pregunta 20 (alternativas — suma de arcos).** Cuatro arcos que completan una circunferencia miden 90°, 70°, x° y 110°. ¿Cuánto vale x?
a) 270°
b) 100°
c) 90°
d) 180°

**Respuesta correcta: c) 90°.**
*Retroalimentación:* 360° − (90° + 70° + 110°) = 90°.

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
a) 20
b) 11
c) 9
d) 5

**Respuesta correcta: b) 11.**
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
**Nota conceptual:** en este nivel escolar se calcula la varianza poblacional, dividiendo la suma de desviaciones cuadráticas entre el número total de observaciones N.

**Pregunta 4 (alternativas — completar).** La varianza es el promedio de los ___ de las desviaciones respecto a la media, y la desviación estándar es su ___.
a) cuadrados; raíz cuadrada
b) valores absolutos; cuadrado
c) inversos; doble
d) logaritmos; potencia

**Respuesta correcta: a) cuadrados; raíz cuadrada.**
*Retroalimentación:* elevar al cuadrado evita que las desviaciones positivas y negativas se anulen.

**Pregunta 5 (alternativas — comparar dispersión).** Dos cursos tienen promedio 5,5; el curso A tiene desviación estándar 0,4 y el B, 1,3. ¿Cuál tuvo resultados más homogéneos?
a) El curso B, porque su desviación es mayor y sus notas se repiten más
b) Ambos por igual, porque tienen el mismo promedio y eso define la homogeneidad
c) No se puede saber sin conocer la nota más alta de cada curso
d) El curso A, porque sus notas están más concentradas en torno al promedio

**Respuesta correcta: d) El curso A, porque sus notas están más concentradas en torno al promedio.**
*Retroalimentación:* menor desviación estándar indica resultados más parejos.

**Pregunta 6 (alternativas — rango en contexto).** Ventas diarias de tomate (kg): 40, 45, 38, 42, 50, 35, 48. ¿Cuál es el rango?
a) 12 kg
b) 15 kg
c) 42,6 kg
d) 50 kg

**Respuesta correcta: b) 15 kg.**
*Retroalimentación:* máximo 50 − mínimo 35 = 15.

**Pregunta 7 (alternativas — varianza y desviación estándar).** Tiempos de 4 trámites (min): 10, 12, 14, 16. ¿Cuáles son la varianza y la desviación estándar?
a) Varianza 20; desviación ≈ 4,47 min
b) Varianza 2,24; desviación 5 min
c) Varianza 5; desviación ≈ 2,24 min
d) Varianza 13; desviación ≈ 3,61 min

**Respuesta correcta: c) Varianza 5; desviación ≈ 2,24 min.**
*Retroalimentación:* media 13; cuadrados de las desviaciones 9, 1, 1, 9 (suma 20); 20/4 = 5 y √5 ≈ 2,24.

**Pregunta 8 (alternativas — decisión con dispersión).** Dos rutas al aeropuerto promedian 45 min; la Ruta 1 tiene desviación estándar 5 min y la Ruta 2, 20 min. Si necesitas llegar con certeza, ¿cuál conviene?
a) La Ruta 1, porque sus tiempos son más predecibles
b) La Ruta 2, porque su desviación es mayor
c) Da lo mismo, porque el promedio es igual
d) Ninguna, porque ambas tardan 45 min en promedio

**Respuesta correcta: a) La Ruta 1, porque sus tiempos son más predecibles.**
*Retroalimentación:* con igual promedio, la menor dispersión reduce el riesgo de una demora inesperada.

**Pregunta 9 (alternativas — fórmula).** ¿Cuál es la fórmula correcta de la probabilidad condicional P(A|B)?
a) P(A∩B) / P(B)
b) P(A∩B) / P(A)
c) P(A) × P(B)
d) P(A) + P(B) − P(A∩B)

**Respuesta correcta: a) P(A∩B) / P(B).**
*Retroalimentación:* la probabilidad condicional "reduce" el espacio muestral al evento que ya se sabe que ocurrió (B), por eso se divide por P(B).

**Pregunta 10 (verdadero o falso).** Si dos eventos A y B son independientes y P(B)>0, entonces P(A|B) = P(A).

**Respuesta correcta: Verdadero.**
*Retroalimentación:* que dos eventos sean independientes significa exactamente eso: que saber que ocurrió B no cambia en nada la probabilidad de A.

**Pregunta 11 (alternativas — árbol sin reposición).** En una bolsa hay 5 bolitas rojas y 3 azules; se sacan dos sin reposición. ¿Cuál es la probabilidad de que ambas sean rojas?
a) 25/64 ≈ 39,1%
b) 5/8
c) 1/2
d) 5/14 ≈ 35,7%

**Respuesta correcta: d) 5/14 ≈ 35,7%.**
*Retroalimentación:* 5/8 · 4/7 = 20/56 = 5/14.

**Pregunta 12 (alternativas — con y sin reposición).** Con la misma bolsa, pero con reposición, ¿cuál es la probabilidad de dos rojas y cómo se compara con el caso sin reposición?
a) 25/64 ≈ 39,1%, menor que sin reposición
b) 25/64 ≈ 39,1%, mayor que sin reposición
c) 5/14, igual que sin reposición
d) 20/56, mayor que sin reposición

**Respuesta correcta: b) 25/64 ≈ 39,1%, mayor que sin reposición.**
*Retroalimentación:* al reponer, la proporción de rojas se mantiene; sin reposición disminuye tras sacar una roja.

**Pregunta 13 (alternativas — tabla de doble entrada).** Se encuesta a 150 personas:

| | Fuma | No fuma | Total |
|---|---|---|---|
| Practica deporte | 10 | 70 | 80 |
| No practica deporte | 25 | 45 | 70 |
| Total | 35 | 115 | 150 |

¿Cuánto vale P(fuma | no practica deporte)?
a) 25/35 ≈ 71,4%
b) 25/150 ≈ 16,7%
c) 25/70 ≈ 35,7%
d) 45/70 ≈ 64,3%

**Respuesta correcta: c) 25/70 ≈ 35,7%.**
*Retroalimentación:* se restringe a la fila "no practica deporte" (70 personas).

**Pregunta 14 (alternativas — misma tabla).** Se encuesta a 150 personas:

| | Fuma | No fuma | Total |
|---|---|---|---|
| Practica deporte | 10 | 70 | 80 |
| No practica deporte | 25 | 45 | 70 |
| Total | 35 | 115 | 150 |

¿Cuánto vale P(practica deporte | no fuma)?
a) 70/115 ≈ 60,9%
b) 70/80 = 87,5%
c) 70/150 ≈ 46,7%
d) 45/115 ≈ 39,1%

**Respuesta correcta: a) 70/115 ≈ 60,9%.**
*Retroalimentación:* se restringe a la columna "no fuma" (115 personas).

**Pregunta 15 (alternativas — árbol con prueba médica).** Un examen detecta al 95% de los enfermos y se aplica donde el 5% está enfermo. ¿Cuánto vale P(enfermo y positivo)?
a) 0,95
b) 0,05
c) 1
d) 0,0475 (4,75%)

**Respuesta correcta: d) 0,0475 (4,75%).**
*Retroalimentación:* P(enfermo) · P(positivo | enfermo) = 0,05 · 0,95.

**Pregunta 16 (alternativas — probabilidad total).** El 30% de los pedidos llega tarde cuando llueve y el 8% cuando no llueve; llueve el 20% de los días. ¿Qué regla se usa y cuál es la probabilidad de que un pedido llegue tarde?
a) Regla aditiva de eventos excluyentes: 30% + 8% = 38%
b) Probabilidad total: 0,30 · 0,20 + 0,08 · 0,80 = 12,4%
c) Promedio ponderado de los casos: (30% + 8%)/2 = 19%
d) Regla multiplicativa de eventos independientes: 30% · 8% = 2,4%

**Respuesta correcta: b) Probabilidad total: 0,30 · 0,20 + 0,08 · 0,80 = 12,4%.**
*Retroalimentación:* cada probabilidad condicional se pondera por la probabilidad de su escenario.

**Pregunta 17 (alternativas — comparar sin calcular).** Dos evaluaciones con promedio 5,0: en la 1 casi todas las notas están entre 4,5 y 5,5; en la 2, entre 2,0 y 7,0. ¿Cuál tiene mayor desviación estándar?
a) La evaluación 1
b) Ambas iguales, porque tienen el mismo promedio de 5,0
c) La evaluación 2, porque sus notas están más dispersas
d) No se puede saber sin calcular cada nota por separado

**Respuesta correcta: c) La evaluación 2, porque sus notas están más dispersas.**
*Retroalimentación:* mayor alejamiento del promedio implica mayor desviación estándar.

**Pregunta 18 (alternativas — tabla con incógnita).** De 100 personas, 40 son adultos, 55 prefieren Rock y 15 adultos prefieren Cumbia. ¿Cuánto vale P(Rock | Adulto)?
a) 25/40 = 62,5%
b) 55/100 = 55%
c) 25/55 ≈ 45,5%
d) 15/40 = 37,5%

**Respuesta correcta: a) 25/40 = 62,5%.**
*Retroalimentación:* de los 40 adultos, 40 − 15 = 25 prefieren Rock.

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
