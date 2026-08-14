import { Component, inject, signal } from '@angular/core';
import { RouterLink } from '@angular/router';
import { ContenidoService, AsignaturaRespuesta } from '../../core/contenido.service';
import { CursoSeccionService, MiCurso } from '../../core/curso-seccion.service';
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

    @if (miCurso(); as curso) {
      <div class="tarjeta mi-curso">
        <span class="mi-curso__etiqueta">Mi Curso</span>
        <h3>{{ curso.nombre_curso }}</h3>
        <p>Profesor: {{ curso.nombre_profesor }}</p>
        @if (curso.comunicados.length) {
          <div class="mi-curso__comunicados">
            @for (c of curso.comunicados.slice(0, 3); track c.id) {
              <div class="comunicado">
                <strong>{{ c.titulo }}</strong>
                <p>{{ c.cuerpo }}</p>
              </div>
            }
          </div>
        }
      </div>
    }

    <h2 class="seccion-titulo">Tus asignaturas</h2>
    @if (error()) {
      <p class="error-carga">{{ error() }}</p>
    }
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
      .mi-curso {
        margin-bottom: 2rem;
        max-width: 480px;
      }
      .mi-curso__etiqueta {
        font-size: 0.7rem;
        font-weight: 700;
        text-transform: uppercase;
        color: var(--color-primario);
      }
      .mi-curso h3 {
        margin: 0.3rem 0 0.15rem;
      }
      .mi-curso p {
        margin: 0;
        color: var(--texto-secundario);
        font-size: 0.85rem;
      }
      .mi-curso__comunicados {
        margin-top: 0.75rem;
        display: flex;
        flex-direction: column;
        gap: 0.5rem;
      }
      .comunicado {
        border-top: 1px solid var(--borde);
        padding-top: 0.5rem;
      }
      .comunicado strong {
        font-size: 0.85rem;
      }
      .comunicado p {
        margin: 0.15rem 0 0;
        font-size: 0.8rem;
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
export class AlumnoInicio {
  asignaturas = signal<AsignaturaRespuesta[]>([]);
  miCurso = signal<MiCurso | null>(null);
  error = signal('');
  private colores = ['#5B4FE9', '#FF6B4A', '#22C55E', '#F59E0B', '#8B5CF6'];

  private contenido = inject(ContenidoService);
  private cursoSeccion = inject(CursoSeccionService);
  private sesion = inject(SesionService);

  constructor() {
    const perfil = this.sesion.perfilActivo();
    if (perfil) {
      this.contenido.listarAsignaturas(perfil.nivel_id).subscribe({
        next: (asigs) => this.asignaturas.set(asigs),
        error: () => this.error.set('No se pudieron cargar tus asignaturas. Intenta recargar la página.'),
      });
      // Autoestudio puro (sin curso asignado) es el caso normal — el backend devuelve
      // null y esta sección simplemente no se muestra. Si la llamada falla, se trata
      // igual que "sin curso" (sección secundaria, no bloquea la página del alumno).
      this.cursoSeccion.obtenerMiCurso(perfil.id).subscribe({
        next: (curso) => this.miCurso.set(curso),
        error: () => this.miCurso.set(null),
      });
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
