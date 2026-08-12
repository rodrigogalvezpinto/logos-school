import { Component, Input, signal, computed } from '@angular/core';
import { Router } from '@angular/router';
import { FormsModule } from '@angular/forms';
import { PREGUNTAS_MOCK, PreguntaMock } from '../../core/mock-data/mock-data';

export type ModoEvaluacion = 'autoevaluacion' | 'prueba' | 'examen';

@Component({
  selector: 'app-evaluacion-runner',
  standalone: true,
  imports: [FormsModule],
  template: `
    @if (!empezada()) {
      <div class="inicio tarjeta">
        <span class="inicio__etiqueta">{{ etiquetaModo() }}</span>
        <h1>{{ nombreEvaluacion }}</h1>
        <ul class="inicio__datos">
          <li>{{ preguntas.length }} preguntas</li>
          @if (modo === 'examen') {
            <li>90 minutos, sin pausas</li>
          } @else if (modo === 'prueba') {
            <li>Sin límite de tiempo — respóndela a tu ritmo</li>
          } @else {
            <li>Feedback inmediato en cada pregunta</li>
          }
        </ul>
        @if (modo === 'examen') {
          <p class="inicio__aviso">
            Esto simula tu examen real: no podrás pausar ni volver a intentarlo. Asegúrate de tener 90
            minutos disponibles antes de comenzar.
          </p>
        }
        <button class="btn btn--primario btn--grande" (click)="empezar()">Comenzar</button>
      </div>
    } @else if (!enviada()) {
      <div class="runner" [class.runner--examen]="modo === 'examen'">
        <div class="runner__barra">
          @if (modo !== 'examen') {
            <button class="runner__salir" (click)="volver()">← Salir (guarda tu avance)</button>
          } @else {
            <span></span>
          }
          <div class="runner__progreso">Pregunta {{ indiceActual() + 1 }} de {{ preguntas.length }}</div>
          @if (modo === 'examen') {
            <div class="runner__cronometro">⏱ {{ tiempoRestante() }}</div>
          } @else {
            <span></span>
          }
        </div>

        <div class="runner__mapa">
          @for (p of preguntas; track p.id; let i = $index) {
            <button
              class="mapa-item"
              [class.mapa-item--respondida]="respuestas()[p.id] !== undefined"
              [class.mapa-item--marcada]="marcadas().has(p.id)"
              [class.mapa-item--actual]="i === indiceActual()"
              (click)="irA(i)"
            >
              {{ i + 1 }}
            </button>
          }
        </div>

        <div class="tarjeta pregunta">
          <p class="pregunta__enunciado">{{ preguntaActual.enunciado }}</p>

          @if (preguntaActual.tipo === 'alternativas') {
            <div class="opciones">
              @for (op of preguntaActual.opciones; track op) {
                <label class="opcion" [class.opcion--elegida]="respuestas()[preguntaActual.id] === op">
                  <input
                    type="radio"
                    [name]="preguntaActual.id"
                    [value]="op"
                    [checked]="respuestas()[preguntaActual.id] === op"
                    (change)="responder(preguntaActual.id, op)"
                  />
                  {{ op }}
                </label>
              }
            </div>
          } @else {
            <div class="opciones">
              <label class="opcion" [class.opcion--elegida]="respuestas()[preguntaActual.id] === 'Verdadero'">
                <input
                  type="radio"
                  [name]="preguntaActual.id"
                  (change)="responder(preguntaActual.id, 'Verdadero')"
                />
                Verdadero
              </label>
              <label class="opcion" [class.opcion--elegida]="respuestas()[preguntaActual.id] === 'Falso'">
                <input
                  type="radio"
                  [name]="preguntaActual.id"
                  (change)="responder(preguntaActual.id, 'Falso')"
                />
                Falso
              </label>
            </div>
          }

          @if (modo === 'autoevaluacion' && respuestas()[preguntaActual.id]) {
            <div class="feedback">✓ ¡Bien! Puedes pasar a la siguiente pregunta.</div>
          }

          <label class="marcar-revisar">
            <input type="checkbox" [checked]="marcadas().has(preguntaActual.id)" (change)="marcarRevisar(preguntaActual.id)" />
            Marcar para revisar después
          </label>
        </div>

        <div class="runner__nav">
          <button class="btn btn--secundario" [disabled]="indiceActual() === 0" (click)="anterior()">Anterior</button>
          @if (indiceActual() < preguntas.length - 1) {
            <button class="btn btn--primario" (click)="siguiente()">Siguiente</button>
          } @else {
            <button class="btn btn--primario" (click)="intentarEnviar()">Entregar</button>
          }
        </div>
      </div>

      @if (mostrarAvisoIncompleto()) {
        <div class="modal-fondo">
          <div class="modal tarjeta">
            <h3>Te falta responder {{ faltantes().length }} pregunta{{ faltantes().length > 1 ? 's' : '' }}</h3>
            <p>
              Pregunta{{ faltantes().length > 1 ? 's' : '' }}
              {{ faltantesTexto() }} — si envías ahora, quedará{{ faltantes().length > 1 ? 'n' : '' }} en
              blanco.
            </p>
            <div class="modal__acciones">
              <button class="btn btn--secundario" (click)="irARevisarFaltantes()">Ir a revisar</button>
              <button class="btn btn--peligro" (click)="confirmarEnvio()">Enviar de todas formas</button>
            </div>
          </div>
        </div>
      }
    } @else {
      <div class="resultado tarjeta">
        <span class="resultado__etiqueta">Resultado</span>
        @if (modo !== 'autoevaluacion') {
          <p class="resultado__nota">Nota: {{ notaSimulada }}</p>
        }
        <p class="resultado__puntaje">{{ correctasSimuladas }} de {{ preguntas.length }} correctas</p>
        <h3>Lo bueno</h3>
        <p>Dominaste la mayoría de las preguntas de valor posicional.</p>
        <h3>A reforzar</h3>
        <p>Repasa comparación de números — 1 pregunta con error.</p>
        <button class="btn btn--primario btn--grande" (click)="volver()">Volver</button>
      </div>
    }
  `,
  styleUrl: './evaluacion-runner.scss',
})
export class EvaluacionRunner {
  @Input() modo: ModoEvaluacion = 'autoevaluacion';
  @Input() nombreEvaluacion = 'Matemática — Números y Operaciones';
  @Input() rutaSalida: string[] = ['/alumno/inicio'];

  preguntas: PreguntaMock[] = PREGUNTAS_MOCK;

  empezada = signal(false);
  enviada = signal(false);
  indiceActual = signal(0);
  respuestas = signal<Record<string, string>>({});
  marcadas = signal<Set<string>>(new Set());
  mostrarAvisoIncompleto = signal(false);
  tiempoRestante = signal('89:47');

  correctasSimuladas = 2;
  notaSimulada = '5.4';

  constructor(private router: Router) {}

  get preguntaActual() {
    return this.preguntas[this.indiceActual()];
  }

  etiquetaModo(): string {
    if (this.modo === 'examen') return 'Examen simulacro';
    if (this.modo === 'prueba') return 'Prueba de unidad';
    return 'Práctica libre';
  }

  faltantes = computed(() => this.preguntas.filter((p) => this.respuestas()[p.id] === undefined));

  faltantesTexto(): string {
    return this.faltantes()
      .map((_, i) => this.preguntas.findIndex((p) => p.id === this.faltantes()[i].id) + 1)
      .join(', ');
  }

  empezar() {
    this.empezada.set(true);
  }

  responder(id: string, valor: string) {
    this.respuestas.update((r) => ({ ...r, [id]: valor }));
  }

  marcarRevisar(id: string) {
    this.marcadas.update((set) => {
      const nuevo = new Set(set);
      nuevo.has(id) ? nuevo.delete(id) : nuevo.add(id);
      return nuevo;
    });
  }

  irA(i: number) {
    this.indiceActual.set(i);
  }

  anterior() {
    if (this.indiceActual() > 0) this.indiceActual.update((i) => i - 1);
  }

  siguiente() {
    if (this.indiceActual() < this.preguntas.length - 1) this.indiceActual.update((i) => i + 1);
  }

  intentarEnviar() {
    if (this.faltantes().length > 0) {
      this.mostrarAvisoIncompleto.set(true);
    } else {
      this.confirmarEnvio();
    }
  }

  irARevisarFaltantes() {
    const primeraFaltante = this.preguntas.findIndex((p) => this.respuestas()[p.id] === undefined);
    this.indiceActual.set(primeraFaltante);
    this.mostrarAvisoIncompleto.set(false);
  }

  confirmarEnvio() {
    this.mostrarAvisoIncompleto.set(false);
    this.enviada.set(true);
  }

  volver() {
    this.router.navigate(this.rutaSalida);
  }
}
