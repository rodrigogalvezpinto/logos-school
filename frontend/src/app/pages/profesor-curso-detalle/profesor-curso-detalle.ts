import { Component, Input, inject, signal } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { AlumnoEncontrado, CursoSeccionService, ProgresoDeCurso } from '../../core/curso-seccion.service';

@Component({
  selector: 'app-profesor-curso-detalle',
  standalone: true,
  imports: [FormsModule],
  template: `
    @if (progreso(); as p) {
      <h1>{{ p.curso.nombre }}</h1>

      <h2>Alumnos y progreso</h2>
      <div class="tarjeta tabla-envoltorio tabla-roster">
        <table>
          <thead>
            <tr><th>Alumno</th><th>Notas por asignatura</th><th></th></tr>
          </thead>
          <tbody>
            @for (a of p.alumnos; track a.perfil_alumno_id) {
              <tr>
                <td>{{ a.nombre }} {{ a.apellidos }}</td>
                <td>
                  @for (n of a.notas_por_asignatura; track n.asignatura_id) {
                    <div class="nota-linea">
                      {{ n.asignatura_nombre }}:
                      <strong>{{ n.nota_practica ?? '—' }}</strong>
                      @if (n.nota_simulacro !== null) {
                        <span class="chip chip--simulacro">Simulacro {{ n.nota_simulacro }}</span>
                      }
                    </div>
                  }
                  @if (!a.notas_por_asignatura.length) {
                    <span class="vacio">Sin evaluaciones rendidas todavía.</span>
                  }
                </td>
                <td>
                  <button class="btn btn--secundario btn--chico" (click)="quitar(a.perfil_alumno_id)">Quitar</button>
                </td>
              </tr>
            }
            @if (!p.alumnos.length) {
              <tr><td colspan="3" class="vacio">Todavía no hay alumnos en este curso.</td></tr>
            }
          </tbody>
        </table>
      </div>

      <h2>Agregar alumno</h2>
      <form class="tarjeta buscador" (submit)="$event.preventDefault(); buscar()">
        <input [(ngModel)]="consulta" name="consulta" placeholder="Busca por nombre, apellido o RUT…" aria-label="Buscar alumno por nombre, apellido o RUT" />
        <button type="submit" class="btn btn--primario">Buscar</button>
      </form>
      @if (errorAgregar()) {
        <p class="aviso-error">{{ errorAgregar() }}</p>
      }
      @if (resultados().length) {
        <div class="tarjeta tabla-envoltorio tabla-resultados-busqueda">
          <table>
            <thead><tr><th>Alumno</th><th>RUT</th><th></th></tr></thead>
            <tbody>
              @for (r of resultados(); track r.perfil_alumno_id) {
                <tr>
                  <td>{{ r.nombre }} {{ r.apellidos }}</td>
                  <td>{{ r.rut }}</td>
                  <td><button class="btn btn--secundario btn--chico" (click)="agregar(r.perfil_alumno_id)">Agregar</button></td>
                </tr>
              }
            </tbody>
          </table>
        </div>
      }

      <h2>Comunicados</h2>
      <form class="tarjeta form-comunicado" (submit)="$event.preventDefault(); publicar()">
        <div class="campo">
          <label for="tituloComunicado">Título</label>
          <input id="tituloComunicado" [(ngModel)]="tituloComunicado" name="tituloComunicado" placeholder="Bienvenida al curso" />
        </div>
        <div class="campo">
          <label for="cuerpoComunicado">Mensaje</label>
          <textarea id="cuerpoComunicado" [(ngModel)]="cuerpoComunicado" name="cuerpoComunicado" rows="3" placeholder="Escribe el comunicado…"></textarea>
        </div>
        <button type="submit" class="btn btn--primario">Publicar comunicado</button>
      </form>
    } @else {
      <p>Cargando…</p>
    }
  `,
  styles: [
    `
      h2 {
        font-size: 1.05rem;
        margin: 2rem 0 0.75rem;
      }
      .tabla-envoltorio {
        padding: 0;
        overflow-x: auto;
      }
      table {
        width: 100%;
        border-collapse: collapse;
      }
      th, td {
        text-align: left;
        padding: 0.85rem 1.25rem;
        font-size: 0.9rem;
      }
      thead th {
        color: var(--texto-secundario);
        font-weight: 600;
        font-size: 0.75rem;
        text-transform: uppercase;
        border-bottom: 1px solid var(--borde);
      }
      tbody tr:not(:last-child) td {
        border-bottom: 1px solid var(--borde);
      }
      .nota-linea {
        font-size: 0.85rem;
        margin-bottom: 0.2rem;
      }
      .chip {
        display: inline-block;
        font-size: 0.7rem;
        font-weight: 600;
        padding: 0.1rem 0.5rem;
        border-radius: 999px;
        margin-left: 0.4rem;
      }
      .chip--simulacro {
        background: var(--color-secundario-suave);
        color: var(--color-secundario-texto);
      }
      .vacio {
        color: var(--texto-secundario);
      }
      .btn--chico {
        padding: 0.4rem 0.75rem;
        font-size: 0.8rem;
      }
      .buscador {
        display: flex;
        gap: 0.75rem;
        max-width: 560px;
        margin-bottom: 1rem;
      }
      .buscador input {
        flex: 1;
      }
      .form-comunicado {
        max-width: 480px;
      }
      .aviso-error {
        color: var(--color-error, #d64545);
        font-size: 0.85rem;
        max-width: 560px;
      }
      textarea {
        width: 100%;
        font-family: inherit;
      }
    `,
  ],
})
export class ProfesorCursoDetalle {
  @Input() id = '';
  progreso = signal<ProgresoDeCurso | null>(null);
  resultados = signal<AlumnoEncontrado[]>([]);
  errorAgregar = signal('');
  consulta = '';
  tituloComunicado = '';
  cuerpoComunicado = '';

  private cursoSeccion = inject(CursoSeccionService);

  ngOnInit() {
    this.cargar();
  }

  private cargar() {
    this.cursoSeccion.obtenerProgreso(Number(this.id)).subscribe((p) => this.progreso.set(p));
  }

  buscar() {
    this.cursoSeccion.buscarAlumnos(this.consulta).subscribe((r) => this.resultados.set(r));
  }

  agregar(perfilAlumnoId: number) {
    this.errorAgregar.set('');
    this.cursoSeccion.agregarAlumno(Number(this.id), perfilAlumnoId).subscribe({
      next: () => {
        this.resultados.set([]);
        this.consulta = '';
        this.cargar();
      },
      error: (err) => {
        this.errorAgregar.set(
          err.status === 400
            ? 'Ese alumno cursa un nivel distinto al de este Curso/Sección — no se puede agregar.'
            : 'No se pudo agregar al alumno.',
        );
      },
    });
  }

  quitar(perfilAlumnoId: number) {
    this.cursoSeccion.quitarAlumno(Number(this.id), perfilAlumnoId).subscribe(() => this.cargar());
  }

  publicar() {
    this.cursoSeccion.publicarComunicado(Number(this.id), this.tituloComunicado, this.cuerpoComunicado).subscribe(() => {
      this.tituloComunicado = '';
      this.cuerpoComunicado = '';
    });
  }
}
