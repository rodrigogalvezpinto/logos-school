import { Component, Input } from '@angular/core';

@Component({
  selector: 'app-emoji-educativo',
  standalone: true,
  template: `
    <div class="emoji-educativo" [class.emoji-educativo--grande]="grande">
      <span class="emoji-educativo__icono">{{ emoji }}</span>
      @if (descripcion && mostrarDescripcion) {
        <span class="emoji-educativo__descripcion">{{ descripcion }}</span>
      }
    </div>
  `,
  styles: [
    `
      .emoji-educativo {
        display: inline-flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        gap: 0.5rem;
        padding: 1rem;
        background: var(--color-primario-suave);
        border-radius: var(--radio-media);
        transition: transform 0.2s ease;
      }

      .emoji-educativo:hover {
        transform: scale(1.05);
      }

      .emoji-educativo--grande {
        padding: 2rem;
        margin: 1rem 0;
      }

      .emoji-educativo__icono {
        font-size: 3rem;
        line-height: 1;
        filter: drop-shadow(0 2px 4px rgba(0, 0, 0, 0.1));
      }

      .emoji-educativo--grande .emoji-educativo__icono {
        font-size: 6rem;
      }

      .emoji-educativo__descripcion {
        font-size: 0.85rem;
        color: var(--texto-secundario);
        text-align: center;
        max-width: 200px;
      }

      @media (max-width: 768px) {
        .emoji-educativo--grande {
          padding: 1.5rem;
        }

        .emoji-educativo--grande .emoji-educativo__icono {
          font-size: 4rem;
        }

        .emoji-educativo__descripcion {
          font-size: 0.75rem;
        }
      }
    `,
  ],
})
export class EmojiEducativo {
  @Input() emoji = '';
  @Input() descripcion = '';
  @Input() grande = false;
  @Input() mostrarDescripcion = true;
}
