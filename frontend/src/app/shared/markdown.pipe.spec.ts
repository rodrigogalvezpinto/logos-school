import { describe, it, expect, beforeEach } from 'vitest';
import { TestBed } from '@angular/core/testing';
import { DomSanitizer } from '@angular/platform-browser';
import { MarkdownPipe } from './markdown.pipe';

describe('MarkdownPipe - Renderizado con KaTeX y compatibilidad', () => {
  let pipe: MarkdownPipe;
  let sanitizer: DomSanitizer;

  beforeEach(() => {
    TestBed.configureTestingModule({
      providers: [MarkdownPipe],
    });
    pipe = TestBed.inject(MarkdownPipe);
    sanitizer = TestBed.inject(DomSanitizer);
  });

  it('renderiza fórmulas en bloque $$ ... $$ con KaTeX en modo display', () => {
    const markdown = 'La ecuación cuadrática es:\n\n$$ x = \\frac{-b \\pm \\sqrt{b^2 - 4ac}}{2a} $$';
    const resultado = pipe.transform(markdown);
    const html = resultado.toString();

    expect(html).toContain('katex-display');
    expect(html).toContain('katex-html');
    expect(html).toContain('frac-line');
  });

  it('renderiza fórmulas en línea \\( ... \\) con KaTeX en modo inline', () => {
    const markdown = 'Calcula el valor de \\( \\sqrt{16} + \\frac{1}{2} \\) en tu cuaderno.';
    const resultado = pipe.transform(markdown);
    const html = resultado.toString();

    expect(html).toContain('katex');
    expect(html).toContain('katex-html');
    expect(html).toContain('sqrt');
  });

  it('renderiza el helper accesible de fracciones [frac: a/b] con KaTeX', () => {
    const markdown = 'El resultado final es [frac: 3/4].';
    const resultado = pipe.transform(markdown);
    const html = resultado.toString();

    expect(html).toContain('katex');
    expect(html).toContain('frac-line');
    expect(html).toContain('3');
    expect(html).toContain('4');
  });

  it('CRÍTICO: preserva precios en pesos chilenos ($15.000) sin colisionar con fórmulas', () => {
    const markdown = 'Camila tenía $15.000 y gastó $4.500 en un libro de $10.500.';
    const resultado = pipe.transform(markdown);
    const html = resultado.toString();

    expect(html).toContain('$15.000');
    expect(html).toContain('$4.500');
    expect(html).toContain('$10.500');
    expect(html).not.toContain('katex-error');
  });
});
