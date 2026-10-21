# 📚 Centro de Documentación y Gobernanza — Logos School

Bienvenido al directorio central de documentación del proyecto **Logos School**. Este espacio consolida los informes de auditoría, las especificaciones técnicas, las líneas base de calidad (QA) y los planes de trabajo del sistema.

---

## 🗂️ Estructura del Directorio `docs/`

```text
docs/
├── README.md                          # Este índice general de documentación
│
├── auditorias/                        # Diagnósticos y auditorías técnicas
│   ├── matematica/                    # Auditoría de Matemática (12 cursos, 116 OAs, 857 preguntas)
│   │   ├── README.md                  # Handover e índice de auditoría matemática
│   │   ├── 01-inventario-auditoria.md # Conteo de líneas, palabras, OAs y tipos de preguntas
│   │   ├── 02-hallazgos-consolidados.md # Fichas técnicas de hallazgos P0 a P3
│   │   ├── 03-matriz-curricular.md    # Contraste de 116 OAs oficiales UCE vs guías
│   │   ├── 04-auditoria-matematica.csv # Dataset con las 857 preguntas reales inventariadas
│   │   ├── 08-resumen-ejecutivo.md    # Síntesis ejecutiva y mapa de decisiones
│   │   └── informe-preliminar-20-oct.md # Informe estático preliminar histórico
│   │
│   └── ux-ui/                         # Experiencia de usuario y accesibilidad
│       └── hallazgos-ux.md            # Diagnóstico de hallazgos UX-001 a UX-005
│
├── planes/                            # Especificaciones técnicas de implementación (Fase 2)
│   ├── 05-especificacion-correcciones.md # Código exacto para Angular, FastAPI y SQL
│   └── 07-prompt-agente-ejecucion.md     # Prompt autónomo para agente programador
│
└── qa/                                # Calidad, suites y líneas base de pruebas
    ├── linea-base.md                  # Certificación formal de 886 tests (Pytest/Vitest/E2E)
    ├── 06-plan-pruebas-regresion.md   # Casos de prueba requeridos para las correcciones
    ├── plan-avance-12-cursos.md       # Protocolo E2E de validación de los 12 cursos
    ├── inventario-suites.md           # Inventario completo de suites de prueba
    └── historico/                     # Reportes y defectos históricos (18-oct-2026)
        ├── reporte-ejecucion-18-oct.md
        ├── defectos-historicos.md
        ├── README.md
        └── RESUMEN.md
```

---

## 🧭 Guía Rápida para Desarrolladores y Agentes IA

1. **Estado del Proyecto:**  
   Consulte [`ESTADO-ACTUAL.md`](../ESTADO-ACTUAL.md) para conocer las métricas vigentes y el estado de la plataforma.
2. **Levantamiento Local y Credenciales:**  
   Ejecute `./iniciar.sh` en la raíz y revise [`ACCESO-Y-PRUEBAS.md`](../ACCESO-Y-PRUEBAS.md) para credenciales de prueba preconfiguradas.
3. **Línea Base de Pruebas:**  
   Revise [`qa/linea-base.md`](qa/linea-base.md) para verificar los comandos y resultados de la suite automatizada (886 pruebas).
4. **Fase de Implementación (Fase 2):**  
   Para implementar las correcciones aprobadas, consulte la especificación técnica en [`planes/05-especificacion-correcciones.md`](planes/05-especificacion-correcciones.md) y el prompt de ejecución en [`planes/07-prompt-agente-ejecucion.md`](planes/07-prompt-agente-ejecucion.md).

---

## 📌 Documentación Histórica y Canónica Adicional

- [`planificacion/`](../planificacion/): Fichas fundacionales de producto, arquitectura, modelo de negocio y capturas originales de Brincus. Se preservan intactas en su ubicación raíz original.
- [`Temarios/`](../Temarios/): Decretos y temarios oficiales de la Unidad de Currículum y Evaluación (UCE) de MINEDUC.
- [`contenido/`](../contenido/): Banco de guías pedagógicas en Markdown para los 12 niveles escolares.
