import { Component, inject, signal } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { AsignaturaRespuesta, ContenidoService, NivelRespuesta, ObjetivoRespuesta } from '../../core/contenido.service';
import { OnboardingService } from '../../core/onboarding.service';
import { PlanDeEstudio, PlanEstudioService, SesionEstudio } from '../../core/plan-estudio.service';
import { SesionService } from '../../core/sesion.service';
import { estiloAsignatura } from '../../shared/estilo-asignatura';
import { IconoAsignatura } from '../../shared/icono-asignatura/icono-asignatura';

type VistaPlan = 'lista' | 'semanal' | 'mensual';

interface GrupoSesiones {
  etiqueta: string;
  sesiones: SesionEstudio[];
}

/** Lunes de la semana ISO a la que pertenece `fechaISO` (YYYY-MM-DD), como string
 * YYYY-MM-DD — clave estable para agrupar sin depender de zona horaria del navegador. */
function lunesDeLaSemana(fechaISO: string): string {
  const [anio, mes, dia] = fechaISO.split('-').map(Number);
  const fecha = new Date(Date.UTC(anio, mes - 1, dia));
  const diaSemana = fecha.getUTCDay() || 7; // domingo=0 -> 7
  fecha.setUTCDate(fecha.getUTCDate() - diaSemana + 1);
  return fecha.toISOString().slice(0, 10);
}

const NOMBRES_MES = [
  'enero', 'febrero', 'marzo', 'abril', 'mayo', 'junio',
  'julio', 'agosto', 'septiembre', 'octubre', 'noviembre', 'diciembre',
];

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
  imports: [FormsModule, IconoAsignatura],
  template: `
    <h1>Plan de Estudio</h1>

    @if (cargando()) {
      <p>Cargando…</p>
    } @else if (plan(); as p) {
      @if (sesionHoy(); as hoy) {
        <div class="banner-hoy" [style.background]="gradienteDe(hoy.asignatura_id)">
          <app-icono-asignatura [icono]="iconoDe(hoy.asignatura_id)" color="#ffffff" />
          <div>
            <span class="banner-hoy__etiqueta">Hoy te toca</span>
            <h2>{{ nombreAsignatura(hoy.asignatura_id) }}</h2>
            <p>{{ hoy.oa_ids.length }} objetivo{{ hoy.oa_ids.length > 1 ? 's' : '' }} · ~{{ hoy.minutos_estimados }} min</p>
          </div>
        </div>
      }

      <div class="cabecera-sesiones">
        <h2>Próximas sesiones</h2>
        <div class="selector-vista">
          @for (v of vistas; track v.valor) {
            <button
              type="button"
              class="selector-vista__opcion"
              [class.selector-vista__opcion--activa]="vista() === v.valor"
              (click)="vista.set(v.valor)"
            >
              {{ v.etiqueta }}
            </button>
          }
        </div>
      </div>

      @if (vista() === 'lista') {
        <div class="lista-sesiones">
          @for (s of proximasSesiones(); track s.id) {
            <div class="fila-sesion" [class.fila-sesion--cumplida]="s.cumplida" [style.--color-asig]="colorDe(s.asignatura_id)">
              <app-icono-asignatura [icono]="iconoDe(s.asignatura_id)" [color]="colorDe(s.asignatura_id)" />
              <div class="fila-sesion__info">
                <span class="fecha">{{ s.fecha_programada }}</span>
                @if (s.es_repaso) {
                  <span class="chip-repaso">📚 Repaso</span>
                }
                <h3>{{ nombreAsignatura(s.asignatura_id) }}</h3>
                <p>{{ s.oa_ids.length }} objetivo{{ s.oa_ids.length > 1 ? 's' : '' }} · ~{{ s.minutos_estimados }} min</p>
              </div>
              <span class="chip" [class.chip--cumplida]="s.cumplida" [class.chip--atrasada]="s.atrasada">{{ etiquetaEstado(s) }}</span>
            </div>
          }
          @if (!proximasSesiones().length) {
            <p class="vacio">¡Completaste todas las sesiones programadas!</p>
          }
        </div>
      } @else {
        <div class="lista-grupos">
          @for (grupo of gruposDeSesiones(); track grupo.etiqueta) {
            <div class="grupo-semana">
              <h3 class="grupo-semana__titulo">{{ grupo.etiqueta }}</h3>
              <div class="lista-sesiones">
                @for (s of grupo.sesiones; track s.id) {
                  <div class="fila-sesion" [class.fila-sesion--cumplida]="s.cumplida" [style.--color-asig]="colorDe(s.asignatura_id)">
                    <app-icono-asignatura [icono]="iconoDe(s.asignatura_id)" [color]="colorDe(s.asignatura_id)" />
                    <div class="fila-sesion__info">
                      <span class="fecha">{{ s.fecha_programada }}</span>
                @if (s.es_repaso) {
                  <span class="chip-repaso">📚 Repaso</span>
                }
                      <h3>{{ nombreAsignatura(s.asignatura_id) }}</h3>
                      <p>{{ s.oa_ids.length }} objetivo{{ s.oa_ids.length > 1 ? 's' : '' }} · ~{{ s.minutos_estimados }} min</p>
                    </div>
                    <span class="chip" [class.chip--cumplida]="s.cumplida" [class.chip--atrasada]="s.atrasada">{{ etiquetaEstado(s) }}</span>
                  </div>
                }
              </div>
            </div>
          }
          @if (!gruposDeSesiones().length) {
            <p class="vacio">¡Completaste todas las sesiones programadas!</p>
          }
        </div>
      }

      <div class="repaso">
        <button type="button" class="btn btn--secundario" (click)="mostrarRepaso.set(!mostrarRepaso())">
          {{ mostrarRepaso() ? '✕ Cerrar' : '📚 Repasar contenido de años anteriores' }}
        </button>

        @if (mostrarRepaso()) {
          <div class="tarjeta form-repaso">
            <p class="form-repaso__ayuda">
              Agrega una sesión de repaso de un curso que ya cursaste — se agenda al final de tu plan actual, sin
              tocar el resto.
            </p>
            <div class="campo">
              <label>¿Qué curso quieres repasar?</label>
              <select [(ngModel)]="nivelRepasoId" name="nivelRepaso" (ngModelChange)="alElegirNivelRepaso($event)">
                <option [ngValue]="null">Elige un curso anterior…</option>
                @for (n of nivelesAnteriores(); track n.id) {
                  <option [ngValue]="n.id">{{ n.nombre }}</option>
                }
              </select>
            </div>
            @if (asignaturasRepaso().length) {
              <div class="campo">
                <label>Asignatura</label>
                <select [(ngModel)]="asignaturaRepasoId" name="asignaturaRepaso" (ngModelChange)="alElegirAsignaturaRepaso($event)">
                  <option [ngValue]="null">Elige una asignatura…</option>
                  @for (a of asignaturasRepaso(); track a.id) {
                    <option [ngValue]="a.id">{{ a.nombre }}</option>
                  }
                </select>
              </div>
            }
            @if (objetivosRepaso().length) {
              <div class="campo">
                <label>¿Qué objetivos quieres repasar?</label>
                <div class="lista-oa-repaso">
                  @for (oa of objetivosRepaso(); track oa.id) {
                    <label class="oa-repaso-opcion">
                      <input
                        type="checkbox"
                        [checked]="oaRepasoElegidos().has(oa.id)"
                        (change)="toggleOaRepaso(oa.id)"
                      />
                      {{ oa.descripcion }}
                    </label>
                  }
                </div>
              </div>
            }
            @if (errorRepaso()) {
              <p class="error">{{ errorRepaso() }}</p>
            }
            <button
              type="button"
              class="btn btn--primario"
              [disabled]="!oaRepasoElegidos().size"
              (click)="agregarRepaso()"
            >
              Agregar al plan
            </button>
          </div>
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
        display: flex;
        align-items: center;
        gap: 1.25rem;
        color: white;
        margin-bottom: 2rem;
        padding: 1.5rem;
        border-radius: var(--radio-basica);
        box-shadow: var(--sombra-tarjeta);
      }
      .banner-hoy ::ng-deep .icono {
        background: rgba(255, 255, 255, 0.22);
        width: 52px;
        height: 52px;
        flex-shrink: 0;
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
      .cabecera-sesiones {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 0.75rem;

        h2 {
          margin-bottom: 0;
        }
      }
      .selector-vista {
        display: flex;
        gap: 0.3rem;
      }
      .selector-vista__opcion {
        padding: 0.35rem 0.75rem;
        border: 1.5px solid var(--borde);
        border-radius: var(--radio-media);
        background: var(--fondo-tarjeta);
        color: var(--texto-secundario);
        font-size: 0.8rem;
        font-weight: 600;
        cursor: pointer;
      }
      .selector-vista__opcion--activa {
        border-color: var(--color-primario);
        background: var(--color-primario-suave);
        color: var(--color-primario);
      }
      .lista-grupos {
        display: flex;
        flex-direction: column;
        gap: 1.5rem;
      }
      .grupo-semana__titulo {
        font-size: 0.85rem;
        color: var(--texto-secundario);
        margin-bottom: 0.6rem;
        padding-bottom: 0.3rem;
        border-bottom: 1px solid var(--borde);
      }
      .lista-sesiones {
        display: flex;
        flex-direction: column;
        gap: 0.75rem;
      }
      .fila-sesion {
        display: flex;
        align-items: center;
        gap: 1rem;
        background: var(--fondo-tarjeta, #fff);
        box-shadow: var(--sombra-tarjeta);
        border-radius: var(--radio-basica);
        border-left: 4px solid var(--color-asig, var(--color-primario));
        padding: 0.85rem 1.1rem;
      }
      .fila-sesion__info {
        flex: 1;
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
        color: var(--color-alerta-texto);
      }
      .chip--cumplida {
        background: var(--color-exito-suave);
        color: var(--color-exito-texto);
      }
      .chip--atrasada {
        background: var(--color-error-suave);
        color: var(--color-error-texto);
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
        color: var(--color-error-texto);
        font-size: 0.85rem;
      }
      .chip-repaso {
        display: inline-block;
        margin-left: 0.5rem;
        font-size: 0.7rem;
        font-weight: 700;
        padding: 0.1rem 0.5rem;
        border-radius: 999px;
        background: var(--color-primario-suave);
        color: var(--color-primario);
      }
      .repaso {
        margin-top: 2rem;
      }
      .form-repaso {
        max-width: 460px;
        margin-top: 1rem;
      }
      .form-repaso__ayuda {
        margin: 0 0 1rem;
        font-size: 0.85rem;
        color: var(--texto-secundario);
      }
      .form-repaso .campo {
        margin-bottom: 1rem;
      }
      .form-repaso .campo label {
        display: block;
        margin-bottom: 0.3rem;
        font-size: 0.85rem;
        font-weight: 600;
      }
      .form-repaso select {
        width: 100%;
        padding: 0.55rem 0.75rem;
        border: 1.5px solid var(--borde);
        border-radius: var(--radio-media);
        background: var(--fondo-tarjeta, #fff);
        color: var(--texto-principal);
        font-size: 0.9rem;
      }
      .lista-oa-repaso {
        display: flex;
        flex-direction: column;
        gap: 0.5rem;
        max-height: 220px;
        overflow-y: auto;
      }
      .oa-repaso-opcion {
        display: flex;
        align-items: flex-start;
        gap: 0.5rem;
        font-size: 0.85rem;
        cursor: pointer;
      }
    `,
  ],
})
export class PlanEstudio {
  plan = signal<PlanDeEstudio | null>(null);
  cargando = signal(true);
  asignaturas = signal<Record<number, string>>({});
  vista = signal<VistaPlan>('lista');
  vistas: { valor: VistaPlan; etiqueta: string }[] = [
    { valor: 'lista', etiqueta: 'Lista' },
    { valor: 'semanal', etiqueta: 'Semanal' },
    { valor: 'mensual', etiqueta: 'Mensual' },
  ];
  dias = DIAS;
  diasElegidos = new Set<string>(['lunes', 'miercoles', 'viernes']);
  fechaObjetivo = '';
  error = signal('');

  // Repaso de contenido de un nivel anterior (hallazgo comparando en vivo contra Brincus
  // — ver planificacion/25-analisis-competencia-brincus.md).
  mostrarRepaso = signal(false);
  nivelesAnteriores = signal<NivelRespuesta[]>([]);
  nivelRepasoId: number | null = null;
  asignaturasRepaso = signal<AsignaturaRespuesta[]>([]);
  asignaturaRepasoId: number | null = null;
  objetivosRepaso = signal<ObjetivoRespuesta[]>([]);
  oaRepasoElegidos = signal<Set<number>>(new Set());
  errorRepaso = signal('');

  private planEstudioService = inject(PlanEstudioService);
  private contenido = inject(ContenidoService);
  private onboarding = inject(OnboardingService);
  private sesion = inject(SesionService);

  constructor() {
    const perfil = this.sesion.perfilActivo();
    if (!perfil) return;

    this.contenido.listarAsignaturas(perfil.nivel_id).subscribe((asigs) => {
      this.asignaturas.set(Object.fromEntries(asigs.map((a) => [a.id, a.nombre])));
    });
    this.onboarding.completarPaso(perfil.id, 'plan_estudio').subscribe();

    this.planEstudioService.obtenerPlan(perfil.id).subscribe({
      next: (p) => {
        this.plan.set(p);
        this.cargando.set(false);
      },
      error: () => this.cargando.set(false),
    });

    // Se filtra por `orden` (posición curricular real: 1=1° básico...12=4° medio), NUNCA
    // por `id` — el id no sigue el orden curricular (ver Nivel.orden en orm_models.py,
    // bug real encontrado con 4° básico, el piloto, importado primero).
    this.contenido.listarNiveles().subscribe((niveles) => {
      const propio = niveles.find((n) => n.id === perfil.nivel_id);
      if (!propio || propio.orden === null) return;
      this.nivelesAnteriores.set(
        niveles.filter((n) => n.orden !== null && n.orden < propio.orden!).sort((a, b) => a.orden! - b.orden!),
      );
    });
  }

  nombreAsignatura(id: number): string {
    return this.asignaturas()[id] || 'Asignatura';
  }

  iconoDe(id: number): string {
    return estiloAsignatura(this.nombreAsignatura(id)).icono;
  }

  colorDe(id: number): string {
    return estiloAsignatura(this.nombreAsignatura(id)).color;
  }

  gradienteDe(id: number): string {
    const color = this.colorDe(id);
    return `linear-gradient(135deg, ${color}, ${color}dd)`;
  }

  etiquetaEstado(s: SesionEstudio): string {
    if (s.cumplida) return 'Cumplida';
    if (s.atrasada) return 'Atrasada';
    return 'Pendiente';
  }

  sesionHoy() {
    const hoy = new Date().toISOString().slice(0, 10);
    return this.plan()?.sesiones.find((s) => s.fecha_programada === hoy && !s.cumplida) || null;
  }

  proximasSesiones() {
    return (this.plan()?.sesiones || []).filter((s) => !s.cumplida);
  }

  /** Agrupa las mismas sesiones de `proximasSesiones()` por semana o por mes — es una
   * mejora de UI sobre datos que ya existen, no un cambio de modelo (Fase 1, ítem 2.10,
   * ver planificacion/27-plan-incorporacion-hallazgos-brincus.md). */
  gruposDeSesiones(): GrupoSesiones[] {
    const sesiones = this.proximasSesiones();
    const porClave = new Map<string, SesionEstudio[]>();

    for (const s of sesiones) {
      const clave = this.vista() === 'semanal' ? lunesDeLaSemana(s.fecha_programada) : s.fecha_programada.slice(0, 7);
      if (!porClave.has(clave)) porClave.set(clave, []);
      porClave.get(clave)!.push(s);
    }

    return Array.from(porClave.entries())
      .sort(([a], [b]) => (a < b ? -1 : 1))
      .map(([clave, sesionesDelGrupo]) => ({
        etiqueta: this.vista() === 'semanal' ? this.etiquetaSemana(clave) : this.etiquetaMes(clave),
        sesiones: sesionesDelGrupo,
      }));
  }

  private etiquetaSemana(lunes: string): string {
    const [anio, mes, dia] = lunes.split('-').map(Number);
    const inicio = new Date(Date.UTC(anio, mes - 1, dia));
    const fin = new Date(Date.UTC(anio, mes - 1, dia + 6));
    const fmt = (f: Date) => `${f.getUTCDate()} de ${NOMBRES_MES[f.getUTCMonth()]}`;
    return `Semana del ${fmt(inicio)} al ${fmt(fin)}`;
  }

  private etiquetaMes(anioMes: string): string {
    const [anio, mes] = anioMes.split('-').map(Number);
    return `${NOMBRES_MES[mes - 1]} ${anio}`;
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

  alElegirNivelRepaso(nivelId: number | null) {
    this.asignaturaRepasoId = null;
    this.asignaturasRepaso.set([]);
    this.objetivosRepaso.set([]);
    this.oaRepasoElegidos.set(new Set());
    if (nivelId === null) return;
    this.contenido.listarAsignaturas(nivelId).subscribe((asigs) => this.asignaturasRepaso.set(asigs));
  }

  alElegirAsignaturaRepaso(asignaturaId: number | null) {
    this.objetivosRepaso.set([]);
    this.oaRepasoElegidos.set(new Set());
    if (asignaturaId === null) return;
    this.contenido.listarObjetivos(asignaturaId).subscribe((objetivos) => this.objetivosRepaso.set(objetivos));
  }

  toggleOaRepaso(oaId: number) {
    this.oaRepasoElegidos.update((set) => {
      const nuevo = new Set(set);
      nuevo.has(oaId) ? nuevo.delete(oaId) : nuevo.add(oaId);
      return nuevo;
    });
  }

  agregarRepaso() {
    this.errorRepaso.set('');
    const perfil = this.sesion.perfilActivo();
    if (!perfil || !this.asignaturaRepasoId || !this.oaRepasoElegidos().size) return;

    this.planEstudioService
      .agregarRepaso(perfil.id, this.asignaturaRepasoId, Array.from(this.oaRepasoElegidos()))
      .subscribe({
        next: () => {
          // La asignatura del repaso es de otro nivel — hay que sumarla al mapa de
          // nombres para que `nombreAsignatura()` la resuelva en la lista de sesiones.
          const asigRepasada = this.asignaturasRepaso().find((a) => a.id === this.asignaturaRepasoId);
          if (asigRepasada) {
            this.asignaturas.update((mapa) => ({ ...mapa, [asigRepasada.id]: asigRepasada.nombre }));
          }
          this.planEstudioService.obtenerPlan(perfil.id).subscribe((p) => this.plan.set(p));
          this.mostrarRepaso.set(false);
          this.nivelRepasoId = null;
          this.asignaturaRepasoId = null;
          this.asignaturasRepaso.set([]);
          this.objetivosRepaso.set([]);
          this.oaRepasoElegidos.set(new Set());
        },
        error: () => this.errorRepaso.set('No se pudo agregar el repaso. Intenta de nuevo.'),
      });
  }
}
