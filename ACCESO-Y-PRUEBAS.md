# 🚀 Guía de Acceso Rápido y Credenciales - Logos School

Para levantar automáticamente todos los servicios (Backend FastAPI + Frontend Angular) y ver en tu terminal las credenciales, ejecuta desde la raíz del proyecto:

```bash
./iniciar.sh
```

---

## 🔑 Credenciales para Probar la Plataforma

### 1. 👨‍👩‍👧‍👦 Cuenta Familiar (Alumno y Apoderado - Recomendada)
*Permite validar todo el flujo de estudio, evaluaciones, notas, gamificación y supervisión parental.*

- **URL de Acceso:** [http://localhost:4200/login](http://localhost:4200/login)
- **Email:** `apoderado.prueba@logos.cl`
- **Contraseña:** `Logos2026!`

#### Perfiles Disponibles al Iniciar Sesión:
1. **Sofía Pérez (4° Básico):**
   - Panel del Alumno ([http://localhost:4200/alumno/inicio](http://localhost:4200/alumno/inicio))
   - **Historial real:** Notas acumuladas, nivel 2 con 125 XP, 8 insignias desbloqueadas.
   - **Asignaturas:** Lenguaje, Matemática, Ciencias Naturales e Historia. Guías con voz sintetizada (`🔊 Escuchar`), calificación con estrellas y descarga en PDF.
   - **Evaluaciones:** Pruebas de unidad y examen simulacro con cronómetro activo.
   - **Plan Lector & Útiles:** Libros curados (*Papelucho*, *El Principito*) y lista de materiales escolares por asignatura.
2. **Mateo Pérez (6° Básico):**
   - Segundo ciclo básico con asignatura de Inglés y formato de 25 preguntas.
3. **Panel del Apoderado:**
   - Botón *"Ir al Panel del Apoderado"* ([http://localhost:4200/apoderado/inicio](http://localhost:4200/apoderado/inicio)).
   - **Coaching parental:** Tips pedagógicos antes de consultar notas.
   - **Certificados oficiales:** Descarga de Certificado de Alumno Regular en PDF con hash de validación.
   - **Informe académico:** Descarga del Informe de Avance general en PDF.
   - **Gestión:** Agregar o desvincular alumnos de forma interactiva.

---

### 2. 👩‍🏫 Cuenta de Profesor
*Para validar la interfaz de gestión docente y comunicación con estudiantes.*

- **URL de Acceso:** [http://localhost:4200/profesor/login](http://localhost:4200/profesor/login)
- **Email:** `profesor.prueba@logos.cl`
- **Contraseña:** `ProfesorLogos2026!`
- **Panel Docente:** Creación de cursos, asociación de asignaturas y publicación de comunicados.

---

### 3. 🛡️ Cuenta de Administrador
*Para supervisar la plataforma, métricas globales y aprobar cuentas docentes.*

- **URL de Acceso:** [http://localhost:4200/admin/login](http://localhost:4200/admin/login)
- **Email:** `admin.prueba@logos.cl`
- **Contraseña:** `AdminLogos2026!`
- **Panel Comercial:** Métricas de suscripciones, altas de cursos y aprobación/rechazo de solicitudes de profesores.

---

### 4. 📝 Registro de una Familia Nueva (Desde Cero)
*Para probar el flujo de onboarding completo tal como llega un nuevo cliente a la landing page.*

- **URL:** [http://localhost:4200/registro](http://localhost:4200/registro)
- **RUTs chilenos de prueba válidos (Módulo 11):**
  - `21.345.678-4`
  - `19.876.543-2`
  - `20.987.654-K`

---

## 🛠️ Servicios y Puertos Locales

| Servicio | Tecnología | URL Local |
|---|---|---|
| **Frontend** | Angular 22 | [http://localhost:4200](http://localhost:4200) |
| **Backend** | FastAPI + SQLModel | [http://localhost:8000](http://localhost:8000) |
| **Documentación Swagger** | OpenAPI | [http://localhost:8000/docs](http://localhost:8000/docs) |
| **Base de Datos** | PostgreSQL | `localhost:5432` (`logos_qa`) |
