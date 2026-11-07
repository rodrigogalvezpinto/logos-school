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

function voz(lang: string, nombre = lang, localService = true, porDefecto = false): SpeechSynthesisVoice {
  return { lang, name: nombre, localService, default: porDefecto, voiceURI: nombre } as SpeechSynthesisVoice;
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

    it('lee en español es-CL a 0.95 por defecto con la voz local de Chile', () => {
      expect(lector.leer('Hola')).toBe('iniciado');
      const u = mock.estado.habladas[0];
      expect(u.lang).toBe('es-CL');
      expect(u.rate).toBe(0.95);
      expect(u.voice?.name).toBe('es-CL');
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

  describe('mejor voz española del dispositivo', () => {
    it('prefiere una voz de calidad («Mejorada») aunque sea de otra variante', () => {
      instalarSintesisFalsa([voz('es-ES', 'Mónica', true, true), voz('es-MX', 'Paulina (Mejorada)'), voz('es-CL', 'Chile compacta')]);
      expect(new LectorVozService().vozPara('es-CL')?.name).toBe('Paulina (Mejorada)');
    });

    it('a igual calidad prefiere Chile, luego América, luego España', () => {
      instalarSintesisFalsa([voz('es-ES', 'Mónica'), voz('es-MX', 'Paulina')]);
      expect(new LectorVozService().vozPara('es-CL')?.name).toBe('Paulina');
      instalarSintesisFalsa([voz('es-ES', 'Mónica'), voz('es-MX', 'Paulina'), voz('es-CL', 'Chile')]);
      expect(new LectorVozService().vozPara('es-CL')?.name).toBe('Chile');
    });

    it('descarta voces novedad y sintetizadores robóticos', () => {
      instalarSintesisFalsa([voz('es-CL', 'Eddy (español (Chile))'), voz('es-ES', 'Mónica'), voz('es', 'eSpeak Spanish')]);
      expect(new LectorVozService().vozPara('es-CL')?.name).toBe('Mónica');
    });

    it('nunca elige una voz remota, aunque sea de calidad', () => {
      instalarSintesisFalsa([voz('es-CL', 'Remota Natural', false), voz('es-ES', 'Mónica')]);
      expect(new LectorVozService().vozPara('es-CL')?.name).toBe('Mónica');
    });

    it('sin voces españolas igual lee con la voz por defecto del navegador', () => {
      const mock = instalarSintesisFalsa([voz('en-US', 'US')]);
      expect(new LectorVozService().leer('Hola')).toBe('iniciado');
      expect(mock.estado.habladas[0].voice).toBeNull();
    });
  });

  describe('lectura por frases', () => {
    it('divide un texto largo en frases y solo termina con la última', () => {
      const mock = instalarSintesisFalsa([voz('es-CL')]);
      const lector = new LectorVozService();
      const frase = 'El gato está debajo de la mesa y mira a la niña que juega. ';
      lector.leer(frase.repeat(8));
      const habladas = mock.estado.habladas;
      expect(habladas.length).toBeGreaterThan(1);
      expect(habladas.every((u) => u.text.length <= 220)).toBe(true);
      expect(habladas.map((u) => u.text).join(' ')).toBe(frase.repeat(8).trim());
      habladas[0].onstart?.();
      habladas[0].onend?.();
      expect(lector.hablando()).toBe(true);
      habladas[habladas.length - 1].onend?.();
      expect(lector.hablando()).toBe(false);
    });
  });

  it('no parte decimales ni horas', async () => {
    const { fragmentarTexto } = await import('./lector-voz.service');
    expect(fragmentarTexto('Mide 3.5 cm. Llega a las 1:30.', 12)).toEqual(['Mide 3.5 cm.', 'Llega a las 1:30.']);
  });
});

describe('LectorVozService - audio pregrabado (voz neuronal)', () => {
  class AudioFalso {
    static creados: AudioFalso[] = [];
    onplaying: (() => void) | null = null;
    onended: (() => void) | null = null;
    onerror: ((e: Event) => void) | null = null;
    pause = vi.fn();
    play = vi.fn(() => Promise.resolve());
    constructor(public src: string) {
      AudioFalso.creados.push(this);
    }
  }
  const audioOriginal = (globalThis as Record<string, unknown>)['Audio'];

  beforeEach(() => {
    AudioFalso.creados = [];
    (globalThis as Record<string, unknown>)['Audio'] = AudioFalso;
  });
  afterEach(() => {
    (globalThis as Record<string, unknown>)['Audio'] = audioOriginal;
    desinstalarSintesisFalsa();
  });

  async function lectorConAudios(textos: string[]) {
    const { claveAudio } = await import('./audio-pregrabado');
    const fetchFalso = vi.fn(async () => ({ ok: true, json: async () => ({ voz: 'piper', claves: textos.map(claveAudio) }) }));
    vi.stubGlobal('fetch', fetchFalso);
    const mock = instalarSintesisFalsa([voz('es-CL')]);
    const lector = new LectorVozService();
    await lector.cargarManifiesto();
    vi.unstubAllGlobals();
    return { lector, mock, claveAudio };
  }

  it('usa el audio pregrabado cuando existe para ese texto exacto', async () => {
    const { lector, mock, claveAudio } = await lectorConAudios(['El gato está … de la mesa.']);
    expect(lector.leer('El gato está … de la mesa.')).toBe('iniciado');
    expect(AudioFalso.creados[0].src).toBe(`audio/es/${claveAudio('El gato está … de la mesa.')}.m4a`);
    expect(mock.sintesis.speak).not.toHaveBeenCalled();
    expect(lector.hablando()).toBe(true);
    AudioFalso.creados[0].onended?.();
    expect(lector.hablando()).toBe(false);
  });

  it('sin audio para ese texto, o en inglés, usa la voz del dispositivo', async () => {
    const { lector, mock } = await lectorConAudios(['Otro texto.']);
    lector.leer('Texto sin audio.');
    lector.leer('apple', { idioma: 'en-US' });
    expect(AudioFalso.creados.length).toBe(0);
    expect(mock.sintesis.speak).toHaveBeenCalled();
  });

  it('si el archivo no carga, cae a la voz del dispositivo', async () => {
    const { lector, mock } = await lectorConAudios(['Hola.']);
    lector.leer('Hola.');
    AudioFalso.creados[0].onerror?.(new Event('error'));
    expect(mock.estado.habladas[0].text).toBe('Hola.');
  });

  it('detener pausa el audio', async () => {
    const { lector } = await lectorConAudios(['Hola.']);
    lector.leer('Hola.');
    lector.detener();
    expect(AudioFalso.creados[0].pause).toHaveBeenCalled();
    expect(lector.hablando()).toBe(false);
  });

  it('la clave es estable para el mismo texto y distinta para otro', async () => {
    const { claveAudio } = await import('./audio-pregrabado');
    expect(claveAudio('Hola.')).toBe(claveAudio('Hola.'));
    expect(claveAudio('Hola.')).not.toBe(claveAudio('Hola!'));
    expect(claveAudio('Hola.')).toMatch(/^[0-9a-f]{16}$/);
  });
});
