import { Component, inject, signal } from '@angular/core';
import { RouterLink } from '@angular/router';
import { ContenidoService, AsignaturaRespuesta } from '../../core/contenido.service';
import { SesionService } from '../../core/sesion.service';
import { IconoAsignatura } from '../../shared/icono-asignatura/icono-asignatura';

@Component({
  selector: 'app-asignaturas-lista',
  standalone: true,
  imports: [RouterLink, IconoAsignatura],
  template: `
    <h1>Mis Asignaturas</h1>
    <p class="subtitulo">El temario oficial completo, organizado por Objetivo de Aprendizaje.</p>

    @if (error()) {
      <p class="error-carga">{{ error() }}</p>
    }
    <div class="grid-asignaturas">
      @for (asig of asignaturas(); track asig.id) {
        <a class="asignatura-card tarjeta" [routerLink]="['/alumno/asignaturas', asig.id]">
          <app-icono-asignatura icono="libro" color="#5B4FE9" />
          <div class="asignatura-card__info">
            <h3>{{ asig.nombre }}</h3>
          </div>
        </a>
      }
    </div>
  `,
  styles: [
    `
      .subtitulo {
        color: var(--texto-secundario);
        margin-top: -0.5rem;
        margin-bottom: 2rem;
      }
      .grid-asignaturas {
        display: grid;
        grid-template-columns: repeat(2, 1fr);
        gap: 1rem;
      }
      .asignatura-card {
        display: flex;
        gap: 1rem;
        text-decoration: none;
        color: inherit;
        transition: transform 0.15s;
      }
      .asignatura-card:hover {
        transform: translateY(-2px);
      }
      .asignatura-card h3 {
        margin: 0;
        font-size: 1.05rem;
      }
      @media (max-width: 700px) {
        .grid-asignaturas {
          grid-template-columns: 1fr;
        }
      }
      .error-carga {
        color: var(--color-error);
      }
    `,
  ],
})
export class AsignaturasLista {
  asignaturas = signal<AsignaturaRespuesta[]>([]);
  error = signal('');

  private contenido = inject(ContenidoService);
  private sesion = inject(SesionService);

  constructor() {
    const perfil = this.sesion.perfilActivo();
    if (perfil) {
      this.contenido.listarAsignaturas(perfil.nivel_id).subscribe({
        next: (asigs) => this.asignaturas.set(asigs),
        error: () => this.error.set('No se pudieron cargar tus asignaturas. Intenta recargar la página.'),
      });
    }
  }
}
