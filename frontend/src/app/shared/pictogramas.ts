/**
 * Emoji → imagen (2026-11-17). Los emoji se veían distinto según el equipo, a veces como un cuadrado vacío, y no
 * salían al imprimir o guardar en PDF. Ahora cada emoji del material se muestra como una ilustración propia
 * (`public/assets/pictogramas/`, Wikimedia Commons con licencia libre: ver CREDITOS.md en esa carpeta).
 * El contenido sigue escrito con emoji (son la «clave» de cada dibujo); el cambio ocurre solo al renderizar.
 *
 * - Fuera de un SVG: el emoji se cambia por <img class="pictograma">.
 * - Dentro de un SVG (dibujos de posición, mapas): `<text …>🐱</text>` se cambia por `<image …>` del mismo tamaño.
 * Los símbolos de texto (→, ✓) no son emoji de dibujo y se dejan como están.
 */
import { PICTOGRAMAS } from './pictogramas-datos';

const RUTA = '/assets/pictogramas/';
const EMO = String.raw`(?:[\u{1F300}-\u{1FAFF}\u{2600}-\u{27BF}\u{2B50}\u{2B55}\u{231A}\u{231B}\u{23F0}-\u{23FF}]\u{FE0F}?(?:\u{200D}[\u{1F300}-\u{1FAFF}\u{2600}-\u{27BF}]\u{FE0F}?)*)`;
const RE_EMO = new RegExp(EMO, 'gu');
const RE_TEXTO_SVG = new RegExp(String.raw`<text([^>]*)>\s*(${EMO})\s*</text>`, 'gu');

const buscar = (e: string) => PICTOGRAMAS[e.replace(/\u{FE0F}/gu, '')];
const atributo = (attrs: string, nombre: string) => {
  const m = attrs.match(new RegExp(`\\b${nombre}="(-?[\\d.]+)"`));
  return m ? parseFloat(m[1]) : undefined;
};

export function imgPictograma(e: string, alt?: string): string | null {
  const p = buscar(e);
  return p ? `<img class="pictograma" src="${RUTA}${p[0]}" alt="${alt ?? p[1]}" draggable="false">` : null;
}

export function reemplazarPictogramas(html: string): string {
  // 1) Dentro de SVG: el emoji ocupa un cuadrado de lado font-size, centrado en x y con la base en y.
  html = html.replace(RE_TEXTO_SVG, (m, attrs: string, e: string) => {
    const p = buscar(e);
    if (!p) return m;
    const x = atributo(attrs, 'x') ?? 0, y = atributo(attrs, 'y') ?? 0, t = atributo(attrs, 'font-size') ?? 16;
    const x0 = /text-anchor="middle"/.test(attrs) ? x - t / 2 : x;
    return `<image href="${RUTA}${p[0]}" x="${+x0.toFixed(1)}" y="${+(y - t * 0.88).toFixed(1)}" width="${t}" height="${t}"><title>${p[1]}</title></image>`;
  });
  // 2) Fuera de etiquetas y fuera de SVG: emoji → <img>.
  let enSvg = 0;
  return html.replace(/(<[^>]*>)|([^<]+)/g, (_m, etiqueta: string | undefined, texto: string | undefined) => {
    if (etiqueta) {
      if (/^<svg\b/i.test(etiqueta)) enSvg++;
      else if (/^<\/svg>/i.test(etiqueta)) enSvg = Math.max(0, enSvg - 1);
      return etiqueta;
    }
    return enSvg ? texto! : texto!.replace(RE_EMO, (e) => imgPictograma(e) ?? e);
  });
}
