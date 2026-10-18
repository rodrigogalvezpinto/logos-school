---
título: Análisis de consistencia visual del contenido en los 12 cursos
estado: auditoría (2026-10-18)
última actualización: 2026-10-18
---

## Problema Identificado

Aunque el contenido pedagógico está escrito (2.917 preguntas, 408 OA), la forma en que se presenta visualmente **NO es consistente** entre los 12 cursos. Hay problemas graves que afectan especialmente a los niveles más bajos (1°-2° básico) que dependen fuertemente de apoyo visual.

## 🔴 Problemas Críticos Encontrados

### 1. Marcadores de Imagen No Implementados (270 ocurrencias)

**Problema:** Hay 270 marcadores `[Imagen: ...]` en todo el contenido que son solo texto, no imágenes reales.

**Ejemplos reales del contenido:**

1° básico, Lenguaje:
```
[Imagen: una mariposa de colores volando]
Palabra: "mariposa"
```

1° básico, Matemática:
```
[Imagen: un estuche abierto con 8 lápices de colores adentro, alineados]
[Imagen: 14 pelotas de fútbol dibujadas, agrupadas en una fila]
[Imagen: 19 estrellitas dibujadas en fila, para representar el número 19
```

**Impacto:**
- Los alumnos ven texto literal `[Imagen: ...]` en vez de una imagen
- Esto rompe completamente la experiencia de aprendizaje, especialmente en 1°-2° básico donde el apoyo visual es crítico
- El contenido no cumple su propósito pedagógico sin las imágenes

**Estado actual:**
- Backend: Parsea el Markdown y lo sirve como texto
- Frontend: Usa `marked` pipe para renderizar Markdown, pero los marcadores `[Imagen: ...]` no se convierten en imágenes reales
- No hay ningún componente visual que reemplace estos marcadores

### 2. Formato Inconsistente Entre Cursos

**1° básico:**
- Muchos marcadores de imagen `[Imagen: ...]`
- Lenguaje más simple, frases cortas
- Actividades con dibujos (contar objetos, identificar formas)

**4° básico:**
- Casi sin marcadores de imagen en las guías
- Texto más extenso, menos dependencia de imágenes
- Narraciones más complejas

**4° medio (Filosofía):**
- Texto puro, sin imágenes
- Lenguaje académico, párrafos largos
-完全没有 apoyo visual

**Problema:** No hay un sistema visual consistente que se adapte al nivel del alumno. La misma UI debe funcionar para:
- 1° básico (6-7 años, necesita imágenes grandes, texto simple)
- 4° medio (17-18 años, puede trabajar con texto puro)

### 3. Falta de Componentes Visuales de Matemática

**Documentado como pendiente en `21-accesibilidad-lectura-y-contenido-visual.md`:**

- ❌ Recta numérica interactiva
- ❌ Modelo de fracciones
- ❌ Figuras geométricas
- ❌ Tablas y gráficos interactivos
- ✅ Lectura en voz alta (implementada)

**Problema:** Matemática necesita componentes visuales específicos que hoy no existen. Los alumnos solo ven texto y preguntas de alternativas, sin herramientas visuales para:
- Contar en una recta numérica
- Visualizar fracciones
- Identificar formas geométricas
- Leer tablas y pictogramas

### 4. UI de Evaluaciones Limitada

**Estado actual (`evaluacion-runner.ts`):**
- ✅ Preguntas de alternativas (radio buttons)
- ✅ Verdadero/Falso
- ✅ Preguntas abiertas (textarea)
- ❌ Preguntas de tipo "emparejar" (formato no soportado)
- ❌ Componentes visuales interactivos (arrastrar y soltar, seleccionar en imagen, etc.)

**Problema:** El motor de evaluación no soporta preguntas visuales como:
- "Selecciona los objetos que suman 10" (clickear en imagen)
- "Arrastra las figuras a su categoría correcta"
- "Haz clic en el triángulo en este dibujo"

### 5. Responsive No Probado en Contenido Real

**Estado actual:**
- ✅ El layout general (sidebar, topbar) fue corregido para móvil
- ❌ El contenido específico (guías, preguntas con imágenes) NO fue probado en móvil
- ❌ No se sabe cómo se ven los marcadores `[Imagen: ...]` en pantallas pequeñas

**Riesgo:** En móvil, el contenido podría ser ilegible si:
- Las imágenes (cuando existan) son muy grandes
- El texto de las preguntas se rompe en pantallas pequeñas
- Los componentes interactivos no funcionan con touch

## 📊 Desglose por Nivel

| Nivel | Imágenes Placeholder | Dificultad Visual | Necesidad de Componentes Visuales |
|-------|---------------------|-------------------|----------------------------------|
| 1° básico | Alta (muchas) | Crítica | Muy alta (contar, formas, colores) |
| 2° básico | Alta | Crítica | Muy alta |
| 3° básico | Media | Alta | Alta |
| 4° básico | Baja | Media | Media |
| 5°-6° básico | Baja | Media | Media (tablas, gráficos) |
| 7°-8° básico | Baja | Media-Baja | Media |
| 1°-2° medio | Muy baja | Baja | Baja |
| 3°-4° medio | Muy baja | Muy baja | Muy baja |

## 🎯 Solución Propuesta

### Fase 1: Sistema de Imágenes Consistente

1. **Crear componente de imagen responsivo**
   - Componente Angular `<app-imagen-educativa>` que:
     - Soporte marcadores `[Imagen: ...]` en Markdown
     - Sea responsivo (se adapte a móvil)
     - Tenga fallback cuando no haya imagen real
     - Permita carga diferida (lazy loading)

2. **Definir estrategia de imágenes**
   - Opción A: Generar ilustraciones con IA (DALL-E, Midjourney) para cada marcador
   - Opción B: Usar iconos SVG/emoji simples para 1°-2° básico
   - Opción C: Usar banco de imágenes libres (Unsplash, Pixabay) con filtros por tema
   - Opción D: No usar imágenes, eliminar los marcadores y reescribir el contenido

3. **Priorizar por nivel**
   - Prioridad #1: 1°-2° básico (crítico para el aprendizaje)
   - Prioridad #2: 3°-4° básico
   - Prioridad #3: 5°-8° básico (solo donde sea necesario, ej. Matemática)
   - Prioridad #4: Media (opcional, texto puro es aceptable)

### Fase 2: Componentes Visuales de Matemática

1. **Crear componentes específicos:**
   - `<app-recta-numerica>` - recta numérica interactiva
   - `<app-modelo-fracciones>` - visualización de fracciones
   - `<app-figuras-geometricas>` - dibujos de formas
   - `<app-tabla-interactiva>` - tablas y pictogramas

2. **Integrar al parser de contenido**
   - El parser debe reconocer cuando una pregunta necesita un componente visual
   - Renderizar el componente apropiado en lugar de texto plano

### Fase 3: Mejorar Motor de Evaluaciones

1. **Agregar tipos de pregunta visuales:**
   - Preguntas de selección en imagen (clickear elementos)
   - Preguntas de arrastrar y soltar
   - Preguntas de "emparejar" (arrastrar elementos a categorías)

2. **Integrar con componentes visuales de Matemática**
   - Permitir que una pregunta use `<app-recta-numerica>` como parte del enunciado
   - El alumno interactúa con el componente para responder

### Fase 4: Responsive del Contenido

1. **Probar contenido real en móvil**
   - Usar Playwright con viewport móvil
   - Probar guías con imágenes
   - Probar preguntas con componentes visuales

2. **Ajustar estilos según tamaño de pantalla**
   - Imágenes responsivas
   - Texto legible en móvil
   - Componentes táctiles funcionales

## 📝 Decisiones Pendientes

1. **¿Qué estrategia usar para las imágenes?**
   - ¿Generar con IA? (costo, tiempo, calidad variable)
   - ¿Usar banco de imágenes libres? (copyright, búsqueda manual)
   - ¿Usar SVG/emoji simple? (limitado pero consistente)
   - ¿Eliminar marcadores y reescribir? (perder apoyo visual)

2. **¿Qué componentes visuales priorizar?**
   - ¿Recta numérica primero?
   - ¿Modelo de fracciones?
   - ¿Figuras geométricas?
   - ¿Todos a la vez?

3. **¿Cómo integrar con el parser actual?**
   - ¿Extender el parser para reconocer nuevos formatos?
   - ¿Crear un nuevo parser para contenido visual?
   - ¿Usar un formato intermedio (JSON) en vez de Markdown?

## 🚀 Siguiente Paso

Antes de construir, necesitamos:
1. Decidir la estrategia de imágenes (A, B, C o D)
2. Definir qué componentes visuales priorizar
3. Crear un prototipo visual para probar con 1° básico
4. Validar con el usuario si el enfoque es correcto

Sin esto, el contenido虽然有 escrito, pero no es pedagógicamente efectivo porque no se presenta de forma visual adecuada para el nivel de cada alumno.
