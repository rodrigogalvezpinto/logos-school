import { describe, it, expect } from 'vitest';
import { reemplazarPictogramas } from './pictogramas';
import { PICTOGRAMAS } from './pictogramas-datos';

describe('pictogramas: emoji → imagen (se ven igual en todo equipo y se imprimen)', () => {
  it('cambia el emoji del texto por una imagen con texto alternativo', () => {
    const h = reemplazarPictogramas('<p>Mochila azul: 🎒🎒 (2)</p>');
    expect(h).not.toContain('🎒');
    expect(h.match(/<img class="pictograma" src="\/assets\/pictogramas\/mochila\.png" alt="mochila"/g)?.length).toBe(2);
  });

  it('dentro de un SVG usa <image> del mismo tamaño y no mete <img>', () => {
    const h = reemplazarPictogramas('<svg viewBox="0 0 240 140"><text x="120" y="72" font-size="44" text-anchor="middle">🐱</text></svg>');
    expect(h).toContain('<image href="/assets/pictogramas/gato.svg" x="98" y="33.3" width="44" height="44">');
    expect(h).not.toContain('<img');
  });

  it('no toca atributos ni símbolos de texto como → y ✓', () => {
    const h = reemplazarPictogramas('<span aria-label="⭐">7 → 8 ✓ ⭐</span>');
    expect(h).toContain('aria-label="⭐"');
    expect(h).toContain('7 → 8 ✓ <img');
  });

  it('acepta el emoji con selector de variación (☀️)', () => {
    expect(reemplazarPictogramas('<p>☀️</p>')).toContain('sol');
  });

  it('cada pictograma apunta a un archivo .png o .svg con texto alternativo', () => {
    for (const [archivo, alt] of Object.values(PICTOGRAMAS)) {
      expect(archivo).toMatch(/^[a-z0-9-]+\.(png|svg)$/);
      expect(alt.length).toBeGreaterThan(1);
    }
  });
});
