import { Injectable, signal } from '@angular/core';

/** Texto-a-voz nativo del navegador (Web Speech API) — sin costo de licencia, sin backend.
 * Decisión de diseño: planificacion/21-accesibilidad-lectura-y-contenido-visual.md. */
@Injectable({ providedIn: 'root' })
export class LectorVozService {
  disponible = 'speechSynthesis' in window;
  hablando = signal(false);

  leer(texto: string) {
    if (!this.disponible || !texto.trim()) return;
    window.speechSynthesis.cancel();
    const utterance = new SpeechSynthesisUtterance(texto);
    utterance.lang = 'es-CL';
    utterance.rate = 0.95;
    utterance.onstart = () => this.hablando.set(true);
    utterance.onend = () => this.hablando.set(false);
    utterance.onerror = () => this.hablando.set(false);
    window.speechSynthesis.speak(utterance);
  }

  detener() {
    if (!this.disponible) return;
    window.speechSynthesis.cancel();
    this.hablando.set(false);
  }

  alternar(texto: string) {
    if (this.hablando()) this.detener();
    else this.leer(texto);
  }
}
