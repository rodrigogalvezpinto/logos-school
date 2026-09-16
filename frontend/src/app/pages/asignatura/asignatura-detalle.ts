import { Component, Input, computed, inject, signal } from '@angular/core';
import { RouterLink } from '@angular/router';
import { ContenidoService, ObjetivoRespuesta } from '../../core/contenido.service';
import { SesionService } from '../../core/sesion.service';
import { estiloAsignatura } from '../../shared/estilo-asignatura';
import { IconoAsignatura } from '../../shared/icono-asignatura/icono-asignatura';

@Component({
  selector: 'app-asignatura-detalle',
  standalone: true,
  imports: [RouterLink, IconoAsignatura],
  template: `
    <div class="cabecera" [style.background]="color()">
      <app-icono-asignatura [icono]="icono()" color="#ffffff" />
      <div>
        <h1>{{ nombreAsignatura() || 'Objetivos de Aprendizaje' }}</h1>
        <p>{{ objetivos().length }} OA en esta asignatura</p>
      </div>
    </div>

    @if (error()) {
      <p class="error-carga">{{ error() }}</p>
    }
    @if (objetivos().length > 5) {
      <input
        class="buscador"
        type="search"
        placeholder="🔍 Buscar por palabra dentro de esta asignatura…"
        [value]="busqueda()"
        (input)="busqueda.set($any($event.target).value)"
      />
    }
    <div class="lista-oa">
      @for (oa of objetivosFiltrados(); track oa.id) {
        <div class="oa-card tarjeta">
          <div class="oa-card__info">
            <span class="oa-card__codigo">{{ oa.codigo_oficial }}</span>
            <h3>{{ oa.descripcion }}</h3>
            <span class="oa-card__duracion">⏱️ ~{{ minutosDeLectura(oa.contenido_guia) }} min de lectura</span>
          </div>
          <div class="oa-card__acciones">
            <a class="btn btn--secundario" [routerLink]="['/alumno/estudiar', oa.id]">Estudiar guía</a>
            <a class="btn btn--primario" [routerLink]="['/alumno/autoevaluacion', oa.id]">Practicar</a>
          </div>
        </div>
      }
      @if (!objetivosFiltrados().length && objetivos().length) {
        <p class="vacio">No encontramos ningún objetivo que coincida con "{{ busqueda() }}".</p>
      }
    </div>

    <a class="btn btn--secundario" [routerLink]="['/alumno/evaluaciones']" [queryParams]="{ asignatura: id }">
      Ver pruebas y exámenes de esta asignatura →
    </a>
  `,
  styles: [
    `
      .cabecera {
        display: flex;
        align-items: center;
        gap: 1rem;
        margin-bottom: 2rem;
        padding: 1.5rem;
        border-radius: var(--radio-basica);
        color: #fff;

        h1 {
          margin: 0;
          color: #fff;
        }
        p {
          margin: 0.2rem 0 0;
          color: rgba(255, 255, 255, 0.85);
        }
      }
      .cabecera app-icono-asignatura ::ng-deep .icono {
        background: rgba(255, 255, 255, 0.22);
      }
      .lista-oa {
        display: flex;
        flex-direction: column;
        gap: 1rem;
        margin-bottom: 1.5rem;
      }
      .oa-card {
        display: flex;
        align-items: center;
        gap: 1.25rem;
      }
      .oa-card__info {
        flex: 1;
      }
      .oa-card__codigo {
        font-size: 0.75rem;
        font-weight: 700;
        color: var(--color-primario);
        text-transform: uppercase;
      }
      .oa-card__info h3 {
        margin: 0.2rem 0 0;
        font-size: 1.05rem;
      }
      .oa-card__duracion {
        display: block;
        margin-top: 0.35rem;
        font-size: 0.78rem;
        color: var(--texto-secundario);
      }
      .oa-card__acciones {
        display: flex;
        gap: 0.5rem;
        flex-shrink: 0;
      }
      @media (max-width: 700px) {
        .oa-card {
          flex-direction: column;
          align-items: flex-start;
        }
      }
      .error-carga {
        color: var(--color-error-texto);
      }
      .buscador {
        width: 100%;
        max-width: 420px;
        padding: 0.6rem 0.9rem;
        border: 1.5px solid var(--borde);
        border-radius: var(--radio-media);
        font-size: 0.9rem;
        margin-bottom: 1.5rem;
        background: var(--fondo-tarjeta, #fff);
        color: var(--texto-principal);
      }
      .buscador:focus {
        outline: none;
        border-color: var(--color-primario);
      }
      .vacio {
        color: var(--texto-secundario);
      }
    `,
  ],
})
export class AsignaturaDetalle {
  @Input() id = '';
  objetivos = signal<ObjetivoRespuesta[]>([]);
  nombreAsignatura = signal('');
  error = signal('');
  busqueda = signal('');

  objetivosFiltrados = computed(() => {
    const termino = this.busqueda().trim().toLowerCase();
    if (!termino) return this.objetivos();
    return this.objetivos().filter(
      (oa) => oa.descripcion.toLowerCase().includes(termino) || oa.codigo_oficial.toLowerCase().includes(termino),
    );
  });

  private contenido = inject(ContenidoService);
  private sesion = inject(SesionService);

  /** Adaptado de la duración de video que muestra Brincus junto a cada lección del
   * temario (hallazgo comparando en vivo — ver planificacion/25-analisis-competencia-
   * brincus.md) — Logos no tiene video, así que se estima el tiempo de LECTURA en su
   * lugar, a partir del propio contenido_guia que ya se descarga con la lista de OA (sin
   * pedir nada nuevo al backend). ~140 palabras/min: ritmo de lectura cómodo para el
   * rango de edad de estos cursos (más lento que el de un adulto). */
  minutosDeLectura(contenidoGuia: string): number {
    const palabras = contenidoGuia.trim().split(/\s+/).filter(Boolean).length;
    return Math.max(1, Math.round(palabras / 140));
  }

  icono(): string {
    return estiloAsignatura(this.nombreAsignatura()).icono;
  }

  color(): string {
    return estiloAsignatura(this.nombreAsignatura()).color;
  }

  ngOnInit() {
    this.contenido.listarObjetivos(Number(this.id)).subscribe({
      next: (objs) => this.objetivos.set(objs),
      error: () => this.error.set('No se pudieron cargar los objetivos de esta asignatura. Intenta recargar la página.'),
    });

    const perfil = this.sesion.perfilActivo();
    if (perfil) {
      this.contenido.listarAsignaturas(perfil.nivel_id).subscribe({
        next: (asigs) => {
          const asig = asigs.find((a) => a.id === Number(this.id));
          if (asig) this.nombreAsignatura.set(asig.nombre);
        },
      });
    }
  }
}
