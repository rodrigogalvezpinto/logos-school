import { describe, it, expect } from 'vitest';
import { TestBed } from '@angular/core/testing';
import { provideRouter } from '@angular/router';
import { Subject, of } from 'rxjs';
import { EvaluacionesService } from '../../core/evaluaciones.service';
import { EvaluacionRunner } from './evaluacion-runner';

/** Hallazgo E2E 2026-11-06: los autosaves en paralelo y un «Entregar» inmediato hacían
 * perder la última respuesta. Los guardados van en cola y la entrega espera a que terminen. */
describe('EvaluacionRunner - guardado en cola antes de entregar', () => {
  it('serializa los autosaves y entrega solo después del último', async () => {
    const eventos: string[] = [];
    const pendientes: Subject<object>[] = [];
    TestBed.configureTestingModule({
      providers: [
        provideRouter([]),
        {
          provide: EvaluacionesService,
          useValue: {
            responder: (_i: number, p: number) => {
              eventos.push(`responder ${p}`);
              const s = new Subject<object>();
              pendientes.push(s);
              return s;
            },
            entregar: () => { eventos.push('entregar'); return of({ puntaje: 2, nota: 7 }); },
            obtenerDetalle: () => of([]),
          },
        },
      ],
    });
    const runner = TestBed.runInInjectionContext(() => new EvaluacionRunner());
    runner.preguntas = [
      { id: 1, tipo: 'alternativas', enunciado: 'a', opciones: ['x', 'y'], respuesta_correcta: 'x', retroalimentacion: '' },
      { id: 2, tipo: 'alternativas', enunciado: 'b', opciones: ['x', 'y'], respuesta_correcta: 'y', retroalimentacion: '' },
    ];
    runner.modo = 'prueba';
    (runner as unknown as { intentoId: number }).intentoId = 99;

    runner.responder(1, 'x');
    runner.responder(2, 'y');
    runner.confirmarEnvio();
    await Promise.resolve();
    expect(eventos).toEqual(['responder 1']); // el 2.º espera al 1.º; la entrega espera a ambos

    pendientes[0].next({}); pendientes[0].complete();
    await new Promise((r) => setTimeout(r));
    expect(eventos).toEqual(['responder 1', 'responder 2']);

    pendientes[1].next({}); pendientes[1].complete();
    await new Promise((r) => setTimeout(r));
    expect(eventos).toEqual(['responder 1', 'responder 2', 'entregar']);
  });
});
