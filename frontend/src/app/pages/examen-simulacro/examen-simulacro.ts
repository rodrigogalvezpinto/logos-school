import { Component, Input } from '@angular/core';
import { EvaluacionRunner } from '../../shared/evaluacion-runner/evaluacion-runner';

@Component({
  selector: 'app-examen-simulacro',
  standalone: true,
  imports: [EvaluacionRunner],
  template: `
    <div class="examen-fondo">
      <div class="examen-marca">🔒 Examen simulacro · Sin pausas</div>
      <app-evaluacion-runner
        modo="examen"
        nombreEvaluacion="Examen integrado Forma A — 4° básico"
        [rutaSalida]="['/alumno/evaluaciones']"
      />
    </div>
  `,
  styleUrl: './examen-simulacro.scss',
})
export class ExamenSimulacro {
  @Input() id = '';
}
