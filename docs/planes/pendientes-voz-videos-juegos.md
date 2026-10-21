# Pendientes tecnológicos: voz natural, videos y juegos educativos

**Fecha de registro:** 21 de octubre de 2026  
**Estado:** Pendiente de prueba técnica y decisión; no implementado en la aplicación.  
**Regla de seguridad:** no modificar producción ni añadir dependencias/costos recurrentes sin una prueba y una decisión explícita.

## Objetivo
Mejorar la accesibilidad y el atractivo de Logos School mediante lectura natural de enunciados, videos educativos breves y juegos interactivos alineados con los Objetivos de Aprendizaje (OA) de Chile.

## 1. Voz natural (prioridad inicial)
**Candidatos para comparar:** Microsoft Azure AI Speech y Google Cloud Text-to-Speech. No declarar ganador antes de probarlos con ejemplos reales en español chileno.

- Azure documenta un nivel gratuito F0 de 500.000 caracteres mensuales para voces neuronales de texto a voz.
- Google documenta un millón de caracteres mensuales sin costo para Chirp 3 HD; otros modelos tienen límites y precios distintos.
- Las cuotas, regiones, modelos disponibles, necesidad de habilitar facturación y precios pueden cambiar. Verificar la página de precios y las condiciones de la cuenta justo antes de activar el servicio.
- No asumir que la voz reproduce acento chileno auténtico solo porque admita español.

**Prueba propuesta:** usar al menos diez enunciados reales, incluyendo divisiones, fracciones, decimales, ecuaciones, signos negativos, potencias e instrucciones largas. Comparar naturalidad, pronunciación matemática, latencia, formatos de audio, accesibilidad, facilidad de integración, costos y límites.

**Implementación futura:** generar audio en backend, proteger las credenciales, limitar el uso y considerar caché de audio para enunciados idénticos. No enviar datos personales del estudiante si solo hace falta el enunciado. Añadir métricas y alertas de gasto. Revisar accesibilidad, controles de pausa/repetición y comportamiento ante errores.

## 2. Videos educativos
**Herramientas candidatas:** Canva, Clipchamp y CapCut para preparar un piloto pequeño. Verificar planes actuales, marca de agua, exportación, derechos comerciales y condiciones de uso antes de decidir.

**Piloto propuesto:** producir 3–5 videos de 1–3 minutos basados en contenidos ya revisados, empezando por un OA de alta prioridad. Evaluar comprensión y uso antes de escalar. No producir videos masivos sin validar el formato.

## 3. Actividades y juegos
### H5P
H5P es una tecnología abierta para crear cuestionarios, actividades de arrastrar y soltar, memoria y videos interactivos. Puede servir para validar actividades rápidamente. Antes de integrarlo, revisar las licencias de la biblioteca y de cada contenido, el método de alojamiento, seguridad, accesibilidad, compatibilidad móvil y cómo recuperar resultados. Un iframe por sí solo no garantiza persistencia en Logos School.

### Phaser
Phaser es un framework HTML5 de código abierto con licencia MIT, apropiado para prototipos propios en navegador. Es candidato para integrar juegos como componentes separados en el frontend Angular, sujeto a un prototipo de rendimiento, accesibilidad y mantenimiento.

**Primer juego sugerido:** misión de multiplicación/división con intentos, pistas graduadas y avance asociado al OA. Guardar resultados en el backend solo después de diseñar y probar correctamente la persistencia, autorización y privacidad.

## 4. Orden recomendado
1. Comparar Azure y Google con una prueba de voz reproducible.
2. Implementar un piloto limitado y medir uso/costo, solo después de elegir proveedor.
3. Crear 3–5 videos con herramientas gratuitas y validar su utilidad.
4. Probar una actividad H5P sin depender inicialmente de resultados externos para el expediente académico.
5. Construir un juego pequeño con Phaser y conectarlo a los OA/progreso cuando exista una solución fiable de persistencia.
6. Revaluar costos, adopción, resultados de aprendizaje y mantenimiento antes de ampliar.

## 5. Criterios de decisión
- Calidad y claridad de la voz en ejercicios matemáticos.
- Costo mensual estimado con uso real y controles para evitar sobrecostos.
- Experiencia en móvil, accesibilidad y facilidad de uso infantil.
- Licencia y derecho de uso comercial de código, recursos, voces y contenidos.
- Integración segura con Angular/FastAPI, autenticación y seguimiento por alumno.
- Evidencia de mejora educativa, no solo métricas de visitas o tiempo de uso.

## Fuentes oficiales iniciales
- [Azure AI Speech: precios](https://azure.microsoft.com/en-us/pricing/details/speech/)
- [Google Cloud Text-to-Speech: precios](https://cloud.google.com/text-to-speech/pricing)
- [H5P: sitio oficial y tecnología abierta](https://h5p.org/)
- [H5P: licencias](https://h5p.org/licensing)
- [Phaser: términos y licencia del framework](https://www.phaser.io/community/terms-of-use)

## Limitaciones de este estudio
La documentación oficial permite confirmar que estas tecnologías existen, sus modelos de licencia y los límites/precios publicados consultados. No permite asegurar todavía cuál será la mejor voz para los estudiantes de Chile, el costo real de producción, la compatibilidad exacta con la arquitectura actual ni el efecto pedagógico. Esas conclusiones requieren una prueba técnica en Logos School y validación con usuarios. Este documento registra una hoja de ruta; no afirma que las funciones estén implementadas ni probadas.
