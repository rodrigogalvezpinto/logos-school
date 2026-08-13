import { Component, inject, signal } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { ContenidoService } from '../../core/contenido.service';
import { PlanDeEstudio, PlanEstudioService } from '../../core/plan-estudio.service';
import { SesionService } from '../../core/sesion.service';

const DIAS: { valor: string; etiqueta: string }[] = [
  { valor: 'lunes', etiqueta: 'Lun' },
  { valor: 'martes', etiqueta: 'Mar' },
  { valor: 'miercoles', etiqueta: 'Mié' },
  { valor: 'jueves', etiqueta: 'Jue' },
  { valor: 'viernes', etiqueta: 'Vie' },
  { valor: 'sabado', etiqueta: 'Sáb' },
  { valor: 'domingo', etiqueta: 'Dom' },
];

@Component({
  selector: 'app-plan-estudio',
  standalone: true,
  imports: [FormsModule],
  template: `
    <h1>Plan de Estudio</h1>

    @if (cargando()) {
      <p>Cargando…</p>
    } @else if (plan(); as p) {
      @if (sesionHoy(); as hoy) {
        <div class="tarjeta banner-hoy">
          <span class="banner-hoy__etiqueta">Hoy te toca</span>
          <h2>{{ nombreAsignatura(hoy.asignatura_id) }}</h2>
          <p>{{ hoy.oa_ids.length }} objetivo{{ hoy.oa_ids.length > 1 ? 's' : '' }} · ~{{ hoy.minutos_estimados }} min</p>
        </div>
      }

      <h2>Próximas sesiones</h2>
      <div class="lista-sesiones">
        @for (s of proximasSesiones(); track s.id) {
          <div class="tarjeta fila-sesion" [class.fila-sesion--cumplida]="s.cumplida">
            <div>
              <span class="fecha">{{ s.fecha_programada }}</span>
              <h3>{{ nombreAsignatura(s.asignatura_id) }}</h3>
              <p>{{ s.oa_ids.length }} objetivo{{ s.oa_ids.length > 1 ? 's' : '' }} · ~{{ s.minutos_estimados }} min</p>
            </div>
            <span class="chip" [class.chip--cumplida]="s.cumplida">{{ s.cumplida ? 'Cumplida' : 'Pendiente' }}</span>
          </div>
        }
        @if (!proximasSesiones().length) {
          <p class="vacio">¡Completaste todas las sesiones programadas!</p>
        }
      </div>
    } @else {
      <p class="subtitulo">Todavía no tienes un plan de estudio. Elige tus días y te armamos un horario.</p>
      <form class="tarjeta form-crear" (submit)="$event.preventDefault(); crear()">
        <div class="campo">
          <label>¿Qué días vas a estudiar? (mínimo 3)</label>
          <div class="dias">
            @for (dia of dias; track dia.valor) {
              <button
                type="button"
                class="dia-chip"
                [class.dia-chip--activo]="diasElegidos.has(dia.valor)"
                (click)="toggleDia(dia.valor)"
              >
                {{ dia.etiqueta }}
              </button>
            }
          </div>
        </div>
        <div class="campo">
          <label>Fecha del examen (si la sabes — opcional)</label>
          <input type="date" [(ngModel)]="fechaObjetivo" name="fechaObjetivo" />
        </div>
        @if (error()) {
          <p class="error">{{ error() }}</p>
        }
        <button type="submit" class="btn btn--primario">Crear mi plan de estudio</button>
      </form>
    }
  `,
  styles: [
    `
      .subtitulo {
        color: var(--texto-secundario);
        margin-bottom: 1.5rem;
      }
      .banner-hoy {
        background: var(--color-primario);
        color: white;
        margin-bottom: 2rem;
      }
      .banner-hoy__etiqueta {
        font-size: 0.75rem;
        font-weight: 700;
        text-transform: uppercase;
        opacity: 0.85;
      }
      .banner-hoy h2 {
        margin: 0.3rem 0 0.2rem;
        color: white;
      }
      .banner-hoy p {
        margin: 0;
        opacity: 0.9;
      }
      h2 {
        font-size: 1.05rem;
        margin-bottom: 0.75rem;
      }
      .lista-sesiones {
        display: flex;
        flex-direction: column;
        gap: 0.75rem;
      }
      .fila-sesion {
        display: flex;
        justify-content: space-between;
        align-items: center;
      }
      .fila-sesion--cumplida {
        opacity: 0.6;
      }
      .fecha {
        font-size: 0.75rem;
        color: var(--texto-secundario);
      }
      .fila-sesion h3 {
        margin: 0.2rem 0 0.15rem;
        font-size: 0.95rem;
      }
      .fila-sesion p {
        margin: 0;
        color: var(--texto-secundario);
        font-size: 0.8rem;
      }
      .chip {
        display: inline-block;
        font-size: 0.75rem;
        font-weight: 600;
        padding: 0.2rem 0.6rem;
        border-radius: 999px;
        background: var(--color-alerta-suave);
        color: var(--color-alerta);
      }
      .chip--cumplida {
        background: var(--color-exito-suave);
        color: var(--color-exito);
      }
      .vacio {
        color: var(--texto-secundario);
      }
      .form-crear {
        max-width: 420px;
      }
      .dias {
        display: flex;
        gap: 0.4rem;
      }
      .dia-chip {
        flex: 1;
        padding: 0.5rem 0;
        border: 1.5px solid var(--borde);
        border-radius: var(--radio-media);
        background: var(--fondo-tarjeta);
        color: var(--texto-secundario);
        font-size: 0.8rem;
        font-weight: 600;
        cursor: pointer;
      }
      .dia-chip--activo {
        border-color: var(--color-primario);
        background: var(--color-primario-suave);
        color: var(--color-primario);
      }
      .error {
        color: var(--color-error);
        font-size: 0.85rem;
      }
    `,
  ],
})
export class PlanEstudio {
  plan = signal<PlanDeEstudio | null>(null);
  cargando = signal(true);
  asignaturas = signal<Record<number, string>>({});
  dias = DIAS;
  diasElegidos = new Set<string>(['lunes', 'miercoles', 'viernes']);
  fechaObjetivo = '';
  error = signal('');

  private planEstudioService = inject(PlanEstudioService);
  private contenido = inject(ContenidoService);
  private sesion = inject(SesionService);

  constructor() {
    const perfil = this.sesion.perfilActivo();
    if (!perfil) return;

    this.contenido.listarAsignaturas(perfil.nivel_id).subscribe((asigs) => {
      this.asignaturas.set(Object.fromEntries(asigs.map((a) => [a.id, a.nombre])));
    });

    this.planEstudioService.obtenerPlan(perfil.id).subscribe({
      next: (p) => {
        this.plan.set(p);
        this.cargando.set(false);
      },
      error: () => this.cargando.set(false),
    });
  }

  nombreAsignatura(id: number): string {
    return this.asignaturas()[id] || 'Asignatura';
  }

  sesionHoy() {
    const hoy = new Date().toISOString().slice(0, 10);
    return this.plan()?.sesiones.find((s) => s.fecha_programada === hoy && !s.cumplida) || null;
  }

  proximasSesiones() {
    return (this.plan()?.sesiones || []).filter((s) => !s.cumplida);
  }

  toggleDia(dia: string) {
    if (this.diasElegidos.has(dia)) {
      this.diasElegidos.delete(dia);
    } else {
      this.diasElegidos.add(dia);
    }
  }

  crear() {
    this.error.set('');
    const perfil = this.sesion.perfilActivo();
    if (!perfil) return;
    if (this.diasElegidos.size < 3) {
      this.error.set('Elige al menos 3 días de estudio a la semana.');
      return;
    }
    const diasElegidos = Array.from(this.diasElegidos);
    this.planEstudioService
      .crearPlan(perfil.id, diasElegidos.length, diasElegidos, this.fechaObjetivo || null)
      .subscribe({
        next: (p) => this.plan.set(p),
        error: () => this.error.set('No se pudo crear el plan de estudio.'),
      });
  }
}
