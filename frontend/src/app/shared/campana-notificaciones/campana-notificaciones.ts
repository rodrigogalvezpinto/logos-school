import { Component, inject, signal } from '@angular/core';
import { Notificacion, NotificacionesService } from '../../core/notificaciones.service';
import { SesionService } from '../../core/sesion.service';

const ICONO_POR_TIPO: Record<Notificacion['tipo'], string> = {
  comunicado: '📣',
  sesion_atrasada: '⏰',
  reporte_resuelto: '✅',
};

/** Centro de notificaciones (Fase 1 del plan de incorporación de hallazgos de Brincus —
 * ver planificacion/27-plan-incorporacion-hallazgos-brincus.md, Paso 12: campana con
 * Notificaciones / Errores reportados). Sin estado leído/no-leído persistido — el badge
 * muestra el total de notificaciones activas calculadas al vuelo por el backend, no un
 * contador aparte que podría desincronizarse. */
@Component({
  selector: 'app-campana-notificaciones',
  standalone: true,
  template: `
    <div class="campana">
      <button
        type="button"
        class="campana__boton"
        (click)="alternar()"
        [attr.aria-expanded]="abierto()"
        aria-label="Notificaciones"
      >
        🔔
        @if (notificaciones().length) {
          <span class="campana__badge">{{ notificaciones().length }}</span>
        }
      </button>
      @if (abierto()) {
        <div class="campana__panel">
          <h3>Notificaciones</h3>
          @if (cargando()) {
            <p class="campana__estado">Cargando…</p>
          } @else if (notificaciones().length) {
            <ul class="campana__lista">
              @for (n of notificaciones(); track n.fecha + n.titulo) {
                <li>
                  <span class="campana__icono">{{ icono(n.tipo) }}</span>
                  <div>
                    <p class="campana__titulo">{{ n.titulo }}</p>
                    <p class="campana__detalle">{{ n.detalle }}</p>
                  </div>
                </li>
              }
            </ul>
          } @else {
            <p class="campana__estado">No tienes notificaciones nuevas.</p>
          }
        </div>
      }
    </div>
  `,
  styles: [
    `
      .campana {
        position: relative;
      }
      .campana__boton {
        position: relative;
        background: none;
        border: none;
        font-size: 1.3rem;
        cursor: pointer;
        padding: 0.3rem;
        line-height: 1;
      }
      .campana__badge {
        position: absolute;
        top: -2px;
        right: -2px;
        background: var(--color-secundario-badge);
        color: white;
        font-size: 0.65rem;
        font-weight: 700;
        min-width: 16px;
        height: 16px;
        border-radius: 999px;
        display: flex;
        align-items: center;
        justify-content: center;
        padding: 0 3px;
        border: 2px solid white;
      }
      .campana__panel {
        position: absolute;
        right: 0;
        top: calc(100% + 0.6rem);
        width: 300px;
        max-height: 380px;
        overflow-y: auto;
        background: var(--fondo-tarjeta, #fff);
        border-radius: var(--radio-basica);
        box-shadow: var(--sombra-tarjeta);
        padding: 1rem 1.1rem;
        z-index: 60;
      }
      .campana__panel h3 {
        margin: 0 0 0.75rem;
        font-size: 0.95rem;
      }
      .campana__estado {
        margin: 0;
        font-size: 0.85rem;
        color: var(--texto-secundario);
      }
      .campana__lista {
        list-style: none;
        margin: 0;
        padding: 0;
        display: flex;
        flex-direction: column;
        gap: 0.75rem;
      }
      .campana__lista li {
        display: flex;
        gap: 0.6rem;
        align-items: flex-start;
      }
      .campana__icono {
        flex-shrink: 0;
        font-size: 1.1rem;
      }
      .campana__titulo {
        margin: 0;
        font-size: 0.85rem;
        font-weight: 700;
        color: var(--texto-principal);
      }
      .campana__detalle {
        margin: 0.15rem 0 0;
        font-size: 0.8rem;
        color: var(--texto-secundario);
      }
    `,
  ],
})
export class CampanaNotificaciones {
  abierto = signal(false);
  cargando = signal(false);
  notificaciones = signal<Notificacion[]>([]);

  private notificacionesService = inject(NotificacionesService);
  private sesion = inject(SesionService);
  private cargado = false;

  ngOnInit() {
    const perfil = this.sesion.perfilActivo();
    if (!perfil) return;
    this.cargando.set(true);
    this.notificacionesService.listar(perfil.id).subscribe({
      next: (n) => {
        this.notificaciones.set(n);
        this.cargando.set(false);
        this.cargado = true;
      },
      error: () => this.cargando.set(false),
    });
  }

  icono(tipo: Notificacion['tipo']): string {
    return ICONO_POR_TIPO[tipo];
  }

  alternar() {
    this.abierto.set(!this.abierto());
  }
}
