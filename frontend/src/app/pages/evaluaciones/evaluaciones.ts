import { Component, inject, signal } from '@angular/core';
import { RouterLink } from '@angular/router';
import { forkJoin } from 'rxjs';
import { ContenidoService, AsignaturaRespuesta } from '../../core/contenido.service';
import { EvaluacionesService, ConjuntoResumen } from '../../core/evaluaciones.service';
import { SesionService } from '../../core/sesion.service';
import { estiloAsignatura } from '../../shared/estilo-asignatura';
import { IconoAsignatura } from '../../shared/icono-asignatura/icono-asignatura';

interface GrupoAsignatura {
  asignatura: AsignaturaRespuesta;
  pruebas: ConjuntoResumen[];
  examenes: ConjuntoResumen[];
}

@Component({
  selector: 'app-evaluaciones',
  standalone: true,
  imports: [RouterLink, IconoAsignatura],
  template: `
    <h1>Pruebas y Exámenes</h1>
    <p class="subtitulo">Todo lo que puedes rendir, agrupado por asignatura.</p>

    <div class="explicacion-tipos">
      <div class="explicacion-tipos__item">
        <span class="explicacion-tipos__badge explicacion-tipos__badge--prueba">Prueba de unidad</span>
        <p>Evalúa lo que ya estudiaste. Puedes rendirla las veces que quieras, sin tiempo límite — es para practicar.</p>
      </div>
      <div class="explicacion-tipos__item">
        <span class="explicacion-tipos__badge explicacion-tipos__badge--examen">Examen simulacro</span>
        <p>Imita el examen real: mismo formato, mismo tiempo. Úsalo para medir cómo te iría de verdad.</p>
      </div>
    </div>

    @if (error()) {
      <p class="error-carga">{{ error() }}</p>
    }
    @for (grupo of grupos(); track grupo.asignatura.id) {
      @if (grupo.pruebas.length || grupo.examenes.length) {
        <div class="grupo" [style.--color-asig]="colorDe(grupo.asignatura.nombre)">
          <div class="grupo__titulo">
            <app-icono-asignatura [icono]="iconoDe(grupo.asignatura.nombre)" [color]="colorDe(grupo.asignatura.nombre)" />
            <h2>{{ grupo.asignatura.nombre }}</h2>
          </div>
          <div class="grid-conjuntos">
            @for (prueba of grupo.pruebas; track prueba.id) {
              <div class="conjunto-card fila">
                <span class="conjunto-card__etiqueta">Prueba de unidad</span>
                <h3>{{ prueba.nombre }}</h3>
                <div class="conjunto-card__meta">
                  <span>📝 {{ prueba.num_preguntas }} preguntas</span>
                  <span>⏱️ sin tiempo límite</span>
                </div>
                @if (prueba.intentos_entregados > 0) {
                  <p class="conjunto-card__historial" [class.conjunto-card__historial--aprobada]="prueba.ultima_nota! >= 4">
                    {{ prueba.ultima_nota! >= 4 ? '✓' : '●' }} Última nota: {{ prueba.ultima_nota }}
                    · {{ prueba.intentos_entregados }} intento{{ prueba.intentos_entregados > 1 ? 's' : '' }}
                  </p>
                }
                <a [routerLink]="['/alumno/prueba', prueba.id]" class="conjunto-card__boton conjunto-card__boton--secundario">
                  {{ prueba.intentos_entregados > 0 ? 'Volver a rendir' : 'Rendir' }}
                </a>
              </div>
            }
            @for (examen of grupo.examenes; track examen.id) {
              <div class="conjunto-card conjunto-card--examen fila fila--examen">
                <span class="conjunto-card__etiqueta">Examen simulacro</span>
                <h3>{{ examen.nombre }}</h3>
                <div class="conjunto-card__meta">
                  <span>📝 {{ examen.num_preguntas }} preguntas</span>
                  <span>⏱️ {{ examen.tiempo_sugerido_min }} min</span>
                </div>
                @if (examen.intentos_entregados > 0) {
                  <p class="conjunto-card__historial" [class.conjunto-card__historial--aprobada]="examen.ultima_nota! >= 4">
                    {{ examen.ultima_nota! >= 4 ? '✓' : '●' }} Última nota: {{ examen.ultima_nota }}
                    · {{ examen.intentos_entregados }} intento{{ examen.intentos_entregados > 1 ? 's' : '' }}
                  </p>
                } @else {
                  <p class="conjunto-card__nota">Imita el formato del examen real</p>
                }
                <a [routerLink]="['/examen', examen.id]" class="conjunto-card__boton">
                  {{ examen.intentos_entregados > 0 ? 'Volver a rendir' : 'Comenzar examen' }}
                </a>
              </div>
            }
          </div>
        </div>
      }
    }

    @if (examenIntegrado(); as ei) {
      <div class="grupo" style="--color-asig: var(--color-primario)">
        <div class="grupo__titulo">
          <app-icono-asignatura icono="examen" color="var(--color-primario)" />
          <h2>Examen simulacro</h2>
        </div>
        <div class="grid-conjuntos">
          <div class="conjunto-card conjunto-card--examen fila fila--examen">
            <span class="conjunto-card__etiqueta">Examen integrado</span>
            <h3>{{ ei.nombre }}</h3>
            <div class="conjunto-card__meta">
              <span>📝 {{ ei.num_preguntas }} preguntas</span>
              <span>⏱️ {{ ei.tiempo_sugerido_min }} min</span>
            </div>
            @if (ei.intentos_entregados > 0) {
              <p class="conjunto-card__historial" [class.conjunto-card__historial--aprobada]="ei.ultima_nota! >= 4">
                {{ ei.ultima_nota! >= 4 ? '✓' : '●' }} Última nota: {{ ei.ultima_nota }}
                · {{ ei.intentos_entregados }} intento{{ ei.intentos_entregados > 1 ? 's' : '' }}
              </p>
            } @else {
              <p class="conjunto-card__nota">Imita el formato del examen real</p>
            }
            <a [routerLink]="['/examen', ei.id]" class="conjunto-card__boton">
              {{ ei.intentos_entregados > 0 ? 'Volver a rendir' : 'Comenzar examen' }}
            </a>
          </div>
        </div>
      </div>
    }
  `,
  styles: [
    `
      .subtitulo {
        color: var(--texto-secundario);
        margin-top: -0.5rem;
        margin-bottom: 1.5rem;
      }
      .explicacion-tipos {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
        gap: 1rem;
        margin-bottom: 2rem;
      }
      .explicacion-tipos__item {
        background: var(--fondo-tarjeta, #fff);
        border-radius: var(--radio-basica);
        box-shadow: var(--sombra-tarjeta);
        padding: 1rem 1.1rem;

        p {
          margin: 0.5rem 0 0;
          font-size: 0.85rem;
          color: var(--texto-secundario);
        }
      }
      .explicacion-tipos__badge {
        display: inline-block;
        font-size: 0.7rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.02em;
        padding: 0.25rem 0.7rem;
        border-radius: 999px;
        color: #fff;
      }
      .explicacion-tipos__badge--prueba {
        background: var(--color-primario);
      }
      .explicacion-tipos__badge--examen {
        background: var(--color-secundario-texto);
      }
      .grupo {
        margin-bottom: 2.5rem;
      }
      .grupo__titulo {
        display: flex;
        align-items: center;
        gap: 0.75rem;
        margin-bottom: 1rem;
      }
      .grupo__titulo app-icono-asignatura ::ng-deep .icono {
        width: 38px;
        height: 38px;
        font-size: 1.15rem;
      }
      .grupo__titulo h2 {
        font-size: 1.1rem;
        margin: 0;
        color: var(--color-asig);
      }
      .grid-conjuntos {
        display: grid;
        grid-template-columns: repeat(auto-fill, minmax(260px, 1fr));
        gap: 1rem;
      }
      .conjunto-card {
        display: flex;
        flex-direction: column;
        border-radius: var(--radio-basica);
        border-top: 5px solid var(--color-asig);
        background: var(--fondo-tarjeta, #fff);
        box-shadow: var(--sombra-tarjeta);
        padding: 1.1rem 1.25rem 1.25rem;
        transition: transform 0.15s, box-shadow 0.15s;
      }
      .conjunto-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 20px rgba(31, 41, 55, 0.12);
      }
      .conjunto-card__etiqueta {
        font-size: 0.7rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.03em;
        color: var(--color-asig);
      }
      .conjunto-card h3 {
        margin: 0.3rem 0 0.6rem;
        font-size: 1rem;
      }
      .conjunto-card__meta {
        display: flex;
        gap: 0.75rem;
        flex-wrap: wrap;
        font-size: 0.8rem;
        color: var(--texto-secundario);
        margin-bottom: 0.75rem;
      }
      .conjunto-card__nota {
        margin: -0.35rem 0 0.75rem;
        font-size: 0.78rem;
        color: var(--color-secundario-texto);
        font-weight: 600;
      }
      .conjunto-card__historial {
        margin: -0.35rem 0 0.75rem;
        font-size: 0.78rem;
        font-weight: 600;
        color: var(--color-error-texto);
      }
      .conjunto-card__historial--aprobada {
        color: var(--color-exito-texto);
      }
      .conjunto-card__boton {
        margin-top: auto;
        text-align: center;
        text-decoration: none;
        font-weight: 700;
        font-size: 0.9rem;
        padding: 0.55rem 1rem;
        border-radius: var(--radio-media);
        background: var(--color-asig);
        color: #fff;
      }
      .conjunto-card__boton--secundario {
        background: transparent;
        color: var(--color-asig);
        border: 1.5px solid var(--color-asig);
      }
      .error-carga {
        color: var(--color-error-texto);
      }
    `,
  ],
})
export class Evaluaciones {
  grupos = signal<GrupoAsignatura[]>([]);
  examenIntegrado = signal<ConjuntoResumen | null>(null);
  error = signal('');

  private contenido = inject(ContenidoService);
  private evaluaciones = inject(EvaluacionesService);
  private sesion = inject(SesionService);

  constructor() {
    const perfil = this.sesion.perfilActivo();
    if (!perfil) return;

    this.contenido.listarAsignaturas(perfil.nivel_id).subscribe({
      next: (asignaturas) => {
        const llamadas = asignaturas.map((a) => this.evaluaciones.listarConjuntosDeAsignatura(a.id, perfil.id));
        forkJoin(llamadas).subscribe({
          next: (listas) => {
            this.grupos.set(
              asignaturas.map((asignatura, i) => ({
                asignatura,
                pruebas: listas[i].filter((c) => c.tipo === 'prueba_unidad'),
                examenes: listas[i].filter((c) => c.tipo === 'examen_simulacro'),
              }))
            );
          },
          error: () => this.error.set('No se pudieron cargar tus pruebas y exámenes. Intenta recargar la página.'),
        });
      },
      error: () => this.error.set('No se pudieron cargar tus pruebas y exámenes. Intenta recargar la página.'),
    });

    this.evaluaciones.listarConjuntosDeNivel(perfil.nivel_id, perfil.id).subscribe({
      next: (conjuntos) => {
        if (conjuntos.length) this.examenIntegrado.set(conjuntos[0]);
      },
      error: () => this.error.set('No se pudieron cargar tus pruebas y exámenes. Intenta recargar la página.'),
    });
  }

  iconoDe(nombre: string): string {
    return estiloAsignatura(nombre).icono;
  }

  colorDe(nombre: string): string {
    return estiloAsignatura(nombre).color;
  }
}
