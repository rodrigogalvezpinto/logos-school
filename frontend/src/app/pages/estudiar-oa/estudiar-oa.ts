import { Component, Input, inject, signal } from '@angular/core';
import { Location } from '@angular/common';
import { RouterLink } from '@angular/router';
import { ContenidoService, ObjetivoRespuesta } from '../../core/contenido.service';
import { ProgresoService } from '../../core/progreso.service';
import { SesionService } from '../../core/sesion.service';
import { BotonEscuchar } from '../../shared/boton-escuchar/boton-escuchar';

@Component({
  selector: 'app-estudiar-oa',
  standalone: true,
  imports: [RouterLink, BotonEscuchar],
  template: `
    @if (objetivo(); as oa) {
      <a href="#" (click)="volver($event)" class="volver">← Volver</a>
      <span class="etiqueta">{{ oa.codigo_oficial }}</span>
      <h1>{{ oa.descripcion }}</h1>

      <app-boton-escuchar class="boton-guia" [texto]="oa.contenido_guia" />
      <div class="tarjeta bloque contenido-guia" [innerText]="oa.contenido_guia"></div>

      <a [routerLink]="['/alumno/autoevaluacion', oa.id]" class="btn btn--primario btn--grande">Practicar este tema</a>
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
        white-space: pre-wrap;
        line-height: 1.6;
        color: var(--texto-principal);
      }
    `,
  ],
})
export class EstudiarOa {
  @Input() oaId = '';
  objetivo = signal<ObjetivoRespuesta | null>(null);

  private contenido = inject(ContenidoService);
  private progreso = inject(ProgresoService);
  private sesion = inject(SesionService);
  private location = inject(Location);

  ngOnInit() {
    this.contenido.obtenerObjetivo(Number(this.oaId)).subscribe((oa) => this.objetivo.set(oa));

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
