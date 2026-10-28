# QA - Inventario de Módulos y Funcionalidades
**Fecha:** 2026-10-18
**Versión:** 5717430
**Estado:** En construcción

---

## FRONTEND (Angular)

### Rutas Públicas

| ID | Ruta | Componente | Estado | Riesgos |
|----|------|------------|--------|---------|
| F001 | `/` | Landing page | Pendiente | |
| F002 | `/como-funciona` | Cómo funciona | Pendiente | |
| F003 | `/preguntas-frecuentes` | Preguntas frecuentes | Pendiente | |
| F004 | `/login` | Login apoderado | Pendiente | |
| F005 | `/registro` | Registro apoderado | Pendiente | |
| F006 | `/admin-login` | Login admin | Pendiente | |
| F007 | `/profesor-login` | Login profesor | Pendiente | |

### Rutas Protegidas - Apoderado/Alumno

| ID | Ruta | Componente | Guard | Estado | Riesgos |
|----|------|------------|-------|--------|---------|
| F008 | `/selector-perfil` | Selector de perfil | auth + perfil | Pendiente | |
| F009 | `/alumno/inicio` | Dashboard alumno | auth + perfil | Pendiente | |
| F010 | `/alumno/asignaturas` | Lista asignaturas | auth + perfil | Pendiente | |
| F011 | `/alumno/asignaturas/{id}` | Detalle asignatura | auth + perfil | Pendiente | |
| F012 | `/alumno/estudiar-oa/{id}` | Estudiar OA | auth + perfil | Pendiente | |
| F013 | `/alumno/autoevaluacion/{id}` | Autoevaluación | auth + perfil | Pendiente | |
| F014 | `/alumno/evaluaciones` | Lista evaluaciones | auth + perfil | Pendiente | |
| F015 | `/alumno/prueba-unidad/{id}` | Prueba unidad | auth + perfil | Pendiente | |
| F016 | `/alumno/examen-simulacro/{id}` | Examen simulacro | auth + perfil | Pendiente | |
| F017 | `/alumno/notas` | Historial notas | auth + perfil | Pendiente | |
| F018 | `/alumno/plan-estudio` | Plan estudio | auth + perfil | Pendiente | |
| F019 | `/alumno/logros` | Logros (gamificación) | auth + perfil | Pendiente | |
| F020 | `/alumno/plan-lector` | Plan lector | auth + perfil | Pendiente | |
| F021 | `/alumno/utiles-escolares` | Útiles escolares | auth + perfil | Pendiente | |
| F022 | `/alumno/configuracion` | Configuración | auth + perfil | Pendiente | |
| F023 | `/apoderado/inicio` | Dashboard apoderado | auth | Pendiente | |
| F024 | `/apoderado/progreso-alumno/{id}` | Progreso alumno | auth | Pendiente | |
| F025 | `/apoderado/estadisticas-familiares` | Estadísticas familiares | auth | Pendiente | |
| F026 | `/apoderado/historial-pagos` | Historial pagos | auth | Pendiente | |

### Rutas Protegidas - Admin

| ID | Ruta | Componente | Guard | Estado | Riesgos |
|----|------|------------|-------|--------|---------|
| F027 | `/admin/inicio` | Dashboard admin | admin | Pendiente | |
| F028 | `/admin/planes` | Gestión planes | admin | Pendiente | |
| F029 | `/admin/descuentos` | Gestión descuentos | admin | Pendiente | |
| F030 | `/admin/cortesias` | Gestión cortesías | admin | Pendiente | |
| F031 | `/admin/profesores` | Aprobación profesores | admin | Pendiente | |

### Rutas Protegidas - Profesor

| ID | Ruta | Componente | Guard | Estado | Riesgos |
|----|------|------------|-------|--------|---------|
| F032 | `/profesor/inicio` | Dashboard profesor | profesor | Pendiente | |
| F033 | `/profesor/cursos` | Mis cursos | profesor | Pendiente | |
| F034 | `/profesor/curso-detalle/{id}` | Detalle curso | profesor | Pendiente | |

### Componentes Reutilizables

| ID | Componente | Ubicación | Estado | Riesgos |
|----|------------|-----------|--------|---------|
| C001 | Sidebar | shared/sidebar/ | Pendiente | |
| C002 | Topbar | shared/topbar/ | Pendiente | |
| C003 | IconoAsignatura | shared/icono-asignatura/ | Pendiente | |
| C004 | BotonEscuchar | shared/boton-escuchar/ | Pendiente | |
| C005 | EvaluacionRunner | shared/evaluacion-runner/ | Pendiente | |
| C006 | ComponentesMatematica | shared/componentes-matematica/ | Pendiente | |
| C007 | CampanaNotificaciones | shared/campana-notificaciones/ | Pendiente | |
| C008 | PlantaJardin | shared/planta-jardin/ | Pendiente | |

---

## BACKEND (FastAPI)

### Endpoints - Auth (Apoderado)

| ID | Método | Ruta | Auth | Estado | Riesgos |
|----|--------|------|------|--------|---------|
| B001 | POST | `/auth/registro` | Público | Pendiente | Rate limiting 5/min |
| B002 | POST | `/auth/login` | Público | Pendiente | Rate limiting 10/min |
| B003 | POST | `/auth/login-google` | Público | Pendiente | Rate limiting 10/min |
| B004 | GET | `/auth/yo` | Token | Pendiente | |
| B005 | POST | `/auth/logout` | Token | Pendiente | |
| B006 | POST | `/auth/alumnos` | Token | Pendiente | Rate limiting 10/min |
| B007 | GET | `/auth/alumnos` | Token | Pendiente | |
| B008 | DELETE | `/auth/alumnos/{id}` | Token | Pendiente | |
| B009 | GET | `/auth/planes` | Token | Pendiente | |
| B010 | POST | `/auth/alumnos/{id}/prueba-gratis` | Token | Pendiente | |
| B011 | GET | `/auth/alumnos/{id}/certificado.pdf` | Token | Pendiente | |
| B012 | GET | `/auth/alumnos/{id}/informe-avance.pdf` | Token | Pendiente | |
| B013 | GET | `/auth/alumnos/{id}/suscripcion` | Token | Pendiente | |

### Endpoints - Contenido

| ID | Método | Ruta | Auth | Estado | Riesgos |
|----|--------|------|------|--------|---------|
| B014 | GET | `/contenido/niveles` | Público | Pendiente | |
| B015 | GET | `/contenido/niveles/{id}/asignaturas` | Público | Pendiente | |
| B016 | GET | `/contenido/asignaturas/{id}/objetivos` | Público | Pendiente | |
| B017 | GET | `/contenido/objetivos/{id}` | Público | Pendiente | |
| B018 | GET | `/contenido/objetivos/{id}/guia.pdf` | Público | Pendiente | |

### Endpoints - Evaluaciones

| ID | Método | Ruta | Auth | Estado | Riesgos |
|----|--------|------|------|--------|---------|
| B019 | GET | `/evaluaciones/autoevaluacion/{id}` | Público | Pendiente | |
| B020 | GET | `/evaluaciones/conjuntos/asignatura/{id}` | Token | Pendiente | Verificar perfil propio |
| B021 | GET | `/evaluaciones/conjuntos/nivel/{id}` | Token | Pendiente | Verificar perfil propio |
| B022 | GET | `/evaluaciones/conjuntos/{id}` | Token | Pendiente | Verificar perfil propio |
| B023 | POST | `/evaluaciones/intentos` | Token | Pendiente | Verificar perfil propio |
| B024 | POST | `/evaluaciones/simulacro-parcial/{id}` | Token | Pendiente | Verificar perfil propio |
| B025 | GET | `/evaluaciones/intentos/{id}` | Token | Pendiente | Verificar intento propio |
| B026 | PATCH | `/evaluaciones/intentos/{id}/responder` | Token | Pendiente | Verificar intento propio |
| B027 | POST | `/evaluaciones/intentos/{id}/entregar` | Token | Pendiente | Verificar intento propio |
| B028 | GET | `/evaluaciones/intentos/{id}/detalle` | Token | Pendiente | Verificar intento propio |
| B029 | POST | `/evaluaciones/preguntas/{id}/reportar-error` | Token | Pendiente | Rate limiting 10/min |

### Endpoints - Progreso

| ID | Método | Ruta | Auth | Estado | Riesgos |
|----|--------|------|------|--------|---------|
| B030 | GET | `/progreso/{id}` | Token | Pendiente | Verificar perfil propio |
| B031 | POST | `/progreso/{id}/guias/{oa_id}/revisada` | Token | Pendiente | Verificar perfil propio |
| B032 | GET | `/progreso/{id}/faltantes` | Token | Pendiente | Verificar perfil propio |

### Endpoints - Plan Estudio

| ID | Método | Ruta | Auth | Estado | Riesgos |
|----|--------|------|------|--------|---------|
| B033 | POST | `/plan-estudio/{id}` | Token | Pendiente | Verificar perfil propio |
| B034 | GET | `/plan-estudio/{id}` | Token | Pendiente | Verificar perfil propio |
| B035 | POST | `/plan-estudio/{id}/repaso` | Token | Pendiente | Verificar perfil propio |

### Endpoints - Gamificación

| ID | Método | Ruta | Auth | Estado | Riesgos |
|----|--------|------|------|--------|---------|
| B036 | GET | `/gamificacion/{id}` | Token | Pendiente | Verificar perfil propio |
| B037 | PATCH | `/gamificacion/{id}/avatar` | Token | Pendiente | Verificar perfil propio |

### Endpoints - Onboarding

| ID | Método | Ruta | Auth | Estado | Riesgos |
|----|--------|------|------|--------|---------|
| B038 | GET | `/onboarding/{id}` | Token | Pendiente | Verificar perfil propio |
| B039 | POST | `/onboarding/{id}/pasos/{paso}/completar` | Token | Pendiente | Verificar perfil propio |

### Endpoints - Bienestar

| ID | Método | Ruta | Auth | Estado | Riesgos |
|----|--------|------|------|--------|---------|
| B040 | GET | `/bienestar/{id}/hoy` | Token | Pendiente | Verificar perfil propio |
| B041 | POST | `/bienestar/{id}/hoy` | Token | Pendiente | Verificar perfil propio |

### Endpoints - Admin

| ID | Método | Ruta | Auth | Estado | Riesgos |
|----|--------|------|------|--------|---------|
| B042 | POST | `/admin/auth/login` | Público | Pendiente | Rate limiting 5/min |
| B043 | GET | `/admin/auth/yo` | Admin | Pendiente | |
| B044 | GET | `/admin/planes` | Admin | Pendiente | |
| B045 | POST | `/admin/planes` | Admin | Pendiente | |
| B046 | PATCH | `/admin/planes/{id}` | Admin | Pendiente | |
| B047 | POST | `/admin/planes/{id}/activar` | Admin | Pendiente | |
| B048 | POST | `/admin/planes/{id}/desactivar` | Admin | Pendiente | |
| B049 | GET | `/admin/descuentos` | Admin | Pendiente | |
| B050 | POST | `/admin/descuentos` | Admin | Pendiente | |
| B051 | POST | `/admin/descuentos/{id}/desactivar` | Admin | Pendiente | |
| B052 | GET | `/admin/alumnos/buscar` | Admin | Pendiente | |
| B053 | POST | `/admin/alumnos/{id}/cortesia` | Admin | Pendiente | |
| B054 | GET | `/admin/metricas` | Admin | Pendiente | |
| B055 | GET | `/admin/profesores/pendientes` | Admin | Pendiente | |
| B056 | POST | `/admin/profesores/{id}/aprobar` | Admin | Pendiente | |
| B057 | POST | `/admin/profesores/{id}/rechazar` | Admin | Pendiente | |
| B058 | PATCH | `/admin/evaluaciones/conjuntos/{id}/programar-fecha` | Admin | Pendiente | |

### Endpoints - Profesor

| ID | Método | Ruta | Auth | Estado | Riesgos |
|----|--------|------|------|--------|---------|
| B059 | POST | `/profesor/auth/registro` | Público | Pendiente | Rate limiting 5/min |
| B060 | POST | `/profesor/auth/login` | Público | Pendiente | Rate limiting 10/min |
| B061 | GET | `/profesor/auth/yo` | Profesor | Pendiente | |
| B062 | POST | `/profesor/cursos` | Profesor | Pendiente | |
| B063 | GET | `/profesor/cursos` | Profesor | Pendiente | |
| B064 | GET | `/profesor/alumnos/buscar` | Profesor | Pendiente | |
| B065 | POST | `/profesor/cursos/{id}/alumnos/{alumno_id}` | Profesor | Pendiente | |
| B066 | DELETE | `/profesor/cursos/{id}/alumnos/{alumno_id}` | Profesor | Pendiente | |
| B067 | POST | `/profesor/cursos/{id}/comunicados` | Profesor | Pendiente | Rate limiting 10/min |
| B068 | GET | `/profesor/cursos/{id}/progreso` | Profesor | Pendiente |
| B069 | GET | `/curso-seccion/mi-curso/{id}` | Token | Pendiente | Verificar perfil propio |

---

## MODELO DE DATOS (26 Tablas)

| ID | Tabla | Estado | Riesgos |
|----|-------|--------|---------|
| D001 | Cuenta | Pendiente | |
| D002 | CuentaAdmin | Pendiente | |
| D003 | CuentaProfesor | Pendiente | |
| D004 | Nivel | Pendiente | |
| D005 | Plan | Pendiente | |
| D006 | PerfilAlumno | Pendiente | |
| D007 | CodigoDescuento | Pendiente | |
| D008 | Suscripcion | Pendiente | |
| D009 | Asignatura | Pendiente | |
| D010 | ObjetivoAprendizaje | Pendiente | |
| D011 | Pregunta | Pendiente | |
| D012 | ConjuntoEvaluacion | Pendiente | |
| D013 | IntentoEvaluacion | Pendiente | |
| D014 | ProgresoOA | Pendiente | |
| D015 | PlanDeEstudio | Pendiente | |
| D016 | SesionEstudio | Pendiente | |
| D017 | CursoSeccion | Pendiente | |
| D018 | Comunicado | Pendiente | |
| D019 | PerfilGamificacion | Pendiente | |
| D020 | ProgresoOnboarding | Pendiente | |
| D021 | RegistroAnimo | Pendiente | |
| D022 | AgendaFamiliarConversada | Pendiente | |
| D023 | LibroPlanLector | Pendiente | |
| D024 | UtilEscolar | Pendiente | |
| D025 | Sugerencia | Pendiente | |
| D026 | CalificacionGuia | Pendiente | |
| D027 | ReporteError | Pendiente | |

---

## RESUMEN

**Total Frontend Rutas:** 34 (7 públicas, 23 protegidas)
**Total Frontend Componentes:** 8
**Total Backend Endpoints:** 69 (15 públicos, 54 protegidos)
**Total Tablas BD:** 26

**Estado del Inventario:** En construcción - Se requiere revisión manual de cada ruta/endpoint/componente
