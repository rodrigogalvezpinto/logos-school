import { HttpClient } from '@angular/common/http';
import { Injectable, inject } from '@angular/core';
import { Observable } from 'rxjs';
import { environment } from '../../environments/environment';

export interface PreguntaAutoevaluacion {
  id: number;
  tipo: string;
  enunciado: string;
  opciones: string[] | null;
  respuesta_correcta: string;
  retroalimentacion: string;
}

export interface PreguntaSinRespuesta {
  id: number;
  tipo: string;
  enunciado: string;
  opciones: string[] | null;
}

export interface ConjuntoResumen {
  id: number;
  tipo: 'prueba_unidad' | 'examen_simulacro';
  nombre: string;
  forma: string | null;
  tiempo_sugerido_min: number | null;
  num_preguntas: number;
}

export interface ConjuntoDetalle extends ConjuntoResumen {
  preguntas: PreguntaSinRespuesta[];
}

export interface IntentoEvaluacion {
  id: number;
  conjunto_evaluacion_id: number;
  fecha_inicio: string;
  fecha_termino: string | null;
  respuestas: Record<string, string>;
  puntaje: number | null;
  nota: number | null;
}

@Injectable({ providedIn: 'root' })
export class EvaluacionesService {
  private http = inject(HttpClient);
  private base = environment.apiUrl;

  obtenerAutoevaluacion(oaId: number): Observable<PreguntaAutoevaluacion[]> {
    return this.http.get<PreguntaAutoevaluacion[]>(`${this.base}/evaluaciones/autoevaluacion/${oaId}`);
  }

  listarConjuntosDeAsignatura(asignaturaId: number): Observable<ConjuntoResumen[]> {
    return this.http.get<ConjuntoResumen[]>(`${this.base}/evaluaciones/conjuntos/asignatura/${asignaturaId}`);
  }

  listarConjuntosDeNivel(nivelId: number): Observable<ConjuntoResumen[]> {
    return this.http.get<ConjuntoResumen[]>(`${this.base}/evaluaciones/conjuntos/nivel/${nivelId}`);
  }

  obtenerConjunto(conjuntoId: number): Observable<ConjuntoDetalle> {
    return this.http.get<ConjuntoDetalle>(`${this.base}/evaluaciones/conjuntos/${conjuntoId}`);
  }

  iniciarIntento(perfilAlumnoId: number, conjuntoEvaluacionId: number): Observable<IntentoEvaluacion> {
    return this.http.post<IntentoEvaluacion>(`${this.base}/evaluaciones/intentos`, {
      perfil_alumno_id: perfilAlumnoId,
      conjunto_evaluacion_id: conjuntoEvaluacionId,
    });
  }

  responder(intentoId: number, preguntaId: number, respuesta: string): Observable<IntentoEvaluacion> {
    return this.http.patch<IntentoEvaluacion>(`${this.base}/evaluaciones/intentos/${intentoId}/responder`, {
      pregunta_id: preguntaId,
      respuesta,
    });
  }

  entregar(intentoId: number): Observable<IntentoEvaluacion> {
    return this.http.post<IntentoEvaluacion>(`${this.base}/evaluaciones/intentos/${intentoId}/entregar`, {});
  }
}
