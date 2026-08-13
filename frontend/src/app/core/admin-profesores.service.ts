import { HttpClient } from '@angular/common/http';
import { Injectable, inject } from '@angular/core';
import { Observable } from 'rxjs';
import { environment } from '../../environments/environment';

export interface CuentaProfesor {
  id: number;
  email: string;
  nombre: string;
  estado: 'pendiente' | 'aprobado' | 'rechazado';
}

@Injectable({ providedIn: 'root' })
export class AdminProfesoresService {
  private http = inject(HttpClient);
  private base = environment.apiUrl;

  listarPendientes(): Observable<CuentaProfesor[]> {
    return this.http.get<CuentaProfesor[]>(`${this.base}/admin/profesores/pendientes`);
  }

  aprobar(cuentaProfesorId: number): Observable<CuentaProfesor> {
    return this.http.post<CuentaProfesor>(`${this.base}/admin/profesores/${cuentaProfesorId}/aprobar`, {});
  }

  rechazar(cuentaProfesorId: number): Observable<CuentaProfesor> {
    return this.http.post<CuentaProfesor>(`${this.base}/admin/profesores/${cuentaProfesorId}/rechazar`, {});
  }
}
