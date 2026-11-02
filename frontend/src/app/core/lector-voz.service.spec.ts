import { describe, it, expect, beforeEach, afterEach, vi } from 'vitest';
import { LectorVozService } from './lector-voz.service';

class UtteranceFalsa {
  lang = '';
  rate = 1;
  voice: SpeechSynthesisVoice | null = null;
  onstart: (() => void) | null = null;
  onend: (() => void) | null = null;
  onerror: (() => void) | null = null;
  constructor(public text: string) {}
}

function voz(lang: string, nombre = lang, localService = true): SpeechSynthesisVoice {
  return { lang, name: nombre, localService, default: false, voiceURI: nombre } as SpeechSynthesisVoice;
}

function instalarSintesisFalsa(vocesIniciales: SpeechSynthesisVoice[] = []) {
  const estado = {
    voces: vocesIniciales,
    habladas: [] as UtteranceFalsa[],
    oyentes: {} as Record<string, () => void>,
  };
  const sintesis = {
    speak: vi.fn((u: UtteranceFalsa) => estado.habladas.push(u)),
    cancel: vi.fn(),
    getVoices: vi.fn(() => estado.voces),
    addEventListener: vi.fn((evento: string, cb: () => void) => (estado.oyentes[evento] = cb)),
    removeEventListener: vi.fn(),
  };
  Object.defineProperty(window, 'speechSynthesis', { value: sintesis, configurable: true, writable: true });
  Object.defineProperty(window, 'SpeechSynthesisUtterance', {
    value: UtteranceFalsa,
    configurable: true,
    writable: true,
  });
  return { sintesis, estado };
}

function desinstalarSintesisFalsa() {
  delete (window as unknown as Record<string, unknown>)['speechSynthesis'];
  delete (window as unknown as Record<string, unknown>)['SpeechSynthesisUtterance'];
}

describe('LectorVozService - idioma, velocidad y voces', () => {
  afterEach(() => desinstalarSintesisFalsa());

  describe('con Web Speech API disponible', () => {
    let mock: ReturnType<typeof instalarSintesisFalsa>;
    let lector: LectorVozService;

    beforeEach(() => {
      mock = instalarSintesisFalsa([voz('es-CL'), voz('en-GB', 'UK'), voz('en-US', 'US')]);
      lector = new LectorVozService();
    });

    it('mantiene español es-CL a 0.95 por defecto sin forzar voz', () => {
      expect(lector.leer('Hola')).toBe('iniciado');
      const u = mock.estado.habladas[0];
      expect(u.lang).toBe('es-CL');
      expect(u.rate).toBe(0.95);
      expect(u.voice).toBeNull();
    });

    it('lee en inglés con voz local en-US y la velocidad pedida', () => {
      expect(lector.leer('apple', { idioma: 'en-US', velocidad: 0.7 })).toBe('iniciado');
      const u = mock.estado.habladas[0];
      expect(u.lang).toBe('en-US');
      expect(u.voice?.name).toBe('US');
      expect(u.rate).toBe(0.7);
    });

    it('acota la velocidad a un rango seguro', () => {
      lector.leer('fast', { idioma: 'en-US', velocidad: 9 });
      lector.leer('slow', { idioma: 'en-US', velocidad: 0.1 });
      expect(mock.estado.habladas[0].rate).toBe(1.5);
      expect(mock.estado.habladas[1].rate).toBe(0.5);
    });

    it('usa otra variante inglesa si no existe la exacta', () => {
      mock.estado.voces = [voz('es-CL'), voz('en_GB', 'UK')];
      lector.cargarVoces();
      lector.leer('water', { idioma: 'en-US' });
      expect(mock.estado.habladas[0].voice?.name).toBe('UK');
    });

    it('ignora texto vacío', () => {
      expect(lector.leer('   ', { idioma: 'en-US' })).toBe('texto-vacio');
      expect(mock.sintesis.speak).not.toHaveBeenCalled();
    });

    it('no reproduce el final tardío de una lectura cancelada sobre la nueva', () => {
      lector.leer('primera', { idioma: 'en-US' });
      const primera = mock.estado.habladas[0];
      lector.leer('segunda', { idioma: 'en-US' });
      const segunda = mock.estado.habladas[1];
      segunda.onstart?.();
      expect(lector.hablando()).toBe(true);
      primera.onerror?.();
      primera.onend?.();
      expect(lector.hablando()).toBe(true);
      segunda.onend?.();
      expect(lector.hablando()).toBe(false);
    });

    it('detener cancela y bloquea un onstart tardío', () => {
      lector.leer('hello', { idioma: 'en-US', origen: 'panel' });
      const u = mock.estado.habladas[0];
      expect(lector.origenActivo()).toBe('panel');
      lector.detener();
      expect(mock.sintesis.cancel).toHaveBeenCalled();
      u.onstart?.();
      expect(lector.hablando()).toBe(false);
      expect(lector.origenActivo()).toBeNull();
    });

    it('detenerOrigen solo detiene la lectura de ese origen', () => {
      lector.leer('guía', { origen: 'otro' });
      mock.sintesis.cancel.mockClear();
      lector.detenerOrigen('panel');
      expect(mock.sintesis.cancel).not.toHaveBeenCalled();
      lector.detenerOrigen('otro');
      expect(mock.sintesis.cancel).toHaveBeenCalledTimes(1);
    });

    it('alternar detiene si ya está hablando', () => {
      lector.leer('hola');
      mock.estado.habladas[0].onstart?.();
      expect(lector.alternar('hola')).toBe('detenido');
      expect(lector.hablando()).toBe(false);
    });

    it('libera el oyente voiceschanged al destruirse', () => {
      lector.ngOnDestroy();
      expect(mock.sintesis.removeEventListener).toHaveBeenCalledWith('voiceschanged', expect.any(Function));
    });
  });

  describe('selección de voz inglesa', () => {
    it('nunca usa una voz española para inglés', () => {
      const mock = instalarSintesisFalsa([voz('es-CL'), voz('es-ES')]);
      const lector = new LectorVozService();
      expect(lector.leer('apple', { idioma: 'en-US' })).toBe('sin-voz');
      expect(mock.sintesis.speak).not.toHaveBeenCalled();
    });

    it('no usa voces remotas que enviarían el texto fuera del dispositivo', () => {
      const mock = instalarSintesisFalsa([voz('en-US', 'Remota', false)]);
      const lector = new LectorVozService();
      expect(lector.vozPara('en-US')).toBeNull();
      expect(lector.leer('apple', { idioma: 'en-US' })).toBe('sin-voz');
      expect(mock.sintesis.speak).not.toHaveBeenCalled();
    });

    it('recoge voces que llegan después con voiceschanged', () => {
      const mock = instalarSintesisFalsa([]);
      const lector = new LectorVozService();
      expect(lector.vozPara('en-US')).toBeNull();
      mock.estado.voces = [voz('en-US', 'US')];
      mock.estado.oyentes['voiceschanged']();
      expect(lector.voces().length).toBe(1);
      expect(lector.leer('apple', { idioma: 'en-US' })).toBe('iniciado');
    });
  });

  describe('sin Web Speech API', () => {
    it('informa no soportado sin lanzar errores', () => {
      desinstalarSintesisFalsa();
      const lector = new LectorVozService();
      expect(lector.disponible).toBe(false);
      expect(lector.leer('hola')).toBe('no-soportado');
      expect(lector.leer('apple', { idioma: 'en-US' })).toBe('no-soportado');
      expect(() => lector.detener()).not.toThrow();
    });
  });
});
