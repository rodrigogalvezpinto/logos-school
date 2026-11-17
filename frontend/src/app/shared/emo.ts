import { Component, computed, input, signal } from '@angular/core';

/**
 * Ícono de la interfaz dibujado como imagen (2026-11-17), en lugar de un emoji de texto: los emoji se veían distinto
 * según el equipo (a veces un cuadrado vacío) y no siempre se imprimían. `<app-emo e="📚" />` muestra
 * `/assets/pictogramas/ui-1f4da.svg` (OpenMoji, CC BY-SA 4.0: un solo estilo para toda la interfaz). Es decorativo:
 * el texto que lo acompaña ya dice lo que significa. Si falta el archivo, se muestra el emoji tal cual.
 */
@Component({
  selector: 'app-emo',
  standalone: true,
  template: `@if (!fallo() && archivo()) {<img class="emo" [src]="archivo()" alt="" aria-hidden="true" draggable="false" (error)="fallo.set(true)" />} @else {{{ e() }}}`,
  styles: [`:host { display: inline-flex; align-items: center; justify-content: center; line-height: 1; vertical-align: -0.15em; } .emo { width: 1.2em; height: 1.2em; object-fit: contain; }`],
})
export class Emo {
  readonly e = input<string>('');
  readonly fallo = signal(false);
  readonly archivo = computed(() => {
    const cps = [...(this.e() ?? '')].filter((c) => c !== '\u{FE0F}').map((c) => c.codePointAt(0)!.toString(16));
    return cps.length ? `/assets/pictogramas/ui-${cps.join('-')}.svg` : '';
  });
}
