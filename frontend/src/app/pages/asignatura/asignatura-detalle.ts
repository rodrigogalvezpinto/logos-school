import { Component, Input, inject, signal } from '@angular/core';
import { RouterLink } from '@angular/router';
import { ContenidoService, ObjetivoRespuesta } from '../../core/contenido.service';
import { IconoAsignatura } from '../../shared/icono-asignatura/icono-asignatura';

@Component({
  selector: 'app-asignatura-detalle',
  standalone: true,
  imports: [RouterLink, IconoAsignatura],
  template: `
    <div class="cabecera">
      <app-icono-asignatura icono="libro" color="#5B4FE9" />
      <div>
        <h1>Objetivos de Aprendizaje</h1>
        <p>{{ objetivos().length }} OA en esta asignatura</p>
      </div>
    </div>

    @if (error()) {
      <p class="error-carga">{{ error() }}</p>
    }
    <div class="lista-oa">
      @for (oa of objetivos(); track oa.id) {
        <div class="oa-card tarjeta">
          <div class="oa-card__info">
            <span class="oa-card__codigo">{{ oa.codigo_oficial }}</span>
            <h3>{{ oa.descripcion }}</h3>
          </div>
          <div class="oa-card__acciones">
            <a class="btn btn--secundario" [routerLink]="['/alumno/estudiar', oa.id]">Estudiar guía</a>
            <a class="btn btn--primario" [routerLink]="['/alumno/autoevaluacion', oa.id]">Practicar</a>
          </div>
        </div>
      }
    </div>

    <a class="btn btn--secundario" [routerLink]="['/alumno/evaluaciones']" [queryParams]="{ asignatura: id }">
      Ver pruebas y exámenes de esta asignatura →
    </a>
  `,
  styles: [
    `
      .cabecera {
        display: flex;
        align-items: center;
        gap: 1rem;
        margin-bottom: 2rem;

        h1 {
          margin: 0;
        }
        p {
          margin: 0.2rem 0 0;
          color: var(--texto-secundario);
        }
      }
      .lista-oa {
        display: flex;
        flex-direction: column;
        gap: 1rem;
        margin-bottom: 1.5rem;
      }
      .oa-card {
        display: flex;
        align-items: center;
        gap: 1.25rem;
      }
      .oa-card__info {
        flex: 1;
      }
      .oa-card__codigo {
        font-size: 0.75rem;
        font-weight: 700;
        color: var(--color-primario);
        text-transform: uppercase;
      }
      .oa-card__info h3 {
        margin: 0.2rem 0 0;
        font-size: 1.05rem;
      }
      .oa-card__acciones {
        display: flex;
        gap: 0.5rem;
        flex-shrink: 0;
      }
      @media (max-width: 700px) {
        .oa-card {
          flex-direction: column;
          align-items: flex-start;
        }
      }
      .error-carga {
        color: var(--color-error);
      }
    `,
  ],
})
export class AsignaturaDetalle {
  @Input() id = '';
  objetivos = signal<ObjetivoRespuesta[]>([]);
  error = signal('');

  private contenido = inject(ContenidoService);

  ngOnInit() {
    this.contenido.listarObjetivos(Number(this.id)).subscribe({
      next: (objs) => this.objetivos.set(objs),
      error: () => this.error.set('No se pudieron cargar los objetivos de esta asignatura. Intenta recargar la página.'),
    });
  }
}
