import { Component, inject, signal } from '@angular/core';
import { Router } from '@angular/router';
import { FormsModule } from '@angular/forms';
import { AuthLayout } from '../../shared/auth-layout/auth-layout';
import { AdminAuthService } from '../../core/admin-auth.service';
import { SesionAdminService } from '../../core/sesion-admin.service';

@Component({
  selector: 'app-admin-login',
  standalone: true,
  imports: [FormsModule, AuthLayout],
  template: `
    <app-auth-layout titulo="Panel de Administración" subtitulo="Acceso restringido — Logos School.">
      <form (submit)="$event.preventDefault(); ingresar()">
        <div class="campo">
          <label>Correo electrónico</label>
          <input type="email" [(ngModel)]="email" name="email" placeholder="admin@logos.cl" />
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
    </app-auth-layout>
  `,
  styles: [
    `
      .error {
        color: var(--color-error);
        font-size: 0.85rem;
        margin: -0.5rem 0 1rem;
      }
    `,
  ],
})
export class AdminLogin {
  email = '';
  password = '';
  cargando = signal(false);
  error = signal('');

  private adminAuth = inject(AdminAuthService);
  private sesion = inject(SesionAdminService);
  private router = inject(Router);

  ingresar() {
    this.error.set('');
    this.cargando.set(true);
    this.adminAuth.login(this.email, this.password).subscribe({
      next: (r) => {
        this.sesion.guardarToken(r.access_token);
        this.adminAuth.yo().subscribe((cuenta) => this.sesion.setNombre(cuenta.nombre));
        this.router.navigate(['/admin/dashboard']);
      },
      error: () => {
        this.cargando.set(false);
        this.error.set('Correo o contraseña incorrectos.');
      },
    });
  }
}
