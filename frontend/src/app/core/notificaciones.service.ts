import { HttpClient } from '@angular/common/http';
import { Injectable, inject } from '@angular/core';
import { Observable } from 'rxjs';
import { environment } from '../../environments/environment';

export interface Notificacion {
  tipo: 'comunicado' | 'sesion_atrasada' | 'reporte_resuelto';
  titulo: string;
  detalle: string;
  fecha: string;
}

@Injectable({ providedIn: 'root' })
export class NotificacionesService {
  private http = inject(HttpClient);
  private base = environment.apiUrl;

  listar(perfilAlumnoId: number): Observable<Notificacion[]> {
    return this.http.get<Notificacion[]>(`${this.base}/notificaciones/${perfilAlumnoId}`);
  }
}
