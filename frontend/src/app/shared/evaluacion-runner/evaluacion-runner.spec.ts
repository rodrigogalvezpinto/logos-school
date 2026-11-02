import { describe, it, expect, beforeEach } from 'vitest';
import { TestBed } from '@angular/core/testing';
import { provideRouter } from '@angular/router';
import { of } from 'rxjs';
import { EvaluacionesService } from '../../core/evaluaciones.service';
import { EvaluacionRunner, PreguntaRunner } from './evaluacion-runner';

describe('EvaluacionRunner - UX y Autoevaluación', () => {
  let runner: EvaluacionRunner;

  const mockPreguntas: PreguntaRunner[] = [
    {
      id: 101,
      tipo: 'alternativas',
      enunciado: '¿Cuánto es 2 + 2?',
      opciones: ['3', '4', '5'],
      respuesta_correcta: '4',
      retroalimentacion: '2 + 2 es igual a 4.',
    },
    {
      id: 102,
      tipo: 'desarrollo_breve',
      enunciado: 'Explica el concepto de fracción.',
      opciones: null,
      respuesta_correcta: 'Una parte de un todo dividido en partes iguales.',
      retroalimentacion: 'Rúbrica: debe mencionar partes iguales y la unidad completa.',
    },
    {
      id: 103,
      tipo: 'verdadero_falso',
      enunciado: 'El número 7 es primo.',
      opciones: ['Verdadero', 'Falso'],
      respuesta_correcta: 'Verdadero',
      retroalimentacion: '7 solo es divisible por 1 y por sí mismo.',
    },
  ];

  beforeEach(() => {
    TestBed.configureTestingModule({
      providers: [
        provideRouter([]),
        {
          provide: EvaluacionesService,
          useValue: {
            responder: () => of({}),
            obtenerDetalle: () => of([]),
            entregar: () => of({ puntaje: 0, nota: 1 }),
            reportarErrorPregunta: () => of({}),
          },
        },
      ],
    });

    runner = TestBed.runInInjectionContext(() => new EvaluacionRunner());
    runner.preguntas = mockPreguntas;
    runner.modo = 'autoevaluacion';
    runner.empezar();
  });

  it.each([false, true])('mantiene el encabezado principal con práctica enviada=%s', (enviada) => {
    const fixture = TestBed.createComponent(EvaluacionRunner);
    fixture.componentRef.setInput('preguntas', mockPreguntas);
    fixture.componentRef.setInput('modo', 'autoevaluacion');
    fixture.componentRef.setInput('nombreEvaluacion', 'Práctica accesible');
    fixture.componentInstance.empezar();
    fixture.componentInstance.enviada.set(enviada);
    fixture.detectChanges();

    const encabezados = fixture.nativeElement.querySelectorAll('h1');
    expect(encabezados.length).toBe(1);
    expect(encabezados[0].textContent).toContain('Práctica accesible');
  });

  it.each([
    ['Una parte de un todo dividido en partes iguales.', 'correcta'],
    ['Representa partes iguales de una unidad completa.', 'correcta'],
    ['Una parte de algo.', 'parcial'],
    ['Es sumar dos números enteros.', 'incorrecta'],
    ['', null],
    ['   ', null],
  ] as const)('revisa desarrollo sin corrección literal: %s', (respuesta, revision) => {
    const fixture = TestBed.createComponent(EvaluacionRunner);
    fixture.componentRef.setInput('preguntas', mockPreguntas);
    const componente = fixture.componentInstance;
    componente.empezar();
    componente.irA(1);
    fixture.detectChanges();
    const campo: HTMLTextAreaElement = fixture.nativeElement.querySelector('textarea.respuesta-abierta');
    campo.value = respuesta;
    campo.dispatchEvent(new Event('input', { bubbles: true }));
    fixture.detectChanges();
    const ayuda: HTMLButtonElement = fixture.nativeElement.querySelector('.btn-ayuda-practica');
    expect(ayuda.disabled).toBe(!respuesta.trim());
    expect(componente.faltantes().some(p => p.id === 102)).toBe(!respuesta.trim());
    if (!revision) return;
    ayuda.click();
    fixture.detectChanges();
    expect(fixture.nativeElement.querySelector('.feedback__orientativo').textContent).toContain('partes iguales');
    expect(fixture.nativeElement.querySelector('.feedback__tag-ok')).toBeNull();
    expect(fixture.nativeElement.querySelector('.feedback__atencion')).toBeNull();
    const botones = Array.from(fixture.nativeElement.querySelectorAll('fieldset.revision-desarrollo button')) as HTMLButtonElement[];
    const elegido = botones.find(b => b.textContent?.trim().toLowerCase() === revision);
    expect(elegido).toBeDefined();
    elegido!.click();
    fixture.detectChanges();
    expect(elegido!.getAttribute('aria-pressed')).toBe('true');
    campo.value = 'Nueva respuesta';
    campo.dispatchEvent(new Event('input', { bubbles: true }));
    fixture.detectChanges();
    expect(botones.every(b => b.getAttribute('aria-pressed') === 'false')).toBe(true);
  });

  it.each([
    ['Una parte de un todo dividido en partes iguales.', 'correcta'],
    ['Representa partes iguales de una unidad completa.', 'correcta'],
    ['Una parte de algo.', 'parcial'],
    ['Es sumar dos números enteros.', 'incorrecta'],
    ['', null],
    ['   ', null],
  ] as const)('muestra pauta y revisión personal tras entregar: %s', (respuesta, revision) => {
    const fixture = TestBed.createComponent(EvaluacionRunner);
    fixture.componentRef.setInput('modo', 'prueba');
    const componente = fixture.componentInstance;
    componente.empezada.set(true);
    componente.enviada.set(true);
    componente.notaFinal.set(7);
    componente.detalle.set([{
      pregunta_id: 102, enunciado: 'Explica el concepto de fracción.', tipo: 'desarrollo_breve',
      opciones: null, respuesta_alumno: respuesta, respuesta_correcta: null, es_correcta: null,
      pauta_orientativa: 'Una parte de un todo dividido en partes iguales.',
      retroalimentacion: 'Rúbrica: partes iguales y unidad completa.',
    }]);
    componente.revisionAbierta.set(102);
    fixture.detectChanges();
    const fila: HTMLElement = fixture.nativeElement.querySelector('.resultado__revision-detalle');
    expect(fila.textContent).toContain('Pauta orientativa');
    expect(fila.textContent).toContain('Rúbrica: partes iguales y unidad completa.');
    expect(fila.textContent).not.toContain('Respuesta correcta:');
    expect(fixture.nativeElement.querySelector('.resultado__nota').textContent).toContain('autocorregibles');
    const botones = Array.from(fila.querySelectorAll('fieldset.revision-desarrollo button')) as HTMLButtonElement[];
    expect(botones.length).toBe(3);
    expect(botones.every(b => b.disabled)).toBe(!respuesta.trim());
    if (revision) {
      botones.find(b => b.textContent?.trim().toLowerCase() === revision)!.click();
      fixture.detectChanges();
      expect(botones.some(b => b.getAttribute('aria-pressed') === 'true')).toBe(true);
    } else {
      componente.revisarDesarrollo(102, 'correcta');
      fixture.detectChanges();
      expect(fila.textContent).toContain('en blanco');
      expect(botones.every(b => b.getAttribute('aria-pressed') === 'false')).toBe(true);
    }
    expect(componente.notaFinal()).toBe(7);
  });

  it('UX-001: no revela la ayuda automáticamente hasta que se solicita explícitamente', () => {
    // Alumno responde pero aún no solicita ayuda
    runner.responder(101, '4');
    expect(runner.ayudasReveladas().has(101)).toBe(false);

    // Alumno hace clic en "Comprobar respuesta / Ver explicación"
    runner.solicitarAyuda(101);
    expect(runner.ayudasReveladas().has(101)).toBe(true);
  });

  it('UX-002: advierte preguntas marcadas para revisar al intentar entregar', () => {
    // Responde todas las preguntas
    runner.responder(101, '4');
    runner.responder(102, 'Mi respuesta abierta');
    runner.responder(103, 'Verdadero');
    expect(runner.faltantes().length).toBe(0);

    // Marca la pregunta 2 (índice 1 en array, número 2 para el estudiante)
    runner.marcarRevisar(102);
    expect(runner.marcadas().size).toBe(1);
    expect(runner.marcadasTexto()).toBe('2');

    // Al intentar entregar, debe abrir el modal de aviso incompleto
    runner.intentarEnviar();
    expect(runner.mostrarAvisoIncompleto()).toBe(true);

    // irARevisarPendientes debe dirigir a la pregunta marcada
    runner.irARevisarPendientes();
    expect(runner.indiceActual()).toBe(1);
    expect(runner.mostrarAvisoIncompleto()).toBe(false);
  });

  it('MAT-UI-001: comprueba respuestas autocorregibles con normalización de espacios y mayúsculas', () => {
    runner.responder(101, ' 4 ');
    expect(runner.esCorrectaEnAutoevaluacion(mockPreguntas[0])).toBe(true);

    runner.responder(103, 'verdadero');
    expect(runner.esCorrectaEnAutoevaluacion(mockPreguntas[2])).toBe(true);
  });
});
