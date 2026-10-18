import { HttpClient } from '@angular/common/http';
import { Injectable, inject } from '@angular/core';
import { Observable } from 'rxjs';
import { environment } from '../../environments/environment';

export interface EstimacionAsignatura {
  asignatura_id: number;
  asignatura_nombre: string;
  nota_estimada: number | null;
  confianza: 'sin_datos' | 'baja' | 'media' | 'alta';
  cobertura_pct: number;
}

export interface EstimacionExamen {
  nota_general_estimada: number | null;
  confianza_general: 'sin_datos' | 'baja' | 'media' | 'alta';
  por_asignatura: EstimacionAsignatura[];
}

export interface AlertaRitmoEstudio {
  tiene_alerta: boolean;
  mensaje: string;
  dias_restantes: number;
  oa_pendientes: number;
  ritmo_actual_oa_por_dia: number;
  ritmo_necesario_oa_por_dia: number;
}

export interface CeldaMapaCalor {
  asignatura_id: number;
  asignatura_nombre: string;
  eje_tematico: string;
  pct_correctas: number;
  total_preguntas: number;
}

export interface ObservacionHorario {
  tiene_observacion: boolean;
  mensaje: string;
  sesiones_tarde: number;
  sesiones_analizadas: number;
}

export type EtapaJardin = 'semilla' | 'brote' | 'crecimiento' | 'floreciendo' | 'flor_completa';

export interface SemanaJardin {
  semana_inicio: string;
  dias_activos: number;
  etapa: EtapaJardin;
}

@Injectable({ providedIn: 'root' })
export class PrediccionService {
  private http = inject(HttpClient);
  private base = environment.apiUrl;

  obtenerNotaEstimada(perfilAlumnoId: number, nivelId: number): Observable<EstimacionExamen> {
    return this.http.get<EstimacionExamen>(`${this.base}/prediccion/${perfilAlumnoId}/nota-estimada`, {
      params: { nivel_id: nivelId },
    });
  }

  obtenerAlertaDeRitmo(perfilAlumnoId: number): Observable<AlertaRitmoEstudio | null> {
    return this.http.get<AlertaRitmoEstudio | null>(`${this.base}/prediccion/${perfilAlumnoId}/ritmo-de-estudio`);
  }

  obtenerMapaDeCalor(perfilAlumnoId: number): Observable<CeldaMapaCalor[]> {
    return this.http.get<CeldaMapaCalor[]>(`${this.base}/prediccion/${perfilAlumnoId}/mapa-calor`);
  }

  obtenerObservacionDeHorario(perfilAlumnoId: number): Observable<ObservacionHorario | null> {
    return this.http.get<ObservacionHorario | null>(`${this.base}/prediccion/${perfilAlumnoId}/horario-de-estudio`);
  }

  obtenerJardinSemanal(perfilAlumnoId: number): Observable<SemanaJardin[]> {
    return this.http.get<SemanaJardin[]>(`${this.base}/prediccion/${perfilAlumnoId}/jardin-semanal`);
  }
}
