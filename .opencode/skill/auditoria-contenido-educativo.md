# Skill: Auditoría de Contenido Educativo — Logos School

## Descripción
Skill especializado para auditar, validar y mejorar el contenido pedagógico de los 12 cursos (1° básico a 4° medio) de Logos School. Cubre los 408 Objetivos de Aprendizaje oficiales, 2.917 preguntas de autoevaluación, 156 pruebas de unidad y exámenes simulacro Forma A/B.

---

## Fuente de Verdad Curricular

### Temarios oficiales (PDFs)
- `Temarios/temario_basica_1deg_basico_UCE.pdf` → 1° básico
- `Temarios/temario_basica_2deg_basico_UCE.pdf` → 2° básico
- ... (hasta 8° básico)
- `Temarios/temario_media_1deg_medio_uce.pdf` → 1° medio
- ... (hasta 4° medio)

### Análisis estructurado (Markdown, 1 archivo por curso)
- `Temarios/analisis/01-primero-basico.md` → `Temarios/analisis/12-cuarto-medio.md`
- `Temarios/analisis/00-resumen-general.md` — Vista comparativa de los 12 niveles

### Contenido producido (validado 2026-08-10)
- `contenido/00-estado-contenido.md` — Estado curso por curso, asignatura por asignatura
- 2.917 preguntas totales (408/408 OA cubiertos)
- 156 pruebas de unidad (calibradas por edad: 6-15 preguntas según ciclo)
- Exámenes simulacro Forma A/B (formato exacto Mineduc por régimen)

---

## Los 3 Regímenes de Examen (Clave para Auditoría)

| Régimen | Cursos | Formato | Asignaturas | Decreto |
|---------|--------|---------|-------------|---------|
| **A** | 1°-4° básico | Integrada 20 preguntas | Lenguaje, Matemática, Ciencias Naturales, Historia/Geo/Cs. Sociales | 439/2012 |
| **B** | 5° básico-2° medio | Por asignatura 25 c/u | + Inglés | 439/2012 (5°-6°) / 614/2013 (7° en adelante) |
| **C** | 3°-4° medio | Por asignatura 25 c/u | Ciencias para la Ciudadanía, Filosofía, Educación Ciudadana (+ base) | 193/2019 |

**Implicación de auditoría**: El contenido de Régimen C **no es reutilizable** de niveles anteriores. Cada OA de 3°-4° medio debe auditarse contra su decreto propio.

---

## Checklist de Auditoría por Componente

### 1. Guías de Estudio (explicación + ejemplos por OA)
- [ ] Cada OA tiene explicación clara, nivel-adecuada
- [ ] Ejemplos resueltos paso a paso (no solo resultado)
- [ ] Vocabulario y contexto chileno (pesos, comunas, nombres, geografía)
- [ ] Conexión con vida cotidiana del estudiante
- [ ] Longitud adecuada: no abruma, no es escueta

### 2. Banco de Preguntas Autoevaluación (2.917 total)
- [ ] **Cobertura**: 100% de OAs tienen preguntas (ver `contenido/00-estado-contenido.md`)
- [ ] **Calidad**: Enunciado claro, una sola respuesta correcta, distractores plausibles
- [ ] **Nivel cognitivo**: Mix de recordar, comprender, aplicar, analizar (Bloom)
- [ ] **Calibración por edad**: 
  - 1°-4° básico: lenguaje simple, enunciados cortos, apoyo visual implícito
  - 5°-8° básico: mayor abstracción, problemas de varios pasos
  - 1°-4° medio: rigor académico, conectar conceptos
- [ ] **Metadatos**: Cada pregunta tiene `oa_codigo`, `asignatura`, `nivel`, `dificultad`, `tipo`

### 3. Pruebas de Unidad (156 totales, formativas)
- [ ] Tamaño calibrado por ciclo (ver `planificacion/08-diseno-pruebas-vs-examenes.md`):
  - Ciclo 1 (1°-4° básico): 6-8 preguntas
  - Ciclo 2 (5°-8° básico): 10-12 preguntas
  - Ciclo 3 (1°-4° medio): 12-15 preguntas
- [ ] Foco en **un OA o grupo pequeño de OAs relacionados**
- [ ] Retroalimentación formativa por pregunta (explicar por qué cada opción)
- [ ] No son simulacro: son para aprender, no para certificar

### 4. Exámenes Simulacro Forma A/B (sumativos, formato real)
- [ ] **Régimen A**: 1 prueba integrada 20 preguntas (4 asignaturas), 2 formas
- [ ] **Régimen B**: 1 prueba por asignatura 25 preguntas, 2 formas c/u
- [ ] **Régimen C**: 1 prueba por asignatura 25 preguntas, 2 formas c/u (asignaturas únicas)
- [ ] Distribución de preguntas por asignatura/OA fiel al decreto
- [ ] Nota en escala 1.0-7.0 con exigencia 60% (ver `planificacion/12-motor-de-evaluacion.md`)
- [ ] Cronómetro, navegación pregunta a pregunta, autosave

---

## Scripts de Validación Automatizada

### `scripts/validar_calidad_contenido.py`
- Corrió sobre los **407 OA reales** (2026-08-14)
- Verifica: cobertura, metadatos, formato, consistencia
- **Ejecutar antes de cualquier cambio masivo de contenido**

### `scripts/qa_completo.sh`
- Suite completa de QA (backend + frontend + contenido)
- Incluye validación de integridad referencial OA ↔ preguntas ↔ pruebas ↔ simulacros

---

## Patrones de Errores Comunes (Detectados en Auditoría 2026-08-14)

| Error | Dónde | Corrección |
|-------|-------|------------|
| Preguntas con 2 respuestas correctas | Banco autoevaluación | Revisar distractores, asegurar clave única |
| Enunciado ambiguo o confuso | Banco autoevaluación | Reescribir con lenguaje preciso, probar con compañero |
| OA sin preguntas asignadas | Cobertura | Verificar `contenido/00-estado-contenido.md`, completar faltantes |
| Pregunta de nivel superior al curso | Calibración | Ajustar dificultad o mover a curso superior |
| Simulacro con distribución incorrecta | Formato examen | Cruzar con decreto correspondiente (439/2012, 614/2013, 193/2019) |
| Contenido Régimen C copiado de Régimen B | 3°-4° medio | Reescribir desde cero para Ciencias para la Ciudadanía, Filosofía, Educación Ciudadana |

---

## Flujo de Trabajo de Auditoría

### Auditoría rápida (un curso/asignatura)
1. Leer `Temarios/analisis/XX-curso.md` → ver OAs e indicadores
2. Abrir `contenido/00-estado-contenido.md` → ver estado de ese curso/asignatura
3. Revisar guías y preguntas contra indicadores de evaluación del OA
4. Ejecutar `python scripts/validar_calidad_contenido.py --curso X --asignatura Y`
5. Documentar hallazgos en `planificacion/XX-auditoria-[curso]-[asignatura].md`

### Auditoría completa (todos los cursos)
1. Ejecutar `scripts/qa_completo.sh`
2. Revisar output de `validar_calidad_contenido.py`
3. Comparar cobertura real vs. 408 OA oficiales
4. Verificar 3 regímenes de simulacro por separado
5. Consolidar en `planificacion/XX-auditoria-general-[fecha].md`

---

## Cómo Reportar Hallazgos

### Formato estándar
```markdown
## Hallazgo: [Título breve]
- **Curso/Asignatura/OA**: [ej. 6° básico / Matemática / OA 12]
- **Componente**: Guía / Preguntas / Prueba unidad / Simulacro
- **Severidad**: Crítica / Mayor / Menor / Cosmética
- **Descripción**: [Qué está mal y por qué]
- **Evidencia**: [Cita textual, captura, o referencia a línea de archivo]
- **Propuesta de corrección**: [Concreta, accionable]
- **Impacto**: [Si afecta simulacro, progreso alumno, cumplimiento curricular]
```

### Severidades
- **Crítica**: Incumple decreto, pregunta con 2 respuestas correctas, OA sin cobertura
- **Mayor**: Error conceptual, nivel inadecuado, distribución simulacro incorrecta
- **Menor**: Redacción mejorable, ejemplo poco claro, falta retroalimentación
- **Cosmética**: Typos, formato, consistencia visual

---

## Referencias Cruzadas (Leer según necesidad)

| Documento | Para qué sirve |
|-----------|----------------|
| `planificacion/05-tipos-de-contenido.md` | Define guía, pruebas, simulacro — reglas de cada tipo |
| `planificacion/08-diseno-pruebas-vs-examenes.md` | Diferencia formativo vs. sumativo, calibración por edad |
| `planificacion/12-motor-de-evaluacion.md` | Cálculo nota 1.0-7.0, exigencia 60%, desglose por OA |
| `planificacion/21-accesibilidad-lectura-y-contenido-visual.md` | Lectura en voz alta (1°-2°), componentes visuales propios (Mate) |
| `planificacion/25-analisis-competencia-brincus.md` | Benchmark de calidad contra competidor real |
| `planificacion/27-plan-incorporacion-hallazgos-brincus.md` | Qué se incorporó de Brincus en Fase 1 (ya hecho) |

---

## Notas de Proceso

- **El contenido está "completo" pero no "perfecto"** — la auditoría continua es parte del ciclo
- **No reescribir masivamente sin validación automatizada** — usar scripts primero
- **Régimen C (3°-4° medio) requiere atención especial** — contenido único, no reutilizable
- **Accesibilidad**: 1°-2° básico debe tener lectura en voz alta nativa (Web Speech API)
- **Matemática**: Usar componentes visuales propios (recta numérica, fracciones, geometría) no imágenes sueltas

---

## Actualización
- Basado en auditoría completa 2026-08-14 (3 bugs de contenido encontrados y corregidos)
- Próxima auditoría programada: antes de Fase 2 Brincus o deployment a producción
- Este skill complementa a `logos-school.md` — úsalos juntos