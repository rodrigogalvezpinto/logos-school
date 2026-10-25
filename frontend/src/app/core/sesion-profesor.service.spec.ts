import { describe, it, expect, beforeEach } from 'vitest';
import { SesionProfesorService } from './sesion-profesor.service';

describe('SesionProfesorService', () => {
  let servicio: SesionProfesorService;
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
    servicio = new SesionProfesorService();
  });

  it('debe inicializarse con token nulo y nombre vacío', () => {
    expect(servicio.token()).toBeNull();
    expect(servicio.nombre()).toBe('');
  });

  it('debe guardar el token de profesor en localStorage y actualizar el signal', () => {
    servicio.guardarToken('jwt-profesor-token-456');
    expect(servicio.token()).toBe('jwt-profesor-token-456');
    expect(localStorage.getItem('logos_profesor_token')).toBe('jwt-profesor-token-456');
  });

  it('debe guardar el nombre del profesor en localStorage y actualizar el signal', () => {
    servicio.setNombre('Prof. Gabriela Mistral');
    expect(servicio.nombre()).toBe('Prof. Gabriela Mistral');
    expect(localStorage.getItem('logos_profesor_nombre')).toBe('Prof. Gabriela Mistral');
  });

  it('debe limpiar token y nombre de profesor al cerrar sesión', () => {
    servicio.guardarToken('token-profesor-temporal');
    servicio.setNombre('Profesor Interino');

    servicio.cerrarSesion();

    expect(servicio.token()).toBeNull();
    expect(servicio.nombre()).toBe('');
    expect(localStorage.getItem('logos_profesor_token')).toBeNull();
    expect(localStorage.getItem('logos_profesor_nombre')).toBeNull();
  });
});
