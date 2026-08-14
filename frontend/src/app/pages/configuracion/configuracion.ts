import { Component, Input, inject } from '@angular/core';
import { SesionService } from '../../core/sesion.service';

@Component({
  selector: 'app-configuracion',
  standalone: true,
  template: `
    <h1>Configuración</h1>
    <p class="subtitulo">Datos de tu cuenta y privacidad.</p>

    @if (contexto === 'apoderado') {
      <div class="tarjeta bloque">
        <h3>Datos de la cuenta</h3>
        <div class="campo">
          <label>Nombre</label>
          <input type="text" [value]="sesion.nombreApoderado()" />
        </div>
        <button class="btn btn--primario">Guardar cambios</button>
      </div>

      <div class="tarjeta bloque">
        <h3>Privacidad</h3>
        <p>Puedes exportar o eliminar los datos de cualquier alumno vinculado a tu cuenta.</p>
        <button class="btn btn--secundario">Exportar mis datos</button>
      </div>
    } @else {
      <!-- Vista de un Alumno: solo su propio nombre, nunca los datos de la cuenta del
           Apoderado (correo, etc.) — mostrarlos acá confundía a los alumnos al probar
           la app, ya que parecía que estaban editando la cuenta de otra persona. -->
      <div class="tarjeta bloque">
        <h3>Mi perfil</h3>
        <div class="campo">
          <label>Nombre</label>
          <input type="text" [value]="nombreAlumno()" disabled />
        </div>
        <p class="ayuda">
          Estos son tus datos de estudiante. Si necesitas cambiarlos, pídele a tu apoderado
          que lo haga desde su propia Configuración.
        </p>
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
      .bloque {
        max-width: 480px;
        margin-bottom: 1.25rem;

        h3 {
          margin-top: 0;
        }
      }
      .ayuda {
        color: var(--texto-secundario);
        font-size: 0.85rem;
      }
    `,
  ],
})
export class Configuracion {
  @Input() contexto: 'alumno' | 'apoderado' = 'alumno';

  sesion = inject(SesionService);

  nombreAlumno(): string {
    const perfil = this.sesion.perfilActivo();
    return perfil ? `${perfil.nombre} ${perfil.apellidos}` : '';
  }
}
