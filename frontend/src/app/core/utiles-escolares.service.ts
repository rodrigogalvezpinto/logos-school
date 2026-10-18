import { HttpClient } from '@angular/common/http';
import { Injectable, inject } from '@angular/core';
import { Observable } from 'rxjs';
import { environment } from '../../environments/environment';

export interface UtilEscolar {
  id: number;
  nombre: string;
  cantidad: string | null;
  asignatura: string | null;
}

@Injectable({ providedIn: 'root' })
export class UtilesEscolaresService {
  private http = inject(HttpClient);
  private base = environment.apiUrl;

  listarPorNivel(nivelId: number): Observable<UtilEscolar[]> {
    return this.http.get<UtilEscolar[]>(`${this.base}/utiles-escolares/nivel/${nivelId}`);
  }
}
