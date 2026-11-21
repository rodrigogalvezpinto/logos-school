import { Component, inject, input, signal } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { HttpErrorResponse } from '@angular/common/http';
import { MensajeTutor, TutorIaService } from '../../core/tutor-ia.service';
import { SesionService } from '../../core/sesion.service';
import { MarkdownPipe } from '../markdown.pipe';
import { Emo } from '../emo';

/** Panel «Pregúntale al Profesor IA» bajo la guía del OA. No se muestra si el backend lo tiene desactivado. */
@Component({
  selector: 'app-tutor-ia',
  standalone: true,
  imports: [FormsModule, MarkdownPipe, Emo],
  template: `
    @if (habilitado()) {
      <section class="tarjeta tutor" aria-labelledby="titulo-tutor">
        <h2 id="titulo-tutor"><app-emo e="🤖" /> Pregúntale al Profesor IA</h2>
        <p class="tutor__aviso">
          Es un tutor con inteligencia artificial: te da pistas sobre esta guía y puede equivocarse.
          <strong>No escribas tu nombre, RUT, dirección ni otros datos personales.</strong>
        </p>
        <div class="tutor__mensajes" aria-live="polite">
          @for (m of mensajes(); track $index) {
            <div class="burbuja" [class.burbuja--alumno]="m.rol === 'alumno'" [class.burbuja--ayuda]="m.derivacion">
              <div [innerHTML]="m.texto | markdown"></div>
            </div>
          }
          @if (pensando()) {
            <div class="burbuja burbuja--pensando">Pensando…</div>
          }
        </div>
        @if (error()) {
          <p class="tutor__error" role="alert">{{ error() }}</p>
        }
        <form class="tutor__form" (submit)="$event.preventDefault(); enviar()">
          <label class="visualmente-oculto" for="pregunta-tutor">Tu pregunta</label>
          <textarea id="pregunta-tutor" name="pregunta" rows="2" maxlength="800" [(ngModel)]="texto"
            placeholder="Por ejemplo: no entiendo el ejemplo 2, ¿me das una pista?"></textarea>
          <button type="submit" class="btn btn--primario" [disabled]="pensando() || !texto.trim()">Preguntar</button>
        </form>
      </section>
    }
  `,
  styles: [
    `
      .tutor { padding: 1.25rem; margin-top: 1.5rem; }
      .tutor h2 { font-size: 1.15rem; margin: 0 0 0.5rem; display: flex; gap: 0.4rem; align-items: center; }
      .tutor__aviso { color: var(--texto-secundario); font-size: 0.88rem; }
      .tutor__mensajes { display: flex; flex-direction: column; gap: 0.5rem; margin: 1rem 0; }
      .burbuja { max-width: 85%; padding: 0.6rem 0.9rem; border-radius: 12px; background: var(--superficie-suave, #F3F4F6); }
      .burbuja--alumno { align-self: flex-end; background: #EEF2FF; }
      .burbuja--ayuda { background: #FEF3C7; border: 1px solid #F59E0B; }
      .burbuja--pensando { color: var(--texto-secundario); font-style: italic; }
      .tutor__error { color: var(--color-error-texto, #B91C1C); font-size: 0.9rem; }
      .tutor__form { display: flex; gap: 0.5rem; align-items: flex-end; }
      .tutor__form textarea { flex: 1; font: inherit; padding: 0.6rem; border-radius: 10px; border: 1px solid var(--borde, #D1D5DB); resize: vertical; }
      .visualmente-oculto { position: absolute; width: 1px; height: 1px; overflow: hidden; clip: rect(0 0 0 0); }
    `,
  ],
})
export class TutorIa {
  readonly oaId = input.required<number>();
  private servicio = inject(TutorIaService);
  private sesion = inject(SesionService);
  habilitado = signal(false);
  mensajes = signal<MensajeTutor[]>([]);
  pensando = signal(false);
  error = signal('');
  texto = '';

  constructor() {
    this.servicio.estado().subscribe({ next: (e) => this.habilitado.set(e.habilitado), error: () => this.habilitado.set(false) });
  }

  enviar() {
    const perfil = this.sesion.perfilActivo();
    const texto = this.texto.trim();
    if (!perfil || !texto || this.pensando()) return;
    this.error.set('');
    const historial = [...this.mensajes(), { rol: 'alumno' as const, texto }];
    this.mensajes.set(historial);
    this.texto = '';
    this.pensando.set(true);
    this.servicio.preguntar(perfil.id, this.oaId(), historial.filter((m) => !m.derivacion)).subscribe({
      next: (r) => {
        this.pensando.set(false);
        this.mensajes.update((ms) => [...ms, { rol: 'tutor', texto: r.texto, derivacion: r.derivacion }]);
      },
      error: (e: HttpErrorResponse) => {
        this.pensando.set(false);
        this.error.set(e.error?.detail ?? 'El Profesor IA no pudo responder ahora. Intenta en unos minutos.');
      },
    });
  }
}
