import { Component, Input } from '@angular/core';
import { RouterLink } from '@angular/router';
import { Logo } from '../logo/logo';

@Component({
  selector: 'app-auth-layout',
  standalone: true,
  imports: [RouterLink, Logo],
  template: `
    <div class="auth">
      <div class="auth__panel">
        <div class="auth__panel-inner">
          <a routerLink="/" class="auth__logo"><app-logo /></a>
          <h1>{{ titulo }}</h1>
          <p class="auth__subtitulo">{{ subtitulo }}</p>
          <ng-content />
        </div>
      </div>
      <div class="auth__ilustracion">
        <svg viewBox="0 0 300 300" fill="none" xmlns="http://www.w3.org/2000/svg">
          <circle cx="150" cy="150" r="140" fill="#EEECFD" />
          <rect x="90" y="90" width="120" height="150" rx="14" fill="white" />
          <rect x="108" y="112" width="84" height="10" rx="5" fill="#5B4FE9" />
          <rect x="108" y="134" width="60" height="8" rx="4" fill="#C9C4F7" />
          <rect x="108" y="150" width="70" height="8" rx="4" fill="#C9C4F7" />
          <circle cx="150" cy="200" r="18" fill="#FF6B4A" />
          <path d="M142 200 L148 206 L160 192" stroke="white" stroke-width="4" stroke-linecap="round" stroke-linejoin="round" />
        </svg>
      </div>
    </div>
  `,
  styles: [
    `
      .auth {
        min-height: 100vh;
        display: flex;
      }
      /* El panel ocupa su mitad del ancho y CENTRA su contenido interno dentro de
         esa mitad (en vez de aplicar max-width + margin:auto directo sobre un
         flex item, que compite con flex-grow y termina pegado a la izquierda). */
      .auth__panel {
        flex: 1;
        display: flex;
        align-items: center;
        justify-content: center;
        padding: 2rem;
      }
      .auth__panel-inner {
        width: 100%;
        max-width: 400px;
      }
      .auth__logo {
        margin-bottom: 2rem;
      }
      .auth__panel h1 {
        font-size: 1.6rem;
        margin-bottom: 0.35rem;
      }
      .auth__subtitulo {
        color: var(--texto-secundario);
        margin-bottom: 2rem;
      }
      .auth__ilustracion {
        flex: 1;
        display: flex;
        align-items: center;
        justify-content: center;
        background: var(--fondo);
      }
      .auth__ilustracion svg {
        width: 340px;
        height: 340px;
      }
      @media (max-width: 900px) {
        .auth__ilustracion {
          display: none;
        }
      }
    `,
  ],
})
export class AuthLayout {
  @Input() titulo = '';
  @Input() subtitulo = '';
}
