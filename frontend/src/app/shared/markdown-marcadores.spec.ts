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

  it('::largo:: dibuja dos lápices alineados sin decir cuál es más largo', () => {
    const salida = html('::largo::A::8::B::5:: ¿Cuál lápiz es más largo?');
    expect(salida).toContain('<svg');
    expect(salida).toContain('width="144"');
    expect(salida).toContain('width="90"');
    expect(salida).not.toMatch(/largo::|corto/);
  });

  it('::regla:: dibuja la regla y el objeto sin escribir la medida', () => {
    const salida = html('::regla::0::5:: ¿Cuánto mide la goma?');
    expect(salida).toContain('width="110"');
    expect(salida).not.toMatch(/regla::|5 cm/);
  });

  it('::balanza:: se inclina hacia el lado mayor y queda horizontal si son iguales', () => {
    expect(html('::balanza::4+7::5+6::')).toContain('y1="40" x2="190" y2="40"');
    expect(html('::balanza::6+3::10::')).toContain('y1="28" x2="190" y2="52"'); // baja el lado del 10
    expect(html('::balanza::6+3::10::')).not.toContain('equilibrada');
  });

  it('::barras:: dibuja una barra por categoría, con eje graduado y sin marcador crudo', () => {
    const salida = html('::barras::Fútbol=10;Básquetbol=6;Natación=8:: ¿Qué deporte prefieren más?');
    expect((salida.match(/<rect /g) || []).length).toBe(3);
    expect(salida).toContain('Natación');
    expect(salida).toContain('>10<');
    expect(salida).not.toContain('::');
  });
  it('::barras:: con dos series, leyenda y eje cortado (gráfico engañoso) marca el corte', () => {
    const salida = html('::barras::Ene=40/55;Feb=48/50::leyenda=Tienda A/Tienda B;eje=30:: ¿Qué tienda vendió más?');
    expect((salida.match(/<rect [^>]*fill="#(5B4FE9|FF6B4A)" rx/g) || []).length).toBe(4);
    expect(salida).toContain('Tienda B');
    expect(salida).toContain('>30<');
    expect(salida).not.toContain('>0<');
    expect(salida).toContain('<path d="M');
    expect(salida).not.toContain('::');
  });

  it('::linea:: une los puntos, admite negativos y decimales con coma y rotula el eje', () => {
    const salida = html('::linea::Lun=-2;Mar=3,5;Mié=8::y=Temperatura (°C):: ¿Qué día hizo más calor?');
    expect((salida.match(/<circle /g) || []).length).toBe(3);
    expect(salida).toContain('<polyline');
    expect(salida).toContain('Temperatura (°C)');
    expect(salida).not.toContain('::');
  });

  it('::circular:: dibuja un sector por categoría y muestra % solo si suman 100', () => {
    const conPct = html('::circular::Bus=50;Metro=30;Bicicleta=20::');
    expect((conPct.match(/<path /g) || []).length).toBe(3);
    expect(conPct).toContain('Bus — 50 %');
    expect(html('::circular::Bus=12;Metro=8::')).toContain('Bus — 12<');
    expect(html('::circular::Bus=50;Metro=50::valores=no::')).not.toContain('50');
  });

  it('::caja:: dibuja caja, mediana y bigotes de cada grupo', () => {
    const salida = html('::caja::Grupo C=10/15/18/22/30;Grupo D=12/16/20/21/24::x=Minutos::');
    expect((salida.match(/fill="#E9E7FD"/g) || []).length).toBe(2);
    expect(salida).toContain('Grupo D');
    expect(salida).toContain('Minutos');
    expect(salida).not.toContain('::');
  });

  it('::mapa:: dibuja los países, las letras sobre cada país y la rosa de los vientos', () => {
    const salida = html('::mapa::sudamerica::A@Perú;B@Bolivia;C@-30,-60::pintar=Chile;rosa=si:: ¿Qué país es la letra A?');
    expect((salida.match(/<path d="M/g) || []).length).toBeGreaterThan(10);
    expect(salida).toContain('fill="#C9C3FB"');          // Chile pintado
    expect(salida).toContain('>A</text>');
    expect(salida).toContain('>N</text>');
    expect(salida).not.toContain('Perú');                 // sin nombres: no delata la respuesta
    expect(salida).not.toContain('::');
  });

  it('::mapa:: de Chile admite íconos, marcas vacías y zonas naturales', () => {
    expect(html('::mapa::chile::🛶@-52,-73.5::')).toContain('🛶');
    // Coordenadas con decimales: marked las convertía en enlaces mailto.
    const conDecimales = html('::mapa::america::1@-34.6,-58.4;Santiago@-33.45,-70.66::');
    expect(conDecimales).toContain('<svg');
    expect(conDecimales).not.toContain('mailto');
    const zonas = html('::mapa::chile::::zonas=si::');
    expect(zonas).toContain('Norte Chico');
    expect(zonas).not.toContain('::');
  });

  it('::mapa:: con un país desconocido no dibuja nada (error visible en la revisión)', () => {
    expect(html('::mapa::sudamerica::A@Atlántida::')).not.toContain('<svg');
  });
});

