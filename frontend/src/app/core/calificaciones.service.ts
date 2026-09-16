import { HttpClient } from '@angular/common/http';
import { Injectable, inject } from '@angular/core';
import { Observable } from 'rxjs';
import { environment } from '../../environments/environment';

export interface Calificacion {
  oa_id: number;
  estrellas: number;
  fecha: string;
}

@Injectable({ providedIn: 'root' })
export class CalificacionesService {
  private http = inject(HttpClient);
  private base = environment.apiUrl;

  calificar(perfilAlumnoId: number, oaId: number, estrellas: number): Observable<Calificacion> {
    return this.http.put<Calificacion>(`${this.base}/calificaciones/${perfilAlumnoId}/guias/${oaId}`, { estrellas });
  }

  obtenerMiCalificacion(perfilAlumnoId: number, oaId: number): Observable<Calificacion | null> {
    return this.http.get<Calificacion | null>(`${this.base}/calificaciones/${perfilAlumnoId}/guias/${oaId}`);
  }
}
