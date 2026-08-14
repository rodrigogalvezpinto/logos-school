import { Component, Input, inject, signal } from '@angular/core';
import { EvaluacionRunner, PreguntaRunner } from '../../shared/evaluacion-runner/evaluacion-runner';
import { EvaluacionesService, ConjuntoDetalle } from '../../core/evaluaciones.service';
import { SesionService } from '../../core/sesion.service';

@Component({
  selector: 'app-examen-simulacro',
  standalone: true,
  imports: [EvaluacionRunner],
  template: `
    <div class="examen-fondo">
      <div class="examen-marca">🔒 Examen simulacro · Sin pausas</div>
      @if (conjunto() && intentoId()) {
        <app-evaluacion-runner
          modo="examen"
          [nombreEvaluacion]="conjunto()!.nombre"
          [preguntas]="preguntas()"
          [intentoId]="intentoId()"
          [resultadoPrevio]="resultadoPrevio()"
          [tiempoLimiteMin]="conjunto()!.tiempo_sugerido_min || 90"
          [rutaSalida]="['/alumno/evaluaciones']"
        />
      } @else if (error()) {
        <p class="error-carga">{{ error() }}</p>
      } @else {
        <p style="color: white; text-align:center;">Cargando…</p>
      }
    </div>
  `,
  styleUrl: './examen-simulacro.scss',
})
export class ExamenSimulacro {
  @Input() id = '';
  conjunto = signal<ConjuntoDetalle | null>(null);
  preguntas = signal<PreguntaRunner[]>([]);
  intentoId = signal<number | null>(null);
  resultadoPrevio = signal<{ puntaje: number | null; nota: number | null } | null>(null);
  error = signal('');

  private evaluaciones = inject(EvaluacionesService);
  private sesion = inject(SesionService);

  ngOnInit() {
    const perfil = this.sesion.perfilActivo();
    if (!perfil) return;

    this.evaluaciones.obtenerConjunto(Number(this.id), perfil.id).subscribe({
      next: (c) => {
        this.conjunto.set(c);
        this.preguntas.set(c.preguntas);
      },
      error: () => this.error.set('No se pudo cargar el examen. Intenta recargar la página.'),
    });
    this.evaluaciones.iniciarIntento(perfil.id, Number(this.id)).subscribe({
      next: (intento) => {
        this.intentoId.set(intento.id);
        if (intento.fecha_termino) {
          this.resultadoPrevio.set({ puntaje: intento.puntaje, nota: intento.nota });
        }
      },
      error: () => this.error.set('No se pudo iniciar tu intento. Intenta recargar la página.'),
    });
  }
}
