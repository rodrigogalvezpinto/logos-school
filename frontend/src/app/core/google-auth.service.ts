import { Injectable, inject } from '@angular/core';
import { environment } from '../../environments/environment';
import { AuthService, TokenRespuesta } from './auth.service';

declare const google: any;

@Injectable({ providedIn: 'root' })
export class GoogleAuthService {
  private auth = inject(AuthService);
  private scriptCargado = false;

  get estaConfigurado(): boolean {
    return Boolean(environment.googleClientId && environment.googleClientId.trim().length > 0);
  }

  inicializar(onExito: (token: TokenRespuesta) => void, onError: (err: string) => void) {
    if (!this.estaConfigurado) return;

    const ejecutarInit = () => {
      if (typeof google === 'undefined' || !google.accounts?.id) return;
      google.accounts.id.initialize({
        client_id: environment.googleClientId,
        callback: (respuesta: { credential?: string }) => {
          if (respuesta.credential) {
            this.auth.loginConGoogle(respuesta.credential).subscribe({
              next: (res) => onExito(res),
              error: (err) => onError(err?.error?.detail || 'Error al iniciar sesión con Google.'),
            });
          }
        },
      });
    };

    if (this.scriptCargado || (typeof google !== 'undefined' && google?.accounts?.id)) {
      ejecutarInit();
    } else {
      const script = document.createElement('script');
      script.src = 'https://accounts.google.com/gsi/client';
      script.async = true;
      script.defer = true;
      script.onload = () => {
        this.scriptCargado = true;
        ejecutarInit();
      };
      document.head.appendChild(script);
    }
  }

  solicitarLogin(onExito: (token: TokenRespuesta) => void, onError: (err: string) => void) {
    if (!this.estaConfigurado) {
      onError('Para iniciar sesión con Google, configura tu GOOGLE_CLIENT_ID en frontend/src/environments/environment.ts y backend/.env.');
      return;
    }
    this.inicializar(onExito, onError);
    if (typeof google !== 'undefined' && google.accounts?.id) {
      google.accounts.id.prompt();
    }
  }
}
