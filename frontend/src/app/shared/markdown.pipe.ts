import { Pipe, PipeTransform, inject } from '@angular/core';
import { DomSanitizer, SafeHtml } from '@angular/platform-browser';
import { marked } from 'marked';

/** Contenido de estudio (guías) se escribe en Markdown — ver `contenido/`. Confiable (propio
 * del equipo, no generado por usuarios), por eso se marca como HTML seguro directamente. */
@Pipe({ name: 'markdown', standalone: true })
export class MarkdownPipe implements PipeTransform {
  private sanitizer = inject(DomSanitizer);

  transform(texto: string | null | undefined): SafeHtml {
    if (!texto) return '';
    const html = marked.parse(texto, { async: false }) as string;
    return this.sanitizer.bypassSecurityTrustHtml(html);
  }
}
