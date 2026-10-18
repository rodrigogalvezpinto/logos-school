import { Component, Input, inject, signal } from '@angular/core';
import { Location } from '@angular/common';
import { RouterLink } from '@angular/router';
import { environment } from '../../../environments/environment';
import { CalificacionesService } from '../../core/calificaciones.service';
import { ContenidoService, ObjetivoRespuesta } from '../../core/contenido.service';
import { OnboardingService } from '../../core/onboarding.service';
import { ProgresoService } from '../../core/progreso.service';
import { SesionService } from '../../core/sesion.service';
import { BotonEscuchar } from '../../shared/boton-escuchar/boton-escuchar';
import { MarkdownPipe } from '../../shared/markdown.pipe';
import { EmojiPipe } from '../../shared/emoji-pipe';
import { PasosAprendizaje } from '../../shared/pasos-aprendizaje/pasos-aprendizaje';

@Component({
  selector: 'app-estudiar-oa',
  standalone: true,
  imports: [RouterLink, BotonEscuchar, MarkdownPipe, EmojiPipe, PasosAprendizaje],
  template: `
    @if (objetivo(); as oa) {
      <a href="#" (click)="volver($event)" class="volver">← Volver</a>
      <app-pasos-aprendizaje [paso]="1" />
      <span class="etiqueta">{{ oa.codigo_oficial }}</span>
      <h1>{{ oa.descripcion }}</h1>

      <div class="acciones-guia">
        <app-boton-escuchar class="boton-guia" [texto]="oa.contenido_guia" />
        <a [href]="urlPdf(oa.id)" target="_blank" rel="noopener" class="descargar-pdf">⬇ Descargar guía en PDF</a>
      </div>
      <div class="tarjeta bloque contenido-guia" [innerHTML]="oa.contenido_guia | emoji | markdown"></div>

      <div class="tarjeta bloque calificar-guia">
        <p class="calificar-guia__pregunta">¿Qué te pareció esta guía?</p>
        <div class="calificar-guia__estrellas">
          @for (n of [1, 2, 3, 4, 5]; track n) {
            <button
              type="button"
              class="calificar-guia__estrella"
              [class.calificar-guia__estrella--llena]="n <= (miCalificacion() ?? 0)"
              (click)="calificar(n)"
              [attr.aria-label]="n + ' estrella' + (n > 1 ? 's' : '')"
            >
              {{ n <= (miCalificacion() ?? 0) ? '★' : '☆' }}
            </button>
          }
        </div>
        @if (miCalificacion()) {
          <p class="calificar-guia__gracias">¡Gracias por tu opinión!</p>
        }
      </div>

      <a [routerLink]="['/alumno/autoevaluacion', oa.id]" class="btn btn--primario btn--grande">
        Ya entendí, quiero practicar →
      </a>
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
      .acciones-guia {
        display: flex;
        align-items: center;
        gap: 1.25rem;
        margin-bottom: 0.75rem;
      }
      .boton-guia {
        display: block;
      }
      .descargar-pdf {
        font-size: 0.85rem;
        color: var(--color-primario);
        text-decoration: none;
        font-weight: 600;
      }
      .descargar-pdf:hover {
        text-decoration: underline;
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
        color: var(--texto-principal);
      }
      .contenido-guia ::ng-deep h3 {
        color: var(--color-primario);
        border-bottom: 2px solid var(--color-primario-suave);
        padding-bottom: 0.4rem;
      }
      .contenido-guia ::ng-deep .callout--importa {
        background: var(--color-primario-suave);
        border-left: 4px solid var(--color-primario);
        border-radius: var(--radio-media);
        padding: 1rem 1.25rem;
        margin: 0 0 1.5rem;
      }
      .contenido-guia ::ng-deep .callout--importa p {
        margin: 0;
      }
      .contenido-guia ::ng-deep .callout__titulo {
        font-weight: 700;
        color: var(--color-primario-oscuro);
        margin-bottom: 0.35rem !important;
      }
      .contenido-guia ::ng-deep .callout__titulo::before {
        content: '💡 ';
      }
      .contenido-guia ::ng-deep .titulo-ejemplos::before {
        content: '📘 ';
      }
      .contenido-guia ::ng-deep .titulo-ejemplos {
        margin-top: 1.75rem;
      }
      .contenido-guia ::ng-deep .ejemplo-titulo {
        display: flex;
        align-items: center;
        gap: 0.6rem;
        font-weight: 700;
        margin: 1.5rem 0 0.6rem !important;
        padding-top: 1.25rem;
        border-top: 1px dashed var(--color-primario-suave);
      }
      .contenido-guia ::ng-deep .ejemplo-titulo:first-of-type {
        border-top: none;
        padding-top: 0;
        margin-top: 0.5rem !important;
      }
      .contenido-guia ::ng-deep .ejemplo-num {
        flex-shrink: 0;
        display: inline-flex;
        align-items: center;
        justify-content: center;
        width: 1.6rem;
        height: 1.6rem;
        border-radius: 50%;
        background: var(--color-secundario);
        color: #fff;
        font-size: 0.85rem;
        font-weight: 700;
      }
      .contenido-guia ::ng-deep ul li::marker,
      .contenido-guia ::ng-deep ol li::marker {
        color: var(--color-secundario-texto);
        font-weight: 700;
      }
      .contenido-guia ::ng-deep .marcador-imagen {
        display: block;
        background: var(--color-primario-suave);
        color: var(--color-primario-oscuro);
        border-radius: var(--radio-media);
        padding: 1.5rem 1rem;
        margin: 0 0 0.85rem;
        text-align: center;
        font-style: italic;
        font-size: 0.95rem;
      }
      .error-carga {
        color: var(--color-error-texto);
      }
      .calificar-guia {
        max-width: 680px;
        text-align: center;
      }
      .calificar-guia__pregunta {
        margin: 0 0 0.5rem;
        font-weight: 600;
        color: var(--texto-principal);
      }
      .calificar-guia__estrellas {
        display: flex;
        justify-content: center;
        gap: 0.3rem;
      }
      .calificar-guia__estrella {
        background: none;
        border: none;
        cursor: pointer;
        font-size: 1.8rem;
        line-height: 1;
        color: var(--borde);
        padding: 0.15rem;
      }
      .calificar-guia__estrella--llena {
        color: var(--color-secundario);
      }
      .calificar-guia__gracias {
        margin: 0.5rem 0 0;
        font-size: 0.85rem;
        color: var(--color-exito-texto);
      }
    `,
  ],
})
export class EstudiarOa {
  @Input() oaId = '';
  objetivo = signal<ObjetivoRespuesta | null>(null);
  error = signal('');
  /** Calificación con estrellas por guía — hallazgo comparando en vivo contra Brincus
   * (tab "Evaluar Sección" separado de "Reportar error", ver
   * planificacion/27-plan-incorporacion-hallazgos-brincus.md, cuarta pasada). */
  miCalificacion = signal<number | null>(null);

  private contenido = inject(ContenidoService);
  private progreso = inject(ProgresoService);
  private calificaciones = inject(CalificacionesService);
  private onboarding = inject(OnboardingService);
  private sesion = inject(SesionService);
  private location = inject(Location);

  ngOnInit() {
    this.contenido.obtenerObjetivo(Number(this.oaId)).subscribe({
      next: (oa) => {
        this.objetivo.set(oa);
        // Solo si la guía realmente cargó: un `oa_id` inexistente (guía rota, link viejo)
        // no debe marcarse como revisada — antes se llamaba sin condición y, con un OA que
        // no existe, el INSERT violaba la FK de `progreso_oa.oa_id` en Postgres (bug real
        // encontrado por Playwright: un 500 sin manejar que el navegador reporta como error
        // de CORS, silenciado porque el `.subscribe()` no tenía manejador de error).
        const perfil = this.sesion.perfilActivo();
        if (perfil) {
          this.progreso.marcarGuiaRevisada(perfil.id, Number(this.oaId)).subscribe();
          this.onboarding.completarPaso(perfil.id, 'ver_guia').subscribe();
          this.calificaciones.obtenerMiCalificacion(perfil.id, Number(this.oaId)).subscribe({
            next: (c) => this.miCalificacion.set(c?.estrellas ?? null),
            error: () => {},
          });
        }
      },
      error: () => this.error.set('No se pudo cargar la guía. Intenta recargar la página.'),
    });
  }

  volver(evento: Event) {
    evento.preventDefault();
    this.location.back();
  }

  urlPdf(oaId: number): string {
    return `${environment.apiUrl}/contenido/objetivos/${oaId}/guia.pdf`;
  }

  calificar(estrellas: number) {
    const perfil = this.sesion.perfilActivo();
    if (!perfil) return;
    this.miCalificacion.set(estrellas);
    this.calificaciones.calificar(perfil.id, Number(this.oaId), estrellas).subscribe();
  }
}
