import { Component, Input, inject, computed, signal } from '@angular/core';
import { RouterOutlet, NavigationStart, Router } from '@angular/router';
import { AyudaContextual } from '../../shared/ayuda-contextual/ayuda-contextual';
import { Sidebar } from '../../shared/sidebar/sidebar';
import { Topbar } from '../../shared/topbar/topbar';
import { AuthService } from '../../core/auth.service';
import { SesionService } from '../../core/sesion.service';

@Component({
  selector: 'app-shell',
  standalone: true,
  imports: [RouterOutlet, Sidebar, Topbar, AyudaContextual],
  template: `
    <div class="shell">
      <app-sidebar [modo]="modo" [abierto]="menuAbierto()" [mostrarEstadisticas]="cantidadAlumnos() >= 2" (cerrar)="menuAbierto.set(false)" />
      <div class="shell__contenido">
        <app-topbar
          [nombre]="nombreMostrado()"
          [curso]="cursoMostrado()"
          [mostrarBusqueda]="modo === 'alumno'"
          (alternarMenu)="menuAbierto.set(!menuAbierto())"
        />
        <main class="shell__main">
          <router-outlet />
        </main>
      </div>
      <app-ayuda-contextual />
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
  cantidadAlumnos = signal(0);

  private sesion = inject(SesionService);
  private auth = inject(AuthService);
  private router = inject(Router);

  constructor() {
    this.router.events.subscribe((evento) => {
      if (evento instanceof NavigationStart) this.menuAbierto.set(false);
    });
  }

  ngOnInit() {
    if (this.modo === 'apoderado') {
      this.auth.listarAlumnos().subscribe((alumnos) => this.cantidadAlumnos.set(alumnos.length));
    }
  }

  nombreMostrado = computed(() => {
    if (this.modo === 'alumno') return this.sesion.perfilActivo()?.nombre || '';
    return this.sesion.nombreApoderado() || 'Apoderado';
  });

  cursoMostrado = computed(() => {
    if (this.modo === 'alumno') return this.sesion.perfilActivo()?.nombre_nivel || '';
    return '';
  });
}
