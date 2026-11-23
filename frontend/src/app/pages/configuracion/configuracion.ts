import { Component, Input, inject, signal } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { Router } from '@angular/router';
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
          <input id="nombre-apoderado" type="text" [value]="sesion.nombreApoderado()" disabled />
        </div>
      </div>

      <div class="tarjeta bloque">
        <h3>Cambiar contraseña</h3>
        <form (submit)="$event.preventDefault(); cambiarPassword()">
          <div class="campo">
            <label for="pass-actual">Contraseña actual</label>
            <input id="pass-actual" type="password" [(ngModel)]="passActual" name="passActual" autocomplete="current-password" />
          </div>
          <div class="campo">
            <label for="pass-nueva">Contraseña nueva (mínimo 8 caracteres)</label>
            <input id="pass-nueva" type="password" [(ngModel)]="passNueva" name="passNueva" autocomplete="new-password" />
          </div>
          <div class="campo">
            <label for="pass-repetir">Repite la contraseña nueva</label>
            <input id="pass-repetir" type="password" [(ngModel)]="passRepetir" name="passRepetir" autocomplete="new-password" />
          </div>
          @if (errorPass()) { <p class="error">{{ errorPass() }}</p> }
          @if (passCambiada()) { <p class="confirmacion" role="status">✓ Contraseña cambiada. Cerramos las sesiones en otros equipos.</p> }
          <button type="submit" class="btn btn--primario" [disabled]="cargandoPass()">
            {{ cargandoPass() ? 'Guardando…' : 'Cambiar contraseña' }}
          </button>
        </form>
      </div>

      <div class="tarjeta bloque bloque--peligro">
        <h3>Eliminar mi cuenta</h3>
        <p class="ayuda">
          Borra tu cuenta y la de cada alumno, con todo su historial: notas, progreso y plan de estudio.
          No se puede deshacer. Para borrar solo a un alumno, hazlo desde «Mis Alumnos».
        </p>
        @if (!confirmandoEliminar()) {
          <button class="btn btn--peligro" (click)="confirmandoEliminar.set(true)">Eliminar mi cuenta</button>
        } @else {
          <form (submit)="$event.preventDefault(); eliminarCuenta()">
            <div class="campo">
              <label for="pass-eliminar">Escribe tu contraseña para confirmar</label>
              <input id="pass-eliminar" type="password" [(ngModel)]="passEliminar" name="passEliminar" autocomplete="current-password" />
            </div>
            <p class="ayuda">¿Entraste solo con Google? Escribe tu correo en vez de la contraseña.</p>
            @if (errorEliminar()) { <p class="error">{{ errorEliminar() }}</p> }
            <div class="acciones">
              <button type="button" class="btn btn--secundario" (click)="confirmandoEliminar.set(false)">Cancelar</button>
              <button type="submit" class="btn btn--peligro" [disabled]="!passEliminar.trim() || cargandoEliminar()">
                Eliminar definitivamente
              </button>
            </div>
          </form>
        }
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
      .error {
        color: var(--color-error-texto);
        font-size: 0.85rem;
      }
      .bloque--peligro {
        border: 1.5px solid var(--color-error-texto);
      }
      .btn--peligro {
        background: var(--color-error-texto);
        color: #fff;
        border: none;
      }
      .acciones {
        display: flex;
        gap: 0.75rem;
        flex-wrap: wrap;
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
  passActual = '';
  passNueva = '';
  passRepetir = '';
  passEliminar = '';
  cargandoPass = signal(false);
  passCambiada = signal(false);
  errorPass = signal('');
  confirmandoEliminar = signal(false);
  cargandoEliminar = signal(false);
  errorEliminar = signal('');
  private router = inject(Router);
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

  cambiarPassword() {
    this.passCambiada.set(false);
    if (this.passNueva.length < 8) return this.errorPass.set('La contraseña nueva debe tener al menos 8 caracteres.');
    if (this.passNueva !== this.passRepetir) return this.errorPass.set('Las dos contraseñas nuevas no coinciden.');
    this.errorPass.set('');
    this.cargandoPass.set(true);
    this.auth.cambiarPassword(this.passActual, this.passNueva).subscribe({
      next: (r) => {
        this.sesion.guardarToken(r.access_token);
        this.cargandoPass.set(false);
        this.passCambiada.set(true);
        this.passActual = this.passNueva = this.passRepetir = '';
      },
      error: (e) => {
        this.cargandoPass.set(false);
        this.errorPass.set(e?.status === 400 ? 'La contraseña actual no es correcta.' : 'No pudimos cambiar la contraseña. Intenta de nuevo.');
      },
    });
  }

  eliminarCuenta() {
    const valor = this.passEliminar.trim();
    const esCorreo = /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(valor);
    this.cargandoEliminar.set(true);
    this.errorEliminar.set('');
    this.auth.eliminarCuenta(esCorreo ? { confirmacion_email: valor, password: this.passEliminar } : { password: this.passEliminar }).subscribe({
      next: () => {
        this.sesion.cerrarSesion();
        this.router.navigate(['/']);
      },
      error: (e) => {
        this.cargandoEliminar.set(false);
        this.errorEliminar.set(e?.status === 400 ? 'La confirmación no es correcta.' : 'No pudimos eliminar la cuenta. Intenta de nuevo.');
      },
    });
  }
}
