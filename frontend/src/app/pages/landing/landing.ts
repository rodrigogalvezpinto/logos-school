import { Component } from '@angular/core';
import { RouterLink } from '@angular/router';
import { Logo } from '../../shared/logo/logo';

// Contenido de estudio 100% completo para los 12 niveles (ver contenido/00-estado-contenido.md)
// — lista estática porque refleja completitud de contenido, no el avance de importación a la
// base de datos (que se hace curso por curso, ver planificacion/22-analisis-de-brechas.md).
const NIVELES = [
  '1° básico', '2° básico', '3° básico', '4° básico',
  '5° básico', '6° básico', '7° básico', '8° básico',
  '1° medio', '2° medio', '3° medio', '4° medio',
];

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

      <section class="landing__diferenciadores">
        <h2>Qué mirar al elegir cómo preparar tu examen libre</h2>
        <div class="landing__diferenciadores-grid">
          <div class="diferenciador">
            <span class="diferenciador__icono">📘</span>
            <h3>100% alineado al temario oficial</h3>
            <p>
              Cada guía y cada pregunta viene de los 12 temarios UCE/Mineduc reales — no material
              genérico. Cubrimos los 3 formatos de examen oficiales, de 1° básico a 4° medio.
            </p>
          </div>
          <div class="diferenciador">
            <span class="diferenciador__icono">💸</span>
            <h3>Gratis o de muy bajo costo</h3>
            <p>
              El contenido de estudio (guías, práctica, pruebas y exámenes de ensayo) es y
              seguirá siendo gratuito. Sin publicidad dirigida a menores, nunca.
            </p>
          </div>
          <div class="diferenciador">
            <span class="diferenciador__icono">🗓️</span>
            <h3>A tu ritmo, con horario si lo necesitas</h3>
            <p>
              Estudia libremente o arma un plan de estudio con la frecuencia que elijas —
              la plataforma reparte lo que falta en sesiones concretas hasta tu examen.
            </p>
          </div>
          <div class="diferenciador">
            <span class="diferenciador__icono">📊</span>
            <h3>Sabes si estás realmente preparado</h3>
            <p>
              Notas por asignatura, historial completo y un examen de práctica idéntico al real
              — no adivinas cómo te va a ir, lo verificas antes del día del examen.
            </p>
          </div>
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

      <section class="landing__niveles">
        <h2>Cubrimos los 12 niveles, de 1° básico a 4° medio</h2>
        <p class="landing__niveles-sub">
          408 Objetivos de Aprendizaje oficiales, con guía, banco de preguntas, pruebas de
          unidad y examen de ensayo — completo en cada uno.
        </p>
        <div class="landing__niveles-grid">
          @for (nivel of niveles; track nivel) {
            <span class="nivel-chip">{{ nivel }}</span>
          }
        </div>
      </section>

      <section class="landing__modos">
        <h2>Dos formas de estudiar en Logos</h2>
        <div class="landing__modos-grid">
          <div class="modo-card">
            <h3>Autoestudio</h3>
            <p>
              Tú eliges tu curso, estudias cuando quieras y avanzas a tu ritmo. Es la forma más
              simple de empezar — sin depender de nadie más.
            </p>
          </div>
          <div class="modo-card">
            <h3>Con un profesor</h3>
            <p>
              Si tu profesor te agrega a un Curso/Sección, además ves su progreso agregado y
              recibe comunicados suyos — el acompañamiento se suma, nunca reemplaza el
              autoestudio.
            </p>
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
export class Landing {
  niveles = NIVELES;
}
