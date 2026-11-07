import { Component, Input, OnInit, signal, computed, inject } from '@angular/core';
import { Router } from '@angular/router';
import { NgTemplateOutlet } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { firstValueFrom } from 'rxjs';
import { DetallePregunta, EvaluacionesService } from '../../core/evaluaciones.service';
import { BotonEscuchar } from '../boton-escuchar/boton-escuchar';
import { MarkdownPipe } from '../markdown.pipe';

export type ModoEvaluacion = 'autoevaluacion' | 'prueba' | 'examen';
type RevisionDesarrollo = 'correcta' | 'parcial' | 'incorrecta';

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
  imports: [FormsModule, BotonEscuchar, MarkdownPipe, NgTemplateOutlet],
  template: `
    <ng-template #revisionDesarrollo let-id>
      <fieldset class="revision-desarrollo">
        <legend>Compara tu respuesta con la pauta</legend>
        @for (estado of estadosRevision; track estado.valor) {
          <button type="button" class="btn btn--secundario"
            [attr.aria-pressed]="revisionesDesarrollo()[id] === estado.valor"
            [disabled]="!respuestaParaRevision(id)?.trim()"
            (click)="revisarDesarrollo(id, estado.valor)">{{ estado.texto }}</button>
        }
        <p>Es tu revisión personal, no una corrección automática. No cambia la nota y no se guarda al salir.</p>
      </fieldset>
    </ng-template>
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
            <li>Feedback bajo demanda en cada pregunta</li>
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
        <h1>{{ nombreEvaluacion }}</h1>
        <div class="runner__barra">
          @if (modo !== 'examen') {
            <button class="runner__salir" (click)="volver()">← Salir (guarda tu avance)</button>
          } @else {
            <span></span>
          }
          <div class="runner__progreso">Pregunta {{ indiceActual() + 1 }} de {{ preguntas.length }}</div>
          <div class="runner__acciones-barra">
            @if (modo === 'examen') {
              <span class="runner__cronometro">⏱ {{ tiempoRestanteTexto() }}</span>
            }
            <button class="runner__finalizar" (click)="intentarEnviar()">Finalizar intento</button>
          </div>
        </div>

        <div class="runner__mapa">
          @for (p of preguntas; track p.id; let i = $index) {
            <button
              class="mapa-item"
              [class.mapa-item--respondida]="!!respuestas()[p.id]?.trim()"
              [class.mapa-item--marcada]="marcadas().has(p.id)"
              [class.mapa-item--actual]="i === indiceActual()"
              (click)="irA(i)"
            >
              {{ i + 1 }}
            </button>
          }
        </div>

        <div class="tarjeta pregunta">
          <app-boton-escuchar class="pregunta__escuchar" [texto]="preguntaActual.enunciado" />
          <div class="pregunta__enunciado" [innerHTML]="preguntaActual.enunciado | markdown"></div>

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
                  @if (tieneMarcadorVisual(op)) {
                    <span class="opcion__visual" [innerHTML]="op | markdown"></span>
                  } @else {
                    {{ op }}
                  }
                </label>
              }
            </div>
          } @else if (preguntaActual.tipo === 'varias_correctas' && preguntaActual.opciones) {
            <p class="opciones__instruccion">Marca todas las alternativas correctas (puede haber más de una).</p>
            <div class="opciones" role="group" aria-label="Marca todas las alternativas correctas">
              @for (op of preguntaActual.opciones; track op) {
                <label class="opcion" [class.opcion--elegida]="estaMarcada(preguntaActual.id, op)">
                  <input
                    type="checkbox"
                    [value]="op"
                    [checked]="estaMarcada(preguntaActual.id, op)"
                    (change)="alternarVarias(preguntaActual, op)"
                  />
                  @if (tieneMarcadorVisual(op)) {
                    <span class="opcion__visual" [innerHTML]="op | markdown"></span>
                  } @else {
                    {{ op }}
                  }
                </label>
              }
            </div>
          } @else if (preguntaActual.tipo === 'verdadero_falso') {
            <div class="opciones">
              <label class="opcion" [class.opcion--elegida]="respuestas()[preguntaActual.id] === 'Verdadero'">
                <input type="radio" [name]="preguntaActual.id" value="Verdadero" [checked]="respuestas()[preguntaActual.id] === 'Verdadero'" (change)="responder(preguntaActual.id, 'Verdadero')" />
                Verdadero
              </label>
              <label class="opcion" [class.opcion--elegida]="respuestas()[preguntaActual.id] === 'Falso'">
                <input type="radio" [name]="preguntaActual.id" value="Falso" [checked]="respuestas()[preguntaActual.id] === 'Falso'" (change)="responder(preguntaActual.id, 'Falso')" />
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

          @if (modo === 'autoevaluacion') {
            @if (!ayudasReveladas().has(preguntaActual.id)) {
              <button
                type="button"
                class="btn btn--secundario btn-ayuda-practica"
                [disabled]="!respuestas()[preguntaActual.id]?.trim()"
                (click)="solicitarAyuda(preguntaActual.id)"
              >
                💡 Comprobar respuesta / Ver explicación
              </button>
            } @else {
              <div class="feedback feedback--revelado">
                @if (esAutocorregible(preguntaActual.tipo)) {
                  @if (esCorrectaEnAutoevaluacion(preguntaActual)) {
                    <div class="feedback__exito">
                      <p class="feedback__tag-ok">✓ ¡Correcto!</p>
                      @if (preguntaActual.retroalimentacion) {
                        <div class="feedback__cuerpo" [innerHTML]="preguntaActual.retroalimentacion | markdown"></div>
                      }
                    </div>
                  } @else {
                    <div class="feedback__atencion">
                      <p><strong>Respuesta correcta: {{ textoRespuesta(preguntaActual.respuesta_correcta, preguntaActual.tipo) }}.</strong></p>
                      @if (preguntaActual.retroalimentacion) {
                        <div class="feedback__cuerpo" [innerHTML]="preguntaActual.retroalimentacion | markdown"></div>
                      }
                    </div>
                  }
                } @else {
                  <!-- Pregunta abierta / desarrollo: No juzga como incorrecta; ofrece solución orientativa -->
                  <div class="feedback__orientativo">
                    <p class="feedback__titulo">Pauta de autoevaluación:</p>
                    <div [innerHTML]="preguntaActual.respuesta_correcta | markdown"></div>
                    @if (preguntaActual.retroalimentacion) {
                      <div class="feedback__retro" [innerHTML]="preguntaActual.retroalimentacion | markdown"></div>
                    }
                    <ng-container [ngTemplateOutlet]="revisionDesarrollo" [ngTemplateOutletContext]="{ $implicit: preguntaActual.id }" />
                  </div>
                }
              </div>
            }
          }

          <label class="marcar-revisar">
            <input type="checkbox" [checked]="marcadas().has(preguntaActual.id)" (change)="marcarRevisar(preguntaActual.id)" />
            Marcar para revisar después
          </label>

          @if (mostrandoFormularioError() === preguntaActual.id) {
            <div class="reportar-error__form">
              <textarea
                rows="2"
                placeholder="¿Qué está mal en esta pregunta? (opcional)"
                [value]="comentarioError()"
                (input)="comentarioError.set($any($event.target).value)"
              ></textarea>
              <div class="reportar-error__acciones">
                <button class="btn btn--secundario" (click)="cancelarReportarError()">Cancelar</button>
                <button class="btn btn--primario" (click)="enviarReporteError(preguntaActual.id)">Enviar reporte</button>
              </div>
            </div>
          } @else if (preguntasReportadas().has(preguntaActual.id)) {
            <p class="reportar-error__confirmacion">✓ Gracias, revisaremos esta pregunta.</p>
          } @else {
            <button class="reportar-error__link" (click)="mostrandoFormularioError.set(preguntaActual.id)">
              ⚠ Reportar error en esta pregunta
            </button>
          }
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
              <button class="btn btn--peligro" (click)="confirmarEnvio()">Enviar de todas formas</button>
            </div>
          </div>
        </div>
      }
    } @else {
      <div class="resultado tarjeta">
        <span class="resultado__etiqueta">Resultado</span>
        <h1>{{ nombreEvaluacion }}</h1>
        @if (modo !== 'autoevaluacion') {
          <p class="resultado__nota" [class.resultado__nota--reprobada]="notaFinal() !== null && notaFinal()! < 4">
            <span class="resultado__alcance-nota">{{ todasAutocorregibles() ? 'Nota:' : 'Nota de preguntas autocorregibles:' }}</span> {{ notaFinal() }}
          </p>
          <p class="resultado__puntaje">{{ puntajeFinal() }} de {{ totalAutocorregible() }} correctas{{ todasAutocorregibles() ? '' : ' (autocorregibles)' }}</p>
        }
        <h2>Revisa tu resultado</h2>
        <p>
          @if (modo === 'autoevaluacion') {
            Practica completada. Puedes repetirla cuando quieras.
          } @else if (notaFinal() !== null && notaFinal()! < 4) {
            Todavía no — revisa el detalle de abajo para ver justo qué te faltó, y vuelve a intentarlo cuando quieras.
          } @else {
            Tu nota se calculó según la escala chilena de exigencia 60%.
          }
        </p>

        @if (detalle().length > 0) {
          <table class="resultado__detalle">
            <thead>
              <tr>
                <th>Pregunta</th>
                <th>Resultado</th>
                <th>Revisión</th>
              </tr>
            </thead>
            <tbody>
              @for (d of detalle(); track d.pregunta_id; let i = $index) {
                <tr>
                  <td>{{ i + 1 }}</td>
                  <td>
                    @if (d.es_correcta === true) {
                      <span class="resultado__ok">✓ Correcta</span>
                    } @else if (d.es_correcta === false) {
                      <span class="resultado__mal">✗ Incorrecta</span>
                    } @else {
                      <span class="resultado__sin-corregir">— Sin corrección automática</span>
                    }
                  </td>
                  <td>
                    <button class="resultado__revisar" (click)="revisionAbierta.set(revisionAbierta() === d.pregunta_id ? null : d.pregunta_id)">
                      {{ revisionAbierta() === d.pregunta_id ? 'Ocultar' : 'Revisar' }}
                    </button>
                  </td>
                </tr>
                @if (revisionAbierta() === d.pregunta_id) {
                  <tr class="resultado__revision-detalle">
                    <td colspan="3">
                      <div class="resultado__enunciado" [innerHTML]="d.enunciado | markdown"></div>
                      <p>Tu respuesta: <strong>{{ textoRespuesta(d.respuesta_alumno, d.tipo) || '(en blanco)' }}</strong></p>
                      @if (d.respuesta_correcta) {
                        <p>Respuesta correcta: <strong>{{ textoRespuesta(d.respuesta_correcta, d.tipo) }}</strong></p>
                      }
                      @if (d.pauta_orientativa) {
                        <p><strong>Pauta orientativa para revisar tu respuesta:</strong></p>
                        <div [innerHTML]="d.pauta_orientativa | markdown"></div>
                      }
                      @if (d.retroalimentacion) {
                        <div [innerHTML]="d.retroalimentacion | markdown"></div>
                      }
                      @if (d.es_correcta === null) {
                        @if (!d.respuesta_alumno?.trim()) {
                          <p>Dejaste esta respuesta en blanco. Puedes estudiar la pauta para intentarlo de nuevo.</p>
                        }
                        <ng-container [ngTemplateOutlet]="revisionDesarrollo" [ngTemplateOutletContext]="{ $implicit: d.pregunta_id }" />
                      }
                    </td>
                  </tr>
                }
              }
            </tbody>
          </table>
        }

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
  /** Necesario para "Reportar error" (identifica quién reporta) — ver
   * planificacion/27-plan-incorporacion-hallazgos-brincus.md, ítems 2.1/2.6. */
  @Input() perfilAlumnoId: number | null = null;
  /** Si el intento ya fue entregado antes (reanudación de una prueba/examen ya
   * rendido), salta directo al resultado en vez de mostrar las preguntas de nuevo. */
  @Input() resultadoPrevio: { puntaje: number | null; nota: number | null } | null = null;
  /** Si el alumno abandonó un intento a medio hacer y vuelve, el backend ya reanuda el
   * mismo intento en vez de crear uno nuevo (ver IniciarIntento.ejecutar) y devuelve las
   * respuestas ya guardadas — sin esto, el runner las descartaba y el alumno veía todas
   * las preguntas como "sin responder" en el mapa aunque ya estuvieran guardadas (hallazgo
   * real comparando con Brincus, que sí retoma el intento visualmente donde quedó). */
  @Input() respuestasIniciales: Record<number, string> = {};
  /** Fecha real de inicio del intento (ISO), del backend — si el alumno recarga la
   * página a mitad de un examen y `empezar()` se llama de nuevo, el cronómetro debe
   * seguir contando desde el inicio real, no reiniciarse al tiempo completo (bug real:
   * recargar la página "regalaba" tiempo extra, contradiciendo el aviso "Sin pausas"). */
  @Input() fechaInicioIntento: string | null = null;

  private router = inject(Router);
  private evaluacionesService = inject(EvaluacionesService);

  cargando = signal(false);
  empezada = signal(false);
  enviada = signal(false);
  indiceActual = signal(0);
  respuestas = signal<Record<number, string>>({});
  marcadas = signal<Set<number>>(new Set());
  ayudasReveladas = signal<Set<number>>(new Set());
  revisionesDesarrollo = signal<Record<number, RevisionDesarrollo>>({});
  readonly estadosRevision = [
    { valor: 'correcta', texto: 'Correcta' },
    { valor: 'parcial', texto: 'Parcial' },
    { valor: 'incorrecta', texto: 'Incorrecta' },
  ] as const;
  mostrarAvisoIncompleto = signal(false);
  tiempoRestanteSeg = signal(0);
  puntajeFinal = signal<number | null>(null);
  notaFinal = signal<number | null>(null);
  detalle = signal<DetallePregunta[]>([]);
  revisionAbierta = signal<number | null>(null);
  mostrandoFormularioError = signal<number | null>(null);
  comentarioError = signal('');
  preguntasReportadas = signal<Set<number>>(new Set());
  private cronometroId?: ReturnType<typeof setInterval>;

  ngOnInit() {
    if (this.resultadoPrevio) {
      this.empezada.set(true);
      this.enviada.set(true);
      this.puntajeFinal.set(this.resultadoPrevio.puntaje);
      this.notaFinal.set(this.resultadoPrevio.nota);
      this.cargarDetalle();
      return;
    }
    if (Object.keys(this.respuestasIniciales).length > 0) {
      this.respuestas.set({ ...this.respuestasIniciales });
    }
    if (this.modo === 'examen') {
      if (this.fechaInicioIntento) {
        const transcurridoSeg = Math.floor((Date.now() - new Date(this.fechaInicioIntento).getTime()) / 1000);
        this.tiempoRestanteSeg.set(Math.max(0, this.tiempoLimiteMin * 60 - transcurridoSeg));
      } else {
        this.tiempoRestanteSeg.set(this.tiempoLimiteMin * 60);
      }
    }
  }

  private cargarDetalle() {
    if (this.intentoId && this.modo !== 'autoevaluacion') {
      this.evaluacionesService.obtenerDetalle(this.intentoId).subscribe((d) => this.detalle.set(d));
    }
  }

  cancelarReportarError() {
    this.mostrandoFormularioError.set(null);
    this.comentarioError.set('');
  }

  enviarReporteError(preguntaId: number) {
    if (!this.perfilAlumnoId) return;
    this.evaluacionesService.reportarErrorPregunta(preguntaId, this.perfilAlumnoId, this.comentarioError()).subscribe(() => {
      this.preguntasReportadas.update((set) => new Set(set).add(preguntaId));
      this.mostrandoFormularioError.set(null);
      this.comentarioError.set('');
    });
  }

  get preguntaActual(): PreguntaRunner {
    return this.preguntas[this.indiceActual()];
  }

  totalAutocorregible(): number {
    return this.preguntas.filter((p) => this.esAutocorregible(p.tipo)).length;
  }

  todasAutocorregibles(): boolean {
    return this.preguntas.length > 0 && this.totalAutocorregible() === this.preguntas.length;
  }

  esAutocorregible(tipo: string | undefined): boolean {
    return tipo === 'alternativas' || tipo === 'verdadero_falso' || tipo === 'varias_correctas';
  }

  /** `varias_correctas` guarda la selección como lista JSON de textos de opción. */
  seleccion(valor: string | null | undefined): string[] {
    try {
      const datos = JSON.parse(valor || '[]');
      return Array.isArray(datos) ? datos.filter((x): x is string => typeof x === 'string') : [];
    } catch {
      return [];
    }
  }

  textoRespuesta(valor: string | null | undefined, tipo: string | undefined): string {
    const texto = tipo === 'varias_correctas' ? this.seleccion(valor).join('; ') : valor || '';
    // Marcadores visuales (::contar::🍎::9::, ::emoji::🍎::desc::) en texto plano legible.
    return texto
      .replace(/::contar::([^:]+)::(\d{1,2})::/g, (_m, e: string, n: string) => `${n} ${e}`)
      .replace(/::emoji::([^:\s]+)::([\s\S]+?)::/g, (_m, e: string, d: string) => `${e} ${d}`);
  }

  /** La opción trae un marcador visual que hay que dibujar (no mostrar como texto crudo). */
  tieneMarcadorVisual(op: string): boolean {
    return op.includes('::contar::') || op.includes('::emoji::');
  }

  estaMarcada(preguntaId: number, opcion: string): boolean {
    return this.seleccion(this.respuestas()[preguntaId]).includes(opcion);
  }

  alternarVarias(p: PreguntaRunner, opcion: string) {
    const actuales = new Set(this.seleccion(this.respuestas()[p.id]));
    actuales.has(opcion) ? actuales.delete(opcion) : actuales.add(opcion);
    const ordenadas = (p.opciones || []).filter((op) => actuales.has(op));
    this.responder(p.id, ordenadas.length ? JSON.stringify(ordenadas) : '');
  }

  etiquetaModo(): string {
    if (this.modo === 'examen') return 'Examen simulacro';
    if (this.modo === 'prueba') return 'Prueba de unidad';
    return 'Práctica libre';
  }

  esCorrectaEnAutoevaluacion(p: PreguntaRunner): boolean {
    if (p.tipo === 'varias_correctas') {
      const normalizar = (xs: string[]) => [...new Set(xs.map((x) => x.trim().toLowerCase()))].sort().join('\u0000');
      const dada = this.seleccion(this.respuestas()[p.id]);
      return dada.length > 0 && normalizar(dada) === normalizar(this.seleccion(p.respuesta_correcta));
    }
    const dada = (this.respuestas()[p.id] || '').trim().toLowerCase();
    return dada.length > 0 && this.esAutocorregible(p.tipo)
      && dada === (p.respuesta_correcta || '').trim().toLowerCase();
  }

  respuestaParaRevision(id: number): string | null | undefined {
    return this.respuestas()[id] ?? this.detalle().find(d => d.pregunta_id === id)?.respuesta_alumno;
  }

  revisarDesarrollo(id: number, estado: RevisionDesarrollo) {
    const tipo = this.preguntas.find(p => p.id === id)?.tipo ?? this.detalle().find(d => d.pregunta_id === id)?.tipo;
    if (!tipo || this.esAutocorregible(tipo) || !this.respuestaParaRevision(id)?.trim()) return;
    if (!this.enviada() && !this.ayudasReveladas().has(id)) return;
    this.revisionesDesarrollo.update(r => ({ ...r, [id]: estado }));
  }

  faltantes = computed(() => this.preguntas.filter((p) => !this.respuestas()[p.id]?.trim()));

  faltantesTexto(): string {
    const nums = this.faltantes().map((f) => this.preguntas.findIndex((p) => p.id === f.id) + 1);
    return nums.join(', ');
  }

  marcadasTexto(): string {
    const indices = this.preguntas
      .map((p, idx) => (this.marcadas().has(p.id) ? idx + 1 : null))
      .filter((idx): idx is number => idx !== null);
    return indices.join(', ');
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
    if (this.respuestas()[preguntaId] !== valor) {
      this.revisionesDesarrollo.update(r => {
        const actualizadas = { ...r };
        delete actualizadas[preguntaId];
        return actualizadas;
      });
    }
    this.respuestas.update((r) => ({ ...r, [preguntaId]: valor }));
    if (this.intentoId) {
      const intentoId = this.intentoId;
      // Los autosaves van en cola, uno tras otro: enviados en paralelo (varias casillas
      // seguidas, o la última respuesta y «Entregar» casi juntos) llegaban desordenados al
      // backend y uno podía pisar al otro (hallazgo E2E 2026-11-06).
      this.guardadosPendientes = this.guardadosPendientes.then(() =>
        firstValueFrom(this.evaluacionesService.responder(intentoId, preguntaId, valor)).then(
          () => undefined,
          () => undefined,
        ),
      );
    }
  }

  /** Cadena de autosaves en curso; `confirmarEnvio` espera a que termine antes de entregar. */
  private guardadosPendientes: Promise<void> = Promise.resolve();

  marcarRevisar(id: number) {
    this.marcadas.update((set) => {
      const nuevo = new Set(set);
      nuevo.has(id) ? nuevo.delete(id) : nuevo.add(id);
      return nuevo;
    });
  }

  solicitarAyuda(preguntaId: number) {
    this.ayudasReveladas.update((set) => new Set(set).add(preguntaId));
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
    if (this.faltantes().length > 0 || this.marcadas().size > 0) {
      this.mostrarAvisoIncompleto.set(true);
    } else {
      this.confirmarEnvio();
    }
  }

  irARevisarPendientes() {
    const primeraFaltante = this.preguntas.findIndex((p) => !this.respuestas()[p.id]?.trim());
    if (primeraFaltante !== -1) {
      this.indiceActual.set(primeraFaltante);
    } else {
      const primeraMarcada = this.preguntas.findIndex((p) => this.marcadas().has(p.id));
      if (primeraMarcada !== -1) {
        this.indiceActual.set(primeraMarcada);
      }
    }
    this.mostrarAvisoIncompleto.set(false);
  }

  confirmarEnvio() {
    this.mostrarAvisoIncompleto.set(false);
    if (this.cronometroId) clearInterval(this.cronometroId);

    if (this.intentoId && this.modo !== 'autoevaluacion') {
      this.cargando.set(true);
      const intentoId = this.intentoId;
      this.guardadosPendientes.then(() => this.evaluacionesService.entregar(intentoId).subscribe((intento) => {
        this.puntajeFinal.set(intento.puntaje);
        this.notaFinal.set(intento.nota);
        this.cargando.set(false);
        this.enviada.set(true);
        this.cargarDetalle();
      }));
    } else {
      this.enviada.set(true);
    }
  }

  volver() {
    if (this.cronometroId) clearInterval(this.cronometroId);
    this.router.navigate(this.rutaSalida);
  }
}
