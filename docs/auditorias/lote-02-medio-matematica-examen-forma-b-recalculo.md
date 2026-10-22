# Lote 2.º medio — recálculo de examen de Matemática Forma B

**Fecha:** 2026-10-21  
**Archivo revisado:** `contenido/02-medio/examenes/matematica-examen-forma-b.md`  
**Alcance:** revisión independiente de enunciados, operaciones y pauta en la fuente Markdown. No incluye cotejo oficial de OA, comparación real con Forma A, render/importación en la app ni validación docente externa.  
**Estado:** revisión parcial con un hallazgo P1 confirmado; no certificado.

## Hallazgo P1 — clave de la pregunta 14 contradictoria

La pregunta 14 pide la inversa de \(f(x)=x+10\). La alternativa a) declara \(f^{-1}(x)=x-10\), que es la inversa correcta. Sin embargo, la pauta dice literalmente: **“a) f⁻¹(x) = x + 10”**, contradiciendo la propia alternativa y el cálculo correcto. La explicación entre paréntesis también está redactada de forma confusa: “deshace la resta de... suma de 10”.

**Impacto:** una clave contradictoria puede enseñar una regla incorrecta o perjudicar la corrección automática/manual.  
**Recomendación:** proponer que la pauta indique \(f^{-1}(x)=x-10\) y explicar: si \(y=x+10\), se intercambian variables y se despeja \(y=x-10\). No se modificó el material fuente en esta fase.

## Revisión de cálculo de los 25 ítems

| Pregunta | Resultado de control independiente | Estado |
|---:|---|---|
| 1 | \(\sqrt{300}=10\sqrt3\), alternativa a | Coincide |
| 2 | \(12/\sqrt6=2\sqrt6\), alternativa a | Coincide |
| 3 | \(\log_2 64-\log_2 4=6-2=4\) | Coincide |
| 4 | Lado \(\sqrt{363}=11\sqrt3\approx19,05\) m | Coincide |
| 5 | \(\log_3 81=4\), alternativa a | Coincide |
| 6 | \(\sqrt[5]{2^7}=2^{7/5}\), alternativa a | Coincide |
| 7 | \(27^{2/3}=(\sqrt[3]{27})^2=9\) | Coincide |
| 8 | \(-\log(10^{-4})=4\) | Coincide |
| 9 | Vértice: coordenada \(x=-2\), alternativa a | Coincide |
| 10 | Coeficiente cuadrático positivo: concavidad hacia arriba y mínimo, alternativa a | Coincide |
| 11 | Raíces −4 y 3; vértice \((-0,5;-12,25)\) | Coincide |
| 12 | Máximo en \(x=6\): precio $600; ganancia $32.000 | Coincide |
| 13 | En \(x=1\), RHS=2 y 3>2; el punto pertenece | Coincide |
| 14 | Inversa correcta \(x-10\); pauta escribe \(x+10\) | **Hallazgo P1** |
| 15 | Inversa de \(7x\): \(x/7\), alternativa a | Coincide |
| 16 | Inversa de \(3x-9\): \((x+9)/3\) | Coincide |
| 17 | Para dominio original \(x\ge0\), inversa \(\sqrt{x+5}\), con dominio \(x\ge-5\) | Coincide |
| 18 | \(\sin\theta=8/17\approx0,47\), alternativa a | Coincide |
| 19 | \(12\tan30^\circ\approx6,93\) cm, alternativa a | Coincide |
| 20 | \(25\sin40^\circ\approx16,07\) cm | Coincide |
| 21 | \(60\tan22^\circ\approx24,24\) m | Coincide |
| 22 | Principio multiplicativo: \(5\times3=15\), alternativa a | Coincide |
| 23 | \(8!/6!=8\times7=56\), alternativa a | Coincide |
| 24 | Seis letras distintas: \(6!=720\) | Coincide |
| 25 | \(\binom{10}{4}=210\) grupos | Coincide |

## Controles adicionales de coherencia

- La suma declarada en el resumen de ejes es 8 + 9 + 4 + 4 = 25 preguntas.
- El texto indica 12 preguntas de alternativas y 13 de desarrollo; la clasificación de los ítems coincide con ese conteo.
- La afirmación de que replica la distribución habitual de Mineduc y que todas las preguntas son originales **no queda demostrada** por esta revisión y requiere fuentes/comparación específica.
- La asignación de OA 1, 2, 3, 5, 8 y 11 se leyó como declaración de la pauta; todavía no se cotejó contra Bases Curriculares oficiales vigentes ni se comprobó que cada ítem mida el OA indicado.
- La pregunta 12 usa ganancia en miles de pesos y precio en cientos de pesos; el cálculo es coherente si se interpreta así, como declara el enunciado.

## Pendientes antes de cerrar el lote

1. Contrastar cada OA con fuente oficial de Mineduc/UCE y registrar URL/versión/evidencia.
2. Revisar criterios de puntaje parcial para las 13 preguntas de desarrollo.
3. Comparar enunciados, datos, habilidades y dificultad con Forma A; no basta la afirmación incluida al final del archivo.
4. Verificar importación, render, selección de alternativas, corrección y persistencia de resultados en la aplicación.
5. Tras autorización, corregir la pauta de la pregunta 14 y agregar prueba de regresión.

**Conclusión:** 24 de los 25 ítems no presentaron discrepancia de cálculo en esta pasada; la pregunta 14 sí tiene una contradicción explícita entre alternativa correcta y pauta. Esto no equivale a certificar todo el examen.
