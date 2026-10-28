# Índice y guía de handover — línea de auditoría de Matemática

> **Alcance y estado, actualizado 2026-10-22:** este directorio reúne un análisis especializado de Matemática y documentación técnica/UX relacionada. **No equivale a la auditoría integral completa de Logos School ni certifica por sí solo el contenido de los 12 cursos.** Para el estado global, la cobertura y las prioridades vigentes, consultar el [Centro de control único de auditoría](../00-CENTRO-DE-CONTROL-AUDITORIA.md).

> Las cifras de pruebas, preguntas, OA y cobertura indicadas en este documento son las del corte/commit señalado por cada artefacto. No se deben presentar como estado actual sin regenerar los conteos y comprobar las ejecuciones correspondientes. Las pruebas verdes documentadas aquí son evidencia histórica o de un alcance específico; no certifican exactitud pedagógica.

---

## Estado técnico documentado en el corte de este informe

- **Rama:** `docs/centralizacion-gobernanza` (base `main`)
- **Línea base de pruebas activas (100% en verde):**
  - **Pytest Backend:** 491 / 491 tests ✅ (`cd backend && .venv/bin/pytest -q`)
  - **Vitest Frontend:** 33 / 33 tests ✅ (`cd frontend && npm test -- --watch=false`)
  - **Playwright E2E:** 362 / 362 tests en 64 suites (evidencia histórica en commit `86a4c93`)
- **Script de Inicio Rápido:**  
  Ejecutar `./iniciar.sh` levanta automáticamente el Backend (puerto 8000) y Frontend (puerto 4200), mostrando en terminal las credenciales de prueba (`apoderado.prueba@logos.cl`, `profesor.prueba@logos.cl`, `admin.prueba@logos.cl`). Ver [`ACCESO-Y-PRUEBAS.md`](../../../ACCESO-Y-PRUEBAS.md).

---

## 📂 Mapa de Documentos de Auditoría en esta Carpeta

1. [`01-inventario-auditoria.md`](01-inventario-auditoria.md)  
   Inventario exhaustivo de los 12 cursos de Matemática: conteo de líneas (9.910), palabras (103.282), OAs (116) y distribución de preguntas (227 alternativas, 509 desarrollo, 121 V/F).
2. [`02-hallazgos-consolidados.md`](02-hallazgos-consolidados.md)  
   Fichas técnicas de los 11 hallazgos clasificados por severidad (P0 a P3), con evidencia, impacto y ubicación de código exacta.
3. [`03-matriz-curricular.md`](03-matriz-curricular.md)  
   Contraste de los 116 OAs oficiales de los temarios UCE MINEDUC (decretos 439/2012, 614/2013 y 193/2019) vs las guías de estudio de Logos School (100% de coincidencia estructural).
4. [`04-auditoria-matematica.csv`](04-auditoria-matematica.csv)  
   Dataset tabular con las **857 preguntas reales de Matemática**, su enunciado, clave, tipo y resultado del análisis sintáctico.
5. [`05-especificacion-correcciones.md`](../../planes/05-especificacion-correcciones.md)  
   Especificación técnica exacta de los cambios requeridos: código TypeScript para el runner de evaluaciones, schemas de API, SQL puntual de limpieza y ajustes editoriales.
6. [`06-plan-pruebas-regresion.md`](../../qa/06-plan-pruebas-regresion.md)  
   Casos de prueba unitarios y E2E requeridos para verificar las nuevas funcionalidades sin romper ninguna de las 886 pruebas base.
7. [`07-prompt-agente-ejecucion.md`](../../planes/07-prompt-agente-ejecucion.md)  
   **EL DOCUMENTO CLAVE PARA LA SIGUIENTE IA:** Prompt autónomo, preciso y secuencial que debe entregarse al agente de programación para implementar las soluciones aprobadas paso a paso.
8. [`08-resumen-ejecutivo.md`](08-resumen-ejecutivo.md)  
   Síntesis ejecutiva de riesgos, prioridades y mapa de decisiones.

---

## 🎯 Instrucciones para Continuar en Otra Sesión o Máquina

Cuando abras este proyecto en otra máquina o con otra IA:
1. Asegúrate de tener los servicios activos o corre `./iniciar.sh`.
2. Lee este archivo [`docs/auditorias/matematica/README.md`](README.md) y [`08-resumen-ejecutivo.md`](08-resumen-ejecutivo.md).
3. Para iniciar la implementación de código aprobada en Fase 2, utiliza directamente el prompt contenido en:  
   👉 **[`07-prompt-agente-ejecucion.md`](../../planes/07-prompt-agente-ejecucion.md)**


## Informes de revisión

- **Segunda revisión de auditoría de Matemática (20 oct 2026)** (informe retirado): inventario corregido, hallazgos H-01 a H-06, muestras aritméticas y límites de cobertura. Su contenido quedó en [02-hallazgos-consolidados.md](02-hallazgos-consolidados.md) y en [AUDITORIA_MAESTRA.md](../AUDITORIA_MAESTRA.md); ver también [ARCHIVOS-ELIMINADOS.md](../ARCHIVOS-ELIMINADOS.md).
