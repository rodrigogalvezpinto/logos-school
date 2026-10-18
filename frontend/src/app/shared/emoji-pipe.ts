import { Pipe, PipeTransform } from '@angular/core';
import { DomSanitizer, SafeHtml } from '@angular/platform-browser';

@Pipe({
  name: 'emoji',
  standalone: true,
})
export class EmojiPipe implements PipeTransform {
  constructor(private sanitizer: DomSanitizer) {}

  transform(value: string): SafeHtml {
    if (!value) return this.sanitizer.bypassSecurityTrustHtml(value);

    // Patrón: ::emoji::🦋::una mariposa de colores volando::
    const patron = /::emoji::([^:]+)::([^:]+)::/g;

    const html = value.replace(patron, (match, emoji, descripcion) => {
      // Generar HTML con el emoji como un elemento visual
      return `
        <div class="emoji-educativo-inline">
          <span class="emoji-educativo-inline__icono">${emoji}</span>
          <span class="emoji-educativo-inline__descripcion">${descripcion}</span>
        </div>
      `;
    });

    return this.sanitizer.bypassSecurityTrustHtml(html);
  }
}
