# Calidad del material: análisis del 2026-11-23

Corpus analizado: base vigente (`logos_qa`, idéntica a la importada en el ensayo de producción): **7.278 preguntas
cerradas** (6.074 alternativas, 888 V/F, 316 «varias correctas»), 58 guías, 156 pruebas de unidad y 92 simulacros
(Formas A y B), 12 cursos. Scripts del análisis: `scripts/qa/calidad/` (ver §5).

## 1. Veredicto

El material es **correcto y completo**. Todas las claves están bien, el contenido coincide con los temarios y los
12 cursos están cubiertos. **Tiene un defecto de diseño de ítems que hay que corregir**: en cursos superiores, la
alternativa correcta se delata por su forma. Hay además problemas menores de redacción y de lectura en las guías.

| Dimensión | Estado | Evidencia |
|---|---|---|
| Exactitud de claves y contenido | Muy bien | 0 errores en 52 preguntas revisadas a mano (muestra al azar, 4 por curso + 4 sospechosas); validadores de claves, factual, anglicismos y estructura en 0 |
| Cobertura curricular | Muy bien | 0 OA sin preguntas de autoevaluación y 0 OA sin preguntas en pruebas o simulacros, en los 12 cursos |
| Posición de la clave | Bien | a/b/c/d equilibradas (b algo más frecuente: 27–29 %) |
| Pistas de forma (longitud, palabras absolutas) | **Débil** | Un alumno que no sabe la materia acierta 43–60 % desde 3.° básico (azar: 25 %) |
| Retroalimentación | Aceptable | Ninguna vacía; mediana 137 caracteres; 64 % empieza en minúscula; algunas no explican el porqué |
| Lenguaje adecuado a la edad (guías) | **Mejorable** | 2.°–3.° básico: 32–36 palabras por oración en promedio y párrafos de 230–270 palabras |
| Jerga interna visible | Menor | 58 preguntas mencionan «OA» al alumno; 5 líneas con notas de autoría en 4.° medio Lengua |

## 2. Hallazgo principal: la forma delata la respuesta

Simulación de un alumno que **no sabe la materia** y aplica dos trucos: descartar las alternativas con palabras
absolutas («nunca», «siempre», «solo», «todas», «exactamente»…) y marcar la más larga de las que quedan.

| Curso | Guías | Pruebas y simulacros |
|---|---|---|
| 1.° básico | 28 % | 28 % |
| 2.° básico | 36 % | 34 % |
| 3.° básico | 34 % | 44 % |
| 4.° básico | 43 % | 43 % |
| 5.° básico | 38 % | 44 % |
| 6.° básico | 51 % | 45 % |
| 7.° básico | 48 % | 49 % |
| 8.° básico | 53 % | 46 % |
| 1.° medio | 43 % | 44 % |
| 2.° medio | 49 % | 43 % |
| 3.° medio | 53 % | 53 % |
| 4.° medio | 60 % | 60 % |

(Azar: 25 % con 4 alternativas.)

- **Por qué importa:** con exigencia del 60 %, el truco solo deja la nota cerca de 4,0 en 4.° medio. Las notas de
  práctica quedan infladas y dan una confianza falsa antes del examen real, que no tiene estas pistas.
- **Causas:**
  - la correcta es estrictamente la más larga en el 40–50 % de los ítems de 7.° básico a 4.° medio;
  - los distractores llevan palabras absolutas 4 a 5 veces más que las claves (13–21 % contra 2–5 %);
  - muchos distractores son extremos fáciles de descartar («Las dos son idénticas: la de 1948 solo copió el texto»).
- **Por qué no lo detectó la guarda C.6:** solo marca los casos evidentes (clave al menos 30 % más larga que el
  promedio y 12 caracteres más), cerca del 1 % de los ítems. El sesgo real es sutil y sistemático.
- **Corrección propuesta:** reescribir los distractores, no las claves. Distractores plausibles, del mismo largo y
  sin absolutos, basados en errores reales de los alumnos. Empezar por pruebas y simulacros de 3.° y 4.° medio, y
  agregar una guarda por curso: el truco no debe superar el 35 %.

## 3. Hallazgos menores

1. **Retroalimentación en minúscula (4.687, 64 %).** En pantalla aparece como párrafo propio bajo «✓ ¡Correcto!» o
   «Respuesta correcta: …», así que se ve como error de tipeo («puedes descomponer 78…»). Se corrige de forma
   mecánica: mayúscula inicial al importar, salvo cuando empieza con la letra de la alternativa.
2. **Retroalimentación que no explica.** Ejemplos:
   - 1.° medio, Historia: «Reconocer a los actores… ayuda a comprender», sin decir por qué la combinación es correcta;
   - 4.° medio, Matemática: «el banco mantiene protegido el valor real de lo prestado»;
   - 8.° básico, Lengua: «el contraste debe ser real y sin errores de concordancia», que es una nota de autoría.
3. **«OA» dicho al alumno (58 preguntas).** Por ejemplo, «según lo estudiado en este OA» o «tal como pide este OA».
   El alumno no sabe qué es un OA. Cambiar por «en esta unidad» o eliminar.
4. **Notas de autoría en 4.° medio Lengua** (`lengua-y-literatura.md` y `pruebas/lengua-y-literatura-unidad-2.md`):
   - «Texto didáctico ficticio de Logos School: la cifra… se simulan…»;
   - «Para producción, se simula A escrito en 2005…»;
   - «Reconocer ese límite no contradice la clave».

   Son defensas de auditoría que confunden al alumno; además, la pregunta pide el dato «más verificable» y la clave
   es una atribución que el mismo texto declara ficticia.
5. **Vocabulario técnico en básica inicial.** «Observa el siguiente estímulo» aparece en 5 preguntas de 1.° a 4.°
   básico; mejor «Observa el mapa / la imagen».
6. **«Ninguna de las anteriores» (8 ítems).** Funciona solo porque la app no baraja alternativas. Si algún día se
   barajan, hay que fijar esa opción al final.
7. **Sin nivel de dificultad.** Las 7.278 preguntas tienen `nivel_dificultad` vacío; no impide nada hoy, pero limita
   la práctica adaptativa.
8. **Lectura de las guías (Explicación pedagógica).**

   | Curso | Palabras por oración | Oraciones de más de 35 palabras |
   |---|---|---|
   | 1.° básico | 24 | 19 % |
   | 2.° básico | 32 | 42 % |
   | 3.° básico | 36 | 46 % |
   | 4.° básico | 26 | 13 % |

   Para 7–9 años conviene apuntar a 12–15 palabras por oración y párrafos cortos. El contenido es correcto; la forma
   exige un lector adulto (en 1.°–2.° básico lo lee el apoderado o el audio, lo que atenúa el problema en esos dos
   cursos). Media también tiene oraciones largas (40–46), más tolerable a esa edad.

## 4. Lo que está bien (no tocar)

- Claves correctas en toda la muestra, con datos y cálculos verificados (por ejemplo, F neta y aceleración,
  modelo exponencial decreciente, regla 68-95-99,7, participios irregulares, *not only… but also*).
- Contextos chilenos auténticos y bien elegidos: La Tirana, oficinas salitreras, UF e IPC, Servel, pipiolos y
  pelucones.
- Explicaciones que anticipan el error típico («Si escribes 36, cambiaste el orden de las decenas y las unidades»).
- Cobertura total de OA, Formas A y B en todos los cursos, sin copias entre pruebas y guías (guarda C.2) y sin
  preguntas abiertas.

## 5. Cómo repetir el análisis

Desde `backend/`, con la base vigente en `DATABASE_URL`:

```bash
.venv/bin/python ../scripts/qa/calidad/analisis.py "$DATABASE_URL"   # cobertura, posición, duplicados, retro
.venv/bin/python ../scripts/qa/calidad/patrones.py "$DATABASE_URL"   # jerga, palabras absolutas, minúsculas
.venv/bin/python ../scripts/qa/calidad/truco.py "$DATABASE_URL"      # alumno que adivina por la forma
.venv/bin/python ../scripts/qa/calidad/muestra.py "$DATABASE_URL" 4 <semilla>   # muestra al azar para revisar a mano
```

Nota: `validar_calidad_contenido.py` debe correrse desde `backend/` (lee `backend/.env`); desde la raíz revisa la
base antigua `logos_dev` y reporta preguntas abiertas que ya no existen.

Corrección hecha en este análisis: `validar_evaluaciones_markdown.py` marcaba como discrepancia 4 claves idénticas a
su alternativa cuando esta termina en un paréntesis («El Servicio Electoral (Servel)»). Ahora: 0 en 307 archivos.
