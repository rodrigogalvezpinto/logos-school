import { describe, it, expect, beforeEach, afterEach, vi } from 'vitest';
import { TestBed } from '@angular/core/testing';
import { provideRouter } from '@angular/router';
import { of } from 'rxjs';
import { CalificacionesService } from '../../core/calificaciones.service';
import { AsignaturaRespuesta, ContenidoService, ObjetivoRespuesta } from '../../core/contenido.service';
import { OnboardingService } from '../../core/onboarding.service';
import { ProgresoService } from '../../core/progreso.service';
import { SesionService } from '../../core/sesion.service';
import { EstudiarOa, esNombreIngles } from './estudiar-oa';

class UtteranceFalsa {
  lang = '';
  rate = 1;
  voice: SpeechSynthesisVoice | null = null;
  onstart: (() => void) | null = null;
  onend: (() => void) | null = null;
  onerror: (() => void) | null = null;
  constructor(public text: string) {}
}

const GUIA_BILINGUE = 'La palabra **apple** significa manzana. Example: I eat an apple.';

function objetivo(id: number): ObjetivoRespuesta {
  return { id, codigo_oficial: 'OA 1', descripcion: 'Comprender textos', eje_tematico: null, contenido_guia: GUIA_BILINGUE };
}

function montar(asignaturas: AsignaturaRespuesta[], objetivosDeAsignatura: ObjetivoRespuesta[]) {
  const contenido = {
    obtenerObjetivo: vi.fn(() => of(objetivo(5))),
    listarAsignaturas: vi.fn(() => of(asignaturas)),
    listarObjetivos: vi.fn(() => of(objetivosDeAsignatura)),
  };
  TestBed.resetTestingModule();
  TestBed.configureTestingModule({
    imports: [EstudiarOa],
    providers: [
      provideRouter([]),
      { provide: ContenidoService, useValue: contenido },
      { provide: ProgresoService, useValue: { marcarGuiaRevisada: () => of({}) } },
      { provide: OnboardingService, useValue: { completarPaso: () => of({}) } },
      { provide: CalificacionesService, useValue: { obtenerMiCalificacion: () => of(null), calificar: () => of({}) } },
      { provide: SesionService, useValue: { perfilActivo: () => ({ id: 9, nombre: 'A', apellidos: 'B', nivel_id: 13 }) } },
    ],
  });
  const fixture = TestBed.createComponent(EstudiarOa);
  fixture.componentRef.setInput('oaId', '5');
  fixture.detectChanges();
  return { fixture, contenido };
}

describe('EstudiarOa - pronunciación inglesa por metadatos de asignatura', () => {
  let habladas: UtteranceFalsa[];

  beforeEach(() => {
    habladas = [];
    Object.defineProperty(window, 'speechSynthesis', {
      value: {
        speak: vi.fn((u: UtteranceFalsa) => habladas.push(u)),
        cancel: vi.fn(),
        getVoices: () => [{ lang: 'en-US', name: 'US', localService: true }],
        addEventListener: vi.fn(),
        removeEventListener: vi.fn(),
      },
      configurable: true,
      writable: true,
    });
    Object.defineProperty(window, 'SpeechSynthesisUtterance', { value: UtteranceFalsa, configurable: true, writable: true });
  });

  afterEach(() => {
    delete (window as unknown as Record<string, unknown>)['speechSynthesis'];
    delete (window as unknown as Record<string, unknown>)['SpeechSynthesisUtterance'];
  });

  it('reconoce el nombre de asignatura Inglés con o sin tilde', () => {
    expect(esNombreIngles('Inglés')).toBe(true);
    expect(esNombreIngles('ingles')).toBe(true);
    expect(esNombreIngles('Lengua y Literatura')).toBe(false);
  });

  it('muestra el panel cuando el OA pertenece a la asignatura Inglés del nivel', () => {
    const { fixture, contenido } = montar(
      [
        { id: 1, nombre: 'Lengua y Literatura' },
        { id: 2, nombre: 'Inglés' },
      ],
      [objetivo(5)],
    );
    expect(contenido.listarAsignaturas).toHaveBeenCalledWith(13);
    expect(contenido.listarObjetivos).toHaveBeenCalledWith(2);
    expect(fixture.componentInstance.esIngles()).toBe(true);
    expect(fixture.nativeElement.querySelector('app-pronunciacion-ingles')).not.toBeNull();
  });

  it('la guía bilingüe completa sigue leyéndose en español, nunca como inglés', () => {
    const { fixture } = montar([{ id: 2, nombre: 'Inglés' }], [objetivo(5)]);
    (fixture.nativeElement.querySelector('.boton-escuchar') as HTMLButtonElement).click();
    expect(habladas.length).toBe(1);
    // Se lee sin los asteriscos del Markdown (texto-para-voz.ts).
    expect(habladas[0].text).toBe('La palabra apple significa manzana. Example: I eat an apple.');
    expect(habladas[0].lang).toBe('es-CL');
  });

  it('no muestra el panel si el OA no está en Inglés aunque la guía tenga palabras inglesas', () => {
    const { fixture } = montar([{ id: 2, nombre: 'Inglés' }], [objetivo(99)]);
    expect(fixture.componentInstance.esIngles()).toBe(false);
    expect(fixture.nativeElement.querySelector('app-pronunciacion-ingles')).toBeNull();
  });

  it('no consulta objetivos si el nivel no tiene asignatura Inglés', () => {
    const { fixture, contenido } = montar([{ id: 1, nombre: 'Matemática' }], []);
    expect(contenido.listarObjetivos).not.toHaveBeenCalled();
    expect(fixture.nativeElement.querySelector('app-pronunciacion-ingles')).toBeNull();
  });
});
