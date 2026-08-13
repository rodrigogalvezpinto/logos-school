import { inject } from '@angular/core';
import { CanActivateFn, Router } from '@angular/router';
import { SesionProfesorService } from './sesion-profesor.service';

export const profesorGuard: CanActivateFn = () => {
  const sesion = inject(SesionProfesorService);
  const router = inject(Router);
  if (sesion.token()) return true;
  return router.parseUrl('/profesor/login');
};
