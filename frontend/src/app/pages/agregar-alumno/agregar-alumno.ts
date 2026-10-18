import { Component, inject, signal } from '@angular/core';
import { Router } from '@angular/router';
import { FormsModule } from '@angular/forms';
import { AuthLayout } from '../../shared/auth-layout/auth-layout';
import { AuthService } from '../../core/auth.service';
import { ContenidoService } from '../../core/contenido.service';
import { PlanEstudioService } from '../../core/plan-estudio.service';
import { validarRut } from '../../core/rut.util';

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
  selector: 'app-agregar-alumno',
  standalone: true,
  imports: [FormsModule, AuthLayout],
  template: `
    <app-auth-layout
      titulo="Agrega a tu primer alumno"
      subtitulo="Puedes agregar más de un hijo o pupilo a tu cuenta más adelante."
    >
      <form (submit)="$event.preventDefault(); continuar()">
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

        <div class="campo">
          <label>¿Qué días va a estudiar? (mínimo 3)</label>
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
        <button type="submit" class="btn btn--primario btn--bloque btn--grande" [disabled]="cargando()">
          {{ cargando() ? 'Guardando…' : 'Continuar' }}
        </button>
      </form>
    </app-auth-layout>
  `,
  styles: [
    `
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
        margin: -0.5rem 0 1rem;
      }
    `,
  ],
})
export class AgregarAlumno {
  nombre = '';
  apellidos = '';
  fechaNacimiento = '';
  rut = '';
  nivelId: number | null = null;
  fechaObjetivo = '';
  dias = DIAS;
  diasElegidos = new Set<string>(['lunes', 'miercoles', 'viernes']);
  niveles = signal<{ id: number; nombre: string }[]>([]);
  cargando = signal(false);
  error = signal('');

  private auth = inject(AuthService);
  private contenido = inject(ContenidoService);
  private planEstudio = inject(PlanEstudioService);
  private router = inject(Router);

  constructor() {
    this.contenido.listarNiveles().subscribe((niveles) => {
      this.niveles.set(niveles);
      if (niveles.length) this.nivelId = niveles[0].id;
    });
  }

  toggleDia(dia: string) {
    if (this.diasElegidos.has(dia)) {
      this.diasElegidos.delete(dia);
    } else {
      this.diasElegidos.add(dia);
    }
  }

  continuar() {
    this.error.set('');
    if (!validarRut(this.rut)) {
      this.error.set('El RUT ingresado no es válido — revisa el número y el dígito verificador.');
      return;
    }
    if (!this.nivelId) {
      this.error.set('Selecciona un curso.');
      return;
    }
    if (this.diasElegidos.size < 3) {
      this.error.set('Elige al menos 3 días de estudio a la semana.');
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
          const diasElegidos = Array.from(this.diasElegidos);
          // No bloquea el registro si falla — el alumno puede armar su plan después
          // desde /alumno/plan-estudio.
          this.planEstudio
            .crearPlan(perfil.id, diasElegidos.length, diasElegidos, this.fechaObjetivo || null)
            .subscribe({
              next: () =>
                this.router.navigate(['/seleccion-plan'], { queryParams: { nombre: perfil.nombre, perfilId: perfil.id } }),
              error: () =>
                this.router.navigate(['/seleccion-plan'], { queryParams: { nombre: perfil.nombre, perfilId: perfil.id } }),
            });
        },
        error: (err) => {
          this.cargando.set(false);
          this.error.set(err?.error?.detail || 'No se pudo agregar al alumno.');
        },
      });
  }
}
