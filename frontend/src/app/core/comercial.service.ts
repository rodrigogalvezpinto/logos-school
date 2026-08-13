import { HttpClient } from '@angular/common/http';
import { Injectable, inject } from '@angular/core';
import { Observable } from 'rxjs';
import { environment } from '../../environments/environment';

export interface Plan {
  id: number;
  nombre: string;
  nivel_de_acceso: string;
  precio_clp: number;
  activo: boolean;
}

export interface Descuento {
  id: number;
  codigo: string;
  tipo: 'porcentaje' | 'monto_fijo';
  valor: number;
  fecha_vencimiento: string | null;
  usos_maximos: number | null;
  usos_actuales: number;
  vigente: boolean;
}

export interface AlumnoEncontrado {
  perfil_alumno_id: number;
  nombre: string;
  apellidos: string;
  rut: string;
  email_apoderado: string;
}

export interface SuscripcionesPorPlan {
  plan_id: number;
  plan_nombre: string;
  activas: number;
}

export interface Metricas {
  apoderados_registrados: number;
  alumnos_registrados: number;
  suscripciones_por_plan: SuscripcionesPorPlan[];
  ingresos_mes_aprox_clp: number;
}

@Injectable({ providedIn: 'root' })
export class ComercialService {
  private http = inject(HttpClient);
  private base = environment.apiUrl;

  listarPlanes(): Observable<Plan[]> {
    return this.http.get<Plan[]>(`${this.base}/admin/planes`);
  }

  crearPlan(nombre: string, nivelDeAcceso: string, precioClp: number): Observable<Plan> {
    return this.http.post<Plan>(`${this.base}/admin/planes`, {
      nombre, nivel_de_acceso: nivelDeAcceso, precio_clp: precioClp,
    });
  }

  editarPlan(id: number, nombre: string, nivelDeAcceso: string, precioClp: number): Observable<Plan> {
    return this.http.patch<Plan>(`${this.base}/admin/planes/${id}`, {
      nombre, nivel_de_acceso: nivelDeAcceso, precio_clp: precioClp,
    });
  }

  cambiarEstadoPlan(id: number, activar: boolean): Observable<Plan> {
    return this.http.post<Plan>(`${this.base}/admin/planes/${id}/${activar ? 'activar' : 'desactivar'}`, {});
  }

  listarDescuentos(): Observable<Descuento[]> {
    return this.http.get<Descuento[]>(`${this.base}/admin/descuentos`);
  }

  crearDescuento(
    codigo: string, tipo: string, valor: number, fechaVencimiento: string | null, usosMaximos: number | null
  ): Observable<Descuento> {
    return this.http.post<Descuento>(`${this.base}/admin/descuentos`, {
      codigo, tipo, valor, fecha_vencimiento: fechaVencimiento, usos_maximos: usosMaximos,
    });
  }

  desactivarDescuento(id: number): Observable<Descuento> {
    return this.http.post<Descuento>(`${this.base}/admin/descuentos/${id}/desactivar`, {});
  }

  buscarAlumnos(consulta: string): Observable<AlumnoEncontrado[]> {
    return this.http.get<AlumnoEncontrado[]>(`${this.base}/admin/alumnos/buscar`, { params: { q: consulta } });
  }

  asignarCortesia(perfilAlumnoId: number, planId: number): Observable<void> {
    return this.http.post<void>(`${this.base}/admin/alumnos/${perfilAlumnoId}/cortesia`, { plan_id: planId });
  }

  obtenerMetricas(): Observable<Metricas> {
    return this.http.get<Metricas>(`${this.base}/admin/metricas`);
  }
}
