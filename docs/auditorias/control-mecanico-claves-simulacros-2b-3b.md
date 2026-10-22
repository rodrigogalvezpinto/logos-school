# Control mecánico de letras de clave — simulacros integrados de 2.º y 3.º básico

**Fecha de ejecución:** 21 de octubre de 2026  
**Rama:** `qa/fase-2-matriz-trazabilidad`  
**Naturaleza:** comprobación documental auxiliar reproducida sobre la fuente Markdown. No es una auditoría pedagógica ni curricular completa.

## Archivos y resultado

| Archivo | Preguntas detectadas | Filas de clave explícitas con letra | Filas comparables con alternativas | Letras no presentes entre las alternativas detectadas |
|---|---:|---:|---:|---:|
| `contenido/02-basico/examenes/examen-integrado-forma-a.md` | 20 | 19 | 19 | 0 |
| `contenido/02-basico/examenes/examen-integrado-forma-b.md` | 20 | 14 | 14 | 0 |
| `contenido/03-basico/examenes/examen-integrado-forma-a.md` | 20 | 15 | 15 | 0 |
| `contenido/03-basico/examenes/examen-integrado-forma-b.md` | 20 | 12 | 12 | 0 |
| **Total** | **80** | **60** | **60** | **0** |

## Qué demuestra y qué no demuestra

La comprobación mecánica encontró que las 60 filas de pauta con una letra explícita que pudo asociarse a una pregunta y sus alternativas no usan una letra ausente de las opciones detectadas.

**No significa que las 60 claves sean semánticamente correctas.** El control compara la presencia de la letra, no si la alternativa es verdadera, si el valor numérico coincide con el resultado, si existe más de una respuesta defendible o si la explicación de la pauta es correcta. Tampoco revisa de forma completa preguntas de desarrollo, verdadero/falso, recursos visuales, OA ni renderizado.

El recuento de preguntas detectadas y filas de clave explícitas es diferente porque hay preguntas de desarrollo y otras que no usan una clave de la forma `a)`–`d)`. Los recuentos corresponden a lo que reconoció el control documental, no a una declaración de que todos los ítems quedaron validados.

## Riesgos que siguen abiertos

- Para 2.º básico, la auditoría previa ya documentó duplicación de preguntas y estímulos entre Formas A y B, además de riesgos de precisión científica e histórica y recursos gráficos que requieren verificación en la aplicación.
- Para 3.º básico, la auditoría previa ya documentó reutilización de textos e ilustraciones entre Formas A y B y preguntas que requieren revisión de convención curricular/contexto.
- En ambos cursos sigue pendiente comprobar que las imágenes descritas en el Markdown existan y se muestren correctamente en el entorno QA.
- No se ha cotejado aquí cada OA con una fuente oficial vigente ni revisado de forma independiente cada distractor y cada respuesta.

## Próximo paso

Incorporar controles que comparen también valores numéricos explícitos, totales y claves en formatos de tabla variados; después revisar manualmente las 80 preguntas, registrando por ítem el resultado y su evidencia. Mantener la revisión automatizada separada de la aprobación pedagógica.

**Estado:** control mecánico parcial completado; los cuatro simulacros continúan sin certificación integral.
