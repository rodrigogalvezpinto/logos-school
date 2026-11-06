# Banco de preguntas abiertas (respaldo para reactivación futura)

**Decisión de producto (2026-11-06):** todas las preguntas de guías, pruebas de unidad y
simulacros pasan a ser de alternativas, porque la app no puede corregir respuestas abiertas
de forma confiable. Esto incluye:

- **Alternativas**: una sola respuesta correcta.
- **Verdadero o falso**.
- **Varias correctas**: el alumno marca todas las alternativas correctas. Se corrige
  todo o nada: el punto se obtiene solo si marca exactamente las correctas.

Hasta ahora, las preguntas de desarrollo (3.299, cerca del 50 % de pruebas y simulacros) no
contaban para la nota. Al convertirlas, la nota de cada evaluación considera todas sus
preguntas.

## Qué contiene este directorio

`preguntas-abiertas.json` guarda las 3.299 preguntas abiertas tal como estaban en el commit
`e6336af`, antes de convertirlas. Por cada una registra el archivo, el curso, el tipo de
recurso, el número o la posición, el OA, el enunciado, la pauta y la retroalimentación. Se
genera con:

```bash
python backend/scripts/exportar_banco_preguntas_abiertas.py e6336af
```

Además, cada versión original completa sigue disponible en el historial de git
(`git show e6336af:contenido/...`).

## Cómo se reactivarán

Cuando exista un corrector validado (un profesor o IA con una tasa de acuerdo medida contra
corrección humana), estas preguntas pueden volver como tipo `desarrollo_breve`, junto a su
versión de alternativas o en su reemplazo. El motor de evaluación ya conserva el recorrido de
desarrollo (pauta visible y revisión personal), así que reactivarlas no exige rehacer la
interfaz.

El importador no lee este archivo: no es contenido activo.
