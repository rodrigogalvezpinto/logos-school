import { HttpInterceptorFn } from '@angular/common/http';
import { inject } from '@angular/core';
import { SesionAdminService } from './sesion-admin.service';
import { SesionService } from './sesion.service';

export const authInterceptor: HttpInterceptorFn = (req, next) => {
  // El token de Admin y el de Apoderado son tipos de JWT distintos (ver
  // ServicioTokenJWT.generar_admin en el backend) — se elige cuál adjuntar según el
  // endpoint, para que una sesión de Apoderado abierta en otra pestaña nunca se envíe por
  // error a /admin/* (y viceversa).
  const esAdmin = req.url.includes('/admin/');
  const token = esAdmin ? inject(SesionAdminService).token() : inject(SesionService).token();
  if (!token) return next(req);
  return next(
    req.clone({
      setHeaders: { Authorization: `Bearer ${token}` },
    })
  );
};
