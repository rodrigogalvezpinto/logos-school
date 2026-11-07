/**
 * Convierte el contenido (Markdown con marcadores visuales) en texto para leer en voz alta.
 *
 * Hallazgo 2026-11-07: el botón «Escuchar» leía el texto crudo. La voz decía los asteriscos, los
 * nombres de los emojis y los marcadores: «::posicion::🐱::debajo::mesa::» se oía como «gato
 * debajo mesa», es decir, la respuesta, y «::contar::⭐::6::» decía el número que el niño debía
 * contar. Aquí los dibujos no se leen: el niño los mira. Solo se lee lo que la pantalla escribe.
 */
const MARCADORES_SOLO_DIBUJO = [
  /::posicion::[^:\s]+::[a-z-]+::[^:\s]+::/g,
  /::fila::(?:[^:\s]+::){2,6}/g,
  /::regla::\d{1,2}::\d{1,2}::/g,
  /::largo::[A-Z]::\d{1,2}::[A-Z]::\d{1,2}::/g,
  /::contar::[^:]+::\d{1,2}::/g,
  /::dibujo::[^:]+::/g,
  /::fraccion::\d{1,2}::\d{1,2}::/g,
  /\[recta:[^\]]*\]/g,
];
const RE_BALANZA_VOZ = /::balanza::([\d+ ]{1,12})::([\d+ ]{1,12})::/g;
const RE_EMOJI_DESCRITO = /::emoji::[^:\s]+::([\s\S]+?)::/g;
const RE_IMAGEN = /\[Imagen:\s*([^\]]+)\]/g;
const RE_FRACCION = /\[fraccion:\s*(\d+)\/(\d+)\]/g;
const RE_PICTOGRAMA = /[\p{Extended_Pictographic}\u{1F1E6}-\u{1F1FF}\u{1F3FB}-\u{1F3FF}\uFE0F\u200D\u20E3]/gu;

export function textoParaVoz(texto: string): string {
  let t = texto ?? '';
  // La balanza lleva escritas sus expresiones: se leen, pero no si está inclinada.
  t = t.replace(RE_BALANZA_VOZ, (_m, i: string, d: string) => ` balanza con ${i.trim()} en un platillo y ${d.trim()} en el otro. `);
  for (const re of MARCADORES_SOLO_DIBUJO) t = t.replace(re, ' ');
  t = t
    .replace(/_{3,}/g, ' … ') // espacio para completar
    // Marcas de conteo («manzana \|\|\|»): se miran y se cuentan; leerlas no sirve.
    .replace(/(?:\\\|\s*)+/g, ' ')
    // Fonemas «/s/»: se lee el sonido, no las barras.
    .replace(/(^|[\s(«"'])\/([a-zñáéíóúü]{1,3})\/(?=[\s.,;:)»"'?!]|$)/gi, '$1$2')
    .replace(RE_EMOJI_DESCRITO, '$1. ')
    .replace(RE_IMAGEN, '$1. ')
    .replace(RE_FRACCION, '$1 de $2 partes')
    .replace(/<\/?[a-z][^>]*>/gi, ' ')
    .replace(/([\d…])\s*<\s*(?=[\d…])/g, '$1 menor que ')
    .replace(/([\d…])\s*>\s*(?=[\d…])/g, '$1 mayor que ')
    .replace(/!?\[([^\]]+)\]\([^)]*\)/g, '$1')
    .replace(/^\s*\|?\s*:?-{3,}.*$/gm, ' ') // separadores de tabla y líneas horizontales
    .replace(/\|/g, ', ')
    // Títulos y líneas solo en negrita: pausa al final (si no terminan ya en puntuación).
    .replace(/^\s{0,3}#{1,6}\s+(.*?)\s*$/gm, (_m, t: string) => (/[.!?:…]$/.test(t) ? t : t + '.'))
    .replace(/^\s*\*\*([^*\n]+)\*\*\s*$/gm, (_m, t: string) => (/[.!?:…]$/.test(t) ? t : t + '.'))
    .replace(/(^|\s)#{1,6}\s/g, '$1')
    .replace(/^\s*>\s?/gm, '')
    // Cita dentro de una línea («responde. > Pepa vive…»), pero no «9 > 4».
    .replace(/(^|[^\d\s)])(\s*)>(?=\s|$)/g, '$1$2')
    .replace(/(^|[^\d\s)])(\s*)>(?=\s|$)/g, '$1$2')
    .replace(/\[([^\]]+)\](?!\()/g, '$1')
    .replace(/^\s*[-*+]\s+/gm, '')
    .replace(/(\*\*|__|\*|`)/g, '')
    .replace(/(^|\s)_([^_\n]+)_(?=\s|[.,;:!?]|$)/g, '$1$2')
    .replace(/[→⇒➜]/g, ', ')
    .replace(RE_PICTOGRAMA, ' ');
  t = leerSimbolosMatematicos(t);
  return t
    .replace(/\(\s*[<>=]\s*\)/g, '') // «mayor que (>)»: ya está dicho con palabras
    .replace(/[ \t]+/g, ' ')
    .replace(/\s*\n\s*\n\s*/g, '. ')
    .replace(/\s*\n\s*/g, ' ')
    .replace(/\s+([.,;:!?])/g, '$1')
    .replace(/([.!?…:;,])(?:\s*[.,;:])+(?!\.)/g, '$1') // «?.», «. .»: queda la primera
    .replace(/^[.,;:]\s*/, '')
    .replace(/([.!?:])(?=[A-Za-zÁÉÍÓÚÑ¿¡"«])/g, '$1 ')
    .replace(/\s{2,}/g, ' ')
    .trim();
}

// Alternativas que son solo un símbolo de comparación.
const SIMBOLOS: Record<string, string> = { '<': 'menor que', '>': 'mayor que', '=': 'igual a' };

const ORDINALES = ['', 'primero', 'segundo', 'tercero', 'cuarto', 'quinto', 'sexto', 'séptimo', 'octavo'];

/** Símbolos que una voz sintética lee mal o no lee: se dicen con palabras. */
function leerSimbolosMatematicos(t: string): string {
  return t
    .replace(/\$\s?(\d(?:[\d.]*\d)?)/g, '$1 pesos')
    .replace(/(\d)\s*°\s*C\b/g, '$1 grados Celsius')
    .replace(/\b([1-8])\s*°\s*(?=(básico|medio|año|ciclo)\b)/gi, (_m, n: string) => ORDINALES[+n] + ' ')
    .replace(/(\d)\s*°/g, '$1 grados')
    .replace(/(\d|\))\s*[×x·]\s*(?=[\d(])/g, '$1 por ')
    .replace(/(\d|\))\s*÷\s*(?=\d)/g, '$1 dividido en ')
    .replace(/(\d|\))\s*\+\s*(?=[\d(])/g, '$1 más ')
    .replace(/(\d|\))\s*−\s*(?=[\d(])/g, '$1 menos ')
    // Guion como resta solo entre números cortos («9 - 4»), no en años o rangos («2018-2019»).
    .replace(/(^|[^\d])(\d{1,3})\s*-\s*(?=\d{1,3}(?!\d))/g, '$1$2 menos ')
    .replace(/(\d|\)|…)\s*=\s*(?=[\d(…])/g, '$1 es igual a ');
}

export interface PreguntaParaVoz {
  tipo?: string;
  enunciado: string;
  opciones?: string[] | null;
}

/** Enunciado y alternativas, en el orden en que se ven. Una alternativa que es solo un dibujo
 * se anuncia como «el dibujo» (sin decir qué muestra). */
export function textoPreguntaParaVoz(p: PreguntaParaVoz): string {
  const partes = [textoParaVoz(p.enunciado)];
  if (p.tipo === 'verdadero_falso') {
    if (!/verdadero o falso/i.test(partes[0])) partes.push('¿Verdadero o falso?');
  } else if (p.opciones?.length) {
    if (p.tipo === 'varias_correctas' && !/marca todas/i.test(partes[0])) partes.push('Marca todas las correctas.');
    const letras = 'abcdefgh';
    partes.push(
      ...p.opciones.map((op, i) => {
        const dicho = SIMBOLOS[op.trim()] ?? (textoParaVoz(op) || `el dibujo número ${i + 1}`);
        return `${letras[i] ?? i + 1}: ${dicho.replace(/[.;]+$/, '')}.`;
      }),
    );
  }
  return partes
    .filter(Boolean)
    .map((s) => (/[.!?…]$/.test(s) ? s : s + '.'))
    .join(' ');
}
