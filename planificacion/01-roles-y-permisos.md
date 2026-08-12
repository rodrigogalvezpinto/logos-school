---
título: Roles y permisos
estado: decisiones cerradas (2026-08-12) — ver `10-privacidad-y-datos-de-menores.md` para
  el modelo de registro y verificación
última actualización: 2026-08-12
---

**Actualización 2026-08-12:** el modelo de registro se resolvió como "Apoderado-primero",
simple y sin verificación de identidad (ver `10-privacidad-y-datos-de-menores.md`, basado en
cómo funciona realmente Wited, plataforma chilena equivalente): el Apoderado —o cualquier
adulto que matricule, no necesariamente el padre/madre— crea la cuenta raíz y, dentro de
ella, agrega Perfiles de Alumno con sus datos (nombre, apellidos, fecha de nacimiento, RUT).
El alumno nunca se registra ni se vincula de forma independiente. El rol Administrador queda
confirmado como necesario, operando en el MVP como backoffice interno del equipo del
proyecto (no un rol autoservicio dentro de la app todavía).

# Roles

## 1. Alumno

El usuario principal de la plataforma. Un niño, niña o adolescente preparándose para un
examen libre.

**Al registrarse:**
- Elige o se le asigna un **Nivel** (ej. "6° básico") — esto es autoservicio, nadie se lo
  asigna. El nivel determina qué asignaturas y material ve.
- *Opcionalmente* puede quedar vinculado a un **Curso/Sección** (ej. "6° básico A"), pero
  **solo si un profesor lo agrega** — el alumno no puede unirse a un curso por su cuenta.

**Puede:**
- Ver y estudiar todo el material de su Nivel (contenido, ejercicios, autoevaluaciones).
- Rendir autoevaluaciones/simulacros basados en los OA del temario oficial.
- Ver su propio progreso e historial de resultados.
- Si pertenece a un Curso/Sección, ver comunicación o material adicional que el profesor
  publique para ese curso (en fase 2, cuando el rol Profesor esté activo).
- Estar vinculado a uno o más Apoderados.

**No puede:**
- Cambiar su propio Nivel libremente sin restricción alguna una vez inscrito en un curso
  formal (a definir: ¿puede cambiar de nivel en cualquier momento, o requiere confirmación
  del apoderado/profesor? — pendiente).
- Autoagregarse a un Curso/Sección.

## 2. Apoderado (madre, padre o tutor legal)

Muy similar al Alumno en cuanto a lo que *ve*, pero con una capa adicional de supervisión.
Definido explícitamente por el usuario como "similar al alumno, pero con otras cosas
adicionales".

**Vinculación (resuelto 2026-08-12, ver `10-privacidad-y-datos-de-menores.md`):**
- El Apoderado crea la cuenta raíz (su propio correo) y, dentro de ella, crea uno o más
  **Perfiles de Alumno** (hijos/pupilos) — el alumno nace dentro de la cuenta del apoderado,
  nunca al revés. No existe un flujo de "vinculación posterior" entre un alumno preexistente
  y un apoderado externo, lo que elimina el riesgo de que un desconocido se vincule a un
  menor.
- El menor accede a su propio perfil (dentro de la cuenta del apoderado) mediante un PIN
  simple — no necesita correo propio, relevante sobre todo en básica inicial.

**Puede (propuesta a confirmar):**
- Ver el progreso, resultados y actividad de estudio de cada uno de sus Alumnos vinculados.
- Ver en qué Nivel y (si aplica) en qué Curso/Sección está cada Alumno.
- Recibir notificaciones/resúmenes sobre el avance del Alumno.
- Comunicarse con el Profesor del Curso/Sección del Alumno (fase 2).
- Gestionar datos administrativos del Alumno (fase posterior: inscripción a la entidad
  examinadora real, fechas de examen, etc. — fuera del alcance del MVP).

**No puede:**
- Estudiar en nombre del alumno / que sus respuestas cuenten como progreso del alumno
  (si el apoderado usa contenido de estudio, es solo lectura/exploración, no se mezcla con
  el registro de progreso del hijo).
- Modificar el Nivel o Curso/Sección del Alumno directamente (eso lo hace el propio alumno
  para el Nivel, y el Profesor para el Curso/Sección) — a confirmar si el apoderado debiera
  tener injerencia aquí dado que muchos alumnos son menores de edad.

## 3. Profesor (rol activo desde fase 2 del roadmap)

Decisión tomada: el MVP parte en **autoestudio**, sin profesores activos. El rol se diseña
igual desde ahora para no tener que rehacer el modelo de datos más adelante.

**Puede:**
- Crear uno o más **Cursos/Secciones** (ej. "6° básico A", "6° básico B") de forma arbitraria
  — el sistema debe permitir crear cursos libremente, no depende de una entidad examinadora
  externa en el MVP.
- Agregar o quitar Alumnos de sus Cursos/Secciones (el alumno no puede autoagregarse, según
  quedó definido).
- Un Profesor puede tener **uno o varios Cursos/Secciones** a la vez, potencialmente en
  distintos Niveles (ej. un profesor de Lenguaje podría tener secciones en 7° y 8° básico).
- Ver el progreso y resultados de los Alumnos de sus Cursos/Secciones.
- Publicar material, comunicados o evaluaciones adicionales dirigidos a su Curso/Sección.
- Corregir o dar seguimiento cualitativo (más allá de lo que la autoevaluación automática
  ya corrige).

**No puede:**
- Ver ni gestionar Alumnos que no pertenezcan a ninguno de sus Cursos/Secciones (los
  alumnos en modo autoestudio puro son invisibles para profesores que no los hayan agregado).
- Modificar el temario oficial/base de contenido curricular (eso lo gestiona el
  Administrador o es fijo, ligado a los documentos UCE).

## 4. Administrador / Coordinador (confirmado 2026-08-12)

Necesario para que el sistema funcione: alguien debe poder verificar cuentas de Profesor
(para evitar que cualquiera se declare "profesor" y empiece a gestionar menores de edad),
gestionar el catálogo de Niveles/Asignaturas/contenido base, y moderar la plataforma.

**Puede:**
- Verificar y aprobar cuentas de Profesor (revisión manual, ver
  `10-privacidad-y-datos-de-menores.md`).
- Gestionar el contenido curricular base (Niveles, Asignaturas, OA, banco de preguntas)
  que proviene de los temarios UCE.
- Ver métricas generales de uso (sin necesariamente ver el detalle de cada alumno, por
  privacidad).
- Resolver disputas o reportes (ej. contenido incorrecto reportado por un apoderado).

**Confirmado:** en el MVP y en la Etapa 2, el Administrador es **el propio equipo del
proyecto operando como backoffice** (no un rol autoservicio con registro público dentro de
la app). Puede evolucionar a un rol con cuenta propia dentro del sistema más adelante, si el
volumen de Profesores a verificar lo justifica.

# Seguridad/privacidad de menores — resuelto

Ver `10-privacidad-y-datos-de-menores.md` para el desarrollo completo de estos puntos
(marco legal Ley 21.719, modelo de registro Apoderado-primero, qué datos se almacenan,
verificación de Profesores, requisitos de producto no negociables). Resumen:

1. **Vínculo Apoderado-Alumno**: no requiere verificación posterior porque el alumno nace
   dentro de la cuenta del apoderado (modelo Apoderado-primero).
2. **Identidad del Profesor**: revisión manual por el Administrador antes de aprobar la
   cuenta (Etapa 2, no bloquea el MVP).
3. **Datos almacenados**: mínimo indispensable (nombre/apodo, fecha de nacimiento, nivel,
   progreso) — explícitamente sin RUT, domicilio, ni datos de salud/NEE en el MVP.
4. **Consentimiento**: explícito y reforzado del Apoderado al crear cada Perfil de Alumno,
   nunca implícito.
