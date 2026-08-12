import { Component, Input } from '@angular/core';
import { EvaluacionRunner } from '../../shared/evaluacion-runner/evaluacion-runner';

@Component({
  selector: 'app-autoevaluacion',
  standalone: true,
  imports: [EvaluacionRunner],
  template: `<app-evaluacion-runner
    modo="autoevaluacion"
    nombreEvaluacion="Práctica — Números y Operaciones"
    [rutaSalida]="['/alumno/asignaturas', 'matematica']"
  />`,
})
export class Autoevaluacion {
  @Input() oaId = '';
}
