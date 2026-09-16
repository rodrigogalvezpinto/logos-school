import { Component, inject, signal } from '@angular/core';
import { GamificacionService, PerfilGamificacion } from '../../core/gamificacion.service';
import { OnboardingService } from '../../core/onboarding.service';
import { PrediccionService, SemanaJardin } from '../../core/prediccion.service';
import { SesionService } from '../../core/sesion.service';
import { PlantaJardin } from '../../shared/planta-jardin/planta-jardin';

/** Emoji simple por avatar — sin arte propio en Fase 1 (ver
 * planificacion/27-plan-incorporacion-hallazgos-brincus.md, ítem 2.2: MVP deliberadamente
 * simple, sin el sistema de "avatares evolucionables bloqueados por nivel" de Brincus). */
const EMOJI_POR_AVATAR: Record<string, string> = {
  monstruo_azul: '🔵',
  monstruo_verde: '🟢',
  monstruo_morado: '🟣',
  monstruo_celeste: '🩵',
  monstruo_rojo: '🔴',
  huevo_espacial: '🥚',
  planeta: '🪐',
  cohete: '🚀',
};

/** Color base por avatar, para el fondo tipo "esfera/gema" con degradado — hallazgo
 * comparando en vivo contra Brincus (cuarta pasada, ver
 * planificacion/27-plan-incorporacion-hallazgos-brincus.md): sus avatares usan formas con
 * degradados metálicos, no círculos de color plano. Acá se logra un salto de calidad
 * visual real con solo CSS (radial-gradient + sombra interna), sin encargar arte gráfico
 * externo — mismo criterio de "cero dependencias, cero licencias" ya aplicado con emoji. */
const COLOR_POR_AVATAR: Record<string, string> = {
  monstruo_azul: '#3B82F6',
  monstruo_verde: '#22C55E',
  monstruo_morado: '#A855F7',
  monstruo_celeste: '#06B6D4',
  monstruo_rojo: '#EF4444',
  huevo_espacial: '#F59E0B',
  planeta: '#5B4FE9',
  cohete: '#FF6B4A',
};

@Component({
  selector: 'app-logros',
  standalone: true,
  imports: [PlantaJardin],
  template: `
    <h1>Mis Logros</h1>
    <p class="subtitulo">Gana XP estudiando y rindiendo pruebas, y sube de nivel.</p>

    @if (perfil(); as p) {
      <div class="resumen">
        <div class="resumen__avatar" [style.background]="esferaAvatar(p.avatar_id)">{{ emoji(p.avatar_id) }}</div>
        <div class="resumen__datos">
          <p class="resumen__nivel">Nivel {{ p.nivel }}</p>
          <p class="resumen__xp">⚡ {{ p.xp }} XP total</p>
          <div class="resumen__barra">
            <div
              class="resumen__barra-relleno"
              [style.width.%]="progresoNivelPct(p)"
            ></div>
          </div>
          <p class="resumen__faltante">Te faltan {{ p.xp_para_siguiente_nivel }} XP para el nivel {{ p.nivel + 1 }} 🚀</p>
        </div>
        @if (p.racha_dias_actual > 0) {
          <div class="resumen__racha">
            <span class="resumen__racha-num">🔥 {{ p.racha_dias_actual }}</span>
            <span class="resumen__racha-etiqueta">{{ p.racha_dias_actual === 1 ? 'día seguido' : 'días seguidos' }}</span>
          </div>
        }
      </div>

      @if (jardin(); as semanas) {
        <h2>Tu jardín</h2>
        <p class="subtitulo subtitulo--chica">Idea propia de Logos School — cada semana suma una plantita, según cuántos días estudiaste. Nunca se marchita, aunque una semana te haya costado más.</p>
        <div class="tarjeta jardin">
          <app-planta-jardin [etapa]="semanas[semanas.length - 1].etapa" tamano="grande" />
          <div class="jardin__historial">
            @for (semana of semanas; track semana.semana_inicio) {
              <app-planta-jardin [etapa]="semana.etapa" tamano="mini" />
            }
          </div>
        </div>
      }

      <h2>Mis insignias</h2>
      <p class="subtitulo subtitulo--chica">{{ logrosDesbloqueados() }} de {{ p.logros.length }} conseguidas</p>
      <div class="grilla-logros">
        @for (logro of p.logros; track logro.id) {
          <div class="logro-card" [class.logro-card--bloqueado]="!logro.desbloqueado" [title]="logro.descripcion">
            <span class="logro-card__icono">{{ logro.icono }}</span>
            <p class="logro-card__nombre">{{ logro.nombre }}</p>
            @if (!logro.desbloqueado) {
              <span class="logro-card__candado">🔒</span>
            }
          </div>
        }
      </div>

      <h2>Elige tu avatar</h2>
      <div class="grilla-avatares">
        @for (a of p.avatares_disponibles; track a) {
          <button
            class="avatar-opcion"
            [class.avatar-opcion--elegido]="a === p.avatar_id"
            (click)="elegirAvatar(a)"
          >
            <span class="avatar-opcion__emoji" [style.background]="esferaAvatar(a)">{{ emoji(a) }}</span>
            @if (a === p.avatar_id) {
              <span class="avatar-opcion__check">✓</span>
            }
          </button>
        }
      </div>

      <h2>Cómo ganar XP</h2>
      <div class="grilla-xp">
        <div class="tarjeta-xp">
          <span class="tarjeta-xp__icono">📝</span>
          <div>
            <p class="tarjeta-xp__valor">+5 XP</p>
            <p class="tarjeta-xp__desc">Por cada prueba o examen que entregues (la primera vez).</p>
          </div>
        </div>
        <div class="tarjeta-xp">
          <span class="tarjeta-xp__icono">📖</span>
          <div>
            <p class="tarjeta-xp__valor">+2 XP</p>
            <p class="tarjeta-xp__desc">Por cada guía que revises por primera vez.</p>
          </div>
        </div>
      </div>

      <h2>¿Sabías que…?</h2>
      <ul class="datos-curiosos">
        <li>Tu racha más larga fue de <strong>{{ p.racha_dias_maxima }}</strong> día{{ p.racha_dias_maxima === 1 ? '' : 's' }} seguido{{ p.racha_dias_maxima === 1 ? '' : 's' }}.</li>
        <li>Has dedicado <strong>{{ tiempoLegible(p.tiempo_evaluando_total_seg) }}</strong> a rendir pruebas y exámenes.</li>
        <li>Has entregado <strong>{{ p.evaluaciones_entregadas_total }}</strong> evaluacion{{ p.evaluaciones_entregadas_total === 1 ? '' : 'es' }}.</li>
        <li>Has revisado <strong>{{ p.guias_revisadas_total }}</strong> guía{{ p.guias_revisadas_total === 1 ? '' : 's' }} de estudio.</li>
      </ul>
    } @else if (error()) {
      <p class="error-carga">{{ error() }}</p>
    } @else {
      <p>Cargando…</p>
    }
  `,
  styles: [
    `
      .subtitulo {
        color: var(--texto-secundario);
        margin-top: -0.5rem;
        margin-bottom: 2rem;
      }
      .resumen {
        display: flex;
        align-items: center;
        gap: 1.5rem;
        margin-bottom: 2rem;
        padding: 1.5rem;
        border-radius: var(--radio-basica);
        background: linear-gradient(135deg, var(--color-primario), var(--color-primario-oscuro));
        box-shadow: var(--sombra-tarjeta);
      }
      .resumen__avatar {
        font-size: 3.5rem;
        line-height: 1;
        width: 88px;
        height: 88px;
        flex-shrink: 0;
        border-radius: 50%;
        border: 3px solid rgba(255, 255, 255, 0.55);
        box-shadow: inset -6px -6px 14px rgba(0, 0, 0, 0.2), inset 4px 4px 10px rgba(255, 255, 255, 0.35), 0 4px 10px rgba(0, 0, 0, 0.15);
        display: flex;
        align-items: center;
        justify-content: center;
      }
      .resumen__datos {
        flex: 1;
      }
      .resumen__nivel {
        font-family: var(--fuente-titulos);
        font-weight: 700;
        font-size: 1.4rem;
        margin: 0;
        color: #fff;
      }
      .resumen__xp {
        color: rgba(255, 255, 255, 0.85);
        margin: 0.15rem 0 0.75rem;
        font-weight: 600;
      }
      .resumen__barra {
        height: 10px;
        border-radius: 999px;
        background: rgba(255, 255, 255, 0.25);
        overflow: hidden;
      }
      .resumen__barra-relleno {
        height: 100%;
        background: var(--color-secundario);
        border-radius: 999px;
        transition: width 0.3s ease;
      }
      .resumen__faltante {
        font-size: 0.8rem;
        color: rgba(255, 255, 255, 0.85);
        margin: 0.5rem 0 0;
      }
      .resumen__racha {
        flex-shrink: 0;
        text-align: center;
        background: rgba(255, 255, 255, 0.16);
        border-radius: var(--radio-media);
        padding: 0.75rem 1.1rem;
      }
      .resumen__racha-num {
        display: block;
        font-family: var(--fuente-titulos);
        font-weight: 700;
        font-size: 1.3rem;
        color: #fff;
      }
      .resumen__racha-etiqueta {
        display: block;
        font-size: 0.72rem;
        color: rgba(255, 255, 255, 0.85);
        white-space: nowrap;
      }
      .jardin {
        display: flex;
        align-items: center;
        gap: 2rem;
        flex-wrap: wrap;
        margin-bottom: 2rem;
      }
      .jardin__historial {
        display: flex;
        gap: 0.9rem;
        flex-wrap: wrap;
        align-items: flex-end;
        border-left: 1px solid var(--borde, #eee);
        padding-left: 1.5rem;
      }
      .subtitulo--chica {
        margin-bottom: 1rem;
        font-size: 0.85rem;
      }
      .grilla-logros {
        display: grid;
        grid-template-columns: repeat(auto-fill, minmax(120px, 1fr));
        gap: 0.85rem;
        margin-bottom: 2rem;
      }
      .logro-card {
        position: relative;
        text-align: center;
        background: var(--fondo-tarjeta, #fff);
        box-shadow: var(--sombra-tarjeta);
        border-radius: var(--radio-basica);
        padding: 1rem 0.5rem;
      }
      .logro-card__icono {
        display: block;
        font-size: 1.9rem;
        margin-bottom: 0.4rem;
      }
      .logro-card__nombre {
        margin: 0;
        font-size: 0.75rem;
        font-weight: 600;
        line-height: 1.3;
      }
      .logro-card--bloqueado {
        opacity: 0.45;
        filter: grayscale(1);
      }
      .logro-card__candado {
        position: absolute;
        top: 0.4rem;
        right: 0.5rem;
        font-size: 0.85rem;
      }
      .grilla-avatares {
        display: grid;
        grid-template-columns: repeat(auto-fill, minmax(64px, 1fr));
        gap: 0.75rem;
        margin-bottom: 2rem;
        max-width: 480px;
      }
      .avatar-opcion {
        position: relative;
        aspect-ratio: 1;
        border-radius: var(--radio-media);
        border: 2px solid var(--borde);
        background: var(--fondo-tarjeta);
        cursor: pointer;
        display: flex;
        align-items: center;
        justify-content: center;
        transition: transform 0.15s;
      }
      .avatar-opcion:hover {
        transform: translateY(-2px);
      }
      .avatar-opcion--elegido {
        border-color: var(--color-primario);
        background: var(--color-primario-suave);
        box-shadow: 0 0 0 3px var(--color-primario-suave);
      }
      .avatar-opcion__emoji {
        font-size: 1.5rem;
        width: 44px;
        height: 44px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        border: 2px solid rgba(255, 255, 255, 0.6);
        box-shadow: inset -4px -4px 8px rgba(0, 0, 0, 0.2), inset 3px 3px 7px rgba(255, 255, 255, 0.35);
      }
      .avatar-opcion__check {
        position: absolute;
        top: -6px;
        right: -6px;
        width: 20px;
        height: 20px;
        border-radius: 50%;
        background: var(--color-exito);
        color: #fff;
        font-size: 0.7rem;
        font-weight: 700;
        display: flex;
        align-items: center;
        justify-content: center;
      }
      .grilla-xp {
        display: grid;
        grid-template-columns: repeat(auto-fill, minmax(240px, 1fr));
        gap: 1rem;
      }
      .tarjeta-xp {
        display: flex;
        align-items: center;
        gap: 1rem;
        padding: 1.1rem;
        border-radius: var(--radio-basica);
        background: var(--fondo-tarjeta, #fff);
        box-shadow: var(--sombra-tarjeta);
        border-left: 4px solid var(--color-secundario);
      }
      .tarjeta-xp__icono {
        font-size: 1.75rem;
      }
      .tarjeta-xp__valor {
        margin: 0;
        font-family: var(--fuente-titulos);
        font-weight: 700;
        color: var(--color-secundario-texto);
      }
      .tarjeta-xp__desc {
        margin: 0.15rem 0 0;
        font-size: 0.82rem;
        color: var(--texto-secundario);
      }
      .datos-curiosos {
        list-style: none;
        margin: 0;
        padding: 0;
        display: flex;
        flex-direction: column;
        gap: 0.6rem;
        max-width: 480px;
      }
      .datos-curiosos li {
        background: var(--color-primario-suave);
        color: var(--texto-principal);
        border-radius: var(--radio-media);
        padding: 0.65rem 1rem;
        font-size: 0.9rem;
      }
      .error-carga {
        color: var(--color-error-texto);
      }
    `,
  ],
})
export class Logros {
  perfil = signal<PerfilGamificacion | null>(null);
  jardin = signal<SemanaJardin[] | null>(null);
  error = signal('');

  private gamificacion = inject(GamificacionService);
  private onboarding = inject(OnboardingService);
  private prediccion = inject(PrediccionService);
  private sesion = inject(SesionService);

  ngOnInit() {
    const perfilActivo = this.sesion.perfilActivo();
    if (!perfilActivo) return;
    this.gamificacion.obtenerPerfil(perfilActivo.id).subscribe({
      next: (p) => this.perfil.set(p),
      error: () => this.error.set('No se pudo cargar tus logros. Intenta recargar la página.'),
    });
    this.prediccion.obtenerJardinSemanal(perfilActivo.id).subscribe({
      next: (semanas) => this.jardin.set(semanas),
      error: () => {}, // sección secundaria: si falla, simplemente no se muestra
    });
  }

  emoji(avatarId: string): string {
    return EMOJI_POR_AVATAR[avatarId] || '❓';
  }

  /** Fondo tipo "esfera/gema" por avatar (radial-gradient con brillo simulado) — ver
   * COLOR_POR_AVATAR. Solo CSS, sin arte gráfico externo. */
  esferaAvatar(avatarId: string): string {
    const color = COLOR_POR_AVATAR[avatarId] || '#94A3B8';
    return `radial-gradient(circle at 32% 28%, rgba(255,255,255,0.9), ${color}cc 42%, ${color} 78%)`;
  }

  /** Espejo de `xp_acumulado_para_nivel` en el backend (curva no lineal — ver
   * planificacion/27-plan-incorporacion-hallazgos-brincus.md): XP total acumulado
   * necesario para alcanzar `nivel`. */
  private xpAcumuladoParaNivel(nivel: number): number {
    return 25 * (nivel - 1) * nivel;
  }

  progresoNivelPct(p: PerfilGamificacion): number {
    const inicioNivel = this.xpAcumuladoParaNivel(p.nivel);
    const finNivel = this.xpAcumuladoParaNivel(p.nivel + 1);
    const xpEnEsteNivel = p.xp - inicioNivel;
    return (xpEnEsteNivel / (finNivel - inicioNivel)) * 100;
  }

  logrosDesbloqueados(): number {
    return this.perfil()?.logros.filter((l) => l.desbloqueado).length ?? 0;
  }

  tiempoLegible(segundos: number): string {
    if (segundos < 60) return `${segundos} seg`;
    const minutos = Math.floor(segundos / 60);
    if (minutos < 60) return `${minutos} min`;
    const horas = Math.floor(minutos / 60);
    const minRestantes = minutos % 60;
    return minRestantes > 0 ? `${horas} h ${minRestantes} min` : `${horas} h`;
  }

  elegirAvatar(avatarId: string) {
    const perfilActivo = this.sesion.perfilActivo();
    if (!perfilActivo) return;
    this.gamificacion.cambiarAvatar(perfilActivo.id, avatarId).subscribe((p) => this.perfil.set(p));
    this.onboarding.completarPaso(perfilActivo.id, 'elegir_avatar').subscribe();
  }
}
