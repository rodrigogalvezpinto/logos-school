import { HttpInterceptorFn } from '@angular/common/http';
import { inject } from '@angular/core';
import { SesionAdminService } from './sesion-admin.service';
import { SesionProfesorService } from './sesion-profesor.service';
import { SesionService } from './sesion.service';

export const authInterceptor: HttpInterceptorFn = (req, next) => {
  // El token de Admin, el de Profesor y el de Apoderado son tipos de JWT distintos (ver
  // ServicioTokenJWT.generar_admin/generar_profesor en el backend) — se elige cuál
  // adjuntar según el endpoint, para que una sesión abierta en otra pestaña nunca se
  // envíe por error al panel equivocado. `/curso-seccion/*` es la excepción: lo consume
  // el Alumno/Apoderado, no el Profesor, así que usa el token de Apoderado normal.
  const esAdmin = req.url.includes('/admin/');
  const esProfesor = req.url.includes('/profesor/');
  const token = esAdmin
    ? inject(SesionAdminService).token()
    : esProfesor
      ? inject(SesionProfesorService).token()
      : inject(SesionService).token();
  if (!token) return next(req);
  return next(
    req.clone({
      setHeaders: { Authorization: `Bearer ${token}` },
    })
  );
};
