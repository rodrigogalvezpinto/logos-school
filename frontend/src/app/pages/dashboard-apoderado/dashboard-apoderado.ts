import { Component, inject, signal } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { ApoderadoService, MetaFamiliar } from '../../core/apoderado.service';
import { AuthService, PerfilAlumnoRespuesta } from '../../core/auth.service';
import { ContenidoService } from '../../core/contenido.service';
import { SesionService } from '../../core/sesion.service';
import { validarRut } from '../../core/rut.util';

/** Fase 1, ítem 2.9 del plan de incorporación de hallazgos de Brincus — agregar un
 * alumno inline en el propio panel del Apoderado, sin salir a la ruta aparte
 * `/agregar-alumno` (esa ruta sigue existiendo tal cual para el primer alumno durante el
 * registro de una cuenta nueva, que sí necesita el flujo completo con plan de estudio y
 * selección de plan). Ver planificacion/27-plan-incorporacion-hallazgos-brincus.md. */
@Component({
  selector: 'app-dashboard-apoderado',
  standalone: true,
  imports: [FormsModule],
  template: `
    <h1>Hola, {{ nombreApoderado() }} 👋</h1>
    <p class="subtitulo">Así va tu familia en Logos School.</p>

    @if (metaFamiliar(); as meta) {
      <div class="tarjeta meta-familiar">
        <span class="chip chip--meta">Meta familiar</span>
        <h3>Esta semana, la familia estudió {{ meta.dias_esta_semana }} día{{ meta.dias_esta_semana !== 1 ? 's' : '' }} combinados</h3>
        @if (meta.es_nueva_marca) {
          <p>Nueva marca — la semana pasada fueron {{ meta.dias_semana_anterior }}.</p>
        } @else {
          <p>La semana pasada fueron {{ meta.dias_semana_anterior }}.</p>
        }
      </div>
    }

    @if (error()) {
      <p class="error-carga">{{ error() }}</p>
    }
    <div class="grid">
      @for (alumno of alumnos(); track alumno.id) {
        <div class="tarjeta alumno-card">
          <div class="alumno-card__avatar">{{ alumno.nombre.charAt(0) }}</div>
          <div class="alumno-card__info">
            <h3>{{ alumno.nombre }} {{ alumno.apellidos }}</h3>
            <span class="chip chip--activo">Plan activo</span>
          </div>
          @if (confirmandoEliminar() === alumno.id) {
            <div class="alumno-card__confirmar">
              <p>¿Eliminar a {{ alumno.nombre }}? Se borra todo su historial (notas, evaluaciones, progreso) — no se puede deshacer.</p>
              <div class="alumno-card__confirmar-acciones">
                <button type="button" class="btn btn--secundario btn--chico" (click)="confirmandoEliminar.set(null)">Cancelar</button>
                <button type="button" class="btn btn--peligro btn--chico" (click)="eliminarAlumno(alumno.id)">Sí, eliminar</button>
              </div>
            </div>
          } @else {
            <button type="button" class="alumno-card__eliminar" (click)="confirmandoEliminar.set(alumno.id)" [attr.aria-label]="'Eliminar a ' + alumno.nombre">🗑️</button>
          }
        </div>
      }

      @if (!mostrandoFormulario()) {
        <button type="button" class="tarjeta agregar-card" (click)="mostrandoFormulario.set(true)">
          <span class="agregar-card__mas">+</span>
          <span>Agregar otro alumno</span>
        </button>
      }
    </div>

    @if (mostrandoFormulario()) {
      <div class="tarjeta formulario-inline">
        <h3>Agregar un nuevo alumno</h3>
        <form (submit)="$event.preventDefault(); agregar()">
          <div class="campo-fila">
            <div class="campo">
              <label>Nombre</label>
              <input type="text" [(ngModel)]="nombre" name="nombre" placeholder="Sofía" />
            </div>
            <div class="campo">
              <label>Apellidos</label>
              <input type="text" [(ngModel)]="apellidos" name="apellidos" placeholder="Pérez González" />
            </div>
          </div>
          <div class="campo-fila">
            <div class="campo">
              <label>Fecha de nacimiento</label>
              <input type="date" [(ngModel)]="fechaNacimiento" name="fechaNacimiento" />
            </div>
            <div class="campo">
              <label>RUT</label>
              <input type="text" [(ngModel)]="rut" name="rut" placeholder="12.345.678-9" />
            </div>
          </div>
          <div class="campo">
            <label>Curso</label>
            <select [(ngModel)]="nivelId" name="nivelId">
              @for (n of niveles(); track n.id) {
                <option [value]="n.id">{{ n.nombre }}</option>
              }
            </select>
          </div>

          @if (errorFormulario()) {
            <p class="error">{{ errorFormulario() }}</p>
          }
          <div class="formulario-inline__acciones">
            <button type="button" class="btn btn--secundario" (click)="cancelar()">Cancelar</button>
            <button type="submit" class="btn btn--primario" [disabled]="cargando()">
              {{ cargando() ? 'Guardando…' : 'Agregar alumno' }}
            </button>
          </div>
        </form>
      </div>
    }
  `,
  styles: [
    `
      .subtitulo {
        color: var(--texto-secundario);
        margin-top: -0.5rem;
        margin-bottom: 2rem;
      }
      .grid {
        display: grid;
        grid-template-columns: repeat(2, 1fr);
        gap: 1rem;
        max-width: 760px;
      }
      @media (max-width: 700px) {
        .grid {
          grid-template-columns: 1fr;
        }
      }
      .alumno-card {
        display: flex;
        align-items: center;
        gap: 1rem;
        flex-wrap: wrap;
        position: relative;
      }
      .alumno-card__eliminar {
        background: none;
        border: none;
        cursor: pointer;
        font-size: 1.1rem;
        padding: 0.3rem;
        opacity: 0.55;
        flex-shrink: 0;
      }
      .alumno-card__eliminar:hover {
        opacity: 1;
      }
      .alumno-card__confirmar {
        flex-basis: 100%;
        background: var(--color-error-suave, #fde8e8);
        border-radius: var(--radio-media);
        padding: 0.75rem 1rem;
        margin-top: 0.25rem;

        p {
          margin: 0 0 0.6rem;
          font-size: 0.82rem;
          color: var(--texto-principal);
        }
      }
      .alumno-card__confirmar-acciones {
        display: flex;
        gap: 0.6rem;
      }
      .btn--chico {
        padding: 0.4rem 0.75rem;
        font-size: 0.8rem;
      }
      .alumno-card__avatar {
        width: 52px;
        height: 52px;
        border-radius: var(--radio-media);
        background: var(--color-primario);
        color: white;
        display: flex;
        align-items: center;
        justify-content: center;
        font-family: var(--fuente-titulos);
        font-weight: 700;
        font-size: 1.3rem;
        flex-shrink: 0;
      }
      .alumno-card__info {
        flex: 1;

        h3 {
          margin: 0 0 0.4rem;
        }
      }
      .chip {
        display: inline-block;
        font-size: 0.75rem;
        font-weight: 600;
        padding: 0.2rem 0.6rem;
        border-radius: 999px;
      }
      .chip--activo {
        background: var(--color-exito-suave);
        color: var(--color-exito-texto);
      }
      .chip--meta {
        background: var(--color-secundario-suave);
        color: var(--color-secundario-texto);
      }
      .meta-familiar {
        max-width: 480px;
        margin-bottom: 1.5rem;
        border: 1.5px solid var(--color-secundario);
      }
      .meta-familiar h3 {
        margin: 0.5rem 0 0.3rem;
      }
      .meta-familiar p {
        margin: 0;
        font-size: 0.85rem;
        color: var(--texto-secundario);
      }
      .agregar-card {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        gap: 0.5rem;
        text-decoration: none;
        color: var(--texto-secundario);
        border: 2px dashed var(--borde);
        box-shadow: none;
        background: none;
        cursor: pointer;
        font-family: var(--fuente-texto);
        width: 100%;
      }
      .agregar-card__mas {
        font-size: 1.8rem;
        color: var(--color-primario);
      }
      .error-carga {
        color: var(--color-error-texto);
      }
      .formulario-inline {
        max-width: 560px;
        margin-top: 1.25rem;

        h3 {
          margin-top: 0;
        }
      }
      .campo-fila {
        display: flex;
        gap: 1rem;

        .campo {
          flex: 1;
          min-width: 0;
        }
      }
      @media (max-width: 480px) {
        .campo-fila {
          flex-direction: column;
          gap: 0;
        }
      }
      .formulario-inline__acciones {
        display: flex;
        gap: 0.75rem;
        justify-content: flex-end;
        margin-top: 1rem;
      }
      .error {
        color: var(--color-error-texto);
        font-size: 0.85rem;
        margin: -0.5rem 0 1rem;
      }
    `,
  ],
})
export class DashboardApoderado {
  alumnos = signal<PerfilAlumnoRespuesta[]>([]);
  metaFamiliar = signal<MetaFamiliar | null>(null);
  error = signal('');

  mostrandoFormulario = signal(false);
  confirmandoEliminar = signal<number | null>(null);
  nombre = '';
  apellidos = '';
  fechaNacimiento = '';
  rut = '';
  nivelId: number | null = null;
  niveles = signal<{ id: number; nombre: string }[]>([]);
  cargando = signal(false);
  errorFormulario = signal('');

  private auth = inject(AuthService);
  private apoderado = inject(ApoderadoService);
  private contenido = inject(ContenidoService);
  private sesion = inject(SesionService);

  constructor() {
    this.auth.listarAlumnos().subscribe({
      next: (alumnos) => this.alumnos.set(alumnos),
      error: () => this.error.set('No se pudo cargar la lista de alumnos. Intenta recargar la página.'),
    });
    this.contenido.listarNiveles().subscribe((niveles) => {
      this.niveles.set(niveles);
      if (niveles.length) this.nivelId = niveles[0].id;
    });
    // El backend ya devuelve null con un solo alumno (idea 9 del boceto de innovación,
    // 2026-08-17) — no hace falta repetir esa condición acá.
    this.apoderado.obtenerMetaFamiliar().subscribe({
      next: (meta) => this.metaFamiliar.set(meta),
      error: () => {}, // sección secundaria: si falla, simplemente no se muestra
    });
  }

  nombreApoderado(): string {
    return this.sesion.nombreApoderado() || 'Apoderado';
  }

  eliminarAlumno(perfilAlumnoId: number) {
    this.auth.eliminarAlumno(perfilAlumnoId).subscribe(() => {
      this.alumnos.set(this.alumnos().filter((a) => a.id !== perfilAlumnoId));
      this.confirmandoEliminar.set(null);
    });
  }

  cancelar() {
    this.mostrandoFormulario.set(false);
    this.errorFormulario.set('');
    this.nombre = '';
    this.apellidos = '';
    this.fechaNacimiento = '';
    this.rut = '';
  }

  agregar() {
    this.errorFormulario.set('');
    if (!validarRut(this.rut)) {
      this.errorFormulario.set('El RUT ingresado no es válido — revisa el número y el dígito verificador.');
      return;
    }
    if (!this.nivelId) {
      this.errorFormulario.set('Selecciona un curso.');
      return;
    }
    this.cargando.set(true);
    this.auth
      .agregarAlumno({
        nombre: this.nombre,
        apellidos: this.apellidos,
        fecha_nacimiento: this.fechaNacimiento,
        rut: this.rut,
        nivel_id: this.nivelId,
      })
      .subscribe({
        next: (perfil) => {
          this.alumnos.update((a) => [...a, perfil]);
          this.cargando.set(false);
          this.cancelar();
        },
        error: (err) => {
          this.cargando.set(false);
          this.errorFormulario.set(err?.error?.detail || 'No se pudo agregar al alumno.');
        },
      });
  }
}
