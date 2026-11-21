import { HttpClient } from '@angular/common/http';
import { Injectable, inject } from '@angular/core';
import { Observable } from 'rxjs';
import { environment } from '../../environments/environment';

export interface MensajeTutor {
  rol: 'alumno' | 'tutor';
  texto: string;
  derivacion?: boolean;
}

/** Profesor IA (tarea 14): solo existe si el backend lo tiene activado (clave de IA configurada). */
@Injectable({ providedIn: 'root' })
export class TutorIaService {
  private http = inject(HttpClient);
  private base = environment.apiUrl;

  estado(): Observable<{ habilitado: boolean }> {
    return this.http.get<{ habilitado: boolean }>(`${this.base}/tutor-ia/estado`);
  }

  preguntar(perfilId: number, oaId: number, mensajes: MensajeTutor[]): Observable<{ texto: string; derivacion: boolean }> {
    return this.http.post<{ texto: string; derivacion: boolean }>(`${this.base}/tutor-ia/${perfilId}/oa/${oaId}`, {
      mensajes: mensajes.map(({ rol, texto }) => ({ rol, texto })),
    });
  }
}
