import { Component } from '@angular/core';

@Component({
  selector: 'app-configuracion',
  standalone: true,
  template: `
    <h1>Configuración</h1>
    <p class="subtitulo">Datos de tu cuenta y privacidad.</p>

    <div class="tarjeta bloque">
      <h3>Datos de la cuenta</h3>
      <div class="campo">
        <label>Nombre</label>
        <input type="text" value="Rodrigo Galvez" />
      </div>
      <div class="campo">
        <label>Correo electrónico</label>
        <input type="email" value="rodrigo&#64;ejemplo.com" />
      </div>
      <button class="btn btn--primario">Guardar cambios</button>
    </div>

    <div class="tarjeta bloque">
      <h3>Privacidad</h3>
      <p>Puedes exportar o eliminar los datos de cualquier alumno vinculado a tu cuenta.</p>
      <button class="btn btn--secundario">Exportar mis datos</button>
    </div>
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
    `,
  ],
})
export class Configuracion {}
