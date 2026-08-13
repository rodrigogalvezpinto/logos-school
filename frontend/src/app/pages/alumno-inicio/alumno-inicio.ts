import { Component, inject, signal } from '@angular/core';
import { RouterLink } from '@angular/router';
import { ContenidoService, AsignaturaRespuesta } from '../../core/contenido.service';
import { SesionService } from '../../core/sesion.service';
import { IconoAsignatura } from '../../shared/icono-asignatura/icono-asignatura';

const ICONOS_POR_NOMBRE: Record<string, string> = {
  'Lenguaje y Comunicación': 'libro',
  'Lengua y Literatura': 'libro',
  Matemática: 'regla',
  'Ciencias Naturales': 'hoja',
  Inglés: 'libro',
};

@Component({
  selector: 'app-alumno-inicio',
  standalone: true,
  imports: [RouterLink, IconoAsignatura],
  template: `
    <h1>¡Hola de nuevo, {{ nombreAlumno() }}! 👋</h1>
    <p class="subtitulo">Sigamos avanzando en tu preparación.</p>

    <h2 class="seccion-titulo">Tus asignaturas</h2>
    <div class="grid-asignaturas">
      @for (asig of asignaturas(); track asig.id) {
        <a class="asignatura-card tarjeta" [routerLink]="['/alumno/asignaturas', asig.id]">
          <app-icono-asignatura [icono]="iconoPara(asig.nombre)" [color]="colorPara(asig.id)" />
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
      .seccion-titulo {
        font-size: 1.2rem;
        margin-bottom: 1rem;
      }
      .grid-asignaturas {
        display: grid;
        grid-template-columns: repeat(2, 1fr);
        gap: 1rem;
      }
      .asignatura-card {
        display: flex;
        gap: 1rem;
        align-items: center;
        text-decoration: none;
        color: inherit;
        transition: transform 0.15s;
      }
      .asignatura-card:hover {
        transform: translateY(-2px);
      }
      .asignatura-card h3 {
        font-size: 1rem;
        margin: 0;
      }
    `,
  ],
})
export class AlumnoInicio {
  asignaturas = signal<AsignaturaRespuesta[]>([]);
  private colores = ['#5B4FE9', '#FF6B4A', '#22C55E', '#F59E0B', '#8B5CF6'];

  private contenido = inject(ContenidoService);
  private sesion = inject(SesionService);

  constructor() {
    const perfil = this.sesion.perfilActivo();
    if (perfil) {
      this.contenido.listarAsignaturas(perfil.nivel_id).subscribe((asigs) => this.asignaturas.set(asigs));
    }
  }

  nombreAlumno(): string {
    return this.sesion.perfilActivo()?.nombre || '';
  }

  iconoPara(nombre: string): string {
    return ICONOS_POR_NOMBRE[nombre] || 'libro';
  }

  colorPara(id: number): string {
    return this.colores[id % this.colores.length];
  }
}
