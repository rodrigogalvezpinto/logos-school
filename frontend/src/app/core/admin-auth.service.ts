import { HttpClient } from '@angular/common/http';
import { Injectable, inject } from '@angular/core';
import { Observable } from 'rxjs';
import { environment } from '../../environments/environment';

export interface TokenAdminRespuesta {
  access_token: string;
  token_type: string;
}

export interface CuentaAdminRespuesta {
  id: number;
  email: string;
  nombre: string;
}

@Injectable({ providedIn: 'root' })
export class AdminAuthService {
  private http = inject(HttpClient);
  private base = environment.apiUrl;

  login(email: string, password: string): Observable<TokenAdminRespuesta> {
    return this.http.post<TokenAdminRespuesta>(`${this.base}/admin/auth/login`, { email, password });
  }

  yo(): Observable<CuentaAdminRespuesta> {
    return this.http.get<CuentaAdminRespuesta>(`${this.base}/admin/auth/yo`);
  }
}
