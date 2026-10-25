import { Component, Input } from '@angular/core';

@Component({
  selector: 'app-modelo-fracciones',
  standalone: true,
  template: `
    <div class="modelo-fracciones">
      <div
        class="modelo-fracciones__circulo"
        [style.background]="conicGradient"
      ></div>
      <div class="modelo-fracciones__etiqueta">
        {{ partesLlenas }}/{{ partes }}
      </div>
      @if (descripcion) {
        <div class="modelo-fracciones__descripcion">{{ descripcion }}</div>
      }
    </div>
  `,
  styles: [
    `
      .modelo-fracciones {
        display: flex;
        flex-direction: column;
        align-items: center;
        gap: 1rem;
        padding: 1.5rem;
        background: var(--color-primario-suave);
        border-radius: var(--radio-basica);
        margin: 1rem 0;
      }

      .modelo-fracciones__circulo {
        width: 150px;
        height: 150px;
        border-radius: 50%;
        border: 3px solid var(--color-primario);
        transition: background 0.3s ease;
      }

      .modelo-fracciones__etiqueta {
        font-size: 1.5rem;
        font-weight: 700;
        color: var(--color-primario);
      }

      .modelo-fracciones__descripcion {
        font-size: 0.9rem;
        color: var(--texto-secundario);
        font-style: italic;
        text-align: center;
      }

      @media (max-width: 768px) {
        .modelo-fracciones {
          padding: 1rem;
        }

        .modelo-fracciones__circulo {
          width: 120px;
          height: 120px;
        }

        .modelo-fracciones__etiqueta {
          font-size: 1.25rem;
        }
      }
    `,
  ],
})
export class ModeloFracciones {
  @Input() partes = 4;
  @Input() partesLlenas = 1;
  @Input() descripcion?: string;

  get conicGradient(): string {
    const angulo = (this.partesLlenas / this.partes) * 360;
    return `conic-gradient(var(--color-primario) 0deg ${angulo}deg, #e0e0e0 ${angulo}deg 360deg)`;
  }
}
