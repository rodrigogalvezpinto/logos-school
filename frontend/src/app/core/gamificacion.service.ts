import { HttpClient } from '@angular/common/http';
import { Injectable, inject } from '@angular/core';
import { Observable } from 'rxjs';
import { environment } from '../../environments/environment';

export interface Logro {
  id: string;
  nombre: string;
  descripcion: string;
  icono: string;
  categoria: 'constancia' | 'contenido' | 'evaluaciones' | 'nivel';
  desbloqueado: boolean;
}

export interface PerfilGamificacion {
  perfil_alumno_id: number;
  xp: number;
  nivel: number;
  avatar_id: string;
  xp_para_siguiente_nivel: number;
  avatares_disponibles: string[];
  racha_dias_actual: number;
  racha_dias_maxima: number;
  guias_revisadas_total: number;
  evaluaciones_entregadas_total: number;
  tiempo_evaluando_total_seg: number;
  logros: Logro[];
}

@Injectable({ providedIn: 'root' })
export class GamificacionService {
  private http = inject(HttpClient);
  private base = environment.apiUrl;

  obtenerPerfil(perfilAlumnoId: number): Observable<PerfilGamificacion> {
    return this.http.get<PerfilGamificacion>(`${this.base}/gamificacion/${perfilAlumnoId}`);
  }

  cambiarAvatar(perfilAlumnoId: number, avatarId: string): Observable<PerfilGamificacion> {
    return this.http.patch<PerfilGamificacion>(`${this.base}/gamificacion/${perfilAlumnoId}/avatar`, {
      avatar_id: avatarId,
    });
  }
}
