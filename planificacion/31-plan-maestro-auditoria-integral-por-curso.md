# Plan Maestro de Auditoría Integral por Curso
**Versión:** 1.0
**Fecha:** 2026-10-18
**Objetivo:** Auditar sistémicamente cada curso (1° básico a 4° medio) probando TODA la funcionalidad, calidad del material, usabilidad y experiencia del usuario sin omitir nada.

---

## 📋 Estructura del Plan

Cada curso se audita siguiendo este checklist completo. Ningún paso se puede omitir.

---

## 🔍 Fase 1: Verificación de Estructura del Curso

### 1.1 Verificar que el curso existe en la base de datos
- [ ] El nivel está creado en la base de datos
- [ ] Las asignaturas del curso están configuradas correctamente
- [ ] El régimen de examen es correcto (A/B/C según el curso)
- [ ] El número de preguntas del examen simulacro es correcto

### 1.2 Verificar contenido curricular
- [ ] Los OAs oficiales están importados desde `Temarios/analisis/`
- [ ] El número de OAs coincide con el temario oficial Mineduc
- [ ] Los ejes temáticos están correctamente configurados
- [ ] Las asignaturas coinciden con el temario oficial

---

## 📚 Fase 2: Auditoría de Contenido por Asignatura

Por cada asignatura del curso (Lenguaje, Matemática, Ciencias, Historia, etc.):

### 2.1 Verificar Guías de Estudio
- [ ] Cada OA tiene una guía de estudio
- [ ] La guía tiene la estructura correcta:
  - [ ] Título del OA
  - [ ] Sección "¿Por qué importa?"
  - [ ] Ejemplos resueltos
  - [ ] Preguntas de autoevaluación
- [ ] El contenido es pedagógicamente apropiado para la edad
- [ ] El lenguaje es comprensible para el nivel
- [ ] Los ejemplos son relevantes y claros
- [ ] Las preguntas de autoevaluación tienen respuestas correctas
- [ ] Las retroalimentaciones son útiles y constructivas

### 2.2 Verificar Calidad del Contenido
- [ ] El contenido no tiene errores gramaticales ni ortográficos
- [ ] Los ejemplos numéricos son correctos
- [ ] Las explicaciones son precisas y completas
- [ ] No hay contradicciones internas
- [ ] El contenido sigue una progresión lógica

### 2.3 Verificar Elementos Visuales
- [ ] Los emojis educativos están presentes (si aplica al nivel)
- [ ] Los emojis son apropiados para el contexto
- [ ] Los componentes matemáticos están integrados (si aplica: Matemática)
- [ ] El contenido visual es atractivo y no confuso
- [ ] El formato es consistente entre secciones

### 2.4 Verificar Banco de Autoevaluación
- [ ] Cada OA tiene preguntas de autoevaluación
- [ ] Las preguntas cubren todos los indicadores de evaluación
- [ ] Los tipos de preguntas son variados (alternativas, V/F, desarrollo)
- [ ] Las respuestas correctas son efectivamente correctas
- [ ] Las retroalimentaciones son específicas y útiles
- [ ] No hay preguntas duplicadas o redundantes

### 2.5 Verificar Pruebas de Unidad
- [ ] Hay pruebas de unidad para cada asignatura
- [ ] El número de preguntas por prueba es apropiado para la edad
- [ ] Las pruebas cubren los OAs de la unidad
- [ ] Las preguntas están bien calibradas en dificultad
- [ ] Las pruebas pueden rendirse múltiples veces

### 2.6 Verificar Exámenes Simulacro
- [ ] Hay examen simulacro del formato correcto:
  - [ ] Régimen A: 1 examen integrado de 20 preguntas
  - [ ] Régimen B: 1 examen por asignatura de 25 preguntas
  - [ ] Régimen C: 1 examen por asignatura de 25 preguntas
- [ ] Las preguntas imitan el formato del examen real Mineduc
- [ ] El tiempo sugerido es apropiado
- [ ] Hay Forma A y Forma B para cada examen

---

## 🎭 Fase 3: Auditoría de Usabilidad del Alumno

### 3.1 Registro y Onboarding
- [ ] El registro funciona correctamente
- [ ] El formulario de agregar alumno es claro
- [ ] El RUT se valida correctamente
- [ ] El onboarding aparece la primera vez
- [ ] El checklist de primeros pasos es claro
- [ ] El check-in emocional aparece cuando debe aparecer

### 3.2 Navegación del Panel del Alumno
- [ ] El sidebar es claro y navegable
- [ ] Las secciones son comprensibles para la edad
- [ ] El diseño es atractivo y no confuso
- [ ] Los iconos son intuitivos
- [ ] Los colores de identidad por asignatura son claros

### 3.3 Flujo de Estudio
- [ ] Ir a Mis Asignaturas funciona
- [ ] Ver las asignaturas del curso funciona
- [ ] Entrar a una asignatura funciona
- [ ] Ver las guías de estudio funciona
- [ ] Abrir una guía funciona
- [ ] El contenido se carga correctamente
- [ ] El botón de lectura en voz alta funciona
- [ ] El botón de descargar PDF funciona
- [ ] El botón de practicar es claro
- [ ] La calificación por estrellas funciona

### 3.4 Flujo de Evaluación
- [ ] Ir a Pruebas y Exámenes funciona
- [ ] Ver las pruebas disponibles funciona
- [ ] Iniciar una prueba funciona
- [ ] El motor de evaluación funciona:
  - [ ] Navegación pregunta a pregunta
  - [ ] Mapa de preguntas funciona
  - [ ] Marcar preguntas respondidas
  - [ ] Cronómetro funciona (en exámenes)
  - [ ] Retomar intento funciona
  - [ ] Entregar prueba funciona
  - [ ] Alerta de preguntas sin responder funciona
- [ ] El resultado se muestra correctamente:
  - [ ] Nota calculada correctamente
  - [ ] Desglose por pregunta
  - [ ] Opción de revisión
  - [ ] Botón de volver

### 3.5 Verificar Mis Notas
- [ ] El historial de notas se muestra correctamente
- [ ] Las notas están ordenadas cronológicamente
- [ ] El progreso por asignatura es visible
- [ ] El porcentaje de avance es correcto
- [ ] El detalle por OA funciona
- [ ] La nota estimada del examen libre es visible (si aplica)

### 3.6 Verificar Mis Logros
- [ ] El nivel y XP son visibles
- [ ] La grilla de avatares funciona
- [ ] Elegir avatar funciona
- [ ] Las insignias son visibles
- [ ] El jardín semanal funciona
- [ ] Las estadísticas de uso son visibles

### 3.7 Verificar Plan de Estudio
- [ ] El plan de estudio se genera correctamente
- [ ] Las sesiones están bien distribuidas
- [ ] Vista lista/semanal/mensual funciona
- [ ] Marcar sesión como completada funciona
- [ ] Las sesiones atrasadas se muestran
- [ ] El plan de repaso funciona (si aplica)

### 3.8 Verificar Otras Funcionalidades
- [ ] Búsqueda global funciona
- [ ] Ayuda contextual funciona
- [ ] Configuración del alumno funciona
- [ ] Reportar error funciona
- [ ] Útiles escolares funciona (si aplica)
- [ ] Plan lector funciona (si aplica)

---

## 👨‍👩‍👧 Fase 4: Auditoría de Usabilidad del Apoderado

### 4.1 Panel del Apoderado
- [ ] El panel del apoderado es accesible
- [ ] Ver los alumnos del apoderado funciona
- [ ] Ver el progreso de cada alumno funciona
- [ ] Agregar alumno inline funciona
- [ ] Eliminar alumno funciona
- [ ] Ver el plan y pagos funciona
- [ ] Ver el historial de pagos funciona
- [ ] La agenda familiar funciona
- [ ] Las observaciones de horario funcionan

---

## 🎓 Fase 5: Auditoría de Usabilidad del Profesor

### 5.1 Flujo del Profesor
- [ ] Registro de profesor funciona
- [ ] Aprobación por admin funciona
- [ ] Crear curso funciona
- [ ] Agregar alumnos al curso funciona
- [ ] Ver progreso del curso funciona
- [ ] Enviar comunicados funciona
- [ ] No se puede agregar alumno de nivel distinto

---

## 🔧 Fase 6: Auditoría Técnica

### 6.1 Verificar Responsive
- [ ] La landing funciona en móvil
- [ ] El sidebar colapsa en móvil
- [ ] El contenido es legible en móvil
- [ ] Los botones son accesibles en móvil
- [ ] No hay scroll horizontal no deseado

### 6.2 Verificar Accesibilidad
- [ ] No hay violaciones WCAG AA graves
- [ ] El contraste de color es correcto
- [ ] Los formularios tienen labels apropiados
- [ ] Los botones tienen aria-label apropiados
- [ ] La campana de notificaciones cumple WCAG

### 6.3 Verificar Performance
- [ ] La página carga en tiempo razonable
- [ ] Las transiciones son suaves
- [ ] No hay errores de consola
- [ ] Las imágenes cargan correctamente
- [ ] El build compila sin warnings críticos

### 6.4 Verificar Tests
- [ ] Los tests E2E del curso pasan
- [ ] Los tests de accesibilidad pasan
- [ ] Los tests de funcionalidad pasan
- [ ] No hay tests fallidos bloqueantes

---

## 🎨 Fase 7: Auditoría de Diseño y Marca

### 7.1 Verificar Identidad Visual
- [ ] Los colores de marca son consistentes
- [ ] La tipografía es consistente
- [ ] El logo es visible
- [ ] Los componentes siguen el sistema de diseño
- [ ] No hay estilos inconsistentes

### 7.2 Verificar Apropiación por Edad
- [ ] El diseño es apropiado para la edad del curso
- [ ] El lenguaje es apropiado para la edad
- [ ] Los emojis son apropiados para la edad
- [ ] La gamificación es motivadora para la edad
- [ ] No hay contenido inapropiado

---

## 📊 Fase 8: Auditoría de Datos

### 8.1 Verificar Integridad de Datos
- [ ] Los datos del curso en la DB son correctos
- [ ] No hay datos corruptos
- [ ] No hay duplicados
- [ ] Las relaciones entre tablas son correctas
- [ ] Las foreign keys se respetan

### 8.2 Verificar Consistencia
- [ ] El contenido de la DB coincide con los archivos Markdown
- [ ] El número de preguntas coincide con la documentación
- [ ] El número de OAs coincide con el temario oficial
- [ ] Los nombres de asignaturas son consistentes

---

## 🔨 Fase 9: Corrección de Problemas Encontrados

### 9.1 Problemas de Contenido
- [ ] Corregir errores gramaticales y ortográficos
- [ ] Corregir errores conceptuales
- [ ] Mejorar explicaciones poco claras
- [ ] Agregar ejemplos cuando sea necesario
- [ ] Corregir respuestas incorrectas
- [ ] Mejorar retroalimentaciones

### 9.2 Problemas de Usabilidad
- [ ] Mejorar textos confusos
- [ ] Simplificar flujos complejos
- [ ] Agregar mensajes claros cuando algo falta
- [ ] Mejorar navegación
- [ ] Corregir elementos no intuitivos

### 9.3 Problemas Técnicos
- [ ] Corregir errores de consola
- [ ] Corregir violaciones de accesibilidad
- [ ] Corregir problemas de responsive
- [ ] Corregir problemas de performance
- [ ] Corregir tests fallidos

### 9.4 Problemas de Diseño
- [ ] Corregir inconsistencias visuales
- [ ] Mejorar contraste de color
- [ ] Ajustar tipografía
- [ ] Mejorar espacios y alineación

---

## 📝 Fase 10: Documentación y Reporte

### 10.1 Documentar Hallazgos
- [ ] Crear documento de auditoría del curso
- [ ] Listar todos los problemas encontrados
- [ ] Clasificar problemas por severidad (crítico, alto, medio, bajo)
- [ ] Documentar todas las correcciones aplicadas
- [ ] Registrar cambios en version control

### 10.2 Verificar Correcciones
- [ ] Re-ejecutar tests después de correcciones
- [ ] Verificar que los problemas no reaparecen
- [ ] Verificar que no se introdujeron nuevos problemas
- [ ] Hacer commit de todas las correcciones

---

## 🎯 Criterios de Aprobación del Curso

Un curso se considera **APROBADO** solo cuando:

1. ✅ Todas las fases del plan han sido completadas
2. ✅ Todos los items del checklist están marcados
3. ✅ No hay problemas críticos o altos sin corregir
4. ✅ Todos los tests E2E pasan
5. ✅ Todos los tests de accesibilidad pasan
6. ✅ El contenido es pedagógicamente apropiado
7. ✅ La usabilidad es excelente para la edad
8. ✅ El diseño es consistente y atractivo
9. ✅ No hay errores técnicos
10. ✅ La documentación está completa

---

## 📅 Orden de Auditoría de Cursos

1. **1° Básico** ✅ (Auditoría inicial completada - pendiente correcciones)
2. **2° Básico** (Pendiente)
3. **3° Básico** (Pendiente)
4. **4° Básico** (Pendiente)
5. **5° Básico** (Pendiente)
6. **6° Básico** (Pendiente)
7. **7° Básico** (Pendiente)
8. **8° Básico** (Pendiente)
9. **1° Medio** (Pendiente)
10. **2° Medio** (Pendiente)
11. **3° Medio** (Pendiente)
12. **4° Medio** (Pendiente)

---

## 🔁 Iteración

Si un curso no cumple los criterios de aprobación:
1. Documentar todos los problemas
2. Priorizar correcciones por severidad
3. Aplicar correcciones
4. Re-auditar las fases afectadas
5. Repetir hasta cumplir criterios de aprobación

---

## 📌 Notas Importantes

- **Ningún paso se puede omitir.** Si algo no aplica al curso, marcar como "N/A" con justificación.
- **Todos los problemas deben corregirse.** Los problemas críticos bloquean la aprobación.
- **La usabilidad se evalúa desde la perspectiva del usuario real del curso** (niño de esa edad, apoderado, profesor).
- **La calidad pedagógica es tan importante como la calidad técnica.**
- **La autonomía es clave:** Corregir problemas sin consultar al usuario, documentar después.
