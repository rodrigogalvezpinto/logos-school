import { Component, inject, signal } from '@angular/core';
import { ActivatedRoute, Router, RouterLink } from '@angular/router';
import { FormsModule } from '@angular/forms';
import { AuthLayout } from '../../shared/auth-layout/auth-layout';
import { AuthService } from '../../core/auth.service';

/** Página del enlace del correo (/restablecer?token=…): crea la contraseña nueva. */
@Component({
  selector: 'app-restablecer-password',
  standalone: true,
  imports: [RouterLink, FormsModule, AuthLayout],
  template: `
    <app-auth-layout titulo="Crea tu contraseña nueva" subtitulo="Al guardarla se cerrarán las sesiones abiertas.">
      @if (!token) {
        <p class="error">El enlace está incompleto. <a routerLink="/recuperar">Pide uno nuevo</a>.</p>
      } @else if (listo()) {
        <p class="aviso" role="status">¡Listo! Tu contraseña cambió. Ya puedes iniciar sesión con la nueva.</p>
        <a routerLink="/login" class="btn btn--primario btn--bloque btn--grande">Iniciar sesión</a>
      } @else {
        <form (submit)="$event.preventDefault(); guardar()">
          <div class="campo">
            <label for="pass-nueva">Contraseña nueva (mínimo 8 caracteres)</label>
            <input id="pass-nueva" type="password" [(ngModel)]="password" name="password" autocomplete="new-password" />
          </div>
          <div class="campo">
            <label for="pass-repetir">Repite la contraseña</label>
            <input id="pass-repetir" type="password" [(ngModel)]="repetir" name="repetir" autocomplete="new-password" />
          </div>
          @if (error()) {
            <p class="error">{{ error() }}
              @if (enlaceInvalido()) { <a routerLink="/recuperar">Pedir un enlace nuevo</a> }
            </p>
          }
          <button type="submit" class="btn btn--primario btn--bloque btn--grande" [disabled]="cargando()">
            {{ cargando() ? 'Guardando…' : 'Guardar contraseña' }}
          </button>
        </form>
      }
    </app-auth-layout>
  `,
  styles: [
    `
      .aviso { background: var(--fondo-suave, #f4f3ff); border-radius: 12px; padding: 1rem; line-height: 1.5; margin-bottom: 1rem; }
      .error { color: var(--color-error-texto); font-size: 0.85rem; margin: -0.5rem 0 1rem;
        a { color: var(--color-primario); font-weight: 600; } }
    `,
  ],
})
export class RestablecerPassword {
  readonly token = inject(ActivatedRoute).snapshot.queryParamMap.get('token') ?? '';
  password = '';
  repetir = '';
  cargando = signal(false);
  listo = signal(false);
  error = signal('');
  enlaceInvalido = signal(false);
  private auth = inject(AuthService);
  private router = inject(Router);

  constructor() {
    // El token no debe quedar en el historial ni en el Referer: se limpia de la barra de direcciones.
    if (this.token) this.router.navigate([], { queryParams: {}, replaceUrl: true });
  }

  guardar() {
    this.enlaceInvalido.set(false);
    if (this.password.length < 8) return this.error.set('La contraseña debe tener al menos 8 caracteres.');
    if (this.password !== this.repetir) return this.error.set('Las dos contraseñas no coinciden.');
    this.cargando.set(true);
    this.error.set('');
    this.auth.restablecerPassword(this.token, this.password).subscribe({
      next: () => { this.cargando.set(false); this.listo.set(true); },
      error: (e) => {
        this.cargando.set(false);
        if (e?.status === 400) { this.enlaceInvalido.set(true); this.error.set('El enlace venció o ya se usó.'); }
        else this.error.set('No pudimos guardar la contraseña. Intenta de nuevo.');
      },
    });
  }
}
