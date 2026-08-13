import { Component, Input, inject, signal } from '@angular/core';
import { ProgresoService, Historial, ItemHistorial } from '../../core/progreso.service';
import { SesionService } from '../../core/sesion.service';

interface FilaHistorial {
  etiqueta: string;
  detalle: string;
  nota: number | null;
  fecha: string;
  tipo: 'prueba_unidad' | 'examen_simulacro' | 'guia';
}

@Component({
  selector: 'app-notas',
  standalone: true,
  template: `
    <h1>Mis Notas</h1>
    <p class="subtitulo">Tu avance por asignatura y todo lo que has estudiado hasta ahora.</p>

    @if (historial(); as h) {
      <div class="grid-notas">
        @for (n of h.notas_por_asignatura; track n.asignatura_id) {
          <div class="tarjeta nota-card">
            <h3>{{ n.asignatura_nombre }}</h3>
            <div class="nota-card__filas">
              <div class="nota-card__fila">
                <span class="chip chip--practica">Nota de práctica</span>
                <span class="nota-card__valor">{{ n.nota_practica ?? '—' }}</span>
              </div>
              <div class="nota-card__fila">
                <span class="chip chip--simulacro">Resultado de simulacro</span>
                <span class="nota-card__valor">{{ n.nota_simulacro ?? '—' }}</span>
              </div>
            </div>
            @if (n.nota_simulacro !== null) {
              <p class="nota-card__aviso">Esta es tu mejor referencia de cómo te iría en el examen real.</p>
            }
          </div>
        }
        @if (!h.notas_por_asignatura.length) {
          <p class="vacio">Todavía no has rendido ninguna prueba de unidad ni examen simulacro.</p>
        }
      </div>

      <h2>Historial</h2>
      <div class="lista-historial">
        @for (fila of filasHistorial(); track fila.fecha + fila.etiqueta) {
          <div class="tarjeta fila-historial">
            <div>
              <span class="chip" [class.chip--practica]="fila.tipo === 'prueba_unidad'"
                [class.chip--simulacro]="fila.tipo === 'examen_simulacro'"
                [class.chip--guia]="fila.tipo === 'guia'">
                {{ etiquetaTipo(fila.tipo) }}
              </span>
              <h4>{{ fila.etiqueta }}</h4>
              <p>{{ fila.detalle }}</p>
            </div>
            @if (fila.nota !== null) {
              <span class="fila-historial__nota">{{ fila.nota }}</span>
            }
          </div>
        }
        @if (!filasHistorial().length) {
          <p class="vacio">Tu historial de estudio va a aparecer acá.</p>
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
      .grid-notas {
        display: grid;
        grid-template-columns: repeat(auto-fill, minmax(260px, 1fr));
        gap: 1rem;
        margin-bottom: 2.5rem;
      }
      .nota-card h3 {
        margin: 0 0 0.75rem;
      }
      .nota-card__filas {
        display: flex;
        flex-direction: column;
        gap: 0.5rem;
      }
      .nota-card__fila {
        display: flex;
        justify-content: space-between;
        align-items: center;
      }
      .nota-card__valor {
        font-family: var(--fuente-titulos);
        font-weight: 700;
        font-size: 1.15rem;
      }
      .nota-card__aviso {
        margin: 0.75rem 0 0;
        font-size: 0.8rem;
        color: var(--texto-secundario);
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
      .chip--practica {
        background: var(--color-primario-suave);
        color: var(--color-primario);
      }
      .chip--simulacro {
        background: var(--color-secundario-suave);
        color: var(--color-secundario);
      }
      .chip--guia {
        background: var(--color-exito-suave);
        color: var(--color-exito);
      }
      .lista-historial {
        display: flex;
        flex-direction: column;
        gap: 0.75rem;
      }
      .fila-historial {
        display: flex;
        justify-content: space-between;
        align-items: center;
        gap: 1rem;

        h4 {
          margin: 0.35rem 0 0.15rem;
          font-size: 0.95rem;
        }
        p {
          margin: 0;
          color: var(--texto-secundario);
          font-size: 0.8rem;
        }
      }
      .fila-historial__nota {
        font-family: var(--fuente-titulos);
        font-weight: 700;
        font-size: 1.1rem;
        flex-shrink: 0;
      }
      .vacio {
        color: var(--texto-secundario);
      }
    `,
  ],
})
export class Notas {
  @Input() perfilAlumnoId = '';
  historial = signal<Historial | null>(null);

  private progreso = inject(ProgresoService);
  private sesion = inject(SesionService);

  ngOnInit() {
    const id = this.perfilAlumnoId ? Number(this.perfilAlumnoId) : this.sesion.perfilActivo()?.id;
    if (!id) return;
    this.progreso.obtenerHistorial(id).subscribe((h) => this.historial.set(h));
  }

  filasHistorial(): FilaHistorial[] {
    const h = this.historial();
    if (!h) return [];
    const evaluaciones: FilaHistorial[] = h.historial.map((i: ItemHistorial) => ({
      etiqueta: i.nombre,
      detalle: i.asignatura_nombre ?? 'Examen integrado',
      nota: i.nota,
      fecha: i.fecha,
      tipo: i.tipo,
    }));
    const guias: FilaHistorial[] = h.guias_revisadas.map((g) => ({
      etiqueta: 'Guía revisada',
      detalle: `OA ${g.oa_id}`,
      nota: null,
      fecha: g.fecha,
      tipo: 'guia' as const,
    }));
    return [...evaluaciones, ...guias].sort((a, b) => (a.fecha < b.fecha ? 1 : -1));
  }

  etiquetaTipo(tipo: FilaHistorial['tipo']): string {
    if (tipo === 'prueba_unidad') return 'Prueba de unidad';
    if (tipo === 'examen_simulacro') return 'Simulacro';
    return 'Guía';
  }
}
