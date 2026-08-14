import { Component, Input, Output, EventEmitter } from '@angular/core';
import { RouterLink, RouterLinkActive } from '@angular/router';
import { Logo } from '../logo/logo';

export interface ItemSidebar {
  etiqueta: string;
  icono: string;
  ruta: string;
  proximamente?: boolean;
}

const SIDEBAR_ALUMNO: ItemSidebar[] = [
  { etiqueta: 'Inicio', icono: '🏠', ruta: '/alumno/inicio' },
  { etiqueta: 'Mis Asignaturas', icono: '📚', ruta: '/alumno/asignaturas' },
  { etiqueta: 'Pruebas y Exámenes', icono: '📝', ruta: '/alumno/evaluaciones' },
  { etiqueta: 'Mis Notas', icono: '📊', ruta: '/alumno/notas' },
  { etiqueta: 'Plan de Estudio', icono: '📅', ruta: '/alumno/plan-estudio' },
];

const SIDEBAR_APODERADO: ItemSidebar[] = [
  { etiqueta: 'Inicio', icono: '🏠', ruta: '/apoderado/inicio' },
  { etiqueta: 'Mis Alumnos', icono: '👨‍👩‍👧', ruta: '/apoderado/alumnos' },
  { etiqueta: 'Progreso por Alumno', icono: '📊', ruta: '/apoderado/progreso' },
  { etiqueta: 'Plan y Pagos', icono: '💳', ruta: '/apoderado/plan' },
];

@Component({
  selector: 'app-sidebar',
  standalone: true,
  imports: [RouterLink, RouterLinkActive, Logo],
  template: `
    @if (abierto) {
      <div class="sidebar__backdrop" (click)="cerrar.emit()"></div>
    }
    <aside class="sidebar" [class.sidebar--abierto]="abierto">
      <div class="sidebar__logo">
        <app-logo />
      </div>
      <nav class="sidebar__nav">
        @for (item of items; track item.ruta) {
          <a
            class="sidebar__item"
            [class.sidebar__item--proximamente]="item.proximamente"
            [routerLink]="item.proximamente ? null : item.ruta"
            routerLinkActive="sidebar__item--activo"
            (click)="cerrar.emit()"
          >
            <span class="sidebar__icono">{{ item.icono }}</span>
            <span>{{ item.etiqueta }}</span>
            @if (item.proximamente) {
              <span class="sidebar__badge">pronto</span>
            }
          </a>
        }
      </nav>
      <div class="sidebar__pie">
        <a class="sidebar__item" [routerLink]="modo === 'alumno' ? '/alumno/configuracion' : '/apoderado/configuracion'" (click)="cerrar.emit()">
          <span class="sidebar__icono">⚙️</span><span>Configuración</span>
        </a>
        <a class="sidebar__item" routerLink="/selector-perfil" (click)="cerrar.emit()">
          <span class="sidebar__icono">🔄</span><span>Cambiar de perfil</span>
        </a>
      </div>
    </aside>
  `,
  styles: [
    `
      .sidebar {
        display: flex;
        flex-direction: column;
        width: 260px;
        min-height: 100vh;
        background: var(--fondo-tarjeta);
        border-right: 1px solid var(--borde);
        padding: 1.25rem 1rem;
        flex-shrink: 0;
      }
      .sidebar__backdrop {
        display: none;
      }
      @media (max-width: 800px) {
        .sidebar {
          position: fixed;
          top: 0;
          left: 0;
          height: 100vh;
          z-index: 200;
          transform: translateX(-100%);
          visibility: hidden;
          transition: transform 0.2s ease, visibility 0s linear 0.2s;
          box-shadow: 0 0 24px rgba(0, 0, 0, 0.15);
        }
        .sidebar--abierto {
          transform: translateX(0);
          visibility: visible;
          transition: transform 0.2s ease, visibility 0s linear 0s;
        }
        .sidebar__backdrop {
          display: block;
          position: fixed;
          inset: 0;
          background: rgba(0, 0, 0, 0.4);
          z-index: 150;
        }
      }
      .sidebar__logo {
        padding: 0 0.5rem 1.5rem;
      }
      .sidebar__nav {
        display: flex;
        flex-direction: column;
        gap: 0.25rem;
        flex: 1;
      }
      .sidebar__item {
        display: flex;
        align-items: center;
        gap: 0.75rem;
        padding: 0.65rem 0.75rem;
        border-radius: var(--radio-media);
        text-decoration: none;
        color: var(--texto-secundario);
        font-weight: 500;
        font-size: 0.95rem;
        cursor: pointer;
        transition: background 0.15s;
      }
      .sidebar__item:hover {
        background: var(--color-primario-suave);
        color: var(--color-primario);
      }
      .sidebar__item--activo {
        background: var(--color-primario-suave);
        color: var(--color-primario);
        font-weight: 600;
      }
      .sidebar__item--proximamente {
        opacity: 0.55;
        cursor: default;
      }
      .sidebar__item--proximamente:hover {
        background: none;
        color: var(--texto-secundario);
      }
      .sidebar__icono {
        font-size: 1.1rem;
      }
      .sidebar__badge {
        margin-left: auto;
        font-size: 0.65rem;
        background: var(--color-alerta-suave);
        color: var(--color-alerta);
        padding: 0.1rem 0.4rem;
        border-radius: 999px;
      }
      .sidebar__pie {
        border-top: 1px solid var(--borde);
        padding-top: 0.75rem;
        display: flex;
        flex-direction: column;
        gap: 0.25rem;
      }
    `,
  ],
})
export class Sidebar {
  @Input() modo: 'alumno' | 'apoderado' = 'alumno';
  @Input() abierto = false;
  @Output() cerrar = new EventEmitter<void>();

  get items(): ItemSidebar[] {
    return this.modo === 'alumno' ? SIDEBAR_ALUMNO : SIDEBAR_APODERADO;
  }
}
