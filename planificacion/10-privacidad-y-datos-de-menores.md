---
título: Registro de usuarios y datos de menores
estado: simplificado (2026-08-12) — corrige el enfoque sobreingenierizado de la versión anterior
última actualización: 2026-08-12
---

## Corrección de enfoque (2026-08-12)

La primera versión de este documento diseñó un flujo de registro con verificación reforzada
tipo "consentimiento parental verificable", basado en leer la Ley 21.719 de forma estricta.
El usuario corrigió esto con criterio directo, basado en experiencia real como apoderado:
**Logos no es un colegio legalizado ante Mineduc, es una plataforma de ayuda de estudio**
(como las que sus propios hijos han usado — Lumbreras, y actualmente el sistema del colegio
LUZ). Ese tipo de plataforma no exige aparataje de verificación de identidad para
registrarse — el registro es simple, como el de cualquier servicio online con planes pagos.

Se investigó **Wited** (wited.com/cl), plataforma chilena real de apoyo escolar y "colegio
online" con miles de alumnos, como referencia directa de cómo resuelven esto en la práctica.
Este documento reemplaza el enfoque anterior por ese modelo, mucho más simple.

## Modelo de registro (basado en Wited, confirmado por investigación 2026-08-12)

1. El **Apoderado** (o quien matricule — no necesariamente un padre/madre; puede ser un tío,
   tutor, o cualquier adulto responsable, igual que en Wited) crea la cuenta con su correo y
   contraseña.
2. Durante o después del registro, indica **cuántos alumnos** va a inscribir (1, 2, 3...).
3. Por cada alumno completa un formulario simple con:
   - Nombre y apellidos.
   - Fecha de nacimiento (de la que se deriva la edad).
   - RUT.
   - Curso/Nivel al que accede.
4. Con eso, el alumno ya tiene su perfil dentro de la cuenta del apoderado — sin invitación,
   sin verificación de identidad adicional, sin flujo de aprobación. Igual que Wited: nombre,
   fecha de nacimiento y RUT del alumno se usan directamente como sus credenciales de acceso
   (más adelante, en diseño de detalle, se define si el alumno usa esos datos para entrar o
   si se genera un PIN/usuario más simple para los cursos de básica inicial — es un detalle
   de UX, no bloquea el modelo de datos).
5. No hay un paso de "aprobación" ni de un tercero (profesor, Mineduc) validando el vínculo
   apoderado-alumno. El apoderado es responsable de los datos que ingresa, igual que en
   cualquier plataforma comercial de este tipo.

**Por qué esto es suficiente:** Logos no emite certificados oficiales ni reemplaza el
trámite real de Mineduc (que sigue haciéndolo el apoderado directamente con el Estado, ver
`07-experto-examenes-libres.md`) — es una herramienta de apoyo de estudio, pagada o
gratuita según el plan. El nivel de fricción en el registro debe ser el de un producto de
consumo (como Wited), no el de un trámite gubernamental.

## Datos que se solicitan

**Del alumno** (igual que Wited): nombre y apellidos, fecha de nacimiento, RUT, curso/nivel.

**Del apoderado**: nombre, correo, contraseña, y **opcionalmente** comuna/región o país, si
se quiere pedir — utilidad declarada: estadística agregada de qué zonas usan más el
servicio (no seguimiento individual, no publicidad dirigida). Al ser opcional y con fines
agregados, no hace falta un flujo de consentimiento especial para este campo — se pide con
un texto simple tipo "para saber desde dónde nos visitan" y el usuario decide si lo llena.

**No se pide** (salvo que un plan específico lo requiera más adelante, ej. certificados o
pagos con boleta): domicilio exacto, datos de salud, NEE, u otros datos sensibles. Si en
algún momento se necesita facturación formal (boleta/factura), ahí sí se pedirán los datos
tributarios que la ley chilena exija para emitir el documento — eso es un requisito de pago,
no de registro.

## Nota legal breve (sin sobre-construir en base a esto)

Chile tiene la Ley 21.719 de protección de datos personales (vigencia plena desde
diciembre de 2026), que en general pide tratar los datos de menores con cuidado razonable:
no usarlos con fines publicitarios, guardarlos con seguridad básica (contraseñas hasheadas,
acceso restringido), y tener una política de privacidad simple que diga qué se guarda y
para qué. Eso es perfectamente compatible con el modelo de registro simple de arriba — no
exige verificación de identidad ni consentimiento notarial para operar una plataforma de
estudio como esta. Si más adelante el proyecto crece mucho o cambia de naturaleza (ej. pasa
a ser colegio reconocido), vale la pena revisar esto de nuevo con un abogado, pero no es
necesario para lanzar ni para operar en esta etapa.

## Verificación de identidad del Profesor (rol de Etapa 2, no bloquea el MVP)

Se mantiene simple, igual que el resto: el Profesor se registra con sus datos, y el
Administrador (backoffice del equipo) puede revisar manualmente si algo se ve irregular —
sin exigir documentación formal por defecto. Se ajusta si en la práctica surgen abusos.
