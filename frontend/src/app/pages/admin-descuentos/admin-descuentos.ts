import { Component, inject, signal } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { ComercialService, Descuento } from '../../core/comercial.service';

@Component({
  selector: 'app-admin-descuentos',
  standalone: true,
  imports: [FormsModule],
  template: `
    <h1>Códigos de descuento</h1>
    <p class="subtitulo">Crea códigos de descuento o desactiva los que ya no quieres que se usen.</p>

    <div class="tarjeta tabla-envoltorio">
      <table>
        <thead>
          <tr><th>Código</th><th>Tipo</th><th>Valor</th><th>Usos</th><th>Vence</th><th>Estado</th><th></th></tr>
        </thead>
        <tbody>
          @for (d of descuentos(); track d.id) {
            <tr>
              <td>{{ d.codigo }}</td>
              <td>{{ d.tipo === 'porcentaje' ? 'Porcentaje' : 'Monto fijo' }}</td>
              <td>{{ d.tipo === 'porcentaje' ? d.valor + '%' : formatearClp(d.valor) }}</td>
              <td>{{ d.usos_actuales }}{{ d.usos_maximos ? ' / ' + d.usos_maximos : '' }}</td>
              <td>{{ d.fecha_vencimiento || 'Sin vencimiento' }}</td>
              <td><span class="chip" [class.chip--activo]="d.vigente">{{ d.vigente ? 'Vigente' : 'No vigente' }}</span></td>
              <td>
                @if (d.vigente) {
                  <button class="btn btn--secundario btn--chico" (click)="desactivar(d)">Desactivar</button>
                }
              </td>
            </tr>
          }
          @if (!descuentos().length) {
            <tr><td colspan="7" class="vacio">Todavía no hay códigos de descuento creados.</td></tr>
          }
        </tbody>
      </table>
    </div>

    <h2>Crear código</h2>
    <form class="tarjeta form-crear" (submit)="$event.preventDefault(); crear()">
      <div class="campo">
        <label>Código</label>
        <input [(ngModel)]="form.codigo" name="codigo" placeholder="BIENVENIDA20" />
      </div>
      <div class="campo">
        <label>Tipo</label>
        <select [(ngModel)]="form.tipo" name="tipo">
          <option value="porcentaje">Porcentaje</option>
          <option value="monto_fijo">Monto fijo (CLP)</option>
        </select>
      </div>
      <div class="campo">
        <label>Valor</label>
        <input type="number" [(ngModel)]="form.valor" name="valor" placeholder="20" />
      </div>
      <div class="campo">
        <label>Fecha de vencimiento (opcional)</label>
        <input type="date" [(ngModel)]="form.fecha_vencimiento" name="fechaVencimiento" />
      </div>
      <div class="campo">
        <label>Usos máximos (opcional)</label>
        <input type="number" [(ngModel)]="form.usos_maximos" name="usosMaximos" placeholder="100" />
      </div>
      @if (error()) {
        <p class="error">{{ error() }}</p>
      }
      <button type="submit" class="btn btn--primario">Crear código</button>
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
        white-space: nowrap;
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
      .btn--chico {
        padding: 0.4rem 0.75rem;
        font-size: 0.8rem;
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
      input, select {
        width: 100%;
      }
    `,
  ],
})
export class AdminDescuentos {
  descuentos = signal<Descuento[]>([]);
  error = signal('');

  form: { codigo: string; tipo: string; valor: number; fecha_vencimiento: string; usos_maximos: number | null } = {
    codigo: '', tipo: 'porcentaje', valor: 0, fecha_vencimiento: '', usos_maximos: null,
  };

  private comercial = inject(ComercialService);

  constructor() {
    this.cargar();
  }

  private cargar() {
    this.comercial.listarDescuentos().subscribe((descuentos) => this.descuentos.set(descuentos));
  }

  crear() {
    this.error.set('');
    this.comercial
      .crearDescuento(
        this.form.codigo, this.form.tipo, this.form.valor,
        this.form.fecha_vencimiento || null, this.form.usos_maximos || null
      )
      .subscribe({
        next: () => {
          this.form = { codigo: '', tipo: 'porcentaje', valor: 0, fecha_vencimiento: '', usos_maximos: null };
          this.cargar();
        },
        error: () => this.error.set('No se pudo crear el código — revisa los datos.'),
      });
  }

  desactivar(d: Descuento) {
    this.comercial.desactivarDescuento(d.id).subscribe(() => this.cargar());
  }

  formatearClp(valor: number): string {
    return '$' + valor.toLocaleString('es-CL');
  }
}
