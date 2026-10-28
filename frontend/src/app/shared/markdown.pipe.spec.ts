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

  it('renderiza raíces con helper [sqrt: x] y [sqrt[n]: x]', () => {
    const markdown = 'Calcula [sqrt: 25] y la raíz cúbica [sqrt[3]: 8].';
    const resultado = pipe.transform(markdown);
    const html = resultado.toString();

    expect(html).toContain('katex');
    expect(html).toContain('sqrt');
  });

  it('renderiza automáticamente raíces cuadradas Unicode (ej: √49)', () => {
    const markdown = 'Calcula √49 y simplifica √(x + 3).';
    const resultado = pipe.transform(markdown);
    const html = resultado.toString();

    expect(html).toContain('katex');
    expect(html).toContain('sqrt');
  });

  it('renderiza automáticamente notación científica (ej: 6,02 × 10²³)', () => {
    const markdown = 'Un mol contiene 6,02 × 10²³ partículas.';
    const resultado = pipe.transform(markdown);
    const html = resultado.toString();

    expect(html).toContain('katex');
    expect(html).toContain('10');
  });

  it('renderiza ecuaciones químicas con helper [chem]', () => {
    const markdown = 'La reacción de síntesis del agua es: [chem]2H2 + O2 -> 2H2O[/chem]';
    const resultado = pipe.transform(markdown);
    const html = resultado.toString();

    expect(html).toContain('katex');
    expect(html).toContain('rightarrow');
  });

  it('renderiza fórmulas de física con [math]', () => {
    const markdown = 'La segunda ley de Newton es [math]F = m \\cdot a[/math]';
    const resultado = pipe.transform(markdown);
    const html = resultado.toString();

    expect(html).toContain('katex');
  });

  it('renderiza potencias y exponentes Unicode como números más pequeños elevados (sup)', () => {
    const markdown = 'Como 7²=49 y 8²=64, el área es 25 m²';
    const resultado = pipe.transform(markdown);
    const html = resultado.toString();

    expect(html).toContain('<sup class="exponente-matematico">2</sup>');
    expect(html).toContain('7<sup');
    expect(html).toContain('8<sup');
    expect(html).toContain('m<sup');
  });
});
