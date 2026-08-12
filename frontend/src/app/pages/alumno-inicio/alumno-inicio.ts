import { Component } from '@angular/core';
import { RouterLink } from '@angular/router';
import { ASIGNATURAS_4_BASICO } from '../../core/mock-data/mock-data';
import { IconoAsignatura } from '../../shared/icono-asignatura/icono-asignatura';

@Component({
  selector: 'app-alumno-inicio',
  standalone: true,
  imports: [RouterLink, IconoAsignatura],
  template: `
    <h1>¡Hola de nuevo, Sofía! 👋</h1>
    <p class="subtitulo">Sigamos avanzando en tu preparación para 4° básico.</p>

    <div class="destacado tarjeta">
      <div>
        <span class="destacado__etiqueta">Continúa donde quedaste</span>
        <h3>Matemática — Adición y sustracción</h3>
        <p>Ibas a mitad de la unidad. ¡Vamos!</p>
      </div>
      <a routerLink="/alumno/asignaturas/matematica" class="btn btn--primario">Continuar</a>
    </div>

    <h2 class="seccion-titulo">Tus asignaturas</h2>
    <div class="grid-asignaturas">
      @for (asig of asignaturas; track asig.id) {
        <a class="asignatura-card tarjeta" [routerLink]="['/alumno/asignaturas', asig.id]">
          <app-icono-asignatura [icono]="asig.icono" [color]="asig.color" />
          <div class="asignatura-card__info">
            <h3>{{ asig.nombre }}</h3>
            <div class="barra-avance">
              <div class="barra-avance__relleno" [style.width.%]="asig.avance" [style.background]="asig.color"></div>
            </div>
            <small>{{ asig.avance }}% completado</small>
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
      .destacado {
        display: flex;
        justify-content: space-between;
        align-items: center;
        background: var(--color-primario-suave);
        margin-bottom: 2.5rem;
      }
      .destacado__etiqueta {
        font-size: 0.75rem;
        font-weight: 700;
        text-transform: uppercase;
        color: var(--color-primario);
        letter-spacing: 0.03em;
      }
      .destacado h3 {
        margin: 0.3rem 0;
      }
      .destacado p {
        margin: 0;
        color: var(--texto-secundario);
      }
      .seccion-titulo {
        font-size: 1.2rem;
        margin-bottom: 1rem;
      }
      .grid-asignaturas {
        display: grid;
        grid-template-columns: repeat(2, 1fr);
        gap: 1rem;
      }
      .asignatura-card {
        display: flex;
        gap: 1rem;
        align-items: center;
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
        font-size: 1rem;
        margin-bottom: 0.5rem;
      }
      .barra-avance {
        height: 6px;
        border-radius: 999px;
        background: var(--borde);
        overflow: hidden;
        margin-bottom: 0.3rem;
      }
      .barra-avance__relleno {
        height: 100%;
        border-radius: 999px;
      }
      .asignatura-card small {
        color: var(--texto-secundario);
      }
    `,
  ],
})
export class AlumnoInicio {
  asignaturas = ASIGNATURAS_4_BASICO;
}
