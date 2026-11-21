import { Component, inject, signal } from '@angular/core';
import { RouterLink } from '@angular/router';
import { FormsModule } from '@angular/forms';
import { AuthLayout } from '../../shared/auth-layout/auth-layout';
import { AuthService } from '../../core/auth.service';

/** «¿Olvidaste tu contraseña?» (2026-11-21): pide el enlace por correo. La respuesta es la misma exista o no la cuenta. */
@Component({
  selector: 'app-recuperar-password',
  standalone: true,
  imports: [RouterLink, FormsModule, AuthLayout],
  template: `
    <app-auth-layout titulo="¿Olvidaste tu contraseña?" subtitulo="Te enviaremos un enlace para crear una nueva.">
      @if (enviado()) {
        <p class="aviso" role="status">
          Si <strong>{{ email }}</strong> está registrado, te llegará un correo con el enlace en unos minutos.
          Revisa también la carpeta de spam. El enlace vence en 1 hora.
        </p>
      } @else {
        <form (submit)="$event.preventDefault(); enviar()">
          <div class="campo">
            <label for="email-recuperar">Correo electrónico de tu cuenta</label>
            <input id="email-recuperar" type="email" [(ngModel)]="email" name="email" placeholder="tucorreo@ejemplo.com" required />
          </div>
          @if (error()) {
            <p class="error">{{ error() }}</p>
          }
          <button type="submit" class="btn btn--primario btn--bloque btn--grande" [disabled]="cargando()">
            {{ cargando() ? 'Enviando…' : 'Enviar enlace' }}
          </button>
        </form>
      }
      <p class="auth__pie"><a routerLink="/login">Volver a iniciar sesión</a></p>
    </app-auth-layout>
  `,
  styles: [
    `
      .aviso { background: var(--fondo-suave, #f4f3ff); border-radius: 12px; padding: 1rem; line-height: 1.5; }
      .error { color: var(--color-error-texto); font-size: 0.85rem; margin: -0.5rem 0 1rem; }
      .auth__pie { margin-top: 1.5rem; text-align: center; font-size: 0.9rem;
        a { color: var(--color-primario); font-weight: 600; text-decoration: none; } }
    `,
  ],
})
export class RecuperarPassword {
  email = '';
  cargando = signal(false);
  enviado = signal(false);
  error = signal('');
  private auth = inject(AuthService);

  enviar() {
    if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(this.email.trim())) {
      this.error.set('Escribe un correo válido.');
      return;
    }
    this.cargando.set(true);
    this.error.set('');
    this.auth.recuperarPassword(this.email.trim()).subscribe({
      next: () => { this.cargando.set(false); this.enviado.set(true); },
      error: (e) => {
        this.cargando.set(false);
        this.error.set(e?.status === 429 ? 'Hiciste muchas solicitudes seguidas. Espera un minuto y vuelve a intentar.' : 'No pudimos enviar el enlace. Intenta de nuevo.');
      },
    });
  }
}
