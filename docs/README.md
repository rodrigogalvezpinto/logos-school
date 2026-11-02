# Centro de Documentación y Gobernanza — Logos School

Este directorio consolida auditorías, especificaciones técnicas, calidad y planes de trabajo.

> **Rama de trabajo actual:** `main`, sincronizada con `origin/main`. La rama `qa/fase-2-matriz-trazabilidad` se integró por el PR #8 y se conserva como referencia histórica. Se pueden crear ramas desde `main` si un cambio necesita aislamiento.

## Estructura

```text
docs/
├── README.md
├── PLAN-CONSOLIDACION-DOCUMENTACION.md  # Plan de consolidación de documentación
├── auditorias/                        # Diagnósticos y auditorías técnicas
│   ├── 00-CENTRO-DE-CONTROL-AUDITORIA.md
│   ├── AUDITORIA_MAESTRA.md           # Auditoría consolidada del contenido
│   ├── ARCHIVOS-ELIMINADOS.md         # Registro de archivos eliminados
│   ├── matematica/                    # Auditoría de Matemática
│   └── ux-ui/                         # Experiencia de usuario y accesibilidad
├── planes/
│   ├── 05-especificacion-correcciones.md
│   ├── 07-prompt-agente-ejecucion.md
│   ├── pendientes-voz-videos-juegos.md
│   └── backlog-producto-tutor-ia-y-lectura.md
└── qa/                                # Calidad, suites y líneas base
    ├── linea-base.md
    ├── inventario-suites.md
    ├── plan-avance-12-cursos.md
    ├── 06-plan-pruebas-regresion.md
    └── historico/                     # Histórico de auditorías
```

## Guía rápida

1. **Estado del proyecto:** Consulte [README.md](../README.md) en la raíz para el estado actual.
2. **Auditoría de contenido:** Revise [auditorias/AUDITORIA_MAESTRA.md](auditorias/AUDITORIA_MAESTRA.md) para hallazgos consolidados.
3. **Auditoría de Matemática:** Vea [auditorias/matematica/README.md](auditorias/matematica/README.md) para el análisis específico.
4. **Resultados de pruebas:** Revise [qa/linea-base.md](qa/linea-base.md) para los resultados de pruebas documentados.
5. **Correcciones aprobadas:** Consulte [planes/05-especificacion-correcciones.md](planes/05-especificacion-correcciones.md) y [planes/07-prompt-agente-ejecucion.md](planes/07-prompt-agente-ejecucion.md).

## Documentación histórica y canónica

- [planificacion/](../planificacion/): especificaciones fundacionales, arquitectura y modelo de negocio.
- [Temarios/](../Temarios/): temarios oficiales de la UCE/MINEDUC.
- [contenido/](../contenido/): guías pedagógicas de los cursos.
- [CLAUDE.md](../CLAUDE.md): memoria del proyecto (contexto para agentes IA).

## Especialistas de Logos School

Invocar `/logos-coordinacion` para repartir un lote entre los cinco perfiles de [`.devin/agents/`](../.devin/agents/): curricular/disciplinar, QA de experiencia, datos/evaluación, desarrollo y seguridad/operación. El [protocolo compartido](../.devin/agent-protocol.md) define fuentes, evidencia, permisos y aprobaciones independientes. Se reconocen con `devin doctor --json`; los perfiles personalizados son experimentales y pueden requerir una sesión nueva para aparecer en las herramientas del agente.

El [piloto de Inglés de 5.º básico](auditorias/AUDITORIA_MAESTRA.md#14-piloto-de-especialistas--ingles-5-basico-2026-11-01) registra revisión, hallazgos, corrección y pruebas reales. No confundir perfiles instalados con auditorías ejecutadas ni dictamen de un lote con certificación oficial o de toda la aplicación.

## Pendientes tecnológicos

- [Voz, videos y juegos](planes/pendientes-voz-videos-juegos.md): opciones por validar.
- [Backlog de tutor IA y evaluación de lectura](planes/backlog-producto-tutor-ia-y-lectura.md): ideas priorizadas; no implementadas.
