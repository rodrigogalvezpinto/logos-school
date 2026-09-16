import { Component, Input } from '@angular/core';
import { EtapaJardin } from '../../core/prediccion.service';

const ETIQUETA_POR_ETAPA: Record<EtapaJardin, string> = {
  semilla: 'Semilla',
  brote: 'Recién brotó',
  crecimiento: 'Creciendo',
  floreciendo: 'Floreciendo',
  flor_completa: 'Floreció del todo',
};

let contadorInstancias = 0;

/** Ilustración propia en SVG (sin arte externo, mismo criterio de "cero dependencias, cero
 * licencias" ya aplicado a avatares y emoji — ver planificacion/15-diseno-visual-y-marca.md)
 * para "Racha de la casa" / jardín semanal (idea 3 del boceto de innovación, 2026-08-17).
 * 5 estados según cuántos días activos tuvo esa semana — más granular que la versión
 * original de 3 estados, para que el crecimiento se sienta gradual, no en saltos bruscos.
 * Maceta con curvas + degradado + sombra de piso (no un polígono recto plano) para que se
 * sienta como una ilustración real, no un ícono genérico. */
@Component({
  selector: 'app-planta-jardin',
  standalone: true,
  template: `
    <div class="planta-jardin" [class.planta-jardin--mini]="tamano === 'mini'">
      <svg viewBox="0 0 100 128" [attr.aria-label]="etiqueta()" role="img">
        <defs>
          <linearGradient [attr.id]="gradId" x1="0" y1="0" x2="0" y2="1">
            <stop offset="0%" stop-color="#FF8A6B" />
            <stop offset="100%" stop-color="#FF6B4A" />
          </linearGradient>
        </defs>

        @if (tamano === 'grande') {
          <circle cx="50" cy="58" r="50" fill="#5B4FE9" opacity="0.06" />
        }

        <!-- Sombra de piso -->
        <ellipse cx="50" cy="124" rx="24" ry="3.4" fill="#000" opacity="0.08" />

        <!-- Maceta, siempre presente -->
        <path d="M30,98 Q30,94 34,94 L66,94 Q70,94 70,98 L64,118 Q63,122 58,122 L42,122 Q37,122 36,118 Z" [attr.fill]="'url(#' + gradId + ')'" />
        <ellipse cx="50" cy="94" rx="20" ry="4.5" fill="#FFB098" />
        <ellipse cx="50" cy="94.5" rx="15.5" ry="3" fill="#6B4A34" />

        @switch (etapa) {
          @case ('semilla') {
            <circle cx="50" cy="92" r="4" fill="#8B5E3C" />
          }
          @case ('brote') {
            <line x1="50" y1="94" x2="50" y2="78" stroke="#4CAF6D" stroke-width="4" stroke-linecap="round" />
            <ellipse cx="42" cy="78" rx="8" ry="5" fill="#5FC786" transform="rotate(-25 42 78)" />
            <ellipse cx="58" cy="78" rx="8" ry="5" fill="#5FC786" transform="rotate(25 58 78)" />
          }
          @case ('crecimiento') {
            <line x1="50" y1="94" x2="50" y2="58" stroke="#4CAF6D" stroke-width="4" stroke-linecap="round" />
            <ellipse cx="40" cy="80" rx="9" ry="5.5" fill="#5FC786" transform="rotate(-25 40 80)" />
            <ellipse cx="60" cy="80" rx="9" ry="5.5" fill="#5FC786" transform="rotate(25 60 80)" />
            <ellipse cx="38" cy="64" rx="9" ry="5.5" fill="#6FD897" transform="rotate(-20 38 64)" />
            <ellipse cx="62" cy="64" rx="9" ry="5.5" fill="#6FD897" transform="rotate(20 62 64)" />
          }
          @case ('floreciendo') {
            <line x1="50" y1="94" x2="50" y2="44" stroke="#4CAF6D" stroke-width="4" stroke-linecap="round" />
            <ellipse cx="38" cy="78" rx="9" ry="5.5" fill="#5FC786" transform="rotate(-25 38 78)" />
            <ellipse cx="62" cy="78" rx="9" ry="5.5" fill="#5FC786" transform="rotate(25 62 78)" />
            <ellipse cx="36" cy="60" rx="9" ry="5.5" fill="#6FD897" transform="rotate(-20 36 60)" />
            <ellipse cx="64" cy="60" rx="9" ry="5.5" fill="#6FD897" transform="rotate(20 64 60)" />
            <circle cx="50" cy="40" r="7.5" fill="#FFB59E" />
            <circle cx="50" cy="40" r="4" fill="#FFD23F" opacity="0.8" />
          }
          @case ('flor_completa') {
            <line x1="50" y1="94" x2="50" y2="38" stroke="#4CAF6D" stroke-width="4" stroke-linecap="round" />
            <ellipse cx="37" cy="76" rx="9" ry="5.5" fill="#5FC786" transform="rotate(-25 37 76)" />
            <ellipse cx="63" cy="76" rx="9" ry="5.5" fill="#5FC786" transform="rotate(25 63 76)" />
            <ellipse cx="35" cy="58" rx="9" ry="5.5" fill="#6FD897" transform="rotate(-20 35 58)" />
            <ellipse cx="65" cy="58" rx="9" ry="5.5" fill="#6FD897" transform="rotate(20 65 58)" />
            <g>
              <ellipse cx="50" cy="26" rx="7.5" ry="11" fill="#FF6B4A" />
              <ellipse cx="50" cy="26" rx="7.5" ry="11" fill="#FF6B4A" transform="rotate(72 50 26)" />
              <ellipse cx="50" cy="26" rx="7.5" ry="11" fill="#FF6B4A" transform="rotate(144 50 26)" />
              <ellipse cx="50" cy="26" rx="7.5" ry="11" fill="#FF6B4A" transform="rotate(216 50 26)" />
              <ellipse cx="50" cy="26" rx="7.5" ry="11" fill="#FF6B4A" transform="rotate(288 50 26)" />
              <circle cx="50" cy="26" r="6.5" fill="#FFD23F" />
            </g>
            <circle cx="74" cy="22" r="1.8" fill="#FFD23F" />
            <circle cx="26" cy="34" r="1.4" fill="#FFD23F" />
            <circle cx="70" cy="42" r="1.2" fill="#5B4FE9" opacity="0.5" />
          }
        }
      </svg>
      @if (tamano === 'grande') {
        <span class="planta-jardin__etiqueta">{{ etiqueta() }}</span>
      }
    </div>
  `,
  styles: [
    `
      .planta-jardin {
        display: flex;
        flex-direction: column;
        align-items: center;
        gap: 0.4rem;
      }
      .planta-jardin svg {
        width: 100px;
        height: 128px;
      }
      .planta-jardin--mini svg {
        width: 46px;
        height: 59px;
      }
      .planta-jardin__etiqueta {
        font-size: 0.8rem;
        font-weight: 700;
        color: var(--texto-principal);
        text-align: center;
      }
    `,
  ],
})
export class PlantaJardin {
  @Input() etapa: EtapaJardin = 'semilla';
  @Input() tamano: 'grande' | 'mini' = 'grande';

  readonly gradId = `planta-maceta-grad-${contadorInstancias++}`;

  etiqueta(): string {
    return ETIQUETA_POR_ETAPA[this.etapa];
  }
}
