import { HttpClient } from '@angular/common/http';
import { Injectable, inject, signal } from '@angular/core';
import { environment } from '../../environments/environment';

export interface PerfilAlumnoActivo {
  id: number;
  nombre: string;
  apellidos: string;
  nivel_id: number;
}

const CLAVE_TOKEN = 'logos_token';
const CLAVE_PERFIL_ACTIVO = 'logos_perfil_activo';
const CLAVE_NOMBRE_APODERADO = 'logos_nombre_apoderado';

function leerPerfilGuardado(): PerfilAlumnoActivo | null {
  const crudo = localStorage.getItem(CLAVE_PERFIL_ACTIVO);
  if (!crudo) return null;
  try {
    return JSON.parse(crudo) as PerfilAlumnoActivo;
  } catch {
    return null;
  }
}

@Injectable({ providedIn: 'root' })
export class SesionService {
  // Persistidos en localStorage — sin esto, recargar la página o abrir en otra
  // pestaña pierde la sesión/el perfil elegido (bug real encontrado probando la app).
  token = signal<string | null>(localStorage.getItem(CLAVE_TOKEN));
  perfilActivo = signal<PerfilAlumnoActivo | null>(leerPerfilGuardado());
  nombreApoderado = signal<string>(localStorage.getItem(CLAVE_NOMBRE_APODERADO) || '');

  private http = inject(HttpClient);

  constructor() {
    // Mantiene localStorage sincronizado con cualquier cambio futuro de los signals.
  }

  guardarToken(token: string) {
    localStorage.setItem(CLAVE_TOKEN, token);
    this.token.set(token);
  }

  setNombreApoderado(nombre: string) {
    localStorage.setItem(CLAVE_NOMBRE_APODERADO, nombre);
    this.nombreApoderado.set(nombre);
  }

  cerrarSesion() {
    // Invalida el token en el servidor (fire-and-forget: si falla por red, igual se
    // borra localmente — no vale la pena bloquear el logout local por eso). Sin este
    // llamado, el token seguía siendo una credencial válida en el servidor hasta
    // expirar (hasta 12 horas) aunque el usuario ya hubiera "cerrado sesión".
    if (this.token()) {
      this.http.post(`${environment.apiUrl}/auth/logout`, {}).subscribe({ error: () => {} });
    }
    localStorage.removeItem(CLAVE_TOKEN);
    localStorage.removeItem(CLAVE_PERFIL_ACTIVO);
    localStorage.removeItem(CLAVE_NOMBRE_APODERADO);
    this.token.set(null);
    this.perfilActivo.set(null);
    this.nombreApoderado.set('');
  }

  elegirPerfil(perfil: PerfilAlumnoActivo) {
    localStorage.setItem(CLAVE_PERFIL_ACTIVO, JSON.stringify(perfil));
    this.perfilActivo.set(perfil);
  }
}
