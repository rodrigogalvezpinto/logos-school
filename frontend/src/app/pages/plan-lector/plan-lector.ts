import { Component, inject, signal } from '@angular/core';
import { LibroPlanLector, PlanLectorService } from '../../core/plan-lector.service';
import { SesionService } from '../../core/sesion.service';

@Component({
  selector: 'app-plan-lector',
  standalone: true,
  template: `
    <h1>Plan Lector</h1>
    <p class="subtitulo">Una selección de libros recomendados para tu nivel — para leer a tu ritmo, fuera de las guías de Lenguaje.</p>

    @if (libros().length) {
      <div class="grid-libros">
        @for (libro of libros(); track libro.id) {
          <div class="libro-card">
            <div class="libro-card__portada">📖</div>
            <div class="libro-card__info">
              <h3>{{ libro.titulo }}</h3>
              <p class="libro-card__autor">{{ libro.autor }}</p>
              <p class="libro-card__editorial">{{ libro.editorial }}</p>
            </div>
          </div>
        }
      </div>
    } @else if (error()) {
      <p class="error-carga">{{ error() }}</p>
    } @else if (cargando()) {
      <p>Cargando…</p>
    } @else {
      <p class="vacio">Todavía no hay un Plan Lector armado para tu nivel.</p>
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
      .grid-libros {
        display: grid;
        grid-template-columns: repeat(auto-fill, minmax(240px, 1fr));
        gap: 1.25rem;
      }
      .libro-card {
        display: flex;
        gap: 1rem;
        background: var(--fondo-tarjeta, #fff);
        box-shadow: var(--sombra-tarjeta);
        border-radius: var(--radio-basica);
        padding: 1.1rem;
      }
      .libro-card__portada {
        flex-shrink: 0;
        width: 56px;
        height: 72px;
        border-radius: var(--radio-media);
        background: var(--color-primario-suave);
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.6rem;
      }
      .libro-card__info h3 {
        margin: 0 0 0.25rem;
        font-size: 1rem;
      }
      .libro-card__autor {
        margin: 0;
        font-size: 0.85rem;
        color: var(--texto-principal);
        font-weight: 600;
      }
      .libro-card__editorial {
        margin: 0.15rem 0 0;
        font-size: 0.78rem;
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
export class PlanLector {
  libros = signal<LibroPlanLector[]>([]);
  cargando = signal(true);
  error = signal('');

  private planLector = inject(PlanLectorService);
  private sesion = inject(SesionService);

  ngOnInit() {
    const perfil = this.sesion.perfilActivo();
    if (!perfil) return;
    this.planLector.listarPorNivel(perfil.nivel_id).subscribe({
      next: (libros) => {
        this.libros.set(libros);
        this.cargando.set(false);
      },
      error: () => {
        this.error.set('No se pudo cargar el Plan Lector. Intenta recargar la página.');
        this.cargando.set(false);
      },
    });
  }
}
