import { describe, it, expect, beforeEach, afterEach, vi } from 'vitest';
import { TestBed } from '@angular/core/testing';
import { BotonEscuchar } from './boton-escuchar';

class UtteranceFalsa {
  lang = '';
  rate = 1;
  voice: SpeechSynthesisVoice | null = null;
  onstart: (() => void) | null = null;
  onend: (() => void) | null = null;
  onerror: (() => void) | null = null;
  constructor(public text: string) {}
}

describe('BotonEscuchar - parámetros de idioma y velocidad', () => {
  let habladas: UtteranceFalsa[];

  beforeEach(() => {
    habladas = [];
    const voces = [{ lang: 'en-US', name: 'US', localService: true } as SpeechSynthesisVoice];
    Object.defineProperty(window, 'speechSynthesis', {
      value: {
        speak: vi.fn((u: UtteranceFalsa) => habladas.push(u)),
        cancel: vi.fn(),
        getVoices: () => voces,
        addEventListener: vi.fn(),
        removeEventListener: vi.fn(),
      },
      configurable: true,
      writable: true,
    });
    Object.defineProperty(window, 'SpeechSynthesisUtterance', { value: UtteranceFalsa, configurable: true, writable: true });
    TestBed.resetTestingModule();
    TestBed.configureTestingModule({ imports: [BotonEscuchar] });
  });

  afterEach(() => {
    delete (window as unknown as Record<string, unknown>)['speechSynthesis'];
    delete (window as unknown as Record<string, unknown>)['SpeechSynthesisUtterance'];
  });

  it('sin parámetros conserva español es-CL a 0.95', () => {
    const fixture = TestBed.createComponent(BotonEscuchar);
    fixture.componentRef.setInput('texto', 'Hola');
    fixture.detectChanges();
    (fixture.nativeElement.querySelector('button') as HTMLButtonElement).click();
    expect(habladas[0].lang).toBe('es-CL');
    expect(habladas[0].rate).toBe(0.95);
  });

  it('entrega idioma y velocidad explícitos al lector', () => {
    const fixture = TestBed.createComponent(BotonEscuchar);
    fixture.componentRef.setInput('texto', 'apple');
    fixture.componentRef.setInput('idioma', 'en-US');
    fixture.componentRef.setInput('velocidad', 0.7);
    fixture.detectChanges();
    (fixture.nativeElement.querySelector('button') as HTMLButtonElement).click();
    expect(habladas[0].lang).toBe('en-US');
    expect(habladas[0].rate).toBe(0.7);
  });
});
