import { Component, Input, inject, computed } from '@angular/core';
import { RouterOutlet } from '@angular/router';
import { Sidebar } from '../../shared/sidebar/sidebar';
import { Topbar } from '../../shared/topbar/topbar';
import { SesionService } from '../../core/sesion.service';

@Component({
  selector: 'app-shell',
  standalone: true,
  imports: [RouterOutlet, Sidebar, Topbar],
  template: `
    <div class="shell">
      <app-sidebar [modo]="modo" />
      <div class="shell__contenido">
        <app-topbar [nombre]="nombreMostrado()" />
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
      .shell__main {
        flex: 1;
        padding: 2rem;
        max-width: 1100px;
        width: 100%;
      }
    `,
  ],
})
export class Shell {
  @Input() modo: 'alumno' | 'apoderado' = 'alumno';

  private sesion = inject(SesionService);

  nombreMostrado = computed(() => {
    if (this.modo === 'alumno') return this.sesion.perfilActivo()?.nombre || '';
    return this.sesion.nombreApoderado() || 'Apoderado';
  });
}
