import { HttpClient } from '@angular/common/http';
import { Injectable, inject } from '@angular/core';
import { Observable } from 'rxjs';
import { environment } from '../../environments/environment';

export interface Sugerencia {
  id: number;
  texto: string;
  fecha: string;
}

@Injectable({ providedIn: 'root' })
export class SugerenciasService {
  private http = inject(HttpClient);
  private base = environment.apiUrl;

  enviar(perfilAlumnoId: number, texto: string): Observable<Sugerencia> {
    return this.http.post<Sugerencia>(`${this.base}/sugerencias/${perfilAlumnoId}`, { texto });
  }

  listarMias(perfilAlumnoId: number): Observable<Sugerencia[]> {
    return this.http.get<Sugerencia[]>(`${this.base}/sugerencias/${perfilAlumnoId}`);
  }
}
