import { Component, inject, signal } from '@angular/core';
import { RouterOutlet, NavigationStart, Router } from '@angular/router';
import { AdminSidebar } from '../../shared/admin-sidebar/admin-sidebar';
import { SesionAdminService } from '../../core/sesion-admin.service';

@Component({
  selector: 'app-admin-shell',
  standalone: true,
  imports: [RouterOutlet, AdminSidebar],
  template: `
    <div class="shell">
      <app-admin-sidebar [abierto]="menuAbierto()" (cerrar)="menuAbierto.set(false)" />
      <div class="shell__contenido">
        <header class="shell__topbar">
          <button type="button" class="shell__hamburguesa" (click)="menuAbierto.set(!menuAbierto())" aria-label="Abrir menú">☰</button>
          <span class="shell__usuario">{{ sesion.nombre() || 'Administrador' }}</span>
        </header>
        <main class="shell__main">
          <router-outlet />
        </main>
      </div>
    </div>
  `,
  styles: [
    `
      .shell {
        display: flex;
        min-height: 100vh;
        max-width: 100vw;
        overflow-x: hidden;
      }
      .shell__contenido {
        flex: 1;
        display: flex;
        flex-direction: column;
        min-width: 0;
      }
      .shell__topbar {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 1.25rem 2rem;
        border-bottom: 1px solid var(--borde);
        background: var(--fondo-tarjeta);
      }
      .shell__usuario {
        font-weight: 500;
        color: var(--texto-principal);
      }
      .shell__hamburguesa {
        display: none;
        background: none;
        border: none;
        font-size: 1.5rem;
        cursor: pointer;
        color: var(--texto-principal);
        padding: 0.25rem;
      }
      .shell__main {
        flex: 1;
        padding: 2rem;
        max-width: 1100px;
        width: 100%;
      }
      @media (max-width: 800px) {
        .shell__hamburguesa {
          display: block;
        }
        .shell__topbar {
          padding: 1rem 1.25rem;
        }
        .shell__main {
          padding: 1.25rem;
        }
      }
    `,
  ],
})
export class AdminShell {
  sesion = inject(SesionAdminService);
  menuAbierto = signal(false);

  private router = inject(Router);

  constructor() {
    this.router.events.subscribe((evento) => {
      if (evento instanceof NavigationStart) this.menuAbierto.set(false);
    });
  }
}
