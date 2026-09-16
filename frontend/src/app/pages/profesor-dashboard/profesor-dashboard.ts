import { Component, inject, signal } from '@angular/core';
import { RouterLink } from '@angular/router';
import { FormsModule } from '@angular/forms';
import { ContenidoService, NivelRespuesta } from '../../core/contenido.service';
import { CursoSeccion, CursoSeccionService } from '../../core/curso-seccion.service';
import { ProfesorAuthService } from '../../core/profesor-auth.service';

@Component({
  selector: 'app-profesor-dashboard',
  standalone: true,
  imports: [RouterLink, FormsModule],
  template: `
    <h1>Mis Cursos</h1>

    @if (cargando()) {
      <p>Cargando…</p>
    } @else if (estado() !== 'aprobado') {
      <div class="tarjeta aviso-pendiente">
        <h3>Tu cuenta está {{ estado() === 'rechazado' ? 'rechazada' : 'en revisión' }}</h3>
        <p>
          @if (estado() === 'rechazado') {
            Un administrador revisó tu solicitud y no fue aprobada. Si crees que es un error, contáctanos.
          } @else {
            Un administrador tiene que aprobar tu cuenta antes de que puedas crear cursos. Vuelve a entrar más tarde.
          }
        </p>
      </div>
    } @else {
      <div class="lista-cursos">
        @for (c of cursos(); track c.id) {
          <a class="tarjeta curso-card" [routerLink]="['/profesor/cursos', c.id]">
            <h3>{{ c.nombre }}</h3>
          </a>
        }
        @if (!cursos().length) {
          <p class="vacio">Todavía no has creado ningún curso.</p>
        }
      </div>

      <h2>Crear curso</h2>
      <form class="tarjeta form-crear" (submit)="$event.preventDefault(); crear()">
        <div class="campo">
          <label for="nombreCurso">Nombre del curso</label>
          <input id="nombreCurso" [(ngModel)]="nombreCurso" name="nombreCurso" placeholder="6° básico A" />
        </div>
        <div class="campo">
          <label for="nivelId">Nivel</label>
          <select id="nivelId" [(ngModel)]="nivelId" name="nivelId">
            @for (n of niveles(); track n.id) {
              <option [value]="n.id">{{ n.nombre }}</option>
            }
          </select>
        </div>
        @if (error()) {
          <p class="error">{{ error() }}</p>
        }
        <button type="submit" class="btn btn--primario">Crear curso</button>
      </form>
    }
  `,
  styles: [
    `
      .aviso-pendiente {
        max-width: 480px;
      }
      .aviso-pendiente h3 {
        margin: 0 0 0.5rem;
      }
      .aviso-pendiente p {
        margin: 0;
        color: var(--texto-secundario);
      }
      .lista-cursos {
        display: grid;
        grid-template-columns: repeat(auto-fill, minmax(220px, 1fr));
        gap: 1rem;
        margin-bottom: 2.5rem;
      }
      .curso-card {
        text-decoration: none;
        color: inherit;
      }
      .curso-card h3 {
        margin: 0;
      }
      .vacio {
        color: var(--texto-secundario);
      }
      h2 {
        font-size: 1.05rem;
        margin-bottom: 0.75rem;
      }
      .form-crear {
        max-width: 420px;
      }
      .error {
        color: var(--color-error-texto);
        font-size: 0.85rem;
      }
    `,
  ],
})
export class ProfesorDashboard {
  cargando = signal(true);
  estado = signal<'pendiente' | 'aprobado' | 'rechazado'>('pendiente');
  cursos = signal<CursoSeccion[]>([]);
  niveles = signal<NivelRespuesta[]>([]);
  nombreCurso = '';
  nivelId: number | null = null;
  error = signal('');

  private profesorAuth = inject(ProfesorAuthService);
  private cursoSeccion = inject(CursoSeccionService);
  private contenido = inject(ContenidoService);

  constructor() {
    this.profesorAuth.yo().subscribe((cuenta) => {
      this.estado.set(cuenta.estado);
      this.cargando.set(false);
      if (cuenta.estado === 'aprobado') this.cargar();
    });
    this.contenido.listarNiveles().subscribe((niveles) => {
      this.niveles.set(niveles);
      if (niveles.length) this.nivelId = niveles[0].id;
    });
  }

  private cargar() {
    this.cursoSeccion.listarMisCursos().subscribe((cursos) => this.cursos.set(cursos));
  }

  crear() {
    this.error.set('');
    if (!this.nivelId) return;
    this.cursoSeccion.crearCurso(this.nivelId, this.nombreCurso).subscribe({
      next: () => {
        this.nombreCurso = '';
        this.cargar();
      },
      error: () => this.error.set('No se pudo crear el curso.'),
    });
  }
}
