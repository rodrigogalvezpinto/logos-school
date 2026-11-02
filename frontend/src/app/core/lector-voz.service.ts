import { Injectable, OnDestroy, signal } from '@angular/core';

export interface OpcionesLectura {
  idioma?: string;
  velocidad?: number;
  origen?: string;
}

export type ResultadoLectura = 'iniciado' | 'no-soportado' | 'texto-vacio' | 'sin-voz';

const IDIOMA_POR_DEFECTO = 'es-CL';
const VELOCIDAD_POR_DEFECTO = 0.95;
const VELOCIDAD_MINIMA = 0.5;
const VELOCIDAD_MAXIMA = 1.5;

function normalizarIdioma(idioma: string): string {
  return idioma.replace('_', '-').toLowerCase();
}

function idiomaBase(idioma: string): string {
  return normalizarIdioma(idioma).split('-')[0];
}

/** Texto-a-voz nativo del navegador (Web Speech API) — sin costo de licencia, sin backend.
 * Decisión de diseño: planificacion/21-accesibilidad-lectura-y-contenido-visual.md. */
@Injectable({ providedIn: 'root' })
export class LectorVozService implements OnDestroy {
  disponible = typeof window !== 'undefined' && 'speechSynthesis' in window && 'SpeechSynthesisUtterance' in window;
  hablando = signal(false);
  origenActivo = signal<string | null>(null);
  voces = signal<SpeechSynthesisVoice[]>([]);

  private sintesis: SpeechSynthesis | null = this.disponible ? window.speechSynthesis : null;
  private turno = 0;
  private alCambiarVoces = () => this.cargarVoces();

  constructor() {
    if (!this.sintesis) return;
    this.cargarVoces();
    this.sintesis.addEventListener?.('voiceschanged', this.alCambiarVoces);
  }

  ngOnDestroy() {
    this.sintesis?.removeEventListener?.('voiceschanged', this.alCambiarVoces);
  }

  cargarVoces() {
    if (!this.sintesis) return;
    this.voces.set(this.sintesis.getVoices() ?? []);
  }

  vozPara(idioma: string): SpeechSynthesisVoice | null {
    const buscado = normalizarIdioma(idioma);
    const base = idiomaBase(idioma);
    const compatibles = this.voces().filter((v) => v.localService && v.lang && idiomaBase(v.lang) === base);
    return compatibles.find((v) => normalizarIdioma(v.lang) === buscado) ?? compatibles[0] ?? null;
  }

  leer(texto: string, opciones: OpcionesLectura = {}): ResultadoLectura {
    if (!this.sintesis) return 'no-soportado';
    if (!texto.trim()) return 'texto-vacio';
    const idioma = opciones.idioma ?? IDIOMA_POR_DEFECTO;
    const requiereVoz = idiomaBase(idioma) !== idiomaBase(IDIOMA_POR_DEFECTO);
    let voz: SpeechSynthesisVoice | null = null;
    if (requiereVoz) {
      if (!this.voces().length) this.cargarVoces();
      voz = this.vozPara(idioma);
      if (!voz) return 'sin-voz';
    }

    this.detener();
    const turno = this.turno;
    const utterance = new SpeechSynthesisUtterance(texto);
    utterance.lang = voz?.lang ?? idioma;
    if (voz) utterance.voice = voz;
    const velocidad = opciones.velocidad ?? VELOCIDAD_POR_DEFECTO;
    utterance.rate = Math.min(VELOCIDAD_MAXIMA, Math.max(VELOCIDAD_MINIMA, velocidad));
    const terminar = () => {
      if (turno !== this.turno) return;
      this.hablando.set(false);
      this.origenActivo.set(null);
    };
    utterance.onstart = () => {
      if (turno === this.turno) this.hablando.set(true);
    };
    utterance.onend = terminar;
    utterance.onerror = terminar;
    this.origenActivo.set(opciones.origen ?? null);
    this.sintesis.speak(utterance);
    return 'iniciado';
  }

  detener() {
    if (!this.sintesis) return;
    this.turno++;
    this.sintesis.cancel();
    this.hablando.set(false);
    this.origenActivo.set(null);
  }

  detenerOrigen(origen: string) {
    if (this.origenActivo() === origen) this.detener();
  }

  alternar(texto: string, opciones: OpcionesLectura = {}): ResultadoLectura | 'detenido' {
    if (this.hablando()) {
      this.detener();
      return 'detenido';
    }
    return this.leer(texto, opciones);
  }
}
