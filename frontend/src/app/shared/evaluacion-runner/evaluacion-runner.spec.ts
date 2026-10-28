import { describe, it, expect, beforeEach } from 'vitest';
import { TestBed } from '@angular/core/testing';
import { Router } from '@angular/router';
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
        { provide: Router, useValue: { navigate: () => Promise.resolve(true) } },
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
