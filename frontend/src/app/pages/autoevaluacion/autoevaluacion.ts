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
    } @else {
      <p>Cargando…</p>
    }
  `,
})
export class Autoevaluacion {
  @Input() oaId = '';
  preguntas = signal<PreguntaRunner[]>([]);

  private evaluaciones = inject(EvaluacionesService);

  ngOnInit() {
    this.evaluaciones.obtenerAutoevaluacion(Number(this.oaId)).subscribe((preguntas) => this.preguntas.set(preguntas));
  }
}
