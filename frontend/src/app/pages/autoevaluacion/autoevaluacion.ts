import { Component, Input, inject, signal } from '@angular/core';
import { RouterLink } from '@angular/router';
import { EvaluacionRunner, PreguntaRunner } from '../../shared/evaluacion-runner/evaluacion-runner';
import { EvaluacionesService } from '../../core/evaluaciones.service';
import { OnboardingService } from '../../core/onboarding.service';
import { PasosAprendizaje } from '../../shared/pasos-aprendizaje/pasos-aprendizaje';
import { SesionService } from '../../core/sesion.service';
import { ContenidoService } from '../../core/contenido.service';
import { MarkdownPipe } from '../../shared/markdown.pipe';

@Component({
  selector: 'app-autoevaluacion',
  standalone: true,
  imports: [EvaluacionRunner, PasosAprendizaje, RouterLink, MarkdownPipe],
  template: `
    @if (preguntas().length) {
      <a [routerLink]="['/alumno/estudiar', oaId]" class="volver-explicacion">← Volver a la explicación</a>
      <app-pasos-aprendizaje [paso]="2" />
      @if (guia()) {
        <!-- Muchas preguntas remiten al texto, poema, tabla o gráfico de la guía: se puede
             consultar aquí sin salir de la práctica (hallazgo de auditoría 2026-11-07). -->
        <details class="guia-consulta">
          <summary>📖 Ver la guía (textos, tablas y ejemplos)</summary>
          <div class="guia-consulta__contenido contenido-guia" [innerHTML]="guia() | markdown"></div>
        </details>
      }
      <app-evaluacion-runner
        modo="autoevaluacion"
        nombreEvaluacion="Práctica de este tema"
        [preguntas]="preguntas()"
        [rutaSalida]="['/alumno/asignaturas']"
      />
    } @else if (error()) {
      <p class="error-carga">{{ error() }}</p>
    } @else {
      <p>Cargando…</p>
    }
  `,
  styles: [
    `
      .error-carga {
        color: var(--color-error-texto);
      }
      .guia-consulta {
        margin-bottom: 1.25rem;
        border: 1px solid var(--borde, #ddd);
        border-radius: 12px;
        padding: 0.75rem 1rem;
        background: var(--superficie, transparent);
      }
      .guia-consulta summary {
        cursor: pointer;
        font-weight: 600;
      }
      .guia-consulta__contenido {
        max-height: 60vh;
        overflow-y: auto;
        margin-top: 0.75rem;
      }
      .volver-explicacion {
        display: inline-block;
        color: var(--texto-secundario);
        text-decoration: none;
        margin-bottom: 1.25rem;
        font-size: 0.9rem;
      }
    `,
  ],
})
export class Autoevaluacion {
  @Input() oaId = '';
  preguntas = signal<PreguntaRunner[]>([]);
  error = signal('');
  guia = signal('');

  private evaluaciones = inject(EvaluacionesService);
  private onboarding = inject(OnboardingService);
  private sesion = inject(SesionService);
  private contenido = inject(ContenidoService);

  ngOnInit() {
    this.evaluaciones.obtenerAutoevaluacion(Number(this.oaId)).subscribe({
      next: (preguntas) => this.preguntas.set(preguntas),
      error: () => this.error.set('No se pudo cargar la práctica. Intenta recargar la página.'),
    });

    this.contenido.obtenerObjetivo(Number(this.oaId)).subscribe({
      next: (oa) => this.guia.set(this.sinPreguntas(oa.contenido_guia ?? '')),
      error: () => this.guia.set(''),
    });

    const perfil = this.sesion.perfilActivo();
    if (perfil) {
      this.onboarding.completarPaso(perfil.id, 'autoevaluacion').subscribe();
    }
  }

  /** La guía incluye al final sus preguntas de autoevaluación con respuestas: se recortan
   * para que el panel de consulta no muestre las claves de la práctica en curso. */
  private sinPreguntas(md: string): string {
    const corte = md.search(/^#{2,5}\s*Preguntas de autoevaluaci[oó]n/im);
    return corte >= 0 ? md.slice(0, corte).trimEnd() : md;
  }
}
