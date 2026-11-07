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

// Voces de mayor calidad que el sistema instala aparte (macOS/iOS «Mejorada»/«Premium», Windows
// «Natural», Android «Neural»/red neuronal local). Suenan mucho menos robóticas que las compactas.
const RE_VOZ_DE_CALIDAD = /premium|enhanced|mejorada|natural|neural|siri/i;
// Voces «novedad» o sintetizadores antiguos: se entienden peor y distraen a un niño que lee.
const RE_VOZ_DESCARTABLE = /espeak|eddy|flo\b|grandma|grandpa|abuel|reed|rocko|sandy|shelley|bad news|bells|boing|bubbles|cellos|jester|organ|superstar|trinoids|whisper|wobble|zarvox|albert|fred|junior|ralph|kathy/i;
// Variantes de español de América: más cercanas al habla chilena que el español de España.
const ESPANOL_AMERICA = new Set(['es-419', 'es-us', 'es-mx', 'es-ar', 'es-co', 'es-pe', 'es-ve', 'es-uy', 'es-bo', 'es-ec', 'es-py']);

/** Puntaje de una voz para el idioma pedido: calidad primero, luego cercanía de la variante. */
export function puntajeVoz(v: SpeechSynthesisVoice, idioma: string): number {
  const lang = normalizarIdioma(v.lang);
  let puntaje = 0;
  if (RE_VOZ_DE_CALIDAD.test(v.name)) puntaje += 100;
  if (RE_VOZ_DESCARTABLE.test(v.name)) puntaje -= 200;
  if (lang === normalizarIdioma(idioma)) puntaje += 30;
  else if (idiomaBase(idioma) === 'es' && ESPANOL_AMERICA.has(lang)) puntaje += 20;
  if (v.default) puntaje += 5;
  return puntaje;
}

/** Corta el texto en frases cortas: la voz hace pausas naturales entre ellas y Chrome no corta
 * las lecturas largas (detiene en silencio las que pasan de ~15 segundos). */
export function fragmentarTexto(texto: string, maximo = 220): string[] {
  // Solo se corta en puntuación seguida de espacio: «3.5» o «1:30» no se parten.
  const frases = texto.replace(/\s+/g, ' ').trim().split(/(?<=[.!?;:])\s+/);
  const fragmentos: string[] = [];
  let actual = '';
  for (const frase of frases.map((f) => f.trim()).filter(Boolean)) {
    if (actual && (actual + ' ' + frase).length > maximo) {
      fragmentos.push(actual);
      actual = frase;
    } else actual = actual ? actual + ' ' + frase : frase;
  }
  if (actual) fragmentos.push(actual);
  return fragmentos.length ? fragmentos : [texto];
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
    // Solo voces locales: una voz remota enviaría el texto fuera del dispositivo.
    const compatibles = this.voces().filter((v) => v.localService && v.lang && idiomaBase(v.lang) === base);
    if (!compatibles.length) return null;
    return [...compatibles].sort((a, b) => puntajeVoz(b, buscado) - puntajeVoz(a, buscado))[0];
  }

  leer(texto: string, opciones: OpcionesLectura = {}): ResultadoLectura {
    if (!this.sintesis) return 'no-soportado';
    if (!texto.trim()) return 'texto-vacio';
    const idioma = opciones.idioma ?? IDIOMA_POR_DEFECTO;
    const requiereVoz = idiomaBase(idioma) !== idiomaBase(IDIOMA_POR_DEFECTO);
    if (!this.voces().length) this.cargarVoces();
    // En español se elige la mejor voz local disponible; si no hay ninguna, el navegador usa la
    // suya. En otro idioma, sin voz propia no se lee (una voz española leería mal el inglés).
    const voz = this.vozPara(idioma);
    if (requiereVoz && !voz) return 'sin-voz';

    this.detener();
    const turno = this.turno;
    const velocidad = Math.min(VELOCIDAD_MAXIMA, Math.max(VELOCIDAD_MINIMA, opciones.velocidad ?? VELOCIDAD_POR_DEFECTO));
    const terminar = () => {
      if (turno !== this.turno) return;
      this.hablando.set(false);
      this.origenActivo.set(null);
    };
    const fragmentos = fragmentarTexto(texto);
    this.origenActivo.set(opciones.origen ?? null);
    fragmentos.forEach((fragmento, i) => {
      const utterance = new SpeechSynthesisUtterance(fragmento);
      utterance.lang = voz?.lang ?? idioma;
      if (voz) utterance.voice = voz;
      utterance.rate = velocidad;
      utterance.onstart = () => {
        if (turno === this.turno) this.hablando.set(true);
      };
      // Termina con el último fragmento, o antes si alguno falla.
      utterance.onerror = terminar;
      if (i === fragmentos.length - 1) utterance.onend = terminar;
      this.sintesis!.speak(utterance);
    });
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
