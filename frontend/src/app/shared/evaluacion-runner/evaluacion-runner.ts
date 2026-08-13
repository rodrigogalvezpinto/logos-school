import { Component, Input, OnInit, signal, computed, inject } from '@angular/core';
import { Router } from '@angular/router';
import { FormsModule } from '@angular/forms';
import { EvaluacionesService } from '../../core/evaluaciones.service';

export type ModoEvaluacion = 'autoevaluacion' | 'prueba' | 'examen';

export interface PreguntaRunner {
  id: number;
  tipo: string;
  enunciado: string;
  opciones: string[] | null;
  respuesta_correcta?: string;
  retroalimentacion?: string;
}

@Component({
  selector: 'app-evaluacion-runner',
  standalone: true,
  imports: [FormsModule],
  template: `
    @if (cargando()) {
      <p class="cargando">Cargando…</p>
    } @else if (!empezada()) {
      <div class="inicio tarjeta">
        <span class="inicio__etiqueta">{{ etiquetaModo() }}</span>
        <h1>{{ nombreEvaluacion }}</h1>
        <ul class="inicio__datos">
          <li>{{ preguntas.length }} preguntas</li>
          @if (modo === 'examen') {
            <li>{{ tiempoLimiteMin }} minutos, sin pausas</li>
          } @else if (modo === 'prueba') {
            <li>Sin límite de tiempo — respóndela a tu ritmo</li>
          } @else {
            <li>Feedback inmediato en cada pregunta</li>
          }
        </ul>
        @if (modo === 'examen') {
          <p class="inicio__aviso">
            Esto simula tu examen real: no podrás pausar ni volver a intentarlo. Asegúrate de tener
            {{ tiempoLimiteMin }} minutos disponibles antes de comenzar.
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
            <div class="runner__cronometro">⏱ {{ tiempoRestanteTexto() }}</div>
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

          @if (preguntaActual.tipo === 'alternativas' && preguntaActual.opciones) {
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
          } @else if (preguntaActual.tipo === 'verdadero_falso') {
            <div class="opciones">
              <label class="opcion" [class.opcion--elegida]="respuestas()[preguntaActual.id] === 'Verdadero'">
                <input type="radio" [name]="preguntaActual.id" (change)="responder(preguntaActual.id, 'Verdadero')" />
                Verdadero
              </label>
              <label class="opcion" [class.opcion--elegida]="respuestas()[preguntaActual.id] === 'Falso'">
                <input type="radio" [name]="preguntaActual.id" (change)="responder(preguntaActual.id, 'Falso')" />
                Falso
              </label>
            </div>
          } @else {
            <div class="opciones">
              <textarea
                class="respuesta-abierta"
                rows="4"
                [value]="respuestas()[preguntaActual.id] || ''"
                (input)="responder(preguntaActual.id, $any($event.target).value)"
                placeholder="Escribe tu respuesta…"
              ></textarea>
            </div>
          }

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
          <p class="resultado__nota">Nota: {{ notaFinal() }}</p>
          <p class="resultado__puntaje">{{ puntajeFinal() }} de {{ totalAutocorregible() }} correctas (autocorregibles)</p>
        }
        <h3>Revisa tu resultado</h3>
        <p>
          @if (modo === 'autoevaluacion') {
            Practica completada. Puedes repetirla cuando quieras.
          } @else {
            Tu nota se calculó según la escala chilena de exigencia 60%.
          }
        </p>
        <button class="btn btn--primario btn--grande" (click)="volver()">Volver</button>
      </div>
    }
  `,
  styleUrl: './evaluacion-runner.scss',
})
export class EvaluacionRunner implements OnInit {
  @Input() modo: ModoEvaluacion = 'autoevaluacion';
  @Input() nombreEvaluacion = '';
  @Input() rutaSalida: string[] = ['/alumno/inicio'];
  @Input() preguntas: PreguntaRunner[] = [];
  @Input() intentoId: number | null = null;
  @Input() tiempoLimiteMin = 90;
  /** Si el intento ya fue entregado antes (reanudación de una prueba/examen ya
   * rendido), salta directo al resultado en vez de mostrar las preguntas de nuevo. */
  @Input() resultadoPrevio: { puntaje: number | null; nota: number | null } | null = null;

  private router = inject(Router);
  private evaluacionesService = inject(EvaluacionesService);

  cargando = signal(false);
  empezada = signal(false);
  enviada = signal(false);
  indiceActual = signal(0);
  respuestas = signal<Record<number, string>>({});
  marcadas = signal<Set<number>>(new Set());
  mostrarAvisoIncompleto = signal(false);
  tiempoRestanteSeg = signal(0);
  puntajeFinal = signal<number | null>(null);
  notaFinal = signal<number | null>(null);
  private cronometroId?: ReturnType<typeof setInterval>;

  ngOnInit() {
    if (this.resultadoPrevio) {
      this.empezada.set(true);
      this.enviada.set(true);
      this.puntajeFinal.set(this.resultadoPrevio.puntaje);
      this.notaFinal.set(this.resultadoPrevio.nota);
      return;
    }
    if (this.modo === 'examen') {
      this.tiempoRestanteSeg.set(this.tiempoLimiteMin * 60);
    }
  }

  get preguntaActual(): PreguntaRunner {
    return this.preguntas[this.indiceActual()];
  }

  totalAutocorregible(): number {
    return this.preguntas.filter((p) => p.tipo === 'alternativas' || p.tipo === 'verdadero_falso').length;
  }

  etiquetaModo(): string {
    if (this.modo === 'examen') return 'Examen simulacro';
    if (this.modo === 'prueba') return 'Prueba de unidad';
    return 'Práctica libre';
  }

  esCorrectaEnAutoevaluacion(p: PreguntaRunner): boolean {
    const dada = (this.respuestas()[p.id] || '').trim().toLowerCase();
    return dada === (p.respuesta_correcta || '').trim().toLowerCase();
  }

  faltantes = computed(() => this.preguntas.filter((p) => this.respuestas()[p.id] === undefined));

  faltantesTexto(): string {
    const nums = this.faltantes().map((f) => this.preguntas.findIndex((p) => p.id === f.id) + 1);
    return nums.join(', ');
  }

  empezar() {
    this.empezada.set(true);
    if (this.modo === 'examen') {
      this.cronometroId = setInterval(() => {
        this.tiempoRestanteSeg.update((s) => Math.max(0, s - 1));
        if (this.tiempoRestanteSeg() === 0) {
          this.confirmarEnvio(); // se agota el tiempo → envío automático, sin excepción
        }
      }, 1000);
    }
  }

  tiempoRestanteTexto(): string {
    const s = this.tiempoRestanteSeg();
    const min = Math.floor(s / 60).toString().padStart(2, '0');
    const seg = (s % 60).toString().padStart(2, '0');
    return `${min}:${seg}`;
  }

  responder(preguntaId: number, valor: string) {
    this.respuestas.update((r) => ({ ...r, [preguntaId]: valor }));
    if (this.intentoId) {
      this.evaluacionesService.responder(this.intentoId, preguntaId, valor).subscribe();
    }
  }

  marcarRevisar(id: number) {
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
    if (this.cronometroId) clearInterval(this.cronometroId);

    if (this.intentoId && this.modo !== 'autoevaluacion') {
      this.cargando.set(true);
      this.evaluacionesService.entregar(this.intentoId).subscribe((intento) => {
        this.puntajeFinal.set(intento.puntaje);
        this.notaFinal.set(intento.nota);
        this.cargando.set(false);
        this.enviada.set(true);
      });
    } else {
      this.enviada.set(true);
    }
  }

  volver() {
    if (this.cronometroId) clearInterval(this.cronometroId);
    this.router.navigate(this.rutaSalida);
  }
}
