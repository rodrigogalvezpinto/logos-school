/**
 * Plano cartesiano dibujado en SVG (2026-11-17). Sirve para figuras que el temario pide «representar en el
 * plano» y que no son gráficos de datos: circunferencia de centro y radio dados (3.° medio), homotecia con su
 * centro y la figura ampliada (1.° medio), traslaciones, reflexiones.
 *
 * Sintaxis:  ::plano::elemento;elemento;...::
 *   poligono A(1,1) B(3,1) C(1,3)   polígono cerrado, con cada vértice rotulado
 *   circulo C(2,1) r=3              circunferencia con su centro rotulado
 *   punto O(0,0)                    punto suelto
 *   segmento O(0,0) A'(2,2)         línea punteada (rayos de una homotecia, radios)
 *   sinejes                         dibujo sin ejes ni números (redes de cuerpos geométricos)
 * Un nombre que empieza con «_» no se rotula. Coordenadas con punto decimal. Cada polígono o circunferencia usa un color distinto, en orden.
 */
export const RE_PLANO = /::plano::([^\n]{5,500}?)::/g;

type Punto = { n: string; x: number; y: number };
const COLORES = ['#5B4FE9', '#FF6B4A', '#059669', '#D97706'];
const esc = (s: string) => s.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');

function puntos(t: string): Punto[] {
  return [...t.matchAll(/([A-Za-z_][A-Za-z0-9_'’]{0,3})\s*\(\s*(-?\d+(?:\.\d+)?)\s*,\s*(-?\d+(?:\.\d+)?)\s*\)/g)].map(
    (m) => ({ n: m[1], x: parseFloat(m[2]), y: parseFloat(m[3]) }),
  );
}

export function htmlPlano(def: string): string {
  const partes = def.split(';').map((e) => e.trim());
  const sinEjes = partes.includes('sinejes');
  const elems = partes.filter((e) => e !== 'sinejes').map((e) => e.trim()).filter(Boolean).map((e) => {
    const tipo = e.split(/\s+/)[0];
    const r = e.match(/r\s*=\s*(\d+(?:\.\d+)?)/);
    return { tipo, pts: puntos(e), r: r ? parseFloat(r[1]) : 0 };
  });
  if (!elems.length || elems.some((e) => !['poligono', 'circulo', 'punto', 'segmento'].includes(e.tipo) || !e.pts.length)) return '';
  const xs = sinEjes ? [] as number[] : [0], ys = sinEjes ? [] as number[] : [0];
  for (const e of elems) for (const p of e.pts) { xs.push(p.x - e.r, p.x + e.r); ys.push(p.y - e.r, p.y + e.r); }
  const x0 = Math.floor(Math.min(...xs)) - 1, x1 = Math.ceil(Math.max(...xs)) + 1;
  const y0 = Math.floor(Math.min(...ys)) - 1, y1 = Math.ceil(Math.max(...ys)) + 1;
  const u = Math.min(36, 300 / Math.max(x1 - x0, y1 - y0));
  const W = (x1 - x0) * u, H = (y1 - y0) * u;
  const X = (x: number) => +((x - x0) * u).toFixed(1), Y = (y: number) => +((y1 - y) * u).toFixed(1);
  let s = `<rect width="${W}" height="${H}" fill="#fff"/>`;
  const paso = x1 - x0 > 16 || y1 - y0 > 16 ? 2 : 1;
  for (let x = x0; x <= x1; x++) {
    s += `<line x1="${X(x)}" y1="0" x2="${X(x)}" y2="${H}" stroke="#E5E7EB"/>`;
    if (!sinEjes && x !== 0 && x % paso === 0 && x > x0 && x < x1) s += `<text x="${X(x)}" y="${Y(0) + 12}" font-size="9" text-anchor="middle" fill="#6B7280">${x}</text>`;
  }
  for (let y = y0; y <= y1; y++) {
    s += `<line x1="0" y1="${Y(y)}" x2="${W}" y2="${Y(y)}" stroke="#E5E7EB"/>`;
    if (!sinEjes && y !== 0 && y % paso === 0 && y > y0 && y < y1) s += `<text x="${X(0) - 4}" y="${Y(y) + 3}" font-size="9" text-anchor="end" fill="#6B7280">${y}</text>`;
  }
  if (!sinEjes) s += `<line x1="0" y1="${Y(0)}" x2="${W}" y2="${Y(0)}" stroke="#374151" stroke-width="1.3"/>` +
    `<line x1="${X(0)}" y1="0" x2="${X(0)}" y2="${H}" stroke="#374151" stroke-width="1.3"/>` +
    `<text x="${W - 4}" y="${Y(0) - 4}" font-size="11" text-anchor="end" fill="#374151">x</text>` +
    `<text x="${X(0) + 5}" y="11" font-size="11" fill="#374151">y</text>`;
  let color = 0;
  const rotulo = (p: Punto, c: string) => p.n.startsWith('_') ? '' :
    `<circle cx="${X(p.x)}" cy="${Y(p.y)}" r="3" fill="${c}"/>` +
    `<text x="${X(p.x) + 5}" y="${Y(p.y) - 5}" font-size="11" font-weight="700" fill="${c}" stroke="#fff" stroke-width="2.5" paint-order="stroke">${esc(p.n)}</text>`;
  for (const e of elems) {
    if (e.tipo === 'segmento' && e.pts.length >= 2) {
      const [a, b] = e.pts;
      s += `<line x1="${X(a.x)}" y1="${Y(a.y)}" x2="${X(b.x)}" y2="${Y(b.y)}" stroke="#9CA3AF" stroke-dasharray="4 3"/>`;
      continue;
    }
    const c = e.tipo === 'punto' ? '#111827' : COLORES[color++ % COLORES.length];
    if (e.tipo === 'poligono') {
      s += `<polygon points="${e.pts.map((p) => `${X(p.x)},${Y(p.y)}`).join(' ')}" fill="${c}" fill-opacity="0.12" stroke="${c}" stroke-width="2"/>`;
    } else if (e.tipo === 'circulo') {
      s += `<circle cx="${X(e.pts[0].x)}" cy="${Y(e.pts[0].y)}" r="${+(e.r * u).toFixed(1)}" fill="${c}" fill-opacity="0.08" stroke="${c}" stroke-width="2"/>`;
    }
  }
  color = 0;
  for (const e of elems) {
    if (e.tipo === 'segmento') continue;
    const c = e.tipo === 'punto' ? '#111827' : COLORES[color++ % COLORES.length];
    for (const p of e.tipo === 'circulo' ? e.pts.slice(0, 1) : e.pts) s += rotulo(p, c);
  }
  return `<span class="grafico plano" role="img" aria-label="plano cartesiano"><svg viewBox="0 0 ${W} ${H}" width="${W}" height="${H}">${s}</svg></span>`;
}
