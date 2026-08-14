import { Component, inject, signal } from '@angular/core';
import { RouterLink } from '@angular/router';
import { forkJoin } from 'rxjs';
import { ContenidoService, AsignaturaRespuesta } from '../../core/contenido.service';
import { EvaluacionesService, ConjuntoResumen } from '../../core/evaluaciones.service';
import { SesionService } from '../../core/sesion.service';

interface GrupoAsignatura {
  asignatura: AsignaturaRespuesta;
  pruebas: ConjuntoResumen[];
  examenes: ConjuntoResumen[];
}

@Component({
  selector: 'app-evaluaciones',
  standalone: true,
  imports: [RouterLink],
  template: `
    <h1>Pruebas y Exámenes</h1>
    <p class="subtitulo">Todo lo que puedes rendir, agrupado por asignatura.</p>

    @if (error()) {
      <p class="error-carga">{{ error() }}</p>
    }
    @for (grupo of grupos(); track grupo.asignatura.id) {
      <div class="grupo">
        <h2>{{ grupo.asignatura.nombre }}</h2>
        @for (prueba of grupo.pruebas; track prueba.id) {
          <div class="fila tarjeta">
            <div>
              <h3>{{ prueba.nombre }}</h3>
              <p>Prueba de unidad · {{ prueba.num_preguntas }} preguntas · sin tiempo límite</p>
            </div>
            <a [routerLink]="['/alumno/prueba', prueba.id]" class="btn btn--secundario">Rendir</a>
          </div>
        }
        @for (examen of grupo.examenes; track examen.id) {
          <div class="fila fila--examen tarjeta">
            <div>
              <h3>{{ examen.nombre }}</h3>
              <p>{{ examen.num_preguntas }} preguntas · {{ examen.tiempo_sugerido_min }} minutos · imita el examen real</p>
            </div>
            <a [routerLink]="['/examen', examen.id]" class="btn btn--primario">Comenzar examen</a>
          </div>
        }
      </div>
    }

    @if (examenIntegrado(); as ei) {
      <div class="grupo">
        <h2>Examen simulacro</h2>
        <div class="fila fila--examen tarjeta">
          <div>
            <h3>{{ ei.nombre }}</h3>
            <p>{{ ei.num_preguntas }} preguntas · {{ ei.tiempo_sugerido_min }} minutos · imita el examen real</p>
          </div>
          <a [routerLink]="['/examen', ei.id]" class="btn btn--primario">Comenzar examen</a>
        </div>
      </div>
    }
  `,
  styles: [
    `
      .subtitulo {
        color: var(--texto-secundario);
        margin-top: -0.5rem;
        margin-bottom: 2rem;
      }
      .grupo {
        margin-bottom: 2rem;
      }
      .grupo h2 {
        font-size: 1.05rem;
        margin-bottom: 0.75rem;
      }
      .fila {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 0.75rem;

        h3 {
          margin: 0 0 0.2rem;
          font-size: 1rem;
        }
        p {
          margin: 0;
          color: var(--texto-secundario);
          font-size: 0.85rem;
        }
      }
      .fila--examen {
        border: 1.5px solid var(--color-primario);
      }
      .error-carga {
        color: var(--color-error);
      }
    `,
  ],
})
export class Evaluaciones {
  grupos = signal<GrupoAsignatura[]>([]);
  examenIntegrado = signal<ConjuntoResumen | null>(null);
  error = signal('');

  private contenido = inject(ContenidoService);
  private evaluaciones = inject(EvaluacionesService);
  private sesion = inject(SesionService);

  constructor() {
    const perfil = this.sesion.perfilActivo();
    if (!perfil) return;

    this.contenido.listarAsignaturas(perfil.nivel_id).subscribe({
      next: (asignaturas) => {
        const llamadas = asignaturas.map((a) => this.evaluaciones.listarConjuntosDeAsignatura(a.id));
        forkJoin(llamadas).subscribe({
          next: (listas) => {
            this.grupos.set(
              asignaturas.map((asignatura, i) => ({
                asignatura,
                pruebas: listas[i].filter((c) => c.tipo === 'prueba_unidad'),
                examenes: listas[i].filter((c) => c.tipo === 'examen_simulacro'),
              }))
            );
          },
          error: () => this.error.set('No se pudieron cargar tus pruebas y exámenes. Intenta recargar la página.'),
        });
      },
      error: () => this.error.set('No se pudieron cargar tus pruebas y exámenes. Intenta recargar la página.'),
    });

    this.evaluaciones.listarConjuntosDeNivel(perfil.nivel_id).subscribe({
      next: (conjuntos) => {
        if (conjuntos.length) this.examenIntegrado.set(conjuntos[0]);
      },
      error: () => this.error.set('No se pudieron cargar tus pruebas y exámenes. Intenta recargar la página.'),
    });
  }
}
