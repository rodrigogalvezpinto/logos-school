import { Component, Input, inject, signal } from '@angular/core';
import { Location } from '@angular/common';
import { RouterLink } from '@angular/router';
import { ContenidoService, ObjetivoRespuesta } from '../../core/contenido.service';
import { ProgresoService } from '../../core/progreso.service';
import { SesionService } from '../../core/sesion.service';
import { BotonEscuchar } from '../../shared/boton-escuchar/boton-escuchar';
import { MarkdownPipe } from '../../shared/markdown.pipe';

@Component({
  selector: 'app-estudiar-oa',
  standalone: true,
  imports: [RouterLink, BotonEscuchar, MarkdownPipe],
  template: `
    @if (objetivo(); as oa) {
      <a href="#" (click)="volver($event)" class="volver">← Volver</a>
      <span class="etiqueta">{{ oa.codigo_oficial }}</span>
      <h1>{{ oa.descripcion }}</h1>

      <app-boton-escuchar class="boton-guia" [texto]="oa.contenido_guia" />
      <div class="tarjeta bloque contenido-guia" [innerHTML]="oa.contenido_guia | markdown"></div>

      <a [routerLink]="['/alumno/autoevaluacion', oa.id]" class="btn btn--primario btn--grande">Practicar este tema</a>
    } @else if (error()) {
      <p class="error-carga">{{ error() }}</p>
    } @else {
      <p>Cargando…</p>
    }
  `,
  styles: [
    `
      .volver {
        display: inline-block;
        color: var(--texto-secundario);
        text-decoration: none;
        margin-bottom: 1.25rem;
        font-size: 0.9rem;
      }
      .etiqueta {
        font-size: 0.75rem;
        font-weight: 700;
        color: var(--color-primario);
        text-transform: uppercase;
      }
      h1 {
        margin: 0.4rem 0 1rem;
        font-size: 1.6rem;
      }
      .bloque {
        margin-bottom: 1.5rem;
        max-width: 680px;
      }
      .boton-guia {
        display: block;
        margin-bottom: 0.75rem;
      }
      .contenido-guia {
        line-height: 1.6;
        color: var(--texto-principal);
      }
      /* El contenido de la guía se inyecta vía [innerHTML] (Markdown ya renderizado) — no
         tiene el atributo de encapsulación de Angular, por eso estos selectores necesitan
         ::ng-deep para alcanzarlo desde los estilos del componente. */
      .contenido-guia ::ng-deep h1,
      .contenido-guia ::ng-deep h2,
      .contenido-guia ::ng-deep h3 {
        font-size: 1.1rem;
        margin: 1.25rem 0 0.5rem;
      }
      .contenido-guia ::ng-deep h1:first-child,
      .contenido-guia ::ng-deep h2:first-child,
      .contenido-guia ::ng-deep h3:first-child {
        margin-top: 0;
      }
      .contenido-guia ::ng-deep p {
        margin: 0 0 0.85rem;
      }
      .contenido-guia ::ng-deep ul,
      .contenido-guia ::ng-deep ol {
        margin: 0 0 0.85rem;
        padding-left: 1.4rem;
      }
      .contenido-guia ::ng-deep li {
        margin-bottom: 0.3rem;
      }
      .contenido-guia ::ng-deep strong {
        font-weight: 700;
      }
      .error-carga {
        color: var(--color-error);
      }
    `,
  ],
})
export class EstudiarOa {
  @Input() oaId = '';
  objetivo = signal<ObjetivoRespuesta | null>(null);
  error = signal('');

  private contenido = inject(ContenidoService);
  private progreso = inject(ProgresoService);
  private sesion = inject(SesionService);
  private location = inject(Location);

  ngOnInit() {
    this.contenido.obtenerObjetivo(Number(this.oaId)).subscribe({
      next: (oa) => this.objetivo.set(oa),
      error: () => this.error.set('No se pudo cargar la guía. Intenta recargar la página.'),
    });

    const perfil = this.sesion.perfilActivo();
    if (perfil) {
      // Fire-and-forget: no bloquea la lectura de la guía si falla o tarda.
      this.progreso.marcarGuiaRevisada(perfil.id, Number(this.oaId)).subscribe();
    }
  }

  volver(evento: Event) {
    evento.preventDefault();
    this.location.back();
  }
}
