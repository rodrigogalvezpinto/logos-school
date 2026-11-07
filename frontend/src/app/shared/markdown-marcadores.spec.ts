import { describe, it, expect } from 'vitest';
import { TestBed } from '@angular/core/testing';
import { MarkdownPipe } from './markdown.pipe';

/** Hallazgo de auditoría 2026-11-07: «::emoji::⭐::6 estrellas dibujadas::» mostraba UNA
 * estrella y la cantidad escrita (el niño leía la respuesta). Ahora se dibujan las 6. */
describe('MarkdownPipe - marcadores visuales para 1° básico', () => {
  const html = (texto: string) => {
    const pipe = TestBed.runInInjectionContext(() => new MarkdownPipe());
    return String((pipe.transform(texto) as { changingThisBreaksApplicationSecurity: string }).changingThisBreaksApplicationSecurity);
  };

  it('::contar:: dibuja la cantidad exacta de elementos y no escribe el número', () => {
    const salida = html('::contar::⭐::6:: ¿Cuántas estrellas hay?');
    expect((salida.match(/contar__item/g) || []).length).toBe(6);
    expect(salida).not.toContain('::');
    expect(salida).not.toMatch(/>\s*6\s*</);
  });

  it('::dibujo:: muestra el dibujo sin rótulo que delate la palabra', () => {
    const salida = html('::dibujo::☀️:: ¿Cuál es la palabra bien escrita?');
    expect(salida).toContain('class="dibujo"');
    expect(salida).not.toContain('sol');
  });

  it('::fraccion:: dibuja las partes sin escribir el número', () => {
    const salida = html('::fraccion::2::3:: ¿Qué fracción está pintada?');
    expect((salida.match(/fraccion-barra__parte--pintada/g) || []).length).toBe(2);
    expect((salida.match(/fraccion-barra__parte[" ]/g) || []).length).toBe(3);
    expect(salida).not.toContain('2/3');
  });

  it('::posicion:: dibuja la relación espacial sin escribir la palabra de posición', () => {
    const salida = html('::posicion::🐱::debajo::mesa:: El gato está ___ de la mesa.');
    expect(salida).toContain('class="posicion"');
    expect(salida).toContain('<svg');
    expect(salida).not.toContain('::');
    expect(salida.replace(/El gato está ___ de la mesa\./, '')).not.toMatch(/debajo/);
  });

  it('::posicion:: con caja dibuja el objeto dentro, tapado por el frente de la caja', () => {
    const salida = html('::posicion::✏️::dentro::caja::');
    expect(salida.indexOf('✏️')).toBeLessThan(salida.lastIndexOf('<rect'));
    expect(salida).not.toMatch(/dentro/);
  });

  it('::fila:: dibuja los elementos de izquierda a derecha en orden', () => {
    const salida = html('::fila::🌳::🪑::🎠::');
    expect((salida.match(/fila-dibujo__item/g) || []).length).toBe(3);
    expect(salida.indexOf('🌳')).toBeLessThan(salida.indexOf('🎠'));
    expect(salida).not.toContain('::');
  });
});
