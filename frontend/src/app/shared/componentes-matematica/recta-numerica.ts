import { Component, Input } from '@angular/core';

@Component({
  selector: 'app-recta-numerica',
  standalone: true,
  template: `
    <div class="recta-numerica">
      <div class="recta-numerica__linea">
        @for (valor of valores; track valor) {
          <div class="recta-numerica__punto" [class.destacado]="valor === valorDestacado">
            <span class="recta-numerica__etiqueta">{{ valor }}</span>
          </div>
        }
      </div>
      @if (etiqueta) {
        <div class="recta-numerica__descripcion">{{ etiqueta }}</div>
      }
    </div>
  `,
  styles: [
    `
      .recta-numerica {
        display: flex;
        flex-direction: column;
        align-items: center;
        gap: 0.5rem;
        padding: 1.5rem;
        background: var(--color-primario-suave);
        border-radius: var(--radio-basica);
        margin: 1rem 0;
      }

      .recta-numerica__linea {
        display: flex;
        align-items: center;
        gap: 1rem;
        position: relative;
        padding: 1rem 0;
      }

      .recta-numerica__linea::before {
        content: '';
        position: absolute;
        top: 50%;
        left: 0;
        right: 0;
        height: 2px;
        background: var(--color-primario);
        transform: translateY(-50%);
      }

      .recta-numerica__punto {
        position: relative;
        z-index: 1;
        display: flex;
        flex-direction: column;
        align-items: center;
        gap: 0.25rem;
      }

      .recta-numerica__punto::before {
        content: '';
        width: 12px;
        height: 12px;
        background: var(--color-primario);
        border-radius: 50%;
        border: 2px solid white;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
      }

      .recta-numerica__punto.destacado::before {
        background: var(--color-secundario);
        transform: scale(1.3);
      }

      .recta-numerica__etiqueta {
        font-size: 0.85rem;
        font-weight: 600;
        color: var(--texto-principal);
        margin-top: 0.5rem;
      }

      .recta-numerica__descripcion {
        font-size: 0.9rem;
        color: var(--texto-secundario);
        font-style: italic;
      }

      @media (max-width: 768px) {
        .recta-numerica {
          padding: 1rem;
        }

        .recta-numerica__linea {
          gap: 0.5rem;
        }

        .recta-numerica__etiqueta {
          font-size: 0.75rem;
        }
      }
    `,
  ],
})
export class RectaNumerica {
  @Input() valores: number[] = [];
  @Input() valorDestacado?: number;
  @Input() etiqueta?: string;
}
