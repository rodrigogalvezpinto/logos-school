import { describe, it, expect } from 'vitest';
import { esRespuestaCorrecta } from './juegos';

const base = { id: 1, enunciado: '¿?', retroalimentacion: '' };

describe('juegos: corrección igual a la autoevaluación', () => {
  it('alternativas y verdadero o falso: compara sin mayúsculas ni espacios', () => {
    const p = { ...base, tipo: 'alternativas', opciones: ['3', '4'], respuesta_correcta: '4' };
    expect(esRespuestaCorrecta(p, ' 4 ')).toBe(true);
    expect(esRespuestaCorrecta(p, '3')).toBe(false);
    expect(esRespuestaCorrecta({ ...base, tipo: 'verdadero_falso', opciones: null, respuesta_correcta: 'Falso' }, 'falso')).toBe(true);
  });

  it('varias correctas: todo o nada, sin importar el orden', () => {
    const p = { ...base, tipo: 'varias_correctas', opciones: ['a', 'b', 'c'], respuesta_correcta: JSON.stringify(['a', 'c']) };
    expect(esRespuestaCorrecta(p, JSON.stringify(['c', 'a']))).toBe(true);
    expect(esRespuestaCorrecta(p, JSON.stringify(['a']))).toBe(false);
    expect(esRespuestaCorrecta(p, JSON.stringify(['a', 'b', 'c']))).toBe(false);
    expect(esRespuestaCorrecta(p, '[]')).toBe(false);
  });
});
