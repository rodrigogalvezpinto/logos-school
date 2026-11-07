import { Pipe, PipeTransform, inject } from '@angular/core';
import { DomSanitizer, SafeHtml } from '@angular/platform-browser';
import { marked } from 'marked';
import katex from 'katex';

// Delimitadores matemáticos para KaTeX (compatibles con precios en pesos chilenos $15.000 sin colisión)
const RE_MATH_BLOCK_DOLLAR = /\$\$([\s\S]+?)\$\$/g;
const RE_MATH_BLOCK_BRACKET = /\\\[([\s\S]+?)\\\]/g;
const RE_MATH_BLOCK_TAG = /\[math:block\]([\s\S]+?)\[\/math:block\]/g;

const RE_MATH_INLINE_PAREN = /\\\(([\s\S]+?)\\\)/g;
const RE_MATH_INLINE_TAG = /\[math\]([\s\S]+?)\[\/math\]/g;
const RE_MATH_FRAC_TAG = /\[frac:\s*([^/\]]+)\s*\/\s*([^\]]+)\]/g;
const RE_MATH_SQRT_TAG = /\[sqrt(?:\s*\[\s*([^\]]+)\s*\])?:\s*([^\]]+)\]/g;
const RE_CHEM_TAG = /\[chem\]([\s\S]+?)\[\/chem\]/g;

// Patrones automáticos para contenido existente en texto plano
const RE_UNICODE_SQRT = /(?<![a-zA-Z0-9\\])√\s*(\d+|\([a-zA-Z0-9+−\s\*\^/]+\))/g;
const RE_NOTACION_CIENTIFICA = /(\d+(?:,\d+)?)\s*[×x]\s*10\^?([⁰¹²³⁴⁵⁶⁷⁸⁹\d]+|[−-]\d+)/g;
const RE_UNICODE_EXPONENTES = /([a-zA-Z0-9\)])([²³⁴⁵⁶⁷⁸⁹]+)/g;

const MAPA_SUPERSCRIPT: Record<string, string> = {
  '⁰': '0', '¹': '1', '²': '2', '³': '3', '⁴': '4',
  '⁵': '5', '⁶': '6', '⁷': '7', '⁸': '8', '⁹': '9',
  '⁻': '-', '⁺': '+',
};

function normalizarExponentes(s: string): string {
  return s.split('').map((c) => MAPA_SUPERSCRIPT[c] || c).join('');
}

function formatearQuimica(formula: string): string {
  let f = formula.trim().replace(/->|→/g, ' \\rightarrow ');
  if (!f.includes('\\text{')) {
    // Formatear fórmulas químicas simples como H2O -> \text{H}_2\text{O}, CO2 -> \text{CO}_2
    f = f.replace(/([A-Z][a-z]?)(\d+)/g, '\\text{$1}_{$2}');
    f = f.replace(/(?<![\\a-zA-Z])([A-Z][a-z]?)(?![a-zA-Z0-9_{])/g, '\\text{$1}');
  }
  return f;
}

function renderizarMatematica(texto: string): string {
  // 1. Fórmulas en bloque (display mode)
  let res = texto.replace(RE_MATH_BLOCK_DOLLAR, (_, formula) => {
    return katex.renderToString(formula.trim(), { displayMode: true, throwOnError: false });
  });
  res = res.replace(RE_MATH_BLOCK_BRACKET, (_, formula) => {
    return katex.renderToString(formula.trim(), { displayMode: true, throwOnError: false });
  });
  res = res.replace(RE_MATH_BLOCK_TAG, (_, formula) => {
    return katex.renderToString(formula.trim(), { displayMode: true, throwOnError: false });
  });

  // 2. Fórmulas en línea (inline mode)
  res = res.replace(RE_MATH_INLINE_PAREN, (_, formula) => {
    return katex.renderToString(formula.trim(), { displayMode: false, throwOnError: false });
  });
  res = res.replace(RE_MATH_INLINE_TAG, (_, formula) => {
    return katex.renderToString(formula.trim(), { displayMode: false, throwOnError: false });
  });

  // 3. Shorthand accesible para fracciones: [frac: numerador / denominador]
  res = res.replace(RE_MATH_FRAC_TAG, (_, num, den) => {
    return katex.renderToString(`\\frac{${num.trim()}}{${den.trim()}}`, {
      displayMode: false,
      throwOnError: false,
    });
  });

  // 4. Shorthand para raíces: [sqrt: x] o [sqrt[n]: x]
  res = res.replace(RE_MATH_SQRT_TAG, (_, idx, expr) => {
    const formula = idx ? `\\sqrt[${idx.trim()}]{${expr.trim()}}` : `\\sqrt{${expr.trim()}}`;
    return katex.renderToString(formula, { displayMode: false, throwOnError: false });
  });

  // 5. Shorthand para química: [chem] 2H2 + O2 -> 2H2O [/chem]
  res = res.replace(RE_CHEM_TAG, (_, formula) => {
    const fKatex = formatearQuimica(formula);
    return katex.renderToString(fKatex, { displayMode: false, throwOnError: false });
  });

  // 6. Detección automática de raíces cuadradas Unicode existentes (ej: √49, √16, √(x+3))
  res = res.replace(RE_UNICODE_SQRT, (_, radicando) => {
    const limpio = radicando.startsWith('(') && radicando.endsWith(')') ? radicando.slice(1, -1) : radicando;
    return katex.renderToString(`\\sqrt{${limpio.trim()}}`, { displayMode: false, throwOnError: false });
  });

  // 7. Detección automática de notación científica existente (ej: 6,02 × 10²³, 3 × 10^8)
  res = res.replace(RE_NOTACION_CIENTIFICA, (_, base, exp) => {
    const expNormal = normalizarExponentes(exp);
    const baseNormal = base.replace(',', '{,}');
    return katex.renderToString(`${baseNormal} \\times 10^{${expNormal}}`, {
      displayMode: false,
      throwOnError: false,
    });
  });

  // 8. Superíndices y potencias Unicode en texto plano (ej: 7², 8², m², cm³) -> <sup> más pequeños y elevados
  res = res.replace(RE_UNICODE_EXPONENTES, (_, base, exp) => {
    return `${base}<sup class="exponente-matematico">${normalizarExponentes(exp)}</sup>`;
  });

  return res;
}

// El contenido de las guías sigue siempre el mismo patrón de autoría (ver
// planificacion/04-modo-de-operacion.md y contenido/*.md): un párrafo en negrita
// "¿Por qué importa?" al inicio de cada OA, y cada ejemplo resuelto como su propio párrafo
// "**Ejemplo N — Título**" seguido del desarrollo. El texto plano resultante (todo con el
// mismo tamaño y color) es lo que el usuario reportó como "muy simple" — se realza acá,
// después del render de Markdown, en vez de tocar el contenido fuente de los 12 cursos.
const RE_POR_QUE_IMPORTA = /<p><strong>¿Por qué importa\?<\/strong>\s*([\s\S]*?)<\/p>/;
// El heading de esta sección no siempre es el mismo nivel en los 12 cursos (### en unos
// archivos, #### en otros) — se detecta cualquiera de los dos.
const RE_TITULO_EJEMPLOS = /<h([34])>Ejemplos resueltos<\/h[34]>/;
// "Ejemplo N — Título" en la mayoría de los cursos, "Actividad N — Título" en 1°-2°
// básico (mismo patrón de autoría, etiqueta distinta para el público más chico).
const RE_EJEMPLO = /<p><strong>(?:Ejemplo|Actividad) (\d+)\s*—\s*([^<]*)<\/strong><\/p>/g;
// 1°-2° básico describe ilustraciones que todavía no existen como imagen real (ver
// contenido/01-basico/*.md) con un marcador de texto "[Imagen: ...]" — sin esto se veía
// tal cual, entre corchetes, lo que confunde más que ayuda a un lector de 6-7 años. Se
// convierte en una tarjeta de marcador de posición mientras no haya ilustración real.
const RE_IMAGEN = /\[Imagen:\s*([^\]]+)\]/g;
// Nuevo: Convertir marcadores de emoji ::emoji::🦋::descripcion:: en HTML visual
// La descripción puede tener «:» y saltos de línea («dos redes: A) …»); antes no se convertía
// y el alumno veía el marcador crudo (hallazgo E2E 2026-11-07).
const RE_EMOJI = /::emoji::([^:\s]+)::([\s\S]+?)::/g;
// Conteo visual: ::contar::⭐::6:: dibuja 6 estrellas reales para contar. Antes se usaba
// ::emoji::⭐::6 estrellas dibujadas::, que mostraba UNA estrella y la cantidad escrita: el
// niño leía la respuesta en vez de contar (hallazgo de auditoría 2026-11-07).
export const RE_CONTAR = /::contar::([^:]+)::(\d{1,2})::/g;
// Dibujo sin rótulo: ::dibujo::☀️:: muestra solo el dibujo grande. En preguntas de escritura
// («¿cuál es la palabra bien escrita para este dibujo?») el rótulo «un sol» daba la respuesta.
export const RE_DIBUJO = /::dibujo::([^:]+)::/g;
// Fracción dibujada: ::fraccion::2::3:: muestra una barra en 3 partes iguales con 2 pintadas, sin
// escribir «2/3» (el componente [fraccion: n/d] escribía el número, es decir, la respuesta).
export const RE_FRACCION_VISUAL = /::fraccion::(\d{1,2})::(\d{1,2})::/g;
export function htmlFraccion(numerador: string, denominador: string): string {
  const d = Math.min(Math.max(parseInt(denominador, 10), 1), 12);
  const n = Math.min(parseInt(numerador, 10), d);
  const partes = Array.from({ length: d }, (_v, i) => `<span class="fraccion-barra__parte${i < n ? ' fraccion-barra__parte--pintada' : ''}"></span>`).join('');
  return `<span class="fraccion-barra" role="img" aria-label="figura dividida en ${d} partes iguales, ${n} pintadas">${partes}</span>`;
}
// Dibujo de posición: ::posicion::🐱::debajo::mesa:: dibuja el gato bajo una mesa, sin escribir
// «debajo». Antes la ilustración se describía con palabras («un gato está debajo de una mesa») y
// esa descripción era justo la respuesta (hallazgo de auditoría 2026-11-07). El objeto de
// referencia puede ser un emoji o una figura dibujada: «mesa» o «caja» (abierta, para «dentro»).
export const RE_POSICION = /::posicion::([^:\s]+)::(encima|debajo|dentro|izquierda|derecha|al-lado|delante|detras)::([^:\s]+)::/g;
// Fila vista de izquierda a derecha: ::fila::🌳::🪑::🎠:: (para «izquierda», «derecha», «entre»).
export const RE_FILA = /::fila::((?:[^:\s]+::){2,6})/g;
const emojiSvg = (e: string, x: number, y: number, tam: number) =>
  `<text x="${x}" y="${y}" font-size="${tam}" text-anchor="middle">${e}</text>`;
const MESA = '<rect x="50" y="62" width="140" height="9" rx="3" fill="#B7791F"/>' +
  '<rect x="60" y="71" width="8" height="62" fill="#975A16"/><rect x="172" y="71" width="8" height="62" fill="#975A16"/>';
const CAJA_FONDO = '<polygon points="70,80 170,80 185,68 85,68" fill="#C68B4E"/>';
const CAJA_FRENTE = '<rect x="70" y="80" width="100" height="52" fill="#DDA15E" stroke="#975A16" stroke-width="2"/>';
export function htmlPosicion(a: string, relacion: string, b: string): string {
  const suelo = '<line x1="10" y1="134" x2="230" y2="134" stroke="#CBD5E1" stroke-width="2"/>';
  let cuerpo: string;
  if (b === 'mesa') {
    const pos: Record<string, [number, number]> = { encima: [120, 58], debajo: [120, 130], 'al-lado': [212, 130], izquierda: [28, 130], derecha: [212, 130] };
    const [x, y] = pos[relacion] ?? pos['al-lado'];
    cuerpo = MESA + emojiSvg(a, x, y, 40);
  } else if (b === 'caja') {
    if (relacion === 'dentro') cuerpo = CAJA_FONDO + `<g transform="rotate(-20 120 78)">${emojiSvg(a, 120, 96, 52)}</g>` + CAJA_FRENTE;
    else {
      const pos: Record<string, [number, number]> = { encima: [120, 66], 'al-lado': [212, 130], izquierda: [32, 130], derecha: [212, 130] };
      const [x, y] = pos[relacion] ?? pos['al-lado'];
      cuerpo = CAJA_FONDO + CAJA_FRENTE + emojiSvg(a, x, y, 40);
    }
  } else {
    const capas: Record<string, string> = {
      izquierda: emojiSvg(a, 70, 128, 56) + emojiSvg(b, 170, 128, 56),
      derecha: emojiSvg(b, 70, 128, 56) + emojiSvg(a, 170, 128, 56),
      'al-lado': emojiSvg(a, 92, 128, 56) + emojiSvg(b, 152, 128, 56),
      encima: emojiSvg(b, 120, 130, 60) + emojiSvg(a, 120, 72, 44),
      debajo: emojiSvg(b, 120, 66, 60) + emojiSvg(a, 120, 130, 44),
      dentro: emojiSvg(b, 120, 126, 90) + emojiSvg(a, 120, 104, 30),
      delante: emojiSvg(b, 120, 104, 72) + emojiSvg(a, 138, 132, 50),
      detras: emojiSvg(a, 152, 116, 44) + emojiSvg(b, 112, 130, 72),
    };
    cuerpo = capas[relacion];
  }
  return `<span class="posicion" role="img" aria-label="dibujo"><svg viewBox="0 0 240 140" width="240" height="140">${suelo}${cuerpo}</svg></span>`;
}
export function htmlFila(lista: string): string {
  const items = lista.split('::').filter(Boolean).map((e) => `<span class="fila-dibujo__item">${e}</span>`).join('');
  return `<span class="fila-dibujo" role="img" aria-label="dibujo, de izquierda a derecha">${items}</span>`;
}
export function htmlContar(emoji: string, cantidad: string): string {
  const n = Math.min(parseInt(cantidad, 10), 30);
  return `<span class="contar" role="img" aria-label="${n} elementos para contar">${`<span class="contar__item">${emoji}</span>`.repeat(n)}</span>`;
}
// Componentes matemáticos: [recta: inicio-fin: valor] para recta numérica
const RE_RECTA = /\[recta:\s*(\d+)-(\d+):\s*(\d+)\]/g;
// Componentes matemáticos: [fraccion: numerador/denominador] para modelo de fracciones
const RE_FRACCION = /\[fraccion:\s*(\d+)\/(\d+)\]/g;

function realzarGuia(html: string): string {
  let resultado = html
    .replace(
      RE_POR_QUE_IMPORTA,
      '<div class="callout callout--importa"><p class="callout__titulo">¿Por qué importa?</p><p>$1</p></div>',
    )
    .replace(RE_TITULO_EJEMPLOS, '<h$1 class="titulo-ejemplos">Ejemplos resueltos</h$1>')
    .replace(RE_EJEMPLO, '<p class="ejemplo-titulo"><span class="ejemplo-num">$1</span>$2</p>')
    .replace(RE_IMAGEN, '<span class="marcador-imagen">🖼️ $1</span>');

  resultado = resultado.replace(RE_POSICION, (_m, a, rel, b) => htmlPosicion(a, rel, b));
  resultado = resultado.replace(RE_FILA, (_m, lista) => htmlFila(lista));
  resultado = resultado.replace(RE_CONTAR, (_m, emoji, cantidad) => htmlContar(emoji, cantidad));
  resultado = resultado.replace(RE_FRACCION_VISUAL, (_m, n, d) => htmlFraccion(n, d));
  resultado = resultado.replace(RE_DIBUJO, (_m, emoji) => `<span class="dibujo" role="img" aria-label="dibujo">${emoji}</span>`);

  // Procesar emoji: ::emoji::🦋::descripcion:: -> HTML visual
  resultado = resultado.replace(RE_EMOJI, (match, emoji, descripcion) => {
    return `
      <div class="emoji-educativo-inline">
        <span class="emoji-educativo-inline__icono">${emoji}</span>
        <span class="emoji-educativo-inline__descripcion">${descripcion}</span>
      </div>
    `;
  });

  // Procesar recta numérica: [recta: 0-100: 50] -> SVG visual
  resultado = resultado.replace(RE_RECTA, (match, inicio, fin, valor) => {
    const inicioNum = parseInt(inicio);
    const finNum = parseInt(fin);
    const valorNum = parseInt(valor);
    const porcentaje = ((valorNum - inicioNum) / (finNum - inicioNum)) * 100;
    return `
      <div class="componente-matematico componente-recta">
        <svg viewBox="0 0 300 60" class="recta-svg">
          <line x1="20" y1="30" x2="280" y2="30" stroke="#5B4FE9" stroke-width="3" />
          <circle cx="20" cy="30" r="5" fill="#5B4FE9" />
          <circle cx="280" cy="30" r="5" fill="#5B4FE9" />
          <circle cx="${20 + porcentaje * 2.6}" cy="30" r="8" fill="#FF6B4A" />
          <text x="20" y="50" text-anchor="middle" font-size="12" fill="#6B7280">${inicio}</text>
          <text x="280" y="50" text-anchor="middle" font-size="12" fill="#6B7280">${fin}</text>
          <text x="${20 + porcentaje * 2.6}" y="15" text-anchor="middle" font-size="14" font-weight="bold" fill="#FF6B4A">${valor}</text>
        </svg>
      </div>
    `;
  });

  // Procesar modelo de fracciones: [fraccion: 1/4] -> SVG visual
  resultado = resultado.replace(RE_FRACCION, (match, numerador, denominador) => {
    const num = parseInt(numerador);
    const den = parseInt(denominador);
    const angulo = (num / den) * 360;
    return `
      <div class="componente-matematico componente-fraccion">
        <svg viewBox="0 0 100 100" class="fraccion-svg">
          <circle cx="50" cy="50" r="45" fill="none" stroke="#E5E7EB" stroke-width="2" />
          <circle cx="50" cy="50" r="45" fill="none" stroke="#5B4FE9" stroke-width="2"
                  stroke-dasharray="${angulo * 0.785} 282.6"
                  transform="rotate(-90 50 50)" />
          <text x="50" y="55" text-anchor="middle" font-size="20" font-weight="bold" fill="#1F2937">${num}/${den}</text>
        </svg>
      </div>
    `;
  });

  return resultado;
}

/** Contenido de estudio (guías) se escribe en Markdown — ver `contenido/`. Confiable (propio
 * del equipo, no generado por usuarios), por eso se marca como HTML seguro directamente. */
@Pipe({ name: 'markdown', standalone: true })
export class MarkdownPipe implements PipeTransform {
  private sanitizer = inject(DomSanitizer);

  transform(texto: string | null | undefined): SafeHtml {
    if (!texto) return '';
    const conMatematica = renderizarMatematica(texto);
    const html = marked.parse(conMatematica, { async: false }) as string;
    return this.sanitizer.bypassSecurityTrustHtml(realzarGuia(html));
  }
}
