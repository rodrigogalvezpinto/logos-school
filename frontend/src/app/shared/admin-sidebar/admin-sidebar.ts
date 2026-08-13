import { Component, Input, Output, EventEmitter, inject } from '@angular/core';
import { Router, RouterLink, RouterLinkActive } from '@angular/router';
import { Logo } from '../logo/logo';
import { SesionAdminService } from '../../core/sesion-admin.service';

interface ItemAdminSidebar {
  etiqueta: string;
  icono: string;
  ruta: string;
}

const ITEMS: ItemAdminSidebar[] = [
  { etiqueta: 'Dashboard', icono: '📊', ruta: '/admin/dashboard' },
  { etiqueta: 'Planes', icono: '💳', ruta: '/admin/planes' },
  { etiqueta: 'Descuentos', icono: '🏷️', ruta: '/admin/descuentos' },
  { etiqueta: 'Cortesías', icono: '🎁', ruta: '/admin/cortesias' },
  { etiqueta: 'Profesores', icono: '🧑‍🏫', ruta: '/admin/profesores' },
];

@Component({
  selector: 'app-admin-sidebar',
  standalone: true,
  imports: [RouterLink, RouterLinkActive, Logo],
  template: `
    @if (abierto) {
      <div class="sidebar__backdrop" (click)="cerrar.emit()"></div>
    }
    <aside class="sidebar" [class.sidebar--abierto]="abierto">
      <div class="sidebar__logo">
        <app-logo />
        <span class="sidebar__etiqueta">Admin</span>
      </div>
      <nav class="sidebar__nav">
        @for (item of items; track item.ruta) {
          <a class="sidebar__item" [routerLink]="item.ruta" routerLinkActive="sidebar__item--activo" (click)="cerrar.emit()">
            <span class="sidebar__icono">{{ item.icono }}</span>
            <span>{{ item.etiqueta }}</span>
          </a>
        }
      </nav>
      <div class="sidebar__pie">
        <a class="sidebar__item" href="#" (click)="cerrarSesion($event)">
          <span class="sidebar__icono">🚪</span><span>Cerrar sesión</span>
        </a>
      </div>
    </aside>
  `,
  styles: [
    `
      .sidebar {
        width: 240px;
        flex-shrink: 0;
        min-height: 100vh;
        background: var(--fondo-tarjeta);
        border-right: 1px solid var(--borde);
        display: flex;
        flex-direction: column;
        padding: 1.5rem 1rem;
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
        display: flex;
        align-items: center;
        gap: 0.5rem;
        padding: 0 0.5rem 1.5rem;
      }
      .sidebar__etiqueta {
        font-size: 0.7rem;
        font-weight: 700;
        text-transform: uppercase;
        color: var(--texto-secundario);
        background: var(--fondo);
        padding: 0.15rem 0.5rem;
        border-radius: 999px;
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
        color: var(--texto-principal);
        text-decoration: none;
        font-size: 0.9rem;
      }
      .sidebar__item:hover {
        background: var(--fondo);
      }
      .sidebar__item--activo {
        background: var(--color-primario-suave);
        color: var(--color-primario);
        font-weight: 600;
      }
      .sidebar__icono {
        font-size: 1.05rem;
      }
      .sidebar__pie {
        border-top: 1px solid var(--borde);
        padding-top: 0.75rem;
      }
    `,
  ],
})
export class AdminSidebar {
  @Input() abierto = false;
  @Output() cerrar = new EventEmitter<void>();

  items = ITEMS;

  private sesion = inject(SesionAdminService);
  private router = inject(Router);

  cerrarSesion(evento: Event) {
    evento.preventDefault();
    this.sesion.cerrarSesion();
    this.router.navigateByUrl('/admin/login');
  }
}
