import { Component, inject, signal } from '@angular/core';
import { RouterLink } from '@angular/router';
import { AuthService, PerfilAlumnoRespuesta } from '../../core/auth.service';

@Component({
  selector: 'app-progreso-alumno',
  standalone: true,
  imports: [RouterLink],
  template: `
    <h1>Progreso por Alumno</h1>
    <p class="subtitulo">Elige un alumno para ver su historial y notas por materia.</p>

    <div class="grid">
      @for (alumno of alumnos(); track alumno.id) {
        <a class="tarjeta alumno-card" [routerLink]="['/apoderado/progreso', alumno.id]">
          <div class="alumno-card__avatar">{{ alumno.nombre.charAt(0) }}</div>
          <h3>{{ alumno.nombre }} {{ alumno.apellidos }}</h3>
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
      .grid {
        display: grid;
        grid-template-columns: repeat(2, 1fr);
        gap: 1rem;
        max-width: 760px;
      }
      @media (max-width: 700px) {
        .grid {
          grid-template-columns: 1fr;
        }
      }
      .alumno-card {
        display: flex;
        align-items: center;
        gap: 1rem;
        text-decoration: none;
        color: inherit;
      }
      .alumno-card__avatar {
        width: 52px;
        height: 52px;
        border-radius: var(--radio-media);
        background: var(--color-primario);
        color: white;
        display: flex;
        align-items: center;
        justify-content: center;
        font-family: var(--fuente-titulos);
        font-weight: 700;
        font-size: 1.3rem;
        flex-shrink: 0;
      }
      .alumno-card h3 {
        margin: 0;
      }
    `,
  ],
})
export class ProgresoAlumno {
  alumnos = signal<PerfilAlumnoRespuesta[]>([]);

  private auth = inject(AuthService);

  constructor() {
    this.auth.listarAlumnos().subscribe((alumnos) => this.alumnos.set(alumnos));
  }
}
