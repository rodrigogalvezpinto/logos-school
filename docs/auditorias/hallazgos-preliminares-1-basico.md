# Hallazgos preliminares — 1° básico, primera lectura de cuatro asignaturas

**Rama:** `qa/fase-2-matriz-trazabilidad`  
**Base documental:** `contenido/01-basico/lenguaje-y-comunicacion.md`, `matematica.md`, `ciencias-naturales.md`, `historia-geografia-y-cs-sociales.md`.  
**Método:** inspección estática de fragmentos de los cuatro archivos principales. No se ejecutó la aplicación, no se verificaron todavía los OA contra el documento oficial completo y no se revisó cada pregunta de los archivos. Por tanto, estos son hallazgos iniciales, no el informe final del curso.

## Resumen

Se detectó al menos una afirmación matemática que puede enseñar una regla falsa y una simplificación lingüística que conviene corregir. También hay formulaciones en Ciencias Naturales e Historia que requieren precisión didáctica e inclusión. Los niveles de severidad son provisionales y deberán confirmarse en la revisión completa.

## Registro inicial

| ID | Archivo / ubicación | Evidencia observada | Evaluación preliminar | Severidad provisional | Acción propuesta |
|---|---|---|---|---|---|
| LS-1B-MAT-001 | `contenido/01-basico/matematica.md`, OA 3, retroalimentación de “diecinueve” | “Recuerda que los números del 11 al 19 casi siempre empiezan sonando como ‘dieci-’.” | La generalización es engañosa: 11–15 se nombran once, doce, trece, catorce y quince; dieciséis a diecinueve sí contienen la secuencia “dieci-”. Un niño podría aprender una regla verbal falsa. | **P1 — Alto**, sujeto a confirmación en contexto | Cambiar por una explicación explícita que distinga 11–15 de 16–19 y comprobar el resto de las explicaciones de numeración verbal. Añadir prueba de revisión del texto si existe validador de contenido. |
| LS-1B-LEN-001 | `contenido/01-basico/lenguaje-y-comunicacion.md`, OA 3 | “Cada sílaba, a su vez, está hecha de sonidos aún más pequeños, llamados fonemas (el sonido de cada letra).” | Un fonema es una unidad sonora distintiva, no literalmente “el sonido de cada letra”. La relación entre letras/grafemas y fonemas no es siempre uno a uno. La frase puede confundir conciencia fonémica con conocimiento de letras. | **P1 — Alto**, sujeto a revisión de especialista de alfabetización | Reescribir para distinguir sonido (fonema) y representación escrita (letra/grafema), con ejemplos orales apropiados a 1° básico y sin introducir terminología excesiva. Revisar todas las definiciones de fonema, grafema, letra y dígrafo del documento. |
| LS-1B-CN-001 | `contenido/01-basico/ciencias-naturales.md`, OA 1 | “Además, todo ser vivo necesita agua, aire y alimento para vivir.” | Es una simplificación amplia. En plantas, “alimento” puede inducir la idea de que obtienen comida del mismo modo que los animales; conviene diferenciar agua, gases, luz y nutrientes con lenguaje de primer ciclo, sin enseñar que las plantas “comen” como los animales. | **P2 — Medio**, requiere revisión disciplinar | Reformular con precisión etaria: los seres vivos tienen necesidades, pero plantas y animales no obtienen energía/nutrientes de la misma manera. Comprobar que la explicación no contradiga el OA y el programa oficial. |
| LS-1B-HIS-001 | `contenido/01-basico/historia-geografia-y-cs-sociales.md`, introducción | “Estas costumbres nos hacen sentir orgullosos y unidos como chilenos.” | Presenta la identidad cultural como experiencia uniforme y presupone que todo niño se siente de la misma manera. La asignatura debe permitir diversidad de pertenencias, culturas familiares y experiencias locales, sin imponer una emoción nacional. | **P2 — Medio**, revisión de inclusión y enfoque curricular | Usar una formulación descriptiva e inclusiva: las tradiciones son expresiones culturales diversas que algunas comunidades comparten y que pueden conocerse y respetarse. Revisar ejemplos para representación territorial y cultural amplia. |

## Qué no se concluye todavía

- No se afirma que todos los contenidos de 1° básico sean defectuosos.
- No se certifica todavía que los OA citados estén completos o correctamente mapeados contra la fuente oficial vigente.
- No se han inspeccionado de forma exhaustiva las preguntas, sus claves ni las pruebas de unidad de estas asignaturas.
- No se ejecutaron tests automáticos ni se validó el renderizado de los recursos visuales.
- Los hallazgos de Ciencias e Historia necesitan revisión disciplinar y curricular antes de aceptar la corrección definitiva.

## Próxima revisión

1. Revisar íntegramente los cuatro archivos principales y todos sus bancos de preguntas, soluciones y retroalimentación.
2. Examinar las 12 pruebas de unidad y los 2 exámenes integrados de 1° básico según el inventario de archivos.
3. Contrastar los OA y las definiciones con los documentos oficiales de la UCE/Mineduc versionados en el repositorio y, cuando haga falta, con la fuente oficial vigente.
4. Comprobar si los mismos patrones aparecen en 2°–4° básico antes de proponer cambios transversales.
5. Preparar correcciones con diffs pequeños y pruebas; no cambiar contenido en masa sin revisión.
