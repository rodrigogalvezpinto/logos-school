import { Component } from '@angular/core';
import { Router } from '@angular/router';
import { AuthLayout } from '../../shared/auth-layout/auth-layout';

@Component({
  selector: 'app-agregar-alumno',
  standalone: true,
  imports: [AuthLayout],
  template: `
    <app-auth-layout
      titulo="Agrega a tu primer alumno"
      subtitulo="Puedes agregar más de un hijo o pupilo a tu cuenta más adelante."
    >
      <form (submit)="$event.preventDefault(); continuar()">
        <div class="campo-fila">
          <div class="campo">
            <label>Nombre</label>
            <input type="text" placeholder="Sofía" />
          </div>
          <div class="campo">
            <label>Apellidos</label>
            <input type="text" placeholder="Pérez González" />
          </div>
        </div>
        <div class="campo-fila">
          <div class="campo">
            <label>Fecha de nacimiento</label>
            <input type="date" />
          </div>
          <div class="campo">
            <label>RUT</label>
            <input type="text" placeholder="12.345.678-9" />
          </div>
        </div>
        <div class="campo">
          <label>Curso</label>
          <select>
            <option>4° básico</option>
          </select>
        </div>
        <button type="submit" class="btn btn--primario btn--bloque btn--grande">Continuar</button>
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
    `,
  ],
})
export class AgregarAlumno {
  constructor(private router: Router) {}

  continuar() {
    this.router.navigate(['/seleccion-plan']);
  }
}
