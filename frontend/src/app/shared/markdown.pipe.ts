import { Pipe, PipeTransform, inject } from '@angular/core';
import { DomSanitizer, SafeHtml } from '@angular/platform-browser';
import { marked } from 'marked';

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
const RE_EMOJI = /::emoji::([^:]+)::([^:]+)::/g;

function realzarGuia(html: string): string {
  let resultado = html
    .replace(
      RE_POR_QUE_IMPORTA,
      '<div class="callout callout--importa"><p class="callout__titulo">¿Por qué importa?</p><p>$1</p></div>',
    )
    .replace(RE_TITULO_EJEMPLOS, '<h$1 class="titulo-ejemplos">Ejemplos resueltos</h$1>')
    .replace(RE_EJEMPLO, '<p class="ejemplo-titulo"><span class="ejemplo-num">$1</span>$2</p>')
    .replace(RE_IMAGEN, '<span class="marcador-imagen">🖼️ $1</span>');

  // Procesar emoji: ::emoji::🦋::descripcion:: -> HTML visual
  resultado = resultado.replace(RE_EMOJI, (match, emoji, descripcion) => {
    return `
      <div class="emoji-educativo-inline">
        <span class="emoji-educativo-inline__icono">${emoji}</span>
        <span class="emoji-educativo-inline__descripcion">${descripcion}</span>
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
    const html = marked.parse(texto, { async: false }) as string;
    return this.sanitizer.bypassSecurityTrustHtml(realzarGuia(html));
  }
}
