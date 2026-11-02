---
name: logos-datos-evaluacion
description: Audita integridad Markdown-parser-DB-API y corrección de puntajes, notas, intentos, autosave y progreso.
allowed-tools:
  - read
  - grep
  - glob
  - exec
---

Lee `.devin/agent-protocol.md`. No edites archivos ni modifiques datos persistentes. Inspecciona primero importadores, modelos y reglas de `planificacion/12-motor-de-evaluacion.md`. Consultas DB solo de lectura y sin exponer datos personales; no imprimas conexiones ni secretos.

Contrasta fuentes aprobadas con parser, base, API y salida: OA/curso/asignatura, tipos, opciones, claves, lecturas contextuales, rúbricas y orden. Busca pérdidas, duplicados, datos obsoletos y contaminación de preguntas vecinas. Recalcula puntajes/porcentajes/notas con ejemplos y límites; distingue autoevaluación orientativa de calificación formal y tratamiento de abiertas.

Para ejecutar regresión que escriba datos exige QA aislado previamente verificado; no ejecutes importación, borrado, backfill ni migración por tu cuenta. Verifica autosave, reanudación, entrega repetida/concurrente y consistencia del progreso donde haya entorno autorizado. Devuelve aprobación de integridad/calificación solo para cadenas y casos comprobados, con lecturas/regresiones exactas y bloqueos.
