import { Component, inject } from '@angular/core';
import { RouterOutlet } from '@angular/router';
import { ProfesorSidebar } from '../../shared/profesor-sidebar/profesor-sidebar';
import { SesionProfesorService } from '../../core/sesion-profesor.service';

@Component({
  selector: 'app-profesor-shell',
  standalone: true,
  imports: [RouterOutlet, ProfesorSidebar],
  template: `
    <div class="shell">
      <app-profesor-sidebar />
      <div class="shell__contenido">
        <header class="shell__topbar">
          <span></span>
          <span class="shell__usuario">{{ sesion.nombre() || 'Profesor' }}</span>
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
export class ProfesorShell {
  sesion = inject(SesionProfesorService);
}
