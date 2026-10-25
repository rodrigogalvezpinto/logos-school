import { describe, it, expect } from 'vitest';
import { validarRut } from './rut.util';

describe('validarRut - Algoritmo Módulo 11 Chileno', () => {
  it('debe validar RUTs válidos con formato estándar', () => {
    // Casos reales con dígito verificador numérico
    expect(validarRut('21.345.678-4')).toBe(true);
    expect(validarRut('11.111.111-1')).toBe(true);
    expect(validarRut('22.222.222-2')).toBe(true);
    expect(validarRut('12.345.678-5')).toBe(true);
  });

  it('debe validar RUTs válidos con dígito verificador K (mayúscula y minúscula)', () => {
    // 11.111.112-K: suma 34, resto 10 -> K
    expect(validarRut('11.111.112-K')).toBe(true);
    expect(validarRut('11.111.112-k')).toBe(true);
    expect(validarRut('11111112K')).toBe(true);
    expect(validarRut('11111112k')).toBe(true);
  });

  it('debe aceptar RUTs válidos sin puntos ni guión', () => {
    expect(validarRut('213456784')).toBe(true);
    expect(validarRut('111111111')).toBe(true);
    expect(validarRut('123456785')).toBe(true);
  });

  it('debe rechazar RUTs con dígito verificador incorrecto', () => {
    expect(validarRut('21.345.678-9')).toBe(false);
    expect(validarRut('11.111.111-2')).toBe(false);
    expect(validarRut('11.111.112-3')).toBe(false);
  });

  it('debe rechazar cadenas vacías o con longitud menor a 2', () => {
    expect(validarRut('')).toBe(false);
    expect(validarRut('1')).toBe(false);
    expect(validarRut('-')).toBe(false);
    expect(validarRut('   ')).toBe(false);
  });

  it('debe rechazar caracteres no numéricos en el cuerpo', () => {
    expect(validarRut('12.34A.678-5')).toBe(false);
    expect(validarRut('ABCDEFGH-K')).toBe(false);
    expect(validarRut('12.345.678-Z')).toBe(false);
  });
});
