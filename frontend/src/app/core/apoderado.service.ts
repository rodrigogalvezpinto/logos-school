import { HttpClient } from '@angular/common/http';
import { Injectable, inject } from '@angular/core';
import { Observable } from 'rxjs';
import { environment } from '../../environments/environment';

export interface EstadisticaAlumno {
  perfil_alumno_id: number;
  nombre: string;
  cobertura_pct: number;
  racha_dias_actual: number;
  tiene_alerta_de_ritmo: boolean;
}

export interface MetaFamiliar {
  dias_esta_semana: number;
  dias_semana_anterior: number;
  es_nueva_marca: boolean;
}

export interface AgendaFamiliar {
  preguntas: string[];
  ya_conversada: boolean;
}

@Injectable({ providedIn: 'root' })
export class ApoderadoService {
  private http = inject(HttpClient);
  private base = environment.apiUrl;

  obtenerEstadisticas(): Observable<EstadisticaAlumno[]> {
    return this.http.get<EstadisticaAlumno[]>(`${this.base}/apoderado/estadisticas`);
  }

  obtenerMetaFamiliar(): Observable<MetaFamiliar | null> {
    return this.http.get<MetaFamiliar | null>(`${this.base}/apoderado/meta-familiar`);
  }

  obtenerAgendaFamiliar(perfilAlumnoId: number): Observable<AgendaFamiliar> {
    return this.http.get<AgendaFamiliar>(`${this.base}/apoderado/agenda-familiar/${perfilAlumnoId}`);
  }

  marcarAgendaFamiliarConversada(perfilAlumnoId: number): Observable<void> {
    return this.http.post<void>(`${this.base}/apoderado/agenda-familiar/${perfilAlumnoId}/conversada`, {});
  }
}
