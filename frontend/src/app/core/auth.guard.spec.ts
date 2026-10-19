import { describe, it, expect, beforeEach } from 'vitest';
import { TestBed } from '@angular/core/testing';
import { Router, UrlTree } from '@angular/router';
import { signal } from '@angular/core';
import { authGuard } from './auth.guard';
import { SesionService } from './sesion.service';

describe('authGuard - Protección de Rutas Privadas', () => {
  let mockSesionService: { token: ReturnType<typeof signal<string | null>> };
  let mockRouter: { parseUrl: (url: string) => UrlTree };

  beforeEach(() => {
    mockSesionService = { token: signal<string | null>(null) };
    mockRouter = {
      parseUrl: (url: string) => ({ toString: () => url } as unknown as UrlTree),
    };

    TestBed.configureTestingModule({
      providers: [
        { provide: SesionService, useValue: mockSesionService },
        { provide: Router, useValue: mockRouter },
      ],
    });
  });

  it('permite el acceso si existe un token en la sesión', () => {
    mockSesionService.token.set('jwt-valido-123');
    const resultado = TestBed.runInInjectionContext(() => authGuard({} as never, {} as never));
    expect(resultado).toBe(true);
  });

  it('redirige a /login si no existe token en la sesión', () => {
    mockSesionService.token.set(null);
    const resultado = TestBed.runInInjectionContext(() => authGuard({} as never, {} as never)) as UrlTree;
    expect(resultado.toString()).toBe('/login');
  });
});
