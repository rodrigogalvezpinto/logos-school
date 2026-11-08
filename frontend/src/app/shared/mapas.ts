/**
 * Mapas dibujados en SVG (auditoría Fase 1, grupo B, 2026-11-07). El temario pide ubicar países, zonas
 * y puntos cardinales en mapas; antes se pedía «imaginar un mapa» descrito con palabras, que a menudo
 * dejaba la respuesta escrita en el enunciado. Contornos: Natural Earth (dominio público), ver
 * scripts/mapas/generar_mapas.py.
 *
 * Sintaxis:  ::mapa::región::marcas::[opciones::]
 *   región    america | sudamerica | chile
 *   marcas    separadas por «;»: TEXTO@País o TEXTO@lat,lon (decimales con punto).
 *             TEXTO de 1–2 letras o números → círculo con la letra; emoji → ícono; palabra → rótulo.
 *             Puede quedar vacío: ::mapa::sudamerica::::pintar=Chile::
 *   opciones  pintar=Chile/Perú (colorea países), nombres=si (escribe los nombres de los países),
 *             rosa=si (rosa de los vientos), zonas=si (zonas naturales de Chile, solo en «chile»).
 */
import { CENTROS, MAPAS } from './mapas-datos';

const OPCION = String.raw`(?:pintar|nombres|rosa|zonas)=[^:;]{0,80}`;
export const RE_MAPA = new RegExp(
  String.raw`::mapa::(america|sudamerica|chile)::((?:[^:;@]{1,24}@[^:;@]{1,40};?){0,12})::(?:(${OPCION}(?:;${OPCION})*)::)?`,
  'g',
);

const esc = (s: string) => s.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
const EMOJI = /\p{Extended_Pictographic}/u;

// Límites aproximados entre las zonas naturales de Chile (latitud) y su nombre.
const ZONAS: [number, string][] = [[-17.5, 'Norte Grande'], [-27, 'Norte Chico'], [-32, 'Zona Central'], [-38, 'Zona Sur'], [-42, 'Zona Austral']];

/** Lado mayor del recuadro que ocupa un país (px): los muy pequeños no se rotulan, se amontonarían. */
function tamano(d: string): number {
  const n = (d.match(/-?\d+(?:\.\d+)?/g) ?? []).map(Number);
  const xs = n.filter((_v, i) => i % 2 === 0), ys = n.filter((_v, i) => i % 2 === 1);
  return Math.max(Math.max(...xs) - Math.min(...xs), Math.max(...ys) - Math.min(...ys));
}

export function htmlMapa(region: string, marcas: string, opciones?: string): string {
  const m = MAPAS[region];
  if (!m) return '';
  const op: Record<string, string> = {};
  for (const p of (opciones ?? '').split(';')) {
    const i = p.indexOf('=');
    if (i > 0) op[p.slice(0, i).trim()] = p.slice(i + 1).trim();
  }
  const xy = (lat: number, lon: number): [number, number] => [(lon - m.lonMin) * m.k * m.c, (m.latMax - lat) * m.k];
  const pintados = new Set((op['pintar'] ?? '').split('/').map((s) => s.trim()).filter(Boolean));
  const margenIzq = region === 'chile' && op['zonas'] === 'si' ? 92 : 0;
  const ancho = m.ancho + margenIzq;
  let s = `<rect x="0" y="0" width="${ancho}" height="${m.alto}" fill="#DCEFFB"/><g transform="translate(${margenIzq} 0)">`;
  for (const [pais, d] of Object.entries(m.paises)) {
    const relleno = pintados.has(pais) ? '#C9C3FB' : pais === 'Chile' && region === 'chile' ? '#FFF7ED' : '#F6F5F2';
    s += `<path d="${d}" fill="${relleno}" stroke="#8B93A1" stroke-width="0.7" stroke-linejoin="round"/>`;
  }
  if (op['nombres'] === 'si') {
    for (const [pais, [lat, lon]] of Object.entries(CENTROS)) {
      const [x, y] = xy(lat, lon);
      if (!m.paises[pais] || x < 8 || x > m.ancho - 8 || y < 8 || y > m.alto - 8 || tamano(m.paises[pais]) < 28) continue;
      s += `<text x="${x}" y="${y}" font-size="10" text-anchor="middle" fill="#374151" stroke="#fff" stroke-width="2.5" paint-order="stroke">${esc(pais)}</text>`;
    }
  }
  s += '</g>';
  if (region === 'chile' && op['zonas'] === 'si') {
    ZONAS.forEach(([lat, nombre], i) => {
      const y0 = xy(lat, 0)[1], y1 = i + 1 < ZONAS.length ? xy(ZONAS[i + 1][0], 0)[1] : m.alto;
      if (i > 0) s += `<line x1="0" y1="${y0}" x2="${ancho}" y2="${y0}" stroke="#6B7280" stroke-dasharray="4 3"/>`;
      s += `<text x="6" y="${(y0 + y1) / 2 + 4}" font-size="11" fill="#111827" font-weight="600">${esc(nombre)}</text>`;
    });
  }
  s += `<g transform="translate(${margenIzq} 0)">`;
  for (const marca of marcas.split(';').filter((x) => x.includes('@'))) {
    const [texto, lugar] = marca.split('@').map((x) => x.trim());
    let pos: [number, number] | undefined;
    const coord = lugar.match(/^(-?\d+(?:\.\d+)?)\s*,\s*(-?\d+(?:\.\d+)?)$/);
    if (coord) pos = xy(parseFloat(coord[1]), parseFloat(coord[2]));
    else if (CENTROS[lugar]) pos = xy(...CENTROS[lugar]);
    if (!pos) return '';
    const [x, y] = pos;
    if (EMOJI.test(texto)) {
      s += `<text x="${x}" y="${y + 7}" font-size="20" text-anchor="middle">${texto}</text>`;
    } else if (texto.length <= 2) {
      s += `<circle cx="${x}" cy="${y}" r="10" fill="#fff" stroke="#5B4FE9" stroke-width="2"/>` +
        `<text x="${x}" y="${y + 4.5}" font-size="13" font-weight="700" text-anchor="middle" fill="#3B2FC9">${esc(texto)}</text>`;
    } else {
      s += `<circle cx="${x}" cy="${y}" r="3" fill="#FF6B4A"/>` +
        `<text x="${x + 6}" y="${y + 4}" font-size="11" fill="#111827" stroke="#fff" stroke-width="3" paint-order="stroke">${esc(texto)}</text>`;
    }
  }
  s += '</g>';
  if (op['rosa'] === 'si') {
    // En Chile, sobre el océano a la izquierda (a un tercio de la altura); en los demás, arriba a la derecha.
    const [cx, cy] = region === 'chile' ? [margenIzq + 30, Math.round(m.alto * 0.3)] : [ancho - 30, 32];
    s += `<g font-size="11" font-weight="700" text-anchor="middle" fill="#111827">` +
      `<circle cx="${cx}" cy="${cy}" r="17" fill="#fff" stroke="#8B93A1"/>` +
      `<path d="M${cx} ${cy - 13} L${cx + 4} ${cy} L${cx} ${cy + 13} L${cx - 4} ${cy} Z" fill="#FF6B4A"/>` +
      `<path d="M${cx - 13} ${cy} L${cx} ${cy - 4} L${cx + 13} ${cy} L${cx} ${cy + 4} Z" fill="#5B4FE9" opacity="0.8"/>` +
      `<text x="${cx}" y="${cy - 20}">N</text><text x="${cx}" y="${cy + 29}">S</text>` +
      `<text x="${cx + 24}" y="${cy + 4}">E</text><text x="${cx - 24}" y="${cy + 4}">O</text></g>`;
  }
  return `<span class="grafico mapa" role="img" aria-label="mapa"><svg viewBox="0 0 ${ancho} ${m.alto}" width="${ancho}" height="${m.alto}">${s}</svg></span>`;
}
