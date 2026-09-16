import { HttpClient } from '@angular/common/http';
import { Injectable, inject } from '@angular/core';
import { Observable } from 'rxjs';
import { environment } from '../../environments/environment';

export interface AnimoDeHoy {
  registrado: boolean;
  estado: string | null;
  fecha: string | null;
  estados_disponibles: string[];
}

@Injectable({ providedIn: 'root' })
export class BienestarService {
  private http = inject(HttpClient);
  private base = environment.apiUrl;

  obtenerAnimoDeHoy(perfilAlumnoId: number): Observable<AnimoDeHoy> {
    return this.http.get<AnimoDeHoy>(`${this.base}/bienestar/${perfilAlumnoId}/hoy`);
  }

  registrarAnimo(perfilAlumnoId: number, estado: string): Observable<AnimoDeHoy> {
    return this.http.post<AnimoDeHoy>(`${this.base}/bienestar/${perfilAlumnoId}/hoy`, { estado });
  }
}
