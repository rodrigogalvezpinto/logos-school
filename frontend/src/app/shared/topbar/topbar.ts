import { Component, Input } from '@angular/core';
import { RouterLink } from '@angular/router';

@Component({
  selector: 'app-topbar',
  standalone: true,
  imports: [RouterLink],
  template: `
    <header class="topbar">
      <div></div>
      <a class="topbar__usuario" routerLink="/selector-perfil">
        <div class="topbar__avatar">{{ inicial }}</div>
        <span>{{ nombre }}</span>
      </a>
    </header>
  `,
  styles: [
    `
      .topbar {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 1.25rem 2rem;
        border-bottom: 1px solid var(--borde);
        background: var(--fondo-tarjeta);
      }
      .topbar__usuario {
        display: flex;
        align-items: center;
        gap: 0.6rem;
        font-weight: 500;
        text-decoration: none;
        color: var(--texto-principal);
      }
      .topbar__avatar {
        width: 38px;
        height: 38px;
        border-radius: 50%;
        background: var(--color-secundario);
        color: white;
        display: flex;
        align-items: center;
        justify-content: center;
        font-family: var(--fuente-titulos);
        font-weight: 600;
      }
    `,
  ],
})
export class Topbar {
  @Input() nombre = 'Sofía';

  get inicial(): string {
    return this.nombre.charAt(0).toUpperCase();
  }
}
