import { HttpClient } from '@angular/common/http';
import { Injectable, inject } from '@angular/core';
import { Observable } from 'rxjs';
import { environment } from '../../environments/environment';

export interface LibroPlanLector {
  id: number;
  titulo: string;
  autor: string;
  editorial: string;
}

@Injectable({ providedIn: 'root' })
export class PlanLectorService {
  private http = inject(HttpClient);
  private base = environment.apiUrl;

  listarPorNivel(nivelId: number): Observable<LibroPlanLector[]> {
    return this.http.get<LibroPlanLector[]>(`${this.base}/plan-lector/nivel/${nivelId}`);
  }
}
