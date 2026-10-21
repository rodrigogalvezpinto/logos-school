# Backlog de producto: tutor IA y evaluación de lectura

**Fecha de registro:** 21 de octubre de 2026  
**Estado:** Ideas priorizadas para descubrimiento y validación; no implementadas ni aprobadas para producción.  
**Ámbito:** Producto educativo de Logos School para estudiantes de Chile.

## Objetivo

Mantener un backlog único de funcionalidades potenciales, con prioridad, valor educativo, dependencias y criterios de validación. Las ideas no deben pasar directamente de una conversación a producción: primero se aclara el problema, luego se define un MVP y se valida técnica y pedagógicamente.

## 1. Evaluación de lectura — idea propuesta por el usuario

### Objetivo
Recuperar y evaluar una funcionalidad que ya existió en otra aplicación del usuario, adaptándola a Logos School después de recuperar la especificación original si está disponible.

### Capacidades posibles
1. **Lectura en voz alta:** el estudiante lee un texto adecuado a su curso por micrófono.
2. **Alineación entre texto y transcripción:** identificar palabras posiblemente omitidas, sustituidas, añadidas o autocorregidas, mostrando confianza y permitiendo revisión.
3. **Fluidez:** observar precisión, ritmo/velocidad y prosodia/pausas; nunca usar velocidad como único indicador.
4. **Comprensión lectora:** preguntas posteriores sobre información explícita, inferencias, vocabulario e idea principal.
5. **Seguimiento:** comparar resultados de varias lecturas y recomendar práctica concreta.
6. **Informe para familias/docentes:** mostrar evidencia y evolución sin presentar la estimación automática como diagnóstico clínico.

### MVP recomendado
- Seleccionar un curso y un texto breve con derechos de uso claros.
- Grabar la lectura solo después de explicar al apoderado/estudiante el propósito y solicitar los consentimientos necesarios.
- Transcribir y alinear la lectura con el texto esperado.
- Mostrar posibles errores para revisión; no tratar automáticamente toda diferencia de pronunciación, acento, tartamudeo, ruido o transcripción como error lector.
- Hacer 3–5 preguntas de comprensión.
- Entregar un informe sencillo de precisión estimada, palabras por minuto, pausas observadas y respuestas de comprensión, con advertencias sobre límites.
- Probar primero con un conjunto pequeño de grabaciones consentidas y revisadas por una persona competente.

### Validación necesaria
- Comparar transcripciones y detección de errores con anotaciones humanas.
- Probar acentos del español de Chile, micrófonos distintos, ruido y estudiantes de distintos cursos.
- Revisar sesgos y falsos positivos; permitir repetir la grabación y corregir errores de reconocimiento.
- Validar textos, rúbricas y criterios con docentes y currículo MINEDUC vigente.
- Definir minimización de datos, acceso, retención y eliminación de audios. Evitar almacenar audio si no es necesario; nunca usar voces de menores para entrenar modelos sin una base legal y consentimiento explícitos.
- No usar el resultado como diagnóstico de dislexia ni de otra condición.

## 2. Profesor agente contextual

**Prioridad propuesta:** alta, tras verificar qué datos de respuestas e intentos se guardan actualmente.

- Acompaña una sesión activa y también responde cuando el alumno pulsa «Necesito ayuda».
- Recibe solo el contexto necesario: curso, OA, ejercicio actual, intentos disponibles y ayudas ya mostradas.
- Utiliza ayuda gradual: pregunta, pista, explicación alternativa y finalmente solución razonada.
- Se abstiene de resolver por el alumno durante evaluaciones formales cuando las reglas no permiten ayuda.
- Al final resume lo practicado y recomienda el siguiente paso, distinguiendo datos observados de inferencias.
- Debe tener límites de uso, controles de costos, registro mínimo, protección de datos y rutas de escalamiento a un adulto si surge una situación preocupante.

## 3. Otras ideas candidatas

| Idea | Valor educativo esperado | Prioridad preliminar | Dependencia / condición |
|---|---|---|---|
| Tutor IA contextual con pistas | Ayuda inmediata ligada al ejercicio | Alta | Verificar contexto y persistencia de intentos |
| Evaluación de lectura oral | Medir y practicar fluidez lectora | Alta para descubrimiento | Recuperar especificación previa y validar con docentes |
| Comprensión lectora | Identificar comprensión literal e inferencial | Alta | Banco de textos y preguntas validados |
| Resumen de sesión | Hacer visible qué se practicó y qué falta | Alta | Datos de sesión confiables |
| Plan de práctica adaptativo | Recomendar actividades según evidencias | Media | Métricas longitudinales y criterios pedagógicos |
| Voz para leer instrucciones y explicaciones | Accesibilidad y apoyo a lectores | Media | Comparación de proveedores y costos |
| Videos educativos cortos | Explicar conceptos difíciles | Media | Guion revisado y prueba de comprensión |
| Juegos interactivos ligados a OA | Practicar con actividades motivadoras | Media | Piloto pequeño y registro fiable de resultados |
| Panel para padres/docentes | Comunicar progreso y necesidades de apoyo | Media | Privacidad, roles y evidencia suficiente |

Estas prioridades son iniciales; deben revisarse con evidencia, alcance, costo y esfuerzo de mantenimiento.

## 4. Cómo gobernar nuevas ideas

Cada idea debe registrar:
- Problema educativo que resuelve y usuarios beneficiados.
- Curso/asignatura/OA relacionado.
- Hipótesis de valor y cómo se medirá.
- Alcance mínimo (MVP) y qué queda explícitamente fuera.
- Dependencias técnicas, datos requeridos, riesgos de seguridad/privacidad y costo recurrente.
- Estado: **Idea → Por investigar → Diseñada → En validación → Aprobada → En desarrollo → Medida → Descartada**.
- Responsable, fecha de revisión y evidencia de decisión.

No aprobar una funcionalidad solo por ser atractiva o novedosa. Debe demostrar valor para el aprendizaje, ser viable y respetar la privacidad de menores.

## 5. Orden recomendado para decidir

1. Recuperar la descripción exacta de la evaluación de lectura de la aplicación anterior: flujo, métricas, proveedor de reconocimiento, limitaciones y resultados conocidos.
2. Auditar en Logos School la persistencia de respuestas, intentos y sesiones antes de diseñar seguimiento personalizado.
3. Definir un prototipo de lectura oral y una rúbrica de revisión humana.
4. Evaluar en paralelo un prototipo pequeño del tutor contextual.
5. Comparar precisión, utilidad educativa, accesibilidad, latencia, costo y esfuerzo de mantenimiento.
6. Elegir el primer MVP con evidencia y autorización explícita; no hacer cambios de producción por el mero registro de esta idea.

## Referencia curricular

El currículo chileno trata la fluidez como precisión, velocidad y prosodia, y la entiende como apoyo a la comprensión, no como un fin en sí mismo. La evaluación de Logos School debe considerar también comprensión lectora y estar alineada al curso y a los objetivos oficiales.

- [MINEDUC — Organización curricular de Lenguaje y Comunicación](https://aprendoenlinea.mineduc.gob.cl/recursos/organizacion-curricular-lenguaje-comunicacion)
- [Currículum Nacional — Lectura y comprensión](https://www.curriculumnacional.cl/614/w3-propertyvalue-60145.html)
- [Dirección de Educación Pública — Evaluación de fluidez lectora](https://dep.gob.cl/mineduc/presentacion-deimpulso-lector-la-primera-evaluacion-censal-de-habilidades-lectoras-en-2-basico/)

## Limitaciones

La idea de evaluación de lectura se ha registrado como candidata; no se ha inspeccionado la aplicación anterior ni se ha verificado aún la arquitectura exacta que utilizaba. Las métricas descritas son opciones de diseño, no capacidades implementadas ni validadas. La precisión del reconocimiento de voz con niños y español chileno debe medirse antes de usar resultados con fines evaluativos.


## 1.1 Flujo de práctica propuesto: texto aleatorio por curso

**Aporte del usuario:** en la aplicación anterior, el estudiante pulsaba «Practicar» y podía escoger entre tres textos o recibir uno aleatorio. Para reducir la memorización o la selección del texto más fácil, se propone que Logos School priorice un texto aleatorio apropiado para el curso, manteniendo una opción de práctica libre separada si se desea.

### Flujo funcional candidato
1. El estudiante pulsa **«Practicar lectura»**.
2. Logos School identifica su curso configurado y selecciona un texto de un banco previamente revisado para ese nivel.
3. El texto se presenta en pantalla y se explica que debe leerlo en voz alta durante el tiempo definido por la evaluación.
4. Se captura la lectura mediante micrófono, con aviso claro sobre el uso del audio y los consentimientos aplicables.
5. El sistema compara la transcripción con el texto esperado e identifica posibles omisiones, sustituciones, adiciones y autocorrecciones, indicando incertidumbre cuando corresponda.
6. Se calculan métricas candidatas: palabras intentadas/leídas en el intervalo, precisión estimada, tipos de error y pausas observables.
7. Se realizan preguntas breves de comprensión, idealmente después de la lectura y sin pistas que alteren la medición inicial.
8. Se muestra una devolución comprensible y respetuosa, con una recomendación concreta para practicar.
9. Se registra el resultado mínimo necesario para observar evolución, respetando las políticas de privacidad y retención de datos.

### Criterios curriculares y de evaluación
- Cada texto y rúbrica debe asociarse a curso, objetivo de aprendizaje, dificultad y versión de la pauta.
- Los umbrales de palabras por minuto, tiempo y errores **no deben inventarse ni extrapolarse entre cursos**: se deben confirmar con fuentes oficiales vigentes del MINEDUC y validar con docentes especialistas antes de presentarlos como criterios curriculares.
- Si las fuentes oficiales no establecen un único umbral aplicable al contexto, el sistema debe mostrar métricas descriptivas y usar una rúbrica pedagógica validada, sin etiquetar automáticamente al niño como «bajo» o «deficiente».
- El texto aleatorio debe provenir de un conjunto de textos equivalentes en dificultad, no de una selección completamente libre que haga incomparables los resultados.
- Mantener una opción separada de lectura libre puede ser útil para practicar textos elegidos por el estudiante; no debería mezclarse con los resultados de evaluaciones comparables.
- Debe existir una forma de revisar o repetir una evaluación si hay mala calidad de audio, interrupciones o errores evidentes de reconocimiento.

### Decisión de diseño pendiente
Confirmar si la primera versión utilizará exclusivamente asignación aleatoria para evaluación comparable, o si ofrecerá dos modos: **Evaluación (texto aleatorio)** y **Práctica libre (texto elegido)**. La recomendación inicial es separar ambos modos para evitar que la elección del texto sesgue la medición.

### Validación específica
- Reunir textos y rúbricas por curso y revisar derechos de uso.
- Construir ejemplos de referencia anotados por evaluadores humanos.
- Medir precisión de transcripción y de detección de errores en español chileno, con distintos micrófonos y condiciones acústicas.
- Comparar métricas automáticas con la evaluación humana antes de mostrar resultados como puntuaciones.
- Probar si las recomendaciones ayudan a mejorar en lecturas nuevas, no solo en textos ya practicados.
