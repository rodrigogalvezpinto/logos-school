import { Component, inject, signal } from '@angular/core';
import { ComercialService, Metricas } from '../../core/comercial.service';

@Component({
  selector: 'app-admin-dashboard',
  standalone: true,
  template: `
    <h1>Dashboard</h1>
    <p class="subtitulo">Cómo va Logos School, de un vistazo.</p>

    @if (metricas(); as m) {
      <div class="grid-resumen">
        <div class="tarjeta resumen-card">
          <span class="resumen-card__etiqueta">Apoderados registrados</span>
          <span class="resumen-card__valor">{{ m.apoderados_registrados }}</span>
        </div>
        <div class="tarjeta resumen-card">
          <span class="resumen-card__etiqueta">Alumnos registrados</span>
          <span class="resumen-card__valor">{{ m.alumnos_registrados }}</span>
        </div>
        <div class="tarjeta resumen-card">
          <span class="resumen-card__etiqueta">Ingresos del mes (aprox.)</span>
          <span class="resumen-card__valor">{{ formatearClp(m.ingresos_mes_aprox_clp) }}</span>
        </div>
      </div>

      <h2>Suscripciones activas por plan</h2>
      @if (m.suscripciones_por_plan.length) {
        <div class="tarjeta tabla-envoltorio">
          <table>
            <thead>
              <tr><th>Plan</th><th>Activas</th></tr>
            </thead>
            <tbody>
              @for (s of m.suscripciones_por_plan; track s.plan_id) {
                <tr><td>{{ s.plan_nombre }}</td><td>{{ s.activas }}</td></tr>
              }
            </tbody>
          </table>
        </div>
      } @else {
        <p class="vacio">Todavía no hay suscripciones activas.</p>
      }
    } @else if (error()) {
      <p class="error-carga">{{ error() }}</p>
    } @else {
      <p>Cargando…</p>
    }
  `,
  styles: [
    `
      .subtitulo {
        color: var(--texto-secundario);
        margin-top: -0.5rem;
        margin-bottom: 2rem;
      }
      .grid-resumen {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
        gap: 1rem;
        margin-bottom: 2.5rem;
      }
      .resumen-card {
        display: flex;
        flex-direction: column;
        gap: 0.5rem;
      }
      .resumen-card__etiqueta {
        font-size: 0.8rem;
        color: var(--texto-secundario);
      }
      .resumen-card__valor {
        font-family: var(--fuente-titulos);
        font-weight: 700;
        font-size: 1.75rem;
      }
      h2 {
        font-size: 1.05rem;
        margin-bottom: 0.75rem;
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
      .vacio {
        color: var(--texto-secundario);
      }
      .error-carga {
        color: var(--color-error-texto);
      }
    `,
  ],
})
export class AdminDashboard {
  metricas = signal<Metricas | null>(null);
  error = signal('');

  private comercial = inject(ComercialService);

  constructor() {
    this.comercial.obtenerMetricas().subscribe({
      next: (m) => this.metricas.set(m),
      error: () => this.error.set('No se pudieron cargar las métricas.'),
    });
  }

  formatearClp(valor: number): string {
    return '$' + valor.toLocaleString('es-CL');
  }
}
