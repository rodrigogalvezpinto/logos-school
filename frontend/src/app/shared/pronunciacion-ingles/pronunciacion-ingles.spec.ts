import { describe, it, expect, beforeEach, afterEach, vi } from 'vitest';
import { TestBed, ComponentFixture } from '@angular/core/testing';
import { LectorVozService } from '../../core/lector-voz.service';
import { MENSAJES_PRONUNCIACION, PronunciacionIngles, VELOCIDAD_LENTA } from './pronunciacion-ingles';

class UtteranceFalsa {
  lang = '';
  rate = 1;
  voice: SpeechSynthesisVoice | null = null;
  onstart: (() => void) | null = null;
  onend: (() => void) | null = null;
  onerror: (() => void) | null = null;
  constructor(public text: string) {}
}

function voz(lang: string, localService = true): SpeechSynthesisVoice {
  return { lang, name: lang, localService, default: false, voiceURI: lang } as SpeechSynthesisVoice;
}

function instalarSintesis(voces: SpeechSynthesisVoice[]) {
  const habladas: UtteranceFalsa[] = [];
  const sintesis = {
    speak: vi.fn((u: UtteranceFalsa) => habladas.push(u)),
    cancel: vi.fn(),
    getVoices: vi.fn(() => voces),
    addEventListener: vi.fn(),
    removeEventListener: vi.fn(),
  };
  Object.defineProperty(window, 'speechSynthesis', { value: sintesis, configurable: true, writable: true });
  Object.defineProperty(window, 'SpeechSynthesisUtterance', { value: UtteranceFalsa, configurable: true, writable: true });
  return { sintesis, habladas };
}

function desinstalarSintesis() {
  delete (window as unknown as Record<string, unknown>)['speechSynthesis'];
  delete (window as unknown as Record<string, unknown>)['SpeechSynthesisUtterance'];
}

function crear(): ComponentFixture<PronunciacionIngles> {
  TestBed.resetTestingModule();
  TestBed.configureTestingModule({ imports: [PronunciacionIngles] });
  const fixture = TestBed.createComponent(PronunciacionIngles);
  fixture.detectChanges();
  return fixture;
}

function escribir(fixture: ComponentFixture<PronunciacionIngles>, texto: string) {
  const campo = fixture.nativeElement.querySelector('input[type="text"]') as HTMLInputElement;
  campo.value = texto;
  campo.dispatchEvent(new Event('input'));
  fixture.detectChanges();
}

function boton(fixture: ComponentFixture<PronunciacionIngles>, texto: string): HTMLButtonElement {
  const botones = Array.from(fixture.nativeElement.querySelectorAll('button')) as HTMLButtonElement[];
  return botones.find((b) => b.textContent?.trim() === texto)!;
}

function estado(fixture: ComponentFixture<PronunciacionIngles>): string {
  return (fixture.nativeElement.querySelector('[role="status"]') as HTMLElement).textContent?.trim() ?? '';
}

describe('PronunciacionIngles - panel de pronunciación', () => {
  afterEach(() => desinstalarSintesis());

  describe('con voz inglesa local', () => {
    let mock: ReturnType<typeof instalarSintesis>;
    let fixture: ComponentFixture<PronunciacionIngles>;

    beforeEach(() => {
      mock = instalarSintesis([voz('es-CL'), voz('en-US')]);
      fixture = crear();
    });

    it('tiene etiqueta asociada, campo en inglés y región de estado accesible', () => {
      const el = fixture.nativeElement as HTMLElement;
      const campo = el.querySelector('input[type="text"]') as HTMLInputElement;
      const etiqueta = el.querySelector('label.pronunciacion__etiqueta') as HTMLLabelElement;
      expect(etiqueta.getAttribute('for')).toBe(campo.id);
      expect(campo.getAttribute('lang')).toBe('en');
      expect(el.querySelector('[role="status"]')?.getAttribute('aria-live')).toBe('polite');
      expect(el.querySelector('section')?.getAttribute('aria-labelledby')).toBe(el.querySelector('h2')?.id);
      expect(boton(fixture, 'Repetir').disabled).toBe(true);
      expect(boton(fixture, 'Detener').disabled).toBe(true);
    });

    it('escucha solo la frase escrita, en en-US y velocidad normal', () => {
      escribir(fixture, '  good   morning ');
      boton(fixture, 'Escuchar en inglés').click();
      fixture.detectChanges();
      expect(mock.habladas.length).toBe(1);
      expect(mock.habladas[0].text).toBe('good morning');
      expect(mock.habladas[0].lang).toBe('en-US');
      expect(mock.habladas[0].voice?.lang).toBe('en-US');
      expect(mock.habladas[0].rate).toBe(1);
      expect(estado(fixture)).toBe(MENSAJES_PRONUNCIACION.reproduciendo);
      expect(boton(fixture, 'Detener').disabled).toBe(false);
    });

    it('velocidad lenta y repetir reutilizan la última frase', () => {
      escribir(fixture, 'thank you');
      const radios = fixture.nativeElement.querySelectorAll('input[type="radio"]') as NodeListOf<HTMLInputElement>;
      radios[1].click();
      fixture.detectChanges();
      boton(fixture, 'Escuchar en inglés').click();
      mock.habladas[0].onend?.();
      fixture.detectChanges();
      escribir(fixture, '');
      boton(fixture, 'Repetir').click();
      expect(mock.habladas.length).toBe(2);
      expect(mock.habladas[1].text).toBe('thank you');
      expect(mock.habladas[1].rate).toBe(VELOCIDAD_LENTA);
    });

    it('detener cancela y anuncia el estado', () => {
      escribir(fixture, 'apple');
      boton(fixture, 'Escuchar en inglés').click();
      fixture.detectChanges();
      boton(fixture, 'Detener').click();
      fixture.detectChanges();
      expect(mock.sintesis.cancel).toHaveBeenCalled();
      expect(estado(fixture)).toBe(MENSAJES_PRONUNCIACION.detenido);
    });

    it('valida texto vacío y frases demasiado largas sin hablar', () => {
      boton(fixture, 'Escuchar en inglés').click();
      fixture.detectChanges();
      expect(estado(fixture)).toBe(MENSAJES_PRONUNCIACION.vacio);
      escribir(fixture, Array.from({ length: 21 }, () => 'word').join(' '));
      boton(fixture, 'Escuchar en inglés').click();
      fixture.detectChanges();
      expect(estado(fixture)).toBe(MENSAJES_PRONUNCIACION.muyLargo);
      expect(mock.sintesis.speak).not.toHaveBeenCalled();
    });

    it('libera la voz al destruirse si este panel está hablando', () => {
      escribir(fixture, 'apple');
      boton(fixture, 'Escuchar en inglés').click();
      mock.sintesis.cancel.mockClear();
      fixture.destroy();
      expect(mock.sintesis.cancel).toHaveBeenCalledTimes(1);
    });

    it('no corta otra lectura al destruirse', () => {
      TestBed.inject(LectorVozService).leer('Texto de la guía');
      mock.sintesis.cancel.mockClear();
      fixture.destroy();
      expect(mock.sintesis.cancel).not.toHaveBeenCalled();
    });
  });

  it('avisa si no hay voz inglesa instalada y no usa la española', () => {
    const mock = instalarSintesis([voz('es-CL'), voz('en-US', false)]);
    const fixture = crear();
    escribir(fixture, 'apple');
    boton(fixture, 'Escuchar en inglés').click();
    fixture.detectChanges();
    expect(mock.sintesis.speak).not.toHaveBeenCalled();
    expect(estado(fixture)).toBe(MENSAJES_PRONUNCIACION.sinVoz);
  });

  it('avisa si el navegador no soporta síntesis de voz', () => {
    desinstalarSintesis();
    const fixture = crear();
    expect(fixture.nativeElement.querySelector('input[type="text"]')).toBeNull();
    expect(estado(fixture)).toBe(MENSAJES_PRONUNCIACION.noSoportado);
  });
});
