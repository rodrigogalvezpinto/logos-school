# 05 — Especificación Técnica de Correcciones (Sin Implementar)
**Fecha:** 21 de octubre de 2026  
**Propósito:** Especificación precisa y accionable de cambios técnicos y editoriales para ser ejecutados en la fase de implementación.

---

## 1. Módulo Evaluaciones: `evaluacion-runner.ts`

### 1.1. Ayuda Bajo Demanda y Eliminación de Auto-spoil (UX-001 y MAT-UI-001)

#### Comportamiento Actual:
En modo `autoevaluacion`, tan pronto como el alumno responde, el bloque `.feedback` aparece automáticamente y evalúa las preguntas abiertas mediante igualdad literal de cadenas (`esCorrectaEnAutoevaluacion()`):
```html
@if (modo === 'autoevaluacion' && respuestas()[preguntaActual.id]) {
  <div class="feedback">
    @if (esCorrectaEnAutoevaluacion(preguntaActual)) {
      ✓ ¡Correcto! {{ preguntaActual.retroalimentacion }}
    } @else {
      <strong>Respuesta esperada: {{ preguntaActual.respuesta_correcta }}.</strong>
      {{ preguntaActual.retroalimentacion }}
    }
  </div>
}
```

#### Comportamiento Especificado:
1. Crear un signal de preguntas cuya ayuda ha sido solicitada:
   ```typescript
   ayudasReveladas = signal<Set<number>>(new Set());
   ```
2. Agregar método para solicitar comprobación o ayuda:
   ```typescript
   solicitarAyuda(preguntaId: number) {
     this.ayudasReveladas.update((set) => new Set(set).add(preguntaId));
   }
   ```
3. En el template, mostrar el botón de ayuda pedagógica cuando el alumno ha interactuado con la pregunta pero aún no solicita ver la retroalimentación:
   ```html
   @if (modo === 'autoevaluacion') {
     @if (!ayudasReveladas().has(preguntaActual.id)) {
       <button
         type="button"
         class="btn-ayuda-practica"
         [disabled]="!respuestas()[preguntaActual.id]"
         (click)="solicitarAyuda(preguntaActual.id)"
       >
         💡 Comprobar respuesta / Ver explicación
       </button>
     } @else {
       <div class="feedback feedback--revelado">
         @if (preguntaActual.tipo === 'alternativas' || preguntaActual.tipo === 'verdadero_falso') {
           @if (esCorrectaEnAutoevaluacion(preguntaActual)) {
             <p class="feedback__exito">✓ ¡Correcto! {{ preguntaActual.retroalimentacion }}</p>
           } @else {
             <p class="feedback__atencion">
               <strong>Respuesta correcta: {{ preguntaActual.respuesta_correcta }}.</strong>
               {{ preguntaActual.retroalimentacion }}
             </p>
           }
         } @else {
           <!-- Pregunta abierta / desarrollo: No juzga como incorrecta; ofrece solución orientativa -->
           <div class="feedback__orientativo">
             <p class="feedback__titulo">Pauta de autoevaluación:</p>
             <p><strong>Idea clave esperada:</strong> {{ preguntaActual.respuesta_correcta }}</p>
             <p class="feedback__retro">{{ preguntaActual.retroalimentacion }}</p>
           </div>
         }
       </div>
     }
   }
   ```
4. Regla estricta para pruebas formales (`modo === 'prueba'` y `modo === 'examen'`):
   En estos modos, `ayudasReveladas` jamás se activa durante la rendición. Las respuestas y notas se calculan exclusivamente en el backend al entregar el intento.

---

### 1.2. Alerta de Preguntas Marcadas para Revisar al Entregar (UX-002)

#### Comportamiento Actual:
`intentarEnviar()` solo inspecciona `this.faltantes().length`. Si no hay preguntas en blanco, entrega de inmediato sin advertir sobre `this.marcadas()`.

#### Comportamiento Especificado:
1. Crear computed para preguntas marcadas que requieren revisión:
   ```typescript
   marcadasTexto = computed(() => {
     const indices = this.preguntas
       .map((p, idx) => (this.marcadas().has(p.id) ? idx + 1 : null))
       .filter((idx): idx is number => idx !== null);
     return indices.join(', ');
   });
   ```
2. Modificar `intentarEnviar()`:
   ```typescript
   intentarEnviar() {
     if (this.faltantes().length > 0 || this.marcadas().size > 0) {
       this.mostrarAvisoIncompleto.set(true);
     } else {
       this.confirmarEnvio();
     }
   }
   ```
3. Actualizar el modal de aviso incompleto:
   ```html
   @if (mostrarAvisoIncompleto()) {
     <div class="modal-fondo">
       <div class="modal tarjeta">
         <h3>Aviso antes de entregar</h3>
         
         @if (faltantes().length > 0) {
           <p class="aviso-faltantes">
             ⚠️ Te falta responder <strong>{{ faltantes().length }}</strong> pregunta{{ faltantes().length > 1 ? 's' : '' }}
             (Pregunta{{ faltantes().length > 1 ? 's' : '' }} {{ faltantesTexto() }}).
           </p>
         }
         
         @if (marcadas().size > 0) {
           <p class="aviso-marcadas">
             📌 Dejaste <strong>{{ marcadas().size }}</strong> pregunta{{ marcadas().size > 1 ? 's' : '' }} marcada{{ marcadas().size > 1 ? 's' : '' }} para revisar
             (Pregunta{{ marcadas().size > 1 ? 's' : '' }} {{ marcadasTexto() }}).
           </p>
         }

         <p class="aviso-confirmacion">¿Deseas revisarlas antes de finalizar?</p>

         <div class="modal__acciones">
           <button class="btn btn--secundario" (click)="irARevisarPendientes()">Ir a revisar</button>
           <button class="btn btn--peligro" (click)="confirmarEnvio()">Entregar de todas formas</button>
         </div>
       </div>
     </div>
   }
   ```
4. Método `irARevisarPendientes()`:
   Navega preferentemente a la primera pregunta en blanco; si no hay en blanco, navega a la primera marcada.

---

### 1.3. Renderizado Enriquecido de Enunciados (UX-003)

#### Comportamiento Actual:
`<p class="pregunta__enunciado">{{ preguntaActual.enunciado }}</p>`
Aqueja pérdida de saltos de línea, estrofas en poemas, viñetas y tablas.

#### Comportamiento Especificado:
Importar `MarkdownPipe` en `EvaluacionRunner` y sustituir por:
```html
<div class="pregunta__enunciado" [innerHTML]="preguntaActual.enunciado | markdown"></div>
```
Estilos requeridos para `.pregunta__enunciado`:
```css
.pregunta__enunciado {
  font-size: 1.05rem;
  line-height: 1.6;
  color: var(--texto-principal);
  margin-bottom: 1.25rem;
}
.pregunta__enunciado p {
  margin: 0.5rem 0;
}
.pregunta__enunciado blockquote {
  border-left: 3px solid var(--color-primario);
  margin: 0.75rem 0;
  padding: 0.25rem 0 0.25rem 1rem;
  color: var(--texto-secundario);
  font-style: italic;
}
```

---

## 2. Módulo de Identidad: Nombre y Curso del Estudiante (UX-004)

### 2.1. Backend (`backend/app/routers/auth.py` y schemas)
1. Extender `PerfilAlumnoRespuesta`:
   ```python
   class PerfilAlumnoRespuesta(BaseModel):
       id: int
       nombre: str
       apellidos: str
       nivel_id: int
       nombre_nivel: str | None = None
   ```
2. En `listar_alumnos` y `agregar_alumno`, realizar join o lookup con `Nivel.nombre` para poblar `nombre_nivel` (ej. `"4° básico"`).

### 2.2. Frontend (`sesion.service.ts`, `shell.ts`, `topbar.ts`, `alumno-inicio.ts`)
1. Actualizar interfaz `PerfilAlumnoActivo`:
   ```typescript
   export interface PerfilAlumnoActivo {
     id: number;
     nombre: string;
     apellidos: string;
     nivel_id: number;
     nombre_nivel?: string;
   }
   ```
2. En `Topbar`:
   ```html
   <a class="topbar__usuario" routerLink="/selector-perfil">
     <div class="topbar__avatar">{{ inicial }}</div>
     <div class="topbar__info-usuario">
       <span class="topbar__nombre">{{ nombre }}</span>
       @if (curso) {
         <span class="topbar__curso">{{ curso }}</span>
       }
     </div>
   </a>
   ```
3. En `alumno-inicio.ts`:
   ```html
   <h1>¡Hola de nuevo, {{ nombreAlumno() }}! 👋 <span class="badge-curso">{{ cursoAlumno() }}</span></h1>
   ```

---

## 3. Módulo Parser y Contenido: OA 165 y PARSER-001

### 3.1. Parser de Contenido (`backend/scripts/parser_contenido.py`)
Modificar la clasificación de tipo para que la presencia de la palabra *"alternativas"* en el texto descriptivo del paréntesis no fuerce el tipo si no existen opciones:
```python
if opciones:
    tipo = "verdadero_falso" if set(o.lower() for o in opciones) <= {"verdadero", "falso"} else "alternativas"
    opciones_finales = opciones
else:
    tipo = "verdadero_falso" if tipo == "verdadero_falso" else "desarrollo_breve"
    opciones_finales = None
```

### 3.2. Descontaminación de Pregunta 4 en OA 165
1. En `contenido/06-basico/examenes/lenguaje-y-comunicacion-examen-forma-b.md`:
   Asegurar que `Texto 3 (Poema: Tren nocturno hacia el sur)` no quede como cola del bloque de la pregunta 4.
2. En la base de datos `logos_qa`:
   Actualizar el registro `id = 2394` de la tabla `pregunta` para que su campo `enunciado` quede exactamente con la instrucción de la pregunta 4:
   ```sql
   UPDATE pregunta 
   SET enunciado = 'Da tu opinión fundamentada sobre la actitud de Antonia al organizar la minga sin que nadie se lo pidiera. Luego, a partir del Texto 2, explica qué conclusión puedes sacar sobre cómo las costumbres de una comunidad pueden ayudar a que una persona enfrente un problema que, sola, no podría resolver.'
   WHERE id = 2394;
   ```
   *Nota de seguridad:* Esta sentencia conserva el `id = 2394`, por lo que **no rompe ningún historial de intentos rendidos**.

---

## 4. Correcciones Editoriales de Matemática (MAT-CONT)

### 4.1. MAT-CONT-001: 6° Básico (Botellas)
- **Archivo:** `contenido/06-basico/matematica.md`, línea 84.
- **Cambio:**
  - *Antes:* `(2.050 ÷ 3 ≈ 683 cajas cada uno).`
  - *Después:* `(2.050 ÷ 3 = 683 cajas para cada distribuidor y sobra 1 caja sin repartir).`

### 4.2. MAT-CONT-002: 6° Básico (Razón 5:3)
- **Archivo:** `contenido/06-basico/matematica.md`, línea 152.
- **Cambio:**
  - *Antes:* `Respuesta esperada: 15 ÷ 5 = 3, por lo tanto 3×3 : 5×3... cuidado con el orden: 5:3 amplificado por 3 es 15:9. Hay **9 libros de ciencia**.`
  - *Después:* `Respuesta esperada: 15 ÷ 5 = 3 (factor de amplificación); la razón 5:3 amplificada por 3 es 15:9. Hay **9 libros de ciencia**.`

### 4.3. MAT-CONT-003: 3° Medio (Varianza)
- **Archivo:** `contenido/03-medio/matematica.md`, sección OA 2.
- **Cambio:** Añadir nota conceptual:
  - *"Nota conceptual: en este nivel escolar se calcula la varianza poblacional, dividiendo la suma de desviaciones cuadráticas entre el número total de observaciones N."*

---

## 5. Módulo Branding: Logo Corporativo (BRAND-001)

### Componente `frontend/src/app/shared/logo/logo.ts`:
1. Estructura con soporte para imagen oficial y fallback seguro:
   ```html
   <div class="logo">
     @if (!errorImagen()) {
       <img
         src="assets/branding/logo.svg"
         [attr.width]="tamano"
         [attr.height]="tamano"
         alt="Logos School"
         (error)="errorImagen.set(true)"
       />
     } @else {
       <!-- Fallback SVG vectorial existente -->
       <svg ...>...</svg>
     }
     @if (!soloIcono) {
       <span class="logo__texto">Logos School</span>
     }
   </div>
   ```
2. Si el usuario sube `logo.svg` o `logo.png` a `frontend/src/assets/branding/`, se mostrará automáticamente sin alterar layouts ni romper páginas.
