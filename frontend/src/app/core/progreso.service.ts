import { HttpClient } from '@angular/common/http';
import { Injectable, inject } from '@angular/core';
import { Observable } from 'rxjs';
import { environment } from '../../environments/environment';

export interface ItemHistorial {
  intento_id: number;
  conjunto_id: number;
  tipo: 'prueba_unidad' | 'examen_simulacro';
  asignatura_id: number | null;
  asignatura_nombre: string | null;
  nombre: string;
  nota: number | null;
  fecha: string;
}

export interface GuiaRevisada {
  oa_id: number;
  fecha: string;
}

export interface NotaPorAsignatura {
  asignatura_id: number;
  asignatura_nombre: string;
  nota_practica: number | null;
  nota_simulacro: number | null;
}

export interface Historial {
  historial: ItemHistorial[];
  guias_revisadas: GuiaRevisada[];
  notas_por_asignatura: NotaPorAsignatura[];
}

@Injectable({ providedIn: 'root' })
export class ProgresoService {
  private http = inject(HttpClient);
  private base = environment.apiUrl;

  obtenerHistorial(perfilAlumnoId: number): Observable<Historial> {
    return this.http.get<Historial>(`${this.base}/progreso/${perfilAlumnoId}`);
  }

  marcarGuiaRevisada(perfilAlumnoId: number, oaId: number): Observable<void> {
    return this.http.post<void>(`${this.base}/progreso/${perfilAlumnoId}/guias/${oaId}/revisada`, {});
  }
}
