# Fase 1 · Control 4 — Indicadores de evaluación: 4.° básico

**Fuente:** `Temarios/temario_basica_4deg_basico_uce.pdf` (`auditoria_indicadores.py "4° básico"`).

**Resultado: 106 de 107 indicadores cubiertos (99 %).**

| Asignatura | Indicadores | Cubiertos | Sin pregunta / débiles |
|---|---|---|---|
| Lenguaje y Comunicación | 27 | 27 | — |
| Matemática | 41 | 40 | OA 1: **expresan números en palabras y cifras** (hay valor posicional, billetes, comparación y descomposición, pero no la conversión palabra ↔ cifra hasta 10.000) |
| Ciencias Naturales | 24 | 24 | — (el PDF repite los indicadores del OA 1; se contaron una vez) |
| Historia, Geografía y Cs. Sociales | 15 | 15 | — |

## Regresión detectada y corregida durante la auditoría

Al reescribir la prueba de Números (§15.30–15.33), la pregunta 4 (reconocer la multiplicación, **OA 5**)
se había cambiado por una división (OA 6), y **el OA 5 quedó sin preguntas en la prueba**. Se restituyó:
ahora es «8 cajas con 150 lápices cada una» (multiplicación, OA 5). Se descartó un primer intento,
«124 marraquetas», porque coincidía con una pregunta del simulacro B. Verificación:
- validador: 0 discrepancias;
- reimportación: 0 preguntas sin OA;
- app: 4.° básico 18/18 en Chromium.

## Otros hallazgos

1. **Pruebas y simulacros independientes de la guía:** 0 % de preguntas copiadas, el único curso así.
2. **OA sin pregunta en simulacros** (control 3): Matemática OA 9, 18, 23 y 27.
