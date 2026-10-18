import { Component, inject, signal } from '@angular/core';
import { RouterLink } from '@angular/router';
import { AuthService } from '../../core/auth.service';
import { BienestarService } from '../../core/bienestar.service';
import { ContenidoService, AsignaturaRespuesta } from '../../core/contenido.service';
import { CursoSeccionService, MiCurso } from '../../core/curso-seccion.service';
import { OnboardingService, ProgresoOnboarding } from '../../core/onboarding.service';
import { SesionService } from '../../core/sesion.service';
import { estiloAsignatura } from '../../shared/estilo-asignatura';
import { IconoAsignatura } from '../../shared/icono-asignatura/icono-asignatura';

/** Fase 1, ítem 2.4 — check-in emocional diario (ver
 * planificacion/27-plan-incorporacion-hallazgos-brincus.md). Mismos 7 estados que
 * verificó el análisis de Brincus. */
const ESTADOS_ANIMO_EMOJI: Record<string, string> = {
  feliz: '😄',
  tranquilo: '🙂',
  normal: '😐',
  cansado: '😴',
  preocupado: '😟',
  triste: '😢',
  frustrado: '😤',
};
const ETIQUETA_ANIMO: Record<string, string> = {
  feliz: 'Feliz',
  tranquilo: 'Tranquilo',
  normal: 'Normal',
  cansado: 'Cansado',
  preocupado: 'Preocupado',
  triste: 'Triste',
  frustrado: 'Frustrado',
};

/** Adaptado de los 7 pasos que verificó el análisis de Brincus a lo que Logos sí tiene
 * hoy en Fase 1 — ver planificacion/27-plan-incorporacion-hallazgos-brincus.md, ítem 2.3. */
const PASOS_INFO: Record<string, { etiqueta: string; ruta: string }> = {
  ver_guia: { etiqueta: 'Revisa una guía de estudio', ruta: '/alumno/asignaturas' },
  autoevaluacion: { etiqueta: 'Responde una autoevaluación', ruta: '/alumno/asignaturas' },
  plan_estudio: { etiqueta: 'Revisa tu Plan de Estudio', ruta: '/alumno/plan-estudio' },
  elegir_avatar: { etiqueta: 'Elige tu avatar en Mis Logros', ruta: '/alumno/logros' },
};

@Component({
  selector: 'app-alumno-inicio',
  standalone: true,
  imports: [RouterLink, IconoAsignatura],
  template: `
    <h1>¡Hola de nuevo, {{ nombreAlumno() }}! 👋</h1>
    <p class="subtitulo">Sigamos avanzando en tu preparación.</p>

    @if (diasRestantesPrueba(); as dias) {
      <div class="aviso-prueba" [class.aviso-prueba--urgente]="dias <= 2">
        ⏳ Tu prueba gratuita {{ dias === 0 ? 'termina hoy' : dias === 1 ? 'termina mañana' : 'termina en ' + dias + ' días' }}
        <a routerLink="/seleccion-plan">Elegir un plan →</a>
      </div>
    }

    @if (mostrarCheckIn()) {
      <div class="modal-fondo">
        <div class="tarjeta checkin">
          <h3>¿Cómo te sientes hoy?</h3>
          <p>Esto nos ayuda a acompañarte mejor en tu camino.</p>
          <div class="checkin__opciones">
            @for (estado of estadosAnimo(); track estado) {
              <button class="checkin__opcion" (click)="registrarAnimo(estado)">
                <span class="checkin__emoji">{{ emojiAnimo(estado) }}</span>
                <span>{{ etiquetaAnimo(estado) }}</span>
              </button>
            }
          </div>
        </div>
      </div>
    }

    @if (onboarding(); as o) {
      @if (!o.completo) {
        <div class="tarjeta onboarding">
          <span class="onboarding__etiqueta">Primeros pasos</span>
          <h3>Conoce Logos School</h3>
          <ul class="onboarding__lista">
            @for (paso of o.pasos; track paso) {
              <li [class.onboarding__paso--hecho]="o.pasos_completados.includes(paso)">
                <a [routerLink]="infoPaso(paso).ruta">
                  <span class="onboarding__check">{{ o.pasos_completados.includes(paso) ? '✓' : '○' }}</span>
                  {{ infoPaso(paso).etiqueta }}
                </a>
              </li>
            }
          </ul>
        </div>
      }
    }

    @if (miCurso(); as curso) {
      <div class="tarjeta mi-curso">
        <span class="mi-curso__etiqueta">Mi Curso</span>
        <h3>{{ curso.nombre_curso }}</h3>
        <p>Profesor: {{ curso.nombre_profesor }}</p>
        @if (curso.comunicados.length) {
          <div class="mi-curso__comunicados">
            @for (c of curso.comunicados.slice(0, 3); track c.id) {
              <div class="comunicado">
                <strong>{{ c.titulo }}</strong>
                <p>{{ c.cuerpo }}</p>
              </div>
            }
          </div>
        }
      </div>
    }

    <h2 class="seccion-titulo">Tus asignaturas</h2>
    @if (error()) {
      <p class="error-carga">{{ error() }}</p>
    }
    <div class="grid-asignaturas">
      @for (asig of asignaturas(); track asig.id) {
        <a class="asignatura-card tarjeta" [routerLink]="['/alumno/asignaturas', asig.id]">
          <app-icono-asignatura [icono]="iconoPara(asig.nombre)" [color]="colorPara(asig.nombre)" />
          <div class="asignatura-card__info">
            <h3>{{ asig.nombre }}</h3>
          </div>
        </a>
      }
    </div>
  `,
  styles: [
    `
      .subtitulo {
        color: var(--texto-secundario);
        margin-top: -0.5rem;
        margin-bottom: 2rem;
      }
      .aviso-prueba {
        display: flex;
        align-items: center;
        gap: 0.75rem;
        flex-wrap: wrap;
        background: var(--color-secundario-suave);
        color: var(--color-secundario-texto);
        border-radius: var(--radio-media);
        padding: 0.7rem 1.1rem;
        font-size: 0.9rem;
        font-weight: 600;
        margin-bottom: 1.5rem;
      }
      .aviso-prueba--urgente {
        background: var(--color-error-suave);
        color: var(--color-error-texto);
      }
      .aviso-prueba a {
        color: inherit;
        text-decoration: underline;
        font-weight: 700;
      }
      .modal-fondo {
        position: fixed;
        inset: 0;
        background: rgba(20, 19, 43, 0.55);
        display: flex;
        align-items: center;
        justify-content: center;
        z-index: 100;
      }
      .checkin {
        max-width: 420px;
        text-align: center;
      }
      .checkin h3 {
        margin: 0 0 0.35rem;
      }
      .checkin p {
        color: var(--texto-secundario);
        font-size: 0.9rem;
        margin: 0 0 1.25rem;
      }
      .checkin__opciones {
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 0.5rem;
      }
      .checkin__opcion {
        display: flex;
        flex-direction: column;
        align-items: center;
        gap: 0.25rem;
        border: 1.5px solid var(--borde);
        border-radius: var(--radio-media);
        background: var(--fondo-tarjeta);
        padding: 0.6rem 0.25rem;
        cursor: pointer;
        font-size: 0.7rem;
        color: var(--texto-secundario);
      }
      .checkin__opcion:hover {
        border-color: var(--color-primario);
        background: var(--color-primario-suave);
      }
      .checkin__emoji {
        font-size: 1.5rem;
      }
      /* Degradado de marca (índigo + coral) — mismo criterio ya aplicado al selector de
         perfil (ver planificacion/27-plan-incorporacion-hallazgos-brincus.md): hallazgo
         comparando en vivo contra Brincus, que da mucha más energía visual a este momento
         de "primeros pasos" que una tarjeta blanca con borde. Paleta propia, no la de
         Brincus. */
      .onboarding {
        margin-bottom: 2rem;
        max-width: 480px;
        background: linear-gradient(135deg, var(--color-primario) 0%, var(--color-primario-oscuro) 55%, var(--color-secundario) 100%);
        border: none;
      }
      .onboarding__etiqueta {
        font-size: 0.7rem;
        font-weight: 700;
        text-transform: uppercase;
        color: rgba(255, 255, 255, 0.85);
      }
      .onboarding h3 {
        margin: 0.3rem 0 0.75rem;
        color: #fff;
      }
      .onboarding__lista {
        list-style: none;
        margin: 0;
        padding: 0;
        display: flex;
        flex-direction: column;
        gap: 0.5rem;
      }
      .onboarding__lista a {
        display: flex;
        align-items: center;
        gap: 0.6rem;
        text-decoration: none;
        color: #fff;
        font-size: 0.9rem;
        background: rgba(255, 255, 255, 0.14);
        border-radius: var(--radio-media);
        padding: 0.5rem 0.75rem;
      }
      .onboarding__check {
        color: #fff;
        font-weight: 700;
      }
      .onboarding__paso--hecho a {
        color: rgba(255, 255, 255, 0.65);
        text-decoration: line-through;
        background: rgba(255, 255, 255, 0.06);
      }
      .onboarding__paso--hecho .onboarding__check {
        color: #7CF7B0;
      }
      .mi-curso {
        margin-bottom: 2rem;
        max-width: 480px;
      }
      .mi-curso__etiqueta {
        font-size: 0.7rem;
        font-weight: 700;
        text-transform: uppercase;
        color: var(--color-primario);
      }
      .mi-curso h3 {
        margin: 0.3rem 0 0.15rem;
      }
      .mi-curso p {
        margin: 0;
        color: var(--texto-secundario);
        font-size: 0.85rem;
      }
      .mi-curso__comunicados {
        margin-top: 0.75rem;
        display: flex;
        flex-direction: column;
        gap: 0.5rem;
      }
      .comunicado {
        border-top: 1px solid var(--borde);
        padding-top: 0.5rem;
      }
      .comunicado strong {
        font-size: 0.85rem;
      }
      .comunicado p {
        margin: 0.15rem 0 0;
        font-size: 0.8rem;
      }
      .seccion-titulo {
        font-size: 1.2rem;
        margin-bottom: 1rem;
      }
      .grid-asignaturas {
        display: grid;
        grid-template-columns: repeat(2, 1fr);
        gap: 1rem;
      }
      .asignatura-card {
        display: flex;
        gap: 1rem;
        align-items: center;
        text-decoration: none;
        color: inherit;
        transition: transform 0.15s;
      }
      .asignatura-card:hover {
        transform: translateY(-2px);
      }
      .asignatura-card h3 {
        font-size: 1rem;
        margin: 0;
      }
      @media (max-width: 700px) {
        .grid-asignaturas {
          grid-template-columns: 1fr;
        }
      }
      .error-carga {
        color: var(--color-error-texto);
      }
    `,
  ],
})
export class AlumnoInicio {
  asignaturas = signal<AsignaturaRespuesta[]>([]);
  miCurso = signal<MiCurso | null>(null);
  onboarding = signal<ProgresoOnboarding | null>(null);
  mostrarCheckIn = signal(false);
  estadosAnimo = signal<string[]>([]);
  diasRestantesPrueba = signal<number | null>(null);
  error = signal('');

  private auth = inject(AuthService);
  private contenido = inject(ContenidoService);
  private cursoSeccion = inject(CursoSeccionService);
  private onboardingService = inject(OnboardingService);
  private bienestar = inject(BienestarService);
  private sesion = inject(SesionService);

  constructor() {
    const perfil = this.sesion.perfilActivo();
    if (perfil) {
      this.contenido.listarAsignaturas(perfil.nivel_id).subscribe({
        next: (asigs) => this.asignaturas.set(asigs),
        error: () => this.error.set('No se pudieron cargar tus asignaturas. Intenta recargar la página.'),
      });
      // Autoestudio puro (sin curso asignado) es el caso normal — el backend devuelve
      // null y esta sección simplemente no se muestra. Si la llamada falla, se trata
      // igual que "sin curso" (sección secundaria, no bloquea la página del alumno).
      this.cursoSeccion.obtenerMiCurso(perfil.id).subscribe({
        next: (curso) => this.miCurso.set(curso),
        error: () => this.miCurso.set(null),
      });
      this.onboardingService.obtenerProgreso(perfil.id).subscribe({
        next: (o) => this.onboarding.set(o),
        error: () => {}, // sección secundaria, no bloquea la página del alumno
      });
      this.bienestar.obtenerAnimoDeHoy(perfil.id).subscribe({
        next: (a) => {
          this.estadosAnimo.set(a.estados_disponibles);
          this.mostrarCheckIn.set(!a.registrado);
        },
        error: () => {}, // sección secundaria, no bloquea la página del alumno
      });
      // Countdown de prueba gratuita (hallazgo comparando en vivo contra Brincus, que lo
      // muestra fijo bajo el avatar en todo momento — ver
      // planificacion/27-plan-incorporacion-hallazgos-brincus.md) — sección secundaria, no
      // bloquea la página si falla o si el alumno no está en prueba gratuita.
      this.auth.obtenerSuscripcion(perfil.id).subscribe({
        next: (s) => {
          if (!s || s.origen !== 'prueba_gratis' || s.estado !== 'activa' || !s.fecha_termino) return;
          const msRestantes = new Date(s.fecha_termino).getTime() - Date.now();
          const dias = Math.ceil(msRestantes / (1000 * 60 * 60 * 24));
          if (dias >= 0) this.diasRestantesPrueba.set(dias);
        },
        error: () => {},
      });
    }
  }

  infoPaso(paso: string): { etiqueta: string; ruta: string } {
    return PASOS_INFO[paso] || { etiqueta: paso, ruta: '/alumno/inicio' };
  }

  emojiAnimo(estado: string): string {
    return ESTADOS_ANIMO_EMOJI[estado] || '🙂';
  }

  etiquetaAnimo(estado: string): string {
    return ETIQUETA_ANIMO[estado] || estado;
  }

  registrarAnimo(estado: string) {
    const perfil = this.sesion.perfilActivo();
    if (!perfil) return;
    this.bienestar.registrarAnimo(perfil.id, estado).subscribe(() => this.mostrarCheckIn.set(false));
  }

  nombreAlumno(): string {
    return this.sesion.perfilActivo()?.nombre || '';
  }

  iconoPara(nombre: string): string {
    return estiloAsignatura(nombre).icono;
  }

  colorPara(nombre: string): string {
    return estiloAsignatura(nombre).color;
  }
}
