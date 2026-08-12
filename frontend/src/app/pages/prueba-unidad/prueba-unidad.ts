import { Component, Input } from '@angular/core';
import { EvaluacionRunner } from '../../shared/evaluacion-runner/evaluacion-runner';

@Component({
  selector: 'app-prueba-unidad',
  standalone: true,
  imports: [EvaluacionRunner],
  template: `<app-evaluacion-runner
    modo="prueba"
    nombreEvaluacion="Prueba de unidad — Números y Operaciones"
    [rutaSalida]="['/alumno/evaluaciones']"
  />`,
})
export class PruebaUnidad {
  @Input() id = '';
}
