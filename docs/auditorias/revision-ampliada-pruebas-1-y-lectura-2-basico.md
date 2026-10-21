# Auditoría de contenido — revisión ampliada de pruebas de 1° básico y lectura inicial de 2° básico

**Rama:** `qa/fase-2-matriz-trazabilidad`  
**Alcance de esta entrega:** revisión directa de 12 pruebas de unidad de 1° básico y lectura inicial de cuatro materiales principales de 2° básico. No constituye certificación completa de ninguno de los cursos.

## Hallazgos confirmados en pruebas de 1° básico

| ID | Archivo / ubicación | Evidencia | Evaluación | Severidad provisional | Acción |
|---|---|---|---|---|---|
| LS-1B-MAT-TEST-001 | `contenido/01-basico/pruebas/matematica-unidad-patrones-y-algebra.md`, preguntas 2 y 3 | Pregunta 2: “Completa la secuencia: 3, 6, 9, ___, 15”. Pregunta 3: “El patrón 20, 17, 14, 11 es decreciente”. El archivo declara OA 11 como fuente. | Son patrones numéricos con saltos de 3, incluida una secuencia decreciente desde 20. No son automáticamente incorrectos, pero requieren comprobarse contra el alcance específico del OA 11 vigente para 1° básico y el temario de validación usado por la app. La prueba no explicita en el encabezado qué desempeño concreto del OA evalúa cada ítem. | **P2 — Medio, pendiente de cotejo curricular** | Contrastar cada ítem con el OA oficial y el temario específico. Si el alcance del instrumento se limita a patrones repetitivos/ámbito más acotado, reemplazar por patrones acordes; en todo caso añadir trazabilidad por pregunta. |
| LS-1B-MAT-TEST-002 | `contenido/01-basico/pruebas/matematica-unidad-medicion-datos-probabilidades.md`, pregunta 2 | “Ordena estos tres objetos de más corto a más largo: una goma de borrar, un lápiz, y una regla.” La pauta asume goma < lápiz < regla. | Sin ilustración ni medidas, los objetos genéricos no tienen longitud garantizada: existen lápices más cortos que gomas y reglas de distintos tamaños. La clave depende de una suposición cotidiana, no de datos dados. | **P1 — Alto para la validez del ítem** | Añadir una imagen con los tres objetos alineados desde un mismo origen o indicar sus longitudes; actualizar la pauta para depender de la representación. |
| LS-1B-HIS-TEST-001 | `contenido/01-basico/pruebas/historia-unidad-historia.md`, pregunta 1 | “¿Qué haces primero en la mañana?”; clave: “Dormir toda la noche”. | No pregunta por una secuencia universal objetiva: rutinas familiares y horarios varían, y “dormir toda la noche” no es necesariamente la primera actividad de la mañana. El enunciado no está alineado de forma clara con una respuesta única. | **P2 — Medio** | Reformular como secuencia explícita de actividades de un personaje o preguntar “¿Qué suele ocurrir antes de levantarse por la mañana?” con contexto claro. |
| LS-1B-HIS-TEST-002 | `contenido/01-basico/pruebas/historia-unidad-historia.md`, pregunta 6 | “La cueca es el baile nacional de Chile. ¿Verdadero o falso?” | Es un dato cultural válido en el marco escolar, pero el ítem aislado mide recuerdo declarativo y no evidencia comprensión histórica o diversidad cultural. No es error factual identificado. | **P3 — Bajo, oportunidad didáctica** | Complementar con una pregunta de observación/interpretación cultural y representar tradiciones diversas sin exigir adhesión emocional. |

## Comprobaciones estructurales de 1° básico

- Las 12 pruebas de unidad recuperadas contienen preguntas numeradas y una pauta de respuestas.
- En los cuatro instrumentos de Matemática, los conteos declarados en metadatos coinciden con el número de ítems observados: Geometría 6; Medición/Datos 8; Números y Operaciones 8; Patrones y Álgebra 6.
- Las tres pruebas de Ciencias Naturales observadas incluyen pautas; la prueba de Ciencias de la Vida incluye una pregunta de seguridad sobre mirar al Sol, cuya respuesta indicada es “Falso”.
- Esta comprobación es estructural. No equivale a cotejar todos los ítems con todos los OA ni a verificar renderizado de imágenes, accesibilidad o ejecución en la plataforma.

## Lectura inicial de 2° básico

Se consultaron fragmentos de los cuatro materiales principales: Matemática, Lenguaje y Comunicación, Ciencias Naturales e Historia/Geografía/Ciencias Sociales.

1. **Trazabilidad curricular declarada:** los documentos citan Bases Curriculares/Decreto 439/2012 y temarios de validación. La cita declarada no demuestra por sí sola que cada sección y cada pregunta correspondan a la versión oficial vigente; se requiere cotejo OA por OA.
2. **Matemática:** el texto declara ámbito numérico hasta 100, sumas/restas sin reserva y tablas del 2, 5 y 10. Estas son afirmaciones verificables contra el temario, pero todavía no se auditó el documento completo ni el banco completo de preguntas.
3. **Lenguaje:** la explicación inicial de diptongo e hiato usa ejemplos coherentes en los fragmentos consultados (“cielo”, “aire”, “leemos”, “María”). Se debe seguir revisando precisión ortográfica y excepciones antes de darlo por aprobado.
4. **Ciencias Naturales:** el texto describe ciclos de vida de mamíferos, aves, insectos y anfibios. Algunas formulaciones son generalizaciones pedagógicas (“las aves adultas sí pueden volar”) que conviene revisar para evitar que una regla general se presente como universal, dado que existen aves no voladoras.
5. **Historia y Geografía:** el texto incluye numerosos pueblos originarios y menciona diferencias territoriales y culturales, lo cual es una fortaleza inicial. Las afirmaciones generales sobre roles de hombres y mujeres deben presentarse con cautela y evidencia específica por pueblo y época para no convertir tendencias variables en reglas universales.

## Acciones siguientes

- Terminar el cotejo de los cuatro documentos de 2° básico, recorriendo el resto de cada archivo y los bancos de preguntas.
- Verificar fuentes curriculares oficiales antes de cerrar los hallazgos pendientes.
- Corregir solo tras establecer el OA y el criterio de aceptación; no hacer cambios masivos por intuición.
- Continuar el inventario por nivel y asignatura, registrando brechas de cobertura separadas de errores pedagógicos.
