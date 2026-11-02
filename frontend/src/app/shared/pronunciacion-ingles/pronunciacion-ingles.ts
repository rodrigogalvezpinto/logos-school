import { Component, OnDestroy, computed, inject, signal } from '@angular/core';
import { LectorVozService } from '../../core/lector-voz.service';

export const IDIOMA_PRONUNCIACION = 'en-US';
export const VELOCIDAD_NORMAL = 1;
export const VELOCIDAD_LENTA = 0.7;
export const MAX_CARACTERES_PRONUNCIACION = 120;
export const MAX_PALABRAS_PRONUNCIACION = 20;

export const MENSAJES_PRONUNCIACION = {
  noSoportado:
    'Este navegador no permite escuchar pronunciación. Prueba con otro navegador o dispositivo actualizado.',
  sinVoz:
    'No encontramos una voz en inglés instalada en este dispositivo. Puedes agregar una voz en inglés en la configuración del sistema o probar otro navegador.',
  vacio: 'Escribe o pega primero una palabra o frase breve en inglés.',
  muyLargo: `Usa una palabra o frase breve (máximo ${MAX_PALABRAS_PRONUNCIACION} palabras).`,
  reproduciendo: 'Reproduciendo en inglés…',
  detenido: 'Reproducción detenida.',
};

let contadorPaneles = 0;

@Component({
  selector: 'app-pronunciacion-ingles',
  standalone: true,
  template: `
    <section class="pronunciacion" [attr.aria-labelledby]="idPanel + '-titulo'">
      <h2 class="pronunciacion__titulo" [id]="idPanel + '-titulo'">Practica la pronunciación en inglés</h2>
      <p class="pronunciacion__ayuda">
        Copia o escribe una palabra o frase breve de la guía. Solo se lee en inglés lo que pongas aquí; la voz
        la genera tu navegador y puede variar según el dispositivo.
      </p>
      @if (lector.disponible) {
        <label class="pronunciacion__etiqueta" [attr.for]="idPanel + '-texto'">Palabra o frase en inglés</label>
        <input
          [id]="idPanel + '-texto'"
          class="pronunciacion__campo"
          type="text"
          lang="en"
          autocomplete="off"
          spellcheck="false"
          [attr.maxlength]="maxCaracteres"
          [value]="texto()"
          (input)="alEscribir($event)"
          (keydown.enter)="escuchar()"
        />
        <fieldset class="pronunciacion__velocidad">
          <legend>Velocidad</legend>
          <label>
            <input
              type="radio"
              [name]="idPanel + '-velocidad'"
              [checked]="velocidad() === velocidadNormal"
              (change)="velocidad.set(velocidadNormal)"
            />
            Normal
          </label>
          <label>
            <input
              type="radio"
              [name]="idPanel + '-velocidad'"
              [checked]="velocidad() === velocidadLenta"
              (change)="velocidad.set(velocidadLenta)"
            />
            Lenta
          </label>
        </fieldset>
        <div class="pronunciacion__acciones">
          <button type="button" class="pronunciacion__boton" (click)="escuchar()">Escuchar en inglés</button>
          <button type="button" class="pronunciacion__boton" (click)="repetir()" [disabled]="!ultimoTexto()">
            Repetir
          </button>
          <button type="button" class="pronunciacion__boton" (click)="detener()" [disabled]="!activo()">
            Detener
          </button>
        </div>
      }
      <p class="pronunciacion__estado" role="status" aria-live="polite">{{ estado() }}</p>
    </section>
  `,
  styles: [
    `
      .pronunciacion {
        max-width: 680px;
        margin: 0 0 1.5rem;
        padding: 1rem 1.25rem;
        border: 1px solid var(--borde);
        border-radius: var(--radio-media);
        background: var(--color-primario-suave);
      }
      .pronunciacion__titulo {
        font-size: 1.05rem;
        margin: 0 0 0.4rem;
      }
      .pronunciacion__ayuda {
        margin: 0 0 0.75rem;
        font-size: 0.9rem;
        color: var(--texto-principal);
      }
      .pronunciacion__etiqueta {
        display: block;
        font-weight: 600;
        margin-bottom: 0.3rem;
      }
      .pronunciacion__campo {
        width: 100%;
        box-sizing: border-box;
        padding: 0.5rem 0.75rem;
        font-size: 1rem;
        border: 1px solid var(--borde);
        border-radius: var(--radio-media);
      }
      .pronunciacion__velocidad {
        display: flex;
        gap: 1rem;
        border: none;
        padding: 0;
        margin: 0.75rem 0;
      }
      .pronunciacion__velocidad legend {
        font-weight: 600;
        margin-bottom: 0.3rem;
      }
      .pronunciacion__acciones {
        display: flex;
        flex-wrap: wrap;
        gap: 0.5rem;
      }
      .pronunciacion__boton {
        background: var(--color-primario);
        color: #fff;
        border: none;
        border-radius: 999px;
        padding: 0.5rem 1rem;
        font-size: 0.9rem;
        font-weight: 600;
        cursor: pointer;
      }
      .pronunciacion__boton:disabled {
        opacity: 0.5;
        cursor: not-allowed;
      }
      .pronunciacion__estado {
        min-height: 1.2em;
        margin: 0.6rem 0 0;
        font-size: 0.9rem;
      }
    `,
  ],
})
export class PronunciacionIngles implements OnDestroy {
  lector = inject(LectorVozService);

  readonly idPanel = `pronunciacion-ingles-${++contadorPaneles}`;
  readonly velocidadNormal = VELOCIDAD_NORMAL;
  readonly velocidadLenta = VELOCIDAD_LENTA;
  readonly maxCaracteres = MAX_CARACTERES_PRONUNCIACION;

  texto = signal('');
  velocidad = signal(VELOCIDAD_NORMAL);
  ultimoTexto = signal('');
  mensaje = signal(this.lector.disponible ? '' : MENSAJES_PRONUNCIACION.noSoportado);

  activo = computed(() => this.lector.origenActivo() === this.idPanel);
  estado = computed(() => (this.activo() ? MENSAJES_PRONUNCIACION.reproduciendo : this.mensaje()));

  alEscribir(evento: Event) {
    this.texto.set((evento.target as HTMLInputElement).value);
  }

  escuchar() {
    this.reproducir(this.texto());
  }

  repetir() {
    this.reproducir(this.ultimoTexto());
  }

  detener() {
    this.lector.detenerOrigen(this.idPanel);
    this.mensaje.set(MENSAJES_PRONUNCIACION.detenido);
  }

  ngOnDestroy() {
    this.lector.detenerOrigen(this.idPanel);
  }

  private reproducir(crudo: string) {
    const frase = crudo.trim().replace(/\s+/g, ' ').slice(0, MAX_CARACTERES_PRONUNCIACION);
    if (!frase) {
      this.mensaje.set(MENSAJES_PRONUNCIACION.vacio);
      return;
    }
    if (frase.split(' ').length > MAX_PALABRAS_PRONUNCIACION) {
      this.mensaje.set(MENSAJES_PRONUNCIACION.muyLargo);
      return;
    }
    const resultado = this.lector.leer(frase, {
      idioma: IDIOMA_PRONUNCIACION,
      velocidad: this.velocidad(),
      origen: this.idPanel,
    });
    if (resultado === 'iniciado') {
      this.ultimoTexto.set(frase);
      this.mensaje.set('');
    } else if (resultado === 'sin-voz') {
      this.mensaje.set(MENSAJES_PRONUNCIACION.sinVoz);
    } else if (resultado === 'no-soportado') {
      this.mensaje.set(MENSAJES_PRONUNCIACION.noSoportado);
    } else {
      this.mensaje.set(MENSAJES_PRONUNCIACION.vacio);
    }
  }
}
