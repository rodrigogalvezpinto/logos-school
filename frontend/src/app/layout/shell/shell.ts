import { Component, Input, inject, computed, signal } from '@angular/core';
import { RouterOutlet, NavigationStart, Router } from '@angular/router';
import { Sidebar } from '../../shared/sidebar/sidebar';
import { Topbar } from '../../shared/topbar/topbar';
import { SesionService } from '../../core/sesion.service';

@Component({
  selector: 'app-shell',
  standalone: true,
  imports: [RouterOutlet, Sidebar, Topbar],
  template: `
    <div class="shell">
      <app-sidebar [modo]="modo" [abierto]="menuAbierto()" (cerrar)="menuAbierto.set(false)" />
      <div class="shell__contenido">
        <app-topbar [nombre]="nombreMostrado()" (alternarMenu)="menuAbierto.set(!menuAbierto())" />
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
      .shell__main {
        flex: 1;
        padding: 2rem;
        max-width: 1100px;
        width: 100%;
      }
      @media (max-width: 800px) {
        .shell__main {
          padding: 1.25rem;
        }
      }
    `,
  ],
})
export class Shell {
  @Input() modo: 'alumno' | 'apoderado' = 'alumno';

  menuAbierto = signal(false);

  private sesion = inject(SesionService);
  private router = inject(Router);

  constructor() {
    this.router.events.subscribe((evento) => {
      if (evento instanceof NavigationStart) this.menuAbierto.set(false);
    });
  }

  nombreMostrado = computed(() => {
    if (this.modo === 'alumno') return this.sesion.perfilActivo()?.nombre || '';
    return this.sesion.nombreApoderado() || 'Apoderado';
  });
}
