# Protocolo de especialistas de Logos School

Leer al recibir un encargo. No es otro tablero: el estado se registra en `docs/auditorias/00-CENTRO-DE-CONTROL-AUDITORIA.md` y el detalle en `docs/auditorias/AUDITORIA_MAESTRA.md`.

## Contrato de trabajo

El coordinador proporciona objetivo, curso/asignatura, archivos/preguntas/OA, commit y cambios locales, fuentes, entorno, permisos y criterio de cierre. Si falta un dato esencial, devolver incertidumbre; no inventarlo. Consultar solo las secciones pertinentes de las instrucciones vigentes. Trabajar localmente en main; preservar cambios existentes, secretos y datos. No desplegar, contratar servicios, modificar producción ni ejecutar operaciones destructivas. No lanzar agentes hijos.

Un solo responsable de escritura por archivo; separar usuarios/fixtures de pruebas que alteren datos. Las revisiones independientes son de solo lectura. No cambiar una clave sin resolver el ítem y cotejar alternativas. Ningún agente aprueba por sí solo su propia corrección crítica.

## Evidencia y dictamen

Entregar alcance exacto revisado, fuentes con páginas/secciones, versión, método, hallazgos con ruta/línea o pregunta, severidad e impacto, reproducción, esperado/observado, recomendación y regresión. Conservar IDs existentes; proponer uno nuevo solo si no existe el hallazgo. Separar defecto confirmado, riesgo y mejora opcional.

Por cada dimensión (educativa, datos/calificación, funcional/visual, seguridad cuando aplique), usar: no revisado, en revisión, cambios requeridos, corregido pendiente de revalidación, aprobado en alcance o bloqueado. Una prueba estructural, captura o título de OA no demuestra cobertura pedagógica ni un flujo E2E. No sumar revisiones parciales como aprobación global.

La aprobación interna exige evidencia de los criterios ejecutados y ausencia de bloqueos críticos/altos en ese alcance. Registrar excepciones y límites: no es certificación Mineduc ni reemplaza revisión docente humana antes de publicación a menores, conforme a `planificacion/04-modo-de-operacion.md`. Para cambios de claves, cálculos o rúbricas de alto impacto exigir segunda resolución independiente.

Formato de retorno compacto: alcance/versión; tabla de hallazgos; comprobaciones ejecutadas con resultados; dictamen por dimensión; bloqueos y siguiente acción. Citar archivos/rangos sin copiar documentos enteros. Nunca afirmar una ejecución que no ocurrió.
