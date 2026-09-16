import { HttpClient } from '@angular/common/http';
import { Injectable, inject } from '@angular/core';
import { Observable } from 'rxjs';
import { environment } from '../../environments/environment';

export interface SesionEstudio {
  id: number;
  fecha_programada: string;
  asignatura_id: number;
  oa_ids: number[];
  incluye_prueba_unidad: boolean;
  minutos_estimados: number;
  cumplida: boolean;
  es_repaso: boolean;
  atrasada: boolean;
}

export interface PlanDeEstudio {
  id: number;
  dias_por_semana: number;
  dias_elegidos: string[];
  fecha_inicio: string;
  fecha_objetivo: string | null;
  sesiones: SesionEstudio[];
}

@Injectable({ providedIn: 'root' })
export class PlanEstudioService {
  private http = inject(HttpClient);
  private base = environment.apiUrl;

  crearPlan(
    perfilAlumnoId: number, diasPorSemana: number, diasElegidos: string[], fechaObjetivo: string | null
  ): Observable<PlanDeEstudio> {
    return this.http.post<PlanDeEstudio>(`${this.base}/plan-estudio/${perfilAlumnoId}`, {
      dias_por_semana: diasPorSemana, dias_elegidos: diasElegidos, fecha_objetivo: fechaObjetivo,
    });
  }

  obtenerPlan(perfilAlumnoId: number): Observable<PlanDeEstudio> {
    return this.http.get<PlanDeEstudio>(`${this.base}/plan-estudio/${perfilAlumnoId}`);
  }

  agregarRepaso(perfilAlumnoId: number, asignaturaId: number, oaIds: number[]): Observable<SesionEstudio> {
    return this.http.post<SesionEstudio>(`${this.base}/plan-estudio/${perfilAlumnoId}/repaso`, {
      asignatura_id: asignaturaId, oa_ids: oaIds,
    });
  }
}
