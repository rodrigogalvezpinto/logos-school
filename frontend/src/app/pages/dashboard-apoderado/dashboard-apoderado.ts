import { Component } from '@angular/core';
import { RouterLink } from '@angular/router';

@Component({
  selector: 'app-dashboard-apoderado',
  standalone: true,
  imports: [RouterLink],
  template: `
    <h1>Hola, Rodrigo 👋</h1>
    <p class="subtitulo">Así va tu familia en Logos.</p>

    <div class="grid">
      <div class="tarjeta alumno-card">
        <div class="alumno-card__avatar">S</div>
        <div class="alumno-card__info">
          <h3>Sofía</h3>
          <p>4° básico</p>
          <span class="chip chip--activo">Plan activo · Por periodo</span>
        </div>
        <a routerLink="/apoderado/progreso" class="btn btn--secundario">Ver progreso</a>
      </div>

      <a routerLink="/apoderado/alumnos" class="tarjeta agregar-card">
        <span class="agregar-card__mas">+</span>
        <span>Agregar otro alumno</span>
      </a>
    </div>
  `,
  styles: [
    `
      .subtitulo {
        color: var(--texto-secundario);
        margin-top: -0.5rem;
        margin-bottom: 2rem;
      }
      .grid {
        display: grid;
        grid-template-columns: repeat(2, 1fr);
        gap: 1rem;
        max-width: 760px;
      }
      .alumno-card {
        display: flex;
        align-items: center;
        gap: 1rem;
      }
      .alumno-card__avatar {
        width: 52px;
        height: 52px;
        border-radius: var(--radio-media);
        background: var(--color-primario);
        color: white;
        display: flex;
        align-items: center;
        justify-content: center;
        font-family: var(--fuente-titulos);
        font-weight: 700;
        font-size: 1.3rem;
        flex-shrink: 0;
      }
      .alumno-card__info {
        flex: 1;

        h3 {
          margin: 0 0 0.15rem;
        }
        p {
          margin: 0 0 0.5rem;
          color: var(--texto-secundario);
          font-size: 0.9rem;
        }
      }
      .chip {
        display: inline-block;
        font-size: 0.75rem;
        font-weight: 600;
        padding: 0.2rem 0.6rem;
        border-radius: 999px;
      }
      .chip--activo {
        background: var(--color-exito-suave);
        color: var(--color-exito);
      }
      .agregar-card {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        gap: 0.5rem;
        text-decoration: none;
        color: var(--texto-secundario);
        border: 2px dashed var(--borde);
        box-shadow: none;
      }
      .agregar-card__mas {
        font-size: 1.8rem;
        color: var(--color-primario);
      }
    `,
  ],
})
export class DashboardApoderado {}
