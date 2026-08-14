import { Component, Input, inject, signal } from '@angular/core';
import { Router } from '@angular/router';
import { Faltantes, ItemHistorial, Historial, ProgresoService } from '../../core/progreso.service';
import { EvaluacionesService } from '../../core/evaluaciones.service';
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
      <h2>Notas por asignatura</h2>
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

      @if (faltantes(); as f) {
        <h2>Pruebas y exámenes faltantes</h2>
        <div class="lista-historial faltantes">
          @for (item of f.faltantes; track item.conjunto_id) {
            <div class="tarjeta fila-historial" [class.fila-historial--bloqueada]="!item.habilitado">
              <div>
                <span class="chip" [class.chip--practica]="item.tipo === 'prueba_unidad'" [class.chip--simulacro]="item.tipo === 'examen_simulacro'">
                  {{ item.tipo === 'prueba_unidad' ? 'Prueba de unidad' : 'Simulacro' }}
                </span>
                <h3>{{ item.nombre }}</h3>
                @if (!item.habilitado) {
                  <p>Se habilita al completar las guías pendientes de esa unidad.</p>
                }
              </div>
              @if (!item.habilitado) {
                <span class="chip">Bloqueada</span>
              }
            </div>
          }
          @if (!f.faltantes.length) {
            <p class="vacio">¡Ya rendiste todo lo disponible!</p>
          }
        </div>

        @for (c of f.coberturas; track c.asignatura_id) {
          @if (c.simulacro_parcial_disponible) {
            <div class="tarjeta aviso-simulacro-parcial">
              <div>
                <h3>Simulacro parcial disponible — {{ c.asignatura_nombre }}</h3>
                <p>Cubres {{ c.cobertura_pct }}% del temario. Puedes rendir un simulacro acotado a lo que ya estudiaste.</p>
              </div>
              <button class="btn btn--primario" (click)="rendirSimulacroParcial(c.asignatura_id)">Rendir simulacro parcial</button>
            </div>
          }
        }
      }

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
              <h3>{{ fila.etiqueta }}</h3>
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
        color: var(--color-secundario-texto);
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

        h3 {
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
      .faltantes {
        margin-bottom: 2rem;
      }
      .fila-historial--bloqueada {
        opacity: 0.8;
      }
      .aviso-simulacro-parcial {
        display: flex;
        justify-content: space-between;
        align-items: center;
        gap: 1rem;
        border: 1.5px solid var(--color-primario);
        margin-bottom: 1.5rem;

        h3 {
          margin: 0 0 0.2rem;
        }
        p {
          margin: 0;
          color: var(--texto-secundario);
          font-size: 0.85rem;
        }
      }
    `,
  ],
})
export class Notas {
  @Input() perfilAlumnoId = '';
  historial = signal<Historial | null>(null);
  faltantes = signal<Faltantes | null>(null);

  private progreso = inject(ProgresoService);
  private evaluaciones = inject(EvaluacionesService);
  private sesion = inject(SesionService);
  private router = inject(Router);

  ngOnInit() {
    const perfilActivo = this.sesion.perfilActivo();
    const id = this.perfilAlumnoId ? Number(this.perfilAlumnoId) : perfilActivo?.id;
    if (!id) return;
    this.progreso.obtenerHistorial(id).subscribe((h) => this.historial.set(h));

    // La sección de faltantes/simulacro parcial es una acción que solo el propio alumno
    // puede iniciar (necesita rendir la prueba) — no se muestra en la vista del apoderado,
    // que no tiene un `perfilActivo` (nivel_id) propio para esta consulta.
    if (!this.perfilAlumnoId && perfilActivo) {
      this.progreso.obtenerFaltantes(id, perfilActivo.nivel_id).subscribe((f) => this.faltantes.set(f));
    }
  }

  rendirSimulacroParcial(asignaturaId: number) {
    const perfil = this.sesion.perfilActivo();
    if (!perfil) return;
    this.evaluaciones.generarSimulacroParcial(asignaturaId, perfil.id).subscribe((intento) => {
      this.router.navigate(['/examen', intento.conjunto_evaluacion_id]);
    });
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
      detalle: `${g.asignatura_nombre} — ${g.codigo_oficial}`,
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
