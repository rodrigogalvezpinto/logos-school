import { HttpClient } from '@angular/common/http';
import { Injectable, inject } from '@angular/core';
import { Observable } from 'rxjs';
import { environment } from '../../environments/environment';

export interface CursoSeccion {
  id: number;
  nivel_id: number;
  nombre: string;
}

export interface Comunicado {
  id: number;
  titulo: string;
  cuerpo: string;
  fecha: string;
}

export interface NotaPorAsignatura {
  asignatura_id: number;
  asignatura_nombre: string;
  nota_practica: number | null;
  nota_simulacro: number | null;
}

export interface ProgresoAlumno {
  perfil_alumno_id: number;
  nombre: string;
  apellidos: string;
  notas_por_asignatura: NotaPorAsignatura[];
}

export interface ProgresoDeCurso {
  curso: CursoSeccion;
  alumnos: ProgresoAlumno[];
}

export interface MiCurso {
  nombre_curso: string;
  nombre_profesor: string;
  comunicados: Comunicado[];
}

export interface AlumnoEncontrado {
  perfil_alumno_id: number;
  nombre: string;
  apellidos: string;
  rut: string;
}

@Injectable({ providedIn: 'root' })
export class CursoSeccionService {
  private http = inject(HttpClient);
  private base = environment.apiUrl;

  crearCurso(nivelId: number, nombre: string): Observable<CursoSeccion> {
    return this.http.post<CursoSeccion>(`${this.base}/profesor/cursos`, { nivel_id: nivelId, nombre });
  }

  listarMisCursos(): Observable<CursoSeccion[]> {
    return this.http.get<CursoSeccion[]>(`${this.base}/profesor/cursos`);
  }

  buscarAlumnos(consulta: string): Observable<AlumnoEncontrado[]> {
    return this.http.get<AlumnoEncontrado[]>(`${this.base}/profesor/alumnos/buscar`, { params: { q: consulta } });
  }

  agregarAlumno(cursoId: number, perfilAlumnoId: number): Observable<void> {
    return this.http.post<void>(`${this.base}/profesor/cursos/${cursoId}/alumnos/${perfilAlumnoId}`, {});
  }

  quitarAlumno(cursoId: number, perfilAlumnoId: number): Observable<void> {
    return this.http.delete<void>(`${this.base}/profesor/cursos/${cursoId}/alumnos/${perfilAlumnoId}`);
  }

  publicarComunicado(cursoId: number, titulo: string, cuerpo: string): Observable<Comunicado> {
    return this.http.post<Comunicado>(`${this.base}/profesor/cursos/${cursoId}/comunicados`, { titulo, cuerpo });
  }

  obtenerProgreso(cursoId: number): Observable<ProgresoDeCurso> {
    return this.http.get<ProgresoDeCurso>(`${this.base}/profesor/cursos/${cursoId}/progreso`);
  }

  obtenerMiCurso(perfilAlumnoId: number): Observable<MiCurso | null> {
    return this.http.get<MiCurso | null>(`${this.base}/curso-seccion/mi-curso/${perfilAlumnoId}`);
  }
}
