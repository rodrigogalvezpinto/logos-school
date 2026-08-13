import { HttpClient } from '@angular/common/http';
import { Injectable, inject } from '@angular/core';
import { Observable } from 'rxjs';
import { environment } from '../../environments/environment';

export interface TokenProfesorRespuesta {
  access_token: string;
  token_type: string;
}

export interface CuentaProfesorRespuesta {
  id: number;
  email: string;
  nombre: string;
  estado: 'pendiente' | 'aprobado' | 'rechazado';
}

@Injectable({ providedIn: 'root' })
export class ProfesorAuthService {
  private http = inject(HttpClient);
  private base = environment.apiUrl;

  registrar(email: string, password: string, nombre: string): Observable<TokenProfesorRespuesta> {
    return this.http.post<TokenProfesorRespuesta>(`${this.base}/profesor/auth/registro`, { email, password, nombre });
  }

  login(email: string, password: string): Observable<TokenProfesorRespuesta> {
    return this.http.post<TokenProfesorRespuesta>(`${this.base}/profesor/auth/login`, { email, password });
  }

  yo(): Observable<CuentaProfesorRespuesta> {
    return this.http.get<CuentaProfesorRespuesta>(`${this.base}/profesor/auth/yo`);
  }
}
