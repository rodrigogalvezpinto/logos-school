import { Component, inject } from '@angular/core';
import { RouterOutlet } from '@angular/router';
import { AdminSidebar } from '../../shared/admin-sidebar/admin-sidebar';
import { SesionAdminService } from '../../core/sesion-admin.service';

@Component({
  selector: 'app-admin-shell',
  standalone: true,
  imports: [RouterOutlet, AdminSidebar],
  template: `
    <div class="shell">
      <app-admin-sidebar />
      <div class="shell__contenido">
        <header class="shell__topbar">
          <span></span>
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
      }
      .shell__contenido {
        flex: 1;
        display: flex;
        flex-direction: column;
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
      .shell__main {
        flex: 1;
        padding: 2rem;
        max-width: 1100px;
        width: 100%;
      }
    `,
  ],
})
export class AdminShell {
  sesion = inject(SesionAdminService);
}
