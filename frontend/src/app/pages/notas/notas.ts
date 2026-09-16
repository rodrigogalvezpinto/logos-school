import { Component, Input, inject, signal } from '@angular/core';
import { Router } from '@angular/router';
import { Faltantes, ItemHistorial, Historial, ProgresoService } from '../../core/progreso.service';
import { AuthService } from '../../core/auth.service';
import { EvaluacionesService } from '../../core/evaluaciones.service';
import { AgendaFamiliar, ApoderadoService } from '../../core/apoderado.service';
import { AlertaRitmoEstudio, CeldaMapaCalor, EstimacionExamen, ObservacionHorario, PrediccionService } from '../../core/prediccion.service';
import { SesionService } from '../../core/sesion.service';
import { estiloAsignatura } from '../../shared/estilo-asignatura';

const ETIQUETA_CONFIANZA: Record<string, string> = {
  sin_datos: 'Sin datos suficientes',
  baja: 'Confianza baja',
  media: 'Confianza media',
  alta: 'Confianza alta',
};

const NOTA_APROBACION = 4.0;

interface FilaHistorial {
  etiqueta: string;
  detalle: string;
  nota: number | null;
  fecha: string;
  tipo: 'prueba_unidad' | 'examen_simulacro' | 'guia';
}

@Component({
  selector: 'app-notas',
  standalone: true,
  template: `
    <div class="cabecera">
      <div>
        <h1>Mis Notas</h1>
        <p class="subtitulo">Tu avance por asignatura y todo lo que has estudiado hasta ahora.</p>
      </div>
      <button class="btn btn--secundario" (click)="descargarInforme()">⬇ Descargar informe en PDF</button>
    </div>

    @if (estimacion(); as e) {
      <div class="tarjeta prediccion" [class.prediccion--sin-datos]="e.nota_general_estimada === null">
        <span class="prediccion__etiqueta">Idea propia de Logos School — ningún colegio online lo muestra</span>
        <h2>Tu nota estimada si rindieras el Examen Libre hoy</h2>
        @if (e.nota_general_estimada !== null) {
          <div class="prediccion__nota-general">
            <span class="prediccion__numero" [class.prediccion__numero--reprobada]="e.nota_general_estimada < 4">{{ e.nota_general_estimada.toFixed(1) }}</span>
            <span class="prediccion__confianza" [class]="'prediccion__confianza--' + e.confianza_general">{{ etiquetaConfianza(e.confianza_general) }}</span>
          </div>
          <p class="prediccion__explicacion">
            Combina tu nota de práctica con tu resultado de simulacro (más parecido al examen real), ponderado por
            cuánto del temario ya cubriste. No es un resultado oficial — es una proyección para saber dónde estás parado.
          </p>
          @if (e.nota_general_estimada < 4) {
            <p class="prediccion__animo">Todavía no estás donde quieres — esta proyección va a subir a medida que sigas estudiando, no es un veredicto final.</p>
          }
          <div class="prediccion__tabla">
            @for (a of e.por_asignatura; track a.asignatura_id) {
              <div class="prediccion__fila">
                <span class="prediccion__fila-nombre">{{ a.asignatura_nombre }}</span>
                <span class="prediccion__fila-nota">{{ a.nota_estimada !== null ? a.nota_estimada.toFixed(1) : '—' }}</span>
                <span class="prediccion__fila-confianza">{{ etiquetaConfianza(a.confianza) }}</span>
              </div>
            }
          </div>
        } @else {
          <p class="prediccion__explicacion">
            Todavía no tienes evaluaciones entregadas — rinde al menos una prueba de unidad o examen simulacro
            para ver tu primera proyección.
          </p>
        }
      </div>
    }

    @if (alertaRitmo(); as a) {
      <div class="tarjeta alerta-ritmo" [class.alerta-ritmo--ok]="!a.tiene_alerta">
        <span class="alerta-ritmo__icono">{{ a.tiene_alerta ? '⚠️' : '✅' }}</span>
        <div>
          <span class="alerta-ritmo__etiqueta">Ritmo de estudio</span>
          <p class="alerta-ritmo__mensaje">{{ a.mensaje }}</p>
        </div>
      </div>
    }

    @if (agendaFamiliar(); as agenda) {
      @if (!agenda.ya_conversada) {
        <div class="tarjeta agenda-familiar">
          <span class="agenda-familiar__etiqueta">Domingo · Agenda familiar</span>
          <h3>{{ agenda.preguntas.length }} pregunta{{ agenda.preguntas.length > 1 ? 's' : '' }} para esta semana</h3>
          <ol class="agenda-familiar__lista">
            @for (pregunta of agenda.preguntas; track pregunta) {
              <li>{{ pregunta }}</li>
            }
          </ol>
          <button class="btn btn--secundario" (click)="marcarAgendaConversada()">Ya conversamos ✓</button>
        </div>
      }
    }

    @if (observacionHorario(); as oh) {
      @if (oh.tiene_observacion) {
        <div class="tarjeta observacion-horario">
          <span class="observacion-horario__icono">🌙</span>
          <div>
            <span class="observacion-horario__etiqueta">Observación</span>
            <p class="observacion-horario__mensaje">{{ oh.mensaje }}</p>
          </div>
        </div>
      }
    }

    @if (mapaCalor(); as mc) {
      @if (mc.length) {
        <h2>Mapa de calor por eje temático</h2>
        <p class="ayuda-seccion">Idea propia de Logos School — en qué ejes específicos de cada asignatura te va mejor o peor, no solo la nota general.</p>
        <div class="mapa-calor">
          @for (grupo of mapaCalorPorAsignatura(); track grupo.asignaturaId) {
            <div class="mapa-calor__asignatura" [style.--color-asig]="colorDe(grupo.asignaturaNombre)">
              <h3>{{ grupo.asignaturaNombre }}</h3>
              <div class="mapa-calor__ejes">
                @for (celda of grupo.celdas; track celda.eje_tematico) {
                  <div class="mapa-calor__celda" [class]="'mapa-calor__celda--' + nivelColor(celda.pct_correctas)">
                    <span class="mapa-calor__eje-nombre">{{ celda.eje_tematico }}</span>
                    <span class="mapa-calor__eje-pct">{{ celda.pct_correctas }}%</span>
                    @if (nivelColor(celda.pct_correctas) === 'bajo') {
                      <span class="mapa-calor__eje-animo">Todavía no — con más práctica vas a lograrlo</span>
                    }
                  </div>
                }
              </div>
            </div>
          }
        </div>
      }
    }

    @if (faltantes(); as f) {
      <h2>Avance de contenido</h2>
      <p class="ayuda-seccion">Cuánto del temario ya revisaste — distinto de tus notas, que miden qué tan bien te fue.</p>
      <div class="grid-avance">
        @for (c of f.coberturas; track c.asignatura_id) {
          <div class="avance-card" [style.--color-asig]="colorDe(c.asignatura_nombre)">
            <div class="avance-card__cabecera">
              <h3>{{ c.asignatura_nombre }}</h3>
              <span class="avance-card__pct">{{ c.cobertura_pct }}%</span>
            </div>
            <div class="avance-card__barra">
              <div class="avance-card__relleno" [style.width.%]="c.cobertura_pct"></div>
            </div>
          </div>
        }
      </div>
    }

    @if (historial(); as h) {
      @if (mostrarCoachingMadre()) {
        <div class="tarjeta coaching-madre">
          <span class="coaching-madre__etiqueta">Antes de ver la nota</span>
          <p>Reaccionar con calma ayuda más que la presión. Pregúntale qué aprendió, no solo qué nota sacó.</p>
          <button class="btn btn--primario" (click)="mostrarCoachingMadre.set(false)">Ver la nota</button>
        </div>
      } @else {
      <h2>Notas por asignatura</h2>
      <div class="grid-notas">
        @for (n of h.notas_por_asignatura; track n.asignatura_id) {
          <div class="nota-card" [style.--color-asig]="colorDe(n.asignatura_nombre)">
            <h3>{{ n.asignatura_nombre }}</h3>
            <div class="nota-card__filas">
              <div class="nota-card__fila">
                <span class="chip chip--practica">Nota de práctica</span>
                <span class="nota-card__valor" [class.nota-card__valor--aprobada]="aprobada(n.nota_practica)" [class.nota-card__valor--reprobada]="!aprobada(n.nota_practica) && n.nota_practica !== null">{{ n.nota_practica ?? '—' }}</span>
              </div>
              <div class="nota-card__fila">
                <span class="chip chip--simulacro">Resultado de simulacro</span>
                <span class="nota-card__valor" [class.nota-card__valor--aprobada]="aprobada(n.nota_simulacro)" [class.nota-card__valor--reprobada]="!aprobada(n.nota_simulacro) && n.nota_simulacro !== null">{{ n.nota_simulacro ?? '—' }}</span>
              </div>
            </div>
            @if (n.nota_simulacro !== null) {
              <p class="nota-card__aviso">Esta es tu mejor referencia de cómo te iría en el examen real.</p>
            }
          </div>
        }
        @if (!h.notas_por_asignatura.length) {
          <p class="vacio">Todavía no has rendido ninguna prueba de unidad ni examen simulacro.</p>
        }
      </div>
      }

      @if (faltantes(); as f) {
        <h2>Pruebas y exámenes faltantes</h2>
        <div class="lista-historial faltantes">
          @for (item of f.faltantes; track item.conjunto_id) {
            <div class="tarjeta fila-historial" [class.fila-historial--bloqueada]="!item.habilitado">
              <div>
                <span class="chip" [class.chip--practica]="item.tipo === 'prueba_unidad'" [class.chip--simulacro]="item.tipo === 'examen_simulacro'">
                  {{ item.tipo === 'prueba_unidad' ? 'Prueba de unidad' : 'Simulacro' }}
                </span>
                <h3>{{ item.nombre }}</h3>
                @if (!item.habilitado) {
                  <p>Se habilita al completar las guías pendientes de esa unidad.</p>
                }
              </div>
              @if (!item.habilitado) {
                <span class="chip">Bloqueada</span>
              }
            </div>
          }
          @if (!f.faltantes.length) {
            <p class="vacio">¡Ya rendiste todo lo disponible!</p>
          }
        </div>

        @for (c of f.coberturas; track c.asignatura_id) {
          @if (c.simulacro_parcial_disponible) {
            <div class="tarjeta aviso-simulacro-parcial">
              <div>
                <h3>Simulacro parcial disponible — {{ c.asignatura_nombre }}</h3>
                <p>Cubres {{ c.cobertura_pct }}% del temario. Puedes rendir un simulacro acotado a lo que ya estudiaste.</p>
              </div>
              <button class="btn btn--primario" (click)="rendirSimulacroParcial(c.asignatura_id)">Rendir simulacro parcial</button>
            </div>
          }
        }
      }

      <h2>Historial</h2>
      <div class="lista-historial">
        @for (fila of filasHistorial(); track fila.fecha + fila.etiqueta) {
          <div class="tarjeta fila-historial">
            <div>
              <span class="chip" [class.chip--practica]="fila.tipo === 'prueba_unidad'"
                [class.chip--simulacro]="fila.tipo === 'examen_simulacro'"
                [class.chip--guia]="fila.tipo === 'guia'">
                {{ etiquetaTipo(fila.tipo) }}
              </span>
              <h3>{{ fila.etiqueta }}</h3>
              <p>{{ fila.detalle }}</p>
            </div>
            @if (fila.nota !== null) {
              <span class="fila-historial__nota" [class.fila-historial__nota--aprobada]="aprobada(fila.nota)" [class.fila-historial__nota--reprobada]="!aprobada(fila.nota)">{{ fila.nota }}</span>
            }
          </div>
        }
        @if (!filasHistorial().length) {
          <p class="vacio">Tu historial de estudio va a aparecer acá.</p>
        }
      </div>
    } @else if (error()) {
      <p class="error-carga">{{ error() }}</p>
    } @else {
      <p>Cargando…</p>
    }
  `,
  styles: [
    `
      .cabecera {
        display: flex;
        justify-content: space-between;
        align-items: flex-start;
        gap: 1rem;
        margin-bottom: 1.25rem;
      }
      .subtitulo {
        color: var(--texto-secundario);
        margin-top: -0.5rem;
        margin-bottom: 0;
      }
      .ayuda-seccion {
        margin: -0.5rem 0 1rem;
        color: var(--texto-secundario);
        font-size: 0.85rem;
      }
      .prediccion {
        max-width: 640px;
        margin-bottom: 2rem;
        background: linear-gradient(135deg, var(--color-primario) 0%, var(--color-primario-oscuro) 100%);
        color: #fff;
      }
      .prediccion--sin-datos {
        background: var(--fondo-tarjeta, #fff);
        color: var(--texto-principal);
      }
      .prediccion__etiqueta {
        font-size: 0.68rem;
        font-weight: 700;
        text-transform: uppercase;
        opacity: 0.85;
      }
      .prediccion h2 {
        margin: 0.3rem 0 1rem;
        color: inherit;
        font-size: 1.15rem;
      }
      .prediccion__nota-general {
        display: flex;
        align-items: baseline;
        gap: 0.75rem;
        margin-bottom: 0.5rem;
      }
      .prediccion__numero {
        font-family: var(--fuente-titulos);
        font-weight: 700;
        font-size: 2.4rem;
      }
      .prediccion__numero--reprobada {
        color: #ffd5cc;
      }
      .prediccion__confianza {
        font-size: 0.75rem;
        font-weight: 700;
        padding: 0.2rem 0.6rem;
        border-radius: 999px;
        background: rgba(255, 255, 255, 0.2);
      }
      .prediccion__explicacion {
        font-size: 0.85rem;
        opacity: 0.9;
        margin: 0 0 1rem;
        max-width: 520px;
      }
      .prediccion__animo {
        font-size: 0.8rem;
        font-weight: 600;
        margin: -0.5rem 0 1rem;
        max-width: 520px;
      }
      .prediccion__tabla {
        display: flex;
        flex-direction: column;
        gap: 0.4rem;
      }
      .prediccion__fila {
        display: grid;
        grid-template-columns: 1fr auto auto;
        gap: 1rem;
        align-items: center;
        background: rgba(255, 255, 255, 0.12);
        border-radius: var(--radio-media);
        padding: 0.45rem 0.75rem;
        font-size: 0.85rem;
      }
      .prediccion--sin-datos .prediccion__fila {
        background: var(--fondo, #f5f5f7);
      }
      .prediccion__fila-nota {
        font-weight: 700;
        font-family: var(--fuente-titulos);
      }
      .prediccion__fila-confianza {
        font-size: 0.72rem;
        opacity: 0.85;
        white-space: nowrap;
      }
      .alerta-ritmo {
        display: flex;
        align-items: flex-start;
        gap: 0.85rem;
        max-width: 640px;
        margin-bottom: 2rem;
        border-left: 4px solid var(--color-alerta);
      }
      .alerta-ritmo--ok {
        border-left-color: var(--color-exito);
      }
      .alerta-ritmo__icono {
        font-size: 1.3rem;
        flex-shrink: 0;
      }
      .alerta-ritmo__etiqueta {
        display: block;
        font-size: 0.7rem;
        font-weight: 700;
        text-transform: uppercase;
        color: var(--texto-secundario);
        margin-bottom: 0.15rem;
      }
      .alerta-ritmo__mensaje {
        margin: 0;
        font-size: 0.9rem;
        color: var(--texto-principal);
      }
      .coaching-madre {
        max-width: 480px;
        margin-bottom: 2rem;
        background: var(--color-primario-suave);
        border: 1.5px solid var(--color-primario);
      }
      .coaching-madre__etiqueta {
        display: block;
        font-size: 0.7rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.03em;
        color: var(--color-primario);
        margin-bottom: 0.4rem;
      }
      .coaching-madre p {
        margin: 0 0 1rem;
        font-size: 0.9rem;
        color: var(--texto-principal);
      }
      .agenda-familiar {
        max-width: 480px;
        margin-bottom: 2rem;
        background: var(--color-secundario-suave);
        border: 1.5px solid var(--color-secundario);
      }
      .agenda-familiar__etiqueta {
        display: block;
        font-size: 0.68rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.03em;
        color: var(--color-secundario-texto);
        margin-bottom: 0.4rem;
      }
      .agenda-familiar h3 {
        margin: 0 0 0.75rem;
        font-size: 1rem;
      }
      .agenda-familiar__lista {
        margin: 0 0 1rem;
        padding-left: 1.2rem;
        display: flex;
        flex-direction: column;
        gap: 0.5rem;
        font-size: 0.88rem;
        color: var(--texto-principal);
      }
      .observacion-horario {
        display: flex;
        align-items: flex-start;
        gap: 0.85rem;
        max-width: 640px;
        margin-bottom: 2rem;
        border-left: 4px solid var(--color-alerta);
      }
      .observacion-horario__icono {
        font-size: 1.3rem;
        flex-shrink: 0;
      }
      .observacion-horario__etiqueta {
        display: block;
        font-size: 0.7rem;
        font-weight: 700;
        text-transform: uppercase;
        color: var(--texto-secundario);
        margin-bottom: 0.15rem;
      }
      .observacion-horario__mensaje {
        margin: 0;
        font-size: 0.9rem;
        color: var(--texto-principal);
      }
      .mapa-calor {
        display: flex;
        flex-direction: column;
        gap: 1rem;
        margin-bottom: 2.5rem;
      }
      .mapa-calor__asignatura {
        background: var(--fondo-tarjeta, #fff);
        box-shadow: var(--sombra-tarjeta);
        border-radius: var(--radio-basica);
        border-left: 4px solid var(--color-asig, var(--color-primario));
        padding: 1rem 1.1rem;

        h3 {
          margin: 0 0 0.65rem;
          font-size: 0.9rem;
        }
      }
      .mapa-calor__ejes {
        display: flex;
        flex-wrap: wrap;
        gap: 0.6rem;
      }
      .mapa-calor__celda {
        display: flex;
        flex-direction: column;
        gap: 0.15rem;
        min-width: 110px;
        padding: 0.5rem 0.75rem;
        border-radius: var(--radio-media);
      }
      .mapa-calor__eje-nombre {
        font-size: 0.75rem;
        font-weight: 600;
      }
      .mapa-calor__eje-pct {
        font-family: var(--fuente-titulos);
        font-weight: 700;
        font-size: 1.1rem;
      }
      .mapa-calor__eje-animo {
        font-size: .68rem;
        font-weight: 600;
      }
      .mapa-calor__celda--bajo {
        /* Ámbar, no rojo — el rojo en contexto escolar se asocia a error/castigo y
           desmotiva (planificacion/15-diseno-visual-y-marca.md); un eje flojo se comunica
           con más énfasis visual (borde), no con un color de alarma. */
        background: var(--color-alerta-suave);
        color: var(--color-alerta-texto);
        border: 1.5px solid var(--color-alerta);
      }
      .mapa-calor__celda--medio {
        background: var(--color-alerta-suave);
        color: var(--color-alerta-texto);
      }
      .mapa-calor__celda--alto {
        background: var(--color-exito-suave);
        color: var(--color-exito-texto);
      }
      .grid-avance {
        display: grid;
        grid-template-columns: repeat(auto-fill, minmax(220px, 1fr));
        gap: 1rem;
        margin-bottom: 2.5rem;
      }
      .avance-card {
        background: var(--fondo-tarjeta, #fff);
        box-shadow: var(--sombra-tarjeta);
        border-radius: var(--radio-basica);
        border-top: 4px solid var(--color-asig, var(--color-primario));
        padding: 1rem 1.1rem;
      }
      .avance-card__cabecera {
        display: flex;
        justify-content: space-between;
        align-items: baseline;
        margin-bottom: 0.6rem;
      }
      .avance-card__cabecera h3 {
        margin: 0;
        font-size: 0.9rem;
      }
      .avance-card__pct {
        font-family: var(--fuente-titulos);
        font-weight: 700;
        color: var(--color-asig, var(--color-primario));
      }
      .avance-card__barra {
        height: 8px;
        border-radius: 999px;
        background: var(--fondo, #eee);
        overflow: hidden;
      }
      .avance-card__relleno {
        height: 100%;
        border-radius: 999px;
        background: var(--color-asig, var(--color-primario));
      }
      .grid-notas {
        display: grid;
        grid-template-columns: repeat(auto-fill, minmax(260px, 1fr));
        gap: 1rem;
        margin-bottom: 2.5rem;
      }
      .nota-card {
        background: var(--fondo-tarjeta, #fff);
        box-shadow: var(--sombra-tarjeta);
        border-radius: var(--radio-basica);
        border-top: 4px solid var(--color-asig, var(--color-primario));
        padding: 1.1rem 1.25rem;
      }
      .nota-card h3 {
        margin: 0 0 0.75rem;
      }
      .nota-card__filas {
        display: flex;
        flex-direction: column;
        gap: 0.5rem;
      }
      .nota-card__fila {
        display: flex;
        justify-content: space-between;
        align-items: center;
      }
      .nota-card__valor {
        font-family: var(--fuente-titulos);
        font-weight: 700;
        font-size: 1.15rem;
      }
      .nota-card__valor--aprobada {
        color: var(--color-exito-texto);
      }
      .nota-card__valor--reprobada {
        color: var(--color-error-texto);
      }
      .nota-card__aviso {
        margin: 0.75rem 0 0;
        font-size: 0.8rem;
        color: var(--texto-secundario);
      }
      .chip {
        display: inline-block;
        font-size: 0.7rem;
        font-weight: 600;
        padding: 0.2rem 0.55rem;
        border-radius: 999px;
        background: var(--fondo);
        color: var(--texto-secundario);
      }
      .chip--practica {
        background: var(--color-primario-suave);
        color: var(--color-primario);
      }
      .chip--simulacro {
        background: var(--color-secundario-suave);
        color: var(--color-secundario-texto);
      }
      .chip--guia {
        background: var(--color-exito-suave);
        color: var(--color-exito-texto);
      }
      .lista-historial {
        display: flex;
        flex-direction: column;
        gap: 0.75rem;
      }
      .fila-historial {
        display: flex;
        justify-content: space-between;
        align-items: center;
        gap: 1rem;

        h3 {
          margin: 0.35rem 0 0.15rem;
          font-size: 0.95rem;
        }
        p {
          margin: 0;
          color: var(--texto-secundario);
          font-size: 0.8rem;
        }
      }
      .fila-historial__nota {
        font-family: var(--fuente-titulos);
        font-weight: 700;
        font-size: 1.1rem;
        flex-shrink: 0;
      }
      .fila-historial__nota--aprobada {
        color: var(--color-exito-texto);
      }
      .fila-historial__nota--reprobada {
        color: var(--color-error-texto);
      }
      .vacio {
        color: var(--texto-secundario);
      }
      .error-carga {
        color: var(--color-error-texto);
      }
      .faltantes {
        margin-bottom: 2rem;
      }
      .fila-historial--bloqueada {
        opacity: 0.8;
      }
      .aviso-simulacro-parcial {
        display: flex;
        justify-content: space-between;
        align-items: center;
        gap: 1rem;
        border: 1.5px solid var(--color-primario);
        margin-bottom: 1.5rem;

        h3 {
          margin: 0 0 0.2rem;
        }
        p {
          margin: 0;
          color: var(--texto-secundario);
          font-size: 0.85rem;
        }
      }
    `,
  ],
})
export class Notas {
  @Input() perfilAlumnoId = '';
  historial = signal<Historial | null>(null);
  faltantes = signal<Faltantes | null>(null);
  estimacion = signal<EstimacionExamen | null>(null);
  alertaRitmo = signal<AlertaRitmoEstudio | null>(null);
  mapaCalor = signal<CeldaMapaCalor[] | null>(null);
  observacionHorario = signal<ObservacionHorario | null>(null);
  agendaFamiliar = signal<AgendaFamiliar | null>(null);
  mostrarCoachingMadre = signal(false);
  error = signal('');

  private progreso = inject(ProgresoService);
  private evaluaciones = inject(EvaluacionesService);
  private prediccion = inject(PrediccionService);
  private apoderadoService = inject(ApoderadoService);
  private sesion = inject(SesionService);
  private auth = inject(AuthService);
  private router = inject(Router);

  ngOnInit() {
    const perfilActivo = this.sesion.perfilActivo();
    const id = this.perfilAlumnoId ? Number(this.perfilAlumnoId) : perfilActivo?.id;
    if (!id) return;
    this.progreso.obtenerHistorial(id).subscribe({
      next: (h) => {
        this.historial.set(h);
        // Coaching a la madre (idea propia): solo en la vista del Apoderado
        // (`perfilAlumnoId` viene de la ruta cuando mira a un hijo, no cuando el propio
        // alumno ve sus notas) y solo si hay al menos una nota reprobada que revelar —
        // no tiene sentido interponer un tip si no hay ninguna nota baja de por medio.
        if (this.perfilAlumnoId && h.notas_por_asignatura.some((n) => !this.aprobada(n.nota_practica) && n.nota_practica !== null || !this.aprobada(n.nota_simulacro) && n.nota_simulacro !== null)) {
          this.mostrarCoachingMadre.set(true);
        }
      },
      error: () => this.error.set('No se pudo cargar tu historial. Intenta recargar la página.'),
    });

    // A diferencia de "avance de contenido"/"nota estimada" (que necesitan el nivel_id del
    // propio perfilActivo), la alerta de ritmo solo necesita el perfil_alumno_id — funciona
    // igual para el propio alumno y para el apoderado viendo el progreso de un hijo.
    this.prediccion.obtenerAlertaDeRitmo(id).subscribe({
      next: (a) => this.alertaRitmo.set(a),
      error: () => {}, // sección secundaria: si falla, simplemente no se muestra
    });

    // Igual que la alerta de ritmo, solo necesita el perfil_alumno_id — sirve tanto para el
    // propio alumno como para el apoderado viendo el progreso de un hijo.
    this.prediccion.obtenerMapaDeCalor(id).subscribe({
      next: (mc) => this.mapaCalor.set(mc),
      error: () => {}, // sección secundaria: si falla, simplemente no se muestra
    });

    // Cruce sueño/horario (idea propia): a propósito SOLO para el Apoderado, nunca para el
    // propio alumno — es información para que un adulto decida, no una alerta directa al
    // niño (se sentiría como vigilancia).
    if (this.perfilAlumnoId) {
      this.prediccion.obtenerObservacionDeHorario(id).subscribe({
        next: (oh) => this.observacionHorario.set(oh),
        error: () => {}, // sección secundaria: si falla, simplemente no se muestra
      });
      // Agenda familiar del domingo (idea propia): también solo para el Apoderado, mismo
      // criterio que el cruce de horario.
      this.apoderadoService.obtenerAgendaFamiliar(id).subscribe({
        next: (agenda) => this.agendaFamiliar.set(agenda),
        error: () => {}, // sección secundaria: si falla, simplemente no se muestra
      });
    }

    // La sección de faltantes/simulacro parcial es una acción que solo el propio alumno
    // puede iniciar (necesita rendir la prueba) — no se muestra en la vista del apoderado,
    // que no tiene un `perfilActivo` (nivel_id) propio para esta consulta.
    if (!this.perfilAlumnoId && perfilActivo) {
      this.progreso.obtenerFaltantes(id, perfilActivo.nivel_id).subscribe({
        next: (f) => this.faltantes.set(f),
        error: () => {}, // sección secundaria: si falla, simplemente no se muestra
      });
      this.prediccion.obtenerNotaEstimada(id, perfilActivo.nivel_id).subscribe({
        next: (e) => this.estimacion.set(e),
        error: () => {}, // sección secundaria: si falla, simplemente no se muestra
      });
    }
  }

  etiquetaConfianza(confianza: string): string {
    return ETIQUETA_CONFIANZA[confianza] ?? confianza;
  }

  marcarAgendaConversada() {
    const id = this.perfilAlumnoId ? Number(this.perfilAlumnoId) : null;
    if (!id) return;
    this.apoderadoService.marcarAgendaFamiliarConversada(id).subscribe(() => {
      const agenda = this.agendaFamiliar();
      if (agenda) this.agendaFamiliar.set({ ...agenda, ya_conversada: true });
    });
  }

  mapaCalorPorAsignatura(): { asignaturaId: number; asignaturaNombre: string; celdas: CeldaMapaCalor[] }[] {
    const celdas = this.mapaCalor();
    if (!celdas) return [];
    const grupos: { asignaturaId: number; asignaturaNombre: string; celdas: CeldaMapaCalor[] }[] = [];
    for (const celda of celdas) {
      let grupo = grupos.find((g) => g.asignaturaId === celda.asignatura_id);
      if (!grupo) {
        grupo = { asignaturaId: celda.asignatura_id, asignaturaNombre: celda.asignatura_nombre, celdas: [] };
        grupos.push(grupo);
      }
      grupo.celdas.push(celda);
    }
    return grupos;
  }

  nivelColor(pct: number): 'bajo' | 'medio' | 'alto' {
    if (pct < 50) return 'bajo';
    if (pct < 80) return 'medio';
    return 'alto';
  }

  descargarInforme() {
    const perfilActivo = this.sesion.perfilActivo();
    const id = this.perfilAlumnoId ? Number(this.perfilAlumnoId) : perfilActivo?.id;
    if (!id) return;
    this.auth.descargarInformeAvance(id).subscribe((blob) => {
      const url = window.URL.createObjectURL(blob);
      window.open(url, '_blank');
    });
  }

  rendirSimulacroParcial(asignaturaId: number) {
    const perfil = this.sesion.perfilActivo();
    if (!perfil) return;
    this.evaluaciones.generarSimulacroParcial(asignaturaId, perfil.id).subscribe((intento) => {
      this.router.navigate(['/examen', intento.conjunto_evaluacion_id]);
    });
  }

  filasHistorial(): FilaHistorial[] {
    const h = this.historial();
    if (!h) return [];
    const evaluaciones: FilaHistorial[] = h.historial.map((i: ItemHistorial) => ({
      etiqueta: i.nombre,
      detalle: i.asignatura_nombre ?? 'Examen integrado',
      nota: i.nota,
      fecha: i.fecha,
      tipo: i.tipo,
    }));
    const guias: FilaHistorial[] = h.guias_revisadas.map((g) => ({
      etiqueta: 'Guía revisada',
      detalle: `${g.asignatura_nombre} — ${g.codigo_oficial}`,
      nota: null,
      fecha: g.fecha,
      tipo: 'guia' as const,
    }));
    return [...evaluaciones, ...guias].sort((a, b) => (a.fecha < b.fecha ? 1 : -1));
  }

  etiquetaTipo(tipo: FilaHistorial['tipo']): string {
    if (tipo === 'prueba_unidad') return 'Prueba de unidad';
    if (tipo === 'examen_simulacro') return 'Simulacro';
    return 'Guía';
  }

  colorDe(nombreAsignatura: string): string {
    return estiloAsignatura(nombreAsignatura).color;
  }

  aprobada(nota: number | null): boolean {
    return nota !== null && nota >= NOTA_APROBACION;
  }
}
