# Roadmap de Inteligencia Educativa para Logos School

**Estado:** propuesta de producto y arquitectura; no implica funcionalidades implementadas.
**Objetivo:** incorporar capacidades de analítica y apoyo educativo de forma gradual, medible y segura.

## Visión

Logos School puede evolucionar hacia una plataforma que observe señales educativas relevantes, detecte dificultades a tiempo y recomiende acciones de apoyo. La IA debe apoyar a estudiantes, familias y responsables educativos; no reemplazar su criterio ni etiquetar permanentemente a los alumnos.

## Ideas de producto

1. **Seguimiento de actividad:** sesiones, última actividad, actividades iniciadas/completadas y evolución semanal.
2. **Alertas tempranas:** detectar cambios sostenidos de participación, tareas pendientes o descenso en resultados; mostrar las señales que originaron la alerta.
3. **Perfil de dominio por objetivo:** estimar qué objetivos de aprendizaje están consolidados y cuáles requieren práctica adicional.
4. **Práctica personalizada:** recomendar ejercicios según errores observados y comprobar después si hubo mejora.
5. **Tutor educativo contextual:** explicar paso a paso, ofrecer pistas progresivas y usar contenido curricular aprobado de Logos School.
6. **Tarjetas de errores frecuentes:** convertir patrones de error en actividades cortas de refuerzo.
7. **Gamificación adaptativa:** misiones y desafíos ajustados al dominio del contenido, sin penalizar al estudiante por necesitar más práctica.
8. **Informes para familias:** resumen semanal de avances, contenidos por reforzar y sugerencias concretas.
9. **Simulaciones interactivas:** experiencias manipulables para temas como fracciones, geometría y ciencias.
10. **Asistente para docentes/administradores:** resumir tendencias agregadas y priorizar casos que requieren revisión humana.

## MVP recomendado

### Fase 1 — Datos confiables
- Revisar el modelo actual de estudiantes, cursos, actividades, intentos y respuestas.
- Identificar qué eventos ya se persisten y qué datos faltan.
- Definir eventos mínimos: actividad iniciada, respuesta enviada, intento finalizado, actividad completada y última interacción.
- Registrar solo los datos necesarios y establecer retención y controles de acceso.

### Fase 2 — Seguimiento descriptivo
- Crear indicadores de actividad por período.
- Mostrar tareas pendientes, cambios de participación y evolución de resultados.
- Empezar con reglas transparentes configurables; no presentar estas reglas como predicciones de IA.
- Permitir revisar, descartar y documentar alertas.

### Fase 3 — Intervenciones personalizadas
- Recomendar ejercicios vinculados a objetivos de aprendizaje y errores concretos.
- Dar pistas progresivas antes de entregar una solución.
- Medir si la intervención mejora el resultado en ejercicios nuevos.

### Fase 4 — Evaluación predictiva
- Definir operacionalmente qué significa “abandono” y el horizonte de predicción.
- Entrenar y validar un modelo solo cuando haya datos históricos suficientes y representativos.
- Evaluar precisión, recuperación, calibración y falsos positivos; comprobar diferencias entre grupos.
- Mostrar estimaciones como señales de apoyo, nunca como certezas ni decisiones automáticas.

## Arquitectura de referencia

- Backend existente de Java/Spring Boot como punto de partida.
- PostgreSQL para eventos y resultados, tras revisar el esquema actual.
- SQL y tareas programadas para los primeros indicadores.
- Python/scikit-learn solo si se justifica un modelo predictivo.
- Modelo de lenguaje mediante una integración aislada para explicaciones o tutoría, fundamentado en contenido curricular revisado.
- Separar el registro de eventos, las reglas de alerta, las recomendaciones y la interfaz administrativa según crezca la necesidad.

No introducir Kafka, microservicios ni una plataforma de ML compleja en el MVP sin evidencia de que sean necesarios.

## Privacidad, seguridad y uso responsable

- Logos School está orientado a estudiantes menores de edad: aplicar minimización de datos, acceso por rol, retención limitada y protección de información.
- No inferir emociones, salud ni circunstancias familiares a partir de señales débiles.
- No usar tiempo conectado o frecuencia de acceso como sustitutos del aprendizaje.
- Dar explicaciones comprensibles de las alertas y permitir revisión humana.
- Evitar que una predicción afecte automáticamente calificaciones, matrícula o acceso a contenidos.
- Revisar obligaciones legales aplicables en Chile antes de procesar datos personales de estudiantes.

## Métricas para validar valor

- Porcentaje de actividades completadas.
- Evolución del dominio en evaluaciones posteriores.
- Porcentaje de alertas revisadas que conducen a una intervención útil.
- Falsos positivos y alertas no accionables.
- Mejora tras las recomendaciones frente a una línea base comparable.
- Accesibilidad, tiempo de respuesta y satisfacción de estudiantes y familias.

## Próximos pasos técnicos

1. Auditar el esquema y los flujos existentes antes de diseñar nuevas tablas o endpoints.
2. Mapear dónde se registran actualmente intentos, respuestas, calificaciones y actividad.
3. Proponer un contrato de eventos mínimo y una política de retención.
4. Diseñar un panel descriptivo inicial y reglas explicables.
5. Revisar la propuesta con criterios educativos, privacidad y seguridad antes de implementarla.

**Importante:** este documento registra una dirección de producto. No afirma que las funcionalidades estén implementadas ni que exista ya un modelo predictivo entrenado.
