# 07 — Prompt de Ejecución para Agente de Programación Externo

> **Instrucciones para el Agente:** Lee este documento completo antes de tocar cualquier archivo. Sigue rigurosamente las restricciones, la secuencia de tareas y los criterios de aceptación. No realices modificaciones no solicitadas.

---

## Rol y Misión
Eres un desarrollador full-stack senior trabajando en el repositorio `Logos School`. Tu misión es implementar con precisión quirúrgica las correcciones técnicas, de UX/UI y editoriales aprobadas en la auditoría de la plataforma, garantizando que el 100% de la suite de pruebas (886 tests) se mantenga en verde.

---

## Reglas Críticas y Restricciones Absolutas
1. **Preservar Datos Históricos:** No ejecutes `DROP TABLE`, `TRUNCATE` ni scripts destructivos. Los `id` de las preguntas, objetivos de aprendizaje e intentos de examen rendidos deben mantenerse intactos.
2. **No Alterar Funcionalidades No Solicitadas:** No cambies bibliotecas, no actualices Angular ni FastAPI, no cambies la estructura general del proyecto.
3. **Verificación Continua:** Después de cada tarea, debes ejecutar las pruebas unitarias y E2E correspondientes.

---

## Tarea 1: Evaluaciones — Ayuda Bajo Demanda y Desacople de Desarrollo (MAT-UI-001 y UX-001)

### Archivo a Modificar:
`frontend/src/app/shared/evaluacion-runner/evaluacion-runner.ts`

### Instrucciones:
1. Agrega el signal:
   ```typescript
   ayudasReveladas = signal<Set<number>>(new Set());
   ```
2. Agrega el método:
   ```typescript
   solicitarAyuda(preguntaId: number) {
     this.ayudasReveladas.update((set) => new Set(set).add(preguntaId));
   }
   ```
3. En el template, dentro del bloque `@if (modo === 'autoevaluacion')`:
   - Sustituye la revelación automática por un botón que solo se habilita cuando `respuestas()[preguntaActual.id]` tiene valor:
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
4. Agrega estilos CSS limpios en el componente para `.btn-ayuda-practica`, `.feedback__orientativo`, etc.
5. **Criterio de Verificación:** Al marcar una alternativa en práctica, la respuesta NO debe revelarse de inmediato. Al pulsar el botón, debe mostrarse la retroalimentación.

---

## Tarea 2: Evaluaciones — Advertencia de Preguntas Marcadas al Entregar (UX-002)

### Archivo a Modificar:
`frontend/src/app/shared/evaluacion-runner/evaluacion-runner.ts`

### Instrucciones:
1. Agrega el computed `marcadasTexto`:
   ```typescript
   marcadasTexto = computed(() => {
     const indices = this.preguntas
       .map((p, idx) => (this.marcadas().has(p.id) ? idx + 1 : null))
       .filter((idx): idx is number => idx !== null);
     return indices.join(', ');
   });
   ```
2. Modifica `intentarEnviar()`:
   ```typescript
   intentarEnviar() {
     if (this.faltantes().length > 0 || this.marcadas().size > 0) {
       this.mostrarAvisoIncompleto.set(true);
     } else {
       this.confirmarEnvio();
     }
   }
   ```
3. En el modal `@if (mostrarAvisoIncompleto())`, renderiza advertencias diferenciadas para preguntas sin responder (`faltantes`) y para preguntas marcadas (`marcadas`), con el botón `"Ir a revisar"` que llame a:
   ```typescript
   irARevisarPendientes() {
     const primeraFaltante = this.preguntas.findIndex((p) => this.respuestas()[p.id] === undefined);
     if (primeraFaltante !== -1) {
       this.indiceActual.set(primeraFaltante);
     } else {
       const primeraMarcada = this.preguntas.findIndex((p) => this.marcadas().has(p.id));
       if (primeraMarcada !== -1) this.indiceActual.set(primeraMarcada);
     }
     this.mostrarAvisoIncompleto.set(false);
   }
   ```
4. **Criterio de Verificación:** Si se marcan preguntas para revisar y se finaliza el intento, el modal debe alertar sobre las preguntas marcadas y permitir ir a revisarlas.

---

## Tarea 3: Evaluaciones — Renderizado Enriquecido de Enunciados (UX-003)

### Archivo a Modificar:
`frontend/src/app/shared/evaluacion-runner/evaluacion-runner.ts`

### Instrucciones:
1. Importa `MarkdownPipe` en los `imports` del componente:
   ```typescript
   import { MarkdownPipe } from '../markdown.pipe';
   ...
   imports: [FormsModule, BotonEscuchar, MarkdownPipe],
   ```
2. En el template, cambia:
   ```html
   <!-- Antes -->
   <p class="pregunta__enunciado">{{ preguntaActual.enunciado }}</p>
   <!-- Después -->
   <div class="pregunta__enunciado" [innerHTML]="preguntaActual.enunciado | markdown"></div>
   ```
3. **Criterio de Verificación:** Los saltos de línea, estrofas de poemas y listas se ven con espaciado vertical y tipografía legible.

---

## Tarea 4: Identidad — Curso Junto al Nombre del Alumno (UX-004)

### Archivos a Modificar:
1. `backend/app/routers/auth.py`:
   - Agrega `nombre_nivel: str | None = None` a `PerfilAlumnoRespuesta`.
   - En `listar_alumnos`, pobla `nombre_nivel` desde `Nivel.nombre`.
2. `frontend/src/app/core/auth.service.ts` y `sesion.service.ts`:
   - Agrega `nombre_nivel?: string` a `PerfilAlumnoRespuesta` y `PerfilAlumnoActivo`.
3. `frontend/src/app/layout/shell/shell.ts` y `topbar.ts`:
   - Muestra el nombre y curso en la barra superior (ej. `Sofía (4° básico)`).
4. `frontend/src/app/pages/alumno-inicio/alumno-inicio.ts`:
   - En el saludo, muestra `¡Hola de nuevo, Sofía! 👋 · 4° Básico`.
5. **Criterio de Verificación:** Al iniciar sesión con `apoderado.prueba@logos.cl` y entrar como Sofía, tanto la barra superior como el saludo de bienvenida deben mostrar claramente su curso.

---

## Tarea 5: Limpieza de Contenido y Base de Datos (CONT-001 y MAT-CONT)

### 1. Corrección de OA 165 (Pregunta 2394):
Ejecuta la actualización en `logos_qa` para remover el poema incrustado en la pregunta 4:
```sql
UPDATE pregunta 
SET enunciado = 'Da tu opinión fundamentada sobre la actitud de Antonia al organizar la minga sin que nadie se lo pidiera. Luego, a partir del Texto 2, explica qué conclusión puedes sacar sobre cómo las costumbres de una comunidad pueden ayudar a que una persona enfrente un problema que, sola, no podría resolver.'
WHERE id = 2394;
```

### 2. Correcciones en Markdown de Matemática:
- `contenido/06-basico/matematica.md` (línea 84):
  Cambia `(2.050 ÷ 3 ≈ 683 cajas cada uno).` por `(2.050 ÷ 3 = 683 cajas para cada distribuidor y sobra 1 caja sin repartir).`
- `contenido/06-basico/matematica.md` (línea 152):
  Remueve la frase `... cuidado con el orden:` dejando la respuesta limpia.
- `contenido/03-medio/matematica.md`:
  Agrega la nota aclaratoria de varianza poblacional en el OA 2.

### 3. Corrección del Parser (`backend/scripts/parser_contenido.py`):
En `_parsear_bloque_preguntas`, si una pregunta no tiene `opciones`, asigna `tipo = "desarrollo_breve"` a menos que sea `"verdadero_falso"`.

---

## Tarea 6: Validación y No-Regresión

Ejecuta secuencialmente los tres comandos de validación:
```bash
# 1. Pruebas Unitarias Frontend
cd frontend && npm test -- --watch=false

# 2. Pruebas Unitarias e Integración Backend
cd ../backend && .venv/bin/pytest -q

# 3. Pruebas End-to-End Playwright
cd ../frontend && npx playwright test e2e/flujo-completo-*.spec.ts e2e/casos-borde.spec.ts e2e/accesibilidad.spec.ts
```

Todos los comandos deben finalizar con código de salida 0 (100% éxito).
