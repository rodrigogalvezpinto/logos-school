/**
 * Gráficos dibujados en SVG a partir de marcadores en el contenido (auditoría Fase 1, grupo B, 2026-11-07).
 *
 * El temario pide «leer e interpretar» gráficos de barras, de líneas, circulares y diagramas de cajón.
 * Antes se describían con palabras («la barra de B llega a 100»), lo que reemplaza la lectura que se
 * quiere evaluar. Se dibujan con código, sin imágenes externas: son exactos y gratuitos.
 *
 * Sintaxis común:  ::tipo::Etiqueta=valor;Etiqueta=valor::[opciones::]
 *   tipo      barras | linea | circular | caja
 *   valor     número con coma o punto decimal, puede ser negativo. «40/55» = dos series (barras, linea).
 *             En caja: mínimo/Q1/mediana/Q3/máximo.
 *   opciones  separadas por «;»: eje=95 (el eje vertical parte en 95, para enseñar gráficos engañosos),
 *             leyenda=Tienda A/Tienda B, x=Mes, y=Temperatura (°C), valores=no (circular sin cifras),
 *             valores=si (barras y líneas con la cifra sobre cada barra o punto, para leer valores exactos).
 * Ejemplo: ::linea::Lun=12;Mar=15;Mié=9::y=°C::
 */
export type TipoGrafico = 'barras' | 'linea' | 'circular' | 'caja';

const OPCION = String.raw`(?:eje|leyenda|valores|x|y)=[^:;]{0,60}`;
export const RE_GRAFICO = new RegExp(
  String.raw`::(barras|linea|circular|caja)::((?:[^:=;]{1,30}=-?[\d.,/-]{1,40};?){1,12})::(?:(${OPCION}(?:;${OPCION})*)::)?`,
  'g',
);

const COLORES = ['#5B4FE9', '#FF6B4A', '#0F9F8F', '#E89B0C', '#2B8FD6', '#8B93A1'];
const TINTA = '#111827';
const GRIS = '#374151';
const REJILLA = '#E5E7EB';

const num = (s: string) => parseFloat(s.trim().replace(',', '.'));
const fmt = (v: number) => (Math.round(v * 100) / 100).toString().replace('.', ',');
const esc = (s: string) => s.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');

interface Dato { et: string; v: number[] }

function leerDatos(datos: string): Dato[] {
  return datos.split(';').filter((d) => d.includes('=')).map((d) => {
    const i = d.indexOf('=');
    return { et: d.slice(0, i).trim(), v: d.slice(i + 1).split('/').map(num) };
  });
}

function leerOpciones(op?: string): Record<string, string> {
  const r: Record<string, string> = {};
  for (const p of (op ?? '').split(';')) {
    const i = p.indexOf('=');
    if (i > 0) r[p.slice(0, i).trim()] = p.slice(i + 1).trim();
  }
  return r;
}

/** Paso «redondo» (1, 2, 5 × 10^k) para que el eje tenga entre 4 y 10 marcas. */
function pasoEje(rango: number): number {
  const bruto = rango / 8;
  const p = Math.pow(10, Math.floor(Math.log10(bruto || 1)));
  return [1, 2, 5, 10].map((k) => k * p).find((s) => rango / s <= 10) ?? 10 * p;
}

function envolver(tipo: string, ancho: number, alto: number, svg: string): string {
  return `<span class="grafico" role="img" aria-label="${tipo}"><svg viewBox="0 0 ${ancho} ${alto}" width="${ancho}" height="${alto}">${svg}</svg></span>`;
}

function leyenda(nombres: string[], x: number, y: number): string {
  return nombres.map((n, i) =>
    `<rect x="${x + i * 120}" y="${y - 9}" width="10" height="10" rx="2" fill="${COLORES[i]}"/>` +
    `<text x="${x + i * 120 + 14}" y="${y}" font-size="11" fill="${TINTA}">${esc(n)}</text>`).join('');
}

/** Ejes cartesianos con categorías en x; usado por barras y líneas. */
function cartesiano(tipo: 'barras' | 'linea', datos: Dato[], op: Record<string, string>): string {
  const series = Math.max(...datos.map((d) => d.v.length));
  const todos = datos.flatMap((d) => d.v);
  const eje = op['eje'] !== undefined ? num(op['eje']) : undefined;
  let min = eje ?? Math.min(0, ...todos);
  const maxDato = Math.max(...todos);
  const paso = pasoEje(maxDato - min);
  if (eje === undefined) min = Math.floor(min / paso) * paso;
  const tope = Math.ceil(maxDato / paso) * paso;
  const nombres = op['leyenda'] ? op['leyenda'].split('/') : [];
  const hayLeyenda = series > 1 && nombres.length > 0;
  const conValores = op['valores'] === 'si';
  const etY = op['y'];
  const x0 = etY ? 52 : 40, arriba = (hayLeyenda ? 26 : 12) + (etY ? 6 : 0), alto = 170;
  const largoEt = Math.max(...datos.map((d) => d.et.length)) * 6.4 + 10; // que las etiquetas no se monten
  const anchoCat = Math.max(tipo === 'barras' ? (series > 1 ? 22 * series + 16 : 62) : 56, largoEt);
  const ancho = Math.max(260, x0 + datos.length * anchoCat + 16);
  const y = (v: number) => arriba + alto - ((v - min) / (tope - min || 1)) * alto;
  let s = '';
  for (let v = min; v <= tope + paso / 1000; v += paso) {
    s += `<line x1="${x0}" y1="${y(v)}" x2="${ancho - 6}" y2="${y(v)}" stroke="${REJILLA}"/>` +
      `<text x="${x0 - 6}" y="${y(v) + 4}" font-size="11" text-anchor="end" fill="${GRIS}">${fmt(v)}</text>`;
  }
  const sep = (ancho - x0 - 10) / datos.length;
  const cx = (i: number) => x0 + sep * i + sep / 2;
  if (tipo === 'barras') {
    const bw = Math.min(series > 1 ? 24 : 34, (sep - 12) / series);
    datos.forEach((d, i) => d.v.forEach((v, k) => {
      const x = cx(i) - (bw * series) / 2 + k * bw;
      const base = y(Math.max(min, 0)), cima = y(v);
      s += `<rect x="${x}" y="${Math.min(base, cima)}" width="${bw - (series > 1 ? 2 : 0)}" height="${Math.abs(base - cima)}" fill="${COLORES[k]}" rx="2"/>`;
      if (conValores) s += `<text x="${x + bw / 2 - (series > 1 ? 1 : 0)}" y="${cima - 4}" font-size="10" text-anchor="middle" fill="${TINTA}">${fmt(v)}</text>`;
    }));
  } else {
    for (let k = 0; k < series; k++) {
      const pts = datos.filter((d) => d.v[k] !== undefined && !isNaN(d.v[k])).map((d) => [cx(datos.indexOf(d)), y(d.v[k])]);
      s += `<polyline points="${pts.map((p) => p.join(',')).join(' ')}" fill="none" stroke="${COLORES[k]}" stroke-width="2.5"/>` +
        pts.map(([px, py], j) => `<circle cx="${px}" cy="${py}" r="3.5" fill="${COLORES[k]}"/>` +
          (conValores ? `<text x="${px}" y="${py - 8}" font-size="10" text-anchor="middle" fill="${TINTA}">${fmt(datos.filter((d) => d.v[k] !== undefined && !isNaN(d.v[k]))[j].v[k])}</text>` : '')).join('');
    }
  }
  datos.forEach((d, i) => {
    s += `<text x="${cx(i)}" y="${arriba + alto + 16}" font-size="11" text-anchor="middle" fill="${TINTA}">${esc(d.et)}</text>`;
  });
  s += `<line x1="${x0}" y1="${arriba}" x2="${x0}" y2="${arriba + alto}" stroke="${GRIS}" stroke-width="1.5"/>` +
    `<line x1="${x0}" y1="${arriba + alto}" x2="${ancho - 6}" y2="${arriba + alto}" stroke="${GRIS}" stroke-width="1.5"/>`;
  if (eje !== undefined && eje > 0) {
    // El corte del eje se marca, como en los gráficos de prensa: el alumno debe notarlo.
    s += `<path d="M${x0 - 5} ${arriba + alto - 8} l10 -4 M${x0 - 5} ${arriba + alto - 3} l10 -4" stroke="${GRIS}" stroke-width="1.5"/>`;
  }
  if (etY) s += `<text x="12" y="${arriba + alto / 2}" font-size="11" fill="${GRIS}" text-anchor="middle" transform="rotate(-90 12 ${arriba + alto / 2})">${esc(etY)}</text>`;
  let altoTotal = arriba + alto + 26;
  if (op['x']) {
    s += `<text x="${(x0 + ancho) / 2}" y="${altoTotal + 4}" font-size="11" fill="${GRIS}" text-anchor="middle">${esc(op['x'])}</text>`;
    altoTotal += 14;
  }
  if (hayLeyenda) s += leyenda(nombres, x0, 14);
  return envolver(tipo === 'barras' ? 'gráfico de barras' : 'gráfico de líneas', ancho, altoTotal, s);
}

function circular(datos: Dato[], op: Record<string, string>): string {
  const total = datos.reduce((a, d) => a + d.v[0], 0) || 1;
  const porcentaje = Math.abs(total - 100) < 0.01;
  const conValores = op['valores'] !== 'no';
  const r = 78, cx = 90, cy = 92;
  let ang = -Math.PI / 2, s = '';
  datos.forEach((d, i) => {
    const frac = d.v[0] / total;
    const a2 = ang + frac * 2 * Math.PI;
    const color = COLORES[i % COLORES.length];
    if (frac >= 0.9999) {
      s += `<circle cx="${cx}" cy="${cy}" r="${r}" fill="${color}"/>`;
    } else {
      const [x1, y1, x2, y2] = [cx + r * Math.cos(ang), cy + r * Math.sin(ang), cx + r * Math.cos(a2), cy + r * Math.sin(a2)];
      s += `<path d="M${cx} ${cy} L${x1} ${y1} A${r} ${r} 0 ${frac > 0.5 ? 1 : 0} 1 ${x2} ${y2} Z" fill="${color}" stroke="#fff" stroke-width="1.5"/>`;
    }
    const valor = conValores ? ` — ${fmt(d.v[0])}${porcentaje ? ' %' : ''}` : '';
    s += `<rect x="190" y="${24 + i * 22}" width="12" height="12" rx="2" fill="${color}"/>` +
      `<text x="208" y="${34 + i * 22}" font-size="12" fill="${TINTA}">${esc(d.et)}${valor}</text>`;
    ang = a2;
  });
  return envolver('gráfico circular', 340, Math.max(186, 34 + datos.length * 22), s);
}

function caja(datos: Dato[], op: Record<string, string>): string {
  const todos = datos.flatMap((d) => d.v);
  const paso = pasoEje(Math.max(...todos) - Math.min(...todos));
  const min = Math.floor(Math.min(...todos) / paso) * paso, max = Math.ceil(Math.max(...todos) / paso) * paso;
  const x0 = 78, ancho = 360, fila = 46;
  const x = (v: number) => x0 + ((v - min) / (max - min || 1)) * (ancho - x0 - 16);
  const base = 12 + datos.length * fila;
  let s = '';
  for (let v = min; v <= max + paso / 1000; v += paso) {
    s += `<line x1="${x(v)}" y1="8" x2="${x(v)}" y2="${base}" stroke="${REJILLA}"/>` +
      `<text x="${x(v)}" y="${base + 16}" font-size="11" text-anchor="middle" fill="${GRIS}">${fmt(v)}</text>`;
  }
  datos.forEach((d, i) => {
    const [mn, q1, me, q3, mx] = d.v;
    const yc = 12 + i * fila + fila / 2 - 4, h = 24;
    s += `<text x="${x0 - 8}" y="${yc + 4}" font-size="12" text-anchor="end" fill="${TINTA}">${esc(d.et)}</text>` +
      `<line x1="${x(mn)}" y1="${yc}" x2="${x(q1)}" y2="${yc}" stroke="${GRIS}" stroke-width="1.5"/>` +
      `<line x1="${x(q3)}" y1="${yc}" x2="${x(mx)}" y2="${yc}" stroke="${GRIS}" stroke-width="1.5"/>` +
      `<line x1="${x(mn)}" y1="${yc - 8}" x2="${x(mn)}" y2="${yc + 8}" stroke="${GRIS}" stroke-width="1.5"/>` +
      `<line x1="${x(mx)}" y1="${yc - 8}" x2="${x(mx)}" y2="${yc + 8}" stroke="${GRIS}" stroke-width="1.5"/>` +
      `<rect x="${x(q1)}" y="${yc - h / 2}" width="${x(q3) - x(q1)}" height="${h}" fill="#E9E7FD" stroke="${COLORES[0]}" stroke-width="1.5"/>` +
      `<line x1="${x(me)}" y1="${yc - h / 2}" x2="${x(me)}" y2="${yc + h / 2}" stroke="${COLORES[1]}" stroke-width="2.5"/>`;
  });
  s += `<line x1="${x0}" y1="${base}" x2="${ancho - 16}" y2="${base}" stroke="${GRIS}" stroke-width="1.5"/>`;
  let alto = base + 26;
  if (op['x']) {
    s += `<text x="${(x0 + ancho) / 2}" y="${alto + 4}" font-size="11" fill="${GRIS}" text-anchor="middle">${esc(op['x'])}</text>`;
    alto += 14;
  }
  return envolver('diagrama de cajón', ancho, alto, s);
}

export function htmlGrafico(tipo: string, datos: string, opciones?: string): string {
  const d = leerDatos(datos), op = leerOpciones(opciones);
  if (!d.length || d.some((x) => x.v.some((v) => isNaN(v)))) return '';
  if (tipo === 'circular') return circular(d, op);
  if (tipo === 'caja') return d.every((x) => x.v.length === 5) ? caja(d, op) : '';
  return cartesiano(tipo as 'barras' | 'linea', d, op);
}
