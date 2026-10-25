import { Pipe, PipeTransform } from '@angular/core';

@Pipe({
  name: 'emoji',
  standalone: true,
})
export class EmojiPipe implements PipeTransform {
  transform(value: string): string {
    if (!value) return value;

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

    return html;
  }
}
