import { describe, it, expect } from 'vitest';
import { EmojiPipe } from './emoji-pipe';

describe('EmojiPipe - Renderizado de Emojis Educativos Accesibles', () => {
  const pipe = new EmojiPipe();

  it('debe retornar string vacío o nulo sin error', () => {
    expect(pipe.transform('')).toBe('');
    expect(pipe.transform(null as unknown as string)).toBeNull();
  });

  it('debe mantener texto plano que no contenga marcadores ::emoji::', () => {
    const texto = 'Este es un texto explicativo normal de matemáticas.';
    expect(pipe.transform(texto)).toBe(texto);
  });

  it('debe transformar marcadores ::emoji:: en estructura HTML con ícono y descripción', () => {
    const entrada = 'Mira esta figura: ::emoji::🦋::una mariposa monarca volando:: en el jardín.';
    const salida = pipe.transform(entrada);

    expect(salida).toContain('<div class="emoji-educativo-inline">');
    expect(salida).toContain('<span class="emoji-educativo-inline__icono">🦋</span>');
    expect(salida).toContain('<span class="emoji-educativo-inline__descripcion">una mariposa monarca volando</span>');
    expect(salida).toContain('Mira esta figura:');
    expect(salida).toContain('en el jardín.');
  });

  it('debe soportar múltiples marcadores de emoji en el mismo párrafo', () => {
    const entrada = '::emoji::🍎::manzana roja:: y ::emoji::🍐::pera verde::';
    const salida = pipe.transform(entrada);

    expect(salida).toContain('🍎');
    expect(salida).toContain('manzana roja');
    expect(salida).toContain('🍐');
    expect(salida).toContain('pera verde');
  });
});
