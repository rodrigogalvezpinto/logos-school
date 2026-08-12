---
título: Conocimiento experto — Proceso de Exámenes Libres (Validación de Estudios, menores de edad)
estado: vigente — base de conocimiento para responder dudas de apoderados; fuente de verdad
  para el futuro chatbot de la aplicación
última actualización: 2026-08-11
fuente: ayudamineduc.cl, epja.mineduc.cl (Mineduc, consultado 2026-08-11)
---

Este documento reúne todo lo que hay que saber del **trámite administrativo** de los
Exámenes Libres de Validación de Estudios para menores de edad en Chile — separado del
contenido académico (que vive en `contenido/`). Es la base de conocimiento pensada para
responder preguntas de apoderados, y sirve de fuente para el futuro chatbot de la
aplicación (ver agente `.claude/agents/experto-examenes-libres.md`).

## ⚠️ Corrección importante a un supuesto inicial del proyecto

No es "un solo examen al año en octubre". Hay **3 periodos de examinación al año** (fechas
2026, se repiten con variaciones menores cada año):

| Periodo | Quién puede rendir | Inscripción | Examen | Resultados |
|---|---|---|---|---|
| **1** | Todos los cursos + NEE | 6-29 abril | 8-19 junio | 27 julio |
| **2** | Solo 4° medio + NEE | 12 mayo-17 julio | 21 sept.-2 oct. | 27 octubre |
| **3** | Todos excepto 4° medio + NEE | 12 mayo-17 julio | 19-30 octubre | 20 noviembre |

- Un alumno de 4° medio solo puede inscribirse en el Periodo 1 o el Periodo 2 (nunca el 3).
- El resto de los cursos (1° básico a 3° medio) puede rendir en el Periodo 1 o el 3.
- **Octubre sí es el mes más común** para la mayoría de los cursos (Periodo 3), pero no es
  la única fecha ni aplica igual para todos — esto es clave para no dar información
  incorrecta a un apoderado.

## Quién puede inscribirse

Menores de 18 años que:
- No hicieron estudios regulares o los interrumpieron.
- Estudiaron en un establecimiento no reconocido oficialmente (ej. homeschooling informal).
- Son extranjeros sin convenio de convalidación, o chilenos que volvieron del extranjero.
- Están en educación especial y quieren completar solo educación media.

**Restricción:** no puede inscribirse si estuvo matriculado en un colegio oficial durante
ese mismo año, salvo por motivos de salud acreditados con certificado médico.

## Cómo se inscribe

- **Quién inscribe:** el padre, madre o tutor legal — no el propio menor, y tampoco
  instituciones de homeschooling directamente.
- **Documentos:** ficha de inscripción oficial, certificado de nacimiento (máx. 3 meses de
  antigüedad), cédula de identidad vigente del apoderado. Extranjeros sin RUN necesitan IPE
  (Identificador Provisorio Escolar) previo y acta de nacimiento legalizada.
- **Canales:** formulario web oficial, o presencial en oficinas de Ayuda Mineduc.
- **Plazo de comprobante:** 15 días hábiles (web) o 5 días hábiles (presencial).
- **Costo: el trámite es completamente gratuito.**

## La "entidad examinadora"

**No la elige la familia.** Es el establecimiento educacional donde se rinde el examen,
**asignado automáticamente por Mineduc** según disponibilidad de cupos e infraestructura de
la región. El comprobante de autorización indica cuál fue asignado. **10 días antes del
examen hay que contactar a ese establecimiento por correo** para confirmar fecha y hora
exactas — este paso es fácil de olvidar y vale la pena que la app lo recuerde.

## El día del examen

- Llevar: cédula de identidad vigente (o certificado de nacimiento) **y** el comprobante de
  autorización — sin ambos, no se puede rendir el examen.
- Materiales permitidos: lápiz, goma, **calculadora desde 5° básico en adelante**,
  diccionario de inglés (desde que Inglés se evalúa, 5° básico en adelante).
- Sin celulares, sin libros, sin acompañamiento de apoderados en la sala.
- 1°-4° básico: una sola prueba integrada (20 preguntas, 90 min). 5° básico en adelante:
  pruebas separadas por asignatura (25 preguntas c/u, 90 min, máx. 2 pruebas por día).

## Si repruebas

**No hay segunda oportunidad dentro del mismo periodo.** Solo se puede volver a inscribir en
otro periodo disponible, si hay cupos. Esto tiene una implicancia directa para el diseño
pedagógico de la app: como no hay margen de error dentro de un mismo periodo, el material de
estudio y las autoevaluaciones deben apuntar a que el alumno llegue con seguridad real, no
solo "cobertura curricular" — ver la auditoría pedagógica en curso.

## Recorrección de la prueba

Posible solo si: el resultado fue reprobación **y** la calificación en esa asignatura quedó
entre 3.0 y 3.9. Se solicita directamente al establecimiento examinador por correo, dentro
de **3 días hábiles** desde la publicación de resultados (plazo que no se puede extender).

## Certificado de estudios

Una vez aprobado, el certificado está disponible en `www.certificados.mineduc.cl` para
menores con RUT chileno. Los que tienen IPE deben solicitarlo presencialmente en oficinas de
Ayuda Mineduc.

## Contacto oficial

Call center Mineduc: 600 600 2626 o +56 2 2353 6750 (lunes a viernes, 8:00-18:00 hrs).

## Dónde descargar más material oficial

- Temarios oficiales para menores de edad (los mismos 12 que ya tenemos en `Temarios/`):
  `epja.mineduc.cl/validacion-de-estudios/examenes-libres-menores-de-18-anos/
  cuales-son-los-temarios-que-se-utilizaran-en-la-examinacion/`
- Preguntas de ejemplo con pauta de corrección oficial: existen, pero son del programa de
  **adultos** (EPJA, decretos 257/2009 y DS 10, agrupado en "Niveles" en vez de por curso) —
  no hay un repositorio de preguntas de ejemplo específico para menores de edad al momento de
  esta investigación. Ver hallazgo completo en `planificacion/05-tipos-de-contenido.md`.

## Pendiente de investigar más adelante (no bloqueante)

- Recomendaciones oficiales de estudio específicas de Mineduc (más allá de "estudiar todo el
  temario aunque el examen tome solo una selección").
- Si existen preparadores/academias reconocidas oficialmente, o si el Mineduc desaconseja
  alguna práctica.
- Detalle de qué pasa con menores en modalidad de educación especial (NEE) — mencionados en
  los periodos pero no investigado en profundidad.
