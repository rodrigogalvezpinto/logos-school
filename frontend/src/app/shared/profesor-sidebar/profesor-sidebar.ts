import { Component, inject } from '@angular/core';
import { Router, RouterLink, RouterLinkActive } from '@angular/router';
import { Logo } from '../logo/logo';
import { SesionProfesorService } from '../../core/sesion-profesor.service';

@Component({
  selector: 'app-profesor-sidebar',
  standalone: true,
  imports: [RouterLink, RouterLinkActive, Logo],
  template: `
    <aside class="sidebar">
      <div class="sidebar__logo">
        <app-logo />
        <span class="sidebar__etiqueta">Profesor</span>
      </div>
      <nav class="sidebar__nav">
        <a class="sidebar__item" routerLink="/profesor/dashboard" routerLinkActive="sidebar__item--activo">
          <span class="sidebar__icono">📚</span><span>Mis Cursos</span>
        </a>
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
export class ProfesorSidebar {
  private sesion = inject(SesionProfesorService);
  private router = inject(Router);

  cerrarSesion(evento: Event) {
    evento.preventDefault();
    this.sesion.cerrarSesion();
    this.router.navigateByUrl('/profesor/login');
  }
}
