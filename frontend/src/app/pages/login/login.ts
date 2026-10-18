import { Component, inject, signal } from '@angular/core';
import { Router, RouterLink } from '@angular/router';
import { FormsModule } from '@angular/forms';
import { AuthLayout } from '../../shared/auth-layout/auth-layout';
import { AuthService } from '../../core/auth.service';
import { SesionService } from '../../core/sesion.service';

@Component({
  selector: 'app-login',
  standalone: true,
  imports: [RouterLink, FormsModule, AuthLayout],
  template: `
    <app-auth-layout titulo="Bienvenido de nuevo" subtitulo="Ingresa para seguir estudiando.">
      <button class="btn-google" disabled title="Requiere configurar GOOGLE_CLIENT_ID (ver planificacion/17)">
        <svg width="18" height="18" viewBox="0 0 18 18"><path fill="#4285F4" d="M17.6 9.2c0-.6-.05-1.2-.15-1.75H9v3.3h4.8a4.1 4.1 0 0 1-1.78 2.7v2.2h2.9c1.7-1.55 2.68-3.85 2.68-6.45z"/><path fill="#34A853" d="M9 18c2.4 0 4.42-.8 5.9-2.15l-2.9-2.2c-.8.55-1.85.85-3 .85-2.3 0-4.25-1.55-4.95-3.65H1.05v2.3A9 9 0 0 0 9 18z"/><path fill="#FBBC05" d="M4.05 10.85a5.4 5.4 0 0 1 0-3.7v-2.3H1.05a9 9 0 0 0 0 8.3z"/><path fill="#EA4335" d="M9 3.6c1.3 0 2.47.45 3.4 1.32l2.55-2.55A8.7 8.7 0 0 0 9 0 9 9 0 0 0 1.05 4.85l3 2.3C4.75 5.05 6.7 3.6 9 3.6z"/></svg>
        Continuar con Google
      </button>
      <div class="divisor-o">o con tu correo</div>
      <form (submit)="$event.preventDefault(); continuar()">
        <div class="campo">
          <label>Correo electrónico</label>
          <input type="email" [(ngModel)]="email" name="email" placeholder="tucorreo@ejemplo.com" />
        </div>
        <div class="campo">
          <label>Contraseña</label>
          <input type="password" [(ngModel)]="password" name="password" placeholder="••••••••" />
        </div>
        @if (error()) {
          <p class="error">{{ error() }}</p>
        }
        <button type="submit" class="btn btn--primario btn--bloque btn--grande" [disabled]="cargando()">
          {{ cargando() ? 'Ingresando…' : 'Iniciar sesión' }}
        </button>
      </form>
      <p class="auth__pie">¿No tienes cuenta? <a routerLink="/registro">Crear cuenta</a></p>
    </app-auth-layout>
  `,
  styles: [
    `
      .auth__pie {
        margin-top: 1.5rem;
        text-align: center;
        color: var(--texto-secundario);
        font-size: 0.9rem;

        a {
          color: var(--color-primario);
          font-weight: 600;
          text-decoration: none;
        }
      }
      .error {
        color: var(--color-error-texto);
        font-size: 0.85rem;
        margin: -0.5rem 0 1rem;
      }
    `,
  ],
})
export class Login {
  email = '';
  password = '';
  cargando = signal(false);
  error = signal('');

  private auth = inject(AuthService);
  private sesion = inject(SesionService);
  private router = inject(Router);

  continuar() {
    this.error.set('');
    this.cargando.set(true);
    this.auth.login(this.email, this.password).subscribe({
      next: (r) => {
        this.sesion.guardarToken(r.access_token);
        this.auth.yo().subscribe((cuenta) => this.sesion.setNombreApoderado(cuenta.nombre));
        this.router.navigate(['/selector-perfil']);
      },
      error: () => {
        this.cargando.set(false);
        this.error.set('Correo o contraseña incorrectos.');
      },
    });
  }
}
