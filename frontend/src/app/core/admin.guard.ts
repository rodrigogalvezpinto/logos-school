import { inject } from '@angular/core';
import { CanActivateFn, Router } from '@angular/router';
import { SesionAdminService } from './sesion-admin.service';

export const adminGuard: CanActivateFn = () => {
  const sesion = inject(SesionAdminService);
  const router = inject(Router);
  if (sesion.token()) return true;
  return router.parseUrl('/admin/login');
};
