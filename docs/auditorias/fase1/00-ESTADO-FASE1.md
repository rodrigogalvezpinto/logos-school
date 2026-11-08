# Fase 1 — Auditoría del material contra los temarios oficiales

**Propósito.** Confirmar, sobre los archivos de `contenido/` y antes de cualquier mejora, que el
material es fiel a los 12 temarios oficiales UCE/Mineduc (`Temarios/*.pdf`, fuente de verdad).
La Fase 1 la propuso el usuario el 2026-11-07: primero auditar el material en archivos; después
aplicarlo a la app una sola vez; y al final las mejoras. Las reescrituras y mejoras quedan en pausa
mientras dure esta fase.

## Controles y estado

| # | Control | Herramienta | Estado |
|---|---|---|---|
| 1 | Cada OA del temario tiene material: guía, preguntas y pruebas | `backend/scripts/auditoria_cobertura_temarios.py` → `cobertura-temarios.md` | ✅ **408/408 OA en los 12 cursos**, sin OA ausentes ni sobrantes |
| 2 | Formato del examen: n.° de preguntas y duración según el temario | misma herramienta + base importada | ✅ 50/50 simulacros. 1.°–4.° básico: 20 preguntas integradas (formas A y B). 5.° básico a 4.° medio: 25 por asignatura (solo Forma B). Todos de 90 minutos |
| 3 | Cada OA aparece en algún simulacro | `cobertura-temarios.md` | ⚠️ **15 OA de régimen A sin pregunta en simulacros.** 1.° básico: Historia OA 6; Matemática OA 13 y 18. 2.° básico: Matemática OA 5, 7, 11, 16 y 20. 3.° básico: Matemática OA 11, 21 y 25. 4.° básico: Matemática OA 9, 18, 23 y 27. Desde 5.° básico: 0 |
| 4 | Cada **indicador de evaluación** del temario se evalúa con al menos una pregunta | lectura curso por curso (temario ↔ preguntas) | en curso (`indicadores-NN-curso.md`): **1.° básico 69/75 (92 %)**, **2.° básico 100/104 (96 %)**, **3.° básico 96/98 (98 %)**, **4.° básico 106/107 (99 %)**. Régimen A completo: **371/384 (97 %)**. **5.° básico ~122/125 (98 %)**. Faltan 7 cursos (6.° básico a 4.° medio). Herramienta: `backend/scripts/auditoria_indicadores.py` |
| 4b | Independencia de la evaluación: pruebas y simulacros no deben repetir la guía | `backend/scripts/solapamiento_pruebas_guias.py` | ⚠️ **Simulacros con el mismo enunciado que la guía:** 1.° básico 35 %, 7.° básico 16 %, 2.° básico 15 %, 3.° medio 15 %, 3.° básico 10 % y el resto entre 0 y 7 %. **Pruebas:** 0 % en 4.° básico, 13 % en 1.° básico y entre 59 y 97 % en los demás cursos |
| 5 | Exactitud de lo cambiado después de la revisión ítem por ítem (§15.26–15.28): reescrituras, rebalanceos y dibujos | lectura de los cambios desde `7ea9828` | pendiente |
| 6 | Versión congelada: tag Git «material aprobado» con informe por curso | — | pendiente |

### Sobre el control 3

El examen real es una *selección* de OA, así que una sola forma de 20 preguntas no puede cubrir los
27–33 OA de un curso de régimen A. Pero las formas A y B juntas suman 40 preguntas y sí podrían
cubrirlos todos. Para preparar bien al alumno, ningún OA del temario debería quedar fuera de los dos
simulacros. **Propuesta**, que se aplica después de cerrar los controles 4 y 5: en cada curso,
reemplazar en la Forma A o B preguntas de OA que ya tienen 3 o más preguntas por preguntas de los OA
faltantes, manteniendo las 20 preguntas y el equilibrio entre asignaturas.

## Cómo se reproduce

```bash
scripts/qa/reimportar_e2e.sh          # base aislada desde contenido/
cd backend && DATABASE_URL=… .venv/bin/python scripts/auditoria_cobertura_temarios.py ../docs/auditorias/fase1/cobertura-temarios.md
```

La lectura del PDF necesitó cuatro ajustes, que la herramienta ya incluye:
- «Idioma Extranjero: Inglés», con dos puntos;
- títulos con sangría o seguidos de «____»;
- «Ciencia para la Ciudadanía», en singular;
- «Objetivo de        Aprendizaje N°      7», con espacios extra.

Sin esos ajustes, los OA de una asignatura se atribuían a la anterior y aparecían como faltantes, lo
que era falso.
