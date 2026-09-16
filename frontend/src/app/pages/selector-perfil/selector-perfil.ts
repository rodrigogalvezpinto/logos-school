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
    <div class="fondo">
      <div class="pagina">
        <div class="pagina__logo"><app-logo /></div>
        <h1>¿Quién va a estudiar hoy?</h1>

      @if (error()) {
        <p class="error-carga">{{ error() }}</p>
      }
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
    </div>
  `,
  styles: [
    `
      /* Degradado de marca (índigo + coral) para dar más energía a este momento de
         bienvenida — hallazgo comparando en vivo contra Brincus (ver
         planificacion/27-plan-incorporacion-hallazgos-brincus.md): usa la paleta propia de
         Logos, no los colores literales de Brincus, para que se sienta más vivo sin dejar
         de sentirse "Logos School". */
      .fondo {
        min-height: 100vh;
        display: flex;
        align-items: center;
        justify-content: center;
        padding: 2rem;
        background: linear-gradient(135deg, var(--color-primario) 0%, var(--color-primario-oscuro) 45%, var(--color-secundario) 100%);
      }
      .pagina {
        max-width: 700px;
        width: 100%;
        margin: 0 auto;
        padding: 3.5rem 2.5rem;
        text-align: center;
        background: var(--fondo-tarjeta, #fff);
        border-radius: var(--radio-basica);
        box-shadow: 0 20px 60px rgba(0, 0, 0, 0.25);
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
      .error-carga {
        color: var(--color-error-texto);
        margin-bottom: 1.5rem;
      }
    `,
  ],
})
export class SelectorPerfil {
  perfiles = signal<PerfilAlumnoRespuesta[]>([]);
  error = signal('');
  private colores = ['#5B4FE9', '#22C55E', '#F59E0B', '#EF4444'];

  private auth = inject(AuthService);
  private sesion = inject(SesionService);
  private router = inject(Router);

  constructor() {
    this.auth.listarAlumnos().subscribe({
      next: (perfiles) => this.perfiles.set(perfiles),
      error: () => this.error.set('No se pudieron cargar tus alumnos. Intenta recargar la página.'),
    });
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
