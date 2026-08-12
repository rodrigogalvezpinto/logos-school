import { Component } from '@angular/core';
import { Router } from '@angular/router';
import { Logo } from '../../shared/logo/logo';

@Component({
  selector: 'app-seleccion-plan',
  standalone: true,
  imports: [Logo],
  template: `
    <div class="pagina">
      <div class="pagina__logo"><app-logo /></div>
      <h1>Elige el plan para Sofía</h1>
      <p class="pagina__subtitulo">Puedes cambiar de plan cuando quieras.</p>

      <div class="planes">
        <button class="plan" [class.plan--activo]="planElegido === 'mensual'" (click)="planElegido = 'mensual'">
          <h3>Mensual</h3>
          <p class="plan__precio">$19.990<span>/mes</span></p>
          <p class="plan__desc">Acceso completo, cancela cuando quieras.</p>
        </button>
        <button
          class="plan plan--destacado"
          [class.plan--activo]="planElegido === 'periodo'"
          (click)="planElegido = 'periodo'"
        >
          <span class="plan__badge">Recomendado</span>
          <h3>Por periodo de examinación</h3>
          <p class="plan__precio">$89.900<span>pago único</span></p>
          <p class="plan__desc">~5 meses de cobertura, ideal si ya sabes cuándo rinde.</p>
        </button>
        <button class="plan" [class.plan--activo]="planElegido === 'anual'" (click)="planElegido = 'anual'">
          <h3>Anual</h3>
          <p class="plan__precio">$159.900<span>pago único</span></p>
          <p class="plan__desc">El mejor precio por mes.</p>
        </button>
      </div>

      <button class="btn btn--primario btn--grande" (click)="continuar()">Continuar al pago</button>
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
      }
      .planes {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 1.25rem;
        margin-bottom: 2.5rem;
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
      @media (max-width: 700px) {
        .planes {
          grid-template-columns: 1fr;
        }
      }
    `,
  ],
})
export class SeleccionPlan {
  planElegido: 'mensual' | 'periodo' | 'anual' = 'periodo';

  constructor(private router: Router) {}

  continuar() {
    this.router.navigate(['/selector-perfil']);
  }
}
