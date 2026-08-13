import { Component, inject, signal } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { Logo } from '../../shared/logo/logo';
import { AuthService, PlanRespuesta } from '../../core/auth.service';

@Component({
  selector: 'app-seleccion-plan',
  standalone: true,
  imports: [Logo],
  template: `
    <div class="pagina">
      <div class="pagina__logo"><app-logo /></div>
      <h1>Elige el plan para {{ nombreAlumno }}</h1>
      <p class="pagina__subtitulo">
        Prueba <strong>7 días completamente gratis</strong> — no se te cobra nada hoy, y puedes cambiar de
        plan cuando quieras.
      </p>

      <div class="planes">
        <button class="plan" [class.plan--activo]="planElegido === 'Mensual'" (click)="planElegido = 'Mensual'">
          <h3>Mensual</h3>
          <p class="plan__precio">{{ precioDe('Mensual') }}<span>/mes</span></p>
          <p class="plan__desc">Acceso completo, cancela cuando quieras.</p>
        </button>
        <button
          class="plan plan--destacado"
          [class.plan--activo]="planElegido === 'Por periodo de examinación'"
          (click)="planElegido = 'Por periodo de examinación'"
        >
          <span class="plan__badge">Recomendado</span>
          <h3>Por periodo de examinación</h3>
          <p class="plan__precio">{{ precioDe('Por periodo de examinación') }}<span>pago único</span></p>
          <p class="plan__desc">~5 meses de cobertura, ideal si ya sabes cuándo rinde.</p>
        </button>
        <button class="plan" [class.plan--activo]="planElegido === 'Anual'" (click)="planElegido = 'Anual'">
          <h3>Anual</h3>
          <p class="plan__precio">{{ precioDe('Anual') }}<span>pago único</span></p>
          <p class="plan__desc">El mejor precio por mes.</p>
        </button>
      </div>

      @if (error()) {
        <p class="error">{{ error() }}</p>
      }
      <button class="btn btn--primario btn--grande" [disabled]="cargando()" (click)="continuar()">
        {{ cargando() ? 'Activando…' : 'Comenzar mis 7 días gratis' }}
      </button>
      <p class="pagina__nota">Sin tarjeta de crédito. Te avisaremos antes de que termine tu prueba.</p>
    </div>
  `,
  styles: [
    `
      .pagina {
        max-width: 780px;
        margin: 0 auto;
        padding: 3rem 2rem;
        text-align: center;
      }
      .pagina__logo {
        display: flex;
        justify-content: center;
        margin-bottom: 2rem;
      }
      h1 {
        font-size: 1.7rem;
      }
      .pagina__subtitulo {
        color: var(--texto-secundario);
        margin-bottom: 2.5rem;
        max-width: 480px;
        margin-left: auto;
        margin-right: auto;

        strong {
          color: var(--color-primario);
        }
      }
      .planes {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 1.25rem;
        margin-bottom: 1.5rem;
      }
      .plan {
        position: relative;
        background: var(--fondo-tarjeta);
        border: 2px solid var(--borde);
        border-radius: var(--radio-basica);
        padding: 1.75rem 1.25rem;
        text-align: left;
        cursor: pointer;
        font-family: var(--fuente-texto);
      }
      .plan--activo {
        border-color: var(--color-primario);
        box-shadow: var(--sombra-tarjeta);
      }
      .plan__badge {
        position: absolute;
        top: -12px;
        right: 1.25rem;
        background: var(--color-primario);
        color: white;
        font-size: 0.7rem;
        font-weight: 600;
        padding: 0.25rem 0.6rem;
        border-radius: 999px;
      }
      .plan h3 {
        margin-bottom: 0.4rem;
      }
      .plan__precio {
        font-family: var(--fuente-titulos);
        font-size: 1.6rem;
        font-weight: 700;
        color: var(--color-primario);
        margin: 0.4rem 0;

        span {
          font-size: 0.85rem;
          color: var(--texto-secundario);
          font-weight: 500;
        }
      }
      .plan__desc {
        color: var(--texto-secundario);
        font-size: 0.85rem;
        margin: 0;
      }
      .pagina__nota {
        margin-top: 0.75rem;
        color: var(--texto-secundario);
        font-size: 0.85rem;
      }
      .error {
        color: var(--color-error);
        font-size: 0.9rem;
        margin-bottom: 1rem;
      }
      @media (max-width: 700px) {
        .planes {
          grid-template-columns: 1fr;
        }
      }
    `,
  ],
})
export class SeleccionPlan {
  planElegido = 'Por periodo de examinación';
  nombreAlumno = 'tu alumno';
  perfilAlumnoId: number | null = null;
  planes = signal<PlanRespuesta[]>([]);
  cargando = signal(false);
  error = signal('');

  private auth = inject(AuthService);

  constructor(private router: Router, private ruta: ActivatedRoute) {
    const nombre = this.ruta.snapshot.queryParamMap.get('nombre');
    if (nombre) this.nombreAlumno = nombre;
    const perfilId = this.ruta.snapshot.queryParamMap.get('perfilId');
    if (perfilId) this.perfilAlumnoId = Number(perfilId);
    this.auth.listarPlanes().subscribe((planes) => this.planes.set(planes));
  }

  precioDe(nombre: string): string {
    const plan = this.planes().find((p) => p.nombre === nombre);
    return plan ? `$${plan.precio_clp.toLocaleString('es-CL')}` : '—';
  }

  continuar() {
    // Sin perfilAlumnoId (ej. entrando desde "Plan y Pagos" del sidebar sin venir de
    // agregar-alumno) no hay a quién activarle la prueba — solo navega.
    if (!this.perfilAlumnoId) {
      this.router.navigate(['/selector-perfil']);
      return;
    }
    const plan = this.planes().find((p) => p.nombre === this.planElegido);
    if (!plan) {
      this.error.set('No se pudo cargar el plan elegido. Intenta de nuevo.');
      return;
    }
    this.error.set('');
    this.cargando.set(true);
    this.auth.iniciarPruebaGratis(this.perfilAlumnoId, plan.id).subscribe({
      next: () => this.router.navigate(['/selector-perfil']),
      error: () => {
        this.cargando.set(false);
        this.error.set('No se pudo activar tu prueba gratis. Intenta de nuevo.');
      },
    });
  }
}
