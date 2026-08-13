import { Component, Input, Output, EventEmitter } from '@angular/core';
import { RouterLink } from '@angular/router';

@Component({
  selector: 'app-topbar',
  standalone: true,
  imports: [RouterLink],
  template: `
    <header class="topbar">
      <button type="button" class="topbar__hamburguesa" (click)="alternarMenu.emit()" aria-label="Abrir menú">☰</button>
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
      .topbar__hamburguesa {
        display: none;
        background: none;
        border: none;
        font-size: 1.5rem;
        cursor: pointer;
        color: var(--texto-principal);
        padding: 0.25rem;
      }
      @media (max-width: 800px) {
        .topbar__hamburguesa {
          display: block;
        }
        .topbar {
          padding: 1rem 1.25rem;
        }
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
  @Output() alternarMenu = new EventEmitter<void>();

  get inicial(): string {
    return this.nombre.charAt(0).toUpperCase();
  }
}
