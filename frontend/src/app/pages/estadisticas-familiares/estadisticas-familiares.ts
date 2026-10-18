import { Component, inject, signal } from '@angular/core';
import { RouterLink } from '@angular/router';
import { ApoderadoService, EstadisticaAlumno } from '../../core/apoderado.service';

/** Idea 1 del boceto de innovación (2026-08-17): "Estadísticas" como vista propia del
 * Apoderado — junta a todos sus hijos en una sola pantalla, antes de entrar al detalle de
 * ninguno. Solo tiene sentido con 2+ alumnos (con uno solo, "Mis Notas" ya cumple ese rol);
 * el sidebar ya la oculta en ese caso, pero la ruta también es accesible por URL directa. */
@Component({
  selector: 'app-estadisticas-familiares',
  standalone: true,
  imports: [RouterLink],
  template: `
    <h1>Estadísticas</h1>
    <p class="subtitulo">Cómo van todos tus alumnos, de un vistazo.</p>

    @if (error()) {
      <p class="error-carga">{{ error() }}</p>
    } @else if (estadisticas(); as lista) {
      <div class="grid">
        @for (e of lista; track e.perfil_alumno_id) {
          <a class="tarjeta estadistica-card" [routerLink]="['/apoderado/progreso', e.perfil_alumno_id]">
            <div class="estadistica-card__top">
              <h3>{{ e.nombre }}</h3>
              <span class="chip" [class.chip--alerta]="e.tiene_alerta_de_ritmo" [class.chip--ok]="!e.tiene_alerta_de_ritmo">
                {{ e.tiene_alerta_de_ritmo ? 'Atrasado' : 'Al día' }}
              </span>
            </div>
            <div class="barra">
              <div class="barra__relleno" [class.barra__relleno--alerta]="e.tiene_alerta_de_ritmo" [style.width.%]="e.cobertura_pct"></div>
            </div>
            <p class="estadistica-card__detalle">
              {{ e.cobertura_pct }}% del temario cubierto
              @if (e.racha_dias_actual > 0) {
                · racha de {{ e.racha_dias_actual }} día{{ e.racha_dias_actual > 1 ? 's' : '' }}
              }
            </p>
          </a>
        }
        @if (!lista.length) {
          <p class="vacio">Todavía no hay alumnos agregados.</p>
        }
      </div>
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
      .grid {
        display: grid;
        grid-template-columns: repeat(auto-fill, minmax(260px, 1fr));
        gap: 1rem;
        max-width: 900px;
      }
      .estadistica-card {
        display: flex;
        flex-direction: column;
        gap: 0.6rem;
        text-decoration: none;
        color: inherit;
      }
      .estadistica-card__top {
        display: flex;
        justify-content: space-between;
        align-items: center;
        gap: 0.5rem;
      }
      .estadistica-card__top h3 {
        margin: 0;
      }
      .chip {
        font-size: 0.68rem;
        font-weight: 700;
        padding: 0.2rem 0.6rem;
        border-radius: 999px;
      }
      .chip--ok {
        background: var(--color-exito-suave);
        color: var(--color-exito-texto);
      }
      .chip--alerta {
        background: var(--color-alerta-suave);
        color: var(--color-alerta-texto);
      }
      .barra {
        height: 8px;
        border-radius: 999px;
        background: var(--fondo, #eee);
        overflow: hidden;
      }
      .barra__relleno {
        height: 100%;
        border-radius: 999px;
        background: var(--color-primario);
      }
      .barra__relleno--alerta {
        background: var(--color-alerta);
      }
      .estadistica-card__detalle {
        margin: 0;
        font-size: 0.82rem;
        color: var(--texto-secundario);
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
export class EstadisticasFamiliares {
  estadisticas = signal<EstadisticaAlumno[] | null>(null);
  error = signal('');

  private apoderado = inject(ApoderadoService);

  ngOnInit() {
    this.apoderado.obtenerEstadisticas().subscribe({
      next: (e) => this.estadisticas.set(e),
      error: () => this.error.set('No se pudieron cargar las estadísticas. Intenta recargar la página.'),
    });
  }
}
