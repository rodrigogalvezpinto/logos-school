import { Component } from '@angular/core';
import { RouterLink } from '@angular/router';
import { ASIGNATURAS_4_BASICO } from '../../core/mock-data/mock-data';
import { IconoAsignatura } from '../../shared/icono-asignatura/icono-asignatura';

@Component({
  selector: 'app-asignaturas-lista',
  standalone: true,
  imports: [RouterLink, IconoAsignatura],
  template: `
    <h1>Mis Asignaturas — 4° básico</h1>
    <p class="subtitulo">El temario oficial completo, organizado por Objetivo de Aprendizaje.</p>

    <div class="grid-asignaturas">
      @for (asig of asignaturas; track asig.id) {
        <a class="asignatura-card tarjeta" [routerLink]="['/alumno/asignaturas', asig.id]">
          <app-icono-asignatura [icono]="asig.icono" [color]="asig.color" />
          <div class="asignatura-card__info">
            <h3>{{ asig.nombre }}</h3>
            <p>{{ asig.objetivos.length }} objetivos de aprendizaje</p>
            <div class="barra-avance">
              <div class="barra-avance__relleno" [style.width.%]="asig.avance" [style.background]="asig.color"></div>
            </div>
          </div>
        </a>
      }
    </div>
  `,
  styles: [
    `
      .subtitulo {
        color: var(--texto-secundario);
        margin-top: -0.5rem;
        margin-bottom: 2rem;
      }
      .grid-asignaturas {
        display: grid;
        grid-template-columns: repeat(2, 1fr);
        gap: 1rem;
      }
      .asignatura-card {
        display: flex;
        gap: 1rem;
        text-decoration: none;
        color: inherit;
        transition: transform 0.15s;
      }
      .asignatura-card:hover {
        transform: translateY(-2px);
      }
      .asignatura-card__info {
        flex: 1;
      }
      .asignatura-card h3 {
        margin: 0 0 0.25rem;
        font-size: 1.05rem;
      }
      .asignatura-card p {
        margin: 0 0 0.5rem;
        color: var(--texto-secundario);
        font-size: 0.85rem;
      }
      .barra-avance {
        height: 6px;
        border-radius: 999px;
        background: var(--borde);
        overflow: hidden;
      }
      .barra-avance__relleno {
        height: 100%;
        border-radius: 999px;
      }
    `,
  ],
})
export class AsignaturasLista {
  asignaturas = ASIGNATURAS_4_BASICO;
}
