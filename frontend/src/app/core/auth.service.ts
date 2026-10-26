import { HttpClient } from '@angular/common/http';
import { Injectable, inject } from '@angular/core';
import { Observable } from 'rxjs';
import { environment } from '../../environments/environment';

export interface TokenRespuesta {
  access_token: string;
  token_type: string;
}

export interface CuentaRespuesta {
  id: number;
  email: string;
  nombre: string;
}

export interface CrearPerfilAlumno {
  nombre: string;
  apellidos: string;
  fecha_nacimiento: string; // YYYY-MM-DD
  rut: string;
  nivel_id: number;
}

export interface PerfilAlumnoRespuesta {
  id: number;
  nombre: string;
  apellidos: string;
  nivel_id: number;
  nombre_nivel?: string;
}

export interface PlanRespuesta {
  id: number;
  nombre: string;
  precio_clp: number;
}

export interface PruebaGratisRespuesta {
  fecha_termino: string;
}

export interface SuscripcionRespuesta {
  plan_id: number;
  plan_nombre: string;
  fecha_inicio: string;
  fecha_termino: string | null;
  estado: string;
  origen: string;
}

@Injectable({ providedIn: 'root' })
export class AuthService {
  private http = inject(HttpClient);
  private base = environment.apiUrl;

  registrar(email: string, password: string, nombre: string): Observable<TokenRespuesta> {
    return this.http.post<TokenRespuesta>(`${this.base}/auth/registro`, { email, password, nombre });
  }

  login(email: string, password: string): Observable<TokenRespuesta> {
    return this.http.post<TokenRespuesta>(`${this.base}/auth/login`, { email, password });
  }

  loginConGoogle(idToken: string): Observable<TokenRespuesta> {
    return this.http.post<TokenRespuesta>(`${this.base}/auth/login-google`, { id_token: idToken });
  }

  yo(): Observable<CuentaRespuesta> {
    return this.http.get<CuentaRespuesta>(`${this.base}/auth/yo`);
  }

  agregarAlumno(datos: CrearPerfilAlumno): Observable<PerfilAlumnoRespuesta> {
    return this.http.post<PerfilAlumnoRespuesta>(`${this.base}/auth/alumnos`, datos);
  }

  listarAlumnos(): Observable<PerfilAlumnoRespuesta[]> {
    return this.http.get<PerfilAlumnoRespuesta[]>(`${this.base}/auth/alumnos`);
  }

  eliminarAlumno(perfilAlumnoId: number): Observable<void> {
    return this.http.delete<void>(`${this.base}/auth/alumnos/${perfilAlumnoId}`);
  }

  listarPlanes(): Observable<PlanRespuesta[]> {
    return this.http.get<PlanRespuesta[]>(`${this.base}/auth/planes`);
  }

  iniciarPruebaGratis(perfilAlumnoId: number, planId: number): Observable<PruebaGratisRespuesta> {
    return this.http.post<PruebaGratisRespuesta>(`${this.base}/auth/alumnos/${perfilAlumnoId}/prueba-gratis`, {
      plan_id: planId,
    });
  }

  obtenerSuscripcion(perfilAlumnoId: number): Observable<SuscripcionRespuesta | null> {
    return this.http.get<SuscripcionRespuesta | null>(`${this.base}/auth/alumnos/${perfilAlumnoId}/suscripcion`);
  }

  descargarCertificado(perfilAlumnoId: number): Observable<Blob> {
    // Blob, no un <a href> directo: el endpoint exige sesión (Bearer token vía
    // auth-interceptor), y una navegación de navegador normal no manda ese header.
    return this.http.get(`${this.base}/auth/alumnos/${perfilAlumnoId}/certificado.pdf`, { responseType: 'blob' });
  }

  descargarInformeAvance(perfilAlumnoId: number): Observable<Blob> {
    return this.http.get(`${this.base}/auth/alumnos/${perfilAlumnoId}/informe-avance.pdf`, { responseType: 'blob' });
  }
}
