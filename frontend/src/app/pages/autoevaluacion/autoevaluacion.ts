import { Component, Input, inject, signal } from '@angular/core';
import { RouterLink } from '@angular/router';
import { EvaluacionRunner, PreguntaRunner } from '../../shared/evaluacion-runner/evaluacion-runner';
import { EvaluacionesService } from '../../core/evaluaciones.service';
import { OnboardingService } from '../../core/onboarding.service';
import { PasosAprendizaje } from '../../shared/pasos-aprendizaje/pasos-aprendizaje';
import { SesionService } from '../../core/sesion.service';

@Component({
  selector: 'app-autoevaluacion',
  standalone: true,
  imports: [EvaluacionRunner, PasosAprendizaje, RouterLink],
  template: `
    @if (preguntas().length) {
      <a [routerLink]="['/alumno/estudiar', oaId]" class="volver-explicacion">← Volver a la explicación</a>
      <app-pasos-aprendizaje [paso]="2" />
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

  private evaluaciones = inject(EvaluacionesService);
  private onboarding = inject(OnboardingService);
  private sesion = inject(SesionService);

  ngOnInit() {
    this.evaluaciones.obtenerAutoevaluacion(Number(this.oaId)).subscribe({
      next: (preguntas) => this.preguntas.set(preguntas),
      error: () => this.error.set('No se pudo cargar la práctica. Intenta recargar la página.'),
    });

    const perfil = this.sesion.perfilActivo();
    if (perfil) {
      this.onboarding.completarPaso(perfil.id, 'autoevaluacion').subscribe();
    }
  }
}
