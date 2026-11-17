# Análisis de cobertura del temario oficial (iniciado 2026-11-17)

Pedido del dueño: identificar **dónde el material no cumple** con lo que el Mineduc exige estudiar para el examen libre,
en cada curso y asignatura. **Solo análisis; las correcciones esperan su decisión.**

Método:
1. `scripts/analisis/cobertura_temario.py` cruza los 410 OA y 1.528 indicadores de `Temarios/analisis/` con la base
   (explicación de la guía y preguntas por OA). Resultado: los 410 OA existen en el material.
2. `scripts/analisis/volcar_curso.py "<curso>" <json>` vuelca, por curso, cada OA con sus indicadores y el texto de la guía.
3. Lectura humana indicador por indicador; el resultado de cada curso queda en `NN-curso.md` de esta carpeta.

Clasificación de brechas: **Falta** (el indicador no se enseña), **Falta parcial**, **Débil** (se menciona sin ejemplo o
sin la profundidad que pide el indicador), **Visual** (mapa o imagen pendiente), **Poca práctica** (pocas preguntas
fuera de la guía).

Estado: 1.° a 4.° básico revisados. Siguen 5.° básico a 4.° medio. Al final: resumen consolidado en este archivo.
