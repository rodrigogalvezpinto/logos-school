import { Component, Input, Output, EventEmitter } from '@angular/core';
import { RouterLink } from '@angular/router';
import { BusquedaGlobal } from '../busqueda-global/busqueda-global';
import { CampanaNotificaciones } from '../campana-notificaciones/campana-notificaciones';

@Component({
  selector: 'app-topbar',
  standalone: true,
  imports: [RouterLink, BusquedaGlobal, CampanaNotificaciones],
  template: `
    <header class="topbar">
      <button type="button" class="topbar__hamburguesa" (click)="alternarMenu.emit()" aria-label="Abrir menú">☰</button>
      @if (mostrarBusqueda) {
        <app-busqueda-global />
      }
      <div class="topbar__acciones">
        @if (mostrarBusqueda) {
          <app-campana-notificaciones />
        }
        <a class="topbar__usuario" routerLink="/selector-perfil">
          <div class="topbar__avatar">{{ inicial }}</div>
          <div class="topbar__info-usuario">
            <span class="topbar__nombre">{{ nombre }}</span>
            @if (curso) {
              <span class="topbar__curso">({{ curso }})</span>
            }
          </div>
        </a>
      </div>
    </header>
  `,
  styles: [
    `
      .topbar {
        display: flex;
        justify-content: space-between;
        align-items: center;
        gap: 1rem;
        padding: 1.25rem 2rem;
        border-bottom: 1px solid var(--borde);
        background: var(--fondo-tarjeta);
      }
      .topbar > app-busqueda-global {
        flex: 1;
        display: flex;
        justify-content: center;
      }
      @media (max-width: 640px) {
        .topbar > app-busqueda-global {
          display: none;
        }
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
      .topbar__acciones {
        display: flex;
        align-items: center;
        gap: 1rem;
      }
      .topbar__usuario {
        display: flex;
        align-items: center;
        gap: 0.6rem;
        font-weight: 500;
        text-decoration: none;
        color: var(--texto-principal);
      }
      .topbar__info-usuario {
        display: flex;
        align-items: baseline;
        gap: 0.35rem;
      }
      .topbar__nombre {
        font-weight: 600;
      }
      .topbar__curso {
        font-size: 0.85rem;
        color: var(--texto-secundario);
        font-weight: 500;
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
  @Input() curso = '';
  @Input() mostrarBusqueda = false;
  @Output() alternarMenu = new EventEmitter<void>();

  get inicial(): string {
    return this.nombre.charAt(0).toUpperCase();
  }
}
