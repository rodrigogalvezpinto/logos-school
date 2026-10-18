import { Component, inject, signal } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { AlumnoEncontrado, ComercialService, Plan } from '../../core/comercial.service';

@Component({
  selector: 'app-admin-cortesias',
  standalone: true,
  imports: [FormsModule],
  template: `
    <h1>Cortesías</h1>
    <p class="subtitulo">Dale a una familia acceso completo gratuito, sin pasar por el flujo de pago.</p>

    <form class="tarjeta buscador" (submit)="$event.preventDefault(); buscar()">
      <input [(ngModel)]="consulta" name="consulta" placeholder="Busca por nombre, apellido o RUT del alumno…" />
      <button type="submit" class="btn btn--primario">Buscar</button>
    </form>

    @if (resultados().length) {
      <div class="tarjeta tabla-envoltorio">
        <table>
          <thead>
            <tr><th>Alumno</th><th>RUT</th><th>Apoderado</th><th>Asignar plan</th><th></th></tr>
          </thead>
          <tbody>
            @for (a of resultados(); track a.perfil_alumno_id) {
              <tr>
                <td>{{ a.nombre }} {{ a.apellidos }}</td>
                <td>{{ a.rut }}</td>
                <td>{{ a.email_apoderado }}</td>
                <td>
                  <select [(ngModel)]="planSeleccionado[a.perfil_alumno_id]" [name]="'plan' + a.perfil_alumno_id">
                    @for (p of planes(); track p.id) {
                      <option [value]="p.id">{{ p.nombre }}</option>
                    }
                  </select>
                </td>
                <td>
                  <button class="btn btn--secundario btn--chico" (click)="asignar(a)">Asignar cortesía</button>
                </td>
              </tr>
            }
          </tbody>
        </table>
      </div>
    } @else if (buscado()) {
      <p class="vacio">No se encontró ningún alumno con esa búsqueda.</p>
    }

    @if (mensaje()) {
      <p class="mensaje">{{ mensaje() }}</p>
    }
    @if (error()) {
      <p class="error-carga">{{ error() }}</p>
    }
  `,
  styles: [
    `
      .subtitulo {
        color: var(--texto-secundario);
        margin-top: -0.5rem;
        margin-bottom: 2rem;
      }
      .buscador {
        display: flex;
        gap: 0.75rem;
        max-width: 560px;
        margin-bottom: 1.5rem;
      }
      .buscador input {
        flex: 1;
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
      .btn--chico {
        padding: 0.4rem 0.75rem;
        font-size: 0.8rem;
      }
      .vacio {
        color: var(--texto-secundario);
      }
      .mensaje {
        margin-top: 1rem;
        color: var(--color-exito-texto);
        font-weight: 600;
      }
      .error-carga {
        margin-top: 1rem;
        color: var(--color-error-texto);
      }
    `,
  ],
})
export class AdminCortesias {
  consulta = '';
  resultados = signal<AlumnoEncontrado[]>([]);
  planes = signal<Plan[]>([]);
  planSeleccionado: Record<number, number> = {};
  buscado = signal(false);
  mensaje = signal('');
  error = signal('');

  private comercial = inject(ComercialService);

  constructor() {
    this.comercial.listarPlanes().subscribe({
      next: (planes) => this.planes.set(planes.filter((p) => p.activo)),
      error: () => this.error.set('No se pudieron cargar los planes.'),
    });
  }

  buscar() {
    this.mensaje.set('');
    this.error.set('');
    this.comercial.buscarAlumnos(this.consulta).subscribe({
      next: (alumnos) => {
        this.resultados.set(alumnos);
        this.buscado.set(true);
        for (const a of alumnos) {
          if (!this.planSeleccionado[a.perfil_alumno_id] && this.planes().length) {
            this.planSeleccionado[a.perfil_alumno_id] = this.planes()[0].id;
          }
        }
      },
      error: () => this.error.set('No se pudo realizar la búsqueda. Intenta de nuevo.'),
    });
  }

  asignar(alumno: AlumnoEncontrado) {
    const planId = this.planSeleccionado[alumno.perfil_alumno_id];
    if (!planId) return;
    this.error.set('');
    this.comercial.asignarCortesia(alumno.perfil_alumno_id, planId).subscribe({
      next: () => this.mensaje.set(`Cortesía asignada a ${alumno.nombre} ${alumno.apellidos}.`),
      error: () => this.error.set('No se pudo asignar la cortesía. Intenta de nuevo.'),
    });
  }
}
