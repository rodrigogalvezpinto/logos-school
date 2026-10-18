import { Component, Input, inject, signal } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { AuthService } from '../../core/auth.service';
import { SesionService } from '../../core/sesion.service';
import { SugerenciasService } from '../../core/sugerencias.service';

@Component({
  selector: 'app-configuracion',
  standalone: true,
  imports: [FormsModule],
  template: `
    <h1>Configuración</h1>
    <p class="subtitulo">Datos de tu cuenta y privacidad.</p>

    @if (contexto === 'apoderado') {
      <div class="tarjeta bloque">
        <h3>Datos de la cuenta</h3>
        <div class="campo">
          <label for="nombre-apoderado">Nombre</label>
          <input id="nombre-apoderado" type="text" [value]="sesion.nombreApoderado()" />
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
          <label for="nombre-alumno">Nombre</label>
          <input id="nombre-alumno" type="text" [value]="nombreAlumno()" disabled />
        </div>
        <p class="ayuda">
          Estos son tus datos de estudiante. Si necesitas cambiarlos, pídele a tu apoderado
          que lo haga desde su propia Configuración.
        </p>
      </div>

      <div class="tarjeta bloque">
        <h3>Certificado de alumno regular</h3>
        <p class="ayuda">
          Una constancia de que estás inscrito y estudiando en Logos School — no reemplaza
          ni certifica la aprobación del Examen Libre, que emite el Ministerio de Educación.
        </p>
        <button class="btn btn--secundario" (click)="descargarCertificado()">⬇ Descargar certificado en PDF</button>
      </div>

      <div class="tarjeta bloque">
        <h3>Ideas para mejorar Logos School</h3>
        <label for="texto-sugerencia" class="ayuda">¿Se te ocurre algo que nos falta o que podríamos hacer mejor? Cuéntanos.</label>
        <textarea
          id="texto-sugerencia"
          rows="3"
          placeholder="Escribe tu idea…"
          [(ngModel)]="textoSugerencia"
          name="sugerencia"
        ></textarea>
        <button class="btn btn--secundario" [disabled]="!textoSugerencia.trim()" (click)="enviarSugerencia()">
          Enviar sugerencia
        </button>
        @if (sugerenciaEnviada()) {
          <p class="confirmacion">✓ ¡Gracias! La leímos.</p>
        }
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
        display: block;
        color: var(--texto-secundario);
        font-size: 0.85rem;
      }
      textarea {
        width: 100%;
        padding: 0.6rem 0.75rem;
        border: 1.5px solid var(--borde);
        border-radius: var(--radio-media);
        background: var(--fondo-tarjeta, #fff);
        color: var(--texto-principal);
        font-family: inherit;
        font-size: 0.9rem;
        margin-bottom: 0.75rem;
        resize: vertical;
      }
      .confirmacion {
        margin: 0.75rem 0 0;
        color: var(--color-exito-texto);
        font-size: 0.85rem;
      }
    `,
  ],
})
export class Configuracion {
  @Input() contexto: 'alumno' | 'apoderado' = 'alumno';

  textoSugerencia = '';
  sugerenciaEnviada = signal(false);

  sesion = inject(SesionService);
  private auth = inject(AuthService);
  private sugerencias = inject(SugerenciasService);

  nombreAlumno(): string {
    const perfil = this.sesion.perfilActivo();
    return perfil ? `${perfil.nombre} ${perfil.apellidos}` : '';
  }

  descargarCertificado() {
    const perfil = this.sesion.perfilActivo();
    if (!perfil) return;
    this.auth.descargarCertificado(perfil.id).subscribe((blob) => {
      const url = window.URL.createObjectURL(blob);
      window.open(url, '_blank');
    });
  }

  enviarSugerencia() {
    const perfil = this.sesion.perfilActivo();
    if (!perfil || !this.textoSugerencia.trim()) return;
    this.sugerencias.enviar(perfil.id, this.textoSugerencia).subscribe(() => {
      this.textoSugerencia = '';
      this.sugerenciaEnviada.set(true);
    });
  }
}
