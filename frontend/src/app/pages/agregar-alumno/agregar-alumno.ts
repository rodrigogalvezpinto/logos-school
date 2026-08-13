import { Component, inject, signal } from '@angular/core';
import { Router } from '@angular/router';
import { FormsModule } from '@angular/forms';
import { AuthLayout } from '../../shared/auth-layout/auth-layout';
import { AuthService } from '../../core/auth.service';
import { ContenidoService } from '../../core/contenido.service';
import { validarRut } from '../../core/rut.util';

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
        }
      }
      .error {
        color: var(--color-error);
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
  niveles = signal<{ id: number; nombre: string }[]>([]);
  cargando = signal(false);
  error = signal('');

  private auth = inject(AuthService);
  private contenido = inject(ContenidoService);
  private router = inject(Router);

  constructor() {
    this.contenido.listarNiveles().subscribe((niveles) => {
      this.niveles.set(niveles);
      if (niveles.length) this.nivelId = niveles[0].id;
    });
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
        next: () => this.router.navigate(['/seleccion-plan']),
        error: (err) => {
          this.cargando.set(false);
          this.error.set(err?.error?.detail || 'No se pudo agregar al alumno.');
        },
      });
  }
}
