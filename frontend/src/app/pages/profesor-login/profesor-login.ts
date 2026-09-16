import { Component, inject, signal } from '@angular/core';
import { Router } from '@angular/router';
import { FormsModule } from '@angular/forms';
import { AuthLayout } from '../../shared/auth-layout/auth-layout';
import { ProfesorAuthService } from '../../core/profesor-auth.service';
import { SesionProfesorService } from '../../core/sesion-profesor.service';

@Component({
  selector: 'app-profesor-login',
  standalone: true,
  imports: [FormsModule, AuthLayout],
  template: `
    <app-auth-layout
      [titulo]="modoRegistro() ? 'Crear cuenta de Profesor' : 'Acceso Profesores'"
      subtitulo="Logos School — gestiona tus cursos y el avance de tus alumnos."
    >
      @if (modoRegistro()) {
        <p class="aviso">Tu cuenta quedará en revisión — un administrador la aprobará antes de que puedas crear cursos.</p>
      }
      <form (submit)="$event.preventDefault(); enviar()">
        @if (modoRegistro()) {
          <div class="campo">
            <label>Nombre</label>
            <input type="text" [(ngModel)]="nombre" name="nombre" placeholder="Tu nombre completo" />
          </div>
        }
        <div class="campo">
          <label>Correo electrónico</label>
          <input type="email" [(ngModel)]="email" name="email" placeholder="profesor@colegio.cl" />
        </div>
        <div class="campo">
          <label>Contraseña</label>
          <input type="password" [(ngModel)]="password" name="password" placeholder="••••••••" />
        </div>
        @if (error()) {
          <p class="error">{{ error() }}</p>
        }
        <button type="submit" class="btn btn--primario btn--bloque btn--grande" [disabled]="cargando()">
          {{ cargando() ? 'Un momento…' : (modoRegistro() ? 'Crear cuenta' : 'Iniciar sesión') }}
        </button>
      </form>
      <p class="auth__pie">
        @if (modoRegistro()) {
          ¿Ya tienes cuenta? <a href="#" (click)="cambiarModo($event)">Inicia sesión</a>
        } @else {
          ¿Eres profesor y no tienes cuenta? <a href="#" (click)="cambiarModo($event)">Crear cuenta</a>
        }
      </p>
    </app-auth-layout>
  `,
  styles: [
    `
      .error {
        color: var(--color-error-texto);
        font-size: 0.85rem;
        margin: -0.5rem 0 1rem;
      }
      .aviso {
        background: var(--color-primario-suave);
        color: var(--color-primario);
        padding: 0.75rem 1rem;
        border-radius: var(--radio-media);
        font-size: 0.85rem;
        margin-bottom: 1rem;
      }
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
    `,
  ],
})
export class ProfesorLogin {
  email = '';
  password = '';
  nombre = '';
  modoRegistro = signal(false);
  cargando = signal(false);
  error = signal('');

  private profesorAuth = inject(ProfesorAuthService);
  private sesion = inject(SesionProfesorService);
  private router = inject(Router);

  cambiarModo(evento: Event) {
    evento.preventDefault();
    this.modoRegistro.set(!this.modoRegistro());
    this.error.set('');
  }

  enviar() {
    if (this.modoRegistro()) this.registrar();
    else this.ingresar();
  }

  private ingresar() {
    this.error.set('');
    this.cargando.set(true);
    this.profesorAuth.login(this.email, this.password).subscribe({
      next: (r) => {
        this.sesion.guardarToken(r.access_token);
        this.profesorAuth.yo().subscribe((cuenta) => this.sesion.setNombre(cuenta.nombre));
        this.router.navigate(['/profesor/dashboard']);
      },
      error: () => {
        this.cargando.set(false);
        this.error.set('Correo o contraseña incorrectos.');
      },
    });
  }

  private registrar() {
    this.error.set('');
    this.cargando.set(true);
    this.profesorAuth.registrar(this.email, this.password, this.nombre).subscribe({
      next: (r) => {
        this.sesion.guardarToken(r.access_token);
        this.profesorAuth.yo().subscribe((cuenta) => this.sesion.setNombre(cuenta.nombre));
        this.router.navigate(['/profesor/dashboard']);
      },
      error: (err) => {
        this.cargando.set(false);
        this.error.set(err?.error?.detail || 'No se pudo crear la cuenta.');
      },
    });
  }
}
