import { HttpClient } from '@angular/common/http';
import { Injectable, inject } from '@angular/core';
import { Observable } from 'rxjs';
import { environment } from '../../environments/environment';

export interface ProgresoOnboarding {
  perfil_alumno_id: number;
  pasos: string[];
  pasos_completados: string[];
  completo: boolean;
}

@Injectable({ providedIn: 'root' })
export class OnboardingService {
  private http = inject(HttpClient);
  private base = environment.apiUrl;

  obtenerProgreso(perfilAlumnoId: number): Observable<ProgresoOnboarding> {
    return this.http.get<ProgresoOnboarding>(`${this.base}/onboarding/${perfilAlumnoId}`);
  }

  completarPaso(perfilAlumnoId: number, pasoId: string): Observable<ProgresoOnboarding> {
    return this.http.post<ProgresoOnboarding>(`${this.base}/onboarding/${perfilAlumnoId}/pasos/${pasoId}/completar`, {});
  }
}
