import { Component, inject, signal } from '@angular/core';
import { RouterLink } from '@angular/router';
import { ContenidoService, AsignaturaRespuesta } from '../../core/contenido.service';
import { SesionService } from '../../core/sesion.service';
import { estiloAsignatura } from '../../shared/estilo-asignatura';
import { IconoAsignatura } from '../../shared/icono-asignatura/icono-asignatura';

@Component({
  selector: 'app-asignaturas-lista',
  standalone: true,
  imports: [RouterLink, IconoAsignatura],
  template: `
    <h1>Mis Asignaturas</h1>
    <p class="subtitulo">El temario oficial completo, organizado por Objetivo de Aprendizaje. Pincha una asignatura para ver su ruta de aprendizaje 👇</p>

    @if (error()) {
      <p class="error-carga">{{ error() }}</p>
    }
    <div class="grid-asignaturas">
      @for (asig of asignaturas(); track asig.id) {
        <a class="asignatura-card" [routerLink]="['/alumno/asignaturas', asig.id]" [style.--color-asig]="colorDe(asig.nombre)">
          <div class="asignatura-card__banner">
            <app-icono-asignatura [icono]="iconoDe(asig.nombre)" color="#ffffff" />
          </div>
          <div class="asignatura-card__info">
            <h3>{{ asig.nombre }}</h3>
            <span class="asignatura-card__cta">Ver ruta de aprendizaje →</span>
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
        grid-template-columns: repeat(auto-fill, minmax(220px, 1fr));
        gap: 1.25rem;
      }
      .asignatura-card {
        display: block;
        text-decoration: none;
        color: inherit;
        border-radius: var(--radio-basica);
        overflow: hidden;
        background: var(--fondo-tarjeta, #fff);
        box-shadow: var(--sombra-tarjeta);
        transition: transform 0.15s, box-shadow 0.15s;
      }
      .asignatura-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 20px rgba(31, 41, 55, 0.12);
      }
      .asignatura-card__banner {
        background: var(--color-asig);
        padding: 1.75rem 1.25rem;
        display: flex;
      }
      .asignatura-card__banner app-icono-asignatura ::ng-deep .icono {
        background: rgba(255, 255, 255, 0.22);
        width: 46px;
        height: 46px;
        font-size: 1.4rem;
      }
      .asignatura-card__info {
        padding: 1rem 1.25rem 1.25rem;
      }
      .asignatura-card__info h3 {
        margin: 0 0 0.35rem;
        font-size: 1.05rem;
      }
      .asignatura-card__cta {
        font-size: 0.8rem;
        font-weight: 700;
        color: var(--color-asig);
      }
      @media (max-width: 700px) {
        .grid-asignaturas {
          grid-template-columns: repeat(auto-fill, minmax(150px, 1fr));
        }
      }
      .error-carga {
        color: var(--color-error-texto);
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

  iconoDe(nombre: string): string {
    return estiloAsignatura(nombre).icono;
  }

  colorDe(nombre: string): string {
    return estiloAsignatura(nombre).color;
  }
}
