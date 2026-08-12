import { Component, Input } from '@angular/core';
import { RouterOutlet } from '@angular/router';
import { Sidebar } from '../../shared/sidebar/sidebar';
import { Topbar } from '../../shared/topbar/topbar';

@Component({
  selector: 'app-shell',
  standalone: true,
  imports: [RouterOutlet, Sidebar, Topbar],
  template: `
    <div class="shell">
      <app-sidebar [modo]="modo" />
      <div class="shell__contenido">
        <app-topbar [nombre]="nombre" />
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
  @Input() nombre = 'Sofía';
}
