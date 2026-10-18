import { DatePipe } from '@angular/common';
import { Component, inject, signal } from '@angular/core';
import { AuthService, PerfilAlumnoRespuesta, SuscripcionRespuesta } from '../../core/auth.service';

interface FilaPago {
  alumno: PerfilAlumnoRespuesta;
  suscripcion: SuscripcionRespuesta | null;
}

const ETIQUETA_ORIGEN: Record<string, string> = {
  pago: 'Pago',
  prueba_gratis: 'Prueba gratis',
  cortesia: 'Cortesía',
};

/** Fase 1, ítem 2.8 del plan de incorporación de hallazgos de Brincus — historial de
 * pagos para el Apoderado, con los datos que ya existen hoy (ver
 * planificacion/27-plan-incorporacion-hallazgos-brincus.md). `Suscripcion` todavía no
 * acumula historial de transacciones (una fila vigente por alumno) ni comprobante con
 * monto real (eso llega con la pasarela de pago) — se muestra lo que sí existe: plan
 * activo, fechas y origen, sin prometer más de lo que hay. */
@Component({
  selector: 'app-historial-pagos',
  standalone: true,
  imports: [DatePipe],
  template: `
    <h1>Plan y Pagos</h1>
    <p class="subtitulo">El plan y estado de suscripción de cada uno de tus alumnos.</p>

    @if (error()) {
      <p class="error-carga">{{ error() }}</p>
    }

    <div class="lista">
      @for (fila of filas(); track fila.alumno.id) {
        <div class="tarjeta fila-pago">
          <div class="fila-pago__alumno">
            <h3>{{ fila.alumno.nombre }} {{ fila.alumno.apellidos }}</h3>
            @if (fila.suscripcion; as s) {
              <span class="chip" [class.chip--activo]="s.estado === 'activa'">{{ s.estado === 'activa' ? 'Plan activo' : s.estado }}</span>
            } @else {
              <span class="chip">Sin plan</span>
            }
          </div>

          @if (fila.suscripcion; as s) {
            <div class="fila-pago__detalle">
              <p><strong>{{ s.plan_nombre }}</strong> — {{ etiquetaOrigen(s.origen) }}</p>
              <p class="fila-pago__fechas">
                Desde {{ s.fecha_inicio | date: 'dd-MM-yyyy' }}
                @if (s.fecha_termino) {
                  hasta {{ s.fecha_termino | date: 'dd-MM-yyyy' }}
                }
              </p>
            </div>
          } @else {
            <p class="fila-pago__vacio">Este alumno todavía no tiene un plan asociado.</p>
          }
        </div>
      }
      @if (!filas().length && !error()) {
        <p class="vacio">Cargando…</p>
      }
    </div>

    <p class="nota">
      El comprobante de pago con el monto exacto cobrado estará disponible cuando se
      integre la pasarela de pago real.
    </p>
  `,
  styles: [
    `
      .subtitulo {
        color: var(--texto-secundario);
        margin-top: -0.5rem;
        margin-bottom: 2rem;
      }
      .lista {
        display: flex;
        flex-direction: column;
        gap: 0.85rem;
        max-width: 560px;
      }
      .fila-pago {
        display: flex;
        justify-content: space-between;
        align-items: flex-start;
        gap: 1rem;
      }
      .fila-pago__alumno h3 {
        margin: 0 0 0.35rem;
      }
      .fila-pago__detalle {
        text-align: right;
        flex-shrink: 0;
        p {
          margin: 0;
        }
      }
      @media (max-width: 480px) {
        .fila-pago {
          flex-direction: column;
          align-items: stretch;
        }
        .fila-pago__detalle {
          text-align: left;
        }
      }
      .fila-pago__fechas {
        font-size: 0.8rem;
        color: var(--texto-secundario);
        margin-top: 0.15rem !important;
      }
      .fila-pago__vacio {
        color: var(--texto-secundario);
        font-size: 0.85rem;
      }
      .chip {
        display: inline-block;
        font-size: 0.7rem;
        font-weight: 600;
        padding: 0.2rem 0.55rem;
        border-radius: 999px;
        background: var(--fondo);
        color: var(--texto-secundario);
      }
      .chip--activo {
        background: var(--color-exito-suave);
        color: var(--color-exito-texto);
      }
      .vacio {
        color: var(--texto-secundario);
      }
      .error-carga {
        color: var(--color-error-texto);
      }
      .nota {
        margin-top: 2rem;
        font-size: 0.8rem;
        color: var(--texto-secundario);
        max-width: 560px;
      }
    `,
  ],
})
export class HistorialPagos {
  filas = signal<FilaPago[]>([]);
  error = signal('');

  private auth = inject(AuthService);

  ngOnInit() {
    this.auth.listarAlumnos().subscribe({
      next: (alumnos) => {
        if (!alumnos.length) return;
        alumnos.forEach((alumno) => {
          this.auth.obtenerSuscripcion(alumno.id).subscribe({
            next: (suscripcion) => this.filas.update((f) => [...f, { alumno, suscripcion }]),
            error: () => this.filas.update((f) => [...f, { alumno, suscripcion: null }]),
          });
        });
      },
      error: () => this.error.set('No se pudo cargar tus alumnos. Intenta recargar la página.'),
    });
  }

  etiquetaOrigen(origen: string): string {
    return ETIQUETA_ORIGEN[origen] || origen;
  }
}
