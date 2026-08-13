import { Component, inject, signal } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { ComercialService, Plan } from '../../core/comercial.service';

@Component({
  selector: 'app-admin-planes',
  standalone: true,
  imports: [FormsModule],
  template: `
    <h1>Planes</h1>
    <p class="subtitulo">Crea, edita o desactiva los planes de pago — sin necesitar un despliegue.</p>

    <div class="tarjeta tabla-envoltorio">
      <table>
        <thead>
          <tr><th>Nombre</th><th>Nivel de acceso</th><th>Precio</th><th>Estado</th><th></th></tr>
        </thead>
        <tbody>
          @for (plan of planes(); track plan.id) {
            <tr>
              @if (editandoId() === plan.id) {
                <td><input [(ngModel)]="formEdicion.nombre" name="nombreEdicion" /></td>
                <td><input [(ngModel)]="formEdicion.nivel_de_acceso" name="nivelEdicion" /></td>
                <td><input type="number" [(ngModel)]="formEdicion.precio_clp" name="precioEdicion" /></td>
                <td><span class="chip" [class.chip--activo]="plan.activo">{{ plan.activo ? 'Activo' : 'Inactivo' }}</span></td>
                <td class="acciones">
                  <button class="btn btn--primario btn--chico" (click)="guardarEdicion(plan)">Guardar</button>
                  <button class="btn btn--secundario btn--chico" (click)="cancelarEdicion()">Cancelar</button>
                </td>
              } @else {
                <td>{{ plan.nombre }}</td>
                <td>{{ plan.nivel_de_acceso }}</td>
                <td>{{ formatearClp(plan.precio_clp) }}</td>
                <td><span class="chip" [class.chip--activo]="plan.activo">{{ plan.activo ? 'Activo' : 'Inactivo' }}</span></td>
                <td class="acciones">
                  <button class="btn btn--secundario btn--chico" (click)="editar(plan)">Editar</button>
                  <button class="btn btn--secundario btn--chico" (click)="cambiarEstado(plan)">
                    {{ plan.activo ? 'Desactivar' : 'Activar' }}
                  </button>
                </td>
              }
            </tr>
          }
          @if (!planes().length) {
            <tr><td colspan="5" class="vacio">Todavía no hay planes creados.</td></tr>
          }
        </tbody>
      </table>
    </div>

    <h2>Crear plan</h2>
    <form class="tarjeta form-crear" (submit)="$event.preventDefault(); crear()">
      <div class="campo">
        <label>Nombre</label>
        <input [(ngModel)]="formCrear.nombre" name="nombre" placeholder="Mensual" />
      </div>
      <div class="campo">
        <label>Nivel de acceso</label>
        <input [(ngModel)]="formCrear.nivel_de_acceso" name="nivelDeAcceso" placeholder="completo" />
      </div>
      <div class="campo">
        <label>Precio (CLP)</label>
        <input type="number" [(ngModel)]="formCrear.precio_clp" name="precioClp" placeholder="19990" />
      </div>
      @if (errorCrear()) {
        <p class="error">{{ errorCrear() }}</p>
      }
      <button type="submit" class="btn btn--primario">Crear plan</button>
    </form>
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
        margin-bottom: 2.5rem;
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
      .chip {
        display: inline-block;
        font-size: 0.75rem;
        font-weight: 600;
        padding: 0.2rem 0.6rem;
        border-radius: 999px;
        background: var(--fondo);
        color: var(--texto-secundario);
      }
      .chip--activo {
        background: var(--color-exito-suave);
        color: var(--color-exito);
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
        color: var(--color-error);
        font-size: 0.85rem;
      }
      input {
        width: 100%;
      }
    `,
  ],
})
export class AdminPlanes {
  planes = signal<Plan[]>([]);
  editandoId = signal<number | null>(null);
  errorCrear = signal('');

  formCrear = { nombre: '', nivel_de_acceso: '', precio_clp: 0 };
  formEdicion = { nombre: '', nivel_de_acceso: '', precio_clp: 0 };

  private comercial = inject(ComercialService);

  constructor() {
    this.cargar();
  }

  private cargar() {
    this.comercial.listarPlanes().subscribe((planes) => this.planes.set(planes));
  }

  crear() {
    this.errorCrear.set('');
    this.comercial.crearPlan(this.formCrear.nombre, this.formCrear.nivel_de_acceso, this.formCrear.precio_clp).subscribe({
      next: () => {
        this.formCrear = { nombre: '', nivel_de_acceso: '', precio_clp: 0 };
        this.cargar();
      },
      error: () => this.errorCrear.set('No se pudo crear el plan — revisa los datos.'),
    });
  }

  editar(plan: Plan) {
    this.editandoId.set(plan.id);
    this.formEdicion = { nombre: plan.nombre, nivel_de_acceso: plan.nivel_de_acceso, precio_clp: plan.precio_clp };
  }

  cancelarEdicion() {
    this.editandoId.set(null);
  }

  guardarEdicion(plan: Plan) {
    this.comercial
      .editarPlan(plan.id, this.formEdicion.nombre, this.formEdicion.nivel_de_acceso, this.formEdicion.precio_clp)
      .subscribe(() => {
        this.editandoId.set(null);
        this.cargar();
      });
  }

  cambiarEstado(plan: Plan) {
    this.comercial.cambiarEstadoPlan(plan.id, !plan.activo).subscribe(() => this.cargar());
  }

  formatearClp(valor: number): string {
    return '$' + valor.toLocaleString('es-CL');
  }
}
