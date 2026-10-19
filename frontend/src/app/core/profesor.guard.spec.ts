import { describe, it, expect, beforeEach } from 'vitest';
import { TestBed } from '@angular/core/testing';
import { Router, UrlTree } from '@angular/router';
import { signal } from '@angular/core';
import { profesorGuard } from './profesor.guard';
import { SesionProfesorService } from './sesion-profesor.service';

describe('profesorGuard - Protección de Panel de Profesores', () => {
  let mockSesionProfesor: { token: ReturnType<typeof signal<string | null>> };
  let mockRouter: { parseUrl: (url: string) => UrlTree };

  beforeEach(() => {
    mockSesionProfesor = { token: signal<string | null>(null) };
    mockRouter = {
      parseUrl: (url: string) => ({ toString: () => url } as unknown as UrlTree),
    };

    TestBed.configureTestingModule({
      providers: [
        { provide: SesionProfesorService, useValue: mockSesionProfesor },
        { provide: Router, useValue: mockRouter },
      ],
    });
  });

  it('permite el acceso si el profesor tiene token activo', () => {
    mockSesionProfesor.token.set('jwt-profesor-token-999');
    const resultado = TestBed.runInInjectionContext(() => profesorGuard({} as never, {} as never));
    expect(resultado).toBe(true);
  });

  it('redirige a /profesor/login si no hay token de profesor', () => {
    mockSesionProfesor.token.set(null);
    const resultado = TestBed.runInInjectionContext(() => profesorGuard({} as never, {} as never)) as UrlTree;
    expect(resultado.toString()).toBe('/profesor/login');
  });
});
