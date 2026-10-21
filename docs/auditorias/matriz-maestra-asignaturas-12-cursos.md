# Matriz maestra de auditoría de asignaturas — 12 cursos

**Fecha de corte:** 21 de octubre de 2026  
**Repositorio:** `rodrigogalvezpinto/logos-school`  
**Rama:** `qa/fase-2-matriz-trazabilidad`  
**Estado:** inventario documental consolidado; no equivale a certificación curricular, matemática o pedagógica.  
**Restricción de seguridad:** no modificar `main`, contenido fuente, aplicación ni base de datos durante esta fase de inventario.

## Propósito

Dar a cualquier agente futuro un punto de entrada único para continuar la auditoría de los 12 cursos, conservar la trazabilidad y evitar declarar materias auditadas solo porque exista un archivo o una prueba.

## 1. Inventario de asignaturas principales detectadas

Fuente primaria: `contenido/00-estado-contenido.md` y `docs/auditorias/inventario-reproducible-contenido-educativo.md`. Las asignaturas de esta tabla son las que aparecen como archivos principales directamente dentro de cada carpeta de curso.

| Curso | Asignaturas/guías principales detectadas | Cantidad |
|---|---|---:|
| 1.º básico | Lenguaje y Comunicación; Matemática; Ciencias Naturales; Historia, Geografía y Ciencias Sociales | 4 |
| 2.º básico | Lenguaje y Comunicación; Matemática; Ciencias Naturales; Historia, Geografía y Ciencias Sociales | 4 |
| 3.º básico | Lenguaje y Comunicación; Matemática; Ciencias Naturales; Historia, Geografía y Ciencias Sociales | 4 |
| 4.º básico | Lenguaje y Comunicación; Matemática; Ciencias Naturales; Historia, Geografía y Ciencias Sociales | 4 |
| 5.º básico | Lenguaje y Comunicación; Matemática; Ciencias Naturales; Historia, Geografía y Ciencias Sociales; Inglés | 5 |
| 6.º básico | Lenguaje y Comunicación; Matemática; Ciencias Naturales; Historia, Geografía y Ciencias Sociales; Inglés | 5 |
| 7.º básico | Lengua y Literatura; Matemática; Ciencias Naturales; Historia, Geografía y Ciencias Sociales; Inglés | 5 |
| 8.º básico | Lengua y Literatura; Matemática; Ciencias Naturales; Historia, Geografía y Ciencias Sociales; Inglés | 5 |
| 1.º medio | Lengua y Literatura; Matemática; Ciencias Naturales; Historia, Geografía y Ciencias Sociales; Inglés | 5 |
| 2.º medio | Lengua y Literatura; Matemática; Ciencias Naturales; Historia, Geografía y Ciencias Sociales; Inglés | 5 |
| 3.º medio | Lengua y Literatura; Matemática; Ciencias para la Ciudadanía; Filosofía; Inglés; Educación Ciudadana | 6 |
| 4.º medio | Lengua y Literatura; Matemática; Ciencias para la Ciudadanía; Filosofía; Inglés; Educación Ciudadana | 6 |
| **Total** | **52 archivos principales de asignatura (según inventario previo)** | **52** |

**Importante:** esta lista refleja el alcance documental existente, no todo el universo de asignaturas que podrían corresponder a cada nivel según las bases, planes de estudio, modalidad y oferta prometida por Logos School. En particular, Artes, Música, Educación Física y Salud, Tecnología, Orientación, Religión, lenguas/culturas de pueblos originarios y otras asignaturas o diferenciaciones de enseñanza media deben clasificarse como: cubiertas, fuera del alcance declarado, pendientes de decisión de producto o no aplicables, después de contrastar el plan oficial correspondiente. No inferir automáticamente que la ausencia de un archivo sea un defecto sin establecer antes el alcance del producto y la modalidad educativa.

## 2. Inventario inicial del repositorio

El documento `docs/auditorias/inventario-reproducible-contenido-educativo.md` registra un conteo estático de 891 archivos versionados, 12 carpetas de curso y 13 archivos Markdown de análisis curricular. Es un conteo histórico de la rama/commit allí indicado; debe regenerarse desde el HEAD actual antes de utilizarlo como cifra de estado vigente.

El documento `contenido/00-estado-contenido.md` declara:
- 1.º–4.º básico: 4 asignaturas principales por curso.
- 5.º básico–2.º medio: 5 asignaturas principales por curso.
- 3.º–4.º medio: 6 asignaturas principales por curso.
- 156 pruebas de unidad, 58 pruebas por asignatura y 92 archivos de examen/simulacro según su propia descripción.
- En el régimen C existe una discrepancia documentada entre 449 preguntas y un total aproximado posterior de 555, pendiente de recálculo.

Estas cifras son declaraciones de documentos fuente; no certifican exactitud de preguntas, integridad del contenido ni alineación curricular.

## 3. Estado de auditoría por dimensión

| Dimensión | Estado actual | Criterio para marcar completado |
|---|---|---|
| Inventario de archivos y cursos | Parcialmente documentado | Recalcular el árbol del HEAD vigente y guardar la salida reproducible |
| Inventario de asignaturas | Consolidado de forma documental; falta cotejo actual del árbol | Confirmar cada ruta existente y detectar recursos adicionales/subdirectorios |
| Cobertura curricular | Declarada por los documentos de contenido; no certificada integralmente | Cotejar OA y contenido real con fuente oficial aplicable, registrando URL, versión y evidencia |
| Exactitud de ejercicios/respuestas | Pendiente de auditoría exhaustiva | Resolver cada ejercicio o justificar clave y retroalimentación con evidencia |
| Calidad pedagógica | Pendiente de auditoría exhaustiva por curso/asignatura | Revisar progresión, claridad, edad, accesibilidad, inclusión y retroalimentación |
| Integridad de parser/importación | Pendiente de validación completa por tipo de contenido | Contrastar contenido fuente con lo que parser e importador efectivamente reconocen |
| UX y evaluación en aplicación | Hay hallazgos documentados; no es el foco de esta matriz | Reproducir cada hallazgo y verificar con pruebas en fase separada |
| Certificación final | No iniciada | No emitir conclusión global hasta cerrar las dimensiones anteriores y registrar excepciones |

## 4. Método de auditoría obligatorio por archivo

Para cada combinación curso-asignatura:

1. Registrar ruta, hash/commit inspeccionado y fecha.
2. Identificar modalidad y programa curricular aplicable.
3. Extraer OA, indicadores, conceptos, ejemplos, actividades, preguntas, opciones, respuestas, rúbricas y retroalimentación.
4. Comparar cobertura con la fuente oficial, citando documento, versión y sección.
5. Verificar independientemente cada respuesta; en Matemática, resolver paso a paso. Para otras materias, comprobar hechos y razonamiento contra fuentes confiables y el nivel curricular.
6. Evaluar si el enunciado tiene información suficiente, si la clave es única cuando corresponde y si la retroalimentación enseña correctamente.
7. Marcar cada elemento como `pendiente`, `sin observaciones en revisión`, `hallazgo probable`, `hallazgo confirmado`, `corregido pendiente de verificación` o `corrección verificada`.
8. Separar observaciones objetivas, inferencias y recomendaciones.
9. Guardar hallazgos con identificador estable, severidad, evidencia, corrección sugerida y prueba de regresión.
10. No editar el contenido original durante la fase de diagnóstico, salvo autorización específica para una corrección crítica acordada.

## 5. Fases y orden de ejecución

### Fase 0 — Control y trazabilidad
- Confirmar HEAD, rama y diferencia con `main`.
- No mezclar la rama de gobernanza documental con la rama de auditoría sin dejar registro explícito.
- Mantener una bitácora para el siguiente agente: última ruta inspeccionada, resultado, pendientes y siguiente paso.

### Fase 1 — Inventario reproducible
- Enumerar rutas reales de contenido, pruebas, exámenes, temarios y recursos auxiliares.
- Recalcular conteos y resolver discrepancias de cifras.
- Distinguir archivos principales, bancos de preguntas, pruebas de unidad y simulacros.

### Fase 2 — Matriz curricular por curso y asignatura
- Determinar alcance del producto y modalidad aplicable.
- Comparar cada asignatura con las fuentes oficiales pertinentes.
- Registrar cobertura completa, parcial, no demostrada, fuera de alcance o no aplicable.

### Fase 3 — Auditoría sustantiva en paralelo
- Línea A: Matemática, resolución paso a paso y verificación de claves.
- Línea B: Lenguaje/Lengua y Literatura, comprensión, vocabulario, ortografía y textos.
- Línea C: Ciencias Naturales/Ciencias para la Ciudadanía, exactitud científica y modelos.
- Línea D: Historia/Geografía/Ciencias Sociales/Educación Ciudadana/Filosofía, exactitud factual, temporal y conceptual.
- Línea E: Inglés, corrección lingüística y progresión por nivel.
- Los hilos/líneas pueden avanzar por separado, pero todos deben usar el mismo esquema de evidencia y reportar hallazgos al registro maestro. La paralelización no debe presentarse como trabajo ejecutado en segundo plano.

### Fase 4 — Revisión cruzada
- Revisar duplicados, claves, retroalimentación, nivel de dificultad, inclusividad, derechos de uso de textos/medios y consistencia entre guía y evaluación.
- Contrastar el material fuente con la salida del parser y lo que realmente consume la aplicación.

### Fase 5 — Informe de cierre
- Publicar cobertura, defectos confirmados, pendientes, riesgos y limitaciones por curso/asignatura.
- No declarar un curso “completo” solo porque haya archivos, OA o tests estructurales.
- El informe global solo se cierra cuando cada unidad del inventario tenga estado y evidencia, o una excepción explícita.

### Fase 6 — Plan de correcciones (posterior al diagnóstico)
- Priorizar riesgos críticos y de alto impacto educativo.
- Presentar el plan de cambios y las pruebas de regresión.
- Implementar solo en una fase autorizada y separada.

## 6. Puntos de entrada para el siguiente agente

1. Leer este archivo.
2. Leer `docs/auditorias/inventario-reproducible-contenido-educativo.md`.
3. Leer `docs/auditorias/matematica/README.md` y `docs/auditorias/matematica/01-inventario-auditoria.md` en la rama de gobernanza documental, respetando la rama correcta y sin asumir que las dos ramas contienen idénticos commits.
4. Leer `contenido/00-estado-contenido.md` y `Temarios/analisis/00-resumen-general.md`.
5. Verificar el árbol real del HEAD antes de continuar.
6. Comenzar por recalcular el inventario y luego seleccionar el primer lote de archivos para auditoría sustantiva.

## 7. Criterio de cierre

La auditoría integral se considera cerrada solo cuando:
- todos los archivos relevantes del inventario tienen estado;
- cada curso/asignatura tiene una evaluación curricular sustentada;
- todas las preguntas evaluativas tienen respuesta/clave y retroalimentación verificadas, o una excepción explícita;
- los hallazgos están registrados y priorizados;
- las limitaciones y los elementos fuera de alcance se declaran;
- otro agente puede retomar el proceso desde este documento sin depender de conversaciones privadas.

**Estado al publicar:** esta matriz consolida el mapa documental disponible y define el método. No certifica todavía las 52 guías ni todos los bancos, pruebas y exámenes.
