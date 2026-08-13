import { Component } from '@angular/core';
import { RouterLink } from '@angular/router';
import { Logo } from '../../shared/logo/logo';

@Component({
  selector: 'app-landing',
  standalone: true,
  imports: [RouterLink, Logo],
  template: `
    <div class="landing">
      <header class="landing__nav">
        <app-logo />
        <div class="landing__nav-links">
          <a routerLink="/como-funciona">Cómo funciona</a>
          <a routerLink="/preguntas-frecuentes">Preguntas frecuentes</a>
          <a routerLink="/login">Iniciar sesión</a>
          <a routerLink="/registro" class="btn btn--primario">Crear cuenta</a>
        </div>
      </header>

      <section class="landing__hero">
        <div class="landing__hero-texto">
          <span class="landing__pill">Preparación para Exámenes Libres · Mineduc</span>
          <h1>Prepárate para tu Examen Libre, con la materia completa y a tu ritmo.</h1>
          <p>
            Guías, práctica, pruebas cortas y un examen de ensayo idéntico al real —
            cubriendo exactamente el temario oficial de tu curso, de 1° básico a 4° medio.
          </p>
          <div class="landing__hero-cta">
            <a routerLink="/registro" class="btn btn--primario btn--grande">Crear cuenta gratis</a>
            <a routerLink="/login" class="btn btn--secundario btn--grande">Ya tengo cuenta</a>
          </div>
        </div>
        <div class="landing__hero-ilustracion">
          <svg viewBox="0 0 320 260" fill="none" xmlns="http://www.w3.org/2000/svg">
            <rect x="20" y="40" width="280" height="180" rx="18" fill="#EEECFD" />
            <rect x="50" y="70" width="120" height="14" rx="7" fill="#5B4FE9" />
            <rect x="50" y="96" width="90" height="10" rx="5" fill="#C9C4F7" />
            <rect x="50" y="116" width="150" height="10" rx="5" fill="#C9C4F7" />
            <circle cx="230" cy="150" r="46" fill="#FF6B4A" fill-opacity="0.15" />
            <path
              d="M210 150 L224 164 L252 132"
              stroke="#22C55E"
              stroke-width="8"
              stroke-linecap="round"
              stroke-linejoin="round"
            />
            <rect x="50" y="150" width="150" height="10" rx="5" fill="#C9C4F7" />
            <rect x="50" y="170" width="110" height="10" rx="5" fill="#C9C4F7" />
          </svg>
        </div>
      </section>

      <section class="landing__como">
        <h2>Cómo funciona</h2>
        <div class="landing__pasos">
          <div class="paso">
            <div class="paso__numero">1</div>
            <h3>Practica libre</h3>
            <p>Estudia cada tema y responde preguntas — feedback inmediato, sin presión, sin nota.</p>
          </div>
          <div class="paso">
            <div class="paso__numero">2</div>
            <h3>Pruebas por unidad</h3>
            <p>Cuando ya estudiaste, rinde una prueba corta a tu ritmo. Ahí sale tu primera nota.</p>
          </div>
          <div class="paso">
            <div class="paso__numero">3</div>
            <h3>Examen de práctica</h3>
            <p>Copia exacta del examen real — mismas preguntas, mismo tiempo. Tu mejor señal de si estás listo.</p>
          </div>
        </div>
      </section>

      <section class="landing__planes">
        <h2>Planes simples, sin letra chica</h2>
        <div class="landing__planes-grid">
          <div class="plan-card">
            <h3>Mensual</h3>
            <p class="plan-card__precio">$19.990<span>/mes</span></p>
            <p>Acceso completo a todas las asignaturas de tu curso.</p>
          </div>
          <div class="plan-card plan-card--destacado">
            <span class="plan-card__badge">Recomendado</span>
            <h3>Por periodo de examinación</h3>
            <p class="plan-card__precio">$89.900<span>pago único</span></p>
            <p>Cubre un periodo completo de examinación Mineduc (~5 meses).</p>
          </div>
          <div class="plan-card">
            <h3>Anual</h3>
            <p class="plan-card__precio">$159.900<span>pago único</span></p>
            <p>El de mejor precio por mes si ya sabes que vas a estar todo el año.</p>
          </div>
        </div>
      </section>

      <footer class="landing__footer">
        <app-logo [tamano]="24" />
        <span>Accesible para todas las familias. © Logos School.</span>
      </footer>
    </div>
  `,
  styleUrl: './landing.scss',
})
export class Landing {}
