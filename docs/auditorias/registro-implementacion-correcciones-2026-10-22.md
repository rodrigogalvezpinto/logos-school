# Bitácora de implementación de correcciones — Logos School

**Fecha de inicio:** 22 de octubre de 2026  
**Rama:** `qa/fase-2-matriz-trazabilidad`  
**Base:** auditoría consolidada aportada el 22-10-2026 y hallazgos ya registrados en el repositorio.  
**Estado:** correcciones aplicadas en rama QA; pendientes de regresión y revisión final. No certifica cierre integral.

## Reglas de ejecución

- Las correcciones se aplican en la rama QA, no en `main`.
- Se conserva la identidad de cada pregunta; no se borran registros ni se ejecutan cambios de base de datos.
- Cada cambio debe tener un hallazgo rastreable, una validación específica y evidencia de regresión.
- Un cambio de contenido queda como **corregido pendiente de revalidación** hasta revisar el archivo final y ejecutar las pruebas aplicables.
- Los hallazgos que dependen de interpretación curricular, render o criterio de evaluación se mantienen abiertos hasta disponer de evidencia suficiente.

## Lote 1 — errores P1 y correcciones inequívocas

| ID / hallazgo | Archivo | Cambio realizado | Estado |
|---|---|---|---|
| LGS-4B-EVAL-001 | `contenido/04-basico/examenes/examen-integrado-forma-b.md`, pauta, pregunta 16 | Se cambió la letra de la clave de `c) 14` a `b) 14`; el cálculo y el enunciado se mantienen | Corregido pendiente de revalidación |
| LGS-5B-EVAL-001 | `contenido/05-basico/examenes/historia-geografia-y-cs-sociales-examen-forma-b.md`, encabezado | Se cambió el total declarado de 30 a 35 puntos, coherente con los puntajes por pregunta, la pauta y la distribución documentada | Corregido pendiente de revalidación |
| LGS-2M-MAT-014 | `contenido/02-medio/examenes/matematica-examen-forma-b.md`, pauta, pregunta 14 | La inversa de (f(x)=x+10) se cambió a (f^{-1}(x)=x-10), con explicación algebraica correcta | Corregido pendiente de revalidación |

## Lote 2 — precisión de contenido y erratas verificadas

| ID / hallazgo | Archivo | Cambio realizado | Estado |
|---|---|---|---|
| LGS-6B-MAT-001 | `contenido/06-basico/matematica.md` | La retroalimentación ahora explica (2050=3\times683+1): 683 cajas por distribuidor y sobra una caja | Corregido pendiente de revalidación |
| MAT-CONT-002 | `contenido/06-basico/matematica.md` | Se retiró la nota editorial «cuidado con el orden» y se dejó la explicación de amplificación de razón 5:3 a 15:9 | Corregido pendiente de revalidación |
| LGS-7B-MAT-001 | `contenido/07-basico/matematica.md` | Se corrigió la tabla de frecuencia para los 20 datos: 0→4 (20%), 1→9 (45%), 2→5 (25%), 3→2 (10%) | Corregido pendiente de revalidación |
| LGS-2M-LEN-002 | `contenido/02-medio/examenes/lengua-y-literatura-examen-forma-b.md` | Se restauró la cita «ya no hay vuelta atrás» en la pregunta 17 | Corregido pendiente de revalidación |
| LGS-5B-ING-001 | `contenido/05-basico/examenes/ingles-examen-forma-b.md` | Se reordenó el diálogo para que la persona que rompió el lápiz se disculpe y la otra responda «That's OK, don't worry» | Corregido pendiente de revalidación |
| LGS-1M-CNT-011 | `contenido/01-medio/ciencias-naturales.md` | Se distinguió el efecto Doppler sonoro (más agudo al acercarse, más grave al alejarse) del corrimiento de la luz (azul al acercarse, rojo al alejarse) | Corregido pendiente de revalidación |
| LGS-8B-HIS-001 | `contenido/08-basico/historia-geografia-y-cs-sociales.md` | Se corrigió «population» por «población» | Corregido pendiente de revalidación |
| LGS-1M-LEN-001 | `contenido/01-medio/lengua-y-literatura.md` | Se corrigió «information implícita» por «información implícita» | Corregido pendiente de revalidación |
| LGS-8B-LEM-001 | `contenido/08-basico/lengua-y-literatura.md` | Se cambió «madrugada» por «tarde» y se actualizó la retroalimentación sobre el terremoto de Valdivia del 22-05-1960 | Corregido pendiente de revalidación |

## Evidencia de commits

| Commit | Archivo / cambio |
|---|---|
| `41e042e3790bae52a9eb0bcc72b1dd35c0551c34` | Clave 4B Forma B |
| `b6c10e262f453a7b2f1be99fa88a7844c57ff16a` | Puntaje Historia 5B |
| `f13c2efe426abfaf142324694a7e1ebad420d520` | Inversa Matemática 2M |
| `739892d18df593fdf1bbf0232a0066cb34951923` | Retroalimentación y limpieza editorial Matemática 6B |
| `5034c79130eecbb950ecc070bf2e352db2255e8a` | Tabla de frecuencias Matemática 7B |
| `9dea1fc2992c94b98612ad1e3ade9a3ae6f039e7` | Cita de Lengua 2M |
| `e2f31eb49221cf718da346564d73fe5801c1a022` | Diálogo Inglés 5B |
| `50ac8feeec312f5533086d9e622a92e4255dd7b9` | Efecto Doppler Ciencias 1M |
| `4c64599d8227167741aa8cc1f67309715e288518` | Errata Historia 8B |
| `b1c48933cedecc8c1044a01ffc1b48eeb2e3af7f` | Errata Lengua 1M |
| `4bdf9c38fe97d9ff2abdd36fe40157b94fea101d` | Contexto histórico Lengua 8B |

## Validación pendiente obligatoria

1. Ejecutar el validador estructural y pruebas unitarias de CI.
2. Añadir o confirmar pruebas de regresión específicas para: letra/valor de 4B P16, total 5B Historia, función inversa 2M P14, frecuencias de 7B, y diálogo 5B Inglés.
3. Releer los fragmentos editados desde la rama remota y confirmar que los cambios quedaron en la versión vigente.
4. Comprobar importación/render y calificación de los tres instrumentos P1 en el entorno QA.
5. Actualizar la matriz maestra y los hallazgos originales al registrar la evidencia de regresión.
6. No marcar P1 como cerrado ni declarar la auditoría completa hasta que los controles pasen.

## Fuera de este lote

- No se han ejecutado cambios en la base de datos `logos_qa`.
- No se han modificado archivos en `main`.
- No se ha corregido la escala de conversión de notas de 5B Historia: la regla del 60 % requiere confirmación de la política de evaluación antes de cambiarla.
- Los desbalances de letras correctas se registran como riesgo de diseño y requieren reequilibrar opciones sin alterar la validez de los distractores; no se resolvieron mediante cambios mecánicos.
