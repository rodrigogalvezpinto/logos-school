# Plan de Pruebas QA Exhaustivas - Logos School
**Objetivo:** Encontrar vulnerabilidades, casos borde y errores en la aplicación
**Enfoque:** Pruebas agresivas, pensamiento fuera de la caja, casos extremos

---

## 🔴 Prioridad CRÍTICA: Seguridad y Validaciones

### 1.1 Validación de RUT
- [ ] RUT con dígito verificador incorrecto
- [ ] RUT con formato inválido (sin puntos, sin guion, con espacios)
- [ ] RUT con caracteres especiales
- [ ] RUT con solo números (sin dígito verificador)
- [ ] RUT vacío o nulo
- [ ] RUT duplicado (mismo RUT para diferentes alumnos)
- [ ] RUT con dígito verificador 'K' (mayúscula vs minúscula)

### 1.2 Protección de rutas
- [ ] Acceder a /alumno/ sin perfil activo
- [ ] Acceder a /apoderado/ sin sesión
- [ ] Acceder a /admin/ sin token admin
- [ ] Acceder a /profesor/ sin token profesor
- [ ] Intentar ver datos de otro alumno (cambiar ID en URL)
- [ ] Intentar modificar datos de otro alumno
- [ ] Intentar eliminar perfil de otro alumno

### 1.3 JWT Token
- [ ] Token expirado
- [ ] Token malformado
- [ ] Token de apoderado intentando acceder a rutas de admin
- [ ] Token de admin intentando acceder a rutas de profesor
- [ ] Token sin firma
- [ ] Token con firma incorrecta

### 1.4 Rate Limiting
- [ ] Exceder límite de registro (5/min)
- [ ] Exceder límite de login (10/min)
- [ ] Exceder límite de reporte de error (10/min)
- [ ] Exceder límite de comunicados (10/min)
- [ ] Bypass de rate limiting (cambiar IP, user-agent)

### 1.5 SQL Injection
- [ ] Inyectar SQL en email
- [ ] Inyectar SQL en nombre
- [ ] Inyectar SQL en RUT
- [ ] Inyectar SQL en búsqueda de alumnos
- [ ] Inyectar SQL en comentarios de reporte

### 1.6 XSS
- [ ] Inyectar script en nombre de alumno
- [ ] Inyectar script en comentarios
- [ ] Inyectar script en comunicados
- [ ] Inyectar script en respuestas de evaluación

### 1.7 CSRF
- [ ] Enviar POST sin token CSRF
- [ ] Enviar POST con token CSRF de otra sesión
- [ ] Reutilizar token CSRF antiguo

---

## 🟠 Prioridad ALTA: Casos Borde en Evaluaciones

### 2.1 Flujo de evaluación
- [ ] Iniciar intento ya existente (debe reanudar)
- [ ] Responder pregunta con respuesta vacía
- [ ] Responder pregunta con respuesta demasiado larga (>4000 chars)
- [ ] Responder pregunta con caracteres especiales
- [ ] Responder pregunta con caracteres Unicode extremos
- [ ] Entregar intento sin responder ninguna pregunta
- [ ] Entregar intento respondiendo solo 1 pregunta
- [ ] Entregar intento respondiendo todas las preguntas incorrectamente
- [ ] Entregar intento respondiendo todas las preguntas correctamente
- [ ] Intentar responder después de entregar
- [ ] Intentar ver detalle antes de entregar
- [ ] Intentar ver detalle de intento de otro alumno
- [ ] Intentar modificar respuestas después de entregar
- [ ] Reanudar intento después de 1 hora
- [ ] Reanudar intento después de 1 día
- [ ] Reanudar intento después de 1 semana
- [ ] Crear intento con conjunto_id que no existe
- [ ] Crear intento con perfil_alumno_id que no pertenece al apoderado

### 2.2 Cálculo de notas
- [ ] Verificar cálculo exacto de nota (escala 1.0-7.0)
- [ ] Verificar exigencia del 60%
- [ ] Preguntas con peso diferente (si aplica)
- [ ] Opciones vacías en preguntas de selección múltiple
- [ ] Respuesta correcta fuera de las opciones
- [ ] Preguntas de tipo desarrollo sin retroalimentación

---

## 🟡 Prioridad MEDIA: Casos Borde en Datos

### 3.1 Entidades inexistentes
- [ ] Acceder a OA que no existe
- [ ] Acceder a asignatura que no existe
- [ ] Acceder a nivel que no existe
- [ ] Acceder a plan que no existe
- [ ] Acceder a suscripción que no existe
- [ ] Acceder a curso/sección que no existe

### 3.2 Datos inválidos
- [ ] Email con formato inválido
- [ ] Email vacío
- [ ] Email con espacios al inicio/final
- [ ] Password con menos de 8 caracteres
- [ ] Password con más de 128 caracteres
- [ ] Password con solo números
- [ ] Password vacío
- [ ] Fecha de nacimiento en el futuro
- [ ] Fecha de nacimiento hoy
- [ ] Fecha de nacimiento hace 100 años
- [ ] Nombre vacío
- [ ] Nombre con solo espacios
- [ ] Nombre con caracteres especiales

### 3.3 Relaciones inconsistentes
- [ ] PerfilAlumno con cuenta_apoderado_id que no existe
- [ ] PerfilAlumno con nivel_id que no existe
- [ ] IntentoEvaluacion con perfil_alumno_id que no existe
- [ ] IntentoEvaluacion con conjunto_evaluacion_id que no existe
- [ ] Suscripcion con perfil_alumno_id que no existe
- [ ] Suscripcion con plan_id que no existe

---

## 🟢 Prioridad BAJA: Casos Borde en Funcionalidad

### 4.1 Gamificación
- [ ] XP negativo (si hay bug)
- [ ] XP que debería subir de nivel
- [ ] XP exacto en el límite de nivel
- [ ] Cambiar avatar a ID inválido
- [ ] Cambiar avatar a ID que no existe
- [ ] Racha de días máxima (día 365+)
- [ ] Racha de días con interrupción
- [ ] Logros duplicados

### 4.2 Plan de Estudio
- [ ] Crear plan con días_por_semana inválido (2, 6, 7)
- [ ] Crear plan con días_elegidos que no calzan con días_por_semana
- [ ] Crear plan con fecha_inicio en el pasado
- [ ] Crear plan con fecha_objetivo antes de fecha_inicio
- [ ] Crear repaso de nivel que no existe
- [ ] Crear repaso de nivel futuro
- [ ] Crear repaso de nivel ya cursado
- [ ] Marcar sesión como completada que no existe

### 4.3 Onboarding
- [ ] Completar paso que no existe
- [ ] Completar mismo paso dos veces
- [ ] Completar pasos fuera de orden
- [ ] Completar onboarding con perfil que no existe

---

## 🔵 Prioridad BAJA: Concurrencia y Performance

### 5.1 Concurrencia
- [ ] Dos usuarios iniciando el mismo intento simultáneamente
- [ ] Dos usuarios entregando el mismo intento simultáneamente
- [ ] Dos usuarios modificando el mismo perfil simultáneamente
- [ ] Dos usuarios registrando el mismo email simultáneamente
- [ ] Race condition en XP (entregar evaluación simultáneamente)

### 5.2 Performance
- [ ] Cargar 1000 preguntas en una sola respuesta
- [ ] Descargar PDF de guía con 100 páginas
- [ ] Generar informe de avance con todos los OA
- [ ] Cargar historial de notas con 100 intentos
- [ ] Renderizar 100 notificaciones simultáneamente

---

## 📊 Criterios de Aceptación

Una prueba se considera **PASADA** si:
- La aplicación maneja el caso borde gracefulmente (error 400, no 500)
- Hay mensaje de error claro y en español
- No hay exposición de datos sensibles
- No hay vulnerabilidad de seguridad
- No hay pérdida de datos

Una prueba se considera **FALLIDA** si:
- La aplicación crash (error 500)
- Hay vulnerabilidad de seguridad
- Hay exposición de datos sensibles
- Hay pérdida de datos
- El error es confuso o incomprensible para el usuario

---

## 🎯 Estrategia de Ejecución

1. **Pruebas automatizadas con Playwright** - Para flujos repetitivos
2. **Pruebas manuales con browser preview** - Para casos complejos
3. **Pruebas de seguridad con herramientas especializadas** - Si es necesario
4. **Análisis de código estático** - Para vulnerabilidades de código
5. **Pruebas de carga** - Para performance bajo estrés

---

## 📝 Registro de Hallazgos

Cada hallazgo debe documentar:
- Descripción del problema
- Severidad (crítica, alta, media, baja)
- Pasos para reproducir
- Comportamiento esperado vs actual
- Impacto en el usuario
- Recomendación de corrección
