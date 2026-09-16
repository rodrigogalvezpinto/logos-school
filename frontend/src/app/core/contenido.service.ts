import { HttpClient } from '@angular/common/http';
import { Injectable, inject } from '@angular/core';
import { Observable } from 'rxjs';
import { environment } from '../../environments/environment';

export interface NivelRespuesta {
  id: number;
  nombre: string;
  regimen: string;
  num_preguntas_examen: number;
  duracion_examen_min: number;
  orden: number | null;
}

export interface AsignaturaRespuesta {
  id: number;
  nombre: string;
}

export interface ObjetivoRespuesta {
  id: number;
  codigo_oficial: string;
  descripcion: string;
  eje_tematico: string | null;
  contenido_guia: string;
}

@Injectable({ providedIn: 'root' })
export class ContenidoService {
  private http = inject(HttpClient);
  private base = environment.apiUrl;

  listarNiveles(): Observable<NivelRespuesta[]> {
    return this.http.get<NivelRespuesta[]>(`${this.base}/contenido/niveles`);
  }

  listarAsignaturas(nivelId: number): Observable<AsignaturaRespuesta[]> {
    return this.http.get<AsignaturaRespuesta[]>(`${this.base}/contenido/niveles/${nivelId}/asignaturas`);
  }

  listarObjetivos(asignaturaId: number): Observable<ObjetivoRespuesta[]> {
    return this.http.get<ObjetivoRespuesta[]>(`${this.base}/contenido/asignaturas/${asignaturaId}/objetivos`);
  }

  obtenerObjetivo(oaId: number): Observable<ObjetivoRespuesta> {
    return this.http.get<ObjetivoRespuesta>(`${this.base}/contenido/objetivos/${oaId}`);
  }
}
