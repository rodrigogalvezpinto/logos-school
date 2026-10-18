import { Component, inject, signal } from '@angular/core';
import { NavigationEnd, Router, RouterLink } from '@angular/router';
import { filter } from 'rxjs';

/** Botón de ayuda contextual (Fase 1 del plan de incorporación de hallazgos de Brincus —
 * ver planificacion/27-plan-incorporacion-hallazgos-brincus.md). Sin IA todavía (eso queda
 * para una fase posterior con Profesor Virtual) — acá es un tip corto según la página en la
 * que está el usuario, más un link a Preguntas Frecuentes. Se prefirió esto por sobre un
 * botón "Contactar soporte" con un correo, porque Logos School todavía no tiene un canal de
 * soporte real operando — un mailto: que nadie revisa sería peor que no ofrecer nada. */

interface TipContextual {
  patron: RegExp;
  texto: string;
}

const TIPS: TipContextual[] = [
  { patron: /\/alumno\/asignaturas\/\d+/, texto: 'Cada objetivo tiene una guía con explicación y ejemplos. Márcalo como revisado cuando lo entiendas — así se habilitan las pruebas de esa unidad.' },
  { patron: /\/alumno\/asignaturas$/, texto: 'Elige una asignatura para ver sus objetivos de aprendizaje y estudiar guía por guía.' },
  { patron: /\/alumno\/evaluaciones/, texto: 'Prueba de unidad: sin tiempo límite, para practicar. Examen simulacro: imita el examen real, con tiempo — úsalo para medir cómo te iría de verdad.' },
  { patron: /\/alumno\/plan-estudio/, texto: 'Tu plan reparte el contenido pendiente en sesiones según los días que elegiste. También puedes agregar repaso de un curso anterior al final del plan.' },
  { patron: /\/alumno\/notas/, texto: 'Acá ves tu nota de práctica (promedio de pruebas de unidad) y tu resultado de simulacro por asignatura — y puedes descargar un informe en PDF.' },
  { patron: /\/alumno\/logros/, texto: 'Ganas XP al revisar guías y rendir evaluaciones. Las insignias se desbloquean por hábito de estudio: racha de días seguidos, contenido revisado y evaluaciones entregadas.' },
  { patron: /\/alumno\/inicio/, texto: 'Este es tu panel: accesos directos a lo que te toca hoy según tu plan de estudio, y a todas tus asignaturas.' },
  { patron: /\/apoderado/, texto: 'Desde acá ves el avance de cada alumno vinculado a tu cuenta: notas, plan de estudio y suscripción.' },
];

const TIP_GENERICO = 'Explora tus asignaturas, rinde pruebas de unidad para practicar sin tiempo límite, y usa los exámenes simulacro cuando quieras medir cómo te iría en el examen real.';

@Component({
  selector: 'app-ayuda-contextual',
  standalone: true,
  imports: [RouterLink],
  template: `
    <div class="ayuda-contextual">
      @if (abierto()) {
        <div class="ayuda-contextual__panel">
          <div class="ayuda-contextual__cabecera">
            <h3>¿Necesitas ayuda?</h3>
            <button type="button" class="ayuda-contextual__cerrar" (click)="abierto.set(false)" aria-label="Cerrar ayuda">✕</button>
          </div>
          <p>{{ tip() }}</p>
          <a routerLink="/preguntas-frecuentes" target="_blank" class="ayuda-contextual__link">Ver todas las preguntas frecuentes ↗</a>
        </div>
      }
      <button
        type="button"
        class="ayuda-contextual__boton"
        (click)="abierto.set(!abierto())"
        [attr.aria-expanded]="abierto()"
        aria-label="Abrir ayuda"
      >
        ?
      </button>
    </div>
  `,
  styles: [
    `
      .ayuda-contextual {
        position: fixed;
        right: 1.5rem;
        bottom: 1.5rem;
        z-index: 100;
      }
      .ayuda-contextual__boton {
        width: 48px;
        height: 48px;
        border-radius: 50%;
        border: none;
        background: var(--color-primario);
        color: white;
        font-size: 1.3rem;
        font-weight: 700;
        cursor: pointer;
        box-shadow: 0 4px 14px rgba(0, 0, 0, 0.2);
      }
      .ayuda-contextual__boton:hover {
        filter: brightness(1.08);
      }
      .ayuda-contextual__panel {
        position: absolute;
        right: 0;
        bottom: calc(100% + 0.75rem);
        width: 280px;
        background: var(--fondo-tarjeta, #fff);
        border-radius: var(--radio-basica);
        box-shadow: var(--sombra-tarjeta);
        padding: 1rem 1.1rem;
      }
      .ayuda-contextual__cabecera {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 0.5rem;
      }
      .ayuda-contextual__cabecera h3 {
        margin: 0;
        font-size: 0.95rem;
      }
      .ayuda-contextual__cerrar {
        background: none;
        border: none;
        cursor: pointer;
        color: var(--texto-secundario);
        font-size: 0.9rem;
        padding: 0.2rem;
      }
      .ayuda-contextual__panel p {
        margin: 0 0 0.75rem;
        font-size: 0.85rem;
        color: var(--texto-principal);
        line-height: 1.4;
      }
      .ayuda-contextual__link {
        font-size: 0.8rem;
        font-weight: 600;
        color: var(--color-primario);
        text-decoration: none;
      }
      .ayuda-contextual__link:hover {
        text-decoration: underline;
      }
    `,
  ],
})
export class AyudaContextual {
  abierto = signal(false);
  private urlActual = signal('');

  private router = inject(Router);

  constructor() {
    this.urlActual.set(this.router.url);
    this.router.events.pipe(filter((e) => e instanceof NavigationEnd)).subscribe((e) => {
      this.urlActual.set((e as NavigationEnd).urlAfterRedirects);
      this.abierto.set(false);
    });
  }

  tip(): string {
    const url = this.urlActual();
    return TIPS.find((t) => t.patron.test(url))?.texto ?? TIP_GENERICO;
  }
}
