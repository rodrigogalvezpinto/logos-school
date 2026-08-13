import { Component, inject, signal } from '@angular/core';
import { Router, RouterLink } from '@angular/router';
import { Logo } from '../../shared/logo/logo';
import { AuthService, PerfilAlumnoRespuesta } from '../../core/auth.service';
import { SesionService } from '../../core/sesion.service';

@Component({
  selector: 'app-selector-perfil',
  standalone: true,
  imports: [Logo, RouterLink],
  template: `
    <div class="pagina">
      <div class="pagina__logo"><app-logo /></div>
      <h1>¿Quién va a estudiar hoy?</h1>

      <div class="perfiles">
        @for (perfil of perfiles(); track perfil.id) {
          <button class="perfil" (click)="entrarComoAlumno(perfil)">
            <div class="perfil__avatar" [style.background]="colorPara(perfil.id)">
              {{ perfil.nombre.charAt(0) }}
            </div>
            <span>{{ perfil.nombre }}</span>
          </button>
        }
        <button class="perfil" (click)="entrarComoApoderado()">
          <div class="perfil__avatar" style="background:#FF6B4A">👤</div>
          <span>Ver como Apoderado</span>
          <small>Progreso y planes</small>
        </button>
        <a class="perfil perfil--agregar" routerLink="/agregar-alumno">
          <div class="perfil__avatar perfil__avatar--agregar">+</div>
          <span>Agregar alumno</span>
        </a>
      </div>
    </div>
  `,
  styles: [
    `
      .pagina {
        max-width: 700px;
        margin: 0 auto;
        padding: 4rem 2rem;
        text-align: center;
      }
      .pagina__logo {
        display: flex;
        justify-content: center;
        margin-bottom: 2.5rem;
      }
      h1 {
        font-size: 1.7rem;
        margin-bottom: 2.5rem;
      }
      .perfiles {
        display: flex;
        justify-content: center;
        gap: 2rem;
        flex-wrap: wrap;
      }
      .perfil {
        display: flex;
        flex-direction: column;
        align-items: center;
        gap: 0.5rem;
        background: none;
        border: none;
        cursor: pointer;
        font-family: var(--fuente-texto);
        color: var(--texto-principal);
        width: 140px;
        text-decoration: none;
      }
      .perfil__avatar {
        width: 96px;
        height: 96px;
        border-radius: var(--radio-basica);
        display: flex;
        align-items: center;
        justify-content: center;
        color: white;
        font-family: var(--fuente-titulos);
        font-size: 2.2rem;
        font-weight: 700;
        transition: transform 0.15s;
      }
      .perfil:hover .perfil__avatar {
        transform: scale(1.05);
        outline: 3px solid var(--color-primario);
        outline-offset: 3px;
      }
      .perfil span {
        font-weight: 600;
      }
      .perfil small {
        color: var(--texto-secundario);
      }
      .perfil__avatar--agregar {
        background: var(--fondo);
        color: var(--texto-secundario);
        border: 2px dashed var(--borde);
      }
    `,
  ],
})
export class SelectorPerfil {
  perfiles = signal<PerfilAlumnoRespuesta[]>([]);
  private colores = ['#5B4FE9', '#22C55E', '#F59E0B', '#EF4444'];

  private auth = inject(AuthService);
  private sesion = inject(SesionService);
  private router = inject(Router);

  constructor() {
    this.auth.listarAlumnos().subscribe((perfiles) => this.perfiles.set(perfiles));
  }

  colorPara(id: number): string {
    return this.colores[id % this.colores.length];
  }

  entrarComoAlumno(perfil: PerfilAlumnoRespuesta) {
    this.sesion.elegirPerfil(perfil);
    this.router.navigate(['/alumno/inicio']);
  }

  entrarComoApoderado() {
    this.router.navigate(['/apoderado/inicio']);
  }
}
