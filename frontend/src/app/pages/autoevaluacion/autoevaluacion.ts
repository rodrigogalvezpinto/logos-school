import { Component, Input, inject, signal } from '@angular/core';
import { EvaluacionRunner, PreguntaRunner } from '../../shared/evaluacion-runner/evaluacion-runner';
import { EvaluacionesService } from '../../core/evaluaciones.service';

@Component({
  selector: 'app-autoevaluacion',
  standalone: true,
  imports: [EvaluacionRunner],
  template: `
    @if (preguntas().length) {
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
  styles: [`.error-carga { color: var(--color-error); }`],
})
export class Autoevaluacion {
  @Input() oaId = '';
  preguntas = signal<PreguntaRunner[]>([]);
  error = signal('');

  private evaluaciones = inject(EvaluacionesService);

  ngOnInit() {
    this.evaluaciones.obtenerAutoevaluacion(Number(this.oaId)).subscribe({
      next: (preguntas) => this.preguntas.set(preguntas),
      error: () => this.error.set('No se pudo cargar la práctica. Intenta recargar la página.'),
    });
  }
}
