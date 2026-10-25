import { describe, it, expect, beforeEach } from 'vitest';
import { TestBed } from '@angular/core/testing';
import { Router, UrlTree } from '@angular/router';
import { signal } from '@angular/core';
import { adminGuard } from './admin.guard';
import { SesionAdminService } from './sesion-admin.service';

describe('adminGuard - Protección de Panel de Administración', () => {
  let mockSesionAdmin: { token: ReturnType<typeof signal<string | null>> };
  let mockRouter: { parseUrl: (url: string) => UrlTree };

  beforeEach(() => {
    mockSesionAdmin = { token: signal<string | null>(null) };
    mockRouter = {
      parseUrl: (url: string) => ({ toString: () => url } as unknown as UrlTree),
    };

    TestBed.configureTestingModule({
      providers: [
        { provide: SesionAdminService, useValue: mockSesionAdmin },
        { provide: Router, useValue: mockRouter },
      ],
    });
  });

  it('permite el acceso si el administrador tiene token activo', () => {
    mockSesionAdmin.token.set('jwt-admin-token-789');
    const resultado = TestBed.runInInjectionContext(() => adminGuard({} as never, {} as never));
    expect(resultado).toBe(true);
  });

  it('redirige a /admin/login si no hay token de administrador', () => {
    mockSesionAdmin.token.set(null);
    const resultado = TestBed.runInInjectionContext(() => adminGuard({} as never, {} as never)) as UrlTree;
    expect(resultado.toString()).toBe('/admin/login');
  });
});
