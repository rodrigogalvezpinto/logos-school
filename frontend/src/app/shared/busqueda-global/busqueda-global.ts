import { Component, inject, signal } from '@angular/core';
import { Router } from '@angular/router';
import { forkJoin } from 'rxjs';
import { AsignaturaRespuesta, ContenidoService, ObjetivoRespuesta } from '../../core/contenido.service';
import { SesionService } from '../../core/sesion.service';

interface ResultadoBusqueda {
  oa: ObjetivoRespuesta;
  asignaturaId: number;
  asignaturaNombre: string;
}

const MAX_RESULTADOS = 8;

/** Búsqueda global de contenido (Fase 1 del plan de incorporación de hallazgos de
 * Brincus — ver planificacion/27-plan-incorporacion-hallazgos-brincus.md): a diferencia del
 * buscador de `asignatura-detalle.ts` (acotado a una asignatura ya abierta), este busca en
 * todos los OA de todas las asignaturas del nivel del alumno a la vez, desde la topbar,
 * visible en cualquier página. Carga y cachea el contenido del nivel una sola vez (mismo
 * volumen de datos que ya recorre `asignatura-detalle.ts` por asignatura, solo que junta
 * todas) — sin backend nuevo de búsqueda de texto completo, consistente con "Fase 1 sin
 * dependencias externas". */
@Component({
  selector: 'app-busqueda-global',
  standalone: true,
  template: `
    <div class="busqueda-global">
      <input
        type="search"
        placeholder="Buscar en tus asignaturas…"
        [value]="termino()"
        (input)="alEscribir($any($event.target).value)"
        (focus)="abierto.set(true)"
        (blur)="alPerderFoco()"
      />
      @if (abierto() && termino().trim().length >= 2) {
        <div class="busqueda-global__resultados">
          @if (cargando()) {
            <p class="busqueda-global__estado">Buscando…</p>
          } @else if (resultados().length) {
            @for (r of resultados(); track r.oa.id) {
              <button type="button" class="busqueda-global__item" (mousedown)="irA(r)">
                <span class="busqueda-global__asignatura">{{ r.asignaturaNombre }}</span>
                <span class="busqueda-global__oa">{{ r.oa.codigo_oficial }} — {{ r.oa.descripcion }}</span>
              </button>
            }
          } @else {
            <p class="busqueda-global__estado">Sin resultados para "{{ termino() }}".</p>
          }
        </div>
      }
    </div>
  `,
  styles: [
    `
      .busqueda-global {
        position: relative;
        width: 100%;
        max-width: 320px;
      }
      input[type='search'] {
        width: 100%;
        padding: 0.5rem 0.85rem;
        border: 1.5px solid var(--borde);
        border-radius: var(--radio-media);
        background: var(--fondo, #f7f7fb);
        color: var(--texto-principal);
        font-size: 0.85rem;
      }
      input[type='search']:focus {
        outline: none;
        border-color: var(--color-primario);
      }
      .busqueda-global__resultados {
        position: absolute;
        top: calc(100% + 0.4rem);
        left: 0;
        right: 0;
        background: var(--fondo-tarjeta, #fff);
        border: 1px solid var(--borde);
        border-radius: var(--radio-basica);
        box-shadow: var(--sombra-tarjeta);
        max-height: 340px;
        overflow-y: auto;
        z-index: 50;
      }
      .busqueda-global__item {
        display: flex;
        flex-direction: column;
        align-items: flex-start;
        gap: 0.15rem;
        width: 100%;
        padding: 0.6rem 0.85rem;
        border: none;
        border-bottom: 1px solid var(--borde);
        background: none;
        text-align: left;
        cursor: pointer;
      }
      .busqueda-global__item:last-child {
        border-bottom: none;
      }
      .busqueda-global__item:hover {
        background: var(--color-primario-suave);
      }
      .busqueda-global__asignatura {
        font-size: 0.7rem;
        font-weight: 700;
        text-transform: uppercase;
        color: var(--color-primario);
      }
      .busqueda-global__oa {
        font-size: 0.85rem;
        color: var(--texto-principal);
      }
      .busqueda-global__estado {
        margin: 0;
        padding: 0.75rem 0.85rem;
        font-size: 0.85rem;
        color: var(--texto-secundario);
      }
    `,
  ],
})
export class BusquedaGlobal {
  termino = signal('');
  abierto = signal(false);
  cargando = signal(false);

  private todosLosOa = signal<ResultadoBusqueda[] | null>(null);
  private contenido = inject(ContenidoService);
  private sesion = inject(SesionService);
  private router = inject(Router);

  private asegurarIndiceCargado() {
    if (this.todosLosOa() !== null || this.cargando()) return;
    const perfil = this.sesion.perfilActivo();
    if (!perfil) return;

    this.cargando.set(true);
    this.contenido.listarAsignaturas(perfil.nivel_id).subscribe((asignaturas: AsignaturaRespuesta[]) => {
      if (!asignaturas.length) {
        this.todosLosOa.set([]);
        this.cargando.set(false);
        return;
      }
      forkJoin(asignaturas.map((a) => this.contenido.listarObjetivos(a.id))).subscribe((listasDeOa) => {
        const indice: ResultadoBusqueda[] = [];
        asignaturas.forEach((a, i) => {
          for (const oa of listasDeOa[i]) {
            indice.push({ oa, asignaturaId: a.id, asignaturaNombre: a.nombre });
          }
        });
        this.todosLosOa.set(indice);
        this.cargando.set(false);
      });
    });
  }

  alEscribir(valor: string) {
    this.termino.set(valor);
    this.abierto.set(true);
    this.asegurarIndiceCargado();
  }

  alPerderFoco() {
    // Timeout corto: deja que el (mousedown) de un resultado se dispare antes de que el
    // dropdown se oculte por el blur del input.
    setTimeout(() => this.abierto.set(false), 150);
  }

  resultados(): ResultadoBusqueda[] {
    const termino = this.termino().trim().toLowerCase();
    const indice = this.todosLosOa();
    if (!indice || termino.length < 2) return [];
    return indice
      .filter(
        (r) =>
          r.oa.codigo_oficial.toLowerCase().includes(termino) ||
          r.oa.descripcion.toLowerCase().includes(termino) ||
          r.oa.contenido_guia.toLowerCase().includes(termino),
      )
      .slice(0, MAX_RESULTADOS);
  }

  irA(r: ResultadoBusqueda) {
    this.termino.set('');
    this.abierto.set(false);
    this.router.navigate(['/alumno/estudiar', r.oa.id]);
  }
}
