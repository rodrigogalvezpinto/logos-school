import { Injectable, signal } from '@angular/core';

const CLAVE_TOKEN_PROFESOR = 'logos_profesor_token';
const CLAVE_NOMBRE_PROFESOR = 'logos_profesor_nombre';

@Injectable({ providedIn: 'root' })
export class SesionProfesorService {
  // Sesión completamente separada de SesionService (Apoderado/Alumno) y de
  // SesionAdminService — mismo criterio ya aplicado dos veces: un Profesor no es una
  // familia ni el dueño del proyecto, con su propio tipo de token en el backend.
  token = signal<string | null>(localStorage.getItem(CLAVE_TOKEN_PROFESOR));
  nombre = signal<string>(localStorage.getItem(CLAVE_NOMBRE_PROFESOR) || '');

  guardarToken(token: string) {
    localStorage.setItem(CLAVE_TOKEN_PROFESOR, token);
    this.token.set(token);
  }

  setNombre(nombre: string) {
    localStorage.setItem(CLAVE_NOMBRE_PROFESOR, nombre);
    this.nombre.set(nombre);
  }

  cerrarSesion() {
    localStorage.removeItem(CLAVE_TOKEN_PROFESOR);
    localStorage.removeItem(CLAVE_NOMBRE_PROFESOR);
    this.token.set(null);
    this.nombre.set('');
  }
}
