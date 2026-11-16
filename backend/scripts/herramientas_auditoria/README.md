# Herramientas de edición asistida del material (auditoría Fase 1)

Ayudantes que se usaron para reescribir preguntas y pautas sin romper el formato. Todos verifican con
el parser real (`parser_prueba_examen.py`) **antes de escribir**: si la clave, el tipo o el OA cambian
por error, abortan sin tocar el archivo. Se usan desde `backend/`:

```python
import sys; sys.path.insert(0, 'scripts/herramientas_auditoria')
from explicar import ver, explicar
from rehacer import rehacer
```

| Función | Para qué |
|---|---|
| `ver(archivo, [n, ...], ctx=False)` | Muestra enunciado, alternativas, clave y explicación de las preguntas indicadas (`archivo` relativo a `contenido/`). `ctx=True` incluye la lectura. |
| `explicar(archivo, {n: "texto"})` | Agrega una explicación a la línea de pauta de la pregunta n (tabla `| n | … |`, lista `n. …` o `**Pregunta n (…).**`). No cambia la clave. |
| `rehacer(archivo, n, enunciado, opciones, explicacion)` | Reemplaza enunciado, alternativas y pauta de la pregunta n. **La clave queda en la misma letra**: pon la alternativa correcta en la posición de la clave original. `opciones=None` para V/F. En «varias correctas» se conservan las mismas letras correctas (pon las alternativas correctas en esas posiciones). |
| `rehacer(archivo, n, None, None, explicacion, solo_explicacion=True)` | Reemplaza **solo** la entrada de la pauta (la explicación que ve el alumno), sin tocar enunciado ni alternativas. Usar para C.4c. Verifica que la pauta termine en la explicación nueva. No escribas «x) clave.» al inicio: `rehacer` la antepone. |
| `retro_guia.cambiar(archivo, inicio, nueva)` / `retro_guia.ver(curso)` | Reemplaza la retroalimentación de una pregunta de **guía** localizada por su texto actual; exige ubicación única y verifica que cambió la pregunta buscada (C.4b). |
| `match.match(archivo, n)` | Muestra la pregunta y la pregunta más parecida de la guía del curso (para decidir si es copia). |
| `vc.vc(archivo)` | Lista compacta de las preguntas cuya explicación solo repite la clave. |

Controles de lectura (no editan): `../solapamiento_pruebas_guias.py`, `../explicaciones_pobres.py`,
`../validar_evaluaciones_markdown.py`, `../estimulos_huerfanos.py`.

`../reemplazar_pregunta_simulacro.py` (vía JSON) es la herramienta antigua de reemplazo de bloques; sigue
funcionando, pero `rehacer` es más simple y verifica más.
