import { Component, computed, inject, signal } from '@angular/core';
import { UtilEscolar, UtilesEscolaresService } from '../../core/utiles-escolares.service';
import { SesionService } from '../../core/sesion.service';

interface GrupoUtiles {
  etiqueta: string;
  items: UtilEscolar[];
}

const ETIQUETA_GENERALES = 'Materiales generales';

@Component({
  selector: 'app-utiles-escolares',
  standalone: true,
  template: `
    <h1>Útiles Escolares</h1>
    <p class="subtitulo">Lo que necesitas comprar para tu nivel, en un solo lugar.</p>

    @if (grupos().length) {
      <div class="lista-grupos">
        @for (grupo of grupos(); track grupo.etiqueta) {
          <div class="tarjeta grupo">
            <h2>{{ grupo.etiqueta }}</h2>
            <ul class="lista-items">
              @for (item of grupo.items; track item.id) {
                <li>
                  <span class="lista-items__nombre">{{ item.nombre }}</span>
                  @if (item.cantidad) {
                    <span class="lista-items__cantidad">× {{ item.cantidad }}</span>
                  }
                </li>
              }
            </ul>
          </div>
        }
      </div>
    } @else if (error()) {
      <p class="error-carga">{{ error() }}</p>
    } @else if (cargando()) {
      <p>Cargando…</p>
    } @else {
      <p class="vacio">Todavía no hay una lista de útiles armada para tu nivel.</p>
    }
  `,
  styles: [
    `
      .subtitulo {
        color: var(--texto-secundario);
        margin-top: -0.5rem;
        margin-bottom: 2rem;
        max-width: 640px;
      }
      .lista-grupos {
        display: grid;
        grid-template-columns: repeat(auto-fill, minmax(260px, 1fr));
        gap: 1.25rem;
      }
      .grupo h2 {
        margin: 0 0 0.75rem;
        font-size: 0.95rem;
      }
      .lista-items {
        list-style: none;
        margin: 0;
        padding: 0;
        display: flex;
        flex-direction: column;
        gap: 0.5rem;
      }
      .lista-items li {
        display: flex;
        justify-content: space-between;
        gap: 0.75rem;
        font-size: 0.9rem;
        color: var(--texto-principal);
      }
      .lista-items__cantidad {
        color: var(--texto-secundario);
        flex-shrink: 0;
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
export class UtilesEscolares {
  utiles = signal<UtilEscolar[]>([]);
  cargando = signal(true);
  error = signal('');

  private utilesEscolares = inject(UtilesEscolaresService);
  private sesion = inject(SesionService);

  ngOnInit() {
    const perfil = this.sesion.perfilActivo();
    if (!perfil) return;
    this.utilesEscolares.listarPorNivel(perfil.nivel_id).subscribe({
      next: (utiles) => {
        this.utiles.set(utiles);
        this.cargando.set(false);
      },
      error: () => {
        this.error.set('No se pudo cargar la lista de útiles escolares. Intenta recargar la página.');
        this.cargando.set(false);
      },
    });
  }

  grupos = computed<GrupoUtiles[]>(() => {
    const porAsignatura = new Map<string, UtilEscolar[]>();
    for (const item of this.utiles()) {
      const clave = item.asignatura ?? ETIQUETA_GENERALES;
      if (!porAsignatura.has(clave)) porAsignatura.set(clave, []);
      porAsignatura.get(clave)!.push(item);
    }
    // Generales primero (estuche, block — aplican a todas las materias), luego cada
    // asignatura en el orden en que aparecieron.
    return Array.from(porAsignatura.entries())
      .sort(([a], [b]) => {
        if (a === ETIQUETA_GENERALES) return -1;
        if (b === ETIQUETA_GENERALES) return 1;
        return 0;
      })
      .map(([etiqueta, items]) => ({ etiqueta, items }));
  });
}
