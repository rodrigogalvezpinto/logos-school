import { Injectable, signal } from '@angular/core';

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
