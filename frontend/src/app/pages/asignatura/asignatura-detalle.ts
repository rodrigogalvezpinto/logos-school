import { Component, Input } from '@angular/core';
import { RouterLink } from '@angular/router';
import { ASIGNATURAS_4_BASICO } from '../../core/mock-data/mock-data';
import { IconoAsignatura } from '../../shared/icono-asignatura/icono-asignatura';

@Component({
  selector: 'app-asignatura-detalle',
  standalone: true,
  imports: [RouterLink, IconoAsignatura],
  template: `
    @if (asignatura) {
      <div class="cabecera">
        <app-icono-asignatura [icono]="asignatura.icono" [color]="asignatura.color" />
        <div>
          <h1>{{ asignatura.nombre }}</h1>
          <p>{{ asignatura.avance }}% del temario completado</p>
        </div>
      </div>

      <div class="lista-oa">
        @for (oa of asignatura.objetivos; track oa.id) {
          <div class="oa-card tarjeta">
            <div class="oa-card__estado" [class]="'estado--' + oa.estado"></div>
            <div class="oa-card__info">
              <span class="oa-card__codigo">{{ oa.codigo }}</span>
              <h3>{{ oa.titulo }}</h3>
              <p>{{ oa.resumen }}</p>
            </div>
            <div class="oa-card__acciones">
              <a class="btn btn--secundario" [routerLink]="['/alumno/estudiar', oa.id]">Estudiar guía</a>
              <a class="btn btn--primario" [routerLink]="['/alumno/autoevaluacion', oa.id]">Practicar</a>
            </div>
          </div>
        }
      </div>
    }
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
      }
      .oa-card {
        display: flex;
        align-items: center;
        gap: 1.25rem;
      }
      .oa-card__estado {
        width: 12px;
        height: 12px;
        border-radius: 50%;
        flex-shrink: 0;
      }
      .estado--dominado {
        background: var(--color-exito);
      }
      .estado--en_progreso {
        background: var(--color-alerta);
      }
      .estado--no_iniciado {
        background: var(--borde);
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
        margin: 0.2rem 0 0.25rem;
        font-size: 1.05rem;
      }
      .oa-card__info p {
        margin: 0;
        color: var(--texto-secundario);
        font-size: 0.9rem;
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
    `,
  ],
})
export class AsignaturaDetalle {
  @Input() id = '';

  get asignatura() {
    return ASIGNATURAS_4_BASICO.find((a) => a.id === this.id) ?? ASIGNATURAS_4_BASICO[0];
  }
}
