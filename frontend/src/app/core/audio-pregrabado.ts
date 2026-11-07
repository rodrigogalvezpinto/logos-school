/**
 * Audio pregrabado con una voz neuronal libre (Piper, `es_MX-claude-high`, licencia Apache-2.0),
 * generado fuera de línea con `scripts/voz/generar_audios.sh`. Suena igual en todos los equipos y
 * no envía texto a ningún servicio. Cada archivo se nombra con la clave del texto exacto que se
 * lee; si el texto cambia (o no hay audio), el lector usa la voz del dispositivo.
 */
export const RUTA_AUDIO = 'audio/es';

/** FNV-1a de 64 bits (dos pasadas de 32) en hexadecimal: estable entre navegador y generador. */
export function claveAudio(texto: string): string {
  const bytes = new TextEncoder().encode(texto.normalize('NFC'));
  let a = 0x811c9dc5;
  let b = 0x01000193 ^ 0x5bd1e995;
  for (const byte of bytes) {
    a = Math.imul(a ^ byte, 0x01000193) >>> 0;
    b = Math.imul(b ^ byte, 0x01000193 + 0x2c) >>> 0;
  }
  return a.toString(16).padStart(8, '0') + b.toString(16).padStart(8, '0');
}

export interface ManifiestoAudio {
  voz: string;
  claves: string[];
}
