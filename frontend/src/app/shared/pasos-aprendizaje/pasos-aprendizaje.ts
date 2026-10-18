import { Component, Input } from '@angular/core';

/** Los dos pasos de aprender un OA: primero la explicación + ejemplos resueltos ("Aprender"),
 * después el banco de preguntas ("Practicar") — antes era una sola página larga con todo
 * junto (guía + botón de practicar al final). Separarlos en dos pasos explícitos, con este
 * indicador visible en ambas pantallas, viene de comparar en vivo contra Brincus: ellos
 * separan "enseñar" (video) de "practicar" (guía-ejercicios) en dos piezas — Logos no tiene
 * video, pero ya tenía las dos piezas equivalentes (explicación+ejemplos, banco de preguntas)
 * fusionadas en una sola pantalla. Bonus: al quedar "Aprender" como su propia pieza bien
 * delimitada, el contenido queda lista para usarse como guion de un video más adelante. */
@Component({
  selector: 'app-pasos-aprendizaje',
  standalone: true,
  template: `
    <div class="pasos">
      <div class="paso" [class.paso--activo]="paso === 1" [class.paso--hecho]="paso > 1">
        <span class="paso__numero">{{ paso > 1 ? '✓' : '1' }}</span>
        <span class="paso__etiqueta">Aprender</span>
      </div>
      <div class="paso__linea" [class.paso__linea--hecha]="paso > 1"></div>
      <div class="paso" [class.paso--activo]="paso === 2">
        <span class="paso__numero">2</span>
        <span class="paso__etiqueta">Practicar</span>
      </div>
    </div>
  `,
  styles: [
    `
      .pasos {
        display: flex;
        align-items: center;
        gap: 0.5rem;
        margin-bottom: 1.5rem;
      }
      .paso {
        display: flex;
        align-items: center;
        gap: 0.5rem;
        color: var(--texto-secundario);
      }
      .paso__numero {
        width: 1.6rem;
        height: 1.6rem;
        flex-shrink: 0;
        border-radius: 50%;
        background: var(--fondo);
        border: 1.5px solid var(--borde);
        display: inline-flex;
        align-items: center;
        justify-content: center;
        font-size: 0.8rem;
        font-weight: 700;
      }
      .paso__etiqueta {
        font-size: 0.85rem;
        font-weight: 600;
      }
      .paso--activo {
        color: var(--color-primario);
      }
      .paso--activo .paso__numero {
        background: var(--color-primario);
        border-color: var(--color-primario);
        color: #fff;
      }
      .paso--hecho .paso__numero {
        background: var(--color-exito);
        border-color: var(--color-exito);
        color: #fff;
      }
      .paso__linea {
        width: 2.5rem;
        height: 2px;
        background: var(--borde);
      }
      .paso__linea--hecha {
        background: var(--color-exito);
      }
    `,
  ],
})
export class PasosAprendizaje {
  /** 1 = pantalla de Aprender (explicación + ejemplos), 2 = pantalla de Practicar. */
  @Input() paso: 1 | 2 = 1;
}
