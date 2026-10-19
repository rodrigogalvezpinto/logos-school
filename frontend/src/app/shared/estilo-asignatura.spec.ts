import { describe, it, expect } from 'vitest';
import { estiloAsignatura } from './estilo-asignatura';

describe('estiloAsignatura - Identidad Visual y Accesibilidad WCAG AA', () => {
  it('debe asignar ícono y color violeta a Matemática', () => {
    const estilo = estiloAsignatura('Matemática');
    expect(estilo.icono).toBe('regla');
    expect(estilo.color).toBe('#7C3AED');
  });

  it('debe asignar ícono y color fucsia a Lenguaje y Comunicación', () => {
    const estilo = estiloAsignatura('Lenguaje y Comunicación');
    expect(estilo.icono).toBe('libro');
    expect(estilo.color).toBe('#D62674');
  });

  it('debe asignar ícono y color fucsia a Lengua y Literatura', () => {
    const estilo = estiloAsignatura('Lengua y Literatura');
    expect(estilo.icono).toBe('libro');
    expect(estilo.color).toBe('#D62674');
  });

  it('debe asignar ícono y color verde a Ciencias Naturales', () => {
    const estilo = estiloAsignatura('Ciencias Naturales');
    expect(estilo.icono).toBe('hoja');
    expect(estilo.color).toBe('#12853C');
  });

  it('debe asignar ícono y color terracota a Historia, Geografía y Cs. Sociales', () => {
    const estilo = estiloAsignatura('Historia, Geografía y Cs. Sociales');
    expect(estilo.icono).toBe('mapa');
    expect(estilo.color).toBe('#C4490A');
  });

  it('debe asignar ícono y color azul a Inglés', () => {
    const estilo = estiloAsignatura('Inglés');
    expect(estilo.icono).toBe('ingles');
    expect(estilo.color).toBe('#2563EB');
  });

  it('debe asignar ícono y color índigo a Filosofía', () => {
    const estilo = estiloAsignatura('Filosofía');
    expect(estilo.icono).toBe('filosofia');
    expect(estilo.color).toBe('#4338CA');
  });

  it('debe asignar ícono y color verde azulado a Ciencias para la Ciudadanía y Educación Ciudadana', () => {
    const estiloCiencias = estiloAsignatura('Ciencias para la Ciudadanía');
    expect(estiloCiencias.icono).toBe('balanza');
    expect(estiloCiencias.color).toBe('#0B7F74');

    const estiloEdu = estiloAsignatura('Educación Ciudadana');
    expect(estiloEdu.icono).toBe('balanza');
    expect(estiloEdu.color).toBe('#0B7F74');
  });

  it('debe retornar estilo por defecto ante asignaturas no catalogadas', () => {
    const estilo = estiloAsignatura('Taller de Robótica');
    expect(estilo.icono).toBe('libro');
    expect(estilo.color).toBe('#5B4FE9');
  });
});
