import { Injectable, signal } from '@angular/core';

const CLAVE_TOKEN_ADMIN = 'logos_admin_token';
const CLAVE_NOMBRE_ADMIN = 'logos_admin_nombre';

@Injectable({ providedIn: 'root' })
export class SesionAdminService {
  // Sesión completamente separada de SesionService (Apoderado/Alumno) — mismas razones
  // que la separación de token en el backend: un panel administrativo no es una "familia".
  token = signal<string | null>(localStorage.getItem(CLAVE_TOKEN_ADMIN));
  nombre = signal<string>(localStorage.getItem(CLAVE_NOMBRE_ADMIN) || '');

  guardarToken(token: string) {
    localStorage.setItem(CLAVE_TOKEN_ADMIN, token);
    this.token.set(token);
  }

  setNombre(nombre: string) {
    localStorage.setItem(CLAVE_NOMBRE_ADMIN, nombre);
    this.nombre.set(nombre);
  }

  cerrarSesion() {
    localStorage.removeItem(CLAVE_TOKEN_ADMIN);
    localStorage.removeItem(CLAVE_NOMBRE_ADMIN);
    this.token.set(null);
    this.nombre.set('');
  }
}
