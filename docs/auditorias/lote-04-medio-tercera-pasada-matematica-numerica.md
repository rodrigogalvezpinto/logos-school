# Tercera pasada — verificación numérica de Matemática, 4.º medio (Forma B)

**Rama:** `qa/fase-2-matriz-trazabilidad`  
**Archivo revisado:** `contenido/04-medio/examenes/matematica-examen-forma-b.md` y conceptos relacionados en `contenido/04-medio/matematica.md`.  
**Método:** recálculo independiente de preguntas numéricas seleccionadas. No se editó el examen ni se certificó el resto de las preguntas.

## Resultados de recálculo

### LGS-4M-MAT-EVAL-001 — Interés compuesto
- **Pregunta 5:** capital $900.000, tasa anual 4%, plazo 5 años.
- **Cálculo:** (900.000(1,04)^5 = 1.094.399,63).
- **Resultado esperado:** aproximadamente **$1.094.400**, según redondeo al peso.
- **Estado:** cálculo verificado.

### LGS-4M-MAT-EVAL-002 — Tasa efectiva anual
- **Pregunta 6:** tasa nominal anual 20%, capitalización mensual.
- **Cálculo:** ((1+0,20/12)^{12}-1 approx 0,21939).
- **Resultado esperado:** aproximadamente **21,94% TEA**.
- **Estado:** cálculo verificado; la pauta debe mostrar la fórmula y redondeo.

### LGS-4M-MAT-EVAL-003 — Poder adquisitivo real
- **Pregunta 8:** sueldo pasa de $600.000 a $624.000 (+4%); IPC acumulado 6%.
- **Cálculo:** variación real aproximada = (1,04/1,06-1 approx -1,89%).
- **Resultado esperado:** el poder adquisitivo **disminuyó aproximadamente 1,89%**. La resta simple de porcentajes da −2 puntos porcentuales como aproximación, no el cambio real exacto.
- **Estado:** resultado verificado; conviene distinguir aproximación de cálculo real.

### LGS-4M-MAT-EVAL-004 — Función potencia
- **Pregunta 13:** (f(x)=5x^4), evaluar en 1 y 3.
- **Cálculo:** (f(1)=5), (f(3)=5cdot81=405); factor de aumento (405/5=81).
- **Resultado esperado:** 5, 405 y factor **81**.
- **Estado:** cálculo verificado.

### LGS-4M-MAT-EVAL-005 — Intensidad inversamente proporcional al cuadrado
- **Pregunta 14:** (I(d)=1200/d^2).
- **Cálculo:** (I(2)=300); (I(8)=18,75); a 2 m la intensidad modelada es 16 veces la de 8 m.
- **Estado:** cálculo verificado.

### LGS-4M-MAT-EVAL-006 — Modelo trigonométrico
- **Pregunta 15:** (T(t)=3\cos((\pi/12)t)+27).
- **Resultado esperado:** máximo 30 °C, mínimo 24 °C y período (2\pi/(\pi/12)=24) horas.
- **Estado:** cálculo verificado.

### LGS-4M-MAT-EVAL-007 — Probabilidad binomial
- **Pregunta 21:** 8 preguntas independientes, (p=0,5), exactamente 6 aciertos.
- **Cálculo:** (inom{8}{6}(0,5)^6(0,5)^2=28/256=0,109375).
- **Resultado esperado:** **10,9375%** (aprox. 10,94%).
- **Estado:** cálculo verificado.

### LGS-4M-MAT-EVAL-008 — Distribución binomial: esperanza y desviación estándar
- **Pregunta 22:** (n=300), (p=0,03).
- **Cálculo:** esperanza (np=9); desviación estándar (sqrt{np(1-p)}=sqrt{8,73}\approx2,954).
- **Resultado esperado:** 9 piezas defectuosas en promedio; desviación estándar aproximada **2,95 piezas**.
- **Estado:** cálculo verificado.

### LGS-4M-MAT-EVAL-009 — Regla empírica normal
- **Pregunta 23:** media 60 minutos, desviación estándar 8 minutos, intervalo aproximado del 99,7%.
- **Cálculo:** (mu\pm3\sigma=60\pm24).
- **Resultado esperado:** aproximadamente **36 a 84 minutos**.
- **Estado:** cálculo verificado.

### LGS-4M-MAT-EVAL-010 — Probabilidad total
- **Pregunta 25:** Norte: 60% de pedidos y 5% de retraso; Sur: 40% y 12%.
- **Cálculo:** (0,60(0,05)+0,40(0,12)=0,078).
- **Resultado esperado:** **7,8%**.
- **Estado:** cálculo verificado.

## Conclusión
Los diez cálculos seleccionados concuerdan con los modelos y datos visibles del enunciado. Esta verificación **no certifica** las 25 respuestas ni la suma total de puntajes: quedan pendientes el recálculo de todas las claves, la revisión de distractores y la comparación pregunta por pregunta con Forma A.
