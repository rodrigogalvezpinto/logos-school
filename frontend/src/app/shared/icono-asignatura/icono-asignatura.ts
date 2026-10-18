import { Component, Input } from '@angular/core';

const ICONOS: Record<string, string> = {
  libro: '📖',
  regla: '📐',
  hoja: '🌱',
  mapa: '🗺️',
  ingles: '🌐',
  filosofia: '🧠',
  balanza: '⚖️',
  examen: '📋',
};

@Component({
  selector: 'app-icono-asignatura',
  standalone: true,
  template: `
    <div class="icono" [style.background]="color + '22'" [style.color]="color">
      {{ emoji }}
    </div>
  `,
  styles: [
    `
      .icono {
        width: 52px;
        height: 52px;
        border-radius: var(--radio-media);
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.6rem;
      }
    `,
  ],
})
export class IconoAsignatura {
  @Input() icono = 'libro';
  @Input() color = '#5B4FE9';

  get emoji(): string {
    return ICONOS[this.icono] ?? '📘';
  }
}
