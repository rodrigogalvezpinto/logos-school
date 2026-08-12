import { Component } from '@angular/core';
import { Router } from '@angular/router';
import { Logo } from '../../shared/logo/logo';

@Component({
  selector: 'app-selector-perfil',
  standalone: true,
  imports: [Logo],
  template: `
    <div class="pagina">
      <div class="pagina__logo"><app-logo /></div>
      <h1>¿Quién va a estudiar hoy?</h1>

      <div class="perfiles">
        <button class="perfil" (click)="entrarComoAlumno()">
          <div class="perfil__avatar" style="background:#5B4FE9">S</div>
          <span>Sofía</span>
          <small>4° básico</small>
        </button>
        <button class="perfil" (click)="entrarComoApoderado()">
          <div class="perfil__avatar" style="background:#FF6B4A">👤</div>
          <span>Ver como Apoderado</span>
          <small>Progreso y planes</small>
        </button>
        <button class="perfil perfil--agregar">
          <div class="perfil__avatar perfil__avatar--agregar">+</div>
          <span>Agregar alumno</span>
        </button>
      </div>
    </div>
  `,
  styles: [
    `
      .pagina {
        max-width: 640px;
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
  constructor(private router: Router) {}

  entrarComoAlumno() {
    this.router.navigate(['/alumno/inicio']);
  }

  entrarComoApoderado() {
    this.router.navigate(['/apoderado/inicio']);
  }
}
