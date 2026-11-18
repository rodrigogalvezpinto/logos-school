import { Component, OnDestroy, computed, inject, signal } from '@angular/core';
import { ContenidoService, AsignaturaRespuesta } from '../../core/contenido.service';
import { EvaluacionesService, PreguntaAutoevaluacion } from '../../core/evaluaciones.service';
import { SesionService } from '../../core/sesion.service';
import { MarkdownPipe } from '../../shared/markdown.pipe';
import { Emo } from '../../shared/emo';

/**
 * Juegos de práctica (Fase 2, 2026-11-18; diseño en planificacion/29-juegos-de-practica.md).
 * Usan el banco de autoevaluación de la asignatura, sin nota ni intento: es práctica con ritmo de juego.
 *  - Contrarreloj: responder la mayor cantidad de preguntas correctas en 90 segundos.
 *  - Racha: responder seguido hasta el primer error.
 * El mejor puntaje se guarda solo en este navegador (comodidad, no un registro oficial).
 */
export type ModoJuego = 'contrarreloj' | 'racha';
type Fase = 'eligiendo' | 'jugando' | 'fin';

export const SEGUNDOS_CONTRARRELOJ = 90;

/** Misma regla de corrección que la autoevaluación (evaluacion-runner). */
export function esRespuestaCorrecta(p: PreguntaAutoevaluacion, respuesta: string): boolean {
  const lista = (v: string) => {
    try {
      const d = JSON.parse(v || '[]');
      return Array.isArray(d) ? d.map((x) => String(x).trim().toLowerCase()) : [];
    } catch {
      return [];
    }
  };
  if (p.tipo === 'varias_correctas') {
    const a = [...new Set(lista(respuesta))].sort().join('\u0000');
    return a.length > 0 && a === [...new Set(lista(p.respuesta_correcta))].sort().join('\u0000');
  }
  return respuesta.trim().length > 0 && respuesta.trim().toLowerCase() === (p.respuesta_correcta || '').trim().toLowerCase();
}

@Component({
  selector: 'app-juegos',
  standalone: true,
  imports: [MarkdownPipe, Emo],
  template: `
    @if (fase() === 'eligiendo') {
      <h1>Juegos</h1>
      <p class="subtitulo">Practica con las preguntas de tus asignaturas, a otro ritmo. No hay nota: cada respuesta te muestra al tiro si acertaste y por qué.</p>

      <h2 class="paso">1. Elige el juego</h2>
      <div class="modos">
        <button type="button" class="modo" [class.modo--activo]="modo() === 'contrarreloj'" (click)="modo.set('contrarreloj')">
          <app-emo e="⏱" /> <strong>Contrarreloj</strong>
          <span>¿Cuántas aciertas en {{ segundosTotales }} segundos?</span>
        </button>
        <button type="button" class="modo" [class.modo--activo]="modo() === 'racha'" (click)="modo.set('racha')">
          <app-emo e="🔥" /> <strong>Racha</strong>
          <span>Responde seguido hasta el primer error.</span>
        </button>
      </div>

      <h2 class="paso">2. Elige la asignatura</h2>
      @if (error()) {
        <p class="error-carga">{{ error() }}</p>
      }
      <div class="asignaturas">
        @for (a of asignaturas(); track a.id) {
          <button type="button" class="asignatura" [disabled]="cargando()" (click)="comenzar(a)">
            <span class="asignatura__nombre">{{ a.nombre }}</span>
            <span class="asignatura__record">Mejor puntaje: {{ mejorPuntaje(a.id, modo()) }}</span>
          </button>
        }
      </div>
    }

    @if (fase() === 'jugando' && actual(); as p) {
      <div class="marcador">
        <span class="marcador__asig">{{ asignatura()?.nombre }} · {{ modo() === 'contrarreloj' ? 'Contrarreloj' : 'Racha' }}</span>
        <span class="marcador__puntos" aria-live="polite">Aciertos: <strong>{{ puntaje() }}</strong></span>
        @if (modo() === 'contrarreloj') {
          <span class="marcador__tiempo" [class.marcador__tiempo--poco]="segundosRestantes() <= 10">{{ segundosRestantes() }} s</span>
        }
      </div>

      <div class="tarjeta pregunta">
        <div class="pregunta__enunciado" [innerHTML]="p.enunciado | markdown"></div>
        @if (p.tipo === 'varias_correctas') {
          <p class="pregunta__nota">Marca todas las correctas.</p>
        }
        <div class="opciones">
          @for (op of opcionesDe(p); track op) {
            <button
              type="button"
              class="opcion"
              [class.opcion--marcada]="marcadas().has(op)"
              [class.opcion--correcta]="respondida() && esOpcionCorrecta(p, op)"
              [class.opcion--incorrecta]="respondida() && marcadas().has(op) && !esOpcionCorrecta(p, op)"
              [disabled]="respondida()"
              [attr.aria-pressed]="marcadas().has(op)"
              (click)="elegir(p, op)"
            >
              <span [innerHTML]="op | markdown"></span>
            </button>
          }
        </div>
        @if (p.tipo === 'varias_correctas' && !respondida()) {
          <button type="button" class="btn btn--primario" [disabled]="marcadas().size === 0" (click)="confirmarVarias(p)">Responder</button>
        }
        @if (respondida()) {
          <div class="retro" [class.retro--bien]="acerto()" role="status">
            <p class="retro__titulo">{{ acerto() ? '¡Correcto!' : 'No era esa.' }}</p>
            <div [innerHTML]="p.retroalimentacion | markdown"></div>
          </div>
          <button type="button" class="btn btn--primario" (click)="siguiente()">{{ terminaAlSeguir() ? 'Ver resultado' : 'Siguiente' }}</button>
        }
      </div>
    }

    @if (fase() === 'fin') {
      <div class="tarjeta fin">
        <h1>{{ puntaje() }} {{ puntaje() === 1 ? 'acierto' : 'aciertos' }}</h1>
        <p>{{ asignatura()?.nombre }} · {{ modo() === 'contrarreloj' ? 'Contrarreloj' : 'Racha' }}</p>
        @if (nuevoRecord()) {
          <p class="fin__record"><app-emo e="🏆" /> ¡Nuevo mejor puntaje!</p>
        } @else {
          <p>Tu mejor puntaje: {{ mejorPuntaje(asignatura()!.id, modo()) }}</p>
        }
        <div class="fin__acciones">
          <button type="button" class="btn btn--primario" (click)="comenzar(asignatura()!)">Jugar otra vez</button>
          <button type="button" class="btn" (click)="volverAElegir()">Elegir otro juego</button>
        </div>
      </div>
    }
  `,
  styles: [
    `
      .subtitulo { color: var(--texto-secundario); margin-bottom: 1.5rem; }
      .paso { font-size: 1.05rem; margin: 1.25rem 0 0.75rem; }
      .modos, .asignaturas { display: grid; grid-template-columns: repeat(auto-fill, minmax(220px, 1fr)); gap: 0.75rem; }
      .modo, .asignatura {
        display: flex; flex-direction: column; gap: 0.35rem; align-items: flex-start; text-align: left;
        padding: 1rem; border-radius: 14px; border: 2px solid var(--borde, #E5E7EB); background: var(--superficie, #fff);
        cursor: pointer; font: inherit; color: inherit;
      }
      .modo span, .asignatura__record { color: var(--texto-secundario); font-size: 0.9rem; }
      .modo--activo { border-color: var(--color-primario); box-shadow: 0 0 0 3px rgba(91, 79, 233, 0.15); }
      .asignatura:hover:not(:disabled) { border-color: var(--color-primario); }
      .asignatura__nombre { font-weight: 600; }
      .marcador { display: flex; flex-wrap: wrap; gap: 1rem; align-items: center; justify-content: space-between; margin-bottom: 1rem; }
      .marcador__asig { color: var(--texto-secundario); }
      .marcador__tiempo { font-weight: 700; font-variant-numeric: tabular-nums; font-size: 1.2rem; }
      .marcador__tiempo--poco { color: var(--color-error-texto, #B91C1C); }
      .pregunta { padding: 1.25rem; }
      .pregunta__nota { color: var(--texto-secundario); font-size: 0.9rem; }
      .opciones { display: grid; gap: 0.5rem; margin: 1rem 0; }
      .opcion {
        text-align: left; padding: 0.75rem 1rem; border-radius: 10px; border: 2px solid var(--borde, #E5E7EB);
        background: var(--superficie, #fff); cursor: pointer; font: inherit; color: inherit;
      }
      .opcion--marcada { border-color: var(--color-primario); }
      .opcion--correcta { border-color: #059669; background: #ECFDF5; }
      .opcion--incorrecta { border-color: #DC2626; background: #FEF2F2; }
      .opcion:disabled { cursor: default; }
      .retro { border-left: 4px solid #DC2626; background: #FEF2F2; padding: 0.75rem 1rem; border-radius: 8px; margin-bottom: 1rem; }
      .retro--bien { border-left-color: #059669; background: #ECFDF5; }
      .retro__titulo { font-weight: 700; margin: 0 0 0.25rem; }
      .fin { text-align: center; padding: 2rem; }
      .fin__record { font-weight: 700; color: var(--color-primario-texto, #4338CA); }
      .fin__acciones { display: flex; gap: 0.75rem; justify-content: center; flex-wrap: wrap; margin-top: 1rem; }
    `,
  ],
})
export class Juegos implements OnDestroy {
  private contenido = inject(ContenidoService);
  private evaluaciones = inject(EvaluacionesService);
  private sesion = inject(SesionService);

  readonly segundosTotales = SEGUNDOS_CONTRARRELOJ;
  asignaturas = signal<AsignaturaRespuesta[]>([]);
  error = signal('');
  cargando = signal(false);
  modo = signal<ModoJuego>('contrarreloj');
  fase = signal<Fase>('eligiendo');
  asignatura = signal<AsignaturaRespuesta | null>(null);
  preguntas = signal<PreguntaAutoevaluacion[]>([]);
  indice = signal(0);
  puntaje = signal(0);
  marcadas = signal<Set<string>>(new Set());
  respondida = signal(false);
  acerto = signal(false);
  segundosRestantes = signal(SEGUNDOS_CONTRARRELOJ);
  nuevoRecord = signal(false);
  actual = computed(() => this.preguntas()[this.indice()]);
  private reloj?: ReturnType<typeof setInterval>;

  constructor() {
    const perfil = this.sesion.perfilActivo();
    if (perfil) {
      this.contenido.listarAsignaturas(perfil.nivel_id).subscribe({
        next: (a) => this.asignaturas.set(a),
        error: () => this.error.set('No se pudieron cargar tus asignaturas. Intenta recargar la página.'),
      });
    }
  }

  ngOnDestroy() {
    this.detenerReloj();
  }

  opcionesDe(p: PreguntaAutoevaluacion): string[] {
    return p.tipo === 'verdadero_falso' && !p.opciones?.length ? ['Verdadero', 'Falso'] : p.opciones ?? [];
  }

  esOpcionCorrecta(p: PreguntaAutoevaluacion, op: string): boolean {
    if (p.tipo === 'varias_correctas') return this.listaCorrecta(p).includes(op.trim().toLowerCase());
    return op.trim().toLowerCase() === (p.respuesta_correcta || '').trim().toLowerCase();
  }

  private listaCorrecta(p: PreguntaAutoevaluacion): string[] {
    try {
      return (JSON.parse(p.respuesta_correcta || '[]') as string[]).map((x) => x.trim().toLowerCase());
    } catch {
      return [];
    }
  }

  comenzar(a: AsignaturaRespuesta) {
    this.cargando.set(true);
    this.error.set('');
    this.evaluaciones.obtenerPreguntasJuego(a.id).subscribe({
      next: (ps) => {
        this.cargando.set(false);
        this.asignatura.set(a);
        this.preguntas.set(ps);
        this.indice.set(0);
        this.puntaje.set(0);
        this.nuevoRecord.set(false);
        this.limpiarRespuesta();
        this.fase.set('jugando');
        if (this.modo() === 'contrarreloj') this.iniciarReloj();
      },
      error: () => {
        this.cargando.set(false);
        this.error.set('Esta asignatura todavía no tiene preguntas para jugar.');
      },
    });
  }

  elegir(p: PreguntaAutoevaluacion, op: string) {
    if (this.respondida()) return;
    if (p.tipo === 'varias_correctas') {
      const s = new Set(this.marcadas());
      s.has(op) ? s.delete(op) : s.add(op);
      this.marcadas.set(s);
      return;
    }
    this.marcadas.set(new Set([op]));
    this.registrar(esRespuestaCorrecta(p, op));
  }

  confirmarVarias(p: PreguntaAutoevaluacion) {
    const elegidas = (p.opciones ?? []).filter((o) => this.marcadas().has(o));
    this.registrar(esRespuestaCorrecta(p, JSON.stringify(elegidas)));
  }

  /** En «Racha», un error termina el juego; en «Contrarreloj», también se acaba si no quedan preguntas. */
  terminaAlSeguir(): boolean {
    return (this.modo() === 'racha' && !this.acerto()) || this.indice() + 1 >= this.preguntas().length;
  }

  siguiente() {
    if (this.terminaAlSeguir()) return this.terminar();
    this.indice.update((i) => i + 1);
    this.limpiarRespuesta();
  }

  volverAElegir() {
    this.detenerReloj();
    this.fase.set('eligiendo');
  }

  mejorPuntaje(asignaturaId: number, modo: ModoJuego): number {
    try {
      return Number(localStorage.getItem(this.claveRecord(asignaturaId, modo)) ?? 0) || 0;
    } catch {
      return 0;
    }
  }

  private registrar(correcta: boolean) {
    this.respondida.set(true);
    this.acerto.set(correcta);
    if (correcta) this.puntaje.update((n) => n + 1);
  }

  private limpiarRespuesta() {
    this.marcadas.set(new Set());
    this.respondida.set(false);
    this.acerto.set(false);
  }

  private iniciarReloj() {
    this.detenerReloj();
    // Contra una hora de término fija: los navegadores frenan los temporizadores en segundo plano.
    const fin = Date.now() + SEGUNDOS_CONTRARRELOJ * 1000;
    this.segundosRestantes.set(SEGUNDOS_CONTRARRELOJ);
    this.reloj = setInterval(() => {
      this.segundosRestantes.set(Math.max(0, Math.ceil((fin - Date.now()) / 1000)));
      if (this.segundosRestantes() === 0) this.terminar();
    }, 250);
  }

  private detenerReloj() {
    if (this.reloj) clearInterval(this.reloj);
    this.reloj = undefined;
  }

  private terminar() {
    this.detenerReloj();
    const a = this.asignatura();
    if (a) {
      const previo = this.mejorPuntaje(a.id, this.modo());
      if (this.puntaje() > previo) {
        this.nuevoRecord.set(true);
        try {
          localStorage.setItem(this.claveRecord(a.id, this.modo()), String(this.puntaje()));
        } catch {
          /* sin almacenamiento local: el juego funciona igual, solo no recuerda el récord */
        }
      }
    }
    this.fase.set('fin');
  }

  private claveRecord(asignaturaId: number, modo: ModoJuego): string {
    const perfil = this.sesion.perfilActivo();
    return `logos-juego-${perfil?.id ?? 'x'}-${asignaturaId}-${modo}`;
  }
}
