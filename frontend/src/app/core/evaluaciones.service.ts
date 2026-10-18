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
  intentos_entregados: number;
  ultima_nota: number | null;
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

export interface DetallePregunta {
  pregunta_id: number;
  enunciado: string;
  tipo: string;
  opciones: string[] | null;
  respuesta_alumno: string | null;
  respuesta_correcta: string | null;
  es_correcta: boolean | null;
}

@Injectable({ providedIn: 'root' })
export class EvaluacionesService {
  private http = inject(HttpClient);
  private base = environment.apiUrl;

  obtenerAutoevaluacion(oaId: number): Observable<PreguntaAutoevaluacion[]> {
    return this.http.get<PreguntaAutoevaluacion[]>(`${this.base}/evaluaciones/autoevaluacion/${oaId}`);
  }

  listarConjuntosDeAsignatura(asignaturaId: number, perfilAlumnoId?: number): Observable<ConjuntoResumen[]> {
    return this.http.get<ConjuntoResumen[]>(`${this.base}/evaluaciones/conjuntos/asignatura/${asignaturaId}`, {
      params: perfilAlumnoId ? { perfil_alumno_id: perfilAlumnoId } : {},
    });
  }

  listarConjuntosDeNivel(nivelId: number, perfilAlumnoId?: number): Observable<ConjuntoResumen[]> {
    return this.http.get<ConjuntoResumen[]>(`${this.base}/evaluaciones/conjuntos/nivel/${nivelId}`, {
      params: perfilAlumnoId ? { perfil_alumno_id: perfilAlumnoId } : {},
    });
  }

  obtenerConjunto(conjuntoId: number, perfilAlumnoId?: number): Observable<ConjuntoDetalle> {
    return this.http.get<ConjuntoDetalle>(`${this.base}/evaluaciones/conjuntos/${conjuntoId}`, {
      params: perfilAlumnoId ? { perfil_alumno_id: perfilAlumnoId } : {},
    });
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

  obtenerDetalle(intentoId: number): Observable<DetallePregunta[]> {
    return this.http.get<DetallePregunta[]>(`${this.base}/evaluaciones/intentos/${intentoId}/detalle`);
  }

  reportarErrorPregunta(preguntaId: number, perfilAlumnoId: number, comentario: string): Observable<unknown> {
    return this.http.post(`${this.base}/evaluaciones/preguntas/${preguntaId}/reportar-error`, {
      perfil_alumno_id: perfilAlumnoId,
      comentario,
    });
  }

  generarSimulacroParcial(asignaturaId: number, perfilAlumnoId: number): Observable<IntentoEvaluacion> {
    return this.http.post<IntentoEvaluacion>(`${this.base}/evaluaciones/simulacro-parcial/${asignaturaId}`, {
      perfil_alumno_id: perfilAlumnoId,
    });
  }
}
