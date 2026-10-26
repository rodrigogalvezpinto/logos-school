import { Component, Input, signal } from '@angular/core';

@Component({
  selector: 'app-logo',
  standalone: true,
  template: `
    <div class="logo" [class.logo--solo-icono]="soloIcono">
      @if (!errorImagen()) {
        <img
          src="assets/branding/logo.svg"
          [attr.width]="tamano"
          [attr.height]="tamano"
          alt="Logos School"
          class="logo__img"
          (error)="errorImagen.set(true)"
        />
      } @else {
        <svg
          [attr.width]="tamano"
          [attr.height]="tamano"
          viewBox="0 0 48 48"
          fill="none"
          xmlns="http://www.w3.org/2000/svg"
        >
          <!-- Libro abierto cuyas páginas forman un camino ascendente -->
          <path
            d="M4 14 C4 12 6 11 8 11.5 L22 15 L22 38 L8 34.5 C6 34 4 33 4 31 Z"
            fill="#5B4FE9"
          />
          <path
            d="M44 14 C44 12 42 11 40 11.5 L26 15 L26 38 L40 34.5 C42 34 44 33 44 31 Z"
            fill="#5B4FE9"
            fill-opacity="0.55"
          />
          <path
            d="M10 27 L18 20 L23 24 L34 13"
            stroke="#FF6B4A"
            stroke-width="3"
            stroke-linecap="round"
            stroke-linejoin="round"
          />
          <path d="M27 13 H34 V20" stroke="#FF6B4A" stroke-width="3" stroke-linecap="round" stroke-linejoin="round" />
        </svg>
      }
      @if (!soloIcono) {
        <span class="logo__texto">Logos School</span>
      }
    </div>
  `,
  styles: [
    `
      .logo {
        display: inline-flex;
        align-items: center;
        gap: 0.5rem;
      }
      .logo__img {
        object-fit: contain;
      }
      .logo__texto {
        font-family: var(--fuente-titulos);
        font-weight: 700;
        font-size: 1.35rem;
        color: var(--texto-principal);
      }
    `,
  ],
})
export class Logo {
  @Input() tamano = 36;
  @Input() soloIcono = false;
  errorImagen = signal(false);
}
