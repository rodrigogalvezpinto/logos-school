import { Component, inject, signal } from '@angular/core';
import { AdminProfesoresService, CuentaProfesor } from '../../core/admin-profesores.service';

@Component({
  selector: 'app-admin-profesores',
  standalone: true,
  template: `
    <h1>Profesores</h1>
    <p class="subtitulo">Revisa y aprueba las cuentas de Profesor antes de que puedan crear cursos.</p>

    <div class="tarjeta tabla-envoltorio">
      <table>
        <thead>
          <tr><th>Nombre</th><th>Correo</th><th></th></tr>
        </thead>
        <tbody>
          @for (p of pendientes(); track p.id) {
            <tr>
              <td>{{ p.nombre }}</td>
              <td>{{ p.email }}</td>
              <td class="acciones">
                <button class="btn btn--primario btn--chico" (click)="aprobar(p)">Aprobar</button>
                <button class="btn btn--secundario btn--chico" (click)="rechazar(p)">Rechazar</button>
              </td>
            </tr>
          }
          @if (!pendientes().length) {
            <tr><td colspan="3" class="vacio">No hay cuentas de profesor pendientes de revisión.</td></tr>
          }
        </tbody>
      </table>
    </div>
  `,
  styles: [
    `
      .subtitulo {
        color: var(--texto-secundario);
        margin-top: -0.5rem;
        margin-bottom: 2rem;
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
      .acciones {
        display: flex;
        gap: 0.5rem;
      }
      .btn--chico {
        padding: 0.4rem 0.75rem;
        font-size: 0.8rem;
      }
      .vacio {
        color: var(--texto-secundario);
      }
    `,
  ],
})
export class AdminProfesores {
  pendientes = signal<CuentaProfesor[]>([]);

  private servicio = inject(AdminProfesoresService);

  constructor() {
    this.cargar();
  }

  private cargar() {
    this.servicio.listarPendientes().subscribe((p) => this.pendientes.set(p));
  }

  aprobar(p: CuentaProfesor) {
    this.servicio.aprobar(p.id).subscribe(() => this.cargar());
  }

  rechazar(p: CuentaProfesor) {
    this.servicio.rechazar(p.id).subscribe(() => this.cargar());
  }
}
