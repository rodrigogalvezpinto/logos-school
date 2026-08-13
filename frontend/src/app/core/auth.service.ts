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
}

export interface PlanRespuesta {
  id: number;
  nombre: string;
  precio_clp: number;
}

export interface PruebaGratisRespuesta {
  fecha_termino: string;
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

  yo(): Observable<CuentaRespuesta> {
    return this.http.get<CuentaRespuesta>(`${this.base}/auth/yo`);
  }

  agregarAlumno(datos: CrearPerfilAlumno): Observable<PerfilAlumnoRespuesta> {
    return this.http.post<PerfilAlumnoRespuesta>(`${this.base}/auth/alumnos`, datos);
  }

  listarAlumnos(): Observable<PerfilAlumnoRespuesta[]> {
    return this.http.get<PerfilAlumnoRespuesta[]>(`${this.base}/auth/alumnos`);
  }

  listarPlanes(): Observable<PlanRespuesta[]> {
    return this.http.get<PlanRespuesta[]>(`${this.base}/auth/planes`);
  }

  iniciarPruebaGratis(perfilAlumnoId: number, planId: number): Observable<PruebaGratisRespuesta> {
    return this.http.post<PruebaGratisRespuesta>(`${this.base}/auth/alumnos/${perfilAlumnoId}/prueba-gratis`, {
      plan_id: planId,
    });
  }
}
