import { Component, Input, inject } from '@angular/core';
import { LectorVozService } from '../../core/lector-voz.service';
import { textoParaVoz } from '../texto-para-voz';

@Component({
  selector: 'app-boton-escuchar',
  standalone: true,
  template: `
    @if (lector.disponible) {
      <button type="button" class="boton-escuchar" (click)="alternar()">
        {{ lector.hablando() ? '⏸ Detener' : '🔊 Escuchar' }}
      </button>
    }
  `,
  styles: [
    `
      .boton-escuchar {
        display: inline-flex;
        align-items: center;
        gap: 0.4rem;
        background: var(--color-primario-suave);
        color: var(--color-primario);
        border: none;
        border-radius: 999px;
        padding: 0.5rem 1rem;
        font-size: 0.9rem;
        font-weight: 600;
        cursor: pointer;
      }
      .boton-escuchar:hover {
        filter: brightness(0.95);
      }
    `,
  ],
})
export class BotonEscuchar {
  @Input({ required: true }) texto = '';
  @Input() idioma?: string;
  @Input() velocidad?: number;

  lector = inject(LectorVozService);

  alternar() {
    // Se lee lo que se ve, sin marcadores ni nombres de emojis (ver texto-para-voz.ts).
    this.lector.alternar(textoParaVoz(this.texto), { idioma: this.idioma, velocidad: this.velocidad });
  }
}
