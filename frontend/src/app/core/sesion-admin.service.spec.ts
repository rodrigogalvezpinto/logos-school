import { describe, it, expect, beforeEach } from 'vitest';
import { SesionAdminService } from './sesion-admin.service';

describe('SesionAdminService', () => {
  let servicio: SesionAdminService;
  let store: Record<string, string>;

  beforeEach(() => {
    store = {};
    const storageMock = {
      getItem: (key: string) => store[key] ?? null,
      setItem: (key: string, value: string) => { store[key] = value; },
      removeItem: (key: string) => { delete store[key]; },
      clear: () => { store = {}; },
    };
    Object.defineProperty(globalThis, 'localStorage', { value: storageMock, configurable: true, writable: true });
    servicio = new SesionAdminService();
  });

  it('debe inicializarse con token nulo y nombre vacío', () => {
    expect(servicio.token()).toBeNull();
    expect(servicio.nombre()).toBe('');
  });

  it('debe guardar el token en localStorage y actualizar el signal', () => {
    servicio.guardarToken('jwt-admin-token-123');
    expect(servicio.token()).toBe('jwt-admin-token-123');
    expect(localStorage.getItem('logos_admin_token')).toBe('jwt-admin-token-123');
  });

  it('debe guardar el nombre en localStorage y actualizar el signal', () => {
    servicio.setNombre('Super Admin');
    expect(servicio.nombre()).toBe('Super Admin');
    expect(localStorage.getItem('logos_admin_nombre')).toBe('Super Admin');
  });

  it('debe limpiar token y nombre en cerrarSesion', () => {
    servicio.guardarToken('token-a-borrar');
    servicio.setNombre('Admin Temporal');

    servicio.cerrarSesion();

    expect(servicio.token()).toBeNull();
    expect(servicio.nombre()).toBe('');
    expect(localStorage.getItem('logos_admin_token')).toBeNull();
    expect(localStorage.getItem('logos_admin_nombre')).toBeNull();
  });
});
