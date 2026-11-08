# Fase 1 · Control 4 — Indicadores de evaluación: 2.° básico

**Fuente:** `Temarios/temario_basica_2deg_basico_UCE.pdf`, extraído con
`backend/scripts/auditoria_indicadores.py "2° básico"`. Base importada desde `contenido/` el 2026-11-07.

**Resultado: 100 de 104 indicadores cubiertos (96 %).**

| Asignatura | Indicadores | Cubiertos | Sin pregunta / débiles |
|---|---|---|---|
| Lenguaje y Comunicación | 16 | 16 | — (OA 1: de las combinaciones, solo ce-ci, gue-gui y güe-güi tienen pregunta propia; que-qui y ge-gi no) |
| Matemática | 31 | 31 | — |
| Ciencias Naturales | 30 | 26 | OA 7: **ubicación** de los órganos (solo hay preguntas de su función). OA 12: **efectos del viento**. OA 12: cambios del tiempo atmosférico a lo largo del año (solo indirecto, vía OA 14). OA 14: identificar las estaciones **en calendarios** |
| Historia, Geografía y Cs. Sociales | 27 | 27 | Débiles: OA 1, idioma y creencias de los pueblos originarios (cubierto por el OA 2). OA 7, ubicar Chile en planisferio o globo terráqueo (solo en un mapa de América) |

## Otros hallazgos

1. **Gráficos descritos con palabras.** El indicador «leen e interpretan gráficos de barra simple» (OA 22)
   se evalúa en la prueba y en el simulacro con texto o una tabla («"en bicicleta" llega hasta el 5»),
   sin mostrar el gráfico. Hace falta un gráfico de barras dibujado; puede ser un marcador
   `::barras::`, que se programa igual que los dibujos de 1.° básico.
2. **Mismos textos de lectura en la guía, la prueba y el simulacro (Lenguaje):** «La fiesta sorpresa de
   Emilia», la carta de Matías y el artículo sobre reciclaje.
3. **Simulacros con el mismo enunciado que la guía:** 6 de 40 (15 %).
4. **OA sin pregunta en simulacros** (control 3): Matemática OA 5, 7, 11, 16 y 20.

## Correcciones propuestas (al cerrar la Fase 1)

- Agregar preguntas para los 4 indicadores de Ciencias sin cubrir.
- Dibujar los gráficos de barras de las preguntas del OA 22.
- Usar textos nuevos en el simulacro e incluir los 5 OA de Matemática faltantes.
