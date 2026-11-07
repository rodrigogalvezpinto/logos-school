import { describe, it, expect } from 'vitest';
import { textoParaVoz, textoPreguntaParaVoz } from './texto-para-voz';

describe('textoParaVoz - lo que se lee en voz alta', () => {
  it('no lee los dibujos de posición (darían la respuesta)', () => {
    const t = textoParaVoz('::posicion::🐱::debajo::mesa:: El gato está ___ de la mesa.');
    expect(t).toBe('El gato está … de la mesa.');
    expect(t).not.toMatch(/debajo|posicion|mesa::/);
  });

  it('no dice la cantidad que el niño debe contar', () => {
    const t = textoParaVoz('::contar::⭐::6:: ¿Cuántas estrellas hay?');
    expect(t).toBe('¿Cuántas estrellas hay?');
  });

  it('quita Markdown y nombres de emojis, y lee las descripciones visibles', () => {
    const t = textoParaVoz('## Ejemplo\n\nUna fila: 👧 **Camila** → 👦 *Mateo*.\n\n::emoji::🦋::una mariposa en una flor::');
    expect(t).not.toMatch(/[*#→]|👧|🦋/u);
    expect(t).toContain('Camila');
    expect(t).toContain('Mateo');
    expect(t).toContain('una mariposa en una flor');
  });

  it('lee la tabla como lista y no los separadores', () => {
    const t = textoParaVoz('| Animal | Patas |\n|---|---|\n| perro | 4 |');
    expect(t).not.toContain('|');
    expect(t).not.toContain('---');
    expect(t).toContain('perro, 4');
  });
});

describe('textoPreguntaParaVoz - enunciado y alternativas', () => {
  it('lee las alternativas con letra, en orden', () => {
    const t = textoPreguntaParaVoz({
      tipo: 'alternativas',
      enunciado: '¿Cuántas sílabas tiene la palabra "**gato**"?',
      opciones: ['1', '2', '3'],
    });
    expect(t).toBe('¿Cuántas sílabas tiene la palabra "gato"? a: 1. b: 2. c: 3.');
  });

  it('una alternativa dibujada se anuncia sin describirla', () => {
    const t = textoPreguntaParaVoz({ tipo: 'alternativas', enunciado: '¿Dónde hay 5?', opciones: ['::contar::🍎::5::', '::contar::🍎::3::'] });
    expect(t).toBe('¿Dónde hay 5? a: el dibujo número 1. b: el dibujo número 2.');
  });

  it('verdadero o falso y varias correctas avisan cómo responder', () => {
    expect(textoPreguntaParaVoz({ tipo: 'verdadero_falso', enunciado: 'El Sol sale de noche.' })).toBe('El Sol sale de noche. ¿Verdadero o falso?');
    expect(textoPreguntaParaVoz({ tipo: 'varias_correctas', enunciado: '¿Cuáles son animales?', opciones: ['perro', 'mesa'] })).toBe(
      '¿Cuáles son animales? Marca todas las correctas. a: perro. b: mesa.',
    );
  });
});

describe('textoParaVoz - casos reales de 1°-2° básico', () => {
  it('lee fonemas sin barras, citas sin «>» y comparaciones con palabras', () => {
    expect(textoParaVoz('¿Con qué sonido empieza "sapo"? /s/')).toBe('¿Con qué sonido empieza "sapo"? s');
    expect(textoParaVoz('Lee el texto y responde. > Pepa vive en Curicó.')).toBe('Lee el texto y responde. Pepa vive en Curicó.');
    expect(textoParaVoz('Es cierto que 9 > 4 y 3 < 8.')).toBe('Es cierto que 9 mayor que 4 y 3 menor que 8.');
  });

  it('no lee las marcas de conteo ni repite «¿Verdadero o falso?»', () => {
    expect(textoParaVoz('manzana \\|\\|\\|\\|, uva \\|\\|. ¿Cuál tiene menos?')).toBe('manzana, uva. ¿Cuál tiene menos?');
    expect(textoPreguntaParaVoz({ tipo: 'verdadero_falso', enunciado: '¿Verdadero o falso? El pez vuela.' })).toBe('¿Verdadero o falso? El pez vuela.');
  });

  it('las alternativas de símbolo se dicen con palabras', () => {
    expect(textoPreguntaParaVoz({ tipo: 'alternativas', enunciado: '9+4 ___ 15', opciones: ['>', '<', '='] })).toBe('9+4 … 15. a: mayor que. b: menor que. c: igual a.');
  });
});

describe('textoParaVoz - pausas', () => {
  it('separa títulos del texto y no duplica la puntuación', () => {
    expect(textoParaVoz('### ¿Qué vamos a aprender?\nTodas las palabras tienen sílabas.')).toBe('¿Qué vamos a aprender? Todas las palabras tienen sílabas.');
    expect(textoParaVoz('**Actividad 3 — El sonido final**\nLa palabra "pan" termina en n.')).toBe('Actividad 3 — El sonido final. La palabra "pan" termina en n.');
  });

  it('no repite la instrucción de varias correctas', () => {
    expect(textoPreguntaParaVoz({ tipo: 'varias_correctas', enunciado: 'Marca todas las correctas: ¿cuáles suman 10?', opciones: ['5 + 5', '4 + 4'] })).toBe(
      'Marca todas las correctas: ¿cuáles suman 10? a: 5 + 5. b: 4 + 4.',
    );
  });
});
