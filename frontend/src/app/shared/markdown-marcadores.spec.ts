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
});
